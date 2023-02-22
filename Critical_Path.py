# Critical Path.py
# A test to compute this stuff easier
# Martin Borgén
# 2023-02-19

from typing import List
from collections import deque

class Task:
    def __init__(self, label: str, dependencies=[], dur=None):
        # Initialize the label
        # Initialize fields but leave them blank for now
        self.label: str = label
        if isinstance(dur, str):
            try:
                self.duration = int(dur)
            except ValueError:
                try:
                    self.duration = float(dur)
                except ValueError:
                    raise ValueError
        else:
            self.duration = dur
        self.earlyStart = None
        self.earlyFinish = None
        self.lateStart = None
        self.lateFinish = None
        self.float = None
        self.dependencies: List[Task] = dependencies
        self.dependsOnThis: List[Task] = []
        self.distanceFromStart = 0
        self.distanceFromEnd = 0 # unused
    
    def calculateFloat(self):
        self.float = self.lateFinish - self.earlyFinish
    
    def calculateEarlies(self): # To be run in forward pass
        if not self.dependencies:
            self.earlyStart = 0
        else:
            self.earlyStart = max([a.earlyFinish for a in self.dependencies])
        self.earlyFinish = self.earlyStart + self.duration

    def calculateLates(self):   # To be run in backwards pass
        if not self.dependsOnThis:
            self.lateFinish = self.earlyFinish
        else:
            self.lateFinish = min([a.lateStart for a in self.dependsOnThis])
        self.lateStart = self.lateFinish - self.duration

    def __str__(self) -> str:
        return self.label
    
    def cliRep(self):
        return (f"="*28 +
                f"\n|{round(self.earlyStart, 2):^8}|{round(self.duration, 2):^8}|{round(self.earlyFinish, 2):^8}|\n"+
                f"-"*28 +
                f"\n|{'':^8}|{self.label:^8}|{'':^8}|\n"+
                f"-"*28 +
                f"\n|{round(self.lateStart, 2):^8}|{round(self.float, 2):^8}|{round(self.lateFinish, 2):^8}|\n"+
                f"="*28 + "\n")

class Path: # This might be re-made into a subclass of a list, come to think of it
    def __init__(self):
        self.totTime = 0
        self.path = []
        self.modified = False
        
    def append(self, task: Task):
        self.path.append(task)
    
    def copy(self):
        out = Path()
        out.totTime = self.totTime
        out.path = self.path.copy()
        return out
    
    def calcTotTime(self):
        tot = 0
        for task in self.path:
            tot += task.duration
        self.totTime = tot

    def __len__(self):
        return len(self.path)

class TaskTree:
    def __init__(self):
        # self.start: Task = None
        self.end: Task = None
        self.tasks: dict[str:Task] = {}     # tasks is a dict where each label correstponds to a Task instnace
        self.noDeps: List[Task] = []    # a list of tasks with no dependencies, useful for finding starting points
        self.paths: List[Path] = []     # This list will hold all possible paths.
        self.criticalPaths = [Path()]      # dummy path so comparisions will return higher

    def compute(self): # The compute method manages the calculations in proper order
        self.mapDependencies()
        self.generatePaths()
        self.updateEarlyLates()

    def createTask(self, label: str, dependencies: List[str]=[], dur=None): # Dependencies must be string labels, hence one has to add in chronological order?
        depTasks = []
        if len(dependencies) > 0 and dependencies[0] == '':
            pass
        elif len(dependencies) > 0 and isinstance(dependencies[0], str): # if we have dependencies and it's strings, convert to list of tasks
            for depLabel in dependencies:
                depTasks.append(self.tasks[depLabel])
        else:
            depTasks = dependencies

        task = Task(label, depTasks, dur)
        self.tasks[task.label] = task
        
        if len(task.dependencies) == 0:
            self.noDeps.append(task)
        
    def mapDependencies(self):  # Maps dependencies both ways
        for task in self.tasks.values():
            for dep in task.dependencies:
                try:
                    depTask = self.tasks[dep.label]
                except KeyError:
                    print(f"Error, dependency {dep.label} of task {task.label} not in WBS!")
                else:
                    depTask.dependsOnThis.append(task)

    def updateEarlyLates(self): # updates the early and late finishes, as well as float for each task
        # pre-setup
        taskTiers = deque()     # TaskTiers will be a deque of deques, where each subdeque is a generation, i.e. a distance from start
        for _ in range(self.end.distanceFromStart + 1):
            taskTiers.append(deque())
        for task in self.tasks.values():
            taskTiers[task.distanceFromStart].append(task)
            task.distanceFromEnd = self.end.distanceFromStart - task.distanceFromStart

        # Forward pass
        for tier in taskTiers:
            for task in tier:
                task.calculateEarlies()
        taskTiers.reverse()
        # Backwards pass
        for tier in taskTiers:
            for task in tier:
                task.calculateLates()

        # fill in float
        for task in self.tasks.values():
            task.calculateFloat()
        
    def generatePaths(self):    # The beginning starts the recursive function. Then the critical path(s) is/are identified
        for current in self.noDeps:
            self._pathRecFun(current, Path())
            
    def _pathRecFun(self, current: Task, pathSoFar: Path):    # Recursively goes through the graph, clones the current path if it finds a fork.
        if current.distanceFromStart < len(pathSoFar): # if statement, so that we only get the furthest distance
            current.distanceFromStart = len(pathSoFar)
        pathSoFar.append(current)

        if not current.dependsOnThis:
            # If we're at the end of the tree
            self.paths.append(pathSoFar)
            pathSoFar.calcTotTime()
            self.end = current # This assumes only one end task
            current.distanceFromEnd = 0

            # check if it's a critical path
            if pathSoFar.totTime > self.criticalPaths[0].totTime:
                self.criticalPaths = [pathSoFar]
            elif pathSoFar.totTime == self.criticalPaths[0].totTime:
                self.criticalPaths.append(pathSoFar)
            return
        
        # First, copy the necessary ammount of pathSoFar. We need one less copy than we have forks, as we already have one path
        # We're copying first to avoid modifying pathSoFar until after we've copied it.
        forks: List[Path] = []
        for i, _ in enumerate(current.dependsOnThis):  # This could be a range(len(current.dependsOnThis) - 1)
            if i == len(current.dependsOnThis) - 1:
                break
            forks.append(pathSoFar.copy())

        # Then recursively continue. 
        for i, fork  in enumerate(forks):
            self._pathRecFun(current.dependsOnThis[i], fork)
        self._pathRecFun(current.dependsOnThis[-1], pathSoFar)

    def getTask(self, taskLabel) -> Task:
        return self.tasks[taskLabel]

    def printTree(self):    # basic printree funciton, used for debugging currently
        for task in self.tasks.values():
            print(f"task {task.label}, that depends on {task.dependencies}")

if __name__ == '__main__':
    pass

# Critical Path.py
# A test to compute this stuff easier

from typing import List
from collections import deque

class Task:
    def __init__(self, label: str, dependencies=[], dur=None):
        # Initialize the label
        # Initialize fields but leave them blank for now
        self.label: str = label
        self.duration = dur
        self.earlyStart = None
        self.earlyFinish = None
        self.lateStart = None
        self.lateFinish = None
        self.float = None
        self.dependencies: List[Task] = dependencies
        self.dependsOnThis: List[Task] = []
        self.distanceFromStart = None
        self.distanceFromEnd = None
    
    def calculateFloat(self):
        self.float = self.earlyStart - self.lateStart
    
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

class Path: # This might be re-made into a subclass of a list, come to think of it
    def __init__(self):
        self.totTime = None
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

class TaskTree:
    def __init__(self):
        self.start: Task = None
        self.end: Task = None
        self.tasks: dict[str:Task] = {}     # tasks is a dict where each label correstponds to a Task instnace
        self.noDeps: List[Task] = []    # a list of tasks with no dependencies, useful for finding starting points
        self.paths: List[Path] = []     # This list will hold all possible paths.

    def createTask(self, label: str, dependencies: List[str]=[], dur=None): # Dependencies must be string labels, hence one has to add in chronological order?
        if len(dependencies) > 0 and isinstance(dependencies[0], str): # if we have dependencies and it's strings, convert to list of tasks
            depTasks = []
            for i in dependencies:
                depTasks.append(self.tasks[i])
        else:
            depTasks = dependencies

        task = Task(label, depTasks, dur=dur)
        self.tasks[task.label] = task
        
        if len(dependencies) == 0:
            self.noDeps.append(task)
        
    def mapDependencies(self):  # so far, this maps the dependencies both ways, but I think it might as well do the early/late start/finishes too?
        for task in self.tasks.values():
            for dep in task.dependencies:
                try:
                    depTask = self.tasks[dep.label]
                except KeyError:
                    print(f"Error, dependency {dep.label} of task {task.label} not in WBS!")
                else:
                    depTask.dependsOnThis.append(task)

    def updateEarlyLates(self):
        # Forward pass
        current = self.start
        current.calculateEarlies()
        
        
        # Backwards pass
        

        # fill in float
        for task in self.tasks.values():
            task.calculateFloat()
        
    def generatePaths(self):    # this is essentially a bootstrapper to the recursive function. At the moment, it must be run only once I think
        current = self.start
        self._pathRecFun(current, Path())
            
    def _pathRecFun(self, current: Task, pathSoFar: Path):    # Recursively goes through the graph, clones the current path if it finds a fork.
        pathSoFar.append(current)
        if not current.dependsOnThis:
            # If we're at the end of the tree
            self.paths.append(pathSoFar)
            pathSoFar.calcTotTime()
            self.end = current # This assumes only one end task
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

    def printTree(self):    # basic printree funciton, used for debugging currently
        for task in self.tasks.values():
            print(f"task {task.label}, that depends on {task.dependencies}")
    
def pathPrinter(path):  # used for debugging mostly
    for i in path:
        print(i.label, end="")
    print()

if __name__ == '__main__':
    tree = TaskTree()
    tree.createTask('A', dur=3)
    tree.createTask('B', ['A'], dur=2)
    tree.createTask('D', ['B'], dur=2)
    tree.createTask('C', ['A'], dur=3)
    tree.createTask('P', ['B'], dur=2)
    tree.createTask('Q', ['A'], dur=1)
    tree.createTask('R', ['Q'], dur=1)
    tree.createTask('E', ['D', 'C', 'P', 'R'], dur=5)

    tree.mapDependencies()
    tree.printTree()

    tree.start = tree.tasks['A']
    tree.generatePaths()
    # tree.updateEarlyLates()
    print("total paths found:", len(tree.paths))

    for path in tree.paths:
        print(f"one path with total time {path.totTime} is:")
        for task in path.path:
            print(task.label)
        print()
    

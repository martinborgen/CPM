# Critical Path.py
# A test to compute this stuff easier

from typing import List
from collections import deque

class Task:
    def __init__(self, label: str, dependencies=[]):
        # Initialize the label
        # Initialize fields but leave them blank for now
        self.label: str = label
        self.duration = None
        self.earliestStart = None
        self.earleistFinish = None
        self.latestStart = None
        self.latestFinish = None
        self.float = None
        self.dependencies: List[Task] = dependencies
        self.dependsOnThis: List[Task] = []
    
    def calculateFloat(self):
        self.float = self.earliestStart - self.latestStart

    def __str__(self) -> str:
        return self.label

class Path:
    def __init__(self):
        self.totTime = None
        self.path = deque()
        self.modified = False
        
    def append(self, task: Task):
        self.path.append(task)
        self.modified = True

    def push(self, task: Task):
        self.path.appendleft(task)
        self.modified = True

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
        self.tasks = {}     # tasks is a dict where each label correstponds to a Task instnace
        self.noDeps = []    # a list of tasks with no dependencies 
        self.paths = []

    def createTask(self, label: str, dependencies: List[str]=[]): # Dependencies must be string labels, hence one has to add in chronological order?
        if len(dependencies) > 0 and isinstance(dependencies[0], str): # if we have dependencies and it's strings, convert to list of tasks
            depTasks = []
            for i in dependencies:
                depTasks.append(self.tasks[i])
        else:
            depTasks = dependencies

        task = Task(label, depTasks)
        self.tasks[task.label] = task
        
        if len(dependencies) == 0:
            self.noDeps.append(task)
        

    def mapDependencies(self):
        for task in self.tasks.values():
            for dep in task.dependencies:
                try:
                    depTask = self.tasks[dep.label]
                except KeyError:
                    print(f"Error, dependency {dep.label} of task {task.label} not in WBS!")
                else:
                    depTask.dependsOnThis.append(task)

    def generatePaths(self):
        current = self.start
        while current.dependsOnThis:
            pass
            
    def __generatePaths_RecursiveFun(self, current):
        pass 

    def printTree(self):
        for task in self.tasks.values():
            print(f"task {task.label}, that depends on {task.dependencies}")
    
if __name__ == '__main__':
    tree = TaskTree()
    tree.createTask('A')
    tree.createTask('B', ['A'])
    tree.createTask('D', ['B'])
    tree.createTask('C', ['A'])
    tree.createTask('E', ['D', 'C'])
    tree.mapDependencies()
    tree.printTree()
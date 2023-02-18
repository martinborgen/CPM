# Critical Path.py
# A test to compute this stuff easier

from typing import List

class Task:
    def __init__(self, label: str, dependencies=[]):
        # Initialize the label
        # Initialize fields but leave them blank for now
        self.label = label
        self.earliestStart = None
        self.earleistFinish = None
        self.latestStart = None
        self.latestFinish = None
        self.float = None
        self.dependencies = dependencies
        self.dependsOnThis = []
    
    def calculateFloat(self):
        self.float = self.earliestStart - self.latestStart

class TaskTree:
    def __init__(self):
        self.head = None
        self.tasks = []
        self.noDeps = [] # a list of tasks with no dependencies 
        self.paths = []

    def createTask(self, label: str, dependencies=[]):
        task = Task(label, dependencies)
        self.tasks.append(task)
        if len(dependencies) == 0:
            self.noDeps.append(task)

    def generatePaths(self):

        for task in self.tasks:
            for dep in task.dependencies:
                pass



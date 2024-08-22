# critical_path_main
# Martin Borgén
# 2023-02-19

# from Critical_Path import TaskTree
import Critical_Path
import csv_module
from exceptions import CSVseparatorError

def load_csv(sep=",", userInput=""):
    
    while True:
        userInput = input("Enter a csv-filename. (Q to cancel)\n")
        if userInput == "Q" or userInput == "q":
            return
        
        try:
            lines = csv_module.csv_reader(userInput, sep=sep)
            break
        except NameError:
            print("error, no such file found!")
            continue
        except CSVseparatorError:
            print("Error, seprator does not yeld three fields or is empty!")
            sep = input("Enter new separator character: ")
            continue

    tree = Critical_Path.TaskTree()
    for line in lines:
        tree.createTask(line[0], line[2:], line[1])
    tree.compute()
    return tree

def print_crit_path(tree):
    print(f"Total ammount of paths found: {len(tree.paths)}")
    for path in tree.criticalPaths:
        print(f"criticalPaths path with total time {path.totTime} is:")
        for task in path.path:
            print(task.cliRep())
        print()

def main():
    tree = None
    sep = ","
    while True:
        userInput = input("Input L to load, input Q to quit, input CP for critical path, input T to view task, EE to print early start/finishes\n").upper()
        if userInput == 'L':
            newSep = input("Current sep is {}, press return if OK, otherwise enter separator token and press return")
            if len(newSep) > 0:
                sep = newSep
            tree = load_csv(sep=sep)
        elif userInput == 'Q':
            break
        elif userInput == 'CP':
            if tree:
                print_crit_path(tree)
            else:
                print("Error, no tree loaded")
        elif userInput == 'T':
            if tree:
                while True:
                    userInput = input("Enter the label of task: (C to cancel)\n")
                    if userInput.upper() == 'C':
                        break
                    
                    try:
                        print(tree.getTask(userInput).cliRep())
                    except KeyError:
                        print("Error, no such task in WBS!")
            else:
                print("Error, no tree loaded")
        elif userInput == 'EE':
            for task in tree.tasks.values():
                print(f"{task.label}, {task.earlyStart}, {task.earlyFinish}")

if __name__ == '__main__:
    main()

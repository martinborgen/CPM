# critical_path_main
# Martin Borgén
# 2023-02-19

# from Critical_Path import TaskTree
import Critical_Path
import csv_module

def load_csv(userInput=""):
    
    while not userInput:
        userInput = input("Enter a csv-filename. (Q to cancel)\n")
        if userInput == "Q" or userInput == "q":
            return
        
        try:
            lines = csv_module.csv_reader(userInput)
            break
        except NameError:
            print("error, no such file found!")
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
    while True:
        userInput = input("Input L to load, input Q to quit, input CP for critical path, input T to view task, EE to print early start/finishes\n").upper()
        if userInput == 'L':
            tree = load_csv()
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

main()
# critical_path_main
# Martin Borgén
# 2023-02-19

# from Critical_Path import TaskTree
import Critical_Path
import csv_module

def main():
    userInput = ""
    while True:
        userInput = input("Enter a csv-filename: \n")
        if userInput == "Q" or userInput == "q":
            quit()
        
        try:
            lines = csv_module.csv_reader(userInput)
            break
        except:
            print("error, no such file found!")
            continue

    tree = Critical_Path.TaskTree()
    for line in lines:
        tree.createTask(line[0], line[2].split(','), line[1])
    # tree.setStart('A')
    tree.compute()
    for path in tree.criticalPaths:
        print(f"criticalPaths path with total time {path.totTime} is:")
        for task in path.path:
            print(task.cliRep())
        print()

main()
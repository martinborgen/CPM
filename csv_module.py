# Reader of csv -files, for critical path program
# Martin Borgén
# 2023-02-19

def csv_reader(filename: str):
    # assume task,dur,dep -format for now
    file = open(filename)
    lines = file.readlines()
    out = []
    for line in lines:
        splitted = line.split(',', 2)
        newLine = []
        for field in splitted:
            newLine.append(field.strip())
        out.append(newLine)
    
    return out


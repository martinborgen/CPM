# Reader of csv -files, for critical path program
# Martin Borgén
# 2023-02-19

from exceptions import CSVseparatorError

def csv_reader(filename: str, sep=',', depSep=','):
    # assume task,dur,dep -format for now. Dep is N ammounts of dependencies
    if (len(sep) == 0):
        raise CSVseparatorError

    file = open(filename)
    lines = file.readlines()
    out = []
    for line in lines:
        splitted = line.split(sep, 2)

        if len(splitted) != 3:
            raise CSVseparatorError

        newLine = []
        newLine += splitted[0:2]
        deps = splitted[2]
        depsSplitted = []
        for dep in deps.split(depSep):
            depsSplitted.append(dep.strip())
        newLine += depsSplitted
        out.append(newLine)
    
    return out


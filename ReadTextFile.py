def ReadTextFile(strFile):
    listLine = []
    with open(strFile) as f:
        for line in f:
            listLine.append(line.strip())
    return listLine
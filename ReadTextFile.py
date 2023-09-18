from Assembler import Assembler
listRiscV = ["add", "nand", "lw", "sw", "beq", "jalr", "halt", "noop" ]

def ReadTextFile(strFile):
    listLine = []
    with open(strFile) as f:
        for line in f:
            listLine.append(ScanToInstruction(line.strip().split("#")))
    return listLine

def ScanToInstruction(list):
    instruction = []
    spltStr = list[0].split(" ")
    for char in spltStr:
        if char != "":
            instruction.append(char)
    if instruction[0] in listRiscV:
        instruction.insert(0, "")
       
    return instruction

doc = Assembler()
doc.RtypeInstruction()
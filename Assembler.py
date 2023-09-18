listRiscV = ["add", "nand", "lw", "sw", "beq", "jalr", "halt", "noop" ]

class Assembler:
    
    saveLabelAndValue = {}
    
    def __init__(self):
        pass
    
    def ScanToInstructions(self, str:str):
        listStr = str.strip().split('#')
        listStr = listStr[0].split(" ")
        listInstruction = []
        for char in listStr:
            if char != "":
                listInstruction.append(char)
        if listInstruction[0] in listRiscV:
            listInstruction.insert(0 , "")
        return listInstruction
    
    def ReadFileText(self, str):
        instruction = []
        count = 0
        with open(str) as f:
            for line in f:
                instruction.append(Pair(self.ScanToInstructions(line), count))
                count+=1
        return instruction
    
    def convertInstruction(self):
        return
    
    
class Pair:
    
    def __init__(self, line, numbLine):
        self.line = line
        self.numbLine = numbLine
        

Asb = Assembler()
lstCode = Asb.ReadFileText('TextFile.txt')
for ints in lstCode:
    print(ints.line, ", ", ints.numbLine)
    
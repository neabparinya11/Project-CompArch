listRiscV = ["add", "nand", "lw", "sw", "beq", "jalr", "halt", "noop" ]
listNumber = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DictRiscV = {
            "add": "000",
            "nand": "001",
            "lw": "010",
            "sw": "011",
            "beq": "100",
            "jalr": "101",
            "halt": "110",
            "noop": "111"
        }
Number = {
    "0" : "000",
    "1" : "001",
    "2" : "010",
    "3" : "011",
    "4" : "100",
    "5" : "101",
    "6" : "110",
    "7" : "111"
}

class Assembler:
    
    saveLabelAndValue = {} # str: "Variable", value: number
    saveLabelAndAddress = {} # str: "Variable", value: number
    def __init__(self):
        pass
    
    def ScanToInstructions(self, str:str, numLine):
        listStr = str.strip().split('#')
        listStr = listStr[0].split(" ")
        listInstruction = []
        for char in listStr:
            if char != "":
                listInstruction.append(char)
        if listInstruction[0] in listRiscV:
            listInstruction.insert(0 , "")
        if listInstruction[0] != "":
            self.saveLabelAndAddress[listInstruction[0]] = numLine
        return listInstruction
    
    def ReadFileText(self, str):
        instruction = []
        count = 0
        with open(str) as f:
            for line in f:
                instruction.append(Pair(self.ScanToInstructions(line, count), count))
                count+=1
        return instruction
    
    def convertInstruction(self, listStr, numbLine): 
        result = ""
        if listStr[1] in (".fill"):
            result = self.FillInstruction(listStr, numbLine)
        if listStr[1] in ("add", "nand"):
            result = self.RtypeInstruction(listStr)
        if listStr[1] in ("jalr"):
            result = self.JtypeInstruction(listStr)
        if listStr[1] in ("lw", "sw", "beq"):
            result = self.ItypeInstruction(listStr)
        if listStr[1] in ("noop", "halt"):
            result = self.OtypeInstruction(listStr)
        return result
    
    def ItypeInstruction(self, listStr):
        machineCode = ""
        
        return machineCode
    
    def JtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DictRiscV[listStr[1]] + Number[listStr[2]] + Number[listStr[3]] + "0".zfill(16)
        return machineCode.zfill(32)
    
    def RtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DictRiscV[listStr[1]] + Number[listStr[2]] + Number[listStr[3]] + "0".zfill(13) + Number[listStr[4]]
        return machineCode.zfill(32)        
    
    def OtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DictRiscV[listStr[1]] + "0".zfill(22)
        return machineCode.zfill(32)
    
    def FillInstruction(self, listStr, line):
        machineCode = ""
        if self.isNumber(listStr[2]):
            machineCode = format(line, 'b')
        else:
            machineCode = format(self.saveLabelAndAddress[listStr[2]], 'b')
        return machineCode.zfill(32)
        
    def isNumber(self, number:str):
        for ch in number:
            if ch in listNumber:
                if ch == '-':
                    continue
                    
                return True
        return False
    
class Pair:
    
    def __init__(self, line, numbLine):
        self.line = line
        self.numbLine = numbLine
        

Asb = Assembler()
lstCode = Asb.ReadFileText('TextFile.txt')

for ints in lstCode:
    print(ints.line, ", ", ints.numbLine)
    print(Asb.convertInstruction(ints.line, ints.numbLine))
    
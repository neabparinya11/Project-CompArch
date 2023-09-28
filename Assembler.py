LISTRISCV = ["add", "nand", "lw", "sw", "beq", "jalr", "halt", "noop" ]
LISTNUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
INVERTBIT = { '0' : '1', '1': '0' }
DICTRISCV = {
            "add": "000",
            "nand": "001",
            "lw": "010",
            "sw": "011",
            "beq": "100",
            "jalr": "101",
            "halt": "110",
            "noop": "111"
        }
NUMBER = {
    "0" : "000",
    "1" : "001",
    "2" : "010",
    "3" : "011",
    "4" : "100",
    "5" : "101",
    "6" : "110",
    "7" : "111"
}

LISTHEXANUMBER = {
    "0000" : "0",
    "0001" : "1",
    "0010" : "2",
    "0011" : "3",
    "0100" : "4",
    "0101" : "5",
    "0110" : "6",
    "0111" : "7",
    "1000" : "8",
    "1001" : "9",
    "1010" : "A",
    "1011" : "B",
    "1100" : "C",
    "1101" : "D",
    "1110" : "E",
    "1111" : "F"
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
        if listInstruction[0] in LISTRISCV:
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
        elif listStr[1] in ("add", "nand"):
            result = self.RtypeInstruction(listStr)
        elif listStr[1] in ("jalr"):
            result = self.JtypeInstruction(listStr)
        elif listStr[1] in ("lw", "sw", "beq"):
            result = self.ItypeInstruction(listStr)
        elif listStr[1] in ("noop", "halt"):
            result = self.OtypeInstruction(listStr)
        else:
            raise ValueError("Invalid opcode")
        return result
    
    def ItypeInstruction(self, listStr):
        machineCode = ""
        offsetFields = ""
        if self.isNumber(listStr[4]):
            offsetFields = NUMBER[listStr[4]]
        else:
            offsetFields = format(self.saveLabelAndAddress[listStr[4]], 'b')
            
        machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + offsetFields.zfill(16)
        return machineCode.zfill(32)
    
    def JtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + "0".zfill(16)
        return machineCode.zfill(32)
    
    def RtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + "0".zfill(13) + NUMBER[listStr[4]]
        return machineCode.zfill(32)        
    
    def OtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DICTRISCV[listStr[1]] + "0".zfill(22)
        return machineCode.zfill(32)
    
    def FillInstruction(self, listStr, line):
        machineCode = ""
        if self.isNumber(listStr[2]):
            if int(listStr[2]) >= 0:
                machineCode = NUMBER[listStr[2]]
            else:
                machineCode = self.TwoComplement(int(listStr[2]), 32)
            # machineCode = bin(listStr[2]) + 1
        else:
            machineCode = format(self.saveLabelAndAddress[listStr[2]], 'b')
        return machineCode.zfill(32)
        
    def isNumber(self, number:str):
        for ch in number:
            if ch in LISTNUMBER:
                if ch == '-':
                    continue
                    
                return True
        return False
    
    def TwoComplement(self, numb, bits)->str:
        s = bin(numb & int("1"*bits, 2))[2:]
        return s
    
    def BinaryToDecimal(self, binary:str):
        if len(binary) != 32:
            raise ValueError("The binary string must be 32 bits")
        if binary[0] == '0':
            return int(binary, 2)
        else:
            result = ""
            for char in binary:
                result += INVERTBIT[char]
            result = int(result, 2) +1
            return (-1)*result
    
    def BinarydecimalToHexadecimal(self, binaryD:str):
        # return hex(int(binaryD, 2))
        if len(binaryD) != 32:
            raise ValueError("The binary string must be 32 bits")
        if binaryD[0] == '0':
            return hex(int(binaryD, 2))
        else:      
            result = "0x"
            for i in range(0, 8):
                result += LISTHEXANUMBER[binaryD[4*i:4*(i+1)]]      
            return result
    
class Pair:
    
    def __init__(self, line, numbLine):
        self.line = line
        self.numbLine = numbLine
        

# Asb = Assembler()
# lstCode = Asb.ReadFileText('TextFile.txt')

# for ints in lstCode:
#     covert = Asb.convertInstruction(ints.line, ints.numbLine)
#     binary = Asb.BinaryToDecimal(covert)
#     hexa = Asb.BinarydecimalToHexadecimal(covert)
#     print(covert)
#     print(binary)
#     print(hexa)
    
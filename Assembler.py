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

RANGEREGISTER = ['0', '1', '2', '3', '4', '5', '6', '7']

import sys
class Assembler:
    
    saveLabelAndValue = {} # str: "Variable", value: number
    saveLabelAndAddress = {} # str: "Variable", value: number
    def __init__(self):
        pass
    
    def ScanToInstructions(self, str:str, numLine):
        listStr = str.strip().split('#')
        listStr = [ input for input in listStr[0].split(" ") if input != '']
        listInstruction = []
        for char in listStr:
            if char != '':
                listInstruction.append(char)
        if listInstruction == []:
            return []
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
                if self.ScanToInstructions(line, count) == []:
                    continue
                else:
                    instruction.append(Pair(self.ScanToInstructions(line, count), count))
                    count+=1
            f.close()
        return instruction
    
    def convertInstruction(self, listStr, numbLine):
        result = ""
        if listStr[1] in (".fill"):
            result = self.FillInstruction(listStr)
        elif listStr[1] in ("add", "nand"):
            result = self.RtypeInstruction(listStr)
        elif listStr[1] in ("jalr"):
            result = self.JtypeInstruction(listStr)
        elif listStr[1] in ("lw", "sw", "beq"):
            result = self.ItypeInstruction(listStr, numbLine)
        elif listStr[1] in ("noop", "halt"):
            result = self.OtypeInstruction(listStr)
        else:
            raise ValueError("Invalid opcode "+ listStr[1]+ " not have")
            
        return result
    
    def ItypeInstruction(self, listStr, pc):
        machineCode = ""
        offsetFields = ""
        
        if self.isNumber(listStr[2]) != True or self.isNumber(listStr[3]) != True:
            raise ValueError('Invalid register')
        
        if self.checkRegister(listStr[2]) != True or self.checkRegister(listStr[3]) != True:
            raise ValueError('Register out of range')
        
        if self.isNumber(listStr[4]):
            address = int(listStr[4])
            
            if address > 32767 or address < -32768:
                raise ValueError('Offset out of bound')
            
            if listStr[1] == "beq":
                offsetFields = self.TwoComplementV2(address, 16)
            else:
                offsetFields = '{0:b}'.format(int(listStr[4]))
        else:
            if listStr[1] == "beq":
                target = int(self.saveLabelAndAddress[listStr[4]])
                compare = (target - pc) -1
                
                if compare > 32767 or compare < -32768:
                    raise ValueError('Offset out of bound')
                
                offsetFields = self.TwoComplementV2(compare, 16)
            else:
                pc_int = self.saveLabelAndAddress[listStr[4]]
                offsetFields = self.TwoComplementV2(pc_int, 16)
            
        machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + offsetFields.zfill(16)
        return machineCode.zfill(32)
    
    def JtypeInstruction(self, listStr):
        machineCode = ""
        
        if self.isNumber(listStr[2]) != True or self.isNumber(listStr[3]) != True:
            raise ValueError('Invalid register')
        
        elif self.checkRegister(listStr[2]) != True or self.checkRegister(listStr[3]) != True:
            raise ValueError('Register out of range')
        
        else:
            machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + "0".zfill(16)
            return machineCode.zfill(32)
    
    def RtypeInstruction(self, listStr):
        machineCode = ""
        
        if self.isNumber(listStr[4]) != True or self.isNumber(listStr[3]) != True or self.isNumber(listStr[2]) != True:
            raise ValueError('Invalid register')
        
        elif self.checkRegister(listStr[4]) != True or self.checkRegister(listStr[3]) != True or self.checkRegister(listStr[2]) != True:
            raise ValueError('Register out of range')
        
        else:
            machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + "0".zfill(13) + NUMBER[listStr[4]]
            return machineCode.zfill(32) 
    
    def OtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DICTRISCV[listStr[1]] + "0".zfill(22)
        return machineCode.zfill(32)
    
    def FillInstruction(self, listStr):
        machineCode = ""
        
        if self.isNumber(listStr[2]):
            if int(listStr[2]) >= 0:
                machineCode ='{0:b}'.format(int(listStr[2]))
            else:
                print
                machineCode = self.TwoComplementV2(int(listStr[2]), 32)
                # machineCode = listStr[2]
        else:
            machineCode = '{0:b}'.format(self.saveLabelAndAddress[listStr[2]])
        return machineCode.zfill(32)
        
    def isNumber(self, number:str):
        for ch in number:
            if ch == '-' and number.index(ch) == 0:
                continue
            if ch in LISTNUMBER:
                continue
            else:
                return False
            
        return True
                    
    def TwoComplementV2(self, numb:int, bits:int):
        return bin(numb & int("1"*bits, 2))[2:]
        
    def TwoComplement(self, numb:int, bits)->str:
        s = '{0:b}'.format(numb).zfill(bits)
        flip_bits = ''
        for ch in s:
            if ch == '1':
                flip_bits += '0'
            elif ch == '0':
                flip_bits += '1'
            elif ch == '-':
                flip_bits += '1'
        add1 = int(flip_bits, 2) + 1
        return '{0:b}'.format(add1)
    
    def ConvertTwoComplementToCecimal(self, numb:int, bits:int)->int:
        two_complement = self.TwoComplement(numb, bits)
        if two_complement[0] == '1':
            return int(two_complement[1:bits], 2)*(-1)
        else:
            return int(two_complement, 2)
    
    def BinaryToDecimal(self, binary:str, bits:int):
        if len(binary) != bits:
            raise ValueError("The binary string must be "+ str(bits) + "bits")
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
        
    def checkRegister(self, register:str):
        if register in RANGEREGISTER:
            return True
        else:
            return False
    
    
class Pair:
    
    def __init__(self, line, numbLine):
        self.line = line
        self.numbLine = numbLine
        
# Asb = Assembler()
# two = Asb.TwoComplementV2(4294705152, 32)
# print(int(two, 2))
# one = Asb.TwoComplementV2(int(two, 2), 32)
# print(Asb.ConvertTwoComplementToCecimal(int(one, 2), 32))
# one = Asb.ConvertTwoComplementToCecimal(int(two, 2), 16)
# print(one)
# lstCode = Asb.ReadFileText('multi.txt')
# for ints in lstCode:
#     covert = Asb.convertInstruction(ints.line, ints.numbLine)
#     print(covert)
# print(Asb.saveLabelAndAddress)
# print(Asb.saveLabelAndValue)
LISTRISCV = ["add", "nand", "lw", "sw", "beq", "jalr", "halt", "noop" ] #LISTRISCV เป็น Dictionary ที่เก็บรวบรวม RiscV Command
LISTNUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] #LISTNUMBER เป็น Dictionary ที่รวบรวมตัวเลขในหลักหน่วย
INVERTBIT = { '0' : '1', '1': '0' } #INVERTBIT เป็น Dictionary ที่จะใช้ในการกลับ bit
DICTRISCV = { #DICTRISCV เป็น Dictionary ที่จะแปลง RiscV Command เป็น opcode
            "add": "000",
            "nand": "001",
            "lw": "010",
            "sw": "011",
            "beq": "100",
            "jalr": "101",
            "halt": "110",
            "noop": "111"
        }
NUMBER = { #NUMBER เป็น Dictionary แปลง เลขหลักหน่วยเป็น Machine Code 3 bits
    "0" : "000",
    "1" : "001",
    "2" : "010",
    "3" : "011",
    "4" : "100",
    "5" : "101",
    "6" : "110",
    "7" : "111"
}

LISTHEXANUMBER = { #LISTHEXANUMBER เป็น Dictionary Machine Code 4 bits เพื่อแปลงเป็น เลขฐาน 16
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

RANGEREGISTER = ['0', '1', '2', '3', '4', '5', '6', '7'] #RANGEREGISTER เป็น Dictionary เพื่อตรวจสอบ ขอบเขต register เกินกำหนดหรือไม่

import sys
class Assembler: #class Assembler saveLabelAndAddress เก็บ Label Address และ Line ที่ Label นั้นอยู่


    
    saveLabelAndValue = {} # str: "Variable", value: number
    saveLabelAndAddress = {} # str: "Variable", value: number
    def __init__(self):
        pass
    
    def ScanToInstructions(self, str:str, numLine): # ฟังก์ชันสำหรับสแกนและดึงคำสั่งจากบรรทัดของอินพุต
        listStr = str.strip().split('#')
        listStr = [ input for input in listStr[0].split(" ") if input != '']
        listInstruction = []
        for char in listStr:
            if char != '':
                listInstruction.append(char)  # เพิ่มที่ไม่เป็นว่างเข้าไปในคำสั่ง
        if listInstruction == []: # ถ้าไม่มีคำสั่ง ใส่ช่องว่าง
            return []
        if listInstruction[0] in LISTRISCV:
            listInstruction.insert(0 , "") # แทรกรหัสสตริงว่างไว้ที่จุดแรกเป็นคำสั่ง RISC-V
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
                    instruction.append(Pair(self.ScanToInstructions(line, count), count))# แทรกรหัสสตริงว่างไว้ที่จุดแรกเป็นคำสั่ง RISC-V
                    count+=1
            f.close()
        return instruction
    
    def convertInstruction(self, listStr, numbLine): # ฟังก์ชันสำหรับแปลงคำสั่ง
        result = ""
        if listStr[1] in (".fill"):
            result = self.FillInstruction(listStr) # แปลงคำสั่ง .fill
        elif listStr[1] in ("add", "nand"):
            result = self.RtypeInstruction(listStr) # แปลงคำสั่งประเภท R
        elif listStr[1] in ("jalr"):
            result = self.JtypeInstruction(listStr) # แปลงคำสั่งประเภท J
        elif listStr[1] in ("lw", "sw", "beq"):
            result = self.ItypeInstruction(listStr, numbLine) # แปลงคำสั่งประเภท I
        elif listStr[1] in ("noop", "halt"):
            result = self.OtypeInstruction(listStr) # แปลงคำสั่งประเภท O
        else:
            raise ValueError("Invalid opcode "+ listStr[1]+ " not have") # ถ้าคำสั่งไม่ถูกต้อง ให้ not have
        return result
    
    def ItypeInstruction(self, listStr, pc):
        machineCode = ""
        offsetFields = ""
        
        if self.isNumber(listStr[2]) != True or self.isNumber(listStr[3]) != True: # ตรวจสอบว่าทุกตัวใน register 2 และ 3 เป็นตัวเลขหรือไม่
            raise ValueError('Invalid register')
        
        if self.checkRegister(listStr[2]) != True or self.checkRegister(listStr[3]) != True: # ตรวจสอบว่า register 2 และ 3 อยู่ในช่วงที่ถูกต้องหรือไม่
            raise ValueError('Register out of range')
        
        if self.isNumber(listStr[4]):  # ถ้า offset เป็นตัวเลข
            address = int(listStr[4])
            
            if address > 32767 or address < -32768:
                raise ValueError('Offset out of bound')
            
            if listStr[1] == "beq":   # ถ้าเป็นคำสั่ง beq ให้ใช้ TwoComplementV2 คำนวณcomplement
                offsetFields = self.TwoComplementV2(address, 16)
            else:
                offsetFields = '{0:b}'.format(int(listStr[4]))
        else:
            if listStr[1] == "beq": # ถ้าเป็นคำสั่ง beq ให้คำนวณ offset จาก label
                target = int(self.saveLabelAndAddress[listStr[4]])
                compare = (target - pc) -1
                
                if compare > 32767 or compare < -32768:
                    raise ValueError('Offset out of bound')
                
                offsetFields = self.TwoComplementV2(compare, 16)
            else:
                pc_int = self.saveLabelAndAddress[listStr[4]]
                offsetFields = self.TwoComplementV2(pc_int, 16)
            
        machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + offsetFields.zfill(16)  # สร้าง machine code โดยรวม opcode, register และ offset
        return machineCode.zfill(32)
    
    def JtypeInstruction(self, listStr):
        machineCode = ""
        
        if self.isNumber(listStr[2]) != True or self.isNumber(listStr[3]) != True: # ตรวจสอบว่า register 2 และ 3 เป็นตัวเลขหรือไม่
            raise ValueError('Invalid register')
        
        elif self.checkRegister(listStr[2]) != True or self.checkRegister(listStr[3]) != True:  # ตรวจสอบว่า register 2 และ 3 อยู่ในช่วงที่ถูกต้องหรือไม่
            raise ValueError('Register out of range')
        
        else:
            machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + "0".zfill(16)   # สร้าง machine code โดยรวม opcode, register 2, และ register 3
            return machineCode.zfill(32)
    
    def RtypeInstruction(self, listStr):
        machineCode = ""
        
        if self.isNumber(listStr[4]) != True or self.isNumber(listStr[3]) != True or self.isNumber(listStr[2]) != True:  # ตรวจสอบว่า register 2, 3, และ 4 เป็นตัวเลขหรือไม่
            raise ValueError('Invalid register')
        
        elif self.checkRegister(listStr[4]) != True or self.checkRegister(listStr[3]) != True or self.checkRegister(listStr[2]) != True:  # ตรวจสอบว่า register 2, 3, และ 4 อยู่ในช่วงที่ถูกต้องหรือไม่
            raise ValueError('Register out of range')
        
        else:
            machineCode = DICTRISCV[listStr[1]] + NUMBER[listStr[2]] + NUMBER[listStr[3]] + "0".zfill(13) + NUMBER[listStr[4]]  # สร้าง machine code โดยรวม opcode, register 2, register 3, และ register 4
            return machineCode.zfill(32) 
    
    def OtypeInstruction(self, listStr):
        machineCode = ""
        machineCode = DICTRISCV[listStr[1]] + "0".zfill(22)  # สร้าง machine code โดยรวม opcode ของคำสั่ง O-type
        return machineCode.zfill(32)
    
    def FillInstruction(self, listStr):
        machineCode = ""
        
        if self.isNumber(listStr[2]):  # ถ้า .fill เป็นตัวเลข
            if int(listStr[2]) >= 0:
                machineCode ='{0:b}'.format(int(listStr[2]))
            else:
                machineCode = self.TwoComplementV2(int(listStr[2]), 32)
                # machineCode = listStr[2]
        else:
            machineCode = '{0:b}'.format(self.saveLabelAndAddress[listStr[2]])  # ถ้า .fill เป็น label
        return machineCode.zfill(32)
        
    def isNumber(self, number:str):   # ตรวจstring เป็นตัวเลขทั้งหมดหรือไม่
        for ch in number:
            if ch == '-' and number.index(ch) == 0:
                continue
            if ch in LISTNUMBER:
                continue
            else:
                return False
            
        return True
                    
    def TwoComplementV2(self, numb:int, bits:int): # คำนวณcomplement ของจำนวน numb ในรูปแบบ bits 
        return bin(numb & int("1"*bits, 2))[2:]
        
    def TwoComplement(self, numb:int, bits)->str:  # คำนวณcomplement ของจำนวน numb ในรูปแบบ bits
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
    
    def ConvertTwoComplementToDecimal(self, numb:int, bits:int)->int:  # ฟังก์ชันแปลงcomplement เป็นเลขฐานสิบ
        two_complement = self.TwoComplement(numb, bits)
        if two_complement[0] == '1':
            return int(two_complement[1:bits], 2)*(-1)
        else:
            return int(two_complement, 2)
    
    def BinaryToDecimal(self, binary:str, bits:int):  # ฟังก์ชันแปลงbinary เป็น decimal
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
    
    def BinarydecimalToHexadecimal(self, binaryD:str): # แปลงbinary ที่เกิดจาก decimal เป็น hexadecimal
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
        
    def checkRegister(self, register:str): # ตรวจว่าregisterถูกต้องหรือไม่
        if register in RANGEREGISTER:
            return True
        else:
            return False
    
    
class Pair: # ใช้เก็บข้อมูลของคำสั่งและหมายเลขบรรทัด
    
    def __init__(self, line, numbLine):
        self.line = line
        self.numbLine = numbLine
        
# two = Asb.TwoComplementV2(4294705152, 32)
# print(int(two, 2))
# binarytodecimal = Asb.BinaryToDecimal(~(6&6), 4)
# print(binarytodecimal)
# print(Asb.ConvertTwoComplementToCecimal(int(one, 2), 32))
# one = Asb.ConvertTwoComplementToCecimal(int(two, 2), 16)
# print(one)
# lstCode = Asb.ReadFileText('multi.txt')
# for ints in lstCode:
#     covert = Asb.convertInstruction(ints.line, ints.numbLine)
#     print(covert)
# print(Asb.saveLabelAndAddress)
# print(Asb.saveLabelAndValue)
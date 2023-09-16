import ReadTextFile as rtf

RiscVCommand = {
    "add" : "000",
    "nand" : "001",
    "lw" : "010",
    "sw" : "011",
    "beq" : "100",
    "jalr" : "101",
    "halt" : "110",
    "noop" : "111",
}

RisVType = {
    "lw" : "I-type",
    "sw" : "I-type",
    "beq" : "I-type",
    "add" : "R-type",
    "nand" : "R-type"
}

Number = {
    "0" : "000",
    "1" : "001",
    "2" : "010",
    "3" : "011",
    "4" : "100",
    "5" : "101",
    "6" : "110",
    "7" : "111",
    "five" : "101"
}
    
# I-type instructions (lw, sw, beq)

#                Bits 24-22 opcode

#                Bits 21-19 reg A (rs)

#                Bits 18-16 reg B (rt)

#                Bits 15-0 offsetField (เลข16-bit และเป็น 2’s complement  โดยอยู่ในช่วง –32768 ถึง 32767)

def ITypeInstructions(strRiscV:str, strRs:str, strRt:str, strOffset:str):
    return RiscVCommand[strRiscV] + Number[strRs] + Number[strRt] + Number[strOffset].zfill(16)
    
# R-type instructions (add, nand)

#                Bits 24-22 opcode

#                Bits 21-19 reg A (rs)

#                Bits 18-16 res B (rt)

#                Bits 15-3 ไม่ใช้ (ควรตั้งไว้ที่ 0)

#                Bits 2-0  destReg (rd)
def RTypeInstructions(strRiscV:str, strRs:str, strRt:str, strRd:str):
    return RiscVCommand[strRiscV] + Number[strRs] + Number[strRt] + "0".zfill(13) + Number[strRd]

# J-Type instructions (jalr)

#                Bits 24-22 opcode

#                Bits 21-19 reg A (rs)

#                Bits 18-16 reg B (rd)

#                Bits 15-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
def JTypeInstructions(strRiscV:str, strRs:str, strRd:str):
    return RiscVCommand[strRiscV] + Number[strRs] + Number[strRd] + "0".zfill(16)

# O-type instructions (halt, noop)

#                Bits 24-22 opcode

#                Bits 21-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
def OTypeInstructions(strRiscV:str):
    return RiscVCommand[strRiscV] + "0".zfill(22)


def AssemblyToMachineCode(strCode:str):
    instruction = ""
    spltCode = strCode.split(" ")
    if spltCode[0] in ("lw", "sw", "beq"):
        instruction = ITypeInstructions(spltCode[0], spltCode[1], spltCode[2], spltCode[3])
    if spltCode[0] in ("add", "nand"):
        instruction = RTypeInstructions(spltCode[0], spltCode[1], spltCode[2], spltCode[3])
    if spltCode[0] in ("jalr"):
        instruction = JTypeInstructions(spltCode[0], spltCode[1], spltCode[2])
    if spltCode[0] in ("halt", "noop"):
        instruction = OTypeInstructions(spltCode[0])

    print(instruction.zfill(32))
    print(int(instruction,2))
    
    return instruction.zfill(32), spltCode[0]
    
# str_code = rtf.ReadTextFile("TextFile.txt")
# AssemblyToMachineCode(str_code[2])
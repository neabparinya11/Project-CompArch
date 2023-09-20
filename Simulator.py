import Assembler as Asb

class Simulator:

    def __init__(self):
        pass
        
    def reset():  # Initialize/reset registers
        Simulator.reg = [0,0,0,0,0,0,0,0]

    # def update(self): #Updates the value on the registers

    def getMembin():
        mem = []
        Assembler = Asb.Assembler()
        lstCode = Assembler.ReadFileText('TextFile.txt')

        for ints in lstCode:
            mem.append(Assembler.convertInstruction(ints.line, ints.numbLine))
            # mem.append(Assembler.BinaryToDecimal(covert))
        return mem    
    
    def BinToDec(binMem):
        Assembler = Asb.Assembler()
        decMem = []

        for i in binMem:
            decMem.append(Assembler.BinaryToDecimal(i))
        return decMem
    
    biMem = getMembin()
    mem = BinToDec(biMem)
    reg = []
    stateCount = 0
    instCount = len(mem)

    

    def printState(pc,mem,reg):
        print("@@@\nstate:")
        # print("\tpc ", pc)
        print("\tmemory:")
        printMemory(mem)
        print("\tregisters:")      
        # printReg(Pc.reg)
        print("end state")


    # def display():
    #     Sim = Simulator()
    #     pc = 0
    #     isHalt = False
    #     Sim.reset()
        
    #     # while คำสั่งยังไม่ halt:
    #     #     Pc.printState(Pc.mem)
    #     #     Pc.update()

    #     for pc in Sim.instCount:
    #         Sim.printState(pc,Sim.mem,Sim.reg)
    #         if isHalt:
    #             break

    #         inst = Sim.biMem[pc]
    #         if len(inst) < 32:
    #             inst.zfill(32-len(inst))

    #         instType = inst[7:10]
    #         rs = int(inst[10:13],2)
    #         rd = int(inst[13:16],2)
    #         imm = int(inst[0:16],2)

    #         match instType:
    #             case "000":
    #                 if(imm !=0):
    #                     Sim.reg[imm] = Sim.reg[rs] + Sim.reg[rd]


    #     print("machine halted")
    #     print("total of ", Sim.stateCount ," instructions executed")
    #     print("final state of machine:")



def printMemory(mem):
    for i in mem:
        print ("\t\tmem[ ",mem.index(i)," ] ",i)

def printReg(reg):
     for i in reg:
        print ("\t\treg[ "+reg.index(i)+" ] "+i)



# mem = "00000000000010100000000000000001"
# print(mem)
# instType = mem[7:10]
# rs = int(mem[10:13],2)
# rd = int(mem[13:16],2)
# imm = int(mem[0:16],2)
# print(instType,rs,rd,imm)

# Simulator = Simulator()
# print (Simulator.biMem)
# Pc.printState(Pc.mem)
# Simulator.reset()
# print (Simulator.reg)



    


   




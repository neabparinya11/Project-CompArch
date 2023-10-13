import Assembler as Asb

class Simulator:
 
    run = True
    max_StateCount = 500
    stateCount = 0
    
    def __init__(self):
        self.binMem = self.getMembin()
        self.mem =  self.BinToDec(self.binMem)
        self.reg = [0,0,0,0,0,0,0,0]
        self.pc = 0
        
    def reset(self):  # Initialize/reset registers
        self.reg = [0,0,0,0,0,0,0,0]


    def getMembin(self):
        mem = []
        Assembler = Asb.Assembler()
        lstCode = Assembler.ReadFileText('combination.txt')

        for ints in lstCode:
            mem.append(Assembler.convertInstruction(ints.line, ints.numbLine))
            # mem.append(Assembler.BinaryToDecimal(covert))
        return mem    
    
    
    def BinToDec(self,binMem):
        Assembler = Asb.Assembler()
        decMem = []

        for i in binMem:
            decMem.append(Assembler.BinaryToDecimal(i, 32))
        return decMem
    

    def fetch(self):
        self.errorDetect()
        instruction = self.binMem[self.pc]
        self.pc += 1
        self.stateCount += 1
        return instruction
    
    def errorDetect(self):          # detect infinite loop or address -1
        if self.stateCount >= self.max_StateCount - 1:
            raise Exception('Infinite loop detected!')
        if self.pc <= -1:
            raise Exception('Address cannot be less than 0!')
        

    def instType(self, instructions):
        inst = str(instructions)
        opcode = inst[7:10]
        rs = int(inst[10:13],2)
        rd = int(inst[13:16],2)
        imm = int(inst[16:32],2)        

        # print(type,rs,rd,imm)

        if opcode == "000":             # ADD
            if(imm !=0):
                 self.reg[imm] = self.reg[rs] + self.reg[rd]

        elif opcode == "001":             # NAND
            if (imm !=0):
                self.reg[imm] = ~(self.reg[rs] & self.reg[rd])
        
        elif opcode == "010":             # LW
            if (rd != 0):
                self.reg[rd] = self.mem[self.reg[rs] + imm];
                
        elif opcode == "011":             # SW
                self.mem[self.reg[rs] + imm] = self.reg[rd];
                
        elif opcode == "100":             # BEQ
            if (self.reg[rs] == self.reg[rd]):
                asb = Asb.Assembler()
                self.pc += asb.BinaryToDecimal('{0:b}'.format(imm).zfill(16), 16)
                
        elif opcode == "101":             # JARL
            if (rd != 0):
                self.reg[rd] = self.pc + 1;
            self.pc = self.reg[rs] - 1;
                
        elif opcode == "110":             # Halt
            # exit
            self.run = False
            print("machine halted")
            print("total of ", self.stateCount ," instructions executed")
            print("final state of machine:", self.pc)
                
        elif opcode == "111"    :         # NOOP
            pass

        
                
    def printState(self,pc,mem,reg):
        print("@@@\nstate:")
        print("\tpc ", pc)
        print("\tmemory:")
        printMemory(mem)
        print("\tregisters:")      
        printReg(reg)
        print("end state")
        print(" ")

    def output(self):
        print('The output of this program is :', self.reg[3])

    def display(self):
        Sim = Simulator()
        self.reset()
        for i in self.mem:
            print('memory[',self.mem.index(i),']=',i)
        print('\t')
        print('\t')
        Sim.printState(self.pc,self.mem,self.reg)

        while self.run:
            instruction = self.fetch()
            if instruction == 0:
                break
            self.instType(instruction)
            Sim.printState(self.pc,self.mem,self.reg)

        # print("machine halted")
        # print("total of ", Sim.stateCount ," instructions executed")
        # print("final state of machine:")
        # Sim.printState(self.pc,self.mem,self.reg)


def printMemory(mem):
    # print(mem)
    memCount = 0
    for i in mem:
        print ("\t\tmem[ ",memCount," ] ",i)
        memCount +=1

def printReg(reg):
    # print(reg)
    for i in range (len(reg)):
        print ("\t\treg[ ",i," ] ",reg[i])




    


   






class Pc:

    def inputmem():
        input = open('AssemblyMachine.txt','r')
        data = input.read()
        mem = data.split("\n")
        print(mem)
        return mem
    
    mem = inputmem()

    # def reset(self):  # Initialize/reset registers

    # def update(self): #Updates the value on the registers

    def printState(mem):
        print("@@@\nstate:")
        # print("\tpc ", StackPointer)
        print("\tmemory:")
        printMemory(mem)
        print("\tregisters:")      
        # printReg(Pc.reg)
        print("end state")
        
def printMemory(mem):
    for i in mem:
        print ("\t\tmem[ ",mem.index(i)," ] ",i)

# def printReg(reg):
#      for i in reg:
#         print ("\t\treg[ "+reg.index(i)+" ] "+i)

# def display(Pc):
    # Pc.reset()
    # while คำสั่งยังไม่ halt:
        # Pc.printState(Pc.mem)
        # Pc.update()
    # else:
    #     print("machine halted")
    #     print("total of ", clckCycle ," instructions executed")
    #     print("final state of machine:")
Pc.printState(Pc.mem)


    


   




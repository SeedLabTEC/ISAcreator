import ALU_Generator as ALU
import Control_Generator as Control
import Utilities as Util
import Inst_Memory_Gen as Inst_Mem 
import readArchitectureFile as Reader 
import sys, os

Util.Write_Log("Starting Main Flow")


reader = Reader.Reader("../Modeling/Architectures/riscV16/riscV-16-Arch.txt")
l = reader.readFile()
inst = reader.getInstructions(l)

ALU_Inst = ""
Control_Inst = ""
for i in inst:
    if i['flag']=="1":
        if Control_Inst == "":
            Control_Inst = i['name']
        else:
            Control_Inst = Control_Inst + ":" + i['name']

for i in inst:
    if i['flag']=="1" and i['type']=="R":
        if ALU_Inst == "":
            ALU_Inst = i['name']
        else:
            ALU_Inst = ALU_Inst + ":" + i['name']

try:
    ALU.Generate_ALU_File(ALU_Inst.upper())
except:
    Util.Write_Log("Error in ALU generation")

try:
    Control.Generate_Control_File(Control_Inst.upper())
except:
    Util.Write_Log("Error in Control Unit generation")



Inst_Mem.Generate_Inst_Mem_File("file.prog")

Util.Write_Log("Execution Complete")

print("*********************************************************************************")
print("*************************Compile and Verification********************************")
print("Possible errors:")
os.system("cd Generated_Hardware && ./run.sh")
print("*********************************************************************************\n\n")

print("*********************************************************************************")
print("*****************************Testbench Results***********************************")
os.system("tail -n +2 ./Logs/TestBench.txt")
print("*********************************************************************************")
import ALU_Generator as ALU
import Control_Generator as Control
import Utilities as Util
import Inst_Memory_Gen as Inst_Mem 
import readArchitectureFile as Reader 

Util.Write_Log("Starting Main Flow")

try:
    ALU.Generate_ALU_File("ADD:OR:AND:SUB:SLT")
except:
    Util.Write_Log("Error on ALU generation")

try:
    Control.Generate_Control_File("OR:LW:SLT:J:SUB")
except:
    Util.Write_Log("Error on Control Unit generation")



Inst_Mem.Generate_Inst_Mem_File("file.prog")

Util.Write_Log("Execution Complete")


reader = Reader.Reader("../Modeling/Architectures/riscV32/riscV-32-Arch.txt")
l = reader.readFile()
inst = reader.getInstructions(l)

for i in inst:
    print(i['name'])
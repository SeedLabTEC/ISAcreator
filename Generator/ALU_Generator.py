import ConfigReader as Cfgr 
import Utilities as Util 
import json as json

def Generate_ALU_File(Operations):
    Util.Write_Log("Starting ALU Generator")
    Cfg_Parameters = Cfgr.ConfigReader()
    Util.Write_Log("Mapping ALU Structure")
    print(Represent_ALU_Structure(Operations, Cfg_Parameters))
    Structure = Create_ALU_Structure(Operations, Cfg_Parameters)
    Create_ALU_File(Structure,Cfg_Parameters)

def Create_ALU_File(Structure,Cfg_Parameters):
    F = open(str(Cfg_Parameters.ALU_Gen),"w")
    R = open(str(Cfg_Parameters.ALU_Template),"r") 
    Util.Write_Log("Creating ALU"+str(Cfg_Parameters.Ext_Type))
    Util.Write_Log("Reading ALU Template")
    data = json.load(R)
    
    Final_String = ""
    for val in Structure:
        Final_String  = Final_String + data[str(val)]
    F.write(Final_String)
    F.close()
    Util.Write_Log("File Generated")

     
def Create_ALU_Structure(Selected_Op,ALU_Parameters):
    list1 = str(ALU_Parameters.ALU_Operations).split(":")
    list2 = str(Selected_Op).split(":")
    final_structure = []
    for val in str(ALU_Parameters.ALU_Structure).split(":"):
        if(val in list2):
            final_structure.append(val)
        elif(val not in list1 and val not in list1):
            final_structure.append(val)
    Util.Write_Log("ALU Structure Created")
    return final_structure 


def Represent_ALU_Structure(Selected_Op,ALU_Parameters):
    Util.Write_Log("Creating ALU Structure")
    R = "**********************************ALU Structure**********************************\n"
    R = R + ">> Languaje: "+ALU_Parameters.Prog_Lang + "\n"
    R = R + ">> Name: "+ALU_Parameters.Processor_Name + "\n"
    R = R + ">> Version: "+ALU_Parameters.Version + "\n"
    tmp1 = ">> Available Operations: " + str(ALU_Parameters.ALU_Operations).replace(":","|")
    tmp2 = ">> Selected Operations: " + str(Selected_Op).replace(":","|")
    R = R + tmp1 + "\n" + tmp2 + "\n"
    tmp3 = ">> File Structure: \n--------------------------------------------------------------------------------\n" 
    list1 = str(ALU_Parameters.ALU_Operations).split(":")
    list2 = str(Selected_Op).split(":")
    for val in str(ALU_Parameters.ALU_Structure).split(":"):
        if(val in list2):
            tmp3 = tmp3 + "|-" + val+ "\n"
        elif(val not in list1 and val not in list1):
            tmp3 = tmp3 + "|-" + val+ "\n"
    R = R + tmp3 + "--------------------------------------------------------------------------------\n"
    R = R + "*********************************************************************************\n"
    return R       



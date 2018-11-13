import ConfigReader as Cfgr 
import Utilities as Util 
import json as json


def Generate_Control_File(Operations):
    Util.Write_Log("Starting Control Generator")
    Cfg_Parameters = Cfgr.ConfigReader()
    Util.Write_Log("Mapping Control Structure")
    print(Represent_Control_Structure(Operations, Cfg_Parameters))
    Structure = Create_Control_Structure(Operations, Cfg_Parameters)
    Create_Control_File(Structure,Cfg_Parameters)

def Create_Control_File(Structure,Cfg_Parameters):
    F = open(str(Cfg_Parameters.Control_Gen),"w")
    R = open(str(Cfg_Parameters.Control_Template),"r") 
    Util.Write_Log("Creating Control"+ str(Cfg_Parameters.Ext_Type))
    Util.Write_Log("Reading Control Template")
    data = json.load(R)
    
    Final_String = ""
    for val in Structure:
        Final_String  = Final_String + data[str(val)]
    F.write(Final_String)
    F.close()
    Util.Write_Log("File Generated")

def Create_Control_Structure(Selected_Op,Control_Parameters):
    list1 = str(Control_Parameters.Control_Operations).split(":")
    list2 = str(Selected_Op).split(":")
    final_structure = []
    for val in str(Control_Parameters.Control_Structure).split(":"):
        if(val in list2):
            final_structure.append(val)
        elif(val not in list1 and val not in list1):
            final_structure.append(val)
    Util.Write_Log("Control Structure Created")
    return final_structure 

def Represent_Control_Structure(Selected_Op,Control_Parameters):
    Util.Write_Log("Creating Control Structure")
    R = "********************************Control Structure********************************\n"
    R = R + ">> Languaje: "+ Control_Parameters.Prog_Lang + "\n"
    R = R + ">> Name: "+ Control_Parameters.Processor_Name + "\n"
    R = R + ">> Version: "+ Control_Parameters.Version + "\n"
    tmp1 = ">> Available Operations: " + str(Control_Parameters.Control_Operations).replace(":","|")
    tmp2 = ">> Selected Operations: " + str(Selected_Op).replace(":","|")
    R = R + tmp1 + "\n" + tmp2 + "\n"
    tmp3 = ">> File Structure: \n--------------------------------------------------------------------------------\n" 
    list1 = str(Control_Parameters.Control_Operations).split(":")
    list2 = str(Selected_Op).split(":")
    for val in str(Control_Parameters.Control_Structure).split(":"):
        if(val in list2):
            tmp3 = tmp3 + "|-" + val+ "\n"
        elif(val not in list1 and val not in list1):
            tmp3 = tmp3 + "|-" + val+ "\n"
    R = R + tmp3 + "--------------------------------------------------------------------------------\n"
    R = R + "*********************************************************************************\n"
    return R   
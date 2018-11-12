import ConfigReader as Cfgr 
import Utilities as Util 
import json as json

def Generate_Inst_Mem_File(Operations):
    Util.Write_Log("Starting Instruction Memory Generator")
    Cfg_Parameters = Cfgr.ConfigReader()
    print(Inst_Mem_specf(Operations, Cfg_Parameters))
    





def Inst_Mem_specf(Selected_Op,Mem_Parameters):
    R = "***********************Instruction Memory specificaction*************************\n"
    R = R + ">> Type: "+ str(Mem_Parameters.Inst_Mem_Type) + "\n"
    R = R + ">> RxC: "+ str(Mem_Parameters.Inst_Mem_Rows)+"x"+str(Mem_Parameters.Inst_Mem_Cols) + "\n"
    R = R + ">> Encoding: "+str(Mem_Parameters.Inst_Mem_Enc) + "\n"
    R = R + ">> Extension: "+str(Mem_Parameters.Inst_Mem_Ext) + "\n"
    R = R + "*********************************************************************************\n"
    return R   
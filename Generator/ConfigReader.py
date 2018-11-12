import configparser
import Utilities as Util






class ConfigReader:

    

    def __init__(self):
        Util.Write_Log("Configuration File Imported")
        config = configparser.ConfigParser()
        config.read(Util.Get_ConfigFile_Path());
        self.Ext_Type = config.get("General","Ext_Type")
        self.Prog_Lang = config.get("General","Prog_Lang")
        self.Processor_Name = config.get("General","Processor_Name")
        self.Version = config.get("General","Version")

        self.ALU_Structure = config.get("ALU","ALU_Structure")
        self.ALU_Sections = config.get("ALU","ALU_Sections")
        self.ALU_Operations = config.get("ALU","ALU_Operations")

        self.ALU_Template = config.get("FilePaths","ALU_Template")
        self.ALU_Gen = config.get("FilePaths","ALU_Gen")
        self.Control_Template = config.get("FilePaths","Control_Template")
        self.Control_Gen = config.get("FilePaths","Control_Gen")

        self.Control_Structure = config.get("Control","Control_Structure")
        self.Control_Sections = config.get("Control","Control_Sections")
        self.Control_Operations = config.get("Control","Control_Operations")
        
        self.Inst_Mem_Type = config.get("Instructions_Memory","Mem_Type")
        self.Inst_Mem_Rows = config.get("Instructions_Memory","Mem_Row")
        self.Inst_Mem_Cols = config.get("Instructions_Memory","Mem_Col")
        self.Inst_Mem_Enc = config.get("Instructions_Memory","Mem_Enc")
        self.Inst_Mem_Ext = config.get("Instructions_Memory","Mem_Ext")

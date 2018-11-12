import os.path
import datetime
import ConfigReader as Cfgr 

LogFile = "./Logs/Generator.log"
ConfigFile = "./Configuration/Config.cfg"

def Write_Log(Line):
    if os.path.exists(LogFile):
        f = open(LogFile, "a")
        f.write("<<< " + str(datetime.datetime.now()) + " ---- " + Line + " >>>\n")
        f.close()
        
    
    else:
        f = open(LogFile, "x")
        f.write("<<< " + str(datetime.datetime.now()) + " ---- Log file created >>>\n")
        f.close()
        f = open(LogFile, "a")
        f.write("<<< " + str(datetime.datetime.now()) + " ---- " + Line + " >>>\n")
        f.close()




def Get_LogFile_Path():
    return LogFile

def Get_ConfigFile_Path():
    return ConfigFile

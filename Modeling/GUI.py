'''
Importing libraries
'''
try:
    import tkinter as tk
    from tkinter import filedialog
except:
    import Tkinter as tk #python 2

from tkinter import messagebox
import sys
import time
import os
from threading import Thread
import threading
from guiObjects import Checkbar, Window, MainWindow
from readArchitectureFile import Reader
from selectInst import selectInstructions
from writeArchitectureFile import Writer

operationsTypeSelected = []


'''
@brief this function is the main function of his file
        its porpuse is to create the graphical interface
        for create a architecture model
@param window, the main tkinter window thats calls createModelWindow
'''
def model(pWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns,pOption, instSize, registerType):
    '''
    @brief method that updates a list of the instruction operation type
            when the user changes
    '''
    def checkOperationTypeSelected(pCheckBarList, pOperationsTypeAvailable):                     
        selected = list(pCheckBarList.getStates())
        for i in range(0, len(selected)-1):
            pOperationsTypeAvailable[i]['flag'] = selected[i]
        selectInstructions(createWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns)

    pWindow.withdraw()
    createWindow = Window()
    createWindow.setConfig('Set Architecture characteristics', '#b3ffb3', '600x400')

    #define gui elements
    selectOperationFrame = tk.Frame(createWindow, width = 200, height = 200, bg = '#eeffe6', highlightbackground="#eeffe6", 
                            highlightcolor="green", highlightthickness=1, cursor = 'fleur')
    titleLable = tk.Label(createWindow, text = "Architecture Characteristics", font = ("Arial Bold", 25), fg= '#444422', bg='#b3ffb3')
    operationsLabel = tk.Label(selectOperationFrame, text = "Select Operations type", font = ("Arial Bold", 15), fg= '#444422', bg='#eeffe6')

    #pack elements into the window
    titleLable.pack()
    selectOperationFrame.place(x = 30, y =60)        
    operationsLabel.pack()

    operationsName = []
    for element in pOperationsTypeAvailable:
        operationsName.append(element['operation'])

    myBars = Checkbar(selectOperationFrame, pBars = operationsName) 
    myBars.pack(side=tk.TOP,  fill=tk.Y)
    
    for i in range(0, len(myBars.barList)-1):
        if(int(pOperationsTypeAvailable[i]['flag']) == 1):
            myBars.setState(i, 1)
            myBars.barList[i].select()
    
    '''
    registersCharacteristics
    '''    
    #define gui elements
    #frame #1
    registersCharacteristicsFrame = tk.Frame(createWindow, width = 100, height = 200, bg = '#eeffe6', highlightbackground="green", highlightcolor="green", highlightthickness=1)    
    simpleRegisterCheckbutton = tk.Label(registersCharacteristicsFrame,text = "Simple Register", font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6', height=2, width = 20)        
    sizeLabelSR = tk.Label(registersCharacteristicsFrame, text="Size",font = ("Arial Bold", 10), fg= 'black', bg='#eeffe6')        
    sizeEntrySR = tk.Entry(registersCharacteristicsFrame, width=20, bd = 2, bg='#eeffe6', font= ('roboto condensed',8),fg='#444422',highlightcolor = '#444422')        
    amountLabelSR = tk.Label(registersCharacteristicsFrame, text="Amount",font = ("Arial Bold", 10), fg= '#444422', bg='white')        
    amountEntrySR = tk.Entry(registersCharacteristicsFrame, width=20, bd = 2, bg='#eeffe6', font= ('roboto condensed',8),fg='#444422',highlightcolor = '#444422')        

    #frame #2
    registersCharacteristicsFrame2 = tk.Frame(createWindow, width = 100, height = 200, bg = '#eeffe6', highlightbackground="green", highlightcolor="green", highlightthickness=1)        
    CheckVar2 = tk.IntVar()         
    fpRegisterCheckbutton = tk.Checkbutton(registersCharacteristicsFrame2,text = "Float Point Register", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6', variable = CheckVar2, onvalue = 1, offvalue = 0,height=2, width = 20)                
    sizeLabelFP = tk.Label(registersCharacteristicsFrame2, text="Size",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    sizeEntryFP = tk.Entry(registersCharacteristicsFrame2, width=20, bd = 2, bg='#eeffe6', font= ('roboto condensed',8),fg='#444422',highlightcolor = '#444422')        
    amountLabelFP = tk.Label(registersCharacteristicsFrame2, text="Amount",font = ("Arial Bold", 10), fg= 'black', bg='#eeffe6')        
    amountEntryFP = tk.Entry(registersCharacteristicsFrame2, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422',highlightcolor = '#444422')        

    #pack gui elements
    #frame #1
    registersCharacteristicsFrame.place(x = 100, y = 170)
    simpleRegisterCheckbutton.pack()
    sizeLabelSR.pack()
    sizeEntrySR.pack()
    amountLabelSR.pack()
    amountEntrySR.pack()

    #frame #2
    registersCharacteristicsFrame2.place(x = 280, y = 170)
    fpRegisterCheckbutton.pack()
    sizeLabelFP.pack()
    sizeEntryFP.pack()
    
    amountLabelFP.pack()
    amountEntryFP.pack()

    for i in registerType:
        if(i['registerType'] == 'simple'):
            sizeEntrySR.insert(0, i['size'])
            amountEntrySR.insert(0, i['amount'])

    instructionButton = tk.Button(createWindow, text="Select Instructions" , width= 20 ,font= ("Arial Bold", 8), bg = '#c3c388', 
                command= lambda:checkOperationTypeSelected(myBars, pOperationsTypeAvailable), activebackground = '#444422', fg = 'white',
                cursor = 'man',activeforeground = '#c3c388')
    encodeButton = tk.Button(createWindow, text="Create Encodification Type" , width= 20 ,font= ("Arial Bold", 8), bg = '#c3c388', 
                command= lambda:createInstEncodWindow(createWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns,pOption, instSize, registerType), activebackground = '#444422', 
                cursor = 'man', fg = 'white')
    createModel = tk.Button(createWindow, text="Create Model" , width= 20 ,font= ("Arial Bold", 8), bg = '#c3c388', 
               command= lambda:createModelFunct(createWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns,pOption, instSize, registerType, sizeEntrySR, amountEntrySR),cursor = 'man',activeforeground = '#444422', fg ='white')

    instructionButton.place(x = 40, y = 350)
    encodeButton.place(x = 210, y = 350)
    createModel.place(x = 390, y = 350)

    createWindow.mainloop()

'''
@brief Windows that show hot to create a new instruction type
@description the user will see a windows that display all the posible parts that can be put on an instruction
            he/she would have to put the size of that part *except for the opcode, it will always gonna have the size
            that has been indicated on the architecture*, and also he must put in which position of the instruction
            thet part is going to begin and end (bit position)
            f.e:
                rs1 size 5, begin 7, ends 11
'''
def createInstEncodWindow(pWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns,pOption, instSize, registerType):
    global source1, source2,destination,imm,funct7,funct3
    source1 = 0
    source2 = 0
    destination = 0
    imm = 0
    funct7 = 0
    funct3 = 0
    pWindow.withdraw()                                          #hide window
    createInstEncodWindow = tk.Toplevel()
    createInstEncodWindow.title('Create Instruction Type')
    createInstEncodWindow.config(bg= '#eeffe6')
    createInstEncodWindow.geometry('880x660')
    createInstEncodWindow.resizable(width=tk.NO, height=tk.NO)
    createInstEncodWindow.focus_set()

    ''' 
    @brief this function update if any of the checkbutton were selected
    '''
    def updateVariable(pValue):
        global source1, source2,destination,imm,funct7,funct3
        if(pValue == 1):
            if(source1 == 0): source1 = 1
            else: source1 = 0
        elif(pValue == 2):
            if(source2 == 0): source2 = 1
            else: source2 = 0
        elif(pValue == 3):
            if(destination == 0): destination = 1
            else: destination = 0
        elif(pValue == 4):
            if(imm == 0): imm = 1
            else: imm = 0
        elif(pValue == 5):
            if(funct7 == 0): funct7 = 1
            else: funct7 = 0
        elif(pValue == 6):
            if(funct3 == 0): funct3 = 1
            else: funct3 = 0        

    #define window elements
    nameLabel = tk.Label(createInstEncodWindow, text="Type name",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    nameEntry = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='#eeffe6', font= ('roboto condensed',8),fg='#33331a')        

    selectLabel = tk.Label(createInstEncodWindow, text="Select Instruction types, then specify its size, the begining \nand ending bits of the instruction",font = ("roboto condensed", 14), fg= '#444422', bg='#eeffe6')
    
    optionLabel =  tk.Label(createInstEncodWindow, text="Option",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    sizeLabel = tk.Label(createInstEncodWindow, text="Size",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    startBitLabel = tk.Label(createInstEncodWindow, text="Start Bit",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    endBitLabel = tk.Label(createInstEncodWindow, text="End Bit",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')                            
    
    #source 1
    source1Checkbutton = tk.Checkbutton(createInstEncodWindow,text = "Source Register 1", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6',height=2, width = 20, command = lambda:updateVariable(1))
    source1Size = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    source1Start = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    source1End = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')

    #source 2
    source2Checkbutton = tk.Checkbutton(createInstEncodWindow,text = "Source Register 2", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6',height=2, width = 20, command = lambda:updateVariable(2))                
    source2Size = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    source2Start = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    source2End = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')

    #destination
    destinationCheckbutton = tk.Checkbutton(createInstEncodWindow,text = "Destination Register", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6',height=2, width = 20, command = lambda:updateVariable(3))
    destinationSize = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    destinationStart = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    destinationEnd = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    
    #immediate
    immCheckbutton = tk.Checkbutton(createInstEncodWindow,text = "Immediate", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6',height=2, width = 20, command = lambda:updateVariable(4))
    immSize = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    immStart = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    immEnd = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')

    #function 7
    funct7Checkbutton = tk.Checkbutton(createInstEncodWindow,text = "Funct 7", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6',height=2, width = 20, command = lambda:updateVariable(5))
    funct7Size = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    funct7Start = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    funct7End = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')

    #function 3
    funct3Checkbutton = tk.Checkbutton(createInstEncodWindow,text = "Funct 3", font = ("Arial Bold", 10), 
        fg= '#444422', bg='#eeffe6',height=2, width = 20, command = lambda:updateVariable(6))
    funct3Size = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    funct3Start = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')
    funct3End = tk.Entry(createInstEncodWindow, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')

    #opcode
    opcodeLabel = tk.Label(createInstEncodWindow, text="Opcode",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    opcodeSizeLabel = tk.Label(createInstEncodWindow, text="7",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    opcodeInitLabel = tk.Label(createInstEncodWindow, text="0",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')
    opcodeEndLabel = tk.Label(createInstEncodWindow, text="6",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6')   

    #place elements
    selectLabel.place(x = 27, y = 20)
    
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 1)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 2)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 3)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 4)
    nameLabel.grid(row= 5, column = 0)
    nameEntry.grid(row= 5, column = 1)

    #start lables
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 6)
    optionLabel.grid(row= 7, column = 0)
    sizeLabel.grid(row= 7, column = 1)
    startBitLabel.grid(row= 7, column = 2)
    endBitLabel.grid(row= 7, column = 3)    

    #check button
    source1Checkbutton.grid(row = 8, column = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 9)
    source2Checkbutton.grid(row = 10, column = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 11)
    destinationCheckbutton.grid(row = 12, column = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 13)
    immCheckbutton.grid(row = 14, column = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 15)
    funct7Checkbutton.grid(row = 16, column = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 17)
    funct3Checkbutton.grid(row = 18, column = 0)
    tk.Label(createInstEncodWindow, text="",font = ("Arial Bold", 10), fg= '#444422', bg='#eeffe6').grid(row = 19)
    opcodeLabel.grid(row = 20, column = 0)

    #size
    source1Size.grid(row = 8, column = 1)
    source2Size.grid(row = 10, column = 1)
    destinationSize.grid(row = 12, column = 1)
    immSize.grid(row = 14, column = 1)
    funct7Size.grid(row = 16, column = 1)
    funct3Size.grid(row = 18, column = 1)
    opcodeSizeLabel.grid(row = 20, column = 1)

    #start
    source1Start.grid(row = 8, column = 2)
    source2Start.grid(row = 10, column = 2)
    destinationStart.grid(row = 12, column = 2)
    immStart.grid(row = 14, column = 2)
    funct7Start.grid(row = 16, column = 2)
    funct3Start.grid(row = 18, column = 2)
    opcodeInitLabel.grid(row = 20, column = 2)        

    #end
    source1End.grid(row = 8, column = 3)
    source2End.grid(row = 10, column = 3)
    destinationEnd.grid(row = 12, column = 3)
    immEnd.grid(row = 14, column = 3)
    funct7End.grid(row = 16, column = 3)
    funct3End.grid(row = 18, column = 3)
    opcodeEndLabel.grid(row = 20, column = 3)                        

    '''
    @brief function to update the gui if a checkbox was selected
    '''
    def entrysDisable():
        while(True):
            try:
                time.sleep(0.1)
                if(source1 == 0):
                    source1Size.config(state = tk.DISABLED)
                    source1Start.config(state = tk.DISABLED)
                    source1End.config(state = tk.DISABLED)
                if(source1 == 1):
                    source1Size.config(state = tk.NORMAL)
                    source1Start.config(state = tk.NORMAL)
                    source1End.config(state = tk.NORMAL)
                if(source2 == 0):
                    source2Size.config(state = tk.DISABLED)
                    source2Start.config(state = tk.DISABLED)
                    source2End.config(state = tk.DISABLED)
                if(source2 == 1):
                    source2Size.config(state = tk.NORMAL)
                    source2Start.config(state = tk.NORMAL)
                    source2End.config(state = tk.NORMAL)
                if(destination == 0):
                    destinationSize.config(state = tk.DISABLED)
                    destinationStart.config(state = tk.DISABLED)
                    destinationEnd.config(state = tk.DISABLED)
                if(destination == 1):
                    destinationSize.config(state = tk.NORMAL)
                    destinationStart.config(state = tk.NORMAL)
                    destinationEnd.config(state = tk.NORMAL)
                if(imm == 0):
                    immSize.config(state = tk.DISABLED)
                    immStart.config(state = tk.DISABLED)
                    immEnd.config(state = tk.DISABLED)
                if(imm == 1):
                    immSize.config(state = tk.NORMAL)
                    immStart.config(state = tk.NORMAL)
                    immEnd.config(state = tk.NORMAL)
                if(funct7 == 0):
                    funct7Size.config(state = tk.DISABLED)
                    funct7Start.config(state = tk.DISABLED)
                    funct7End.config(state = tk.DISABLED)
                if(funct7 == 1):
                    funct7Size.config(state = tk.NORMAL)
                    funct7Start.config(state = tk.NORMAL)
                    funct7End.config(state = tk.NORMAL)
                if(funct3 == 0):
                    funct3Size.config(state = tk.DISABLED)
                    funct3Start.config(state = tk.DISABLED)
                    funct3End.config(state = tk.DISABLED)
                if(funct3 == 1):
                    funct3Size.config(state = tk.NORMAL)
                    funct3Start.config(state = tk.NORMAL)
                    funct3End.config(state = tk.NORMAL)
            except:
                print("Ending thread")
                break

    try:
        entrysThread=Thread(target=entrysDisable, args=())
        entrysThread.daemon = True
        entrysThread.start()
    except:
        print("Error: unable to start thread")
    
    '''
    @brief when the user ends to creat the encodification it has to be check that it has sense
    @description it measure if the size of the part match with the size of the begining and ended space
                also it checks if the instruction has the size of 32 (dependes of the architecture model he choose)
    '''
    def checkEncodification():
        listOfEntrys = [[source1,source1Size,source1Start,source1End, "source 1 register", 'RS1'],[source2,source2Size,source2Start,source2End, "source 2 register", 'RS2'],
                        [destination,destinationSize,destinationStart,destinationEnd, "destination register",'RD'],[imm,immSize,immStart,immEnd, "immediate",'IMM'],
                        [funct7,funct7Size,funct7Start,funct7End, "function 7", 'funct7'],[funct3,funct3Size,funct3Start,funct3End, "function 3", 'funct3']]
        instructionSize = 25
        size=0
        init = 0
        end = 0
        tmp = []
        flag = 0
        if(nameEntry.get() == '' ):
            messagebox.showinfo(message="The name of the new operation type is not defined")              
        else:
            for entry in listOfEntrys:
                if(entry[0] == 1):
                    if(entry[1].get() != ''): 
                        size = int(entry[1].get())
                        if(entry[2].get() != ''): 
                            init = int(entry[2].get())
                            if(entry[3].get() != ''): 
                                end = int(entry[3].get())
                                if((init not in [0,1,2,3,4,5,6]) and (end not in [0,1,2,3,4,5,6])):
                                    if(((end - init)+1) != size):
                                        flag = 1
                                        messagebox.showinfo(message="On " + entry[4] + " selected the size does not match with\n the corresponding start and end bit, try again")
                                        break
                                    else: 
                                        tmp.append([entry[5],size,init,end])
                                        instructionSize -= size
                                else:
                                    flag = 1
                                    messagebox.showinfo(message="You select "+entry[4]+", but init or end position have not at available position (0, ...,6), try again")
                                    break 
                            else: 
                                flag = 1
                                messagebox.showinfo(message="You select "+entry[4]+", but end position is not defined, try again")
                                break
                        else: 
                            flag = 1
                            messagebox.showinfo(message="You select "+entry[4]+", but start position is not defined, try again")                                
                            break
                    else:
                        flag = 1
                        messagebox.showinfo(message="You select "+entry[4]+", but the size is not defined,, try again")                
                        break
        if(instructionSize != 0 and flag != 0):
            messagebox.showinfo(message="The encodification does not match with instruction size, try again")                
        else:
            newOPName = nameEntry.get()
            pOperationsTypeAvailable.append({'operation':newOPName, 'type': newOPName,'flag': '0'})
            x = {'type':newOPName}
            for i in tmp:
                x[str(i[0])] ='' + str(i[1]) + '|' + str(i[2]) +'|'+str(i[3])
            pEncodes.append({'endocodification':x})
            createInstEncodWindow.destroy()
            model(pWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns,pOption, instSize, registerType)


    createButton = tk.Button(createInstEncodWindow, text="Finish" , width= 20 ,font= ("Arial Bold", 8), bg = 'white', 
            command= lambda:checkEncodification(), activebackground = '#c3c388', activeforeground = '#c3c388')
    def back():
        createInstEncodWindow.destroy()
        pWindow.deiconify()

    backButton = tk.Button(createInstEncodWindow, text="Back" , width= 20 ,font= ("Arial Bold", 8), bg = 'white', 
            command= lambda:back(), activebackground = '#c3c388', activeforeground = '#c3c388')

    createButton.grid(row = 21, column = 1)
    backButton.grid(row = 21, column = 2)
    createInstEncodWindow.mainloop()

def createModelFunct(pWindow, pOperationsTypeAvailable, pEncodes, pFileName,listOfIns,pOption, instSize, registerType,sizeEntrySR, amountEntrySR):
    for i in range(0,len(registerType)-1):
        if(registerType[i]['registerType'] == 'simple'):
            registerType[i]['size'] = sizeEntrySR.get()
            registerType[i]['amount'] = amountEntrySR.get()
    if(pOption != 1):
        pWindow.withdraw()
        createModel = tk.Toplevel()
        createModel.title('Create Instruction')
        createModel.config(bg= '#eeffe6')
        createModel.focus_set()           
        nameLabel = tk.Label(createModel, text="name",font = ("Arial Bold", 10), fg= 'black', bg='white')
        nameEntry = tk.Entry(createModel, width=20, bd = 2, bg='white', font= ('roboto condensed',8),fg='#444422')

        nameLabel.grid(row = 0, column = 0)
        nameEntry.grid(row = 0, column = 1)

        nextButton = tk.Button(createModel, text="Next" , width= 20 ,font= ("Arial Bold", 8), bg = 'white', 
            command= lambda:nextStep(), activebackground = '#c3c388', activeforeground = '#c3c388').grid(row =1, column  = 0)

        def nextStep():
            myName = nameEntry.get()
            try:  
                os.mkdir("./Architectures/"+myName)                
            except OSError:  
                print ("Creation of the directory %s failed" % "./Architectures/"+myName)
            else:  
                writer = Writer("./Architectures/"+myName+".txt")
                writer.setOperations(pOperationsTypeAvailable)
                writer.setEncodifications(pEncodes)
                writer.setRegister(registerType)
                writer.setInstSize(instSize)
                writer.setInstructions(listOfIns)
                pWindow.destroy()
                InitWindow()
                print ("Successfully created the directory %s " % "./Architectures/"+myName)
    else:
        writer = Writer(pFileName)
        writer.setOperations(pOperationsTypeAvailable)
        writer.setEncodifications(pEncodes)
        writer.setRegister(registerType)
        writer.setInstSize(instSize)
        writer.setInstructions(listOfIns)
        print ("Successfully created")
        pWindow.destroy()
        InitWindow()        

'''
#init window
#'''
def InitWindow():
    #windows declare
    initWindow = tk.Tk()
    initWindow.title("Aplication Specific Processor: Modeling")
    initWindow.config(bg = '#b3ffb3')
    initWindow.geometry("580x340")
    initWindow.focus_set()

    #to decide what to do next
    #acording to the selection of the user
    def nextAction(pAction):
        if(pAction == "create"):
            selectArch(initWindow, 1)
        elif(pAction == "load"):
            selectArch(initWindow, 2)
        elif(pAction == "exit"):
            sys.exit()

    #windows elements
    initFrame = tk.Frame(initWindow, width = 580, height = 340, bg = '#b3ffb3')

    titleLable = tk.Label(initFrame, text = "ASP Specification", font = ("Arial Bold", 25), fg= '#ff471a', bg='#b3ffb3')

    createButton = tk.Button(initFrame, text="Create Model" , width= 10, font= ("Arial Bold", 15),
                     bg = "white", command= lambda:nextAction("create"),
                     activebackground = '#ffffb3', 
                     cursor = 'fleur',activeforeground = '#1a1a00')
    loadButton = tk.Button(initFrame, text="Load Model" , width= 10 ,font= ("Arial Bold", 15), bg = "white", 
                    command= lambda:nextAction("load"), activebackground = '#ffffb3', 
                    cursor = 'fleur',activeforeground = '#1a1a00')
    exitButton = tk.Button(initFrame, text="Exit" , width= 10, font= ("Arial Bold", 15), bg = "white", 
                command= lambda:nextAction("exit"), activebackground = '#ffffb3', 
                cursor = 'fleur',activeforeground = '#1a1a00')

    titleLable.pack(pady = 30)
    initFrame.pack(side = tk.TOP, pady = 10)
    createButton.pack(pady = 10)
    loadButton.pack(pady = 10)
    exitButton.pack(pady = 10)
    initWindow.mainloop()


'''
@brief
@description
'''
def nextStep(pWindow, pFileName, pWindow2,pOption = 0):
    reader = Reader(pFileName)
    listOfElements = reader.readFile()
    listOfOperations = reader.getOperations(listOfElements)
    listOfEncode = reader.getEncodifications(listOfElements)
    listOfIns = reader.getInstructions(listOfElements)
    instSize = reader.getInstSize(listOfElements)
    registerType = reader.getRegister(listOfElements)
    pWindow2.destroy()
    model(pWindow, listOfOperations, listOfEncode, pFileName,listOfIns,pOption, instSize, registerType)
    
    

'''
@brief
@description
'''
def selectArch(pWindow, pOption = 1):
    pWindow.withdraw()
    window = tk.Toplevel()
    window.title('Select Architecture model')
    window.config(bg= '#eeffe6')
    window.resizable(width=tk.YES, height=tk.YES)
    window.focus_set()

    if(pOption == 1):
        riscV32 = tk.Button(window, text="Risc V 32" , width= 10, font= ("Arial Bold", 12),
                        bg = "white", command= lambda:nextStep(pWindow,"./Architectures/riscV32/riscV-32-Arch.txt", window),
                        activebackground = '#ffffb3', 
                        cursor = 'fleur',activeforeground = '#1a1a00')
        riscV16 = tk.Button(window, text="Risc V 16" , width= 10, font= ("Arial Bold", 12),
                        bg = "white", command= lambda:nextStep(pWindow,"./Architectures/riscV16/riscV-16-Arch.txt",window),
                        activebackground = '#ffffb3', 
                        cursor = 'fleur',activeforeground = '#1a1a00')
        mips32 = tk.Button(window, text="Mips 32" , width= 10, font= ("Arial Bold", 12),
                        bg = "white", command= lambda:nextStep(pWindow,"./Architectures/mips32/riscV-32-Arch.txt",window),
                        activebackground = '#ffffb3', 
                        cursor = 'fleur',activeforeground = '#1a1a00')
        mips16 = tk.Button(window, text="Mips 16" , width= 10, font= ("Arial Bold", 12),
                        bg = "white", command= lambda:nextStep(pWindow,"./Architectures/mips16/riscV-32-Arch.txt",window),
                        activebackground = '#ffffb3', 
                        cursor = 'fleur',activeforeground = '#1a1a00')
        riscV32.pack()
        riscV16.pack()
        mips32.pack()
        mips16.pack()
    else: 
        nextButton = tk.Button(window, text="Next" , width= 10, font= ("Arial Bold", 12),
                        bg = "white", command= lambda:nextStep(pWindow, window.filename, window,1),
                        activebackground = '#ffffb3', 
                        cursor = 'fleur',activeforeground = '#1a1a00')
        nextButton.pack()
        window.filename =  tk.filedialog.askopenfilename(title = "Select file")        


InitWindow()
'''
Importing libraries
'''
try:
    import tkinter as tk
except:
    import Tkinter as tk #python 2

from tkinter import messagebox
import sys
import time
from readArchitectureFile import Reader
from guiObjects import Checkbar
 
listOfOpcodesRisc32 = ['1111111','1011111','1101111','1110111','1111011','1111101','1111110','1001111','1010111','1011011',
                '1011101','1011110','1100111','1101011','1101101','1101110','0000001','1000000','1100000','0011010', 
                '0111010']

listOfOpcodesRisc16 = ['00014','00015']
listOfInstAvailable = ['Square', 'power', 'logarithm','sin', 'cos', 'euler','tan', 'fact', 'fibonacci']
listOfFunct3 = ['---','000','001','010', '100','011', '100', '110','111']
listOfFunct7 = ['-------','0000000','0000001','0000010','0000100']

'''
@brief function to display the posible instructions that the user can select to his architecture model
@param pWindow the past windows he was using
@description it will display the instruction by type and the user can select with a checkbox if he/she wants
            that instruction 
'''
def selectInstructions(pWindow, pOperationsTypeSelected, pEncodes,pFileName,listOfInst, pModel = 0):     

    '''
    @brief for create instructions
    '''
    def createInstruction():
        root.withdraw()
        createInstWindow = tk.Toplevel()
        createInstWindow.title('Create Instruction')
        createInstWindow.config(bg= '#eeffe6')
        createInstWindow.focus_set()   
        
        opcodeLabel = tk.Label(createInstWindow, text="Select an opcode",font = ("Arial Bold", 10), fg= 'black', bg='white')
        
        opcodeSelect = tk.StringVar(createInstWindow)
        opcodeSelect.set('')             

        #define gui elements
        opcodeMenu = tk.OptionMenu(createInstWindow, opcodeSelect, *listOfOpcodesRisc32)        

        #pack gui elements 
        opcodeLabel.grid(row = 0, column = 0)
        opcodeMenu.grid(row = 0, column = 1)        

        listOfOpName = []
        for j in pOperationsTypeSelected: 
            listOfOpName.append(j['type'])
        

        operationTypeSelect = tk.StringVar(createInstWindow)
        operationTypeSelect.set('')


        #define gui elements
        opcodeLabel = tk.Label(createInstWindow, text="Select an operation type",font = ("Arial Bold", 10), fg= 'black', bg='white')
        operationMenu = tk.OptionMenu(createInstWindow, operationTypeSelect, *listOfOpName)        

        #pack gui elements 
        opcodeLabel.grid(row = 1, column = 0)
        operationMenu.grid(row = 1, column = 1)

        funct3Select = tk.StringVar(createInstWindow)
        funct3Select.set('')


        #define gui elements
        funct3Label = tk.Label(createInstWindow, text="Select a funct3",font = ("Arial Bold", 10), fg= 'black', bg='white')
        funct3Menu = tk.OptionMenu(createInstWindow, funct3Select, *listOfFunct3)        

        #pack gui elements 
        funct3Label.grid(row = 2, column = 0)
        funct3Menu.grid(row = 2, column = 1)

        funct7Select = tk.StringVar(createInstWindow)
        funct7Select.set('')


        #define gui elements
        funct7Label = tk.Label(createInstWindow, text="Select a funct7",font = ("Arial Bold", 10), fg= 'black', bg='white')
        funct7Menu = tk.OptionMenu(createInstWindow, funct7Select, *listOfFunct7)        

        #pack gui elements 
        funct7Label.grid(row = 3, column = 0)
        funct7Menu.grid(row = 3, column = 1)

        instSelect = tk.StringVar(createInstWindow)
        instSelect.set('')


        #define gui elements
        instLabel = tk.Label(createInstWindow, text="Select a instruction",font = ("Arial Bold", 10), fg= 'black', bg='white')
        instMenu = tk.OptionMenu(createInstWindow, instSelect, *listOfInstAvailable)        

        #pack gui elements 
        instLabel.grid(row = 4, column = 0)
        instMenu.grid(row = 4, column = 1)

        def verify():
            listOfVar = [opcodeSelect,funct3Select,funct7Select,instSelect]
            lsiOfList = [listOfOpcodesRisc32, listOfFunct3, listOfFunct7, listOfInstAvailable]
            counter = 0
            for i in range(0,len(listOfVar)):                
                opcodeChoosed = listOfVar[i].get()
                if(opcodeChoosed != ""):
                    counter += 1
                    if(opcodeChoosed != '---' and opcodeChoosed != '-------'):
                        lsiOfList[i].remove(opcodeChoosed)
                else:
                    messagebox.showinfo(message="please fill in all the indicated")
                    break
            if(operationTypeSelect.get() != ""):
                counter+=1
            if(counter == len(listOfVar)+1):
                x = {}
                x['name']=instSelect.get()
                if(operationTypeSelect not in ["I", "S"]):
                    x['funct7'] = funct7Select.get()
                x['funct3'] = funct3Select.get()
                x['opcode'] = opcodeSelect.get()
                x['type'] = operationTypeSelect.get()
                listOfInst.append(x)
                createInstWindow.destroy()
                selectInstructions(pWindow, pOperationsTypeSelected, pEncodes,pFileName,listOfInst)
            else:
                messagebox.showinfo(message="please fill in all the indicated")
        def cancel():
            createInstWindow.destroy()
            root.deiconify()

        tk.Button(createInstWindow, text='Create', command=verify).grid(row = 5, column = 0)
        tk.Button(createInstWindow, text='Cancel', command=cancel).grid(row = 5, column = 1) 


    if(len(pOperationsTypeSelected) == 0):
        messagebox.showinfo(message="There is no operation type selected")
    else:  
        root = tk.Toplevel()
        root.title('Select Instructions')
        root.config(bg= '#eeffe6')         
        listOfObj = []
        tmplistOfInst = []
        reader = Reader(pFileName)
        def updateFlags():  
            selected = []
            for lng in listOfObj:               
                selected += list(lng.getStates())
            for i in range(0,len(selected)-1):         
                for j in range(0,len(listOfInst)-1):                    
                    if(listOfInst[j]['name'] == tmplistOfInst[i]['name']):
                        if(selected[i] == 1):
                            listOfInst[j]['flag'] = ''+str(selected[i])+''
            root.destroy()
        for j in pOperationsTypeSelected:           
            if(int(j['flag']) == 1):             
                listOfInstType = reader.getInstructionsByType(listOfInst, j['type'])
                tmplistOfInst+=listOfInstType
                l = []
                for i in listOfInstType:
                    l.append(reader.getObjectByToken(i,'name'))                 
                lng = Checkbar(root, l)                
                lng.pack(side=tk.TOP,  fill=tk.X)
                lng.config(relief=tk.GROOVE, bd=2)    
                listOfObj.append(lng)  
        
        for lng in listOfObj:
            for i in range(0, len(lng.bars)-1):
                for j in range(0,len(listOfInst)-1):
                    if(listOfInst[j]['name'] == lng.bars[i]):    
                        if(listOfInst[j]['flag'] == '1'):    
                            lng.setState(i, 1)
                            lng.barList[i].select()
                                    
        tk.Button(root, text='Peek', command=updateFlags).pack(side=tk.RIGHT)
        tk.Button(root, text='Create Inst', command=createInstruction).pack(side=tk.RIGHT)                
        root.mainloop()    

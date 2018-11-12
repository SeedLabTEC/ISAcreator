try:
    import tkinter as tk
except:
    import Tkinter as tk #python 2


'''
@brief class of check buttons list
'''
class Checkbar(tk.Frame):
    def __init__(self, parent=None, pBars=[], side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vars = []
        self.bars = pBars 
        self.barList = []       
        for bar in self.bars:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=bar, variable=var,fg= '#444422', bg='#eeffe6', onvalue = 1, offvalue = 0,
            activebackground = '#c3c388', cursor = 'arrow',activeforeground = 'white',relief = tk.FLAT)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)
            self.barList.append(chk)
    
    '''
    @brief to get the state of the checkbuttons
    '''
    def getStates(self):
      return map((lambda var: var.get()), self.vars)
      
    '''
    @brief to set a checkbutton status value
    '''
    def setState(self,pIndex, pValue):
        self.bars[pIndex] = pValue


    def setGraphicState(self, pIndex):
        self.barList[pIndex].select()
        self.bars[pIndex] = 1

class MainWindow(tk.Tk): #Create a window"
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)

    def setConfig(self,  pTitle = "", pConfig = "", pGeometry=""):
        self.title("This is title Name")
        self.title(pTitle)
        self.config(bg= pConfig)
        self.geometry(pGeometry)
        self.resizable(width=tk.NO, height=tk.NO)
        self.focus_set()  

class Window(tk.Toplevel): #Create a window"
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)

    def setConfig(self,  pTitle = "", pConfig = "", pGeometry=""):
        self.title("This is title Name")
        self.title(pTitle)
        self.config(bg= pConfig)
        self.geometry(pGeometry)
        self.resizable(width=tk.NO, height=tk.NO)
        self.focus_set()  

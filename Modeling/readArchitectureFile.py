import ast 


class Reader():
    def __init__(self, pName):
        self.fileName = pName
    
    '''
    @brief this method reads a file which contains the set of instruction of a model
    '''
    def readFile(self):
        file = open(self.fileName, "r")
        listOfElements = []
        for element in file:
            print(element)
            listOfElements.append(ast.literal_eval(element)) #to read element as a dict type
        return listOfElements

    '''
    @brief return all the instructions for the file
    @description it recieve all the instruction from the file
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the instruction type
    '''
    def getInstructions(self, pFileElements):
        instructionList = []
        for element in pFileElements:
            try:
                instructionList.append(element['instruction'])
            except:
                continue
        return instructionList

    '''
    @brief return all the encodes for the file
    @description it recieve all the element from the file and filter the elements that are instruction 
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the encodification type
    '''
    def getEncodifications(self, pFileElements):
        encodeList = []
        for element in pFileElements:
            try:
                if(element['endocodification'] != None):
                    encodeList.append(element['endocodification'])
            except:
                continue
        return encodeList

    '''
    @brief return all the operation for the file
    @description it recieve all the element from the file and filter the elements that are operation 
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the operation type
    '''
    def getOperations(self,pFileElements):
        operationList = []
        for element in pFileElements:
            try:
                if(element['operation'] != ""):
                    operationList.append(element)
            except:
                continue
        return operationList


    '''
    @brief this method return all the instruction by its type
    @param pInstructionList a list of all the instructions on the architecture
    @param pType the filter
    @return the list of instructions of a specific type
    '''
    def getInstructionsByType(self,pInstructionList, pType):
        instructionList = []
        for element in pInstructionList:
            if(element['type'] == pType): 
                instructionList.append(element)
        return instructionList

    '''
    @brief this function read a dictionary (element), and return an specific value, that corresponds to a specific token/key
    @param pObject type:dictionary
    @param pToken, key or token to get access to an specific value of the dictionary
    @return a value from the dictionary
    '''
    def getObjectByToken(self,pObject, pToken):
        obj = None
        try:
            obj = pObject[pToken]
            return obj
        except:
            print("Error getting token: " + pToken)


    '''
    @brief return all the register type for the file
    @description it recieve all the element from the file and filter the elements that are register type 
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the register type type
    '''
    def getRegister(self,pFileElements):
        registerList = []
        for element in pFileElements:
            try:
                if(element['registerType'] != ""):
                    registerList.append(element)
            except:
                continue
        return registerList

    '''
    @brief
    @description
    '''
    def getInstSize(self, pFileElements):
        instSize = None
        for element in pFileElements:
            try:
                if(element['instructionSize'] != ""):
                    instSize = element
            except:
                continue
        return instSize
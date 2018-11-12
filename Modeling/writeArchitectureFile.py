import json


class Writer():
    def __init__(self, pName):
        self.fileName = pName   
        file = open(self.fileName, "w") 
        file.close()

    '''
    @brief return all the instructions for the file
    @description it recieve all the instruction from the file
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the instruction type
    '''
    def setInstructions(self, pFileElements):
        file = open(self.fileName, "a")
        for i in pFileElements:
            x= {}
            x['instruction'] = i
            file.write(json.dumps(x))
            file.write("\n")
        file.close()

    '''
    @brief return all the encodes for the file
    @description it recieve all the element from the file and filter the elements that are instruction 
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the encodification type
    '''
    def setEncodifications(self, pFileElements):
        file = open(self.fileName, "a")
        for i in pFileElements:
            x= {}
            x['endocodification'] = i
            file.write(json.dumps(x))
            file.write("\n")
        file.close()

    '''
    @brief return all the operation for the file
    @description it recieve all the element from the file and filter the elements that are operation 
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the operation type
    '''
    def setOperations(self,pFileElements):
        file = open(self.fileName, "a")
        for i in pFileElements:
            file.write(json.dumps(i))
            file.write("\n")
        file.close()

    '''
    @brief return all the register type for the file
    @description it recieve all the element from the file and filter the elements that are register type 
    @param pFileElements a list of all elements by line on the file
    @return all the elements that correspond to the register type type
    '''
    def setRegister(self,pFileElements):
        file = open(self.fileName, "a")
        for i in pFileElements:
            file.write(json.dumps(i))
            file.write("\n")
        file.close()
    '''
    @brief
    @description
    '''
    def setInstSize(self, pFileElement):
        file = open(self.fileName, "a")
        file.write(json.dumps(pFileElement))
        file.write("\n")
        file.close()        

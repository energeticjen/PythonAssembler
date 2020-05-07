import os.path
import re

savePath = 'C:\\Users\\Jenny\\Documents\\School\\Spring 2020\\CS 300\\CS300Project\\ProjectPython\\'

# initializing symtab dictionary
# including static register values
symtab = {
    "A":"0",
    "X":"1",
    "L":"2",
    "B":"3",
    "S":"4",
    "T":"5",
    "F":"6",
    "PC":"8",
    "SW":"9"
    }

#Initialize LOCCTR to hex 1000
locctr = "0x1000"

# initialize program name
programName = "prgram"

# initialize program length
programLength = "0x0000" 

def passOne():

    global symtab
    global locctr
    global programName
    global programLength

    document = "basic"
    programName = document
    completeName = os.path.join(savePath, document+".txt")

    # This will automatically close the file after reading it
    with open (completeName, "r") as myfile:

        outputDocument = os.path.join(savePath, "intermediateFile.txt")
        with open(outputDocument, "w", encoding='utf-8') as fileWrite:
           
            if myfile.mode == "r":
                # While not end of file
                # for each line of text
                for fileLine in myfile:

                    #Read in current line
                    #take first section of line (usually has OPCODE)
                    #compare that section to OPCODE TABLE

                    # separate each line into sections (based on column)
                    searchR = re.split('\s+', fileLine)
                    section1 = searchR[0] # labels - ADDLP, ALPHA, BETA, GAMMA
                    section2 = searchR[1] # opcodes - LDS, ADDR, JLT, RESW, etc
                    section3 = searchR[2] # actual data like #3, ALPHA,X, RESW value 100
                    section4 = searchR[3] # comments.

                    if section2 == "START":
                        # assuming section3 is already in hex format
                        locctr = section3
                        programName = section1
                    
                    # remove leading "0x"
                    tempLocctr = (locctr)[2:]
                    # make upper case
                    tempLocctr = tempLocctr.upper()
                    fileWrite.write(tempLocctr + "\t")

                    # if there is a symbol in the LABEL field (section 1)
                    if section1 != "":
                        # if symbol not in symtab, add it and the locctr value (location)
                        if section1 not in symtab:
                            # remove leading "0x"
                            tempLocctr = (locctr)[2:]
                            # make upper case
                            tempLocctr = tempLocctr.upper() 
                            symtab[section1] = tempLocctr
                        # if symbol already there, set error flag
                        else:
                            print("Error! This symbol has already been used!")
                    else:
                        # something needs to placed to maintain proper spacing
                        section1 = "*"

                    if section2 == "WORD":
                        # turn hex string into int decimal equivalent
                        locctr = int(locctr, 16)
                        # add 3 in base 10
                        locctr = locctr + 3
                        # turn into hex string equivalent
                        locctr = hex(locctr)

                    elif section2 == "RESW":
                        # turn hex string into int decimal equivalent
                        locctr = int(locctr, 16)
                        # words are 3 bytes long
                        locctr = locctr + (int(section3)*3)
                        # turn the int decimal back into hex string
                        locctr = hex(locctr)
                    elif section2 == "RESB":
                        # turn hex string into int decimal equivalent
                        locctr = int(locctr, 16)
                        # add value of current section3
                        locctr == locctr + int(section3)
                        # turn the int decimal back into hex string
                        locctr = hex(locctr)
                    else:
                        opcodeFound = False
                        # open the OPCODE TABLE
                        opcodeTableFile = os.path.join(savePath, 'opcodeTable.txt')
                        with open (opcodeTableFile, "r") as optab:
                            for opline in optab:
                                # split the data into a list by line
                                searchO = re.split('\s+', opline)
                                # first part is the mnemonic
                                mnemonic = searchO[0]
                                # make instruction length an integer
                                instructLen = int(searchO[1])
                                # make the opcode into a hex value
                                opCodeInt = int(searchO[2], 16)
                                opCode = hex(opCodeInt)
                                # if the opcode from the program is in the opcode table
                                if section2 == mnemonic:
                                    # turn hex string into int decimal equivalent
                                    locctr = int(locctr, 16)
                                    # add the related instruction length to the locctr
                                    locctr = locctr + instructLen
                                    # turn the int decimal back into hex string
                                    locctr = hex(locctr)
                                    opcodeFound = True
                                    break
                            if not opcodeFound:
                                print("Error! No opcode has been found!")

                    fileWrite.write(section1 + "\t" + section2 + "\t" + section3 + "\n")
    
    fileWrite.close()

    # Save LOCCTR as program length
    # remove leading "0x"
    tempLocctr = (locctr)[2:]
    # make upper case
    tempLocctr = tempLocctr.upper()
    programLength = tempLocctr

#########################################################################################################

def passTwo():
    global locctr
    global symtab
    global programName

    fileLines = []

    intermediateFile = os.path.join(savePath, "intermediateFile.txt")

    # This will automatically close the file after reading it
    with open (intermediateFile, "r") as myfile:

        outputDocument = os.path.join(savePath, "objectProgram.txt")
        with open(outputDocument, "w", encoding='utf-8') as fileWrite:
           
            if myfile.mode == "r":

                # for each line of text
                for fileLine in myfile:
                    # add to list (this allows access to the next line's locctr)
                    fileLines.append(fileLine)

                #print(fileLines)

                # for each element in list
                j = 0
                while j < len(fileLines):
                    objCode = ""
                    fileContent = fileLines[j]                   
                   
                    # fileLines is entire document
                    # fileContent is individual lines
             
                    # for each line of text
                    # take first section of line (usually has OPCODE)
                    # compare that section to OPCODE TABLE

                    # separate each line into sections (based on column)
                    searchR = re.split('\s+', fileContent)
                    section1 = searchR[0] # LOCCTR from pass 1
                    section2 = searchR[1] # mostly empty, lables
                    section3 = searchR[2] # opcodes
                    section4 = searchR[3] #actual data like #3, ALPHA,X, RESW value 100

                    if section3 == "START":
                        fileWrite.write(section1 + "\t"+ section2 + "\t" + section3 + "\t" + section4 + "\n")
                    elif section3 == "WORD" or section3 == "RESW" or section3 == "RESB" or section3 == "BYTE":
                        fileWrite.write(section1 + "\t"+ section2 + "\t" + section3 + "\t" + section4 + "\t")
                    else:
                        fileWrite.write(section1 + "\t"+ section2 + "\t" + section3 + "\t" + section4 + "\t")
                        opcodeFound = False
                        # open the OPCODE TABLE
                        opcodeTableFile = os.path.join(savePath, 'opcodeTable.txt')
                        with open (opcodeTableFile, "r") as optab:
                            for opline in optab:
                                # split the data into a list by line
                                searchO = re.split('\s+', opline)
                                # first part is the mnemonic
                                mnemonic = searchO[0]
                                # make instruction length an integer
                                instructLen = int(searchO[1])
                                # make the opcode into a hex value
                                opCodeInt = int(searchO[2], 16)
                                
                                # if the opcode from the program is in the opcode table
                                if section3 == mnemonic:
                                    # get the binary value of the opCode
                                    binCode = (bin(opCodeInt))
                                    # convert to string to remove leading 0b
                                    binCode = str(binCode)
                                    binCode = binCode[2:]
                                    
                                    # add leading 0s until length of 8
                                    for y in range(7):
                                        if len(binCode) < 8:
                                            binCode = "0" + binCode
                                   

                                    # for register to register (ADDR, COMPR, TIXR)
                                    if instructLen == 2:
                                        # value from symtab for first register
                                        first = symtab[section4[0]] 
                                        # value from symtab for second register
                                        second = symtab[section4[-1]]
                                        # concatenate the strings
                                        ta = first + second                         
                                        # convert binary opcode to hex string, then concatenate       
                                        binCode = hex(int((binCode), 2))
                                         
                                        objCode = binCode + ta
                                        # remove leading 0x
                                        objCode = objCode[2:]
                                        # conver to all upper case
                                        objCode = objCode.upper()
                                        

                                    # for typical nixbpe
                                    elif instructLen == 3:
                                        # remove last two 0s to make room for nixbpe
                                        binCode = binCode[:6] 
                                        

                                        # find the nixbpe info
                                        n = "1"
                                        i = "1"
                                        x = "0"
                                        b = "0"
                                        p = "1"
                                        e = "0"

                                        # if immediate addressing
                                        if section4[0] == "#":
                                            n = "0"
                                            p = "0"

                                        # if indexed addressing
                                        if section4[-2:] == ",X":
                                            x = "1"
                                        
                                        # find the displacement (TA - PC, TA-B, TA)

                                        # if pc-relative
                                        if p == "1" and x == "0":
                                            # target address = TA - PC (next section1)
                                            ta = "0x" + (symtab[section4])
                                            pc = "0x" + (fileLines[j+1][0:4])
                                           

                                            # turns ta and pc into binary strings of hex value                                
                                            ta = bin(int((ta), 16))
                                            pc = bin(int((pc), 16))
                                            # cuts off the leading 0b
                                            ta = ta[2:]
                                            pc = pc[2:]
                                            # turns ta and pc into decimal ints???
                                            ta = int((ta), 2)
                                            pc = int((pc), 2)

                                            # disp is the correct decimal value
                                            disp = ta - pc
                                            
                                            # if disp is negative
                                            if disp < 0:
                                                # make into binary string
                                                disp = bin(disp)
                                                # remove leading "-0b"
                                                disp = disp[3:]
                                                # create a flipped disp
                                                flipDisp = ""
                                                # for length less than 12, add leading 1 to flipDisp
                                                a = len(disp)
                                                while a < 12:
                                                    flipDisp = "1" + flipDisp
                                                    a += 1

                                                for y in range(len(disp)):
                                                    if disp[y] == "1":
                                                        flipDisp = flipDisp + "0"
                                                    elif disp[y] == "0":
                                                        flipDisp = flipDisp + "1"
                                                # add flipDisp + 1 (in binary!)
                                                flipDisp = "0b" + flipDisp
                                                flipDisp = int(flipDisp, 2)
                                                disp = flipDisp + 1

                                            # turns disp into hex string
                                            disp = hex(disp)
                                            

                                            # remove leading 0x
                                            disp = disp[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(disp) < 3:
                                                    disp = "0" + disp
                                            

                                            # binCode + nixbpe + disp
                                            # objCode is string of 12 binary bits
                                            objCode = binCode + n + i + x + b + p + e
                                            
                                            # convert to decimal integer
                                            objCode = int((objCode), 2)
                                            
                                            objCode = hex(objCode)
                                            

                                            # remove leading 0x
                                            objCode = objCode[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(objCode) < 3:
                                                    objCode = "0" + objCode
                                           

                                            objCode = objCode + disp
                                            objCode = objCode.upper()
                                           

                                        # if pc-relative indexed addressing
                                        if p == "1" and x == "1":
                                            # split section4 at ,
                                            section4 = section4.split(",")

                                            # ta and pc need to be hex ints

                                            # turns ta and pc into hex strings
                                            ta = "0x" + (symtab[section4[0]])
                                            pc = "0x" + (fileLines[j+1][0:4])
                                            
                                            # turns ta and pc into binary strings of hex value                                
                                            ta = bin(int((ta), 16))
                                            pc = bin(int((pc), 16))
                                            # cuts off the leading 0b
                                            ta = ta[2:]
                                            pc = pc[2:]
                                            # turns ta and pc into decimal ints???
                                            ta = int((ta), 2)
                                            pc = int((pc), 2)

                                            # disp is the correct decimal value
                                            disp = ta - pc
                                           
                                            # turns disp into hex string
                                            disp = hex(disp)
                                            

                                            # remove leading 0x
                                            disp = disp[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(disp) < 3:
                                                    disp = "0" + disp
                                           

                                            # binCode + nixbpe + disp
                                            # objCode is string of 12 binary bits
                                            objCode = binCode + n + i + x + b + p + e
                                            
                                            # convert to decimal integer
                                            objCode = int((objCode), 2)
                                            
                                            objCode = hex(objCode)
                                            

                                            # remove leading 0x
                                            objCode = objCode[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(objCode) < 3:
                                                    objCode = "0" + objCode
                                            

                                            objCode = objCode + disp
                                            objCode = objCode.upper()
                                            

                                        # if base relative
                                        if b == "1":
                                            # TA = TA - B (symtab locctr value)
                                            # split section4 at ,
                                            #section4 = section4.split(",")
                                            #ta = symtab[section4[0]]
                                            break

                                        # if immediate addressing
                                        if b == "0" and p == "0":    
                                            # take the value after the # and turn it into hex value
                                            disp = int(section4[1:], 16)
                                            

                                            disp = hex(disp)
                                            
                                            # remove leading 0x
                                            disp = disp[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(disp) < 3:
                                                    disp = "0" + disp
                                            

                                            # binCode + nixbpe + disp
                                            # objCode is string of 12 binary bits
                                            objCode = binCode + n + i + x + b + p + e
                                            
                                            # convert to decimal integer
                                            objCode = int((objCode), 2)
                                            
                                            objCode = hex(objCode)
                                           
                                            # remove leading 0x
                                            objCode = objCode[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(objCode) < 3:
                                                    objCode = "0" + objCode
                                            

                                            objCode = objCode + disp
                                            objCode = objCode.upper()
                                            
                                    
                                    opcodeFound = True
                                    break
                            if not opcodeFound:
                                print("Error! No opcode has been found!")

                    fileWrite.write(objCode + "\n")
                    j += 1

################################################################################################
# This section makes the Text Record

fileLines2 = []
objCodeList = []

objectProgram = os.path.join(savePath, "objectProgram.txt")
# This will automatically close the file after reading it
with open (objectProgram, "r") as myfile:
    
    outputDocument = os.path.join(savePath, "textRecord.txt")

    with open(outputDocument, "w", encoding='utf-8') as fileWrite:
        
        if myfile.mode == "r":

            # for each line of text
            for fileLine in myfile:
                # add to list (this allows access to the next line's locctr)
                fileLines2.append(fileLine)

            firstTime = True
            j = 0
            while j < len(fileLines2):
                fileContent = fileLines2[j]
                        
                # separate each line into sections (based on column)
                searchR = re.split('\s+', fileContent)
                section1 = searchR[0] # LOCCTR from pass 1
                section2 = searchR[1] # mostly empty, lables
                section3 = searchR[2] # opcodes
                section4 = searchR[3] # actual data like #3, ALPHA,X, RESW value 100
                section5 = searchR[4] # object codes

                # program name should be 6 characters long
                if len(programName) > 6:
                    programName = (programName.upper())[:6]
                elif len(programName) < 6:
                    for y in range(6):
                        if len(programName) < 6:
                            programName = programName + " "

                # write header and beginning of text section
                if j == 0:
                    begin = section1
                    programLength = programLength[2:]
                    fileWrite.write("H" + (programName.upper()) + "00" + begin + "00" + programLength + "\n")
                    fileWrite.write("T" + "00" + begin)

                if section5:   
                    objCodeList.insert(j, section5)

                # find last section1 where same section4 not empty
                # take that section1 and subtract value of begin
                # this is length of text record
                if not section5 and firstTime:
                    end = fileLines2[j-1][0:4]
                    end = "0x" + end
                    begin = "0x" + begin
                    end = int(end, 16)
                    begin = int(begin, 16)
                    total = end - begin
                    total = hex(total)
                    total = total[2:]
                    fileWrite.write(total)
                    firstTime = False

                j += 1

            # check the object codes for length of 6
            for k in range(len(objCodeList)):
                tempObjCode = objCodeList[k]
                if len(tempObjCode) < 6:
                    tempObjCode = "0" + tempObjCode

                # write rest of text section
                fileWrite.write(tempObjCode)
            
            # write end record
            fileWrite.write("\n" + "E" + "00" + str(begin))


def main():

    passOne()
    passTwo()



if __name__ == "__main__":
    main()

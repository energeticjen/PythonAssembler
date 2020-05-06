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

#Initialize LOCCTR to 1000
locctr = 1000

def passOne():

    global symtab
    global locctr

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
                        locctr = int(section3)
                        programName = section1
                    
                    fileWrite.write(str(locctr) + "\t")

                    # if there is a symbol in the LABEL field (section 1)
                    if section1 != "":
                        # if symbol not in symtab, add it and the locctr value (location)
                        if section1 not in symtab:
                            symtab[section1] = locctr
                        # if symbol already there, set error flag
                        else:
                            # *** THE ERROR FLAG COULD GO IN SECTION 1 OR 4 TO BE CHECKED FOR IN PASS 2 ***
                            print("Error! This symbol has already been used!")
                    else:
                        # something needs to placed to maintain proper spacing
                        section1 = "*"

                    if section2 == "WORD":
                        locctr = locctr + 3
                    elif section2 == "RESW":
                        locctr = locctr + (int(section3)*3)
                    elif section2 == "RESB":
                        locctr == locctr + int(section3)
                    #elif section2 == "BYTE":
                        # no freaking clue
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
                                # *** BOTH OF THESE STEPS MAY NOT BE NEEDED ***
                                opCodeInt = int(searchO[2], 16)
                                opCode = hex(opCodeInt)
                                # if the opcode from the program is in the opcode table
                                if section2 == mnemonic:
                                    # add the related instruction length to the locctr
                                    locctr = locctr + instructLen
                                    opcodeFound = True
                                    break
                            if not opcodeFound:
                                # *** THE ERROR FLAG COULD GO IN SECTION 1 OR 4 TO BE CHECKED FOR IN PASS 2 ***
                                print("Error! No opcode has been found!")

                    fileWrite.write(section1 + "\t" + section2 + "\t" + section3 + "\n")
    
    fileWrite.close()

    # Save LOCCTR as program length  
    programLength = locctr

#########################################################################################################

def passTwo():
    global locctr
    global symtab

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
                    #print(j)
                    #print(fileContent)
                   
                    # fileLines is entire document
                    # fileContent is individual lines
             
                    # for each line of text
                    #take first section of line (usually has OPCODE)
                    #compare that section to OPCODE TABLE

                    # separate each line into sections (based on column)
                    searchR = re.split('\s+', fileContent)
                    section1 = searchR[0] # LOCCTR from pass 1
                    section2 = searchR[1] # mostly empty, lables
                    section3 = searchR[2] # opcodes
                    section4 = searchR[3] #actual data like #3, ALPHA,X, RESW value 100

                    if section3 == "START":
                        fileWrite.write(section1 + "\t"+ section2 + "\t" + section3 + "\t" + section4 + "\n")
                    # I think this next little section about WORD, RESW, RESB is not needed in pass 2
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
                                    print(mnemonic)
                                    print(binCode)
                                    # add leading 0s until length of 8
                                    for y in range(7):
                                        if len(binCode) < 8:
                                            binCode = "0" + binCode
                                    print(binCode)
                                    print("")

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
                                        print(binCode) 
                                        objCode = binCode + ta
                                        # remove leading 0x
                                        objCode = objCode[2:]
                                        # conver to all upper case
                                        objCode = objCode.upper()
                                        print(objCode)

                                    # for typical nixbpe
                                    elif instructLen == 3:
                                        # remove last two 0s to make room for nixbpe
                                        binCode = binCode[:6] 
                                        #print(binCode)

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
                                            ta = hex(symtab[section4])
                                            pc = hex(int(fileLines[j+1][0:4]))
                                            print("p = 1")
                                            print(ta)
                                            print(pc)

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
                                            print(disp)

                                            # if disp is negative
                                            if disp < 0:
                                                # make into binary string
                                                disp = bin(disp) 
                                                print(int(disp, 2))
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
                                            print(disp)

                                            # remove leading 0x
                                            disp = disp[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(disp) < 3:
                                                    disp = "0" + disp
                                            print(disp)

                                            # binCode + nixbpe + disp
                                            # objCode is string of 12 binary bits
                                            objCode = binCode + n + i + x + b + p + e
                                            print(objCode)
                                            # convert to decimal integer
                                            objCode = int((objCode), 2)
                                            print(objCode)
                                            objCode = hex(objCode)
                                            print(objCode)

                                            # remove leading 0x
                                            objCode = objCode[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(objCode) < 3:
                                                    objCode = "0" + objCode
                                            print(objCode)

                                            objCode = objCode + disp
                                            objCode = objCode.upper()
                                            print(objCode)

                                        # if pc-relative indexed addressing
                                        if p == "1" and x == "1":
                                            # split section4 at ,
                                            section4 = section4.split(",")

                                            # ta and pc need to be hex ints

                                            # turns ta and pc into hex strings
                                            ta = hex(symtab[section4[0]])
                                            pc = hex(int(fileLines[j+1][0:4]))
                                            #print("p = 1 and x = 1")
                                            #print(ta)
                                            #print(pc)
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
                                            #print(disp)
                                            # turns disp into hex string
                                            disp = hex(disp)
                                            print(disp)

                                            # remove leading 0x
                                            disp = disp[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(disp) < 3:
                                                    disp = "0" + disp
                                            print(disp)

                                            # binCode + nixbpe + disp
                                            # objCode is string of 12 binary bits
                                            objCode = binCode + n + i + x + b + p + e
                                            print(objCode)
                                            # convert to decimal integer
                                            objCode = int((objCode), 2)
                                            print(objCode)
                                            objCode = hex(objCode)
                                            print(objCode)

                                            # remove leading 0x
                                            objCode = objCode[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(objCode) < 3:
                                                    objCode = "0" + objCode
                                            print(objCode)

                                            objCode = objCode + disp
                                            objCode = objCode.upper()
                                            print(objCode)

                                        # if base relative
                                        if b == "1":
                                            # TA = TA - B (symtab locctr value)
                                            # split section4 at ,
                                            #section4 = section4.split(",")
                                            #ta = symtab[section4[0]]
                                            print("skipping for now")

                                        # if immediate addressing
                                        if b == "0" and p == "0":    
                                            # take the value after the # and turn it into hex value
                                            disp = int(section4[1:], 16)
                                            print(disp)

                                            disp = hex(disp)
                                            
                                            # remove leading 0x
                                            disp = disp[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(disp) < 3:
                                                    disp = "0" + disp
                                            print(disp)

                                            # binCode + nixbpe + disp
                                            # objCode is string of 12 binary bits
                                            objCode = binCode + n + i + x + b + p + e
                                            print(objCode)
                                            # convert to decimal integer
                                            objCode = int((objCode), 2)
                                            print(objCode)
                                            objCode = hex(objCode)
                                            print(objCode)

                                            # remove leading 0x
                                            objCode = objCode[2:]

                                            # add leading 0s until length of 3
                                            for y in range(2):
                                                if len(objCode) < 3:
                                                    objCode = "0" + objCode
                                            print(objCode)

                                            objCode = objCode + disp
                                            objCode = objCode.upper()
                                            print(objCode)

                                    # concatenate and turn into hex, save as objectCode
                                    print("we're getting there!")
                                    
                                    opcodeFound = True
                                    break
                            if not opcodeFound:
                                print("Error! No opcode has been found!")

                    fileWrite.write(objCode + "\n")
                    j += 1

        '''
        for LDA ALPHA, X :
        the disp still = ta - pc
        and the p = 1 in the nixbpe
        nixbpe = 111010
        and the ta = where ALPHA is stored (in this case)

        if opCode = Start
            write line
            read next line
        write header to object program
        open new text record
        while opCode != end
            if not a comment
                search OPTab for opCode
                if found
                    if there is a symbol in operand field
                        search symtab for operand
                        if found
                            store symbol as operand address
                        else
                            store 0 as operand address
                            error "symbol not found"
                    else	
                        store 0 as operand address
                    assemble object code
                else if	opCode = byte or word
                    convert constant to object
                if object code doesn't fit into text record
                    write to object program
                    create new text record
                add object code to text record
            write listing line
            read next line
        write last text record to object program
        write end record to object program
        write last listing line'''



def main():

    passOne()
    passTwo()



if __name__ == "__main__":
    main()
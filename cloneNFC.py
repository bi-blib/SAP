import os

numBytes = 16
numBlocks = 4

def grabKeyA(cardInfo, sectorNo):
    # Try standard keys first
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
    keyA = sectorTrailer[0:6]

    from formattedKeys import knownKeys
    for key in knownKeys:
        if (key == keyA):
            return key

    # This could take up to 3 days (longer on a regular laptop)
    for i in range(0, 16**6):
        bruteForceKey = format(i, '012x')
        if (bruteForceKey == keyA):
            return bruteForceKey

def grabKeyB(cardInfo, sectorNo):
    # Try standard keys first
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  
    keyB = sectorTrailer[10:16]
    from formattedKeys import knownKeys
    for key in knownKeys:
        if (key == keyB):
            return key

    # This could take up to 3 days (longer on a regular laptop)
    for i in range(0, 16**6):
        bruteForceKey = format(i, '012x')
        if (bruteForceKey == keyB):
            return bruteForceKey

################################################################################
##################### Key Cracking is above / Read is below ####################
################################################################################
def validKeyFormat(key):
    return len(key) == 6

################ Helper: collect and format a key from user input ##############
def readKey(question):
    while True:
        rawKey = input(question)  
        rawKey = rawKey.strip()   
        # Check if the input starts with '0x'
        if rawKey.startswith("0x"):
            key = int(rawKey, 16)  
            # Store the key as 6 bytes
            keyBytes = key.to_bytes(6, byteorder='big')  
                
            if (validKeyFormat(keyBytes) == False):
                print("Invalid key: Must be 6 bytes long.")
                continue
                
            return keyBytes  # Return the bytes object
        else:
            print("Please enter the key starting with '0x'.")

################ Collects the data of a sector of the cloned card ##############
def fetchSectorInfo(cardInfo, sectorNo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
    access = sectorTrailer[6:9]

    halfAccess = int.from_bytes(access, byteorder='little') & 0xFFF
    group1 = 0
    group2 = 0 
    group3 = 0 
    group4 = 0
    for x in range(3):
        for y in range(4):
            if (y == 0):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group1 += 1
            elif (y == 1):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group2 += 1
            elif (y == 2):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group3 += 1
            elif (y == 3):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group4 += 1
        
    keyA = grabKeyA(cardInfo, sectorNo)                       # Brute Force KeyA
    keyB = grabKeyB(cardInfo, sectorNo)                       # Brute Force KeyB

    sectorData = collectDataBlock(sectorNo, keyA, keyB, group1, group4, 0, cardInfo)
    sectorData += collectDataBlock(sectorNo, keyA, keyB, group2, group4, 1, cardInfo)
    sectorData += collectDataBlock(sectorNo, keyA, keyB, group3, group4, 2, cardInfo)
    sectorData += collectDataSector(sectorNo, keyA, keyB, group4, 3, cardInfo)
    return sectorData

############### Determines whether data block is collectable ###################
def collectDataBlock(sectorNo, keyA, keyB, groupAccess, sectorAccess, groupNo, cardInfo):
    if (correctDataKey(sectorNo, groupAccess, sectorAccess, groupNo, keyA, cardInfo) == True):
        return readData(sectorNo, groupAccess, sectorAccess, groupNo, keyA, cardInfo)        
    elif (useableKeyB(sectorAccess) == True):
        if (correctDataKey(sectorNo, groupAccess, sectorAccess, groupNo, keyB, cardInfo) == True):
            return readData(sectorNo, groupAccess, sectorAccess, groupNo, keyB, cardInfo)

    return b'\x00' * 16              # Data is unreadable so block is left blank

############### Collects the data block of card being cloned ###################
def readData(sectorNo, access, trailerAccess, group, key, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  
    blockNum = sectorNo * 4 + group
    blockData = cardInfo[blockNum * 16:(blockNum + 1) * 16]

    if (access == 0b111):
        return b'\x00' * 16     # data is unreadable

    keyA = sectorTrailer[0:6]
    validKey = False 

    if (keyA == key and (access != 0b011 or access != 0b101)):
        return blockData

    # Ensure that the keyB is able to be used to authenticate based on trailer access
    if (useableKeyB(trailerAccess) == True):
        keyB = sectorTrailer[10:16]
        if (keyB == key):
            return blockData

    # Block 0 is always readable
    if (sectorNo == 0 and group == 0):
        return blockData
    
    return b'\x00' * 16

############# Collects the sectorTrailer of card being clones ##################
def collectDataSector(sectorNo, keyA, keyB, sectorAccess, groupNo, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):] 

   
    accessBits = sectorTrailer[6:10]

    actualKeyA = sectorTrailer[0:6]
    actualKeyB = sectorTrailer[10:16]


    trailerData = actualKeyA

    if (keyA == actualKeyA):
        trailerData += sectorTrailer[6:10]
    elif ((keyB == actualKeyB) and 
          (sectorAccess != 0b000 and sectorAccess != 0b010 and sectorAccess != 0b001)):
        trailerData += sectorTrailer[6:10]
    else:
        trailerData += b'\x00' * 4

    trailerData += actualKeyB

    return trailerData

################# Verifies if the key can read data block #####################
def correctDataKey(sectorNo, access, trailerAccess, group, key, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  
    blockNum = sectorNo * 4 + group

    if (access == 0b111):
        return False

    keyA = sectorTrailer[0:6]
    validKey = False 

    if (keyA == key and (access != 0b011 or access != 0b101)):
        return True

    # Ensure that the keyB is able to be used to authenticate based on trailer access
    if (useableKeyB(trailerAccess) == True):
        keyB = sectorTrailer[10:16]
        if (keyB == key):
            return True

    # Block 0 is always readable
    if (sectorNo == 0 and group == 0):
        return True
    return False

################# Helper: keyB is able to authorise access #####################
def useableKeyB(access):
    if (access == 0): return True
    elif (access == 0b010): return True
    elif (access == 0b001): return True
    return False

######################### Helper: returns file data ############################
def openCardFile(filename):
    with open(filename, 'rb') as f:
        return f.read()

######################### Helper: returns file data ############################
def initiateReadCommunication(cardFile):
    cardInfo = openCardFile(cardFile)
    clonedData = b""                                       # Initialise to bytes
    for sectorNo in range(16):
        clonedData += fetchSectorInfo(cardInfo, sectorNo)
    return clonedData

#################### Maximises read access to cloned card ######################
def cardIsFullReadable(filename):
    cardInfo = openCardFile(filename)
    for sectorNo in range(16):
        sectorIsReadable(sectorNo, cardInfo)

#################### Maximises read access to cloned card ######################
def sectorIsReadable(sectorNo, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]     # Collect trailer from last 16 bytes
    access = sectorTrailer[6:9]

    halfAccess = int.from_bytes(access, byteorder='little') & 0xFFF
    group1 = 0
    group2 = 0 
    group3 = 0 
    group4 = 0
    for x in range(3):
        for y in range(4):
            if (y == 0):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group1 += 1
            elif (y == 1):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group2 += 1
            elif (y == 2):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group3 += 1
            elif (y == 3):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group4 += 1
    
    sectorReadable = True
    accessModifiable = False
    newAccess = int.from_bytes(access, byteorder='little') & 0xFFFFFF
    if (group1 == 0b111 and sectorNo != 0):
        if (group4 == 0b001 or group4 == 0b011 or group4 == 0b101):
            accessModifiable = True
            newAccess = newAccess & 0b111011101110111011101110          # Sets block0 to transport configuration
            print(f'Changing access bits of sector {sectorNo} to transport configuration to retrieve data block 1')
        else:
            print(f'Unable to access {sectorNo} retrievea data block 2')
        sectorReadable = False
    if (group2 == 0b111):
        if (group4 == 0b001 or group4 == 0b011 or group4 == 0b101):
            accessModifiable = True
            newAccess = newAccess & 0b110111011101110111011101           # Sets block1 to transport configuration
            print(f'Changing access bits of sector {sectorNo} to transport configuration to retrieve data block 2')
        else:
            print(f'Unable to access {sectorNo} retrieve data block 2')
        sectorReadable = False
    if (group3 == 0b111):
        if (group4 == 0b001 or group4 == 0b011 or group4 == 0b101):
            accessModifiable = True
            newAccess = newAccess & 0b101110111011101110111011            # Sets block2 to transport configuration
            print(f'Changing access bits of sector {sectorNo} to transport configuration to retrieve data block 3')
        else:
            print(f'Unable to access {sectorNo} retrieve data block 2')
        sectorReadable = False

    # If needed and possible, change accessBits to sector to make data readable
    if (sectorReadable == False and accessModifiable == True):            
        with open(filename, 'rb+') as f:   
            offset = offset + (3 * numBytes) + 6
            f.seek(offset)
            f.write(newAccess)

################################################################################
######################## Read is above / Write is below ########################
################################################################################

def initiateWriteCommunication(filename, clonedData):
    with open(filename, 'rb') as f:
        cardInfo = f.read()
    
    for sectorNo in range(16):
        if (accessSector(cardInfo, sectorNo) == False):
            print("Unauthorised access to write to a sector, provide a blank card to clone to")
            exit()
        else:
            offset = sectorNo * (numBlocks * numBytes)
            sectorData = clonedData[offset : offset + (numBlocks * numBytes)]
            # Add a check that sector
            with open(filename, 'rb+') as f:
                f.seek(offset)
                f.write(sectorData)


def accessSector(cardInfo, sectorNo):
    # Check if any standard or common key can authenticate the card.
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
    # Add a check if keyB is readable
    access = sectorTrailer[6:9]
    accessBits = f"{int.from_bytes(access, byteorder='little'):024b}"

    halfAccess = int.from_bytes(access, byteorder='little') & 0xFFF
    group1 = 0
    group2 = 0 
    group3 = 0 
    group4 = 0
    for x in range(3):
        for y in range(4):
            if (y == 0):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group1 += 1
            elif (y == 1):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group2 += 1
            elif (y == 2):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group3 += 1
            elif (y == 3):
                if (halfAccess >> (x * 4 + y)) & 1:
                    group4 += 1

    if (group4 != 0b001 and group4 != 0b011):
        return False

    foundKeyA = grabKeyA(cardInfo, sectorNo)
    foundKeyB = grabKeyB(cardInfo, sectorNo)

    if (sectorNo == 0):
        if (writeBlockData(foundKeyA, foundKeyB, sectorNo, group2, group4, 1, cardInfo) == False 
            or writeBlockData(foundKeyA, foundKeyB, sectorNo, group3, group4, 2, cardInfo) == False):
            return False
    else: 
        if (writeBlockData(foundKeyA, foundKeyB, sectorNo, group1, group4, 0, cardInfo) == False
            or writeBlockData(foundKeyA, foundKeyB, sectorNo, group2, group4, 1, cardInfo) == False 
            or writeBlockData(foundKeyA, foundKeyB, sectorNo, group3, group4, 2, cardInfo) == False):
            return False
    
    return True

def writeBlockData(foundKeyA, foundKeyB, sectorNo, access, trailerAccess, group, cardInfo):
    if (access == 0b010 or access == 0b001 or access == 0b101 or access == 0b111):
        return False

    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  

    keyA = sectorTrailer[0:6]
    
    validKey = False 
    if (keyA == foundKeyA and access == 0):
        validKey = True
 
    # Ensure that the keyB is able to be used to authenticate based on trailer access
    if (useableKeyB(trailerAccess) == True):
        keyB = sectorTrailer[10:16]
        if (keyB == foundKeyB):
            validKey = True

    if (validKey):
        if (trailerAccess == 0b001 and keyA == foundKeyA):
            return True
        elif (trailerAccess == 0b011 and keyB == foundKeyB):
            return True
    return False

################################################################################
######################## Write is above / Main is below ########################
################################################################################
while (True):
    filename = str(input("What is the name of the NFC Card File you would like to clone? "))
    filename = filename.strip()     
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break
# Will try to maximise read access where possible or inform use of unclonable data blocks
cardIsFullReadable(filename)                        
clonedData = initiateReadCommunication(filename)


while (True):
    filename = str(input("What is the name of the NFC Card File recieving the clone? "))
    filename = filename.strip()     
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break

initiateWriteCommunication(filename, clonedData)
print("Successful cloning completed!")

import os
standardKeys = [
    b'\xFF\xFF\xFF\xFF\xFF\xFF',
    b'\xA0\xA1\xA2\xA3\xA4\xA5',
    b'\xD3\xF7\xD3\xF7\xD3\xF7',
    b'\x00\x00\x00\x00\x00\x00'
]

knownCommonKeys = [
    b'\xB0\xB1\xB2\xB3\xB4\xB5',
    b'\x4D\x3A\x99\xC3\x51\xDD',
    b'\x1A\x98\x2C\x7E\x45\x9A',
    b'\xAA\xBB\xCC\xDD\xEE\xFF',
    b'\x71\x4C\x5C\x88\x6E\x97',
    b'\x58\x7E\xE5\xF9\x35\x0F',
    b'\xA0\x47\x8C\xC3\x90\x91',
    b'\x53\x3C\xB6\xC7\x23\xF6',
    b'\x8F\xD0\xA4\xF2\x56\xE9',
    b'\xA6\x45\x98\xA7\x74\x78',
    b'\x26\x94\x0B\x21\xFF\x5D',
    b'\xFC\x00\x01\x87\x78\xF7',
    b'\x00\x00\x0F\xFE\x24\x88',
    b'\x5C\x59\x8C\x9C\x58\xB5',
    b'\xE4\xD2\x77\x0A\x89\xBE'
    b'\x43\x4F\x4D\x4D\x4F\x41',
    b'\x43\x4F\x4D\x4D\x4F\x42',
    b'\x47\x52\x4F\x55\x50\x41',
    b'\x47\x52\x4F\x55\x50\x42',
    b'\x50\x52\x49\x56\x41\x41',
    b'\x50\x52\x49\x56\x41\x42'
    b'\x02\x97\x92\x7C\x0F\x77',
    b'\xEE\x00\x42\xF8\x88\x40',
    b'\x72\x2B\xFC\xC5\x37\x5F',
    b'\xF1\xD8\x3F\x96\x43\x14'
    b'\x54\x72\x61\x76\x65\x6C',
    b'\x77\x69\x74\x68\x75\x73',
    b'\x4A\xF9\xD7\xAD\xEB\xE4',
    b'\x2B\xA9\x62\x1E\x0A\x36'
    b'\x00\x00\x00\x00\x00\x01',
    b'\x12\x34\x56\x78\x9A\xBC',
    b'\xB1\x27\xC6\xF4\x14\x36',
    b'\x12\xF2\xEE\x34\x78\xC1',
    b'\x34\xD1\xDF\x99\x34\xC5',
    b'\x55\xF5\xA5\xDD\x38\xC9',
    b'\xF1\xA9\x73\x41\xA9\xFC',
    b'\x33\xF9\x74\xB4\x27\x69',
    b'\x14\xD4\x46\xE3\x33\x63',
    b'\xC9\x34\xFE\x34\xD9\x34',
    b'\x19\x99\xA3\x55\x4A\x55',
    b'\x27\xDD\x91\xF1\xFC\xF1',
    b'\xA9\x41\x33\x01\x34\x01',
    b'\x99\xC6\x33\x44\x33\x43',
    b'\x43\xAB\x19\xEF\x5C\x31',
    b'\xA0\x53\xA2\x92\xA4\xAF',
    b'\x50\x52\x49\x56\x54\x41',
    b'\x50\x52\x49\x56\x54\x42'
    b'\xFC\x00\x01\x87\x7B\xF7'
    b'\xA0\xB0\xC0\xD0\xE0\xF0',
    b'\xA1\xB1\xC1\xD1\xE1\xF1'
    b'\xBD\x49\x3A\x39\x62\xB6',
    b'\x01\x02\x03\x04\x05\x06',
    b'\x11\x11\x11\x11\x11\x11',
    b'\x22\x22\x22\x22\x22\x22',
    b'\x33\x33\x33\x33\x33\x33',
    b'\x44\x44\x44\x44\x44\x44',
    b'\x55\x55\x55\x55\x55\x55',
    b'\x66\x66\x66\x66\x66\x66',
    b'\x77\x77\x77\x77\x77\x77',
    b'\x88\x88\x88\x88\x88\x88',
    b'\x99\x99\x99\x99\x99\x99',
    b'\xAA\xAA\xAA\xAA\xAA\xAA',
    b'\xBB\xBB\xBB\xBB\xBB\xBB',
    b'\xCC\xCC\xCC\xCC\xCC\xCC',
    b'\xDD\xDD\xDD\xDD\xDD\xDD',
    b'\xEE\xEE\xEE\xEE\xEE\xEE',
    b'\x01\x23\x45\x67\x89\xAB',
    b'\x00\x00\x00\x00\x00\x02',
    b'\x00\x00\x00\x00\x00\x0A',
    b'\x00\x00\x00\x00\x00\x0B',
    b'\x10\x00\x00\x00\x00\x00',
    b'\x20\x00\x00\x00\x00\x00',
    b'\xA0\x00\x00\x00\x00\x00',
    b'\xB0\x00\x00\x00\x00\x00',
    b'\xAB\xCD\xEF\x12\x34\x56',
    b'\xF4\xA9\xEF\x2A\xFC\x6D'
    b'\xBD\x49\x3A\x39\x62\xB6'
    b'\x01\x02\x03\x04\x05\x06'
    b'\x11\x11\x11\x11\x11\x11'
    b'\x22\x22\x22\x22\x22\x22'
    b'\x33\x33\x33\x33\x33\x33'
    b'\x44\x44\x44\x44\x44\x44'
    b'\x55\x55\x55\x55\x55\x55'
    b'\x66\x66\x66\x66\x66\x66'
    b'\x77\x77\x77\x77\x77\x77'
    b'\x88\x88\x88\x88\x88\x88'
    b'\x99\x99\x99\x99\x99\x99'
    b'\xAA\xAA\xAA\xAA\xAA\xAA'
    b'\xBB\xBB\xBB\xBB\xBB\xBB'
    b'\xCC\xCC\xCC\xCC\xCC\xCC'
    b'\xDD\xDD\xDD\xDD\xDD\xDD'
    b'\xEE\xEE\xEE\xEE\xEE\xEE'
    b'\x01\x23\x45\x67\x89\xAB'
    b'\xAB\xCD\xEF\x12\x34\x56'
]

numBytes = 16
numBlocks = 4


def grabKeyA(cardInfo, sectorNo):
    # Try standard keys first
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
    keyA = sectorTrailer[0:6]
    
    for key in standardKeys:
        if (key == keyA):
            return key

    for key in knownCommonKeys:
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
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
    keyB = sectorTrailer[10:16]

    for key in standardKeys:
        if (key == keyB):
            return key

    for key in knownCommonKeys:
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
    elif (useableKeyB(group4) == True):
        if (correctDataKey(sectorNo, groupAccess, sectorAccess, groupNo, keyB, cardInfo) == True):
            return readData(sectorNo, groupAccess, sectorAccess, groupNo, keyB, cardInfo)

    return b'\x00' * 16              # Data is unreadable so block is left blank

############### Collects the data block of card being cloned ###################
def readData(sectorNo, access, trailerAccess, group, key, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
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
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes

    sectorTrailer = keyA
    actualKeyA = sectorTrailer[0:6]
    actualKeyB = sectorTrailer[10:16]

    if (keyA == actualKeyA):
        sectorTrailer += sectorTrailer[6:10]
    elif ((keyB == actualKeyB) and 
          (sectorAccess != 0b000 and sectorAccess != 0b010 and sectorAccess != 0b001)):
        sectorTrailer += sectorTrailer[6:10]
    else:
        sectorTrailer += b'\x00' * 4
    sectorTrailer += keyB

    return sectorTrailer

################# Verifies if the key can read data block #####################
def correctDataKey(sectorNo, access, trailerAccess, group, key, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes
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
    print(f'access bytes {access}')
    accessBits = f"{int.from_bytes(access, byteorder='little'):024b}"
    print(f'access bits {accessBits}')

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
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes

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
print(f'{clonedData}')

while (True):
    filename = str(input("What is the name of the NFC Card File recieving the clone? "))
    filename = filename.strip()     
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break

initiateWriteCommunication(filename, clonedData)

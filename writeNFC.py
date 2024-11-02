import os

# Will write to a card if sector allows for it. 

numBytes = 16
numBlocks = 4

def validKeyFormat(key):
    return len(key) == 6

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

def initiateCommunication(filename):
    """Ask for the key"""
    with open(filename, 'rb') as f:
        cardInfo = f.read()
    cardUID = getUID(cardInfo)
    print(f"Card UID: {cardUID.hex()}")
    
    while (True):
        sectorNo = int(input("Which sector (0-15) do you want to access? "))
        if ((sectorNo < 0) or (sectorNo > 15)):
            print("Invalid number, has to be 0-15")
        else:
            break
    if (accessSector(cardInfo, sectorNo) == False):
        print("Unauthorised access to write to this sector, change access bits first")
    else:
        while (True):
            userData = str(input("Access authorised. What do you wish to write? "))
            byteLength = len(userData.encode('utf-8')) 
            if ((sectorNo == 0 and byteLength > 32) or (byteLength > 48)):
                print(f"Byte length of {byteLength} is too large for this sector, please try again")
            else:
                break
        with open(filename, 'rb+') as f:
            offset = sectorNo * (numBlocks * numBytes)
            if (sectorNo == 0):
                offset = offset + numBytes      # don't overwrite block 0
            
            # Convert data to byte object
            f.seek(offset)
            f.write(userData.encode('utf-8'))


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
    if (sectorNo == 0):
        if (writeBlockData(sectorNo, group2, group4, 1, cardInfo) == False 
            or writeBlockData(sectorNo, group3, group4, 2, cardInfo) == False):
            return False
    else: 
        if (writeBlockData(sectorNo, group1, group4, 0, cardInfo) == False
            or writeBlockData(sectorNo, group2, group4, 1, cardInfo) == False 
            or writeBlockData(sectorNo, group3, group4, 2, cardInfo) == False):
            return False
    return True

def writeBlockData(sectorNo, access, trailerAccess, group, cardInfo):
    if (access == 0b010 or access == 0b001 or access == 0b101 or access == 0b111):
        return False
    key = readKey("What is the key for data block {}? (e.g., 0xFFFFFFFFFFFF): ".format(group))

    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes

    keyA = sectorTrailer[0:6]
    validKey = False 
    if (keyA == key and access == 0):
        validKey = True
 
    # Ensure that the keyB is able to be used to authenticate based on trailer access
    if (readableKeyB(trailerAccess) == True):
        keyB = sectorTrailer[10:16]
        if (keyB == key):
            validKey = True

    if (validKey):
        return True
    else: 
        return False

def readableKeyB(access):
    if (access == 0): return True
    elif (access == 0b010): return True
    elif (access == 0b001): return True
    return False

def getUID(cardInfo): 
    # Extract the first 4 bytes as the card UID.
    cardUID = cardInfo[:4]
    return cardUID

# Main
filename = str(input("What is the name of the MIFARE Card File? "))
filename = filename.strip()     
if not os.path.isfile(filename):
    print("Unable to find file, please try again")
else:
    initiateCommunication(filename)
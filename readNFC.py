import os

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

def initiateCommunication(cardFile):
    """Start the communication process by reading the card data."""
    cardInfo = openCardFile(cardFile)
    cardUID = getUID(cardInfo)
    print(f"Card UID: {cardUID.hex()}")
    
    while (True):
        sectorNo = int(input("Which sector (0-15) do you want to access? "))
        if ((sectorNo < 0) or (sectorNo > 15)):
            print("Invalid number, has to be 0-15")
        else: 
            break
    accessSector(cardInfo, sectorNo)


def accessSector(cardInfo, sectorNo):
    # Check if any standard or common key can authenticate the card.
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  
    
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

    if (sectorNo == 0):
        key1 = 0
    else: 
        key1 = readKey("What is the key for data block 0? (e.g., 0xFFFFFFFFFFFF): ")
    
    key2 = readKey("What is the key for data block 1? (e.g., 0xFFFFFFFFFFFF): ")
    key3 = readKey("What is the key for data block 2? (e.g., 0xFFFFFFFFFFFF): ")
    key4 = readKey("What is the key for data block 3? (e.g., 0xFFFFFFFFFFFF): ")
    readData(sectorNo, group1, group4, 0, key1, cardInfo)
    readData(sectorNo, group2, group4, 1, key2, cardInfo)
    readData(sectorNo, group3, group4, 2, key3, cardInfo)
    readSectorData(sectorNo, group4, key4, cardInfo)

def readData(sectorNo, access, trailerAccess, group, key, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  
    blockNum = sectorNo * 4 + group
    data = cardInfo[blockNum * 16:(blockNum + 1) * 16]

    if (access == 0b111):
        hexData = ' '.join("--" for _ in data)
        print(f"  Block {blockNum:02}: {hexData}")
        return


    keyA = sectorTrailer[0:6]
    keyB = sectorTrailer[10:16]
    validKey = False 

    if (keyA == key and (access != 0b011 or access != 0b101)):
        validKey = True

    # Ensure that the keyB is able to be used to authenticate based on trailer access
    if (readableKeyB(trailerAccess) == True):
        keyB = sectorTrailer[10:16]
        if (keyB == key):
            validKey = True

    # Block 0 is always readable
    if (sectorNo == 0 and group == 0):
        validKey = True

    if (validKey):
        hexData = ' '.join(f"{byte:02X}" for byte in data)
        print(f"  Block {blockNum:02}: {hexData}")
    else: 
        hexData = ' '.join("--" for _ in data)
        print(f"  Block {blockNum:02}: {hexData}")
    return

def readSectorData(sectorNo, access, key, cardInfo):
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  

    keyA = sectorTrailer[0:6]
    validAccess = False 
    if (keyA == key):
        validAccess = True
    elif ((validAccess == False) and (access != 0 and access != 0b010 and access != 0b001)):
        keyB = sectorTrailer[10:16]
        if (keyB == key):
            validAccess = True

    readKeyB = False
    if (keyA == key and (access == 0 and access == 0b010 and access == 0b001)):
        readKeyB = True
    
    printKeyA = sectorTrailer[0:6]
    printAccess = sectorTrailer[6:10]
    printKeyB = sectorTrailer[10:16]

    printKeyA =  ' '.join("--" for _ in printKeyA)
    if (validAccess):
        printAccess =  ' '.join(f"{byte:02X}" for byte in printAccess)
    else: 
        printAccess = ' '.join("--" for _ in printAccess)

    if (readKeyB):
        printKeyB =  ' '.join(f"{byte:02X}" for byte in printKeyB)
    else: 
        printKeyB = ' '.join("--" for _ in printKeyB)
    print(f"  Block {3:02}: {printKeyA} {printAccess} {printKeyB}")
    

def readableKeyB(access):
    if (access == 0): return True
    elif (access == 0b010): return True
    elif (access == 0b001): return True
    return False

def openCardFile(filename):
    with open(filename, 'rb') as f:
        return f.read()

def getUID(cardInfo): 
    # Extract the first 4 bytes as the card UID.
    cardUID = cardInfo[:4]
    return cardUID

# Main
while (True):
    filename = str(input("What is the name of your MIFARE Card File? "))
    filename = filename.strip()     
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break
initiateCommunication(filename)
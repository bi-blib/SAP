import os

# Will write to a card if sector allows for it. 

numBytes = 16
numBlocks = 4

def validKeyFormat(key):
    return len(key) == 6

def validAccessFormat(key):
    return len(key) == 3

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

def readAccess(question):
    while True:
        rawInput = input(question)  
        rawInput = rawInput.strip()   
        # Check if the input starts with '0x'
        if rawInput.startswith("0x"):
            accessBits = int(rawInput, 16)  
            # Store the key as 6 bytes
            AccessBytes = accessBits.to_bytes(3, byteorder='big')  
                
            if (validAccessFormat(AccessBytes) == False):
                print("Invalid key: Must be 3 bytes long.")
                continue
                
            return AccessBytes  # Return the bytes object
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
    
    while (True):
        areaAccess = int(input("Would you like to write 1. KeyA, 2. Access Bits, 3. KeyB (e.g. 1) "))
        if ((areaAccess < 1) or (areaAccess > 3)):
            print("Invalid number, has to be 1-3")
        else:
            break
    
    if (accessSector(cardInfo, sectorNo, areaAccess) == False):
        print("Unauthorised access to write to this area, change access bits first")
    else:
        offset = sectorNo * (numBlocks * numBytes) + (3 * numBytes)   # Start of the sectorTrailer
        if (areaAccess == 1):
            userData = readKey("Access authorised. What do you wish KeyA to be? ")
        elif (areaAccess == 2):
            userData = readAccess("Access authorised. What do you wish AccessBits to be? (e.g., 0x000880): ")
            offset = offset + 6
        else: 
            userData = readKey("Access authorised. What do you wish KeyB to be? ")
            offset = offset + 10 
        
        with open(filename, 'rb+') as f:   
            # Convert data to byte object
            f.seek(offset)
            f.write(userData)

def accessSector(cardInfo, sectorNo, areaAccess):
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
    if (areaAccess == 1 or areaAccess == 3):
        return writeAccessKey(sectorNo, group4, cardInfo)
    else: 
        return writeAccessBits(sectorNo, group4, cardInfo)


def writeAccessKey(sectorNo, access, cardInfo):
    # Access to write is completely locked
    if (access == 0b010 or access == 0b110 or access == 0b101 or access == 0b111):
        return False
    key = readKey("What is the key for this data? (e.g., 0xFFFFFFFFFFFF): ")

    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes

    keyA = sectorTrailer[0:6]
    validKey = False 
    if (keyA == key and (access == 0 or access == 0b001)):
        return True
 
    # Ensure that the keyB is able to be used to authenticate based on trailer access
    keyB = sectorTrailer[10:16]
    if (keyB == key and (access == 0b100 or access == 0b011)):
        return True
    
    return False

def writeAccessBits(sectorNo, access, cardInfo):
    # Access to write is completely locked
    if (access != 0b001 and access != 0b011 and access != 0b101):
        return False
    
    key = readKey("What is the key for this data? (e.g., 0xFFFFFFFFFFFF): ")

    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes

    keyA = sectorTrailer[0:6]
    validKey = False 
    if (keyA == key and access == 0b001):
        return True
 
    # Ensure that the keyB is able to be used to authenticate based on trailer access
    keyB = sectorTrailer[10:16]
    if (keyB == key and (access == 0b011  or access == 0b101)):
        return True
    
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
while (True):
    filename = str(input("What is the name of the MIFARE Card File? "))
    filename = filename.strip()     
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break
initiateCommunication(filename)
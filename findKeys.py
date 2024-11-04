import os

numBytes = 16
numBlocks = 4

def initiateCommunication(cardFile):
    """Start the communication process by reading the card data."""
    cardInfo = openCardFile(cardFile)
    cardUID = getUID(cardInfo)
    print(f"Card UID: {cardUID.hex()}")
    
    sectorNo = int(input("Which sector (0-15) do you need the key for? "))
    if ((sectorNo < 0) or (sectorNo > 15)):
        print("Invalid number, has to be 0-15")
    else: 
        checkCommonKeys(cardInfo, sectorNo)

def checkCommonKeys(cardInfo, sectorNo):
    # Check if any standard or common key can authenticate the card.
    offset = sectorNo * (numBlocks * numBytes)
    sectorTrailer = cardInfo[-(offset + numBytes):]  # Assuming sector trailer is the last 16 bytes

    keyA = sectorTrailer[0:6]
    
    # Add a check if keyB is readable
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

    # Try standard keys first
    foundKeyA = False
    foundKeyB = False

    from formattedKeys import knownKeys
    for key in knownKeys:
        if (key == keyA):
            print(f"Authentication succeeded with Key A: {key.hex()}")
            foundKeyA = True
            break
    
    # Look for KeyB
    if (readableKeyB(group4) == True):
        keyB = sectorTrailer[10:16]
        for key in knownKeys:
            if (key == keyB):
                print(f"Authentication succeeded with Key B: {key.hex()}")
                foundKeyB = True
                break
    else: 
        print("KeyB is not readable from Sector Trailer")

    if ((foundKeyA == False) and (foundKeyB == False)):
        print("Unable to find keys amongst common values, attempting to brute force could take up to 3 days")

    for i in range(0, 16**6):
        bruteForceKey = format(i, '012x')
        if (bruteForceKey == keyA):
            foundKeyA = True
            print(f"Authentication succeeded with Key A: {key.hex()}")
            
        if (bruteForceKey == keyB):
            foundKeyB = True
            print(f"Authentication succeeded with Key B: {key.hex()}")
            return bruteForceKey

        if ((foundKeyA == True) and (foundKeyB == True)):
            break

def readableKeyB(access):
    if (access == 0): return True
    elif (access == 0b010): return True
    elif (access == 0b001): return True
    return False

def openCardFile(filename):
    """Read the card file and return its content."""
    with open(filename, 'rb') as f:
        return f.read()

def getUID(cardInfo): 
    # Extract the first 4 bytes as the card UID.
    cardUID = cardInfo[:4]
    return cardUID

# Main
while (True):
    filename = str(input("What is the name of your MIFARE Card File? "))
    filename = filename.strip()     # Strip any leading or trailing whitespace
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break
initiateCommunication(filename)
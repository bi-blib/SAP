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

    print(f"Sector 1 access: {group1}")
    print(f"Sector 2 access: {group2}")
    print(f"Sector 3 access: {group3}")
    print(f"Trailer sector access: {group4}")

    
    # print(f"Key A is: {keyA.hex()}")

    # Try standard keys first
    foundKeyA = False
    foundKeyB = False
    for key in standardKeys:
        if (key == keyA):
            print(f"Authentication succeeded with Key A: {key.hex()}")
            foundKeyA = True
            break

    if (foundKeyA == False):
        for key in knownCommonKeys:
            if (key == keyA):
                print(f"Authentication succeeded with Key A: {key.hex()}")
                foundKeyA = True
                break
    
    # Look for KeyB
    if (readableKeyB(group4) == True):
        keyB = sectorTrailer[10:16]
        for key in standardKeys:
            if (key == keyB):
                print(f"Authentication succeeded with Key B: {key.hex()}")
                foundKeyB = True
                break

        if (foundKeyB == False):
            for key in knownCommonKeys:
                if (key == keyB):
                    print(f"Authentication succeeded with Key B: {key.hex()}")
                    foundKeyB = True
                    break
    else: 
        print("KeyB is not readable from Sector Trailer")

    if ((foundKeyA == False) and (foundKeyB == False)):
        print("Unable to find keys amongst common values, attempting to brute force could take up to 3 days")

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
filename = str(input("What is the name of your MIFARE Card File? "))
filename = filename.strip()     # Strip any leading or trailing whitespace
if not os.path.isfile(filename):
    print("Unable to find file, please try again")
else:
    initiateCommunication(filename)
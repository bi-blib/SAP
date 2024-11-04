import random
import os

blockSize = 16

def initialize_card(file_name):
    with open(file_name, 'wb') as f:
        for sector in range(16):
            for block in range(4):
                if sector == 0 and block == 0:
                    writeBlock0(f)
                elif block == 3:  # Sector trailer (access control and keys)
                    # Key A (6 bytes) + Access bits (4 bytes) + Key B (6 bytes)
                    keyA = b'\xFF' * 6
                    accessBits = b'\x00\x08\x80' 
                    userData = b'\x00'
                    keyB = b'\xFF' * 6
                    sectorTrailer = keyA  + accessBits + userData + keyB
                    f.write(sectorTrailer)
                else:
                    # Default data blocks filled with 0x00
                    f.write(b'\x00' * blockSize)

def print_hexdump(card_data):
    """Print the card data as a hexdump, formatted by sector and block."""
    print("MIFARE Classic 1K Hexdump\n" + "-" * 60)
    
    for sector in range(16):
        print(f"Sector {sector}:")
        for block in range(4):
            block_num = sector * 4 + block
            data = card_data[block_num * blockSize:(block_num + 1) * blockSize]
            hex_data = ' '.join(f"{byte:02X}" for byte in data)
            print(f"  Block {block_num:02}: {hex_data}")
        print("-" * 60)

def writeBlock0(f):
    # Write manufacturer block
    uniqueIdentifier = os.urandom(4)
    blockCheckChar = bccCalculator(uniqueIdentifier)
    sakByte = b'\x08'
    manufacturerID = generateVendorID().encode()[:4]
    serialNo =  "SN-2024-XYZ-001234".encode()[:6]
    manufacturerData = sakByte + manufacturerID + serialNo 
    block0 = uniqueIdentifier + blockCheckChar + manufacturerData 
    f.write(block0.ljust(16, b'\xFF'))           # pad any remaining available bytes

def bccCalculator(value):
    blockCheck = 0
    for byte in value:
        blockCheck = blockCheck^byte
    return blockCheck.to_bytes(1, 'big')        # Ensures a singular byte is returned

def generateVendorID():
    vendorID = random.randint(0x0000, 0xFFFF)
    return f"{vendorID:04X}"    # format as a 4 digit hex string

# Call the function to initialize the virtual card
fileName = str(input("What is the name of the file? "))
fileName += '.bin'
initialize_card(fileName)
print(f"You can find default MIFARE Classic 1k Card under the name {fileName}")
with open(fileName, 'rb') as f:
    print(f"Here is the blank card")
    card_data = f.read() 
    print_hexdump(card_data)
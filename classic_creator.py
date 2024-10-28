import random

# Initialize a blank MIFARE 1KB card with default values
def initialize_card(file_name):
    # Create a blank 1KB file (1024 bytes)
    with open(file_name, 'wb') as f:
        # Iterate through all 16 sectors
        for sector in range(16):
            # Write 4 blocks (16 bytes each) per sector
            for block in range(4):
                if sector == 0 and block == 0:
                    write_block0(f)
                elif block == 3:  # Sector trailer (access control and keys)
                    # Key A (6 bytes) + Access bits (4 bytes) + Key B (6 bytes)
                    keyA = b'\xFF' * 6
                    # Access bits to lock block 
                    accessBits = b'\xFF\x07\x80\x69' 
                    keyB = b'\xFF' * 6
                    sector_trailer = keyA  + accessBits + keyB
                    f.write(sector_trailer)
                else:
                    # Default data blocks filled with 0x00
                    f.write(b'\x00' * 16)

def print_hexdump(card_data):
    """Print the card data as a hexdump, formatted by sector and block."""
    print("MIFARE Classic 1K Hexdump\n" + "-" * 60)
    
    for sector in range(16):
        print(f"Sector {sector}:")
        for block in range(4):
            block_num = sector * 4 + block
            data = card_data[block_num * 16:(block_num + 1) * 16]
            hex_data = ' '.join(f"{byte:02X}" for byte in data)
            print(f"  Block {block_num:02}: {hex_data}")
        print("-" * 60)

def write_block0(f):
    # Write manufacturer block
    uniqueIdentifier = b'\xDE\xAD\xBE\xEF'
    blockCheckChar = bccCalculator(uniqueIdentifier)
    manufacturerID = generateVendorID().encode()[:4]
    productName = "MC1k".encode()[:3]
    serialNo =  "SN-2024-XYZ-001234".encode()[:4]
    manufacturerData = manufacturerID + productName + serialNo 
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
    card_data = f.read() 
    print_hexdump(card_data)
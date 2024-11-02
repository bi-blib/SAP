import os

####################### Dumps info of card for debugging #######################
def print_hexdump(card_data):
    print("MIFARE Classic 1K Hexdump\n" + "-" * 60)
    
    for sector in range(16):
        print(f"Sector {sector}:")
        for block in range(4):
            block_num = sector * 4 + block
            data = card_data[block_num * 16:(block_num + 1) * 16]
            hex_data = ' '.join(f"{byte:02X}" for byte in data)
            print(f"  Block {block_num:02}: {hex_data}")
        print("-" * 60)

################################### Main #######################################
while (True):
    filename = str(input("What is the name of the file being read? "))
    filename = filename.strip()     
    if not os.path.isfile(filename):
        print("Unable to find file, please try again")
    else:
        break

with open(filename, 'rb') as f:
    card_data = f.read() 
    print_hexdump(card_data)
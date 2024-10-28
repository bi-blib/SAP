blockSize = 16

def writeMemoryBlock(file, sector, block, data):
    if (len(data) > blockSize) return 'invalid data'
    # data needs to be padded to be 16 bytes, ljust padds after data 
    data = data.ljust(16, b'\x00')
    offset = (sector * 4) + block
    f = open(file, 'r+b')
    f.seek(offset)
    f.write(data)
    f.close()

def printManufacturerBlock(file):
    f = open(file, 'r')
    f.read(blockSize)

def write1kCard(file):
    for x in range(16) 
        for y in range(4) 
            writeMemoryBlock(file, x, y, b'\x00')
            if (x = 0 and y = 0):
                printManufacturerBlock(file)
            continue
             else if (x = 0 and y = 3):
                require authentication
            else:
                writeMemoryBlock(file, x, y, b'\x00')
           
            
    
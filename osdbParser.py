import struct

def readLEB128(f):
    integer = 0
    i = 0
    while (b := f.read(1)):
        b = b[0]
        if b >> 7:
            integer = integer + ((b & 0x7f) << (i * 7))
        else:
            integer = integer + ((b & 0x7f) << (i * 7))
            break
        i += 1
    return integer


def readString(f):
    a = struct.unpack("<B", f.read(1))[0]
    if a == 0x0b:
        size = readLEB128(f)
        return [size, f.read(size)]
    return []

def readHeader(f):
    a = list(struct.unpack("<II?Q", f.read(17)))
    a.append(readString(f))
    b = struct.unpack("<I", f.read(4))[0]
    a.append(b)
    return a

def readBeatmap(f):
    a = []
    for i in range(9):
        s = readString(f)
        a.append(s)
    b = list(struct.unpack("<BHHHQffffd", f.read(1+2+2+2+8+4+4+4+4+8)))
    a += b

    a.append(readIntDoublePairs(f))
    a += list(struct.unpack("<III", f.read(4+4+4)))
    nTimingPoints = struct.unpack("<I", f.read(4))[0]
    timingPoints = [nTimingPoints]
    for i in range(nTimingPoints):

        timingPoints.append(list(struct.unpack("dd?", f.read(17))))

    a.append(timingPoints)
    a += list(struct.unpack("<IIIBBBBHfB", f.read(4+4+4+1+1+1+1+2+4+1)))

    for i in range(2):
        a.append(readString(f))

    a += list(struct.unpack("<H", f.read(2)))

    a.append(readString(f))

    a += list(struct.unpack("<?Q?", f.read(1+8+1)))

    a.append(readString(f))

    a += list(struct.unpack("<Q?????IB", f.read(8+1+1+1+1+1+4+1)))
    return a

def readIntDoublePairs(f):
    pairs = [[],[],[],[]]
    for mode in range(4):
        counter = f.read(4)[0]

        pairs[mode].append(readIntDoublePair(f, counter))
    return pairs

def readIntDoublePair(f, amount):
    pairs = []

    for i in range(amount):
        a = struct.unpack("<BIBd", f.read(14))
        pairs.append(a)

    return pairs

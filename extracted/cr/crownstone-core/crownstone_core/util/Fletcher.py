from crownstone_core.util.Conversion import Conversion


def fletcher32_uint8Arr(uint8Array):
    uint16Array = Conversion.uint8_array_to_uint16_array(uint8Array)
    return fletcher32_uint16Arr(uint16Array)

def fletcher32_uint16Arr(uint16Array):
    uint32_max = 4294967295
    c0 = 0
    c1 = 0
    iterations = int(len(uint16Array) / 360)
    length = len(uint16Array)
    index = 0
    for i in range(iterations + 1):
        blockLength = min(360, length)
        for j in range(blockLength):
            c0 = (c0 + uint16Array[index]) % uint32_max
            c1 = c1 + c0
            index += 1

        c0 = c0 % 65535
        c1 = c1 % 65535
        length -= 360

    return ((c1 << 16) % uint32_max) | c0

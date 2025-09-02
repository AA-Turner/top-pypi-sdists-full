"""WiLight Protocol Extended Support."""
import random

HA_ID = "9A37B1F272931586"
COD_APLIC = "Tf(XFGZAXaTe;QO[f]MGVb+H@`/^?8Z>"

def codingVectors():
    """Create coding vetors."""

    car1 = random.randint(63, 126)

    vetCod_1 = (car1 + 1) % 32
    vetCod_2 = random.randint(1, 10)
    vetCod_3 = random.randint(1, 10)

    vetCod_4 = vetCod_1 + vetCod_2 + vetCod_3
    vetCod_4 = vetCod_4 & 7
    vetCod_4 = vetCod_4 + 1

    len = 3 + vetCod_4
    buf = bytearray(len)
    buf[0] = car1
    buf[1] = (vetCod_2 + 47)
    buf[2] = (vetCod_3 + 47)

    for i in range(1, vetCod_4 + 1):
        buf[i + 2] = random.randint(1, 10) + 47

    return buf;

def cmdInit(numSerie):
    """Command intial."""

    ini = '\x1F'
    ini = ini + codingVectors().decode()
    ini = ini + HA_ID
    ini = ini + numSerie

    return ini;

def codeData(dado):
    """Code data."""

    lenDado = len(dado)
    bufOut = bytearray(dado)
    codeAplic = COD_APLIC.encode()

    vetCod_1 = (bufOut[1] + 1) % 32
    vetCod_2 = bufOut[2] - 47
    vetCod_3 = bufOut[3] - 47

    vetCod_4 = vetCod_1 + vetCod_2 + vetCod_3
    vetCod_4 = vetCod_4 & 7
    vetCod_4 = vetCod_4 + 1

    vetCod_5 = 0

    for i in range(1, vetCod_4 + 1):
        vetCod_5 = vetCod_5 + bufOut[i + 3] - 48 # 48 porque 0 a 9...

    vetCod_5 = vetCod_5 & 7

    altFlag = False
    for n in range(2, lenDado):
        b = bufOut[n] - 48
        if (n == vetCod_4 + 4):
            vetCod_1 = vetCod_1 + vetCod_5
            vetCod_1 = vetCod_1 & 31
            vetCod_5 = vetCod_5 % 4
        if (n >= vetCod_4 + 4):
            b = b + vetCod_5
            vetCod_5 = vetCod_5 + 1
            if (vetCod_5 > 3):
                vetCod_5 = 0
        bufOut[n] = b + codeAplic[vetCod_1]
        if altFlag:
            vetCod_1 = vetCod_1 + vetCod_3
            vetCod_1 = vetCod_1 & 31
            altFlag = False
        else:
            vetCod_1 = vetCod_1 + vetCod_2
            vetCod_1 = vetCod_1 & 31
            altFlag = True

    return bufOut

def codeCmd(cmd, numSerie):
    """Code Command."""

    inic = cmdInit(numSerie)

    buf = inic.encode() + cmd.encode()
    lenBuf = len(buf)

    iChkSum = 0
    for n in range(0, lenBuf):
        iChkSum = iChkSum + buf[n]
    iChkSum = iChkSum % 256;

    sChkSum = '{:0>3}'.format(iChkSum)

    buf = buf + sChkSum.encode()

    buf = codeData(buf)

    return buf

def decodeData(dado):

    lenDado = len(dado)
    buf = bytearray(dado)
    codeAplic = COD_APLIC.encode()

    vetCod_1 = (buf[1] + 1) % 32
    vetCod_2 = buf[2] - codeAplic[vetCod_1]
    vetCod_2 = vetCod_2 & 31
    vetCod_2 = vetCod_2 + 1
    vetCod_3 = vetCod_1 + vetCod_2
    vetCod_3 = vetCod_3 & 31
    vetCod_3 = buf[3] - codeAplic[vetCod_3]
    vetCod_3 = vetCod_3 & 31
    vetCod_3 = vetCod_3 + 1

    vetCod_4 = vetCod_1 + vetCod_2 + vetCod_3
    vetCod_4 = vetCod_4 & 7
    vetCod_4 = vetCod_4 + 1

    vetCod_5 = 0

    altFlag = False
    for n in range(2, lenDado):
        b = buf[n] - codeAplic[vetCod_1]
        if ((n > 3) and (n < vetCod_4 + 4)):
            vetCod_5 = vetCod_5 + b
        if (n == vetCod_4 + 4):
            vetCod_5 = vetCod_5 % 8
            vetCod_1 = vetCod_1 + vetCod_5
            vetCod_1 = vetCod_1 & 31
            vetCod_5 = vetCod_5 % 4
            b = buf[n] - codeAplic[vetCod_1]
        if (n >= vetCod_4 + 4):
            b = b - vetCod_5
            vetCod_5 = vetCod_5 + 1
            if (vetCod_5 > 3):
                vetCod_5 = 0
        buf[n] = ((b + 48) & 255)
        if altFlag:
            vetCod_1 = vetCod_1 + vetCod_3
            vetCod_1 = vetCod_1 & 31
            altFlag = False
        else:
            vetCod_1 = vetCod_1 + vetCod_2
            vetCod_1 = vetCod_1 & 31
            altFlag = True

    bufRet = b'&'
    for n in range(4 + vetCod_4, lenDado - 3):
        bufRet = bufRet + bytes([buf[n]])

    return bufRet

import binascii
import re

# this mangled "shorthand" output basically throws out exact timings while
# keeping the relative length of each time period. Good for comparing
# received codes against known values
def mangleIR(data, ignore_errors=False):
    """Mangle a raw Kira data packet into shorthand"""
    try:
        # Packet mangling algorithm inspired by Rex Becket's kirarx vera plugin
        # Determine a median value for the timing packets and categorize each
        # timing as longer or shorter than that. This will always work for signals
        # that use pulse width modulation (since varying by long-short is basically
        # the definition of what PWM is). By lucky coincidence this also works with
        # the RC-5/RC-6 encodings used by Phillips (manchester encoding)
        # because time variations of opposite-phase/same-phase are either N or 2*N
        if isinstance(data, bytes):
            data = data.decode('ascii')
        data = data.strip()
        times = [int(x, 16) for x in data.split()[2:]]
        minTime = min(times[2:-1])
        maxTime = max(times[2:-1])
        margin = (maxTime - minTime) / 2 + minTime
        return ''.join([(x < margin and 'S' or 'L') for x in times])
    except:
        # Probably a mangled packet.
        if not ignore_errors:
            raise

# pronto codes provide basically the same information as a Kira code
# just in a slightly different form. (Kira represents timings in uS
# while pronto uses multiples of the base clock cycle.)
# Thus they can be used for transmission
def pronto2kira(data):
    """Convert a pronto code to a discrete (single button press) Kira code"""
    octets = [int(x, 16) for x in data.split()]
    preamble = octets[:4]
    convert = lambda x: 1000.0 / (x * 0.241246)
    freq = convert(preamble[1])
    period = 1000000.0 / (freq * 1000.0)
    dataLen = preamble[2]
    res = "K %02X%02X " %(freq, dataLen)
    res += " ".join(["%0.4X" % min(0x2000, (period * x)) for x in octets[4: 4+(2*dataLen)]])
    return res

def mangleNec(code, freq=40):
    """Convert NEC code to shorthand notation"""
    # base time is 550 microseconds
    # unit of burst time
    # lead in pattern:   214d 10b3
    # "1" burst pattern: 0226 0960
    # "0" burst pattern: 0226 0258
    # lead out pattern:  0226 2000
    # there's large disagreement between devices as to a common preamble
    # or the "long" off period for the representation of a binary 1
    # thus we can't construct a code suitable for transmission
    # without more information--but it's good enough for creating
    # a shorthand representaiton for use with recv
    timings = []
    for octet in binascii.unhexlify(code.replace(" ", "")):
        burst = lambda x: x and "0226 06AD" or "0226 0258"
        for bit in reversed("%08d" % int(bin(ord(octet))[2:])):
            bit = int(bit)
            timings.append(burst(bit))
    return mangleIR("K %0X22 214d 10b3 " % freq + " ".join(timings) + " 0226 2000")

def inferCodeType(data):
    # a series of L/S chars
    if re.match('^[LS]+$', data):
        return 'shorthand'
    # "K " followed by groups of 4 hex chars
    if re.match("^K ([0-9a-fA-F]{4} )*[0-9a-fA-F]{4}$", data):
        return 'kira'
    # 2 groups of 4 hex chars
    if re.match("^[0-9a-fA-F]{4} [0-9a-fA-F]{4}$", data):
        return 'nec'
    # multiple groups of 4 hex chars
    if re.match("^([0-9a-fA-F]{4} )*[0-9a-fA-F]{4}$", data):
        return 'pronto'

# convert code into a raw kira code that can be transmitted
def code2kira(code, codeType=None):
    if codeType is None:
        codeType = inferCodeType(code)
    if codeType == "kira":
        return code.strip()
    if codeType == "pronto":
        return pronto2kira(code)

# convert code to a form ready for comparison
def mangleCode(code, codeType=None):
    if codeType is None:
        codeType = inferCodeType(code)
    if codeType == "shorthand":
        return code.strip()
    if codeType == "kira":
        return mangleIR(code)
    if codeType == "pronto":
        return mangleIR(pronto2kira(code))
    if codeType == "nec":
        return mangleNec(code)

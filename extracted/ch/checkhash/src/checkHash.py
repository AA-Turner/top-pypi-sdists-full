"""
checkHash
https://github.com/xhelphin/checkHash

Python package to check if a string is a valid hash.
"""

from isHex import isHex, isHexUpper

def isMD2(hash):
    """
    Returns True if supplied argument is a valid MD2 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 32:
        return False
    return True


def isMD4(hash):
    """
    Returns True if supplied argument is a valid MD4 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 32:
        return False
    return True


def isMD5(hash):
    """
    Returns True if supplied argument is a valid MD5 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 32:
        return False
    return True

def isMD6128(hash):
    """
    Returns True if supplied argument is a valid MD6 128 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 32:
        return False
    return True


def isMD6256(hash):
    """
    Returns True if supplied argument is a valid MD6 256 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 64:
        return False
    return True


def isMD6512(hash):
    """
    Returns True if supplied argument is a valid MD6 512 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 128:
        return False
    return True


def isSHA1(hash):
    """
    Returns True if supplied argument is a valid SHA1 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 40:
        return False
    return True


def isSHA2224(hash):
    """
    Returns True if supplied argument is a valid SHA-2 224 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 56:
        return False
    return True

def isSHA2256(hash):
    """
    Returns True if supplied argument is a valid SHA-2 256 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 64:
        return False
    return True

def isSHA2384(hash):
    """
    Returns True if supplied argument is a valid SHA-2 384 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 96:
        return False
    return True

def isSHA2512(hash):
    """
    Returns True if supplied argument is a valid SHA-2 512 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 128:
        return False
    return True

def isSHA3224(hash):
    """
    Returns True if supplied argument is a valid SHA-3 224 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 56:
        return False
    return True

def isSHA3256(hash):
    """
    Returns True if supplied argument is a valid SHA-3 256 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 64:
        return False
    return True

def isSHA3384(hash):
    """
    Returns True if supplied argument is a valid SHA-3 384 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 96:
        return False
    return True

def isSHA3512(hash):
    """
    Returns True if supplied argument is a valid SHA-3 512 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 128:
        return False
    return True

def isNTLM(hash):
    """
    Returns True if supplied argument is a valid NTLM hash, else returns False.
    """
    if not isHexUpper(hash):
        return False
    if len(hash) != 32:
        return False
    return True

def isOtherHash(hash, length):
    """
    Returns True if supplied argument is a valid hash with the user-specified length, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != length:
        return False
    return True

def isRipeMD128(hash):
    """
    Returns True if supplied argument is a valid RipeMD-128 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 32:
        return False
    return True

def isRipeMD160(hash):
    """
    Returns True if supplied argument is a valid RipeMD-160 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 40:
        return False
    return True

def isRipeMD256(hash):
    """
    Returns True if supplied argument is a valid RipeMD-256 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 64:
        return False
    return True

def isRipeMD320(hash):
    """
    Returns True if supplied argument is a valid RipeMD-320 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 80:
        return False
    return True

def isCRC16(hash):
    """
    Returns True if supplied argument is a valid CRC16 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 4:
        return False
    return True

def isCRC32(hash):
    """
    Returns True if supplied argument is a valid CRC32 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 8:
        return False
    return True

def isAdler32(hash):
    """
    Returns True if supplied argument is a valid Adler32 hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 8:
        return False
    return True

def isWhirlpool(hash):
    """
    Returns True if supplied argument is a valid Whirlpool hash, else returns False.
    """
    if not isHex(hash):
        return False
    if len(hash) != 128:
        return False
    return True

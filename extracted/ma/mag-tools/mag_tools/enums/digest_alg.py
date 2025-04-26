from mag_tools.enums.base_enum import BaseEnum


class DigestAlg(BaseEnum):
    #
    MD5 = ("MD5", "长度为16字节")
    SHA1 = ("SHA1", "长度为20字节")
    # SHA-2代
    SHA224 = ("SHA224", "长度为28字节")
    SHA256 = ("SHA256", "长度为32字节")
    SHA384 = ("SHA384", "长度为48字节")
    SHA512 = ("SHA512", "长度为64字节")
    # SHA-3代
    SHA3_224 = ("SHA3-224", "长度为28字节")
    SHA3_256 = ("SHA3-256", "长度为32字节")
    SHA3_384 = ("SHA3-384", "长度为48字节")
    SHA3_512 = ("SHA3-512", "长度为64字节")
    # HMAC
    HMAC_SHA224 = ("HMAC_SHA224", "长度为18字节")
    HMAC_SHA256 = ("HMAC_SHA256", "长度为32字节")
    HMAC_SHA384 = ("HMAC_SHA384", "长度为48字节")
    HMAC_SHA512 = ("HMAC_SHA512", "长度为64字节")

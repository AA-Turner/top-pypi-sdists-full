from mag_tools.enums.base_enum import BaseEnum


class CryptAlg(BaseEnum):
    # 定义加密算法枚举
    UNKNOWN = ("Unknown", "未知")
    RSA = ("RSA", "非对称算法，密钥128、256或512字节")
    DSA = ("DSA", "非对称算法，密钥128字节")
    AES256 = ("AES256", "对称算法，密钥32字节")
    X_CHA_CHA20 = ("XChaCha20", "对称算法，密钥32字节")
    TWOFISH = ("Twofish", "对称算法，密钥16字节")
    IDEA = ("Idea", "对称算法，密钥16字节")
    SM4 = ("SM4", "国密算法，密钥16字节")
    RC4 = ("RC4", "对称算法，密钥16字节")
    RC5 = ("RC5", "对称算法，密钥0到16字节")
    BLOWFISH = ("Blowfish", "对称算法，密钥1到56字节")
    DES = ("Des", "对称算法，密钥8字节，不推荐")
    DES_EDE = ("DesEde", "对称算法，密钥24字节")
    TRIPLE_DES = ("3Des", "对称算法，密钥24字节")
    AES = ("AES", "对称算法，密钥16、24或32字节")
    DIFFIE_HELLMAN = ("Diffie-Hellman", "对称算法，密钥256字节")

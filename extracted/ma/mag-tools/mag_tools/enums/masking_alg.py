from mag_tools.enums.base_enum import BaseEnum


class MaskingAlg(BaseEnum):
    # 加密
    DES = ("DES", "DES加密")
    DES_EDE = ("DES_EDE", "DesEde加密")
    TRIPLE_DES = ("TRIPLE_DES", "3Des加密")
    AES = ("AES", "AES加密")
    # Hash
    MD_5 = ("MD5", "MD5 Hash")
    SHA_1 = ("SHA1", "SHA1 Hash")
    SHA_256 = ("SHA256", "SHA256 Hash")
    # 掩码
    STAR_REPLACE = ("STAR_REPLACE", "星号替代掩码法")
    RANDOM_REPLACE = ("RANDOM_REPLACE", "随机值替代掩码法")

    def is_masking(self):
        """
        判断是否为掩码算法
        :return: 是否为掩码算法
        """
        return self in {MaskingAlg.STAR_REPLACE, MaskingAlg.RANDOM_REPLACE}

    def is_crypt(self):
        """
        判断是否为加密算法
        :return: 是否为加密算法
        """
        return self in {MaskingAlg.DES, MaskingAlg.DES_EDE, MaskingAlg.TRIPLE_DES, MaskingAlg.AES}

    def is_hash(self):
        """
        判断是否为Hash算法
        :return: 是否为Hash算法
        """
        return self in {MaskingAlg.MD_5, MaskingAlg.SHA_1, MaskingAlg.SHA_256}


if __name__ == "__main__":
    # 示例使用
    print(MaskingAlg.of_code("AES"))  # 输出: MaskingAlg.AES
    print(MaskingAlg.AES.is_crypt())  # 输出: True
    print(MaskingAlg.MD_5.is_hash())  # 输出: True
    print(MaskingAlg.STAR_REPLACE.is_masking())  # 输出: True

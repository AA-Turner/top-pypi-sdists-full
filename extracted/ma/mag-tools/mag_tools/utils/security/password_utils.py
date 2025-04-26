import hashlib
import random
import string
from typing import  Optional

from mag_tools.exception.app_exception import AppException
from mag_tools.enums.crypt_alg import CryptAlg
from mag_tools.utils.data.bytes_utils import BytesUtils
from mag_tools.utils.security.crypt_utils import CryptUtils


class PasswordUtils:
    SALT_BYTE_SIZE = 16
    MIN_HASH_TIMES = 5000
    MIN_INITIAL_HASH_TIMES = 100000
    MAX_INITIAL_HASH_TIMES = 200000

    @staticmethod
    def make_salt() -> str:
        """
        产生密码调剂参数
        :return: String salt
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=PasswordUtils.SALT_BYTE_SIZE))

    @staticmethod
    def make_initial_hash_times() -> int:
        """
        生成初始的Hash次数
        :return: Hash次数
        """
        return random.randint(PasswordUtils.MIN_INITIAL_HASH_TIMES, PasswordUtils.MAX_INITIAL_HASH_TIMES)

    @staticmethod
    def check_password_info(salt: str, hash_count: int) -> bool:
        """
        检查SALT和Hash次数是否符合规范
        :param salt: 密码摘要使用的调剂数(十六进制格式)
        :param hash_count: 密码摘要次数
        :return: 是否符合规范
        """
        ba_salt = BytesUtils.hex_to_bytes(salt)
        return (ba_salt is not None and len(ba_salt) == PasswordUtils.SALT_BYTE_SIZE) and (
                hash_count >= PasswordUtils.MIN_HASH_TIMES)

    @staticmethod
    def make_identify_code(length: int) -> str:
        """
        生成验证码
        :param length: 验证码长度
        :return: 验证码
        """
        verify_code = ''.join(random.choices(string.digits, k=length))
        # 舍弃尾数为4的验证码
        while verify_code.endswith('4'):
            verify_code = ''.join(random.choices(string.digits, k=length))
        return verify_code

    @staticmethod
    def sha256_password(password: str, salt: str, hash_times: int) -> str:
        """
        使用SHA256对密码和Salt进行多次Hash
        :param password: 源密码
        :param salt: 密码摘要使用的调剂数(十六进制格式)
        :param hash_times: 密码摘要次数
        :return: Hash值(十六进制格式)
        """
        hash_value = password + salt
        for _ in range(hash_times):
            hash_value = hashlib.sha256(hash_value.encode()).hexdigest()
        return hash_value

    @staticmethod
    def encrypt_passwd(password: str, key: str) -> str:
        """
        加密密码
        :param password: 源密码
        :param key: 加密密钥
        :return: 密码密文的Hex字符串
        """
        ba_password = password.encode()
        ba_key = key.encode()
        ba_encrypt_passwd = CryptUtils.encrypt_bytes(ba_password, CryptAlg.TRIPLE_DES, ba_key)
        return BytesUtils.bytes_to_hex(ba_encrypt_passwd)

    @staticmethod
    def decrypt_password(hex_cipher_passwd: str, key: str) -> str:
        """
        解密密码
        :param hex_cipher_passwd: 密码密文的Hex字符串
        :param key: 加密密钥
        :return: 密码明文
        """
        return CryptUtils.decrypt(hex_cipher_passwd, CryptAlg.TRIPLE_DES, key)

    @staticmethod
    def make_sign_token(map_: dict[str, str]) -> Optional[str]:
        """
        生成MD5签名
        将传参按照ASCII码字典序排序，并将生成的字符串进行MD5加密
        :param map_: 参数
        :return: 签名
        """
        try:
            info_ids = list(map_.items())
            # 对所有传入参数按照字段名的ASCII码从小到大排序（字典序）
            info_ids.sort(key=lambda item: item[0])

            # 构造签名键值对的格式
            sb = '&'.join(f"{key}={val}" for key, val in info_ids if val)

            # 进行MD5加密
            sign = hashlib.md5(sb.encode()).hexdigest().upper()
            return sign
        except AppException:
            return None

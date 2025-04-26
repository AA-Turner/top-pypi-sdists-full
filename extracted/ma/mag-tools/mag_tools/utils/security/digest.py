import hashlib
from typing import Union

from mag_tools.exception.app_exception import AppException
from mag_tools.utils.data.bytes_utils import BytesUtils
from mag_tools.enums.digest_alg import DigestAlg


class Digest:
    @staticmethod
    def digest_bytes(message: bytes, algorithm: DigestAlg) -> bytes:
        """
        计算摘要
        :param message: 消息内容
        :param algorithm: 摘要算法
        :return: 摘要
        """
        try:
            digest = hashlib.new(algorithm.code.lower())
            digest.update(message)
            ba_hash = digest.digest()
            return ba_hash
        except ValueError as e:
            raise AppException(f"该摘要算法[{algorithm}]不存在") from e

    @staticmethod
    def digest(message: str, algorithm: DigestAlg) -> Union[str, bytes]:
        """
        计算摘要
        :param message: 消息内容
        :param algorithm: 摘要算法
        :return: 摘要(十六进制格式) 或 摘要
        """
        ba_message = message.encode()
        ba_hash = Digest.digest_bytes(ba_message, algorithm)
        return BytesUtils.bytes_to_hex(ba_hash)

    @staticmethod
    def md5(message: str) -> str:
        """
        计算SHA256摘要
        :param message: 消息内容
        :return: 摘要(十六进制格式)
        """
        return Digest.digest(message, DigestAlg.MD5)

    @staticmethod
    def sha1(message: str) -> str:
        """
        计算SHA256摘要
        :param message: 消息内容
        :return: 摘要(十六进制格式)
        """
        return Digest.digest(message, DigestAlg.SHA1)

    @staticmethod
    def sha256(message: str) -> str:
        """
        计算SHA256摘要
        :param message: 消息内容
        :return: 摘要(十六进制格式)
        """
        return Digest.digest(message, DigestAlg.SHA256)

    @staticmethod
    def sha512(message: str) -> str:
        """
        计算SHA512摘要
        :param message: 消息内容
        :return: 摘要(十六进制格式)
        """
        return Digest.digest(message, DigestAlg.SHA512)

    @staticmethod
    def sha3_256(message: str) -> str:
        """
        计算SHA3-256摘要
        :param message: 消息内容
        :return: 摘要(十六进制格式)
        """
        return Digest.digest(message, DigestAlg.SHA3_256)

    @staticmethod
    def sha3_512(message: str) -> str:
        """
        计算SHA3-512摘要
        :param message: 消息内容
        :return: 摘要(十六进制格式)
        """
        return Digest.digest(message, DigestAlg.SHA3_512)

    @staticmethod
    def digest_more_times_bytes(message: bytes, algorithm: DigestAlg, hash_times: int) -> bytes:
        """
        进行多次Hash
        :param message: 消息内容
        :param algorithm: 摘要算法
        :param hash_times: hash次数
        :return: 摘要
        """
        ba_hash = message
        for _ in range(hash_times):
            ba_hash = Digest.digest(ba_hash, algorithm)
        return ba_hash

    @staticmethod
    def digest_more_times(message: str, algorithm: DigestAlg, hash_times: int) -> str:
        """
        进行多次Hash
        :param message: 消息内容
        :param algorithm: 摘要算法
        :param hash_times: hash次数
        :return: 摘要
        """
        ba_hash = Digest.digest_more_times_bytes(message.encode(), algorithm, hash_times)
        return BytesUtils.bytes_to_hex(ba_hash)

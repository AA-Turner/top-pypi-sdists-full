
from Crypto.Cipher import AES, Blowfish, DES3
from Crypto.Util.Padding import pad, unpad

from mag_tools.exception.app_exception import AppException
from mag_tools.enums.crypt_alg import CryptAlg
from mag_tools.utils.data.bytes_utils import BytesUtils


class CryptUtils:
    @staticmethod
    def encrypt(clear_text: str, crypt_alg: CryptAlg, key: str) -> str:
        """
        加密处理
        支持常用算法
        :return: 加密数据的Hex字符串
        """
        ba_clear_text = clear_text.encode()
        ba_key = key.encode()
        ba_en_data = CryptUtils.encrypt_bytes(ba_clear_text, crypt_alg, ba_key)
        return BytesUtils.bytes_to_hex(ba_en_data)

    @staticmethod
    def decrypt(hex_cipher_text: str, crypt_alg: CryptAlg, key: str) -> str:
        """
        解密处理
        支持常用算法
        :return: 明文数据
        """
        ba_key = key.encode()
        ba_cipher_text = BytesUtils.hex_to_bytes(hex_cipher_text)
        ba_clear_text = CryptUtils.decrypt_bytes(ba_cipher_text, crypt_alg, ba_key)
        return ba_clear_text.decode()

    @staticmethod
    def encrypt_bytes(clear_text: bytes, crypt_alg: CryptAlg, key: bytes) -> bytes:
        """
        加密处理
        支持常用算法
        """
        try:
            if crypt_alg == CryptAlg.UNKNOWN:
                ba_en_data = clear_text
            elif crypt_alg in [CryptAlg.DES_EDE, CryptAlg.TRIPLE_DES]:
                cipher = DES3.new(key[:24], DES3.MODE_ECB)
                ba_en_data = cipher.encrypt(pad(clear_text, DES3.block_size))
            elif crypt_alg == CryptAlg.DES:
                cipher = DES3.new(key[:8], DES3.MODE_ECB)
                ba_en_data = cipher.encrypt(pad(clear_text, DES3.block_size))
            elif crypt_alg == CryptAlg.AES:
                cipher = AES.new(key[:16], AES.MODE_ECB)
                ba_en_data = cipher.encrypt(pad(clear_text, AES.block_size))
            elif crypt_alg == CryptAlg.AES256:
                cipher = AES.new(key[:32], AES.MODE_ECB)
                ba_en_data = cipher.encrypt(pad(clear_text, AES.block_size))
            elif crypt_alg == CryptAlg.BLOWFISH:
                cipher = Blowfish.new(key[:56], Blowfish.MODE_ECB)
                ba_en_data = cipher.encrypt(pad(clear_text, Blowfish.block_size))
            else:
                raise AppException(f"Unsupported algorithm: {crypt_alg}")
        except Exception as e:
            raise AppException(str(e))

        return ba_en_data

    @staticmethod
    def decrypt_bytes(cipher_text: bytes, crypt_alg: CryptAlg, key: bytes) -> bytes:
        """
        解密处理
        支持常用算法
        :return: 解密后UTF-8字符串
        """
        try:
            if crypt_alg == CryptAlg.UNKNOWN:
                ba_de_data = cipher_text
            elif crypt_alg in [CryptAlg.DES_EDE, CryptAlg.TRIPLE_DES]:
                cipher = DES3.new(key[:24], DES3.MODE_ECB)
                ba_de_data = unpad(cipher.decrypt(cipher_text), DES3.block_size)
            elif crypt_alg == CryptAlg.DES:
                cipher = DES3.new(key[:8], DES3.MODE_ECB)
                ba_de_data = unpad(cipher.decrypt(cipher_text), DES3.block_size)
            elif crypt_alg == CryptAlg.AES:
                cipher = AES.new(key[:16], AES.MODE_ECB)
                ba_de_data = unpad(cipher.decrypt(cipher_text), AES.block_size)
            elif crypt_alg == CryptAlg.AES256:
                cipher = AES.new(key[:32], AES.MODE_ECB)
                ba_de_data = unpad(cipher.decrypt(cipher_text), AES.block_size)
            elif crypt_alg == CryptAlg.BLOWFISH:
                cipher = Blowfish.new(key[:56], Blowfish.MODE_ECB)
                ba_de_data = unpad(cipher.decrypt(cipher_text), Blowfish.block_size)
            else:
                raise AppException(f"Unsupported algorithm: {crypt_alg}")
        except Exception as e:
            raise AppException(str(e))

        return ba_de_data

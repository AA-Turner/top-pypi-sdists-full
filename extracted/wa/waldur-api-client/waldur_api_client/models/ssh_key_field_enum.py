from enum import Enum


class SshKeyFieldEnum(str, Enum):
    FINGERPRINT_MD5 = "fingerprint_md5"
    FINGERPRINT_SHA256 = "fingerprint_sha256"
    FINGERPRINT_SHA512 = "fingerprint_sha512"
    IS_SHARED = "is_shared"
    NAME = "name"
    PUBLIC_KEY = "public_key"
    TYPE = "type"
    URL = "url"
    USER_UUID = "user_uuid"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)

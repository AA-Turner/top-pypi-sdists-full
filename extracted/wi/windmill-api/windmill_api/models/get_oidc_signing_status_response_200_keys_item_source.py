from enum import Enum


class GetOidcSigningStatusResponse200KeysItemSource(str, Enum):
    DATABASE = "database"
    FILE = "file"
    PUBLISH_DIR = "publish_dir"
    SIGNER = "signer"

    def __str__(self) -> str:
        return str(self.value)

from __future__ import annotations

from typing import Any


class SecretStr(str):
    _mask: str
    _secret: str

    @property
    def mask(self) -> str:
        return self._mask

    def __str__(self) -> str:
        return self.mask

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(masked={self.mask})>"

    def reveal(self) -> str:
        return self._secret

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SecretString):
            return self._secret == other._secret
        if isinstance(other, str):
            return self._secret == other
        return False


class SecretString(SecretStr):
    def __new__(cls, secret: str, mask: str = "***") -> SecretString:
        obj = super().__new__(cls, secret)
        obj._mask = mask
        obj._secret = secret
        return obj


class SecretArgString(SecretStr):
    _delimitor: str

    def __new__(cls, secret: str, mask: str = "***", delimitor: str = "=") -> SecretArgString:
        obj = super().__new__(cls, secret)
        obj._mask = mask
        obj._secret = secret
        obj._delimitor = delimitor
        return obj

    @property
    def mask(self) -> str:
        if self._delimitor in self._secret:
            key, _ = self._secret.split("=", 1)
            return f"{key}{self._delimitor}{self._mask}"
        return self._mask

from __future__ import annotations
import re


class VersionManager:
    PATTERN = r"^v\d+\.\d+\.\d+$"

    @classmethod
    def is_valid(cls, name: str) -> bool:
        return bool(re.match(cls.PATTERN, name))

    @classmethod
    def ensure_v_prefix(cls, version: str) -> str:
        if not version.startswith("v"):
            return f"v{version}"
        return version

    @staticmethod
    def parse(version: str) -> tuple[int, int, int]:
        v = version.lstrip("v")
        parts = v.split(".")
        return (int(parts[0]), int(parts[1]), int(parts[2]))

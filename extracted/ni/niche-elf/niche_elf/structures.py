"""All the relevant structures are defined here."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from . import datatypes

if TYPE_CHECKING:
    import ctypes


@dataclass
class Symbol:
    """Represents a symbol (function or global variable) in the binary."""

    name: str
    bind: int
    typ: int
    value: int
    size: int

    @classmethod
    def generic(cls, name: str, addr: int, size: int, bind: int) -> Symbol:
        return cls(
            name=name,
            bind=bind,
            # LIEF emits this type, so I trust.
            typ=datatypes.Constants.STT_COMMON,
            value=addr,
            size=size,
        )

    @classmethod
    def function(cls, name: str, addr: int, size: int, bind: int) -> Symbol:
        return cls(
            name=name,
            bind=bind,
            typ=datatypes.Constants.STT_FUNC,
            value=addr,
            size=size,
        )

    @classmethod
    def object(cls, name: str, addr: int, size: int, bind: int) -> Symbol:
        return cls(
            name=name,
            bind=bind,
            typ=datatypes.Constants.STT_OBJECT,
            value=addr,
            size=size,
        )


@dataclass
class Section:
    # `name` is not in the section header, but rather added to the shstrtab.
    name: str
    # `data` is the data of the section (also not in the section header)
    data: bytes
    # https://www.man7.org/linux/man-pages/man5/elf.5.html#:~:text=Section%20header%20%28Shdr
    header: ctypes.Structure
    # self.header.sh_offset should initially be set to -1 and then later populated
    # during write.

    def padded_data(self) -> bytes:
        pad_len = (-len(self.data)) % self.header.sh_addralign
        return bytes(self.data + b"\x00" * pad_len)

    def packed_header(self) -> bytes:
        if len(self.data) > self.header.sh_size:
            raise AssertionError(
                f"Section data is bigger than sh_size for section {self.name} "
                f"({len(self.data)} vs {self.header.sh_size}).",
            )
        if self.header.sh_offset == -1:
            raise AssertionError(f"sh_offset in section {self.name} was not initialized.")

        return bytes(self.header)


@dataclass
class SHStrTabEntry:
    name: str
    offset: int = 0


@dataclass
class SHStrTab:
    entries: list[SHStrTabEntry] = field(default_factory=list)
    data: bytes = b"\x00"

    def add(self, name: str) -> int:
        """Add a name and return its offset."""
        offset = len(self.data)
        self.entries.append(SHStrTabEntry(name, offset))
        self.data += name.encode() + b"\x00"
        return offset

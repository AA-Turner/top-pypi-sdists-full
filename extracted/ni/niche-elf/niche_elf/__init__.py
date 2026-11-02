"""The niche-elf library."""

from .elf import ELFFile
from .structures import Symbol

__all__ = ["ELFFile", "Symbol"]

# https://refspecs.linuxbase.org/elf/elf.pdf
# https://www.man7.org/linux/man-pages/man5/elf.5.html

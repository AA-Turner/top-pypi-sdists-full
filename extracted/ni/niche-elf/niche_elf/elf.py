"""The main library entrypoint."""

from . import datatypes
from .builder import ELFBuilder
from .structures import Symbol
from .util import zig_target_arch_to_elf

DEFAULT_BIND: int = datatypes.Constants.STB_GLOBAL


class ELFFile:
    """Represents an ELF file (public API)."""

    def __init__(self, textbase: int) -> None:
        """
        Initialize an ELF file.

        Arguments:
            textbase: The Virtual Memory Address of the .text section of the file we are
                trying to symbolicate. (there does not need to be an actual ".text" section there)

        """
        # zig_target_arch: The target architecture for the ELF file. Run `zig targets | less` and
        #     look at the `.arch = {` structure to see the valid values.
        # ptrbits: Can either be 32 or 64. Determines the type of the ELF file.

        # For some reason, this works for me even when debugging other architectures (e.g. aarch32),
        # and when debugging from different host architectures (e.g. aarch64). So I'm pinning it to
        # x86_64 with ELFCLASS64 (which is what ptrbits controls) until we encounter some issues.
        # Important to note: ELFCLASS64 with zig_target_arch set to a more obscure architecture
        # doesn't work.
        # My stupid chungus life.
        ptrbits = 64
        zig_target_arch = "x86_64"

        if ptrbits not in {32, 64}:
            raise AssertionError(f"ptrbits must be 32 or 64, but is {ptrbits}")

        self.textbase: int = textbase
        self.zig_target_arch: str = zig_target_arch
        self.ptrsize: int = ptrbits
        self.symbols: list[Symbol] = []

    # I'm not sure whether size=0 or size=ptrsize or whatever makes a difference as a default.
    # I don't observer a difference.

    def add_generic_symbol(
        self,
        name: str,
        addr: int,
        size: int = 0,
        bind: int = DEFAULT_BIND,
    ) -> None:
        """If you don't know whether the symbols is a function or global variable use this."""
        self.symbols.append(Symbol.generic(name, addr, size, bind))

    def add_function(self, name: str, addr: int, size: int = 0, bind: int = DEFAULT_BIND) -> None:
        """Use this if you know the symbol is a function."""
        self.symbols.append(Symbol.function(name, addr, size, bind))

    def add_object(self, name: str, addr: int, size: int = 0, bind: int = DEFAULT_BIND) -> None:
        """Use this if you know the symbols is a global or local variable."""
        self.symbols.append(Symbol.object(name, addr, size, bind))

    def write(self, path: str) -> None:
        writer = ELFBuilder(zig_target_arch_to_elf(self.zig_target_arch), self.ptrsize)

        writer.add_text_section(self.textbase)
        writer.add_symbols(self.symbols)

        writer.write(path)

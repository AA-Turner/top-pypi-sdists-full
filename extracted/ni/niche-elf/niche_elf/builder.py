"""Handles crafting a minimal ELF file using structured classes."""

import ctypes
from pathlib import Path

from . import datatypes
from .structures import Section, SHStrTab, Symbol


def align(offset: int, alignment: int) -> int:
    return (offset + alignment - 1) & ~(alignment - 1)


# Section `sh_addralign` values taken from a normal executable.

class ELFBuilder:
    """Main ELF file builder."""

    def __init__(self, e_machine: int, ptrbits: int) -> None:
        if ptrbits not in {32, 64}:
            raise AssertionError(f"ptrbits must be 32 or 64, but is {ptrbits}")

        self.ElfEhdr = {32: datatypes.ElfEhdr32, 64: datatypes.ElfEhdr64}[ptrbits]
        self.ElfPhdr = {32: datatypes.ElfPhdr32, 64: datatypes.ElfPhdr64}[ptrbits]
        self.ElfShdr = {32: datatypes.ElfShdr32, 64: datatypes.ElfShdr64}[ptrbits]
        self.ElfSym = {32: datatypes.ElfSym32, 64: datatypes.ElfSym64}[ptrbits]
        # self.ElfRel = {32: datatypes.ElfRel32, 64: datatypes.ElfRel64}[ptrsize]
        # self.ElfLinkMap = {32: datatypes.ElfLinkMap32, 64: datatypes.ElfLinkMap64}[ptrsize]

        self.e_ident = (
            b"\x7fELF"
            + bytes(
                [
                    # EI_CLASS (ELFCLASS32 or ELFCLASS64)
                    ptrbits // 32,
                    # EI_DATA (ELFDATA2LSB or ELFDATA2MSB)
                    # We set it to little endian, and hope GDB figures it out regardless of the
                    # target architecture.
                    1,
                    # EI_VERSION
                    1,
                    # EI_PAD
                    0,
                ],
            )
            + b"\x00" * 8
        )

        # For some reason GDB does actually care about the e_machine field in the ELF header.
        # For some arches, the symbol addresses will be truncated to 32 bits, but its not
        # clear to me which arches exactly. Also, setting breakpoints can be broken
        # or we can encounter a SIGILL.
        self.e_machine: int = e_machine

        null_section = Section(
            "doesntmatter",
            b"",
            header=self.ElfShdr(
                sh_name=0,
                sh_type=0,
                sh_flags=0,
                sh_addr=0,
                sh_size=0,
                sh_link=0,
                sh_info=0,
                sh_addralign=1,
                sh_entsize=0,
                sh_offset=0,
            ),
        )
        self.sections: list[Section] = [null_section]
        self.shstrtab = SHStrTab()

    def add_text_section(self, addr: int) -> None:
        name_offset = self.shstrtab.add(".text")
        sec = Section(
            name=".text",
            data=b"",
            header=self.ElfShdr(
                sh_name=name_offset,
                sh_type=datatypes.Constants.SHT_NOBITS,
                sh_flags=datatypes.Constants.SHF_ALLOC | datatypes.Constants.SHF_EXECINSTR,
                sh_addr=addr,
                sh_size=-1,  # Fixed later.
                sh_link=0,
                sh_info=0,
                sh_addralign=0x10,
                sh_entsize=0,
                sh_offset=-1,  # Fixed later.
            ),
        )
        self.sections.append(sec)

    def add_symbols(self, symbols: list[Symbol]) -> None:
        strtab = bytearray(b"\x00")
        name_offsets = {}
        max_addr: int = 0
        for s in symbols:
            name_offsets[s.name] = len(strtab)
            strtab.extend(s.name.encode() + b"\x00")
            max_addr = max(max_addr, s.value + s.size)

        # Fix .text section size so examining in GDB works properly.
        # We do +1 to cover the last symbol even if its size=0.
        # Note that this may be bigger than the .text section of the loaded objfile we are trying to
        # symbolicate (e.g. it may include the .data and .bss sections), it doesn't matter.
        self.sections[1].header.sh_size = max_addr + 1 - self.sections[1].header.sh_addr

        symtab_entries = [
            self.ElfSym(
                st_name=0,
                st_value=0,
                st_size=0,
                bind=0,
                typ=0,
                st_other=0,
                st_shndx=0,
            ),
        ] + [
            self.ElfSym(
                st_name=name_offsets[s.name],
                st_value=s.value,
                st_size=s.size,
                bind=s.bind,
                typ=s.typ,
                st_other=0,
                st_shndx=1,  # Sucks that we are hardcoding, this is .text
            )
            for s in symbols
        ]

        # We add symtab then strtab,
        # so the strtab index = len(self.sections) - 1 + 2
        strtab_index = len(self.sections) + 1

        symtab_data = b"".join(bytes(e) for e in symtab_entries)
        symtab_name_offset = self.shstrtab.add(".symtab")
        symtab_sec = Section(
            name=".symtab",
            data=symtab_data,
            header=self.ElfShdr(
                sh_name=symtab_name_offset,
                sh_type=datatypes.Constants.SHT_SYMTAB,
                sh_flags=0,
                sh_addr=0,
                sh_size=len(symtab_data),
                sh_link=strtab_index,
                # See System V specific part of ELF.
                # > A symbol table section's sh_info section header member holds
                # > the symbol table index for the first non-local symbol.
                # FIXME: Check does GDB actually look at this?
                sh_info=1,
                sh_addralign=8,
                # Fucking crucial, or you'll fail a check in GDB's bfd/elf.c:bfd_section_from_shdr
                # if (hdr->sh_entsize != bed->s->sizeof_sym)
                sh_entsize=ctypes.sizeof(self.ElfSym),
                sh_offset=-1,
            ),
        )
        self.sections.append(symtab_sec)

        strtab_name_offset = self.shstrtab.add(".strtab")
        strtab_sec = Section(
            name=".strtab",
            data=bytes(strtab),
            header=self.ElfShdr(
                sh_name=strtab_name_offset,
                sh_type=datatypes.Constants.SHT_STRTAB,
                sh_flags=0,
                sh_addr=0,
                sh_size=len(strtab),
                sh_link=0,
                sh_info=0,
                sh_addralign=1,
                sh_entsize=0,
                sh_offset=-1,
            ),
        )
        self.sections.append(strtab_sec)

    def write(self, path: str) -> None:
        offset = 64  # ELF header size

        # Fix section offsets now. (but skip the NULL section)
        for sec in self.sections[1:]:
            offset = align(offset, sec.header.sh_addralign)
            sec.header.sh_offset = offset
            offset += len(sec.padded_data())

        shstrtab_sec_name_offset: int = self.shstrtab.add(".shstrtab")
        shstrtab_sec = Section(
            name=".shstrtab",
            data=self.shstrtab.data,
            header=self.ElfShdr(
                sh_name=shstrtab_sec_name_offset,
                sh_type=datatypes.Constants.SHT_STRTAB,
                sh_flags=0,
                sh_addr=0,
                sh_offset=offset,
                sh_size=len(self.shstrtab.data),
                sh_link=0,
                sh_info=0,
                sh_addralign=1,
                sh_entsize=0,
            ),
        )
        offset += len(shstrtab_sec.data)

        shoff = align(offset, 8)
        shnum = len(self.sections) + 1  # all + shstrtab
        shstrndx = shnum - 1

        header = self.ElfEhdr(
            e_ident=self.e_ident,
            e_type=datatypes.Constants.ET_EXEC,
            e_machine=self.e_machine,
            e_version=1,
            e_entry=0,
            e_phoff=0,
            e_shoff=shoff,
            e_flags=0,
            e_ehsize=ctypes.sizeof(self.ElfEhdr),
            e_phentsize=0,
            e_phnum=0,
            e_shentsize=ctypes.sizeof(self.ElfShdr),
            e_shnum=shnum,
            e_shstrndx=shstrndx,
        )

        with Path(path).open("wb") as f:
            f.write(bytes(header))

            # write sections (but skip the NULL section)
            for sec in self.sections[1:]:
                f.seek(sec.header.sh_offset)
                f.write(sec.padded_data())

            # write shstrtab
            f.seek(shstrtab_sec.header.sh_offset)
            f.write(shstrtab_sec.data)

            # write section headers
            f.seek(shoff)
            for sec in [*self.sections, shstrtab_sec]:
                f.write(sec.packed_header())

from .datatypes import Constants


# https://github.com/ziglang/zig/blob/738d2be9d6b6ef3ff3559130c05159ef53336224/lib/std/Target.zig#L1038
def zig_target_arch_to_elf(zigarch: str) -> int:  # noqa: C901, PLR0911, PLR0912
    """
    Convert a zig target architecture string to an ELF e_machine.

    To see valid values, run `zig targets | less` and look at the `.arch = {` structure.

    Raises a ValueErorr if the passed string is not a valid zig cpu architecture.
    """
    match zigarch:
        case "aarch64" | "aarch64_be":
            return Constants.EM_AARCH64
        case "alpha":
            return Constants.EM_ALPHA
        case "amdgcn":
            return Constants.EM_AMDGPU
        case "arc" | "arceb":
            return Constants.EM_ARC_COMPACT2
        case "arm" | "armeb" | "thumb" | "thumbeb":
            return Constants.EM_ARM
        case "avr":
            return Constants.EM_AVR
        case "bpfeb" | "bpfel":
            return Constants.EM_BPF
        case "csky":
            return Constants.EM_CSKY
        case "hexagon":
            return Constants.EM_QDSP6
        case "hppa" | "hppa64":
            return Constants.EM_PARISC
        case "kalimba":
            return Constants.EM_CSR_KALIMBA
        case "kvx":
            return Constants.EM_KVX
        case "lanai":
            return Constants.EM_LANAI
        case "loongarch32" | "loongarch64":
            return Constants.EM_LOONGARCH
        case "m68k":
            return Constants.EM_68K
        case "microblaze" | "microblazeel":
            return Constants.EM_MICROBLAZE
        case "mips" | "mips64" | "mipsel" | "mips64el":
            return Constants.EM_MIPS
        case "msp430":
            return Constants.EM_MSP430
        case "or1k":
            return Constants.EM_OR1K
        case "powerpc" | "powerpcle":
            return Constants.EM_PPC
        case "powerpc64" | "powerpc64le":
            return Constants.EM_PPC64
        case "propeller":
            return Constants.EM_PROPELLER
        case "riscv32" | "riscv32be" | "riscv64" | "riscv64be":
            return Constants.EM_RISCV
        case "s390x":
            return Constants.EM_S390
        case "sh" | "sheb":
            return Constants.EM_SH
        case "sparc":
            # Impossible for me to check for this here:
            # .sparc => if (target.cpu.has(.sparc, .v9)) .SPARC32PLUS else .SPARC,
            # So lets just default to SPARC. If you want EM_SPARCV9 then pass sparc64.
            return Constants.EM_SPARC
        case "sparc64":
            return Constants.EM_SPARCV9
        case "ve":
            return Constants.EM_VE
        case "x86_16" | "x86":
            return Constants.EM_386
        case "x86_64":
            return Constants.EM_X86_64
        case "xcore":
            return Constants.EM_XCORE
        case "xtensa" | "xtensaeb":
            return Constants.EM_XTENSA
        case "nvptx" | "nvptx64" | "spirv32" | "spirv64" | "wasm32" | "wasm64":
            return Constants.EM_NONE
        case _:
            raise ValueError(f"Invalid zig target {zigarch}.")

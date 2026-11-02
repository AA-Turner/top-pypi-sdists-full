# File origin: https://github.com/zeroSteiner/mayhem/blob/master/mayhem/datatypes/elf.py
# Taken from: https://github.com/Gallopsled/pwntools/blob/1320659f9ecb0ac1c8f7d66d2852051217bfdb53/pwnlib/elf/datatypes.py
# Edited by: k4lizen

#  mayhem/datatypes/elf.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import ctypes
import typing

Elf32_Addr = ctypes.c_uint32
Elf32_Half = ctypes.c_uint16
Elf32_Off = ctypes.c_uint32
Elf32_Sword = ctypes.c_int32
Elf32_Word = ctypes.c_uint32

Elf64_Addr = ctypes.c_uint64
Elf64_Half = ctypes.c_uint16
Elf64_SHalf = ctypes.c_int16
Elf64_Off = ctypes.c_uint64
Elf64_Sword = ctypes.c_int32
Elf64_Word = ctypes.c_uint32
Elf64_Xword = ctypes.c_uint64
Elf64_Sxword = ctypes.c_int64


AT_CONSTANTS = {
    0: "AT_NULL",  # /* End of vector */
    1: "AT_IGNORE",  # /* Entry should be ignored */
    2: "AT_EXECFD",  # /* File descriptor of program */
    3: "AT_PHDR",  # /* Program headers for program */
    4: "AT_PHENT",  # /* Size of program header entry */
    5: "AT_PHNUM",  # /* Number of program headers */
    6: "AT_PAGESZ",  # /* System page size */
    7: "AT_BASE",  # /* Base address of interpreter */
    8: "AT_FLAGS",  # /* Flags */
    9: "AT_ENTRY",  # /* Entry point of program */
    10: "AT_NOTELF",  # /* Program is not ELF */
    11: "AT_UID",  # /* Real uid */
    12: "AT_EUID",  # /* Effective uid */
    13: "AT_GID",  # /* Real gid */
    14: "AT_EGID",  # /* Effective gid */
    15: "AT_PLATFORM",  # /* String identifying platform */
    16: "AT_HWCAP",  # /* Machine dependent hints about processor capabilities */
    17: "AT_CLKTCK",  # /* Frequency of times() */
    18: "AT_FPUCW",
    19: "AT_DCACHEBSIZE",
    20: "AT_ICACHEBSIZE",
    21: "AT_UCACHEBSIZE",
    22: "AT_IGNOREPPC",
    23: "AT_SECURE",
    24: "AT_BASE_PLATFORM",  # String identifying real platforms
    25: "AT_RANDOM",  # Address of 16 random bytes
    31: "AT_EXECFN",  # Filename of executable
    32: "AT_SYSINFO",
    33: "AT_SYSINFO_EHDR",
    34: "AT_L1I_CACHESHAPE",
    35: "AT_L1D_CACHESHAPE",
    36: "AT_L2_CACHESHAPE",
    37: "AT_L3_CACHESHAPE",
}


class Constants:
    EI_MAG0 = 0
    EI_MAG1 = 1
    EI_MAG2 = 2
    EI_MAG3 = 3
    EI_CLASS = 4
    EI_DATA = 5
    EI_VERSION = 6
    EI_OSABI = 7
    EI_ABIVERSION = 8
    EI_PAD = 9
    EI_NIDENT = 16

    ELFMAG0 = 0x7F
    ELFMAG1 = ord("E")
    ELFMAG2 = ord("L")
    ELFMAG3 = ord("F")

    ELFCLASSNONE = 0
    ELFCLASS32 = 1
    ELFCLASS64 = 2

    ELFDATANONE = 0
    ELFDATA2LSB = 1
    ELFDATA2MSB = 2

    # Legal values for Elf_Phdr.p_type (segment type).
    PT_NULL = 0
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    PT_SHLIB = 5
    PT_PHDR = 6
    PT_TLS = 7

    # Legal values for Elf_Ehdr.e_type (object file type).
    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4

    # Legal values for Elf_Dyn.d_tag (dynamic entry type).
    DT_NULL = 0
    DT_NEEDED = 1
    DT_PLTRELSZ = 2
    DT_PLTGOT = 3
    DT_HASH = 4
    DT_STRTAB = 5
    DT_SYMTAB = 6
    DT_RELA = 7
    DT_RELASZ = 8
    DT_RELAENT = 9
    DT_STRSZ = 10
    DT_SYMENT = 11
    DT_INIT = 12
    DT_FINI = 13
    DT_SONAME = 14
    DT_RPATH = 15
    DT_SYMBOLIC = 16
    DT_REL = 17
    DT_RELSZ = 18
    DT_RELENT = 19
    DT_PLTREL = 20
    DT_DEBUG = 21
    DT_TEXTREL = 22
    DT_JMPREL = 23
    DT_ENCODING = 32

    # Legal values for Elf_Shdr.sh_type (section type).
    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    SHT_SHLIB = 10
    SHT_DYNSYM = 11
    SHT_NUM = 12

    # Legal values for ST_TYPE subfield of Elf_Sym.st_info (symbol type).
    STT_NOTYPE = 0
    STT_OBJECT = 1
    STT_FUNC = 2
    STT_SECTION = 3
    STT_FILE = 4
    STT_COMMON = 5
    STT_TLS = 6

    #
    # Notes used in ET_CORE. Architectures export some of the arch register sets
    # using the corresponding note types via the PTRACE_GETREGSET and
    # PTRACE_SETREGSET requests.
    #
    NT_PRSTATUS = 1
    NT_PRFPREG = 2
    NT_PRPSINFO = 3
    NT_TASKSTRUCT = 4
    NT_AUXV = 6
    #
    # Note to userspace developers: size of NT_SIGINFO note may increase
    # in the future to accommodate more fields, don't assume it is fixed!
    #
    NT_SIGINFO = 0x53494749
    NT_FILE = 0x46494C45
    NT_PRXFPREG = 0x46E62B7F
    NT_PPC_VMX = 0x100
    NT_PPC_SPE = 0x101
    NT_PPC_VSX = 0x102
    NT_386_TLS = 0x200
    NT_386_IOPERM = 0x201
    NT_X86_XSTATE = 0x202
    NT_S390_HIGH_GPRS = 0x300
    NT_S390_TIMER = 0x301
    NT_S390_TODCMP = 0x302
    NT_S390_TODPREG = 0x303
    NT_S390_CTRS = 0x304
    NT_S390_PREFIX = 0x305
    NT_S390_LAST_BREAK = 0x306
    NT_S390_SYSTEM_CALL = 0x307
    NT_S390_TDB = 0x308
    NT_ARM_VFP = 0x400
    NT_ARM_TLS = 0x401
    NT_ARM_HW_BREAK = 0x402
    NT_ARM_HW_WATCH = 0x403
    NT_METAG_CBUF = 0x500
    NT_METAG_RPIPE = 0x501
    NT_METAG_TLS = 0x502

    AT_NULL = 0
    AT_IGNORE = 1
    AT_EXECFD = 2
    AT_PHDR = 3
    AT_PHENT = 4
    AT_PHNUM = 5
    AT_PAGESZ = 6
    AT_BASE = 7
    AT_FLAGS = 8
    AT_ENTRY = 9
    AT_NOTELF = 10
    AT_UID = 11
    AT_EUID = 12
    AT_GID = 13
    AT_EGID = 14
    AT_PLATFORM = 15
    AT_HWCAP = 16
    AT_CLKTCK = 17
    AT_FPUCW = 18
    AT_DCACHEBSIZE = 19
    AT_ICACHEBSIZE = 20
    AT_UCACHEBSIZE = 21
    AT_IGNOREPPC = 22
    AT_SECURE = 23
    AT_BASE_PLATFORM = 24
    AT_RANDOM = 25
    AT_EXECFN = 31
    AT_SYSINFO = 32
    AT_SYSINFO_EHDR = 33
    AT_L1I_CACHESHAPE = 34
    AT_L1D_CACHESHAPE = 35
    AT_L2_CACHESHAPE = 36
    AT_L3_CACHESHAPE = 37

    # Legal flags used in the d_val field of the DT_FLAGS dynamic entry.
    DF_ORIGIN = 0x01
    DF_SYMBOLIC = 0x02
    DF_TEXTREL = 0x04
    DF_BIND_NOW = 0x08
    DF_STATIC_TLS = 0x10

    # Legal flags used in the d_val field of the DT_FLAGS_1 dynamic entry.
    DF_1_NOW = 0x00000001
    DF_1_GLOBAL = 0x00000002
    DF_1_GROUP = 0x00000004
    DF_1_NODELETE = 0x00000008
    DF_1_LOADFLTR = 0x00000010
    DF_1_INITFIRST = 0x00000020
    DF_1_NOOPEN = 0x00000040
    DF_1_ORIGIN = 0x00000080
    DF_1_DIRECT = 0x00000100
    DF_1_TRANS = 0x00000200
    DF_1_INTERPOSE = 0x00000400
    DF_1_NODEFLIB = 0x00000800
    DF_1_NODUMP = 0x00001000
    DF_1_CONFALT = 0x00002000
    DF_1_ENDFILTEE = 0x00004000
    DF_1_DISPRELDNE = 0x00008000
    DF_1_DISPRELPND = 0x00010000
    DF_1_NODIRECT = 0x00020000
    DF_1_IGNMULDEF = 0x00040000
    DF_1_NOKSYMS = 0x00080000
    DF_1_NOHDR = 0x00100000
    DF_1_EDITED = 0x00200000
    DF_1_NORELOC = 0x00400000
    DF_1_SYMINTPOSE = 0x00800000
    DF_1_GLOBAUDIT = 0x01000000
    DF_1_SINGLETON = 0x02000000

    # Flag values for the sh_flags field of section headers
    SHF_WRITE = 0x1
    SHF_ALLOC = 0x2
    SHF_EXECINSTR = 0x4
    SHF_MERGE = 0x10
    SHF_STRINGS = 0x20
    SHF_INFO_LINK = 0x40
    SHF_LINK_ORDER = 0x80
    SHF_OS_NONCONFORMING = 0x100
    SHF_GROUP = 0x200
    SHF_TLS = 0x400
    SHF_COMPRESSED = 0x800
    SHF_MASKOS = 0x0FF00000
    SHF_EXCLUDE = 0x80000000
    SHF_MASKPROC = 0xF0000000

    # st_info bindings in the symbol header
    STB_LOCAL = 0
    STB_GLOBAL = 1
    STB_WEAK = 2
    STB_NUM = 3
    STB_LOOS = 10
    STB_HIOS = 12
    STB_LOPROC = 13
    STB_HIPROC = 15

    # e_machine in the ELF header
    EM_NONE = 0  # No machine
    EM_M32 = 1  # AT&T WE 32100
    EM_SPARC = 2  # SPARC
    EM_386 = 3  # Intel 80386
    EM_68K = 4  # Motorola 68000
    EM_88K = 5  # Motorola 88000
    EM_IAMCU = 6  # Intel MCU
    EM_860 = 7  # Intel 80860
    EM_MIPS = 8  # MIPS I Architecture
    EM_S370 = 9  # IBM System/370 Processor
    EM_MIPS_RS3_LE = 10  # MIPS RS3000 Little-endian
    EM_PARISC = 15  # Hewlett-Packard PA-RISC
    EM_VPP500 = 17  # Fujitsu VPP500
    EM_SPARC32PLUS = 18  # Enhanced instruction set SPARC
    EM_960 = 19  # Intel 80960
    EM_PPC = 20  # PowerPC
    EM_PPC64 = 21  # 64-bit PowerPC
    EM_S390 = 22  # IBM System/390 Processor
    EM_SPU = 23  # IBM SPU/SPC
    EM_V800 = 36  # NEC V800
    EM_FR20 = 37  # Fujitsu FR20
    EM_RH32 = 38  # TRW RH-32
    EM_RCE = 39  # Motorola RCE
    EM_ARM = 40  # ARM 32-bit architecture (AARCH32)
    EM_ALPHA = 41  # Digital Alpha
    EM_SH = 42  # Hitachi SH
    EM_SPARCV9 = 43  # SPARC Version 9
    EM_TRICORE = 44  # Siemens TriCore embedded processor
    EM_ARC = 45  # Argonaut RISC Core, Argonaut Technologies Inc.
    EM_H8_300 = 46  # Hitachi H8/300
    EM_H8_300H = 47  # Hitachi H8/300H
    EM_H8S = 48  # Hitachi H8S
    EM_H8_500 = 49  # Hitachi H8/500
    EM_IA_64 = 50  # Intel IA-64 processor architecture
    EM_MIPS_X = 51  # Stanford MIPS-X
    EM_COLDFIRE = 52  # Motorola ColdFire
    EM_68HC12 = 53  # Motorola M68HC12
    EM_MMA = 54  # Fujitsu MMA Multimedia Accelerator
    EM_PCP = 55  # Siemens PCP
    EM_NCPU = 56  # Sony nCPU embedded RISC processor
    EM_NDR1 = 57  # Denso NDR1 microprocessor
    EM_STARCORE = 58  # Motorola Star*Core processor
    EM_ME16 = 59  # Toyota ME16 processor
    EM_ST100 = 60  # STMicroelectronics ST100 processor
    EM_TINYJ = 61  # Advanced Logic Corp. TinyJ embedded processor family
    EM_X86_64 = 62  # AMD x86-64 architecture
    EM_PDSP = 63  # Sony DSP Processor
    EM_PDP10 = 64  # Digital Equipment Corp. PDP-10
    EM_PDP11 = 65  # Digital Equipment Corp. PDP-11
    EM_FX66 = 66  # Siemens FX66 microcontroller
    EM_ST9PLUS = 67  # STMicroelectronics ST9+ 8/16 bit microcontroller
    EM_ST7 = 68  # STMicroelectronics ST7 8-bit microcontroller
    EM_68HC16 = 69  # Motorola MC68HC16 Microcontroller
    EM_68HC11 = 70  # Motorola MC68HC11 Microcontroller
    EM_68HC08 = 71  # Motorola MC68HC08 Microcontroller
    EM_68HC05 = 72  # Motorola MC68HC05 Microcontroller
    EM_SVX = 73  # Silicon Graphics SVx
    EM_ST19 = 74  # STMicroelectronics ST19 8-bit microcontroller
    EM_VAX = 75  # Digital VAX
    EM_CRIS = 76  # Axis Communications 32-bit embedded processor
    EM_JAVELIN = 77  # Infineon Technologies 32-bit embedded processor
    EM_FIREPATH = 78  # Element 14 64-bit DSP Processor
    EM_ZSP = 79  # LSI Logic 16-bit DSP Processor
    EM_MMIX = 80  # Donald Knuth's educational 64-bit processor
    EM_HUANY = 81  # Harvard University machine-independent object files
    EM_PRISM = 82  # SiTera Prism
    EM_AVR = 83  # Atmel AVR 8-bit microcontroller
    EM_FR30 = 84  # Fujitsu FR30
    EM_D10V = 85  # Mitsubishi D10V
    EM_D30V = 86  # Mitsubishi D30V
    EM_V850 = 87  # NEC v850
    EM_M32R = 88  # Mitsubishi M32R
    EM_MN10300 = 89  # Matsushita MN10300
    EM_MN10200 = 90  # Matsushita MN10200
    EM_PJ = 91  # picoJava
    EM_OPENRISC = 92  # OpenRISC 32-bit embedded processor
    EM_ARC_COMPACT = 93  # ARC International ARCompact processor (old spelling/synonym: EM_ARC_A5)
    EM_XTENSA = 94  # Tensilica Xtensa Architecture
    EM_VIDEOCORE = 95  # Alphamosaic VideoCore processor
    EM_TMM_GPP = 96  # Thompson Multimedia General Purpose Processor
    EM_NS32K = 97  # National Semiconductor 32000 series
    EM_TPC = 98  # Tenor Network TPC processor
    EM_SNP1K = 99  # Trebia SNP 1000 processor
    EM_ST200 = 100  # STMicroelectronics (www.st.com) ST200 microcontroller
    EM_IP2K = 101  # Ubicom IP2xxx microcontroller family
    EM_MAX = 102  # MAX Processor
    EM_CR = 103  # National Semiconductor CompactRISC microprocessor
    EM_F2MC16 = 104  # Fujitsu F2MC16
    EM_MSP430 = 105  # Texas Instruments embedded microcontroller msp430
    EM_BLACKFIN = 106  # Analog Devices Blackfin (DSP) processor
    EM_SE_C33 = 107  # S1C33 Family of Seiko Epson processors
    EM_SEP = 108  # Sharp embedded microprocessor
    EM_ARCA = 109  # Arca RISC Microprocessor
    EM_UNICORE = 110  # Microprocessor series from PKU-Unity Ltd. and MPRC of Peking University
    EM_EXCESS = 111  # eXcess: 16/32/64-bit configurable embedded CPU
    EM_DXP = 112  # Icera Semiconductor Inc. Deep Execution Processor
    EM_ALTERA_NIOS2 = 113  # Altera Nios II soft-core processor
    EM_CRX = 114  # National Semiconductor CompactRISC CRX microprocessor
    EM_XGATE = 115  # Motorola XGATE embedded processor
    EM_C166 = 116  # Infineon C16x/XC16x processor
    EM_M16C = 117  # Renesas M16C series microprocessors
    EM_DSPIC30F = 118  # Microchip Technology dsPIC30F Digital Signal Controller
    EM_CE = 119  # Freescale Communication Engine RISC core
    EM_M32C = 120  # Renesas M32C series microprocessors
    EM_TSK3000 = 131  # Altium TSK3000 core
    EM_RS08 = 132  # Freescale RS08 embedded processor
    EM_SHARC = 133  # Analog Devices SHARC family of 32-bit DSP processors
    EM_ECOG2 = 134  # Cyan Technology eCOG2 microprocessor
    EM_SCORE7 = 135  # Sunplus S+core7 RISC processor
    EM_DSP24 = 136  # New Japan Radio (NJR) 24-bit DSP Processor
    EM_VIDEOCORE3 = 137  # Broadcom VideoCore III processor
    EM_LATTICEMICO32 = 138  # RISC processor for Lattice FPGA architecture
    EM_SE_C17 = 139  # Seiko Epson C17 family
    EM_TI_C6000 = 140  # The Texas Instruments TMS320C6000 DSP family
    EM_TI_C2000 = 141  # The Texas Instruments TMS320C2000 DSP family
    EM_TI_C5500 = 142  # The Texas Instruments TMS320C55x DSP family
    EM_TI_ARP32 = 143  # Texas Instruments Application Specific RISC Processor 32bit fetch
    EM_TI_PRU = 144  # Texas Instruments Programmable Realtime Unit
    EM_MMDSP_PLUS = 160  # STMicroelectronics 64bit VLIW Data Signal Processor
    EM_CYPRESS_M8C = 161  # Cypress M8C microprocessor
    EM_R32C = 162  # Renesas R32C series microprocessors
    EM_TRIMEDIA = 163  # NXP Semiconductors TriMedia architecture family
    EM_QDSP6 = 164  # QUALCOMM DSP6 Processor
    EM_8051 = 165  # Intel 8051 and variants
    EM_STXP7X = 166  # STMicroelectronics STxP7x family of configurable and extensible RISC processors  # noqa: E501
    EM_NDS32 = 167  # Andes Technology compact code size embedded RISC processor family
    EM_ECOG1 = 168  # Cyan Technology eCOG1X family
    EM_ECOG1X = 168  # Cyan Technology eCOG1X family
    EM_MAXQ30 = 169  # Dallas Semiconductor MAXQ30 Core Micro-controllers
    EM_XIMO16 = 170  # New Japan Radio (NJR) 16-bit DSP Processor
    EM_MANIK = 171  # M2000 Reconfigurable RISC Microprocessor
    EM_CRAYNV2 = 172  # Cray Inc. NV2 vector architecture
    EM_RX = 173  # Renesas RX family
    EM_METAG = 174  # Imagination Technologies META processor architecture
    EM_MCST_ELBRUS = 175  # MCST Elbrus general purpose hardware architecture
    EM_ECOG16 = 176  # Cyan Technology eCOG16 family
    EM_CR16 = 177  # National Semiconductor CompactRISC CR16 16-bit microprocessor
    EM_ETPU = 178  # Freescale Extended Time Processing Unit
    EM_SLE9X = 179  # Infineon Technologies SLE9X core
    EM_L10M = 180  # Intel L10M
    EM_K10M = 181  # Intel K10M
    EM_AARCH64 = 183  # ARM 64-bit architecture (AARCH64)
    EM_AVR32 = 185  # Atmel Corporation 32-bit microprocessor family
    EM_STM8 = 186  # STMicroeletronics STM8 8-bit microcontroller
    EM_TILE64 = 187  # Tilera TILE64 multicore architecture family
    EM_TILEPRO = 188  # Tilera TILEPro multicore architecture family
    EM_MICROBLAZE = 189  # Xilinx MicroBlaze 32-bit RISC soft processor core
    EM_CUDA = 190  # NVIDIA CUDA architecture
    EM_TILEGX = 191  # Tilera TILE-Gx multicore architecture family
    EM_CLOUDSHIELD = 192  # CloudShield architecture family
    EM_COREA_1ST = 193  # KIPO-KAIST Core-A 1st generation processor family
    EM_COREA_2ND = 194  # KIPO-KAIST Core-A 2nd generation processor family
    EM_ARC_COMPACT2 = 195  # Synopsys ARCompact V2
    EM_OPEN8 = 196  # Open8 8-bit RISC soft processor core
    EM_RL78 = 197  # Renesas RL78 family
    EM_VIDEOCORE5 = 198  # Broadcom VideoCore V processor
    EM_78KOR = 199  # Renesas 78KOR family
    EM_56800EX = 200  # Freescale 56800EX Digital Signal Controller (DSC)
    EM_BA1 = 201  # Beyond BA1 CPU architecture
    EM_BA2 = 202  # Beyond BA2 CPU architecture
    EM_XCORE = 203  # XMOS xCORE processor family
    EM_MCHP_PIC = 204  # Microchip 8-bit PIC(r) family
    EM_INTEL205 = 205  # Reserved by Intel
    EM_INTEL206 = 206  # Reserved by Intel
    EM_INTEL207 = 207  # Reserved by Intel
    EM_INTEL208 = 208  # Reserved by Intel
    EM_INTEL209 = 209  # Reserved by Intel
    EM_KM32 = 210  # KM211 KM32 32-bit processor
    EM_KMX32 = 211  # KM211 KMX32 32-bit processor
    EM_KMX16 = 212  # KM211 KMX16 16-bit processor
    EM_KMX8 = 213  # KM211 KMX8 8-bit processor
    EM_KVARC = 214  # KM211 KVARC processor
    EM_CDP = 215  # Paneve CDP architecture family
    EM_COGE = 216  # Cognitive Smart Memory Processor
    EM_COOL = 217  # Bluechip Systems CoolEngine
    EM_NORC = 218  # Nanoradio Optimized RISC
    EM_CSR_KALIMBA = 219  # CSR Kalimba architecture family
    EM_Z80 = 220  # Zilog Z80
    EM_VISIUM = 221  # Controls and Data Services VISIUMcore processor
    EM_FT32 = 222  # FTDI Chip FT32 high performance 32-bit RISC architecture
    EM_MOXIE = 223  # Moxie processor family
    EM_AMDGPU = 224  # AMD GPU architecture
    EM_RISCV = 243  # RISC-V
    EM_BPF = 247  # Linux BPF - in-kernel virtual machine
    EM_CSKY = 252  # C-SKY
    EM_LOONGARCH = 258  # LoongArch
    EM_FRV = 0x5441  # Fujitsu FR-V
    # Reservations
    # reserved  11-14   Reserved for future use
    # reserved  16      Reserved for future use
    # reserved  24-35   Reserved for future use
    # reserved  121-130 Reserved for future use
    # reserved  145-159 Reserved for future use
    # reserved  145-159 Reserved for future use
    # reserved  182     Reserved for future Intel use
    # reserved  184     Reserved for future ARM use
    # unknown/reserve?  225 - 242

    # Extra architectures pulled from
    # https://github.com/ziglang/zig/blob/738d2be9d6b6ef3ff3559130c05159ef53336224/lib/std/elf.zig#L1711
    # should probably just be taking directly from
    # http://www.sco.com/developers/gabi/latest/ch4.eheader.html ...
    EM_KVX = 256  # Kalray VLIW core of the MPPA processor family
    EM_LANAI = 244  # Lanai 32-bit processor
    EM_OR1K = 92  # OpenRISC 1000 32-bit embedded processor
    # Parallax Propeller (P1)
    # This value is an unofficial ELF value used in: https://github.com/parallaxinc/propgcc
    EM_PROPELLER = 0x5072
    EM_VE = 251  # NEC Vector Engine


class ElfEhdr32(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("e_ident", (ctypes.c_ubyte * 16)),
        ("e_type", Elf32_Half),
        ("e_machine", Elf32_Half),
        ("e_version", Elf32_Word),
        ("e_entry", Elf32_Addr),
        ("e_phoff", Elf32_Off),
        ("e_shoff", Elf32_Off),
        ("e_flags", Elf32_Word),
        ("e_ehsize", Elf32_Half),
        ("e_phentsize", Elf32_Half),
        ("e_phnum", Elf32_Half),
        ("e_shentsize", Elf32_Half),
        ("e_shnum", Elf32_Half),
        ("e_shstrndx", Elf32_Half),
    ]

    def __init__(
        self,
        *,
        e_ident: bytes | bytearray,
        e_type: int,
        e_machine: int,
        e_version: int,
        e_entry: int,
        e_phoff: int,
        e_shoff: int,
        e_flags: int,
        e_ehsize: int,
        e_phentsize: int,
        e_phnum: int,
        e_shentsize: int,
        e_shnum: int,
        e_shstrndx: int,
    ) -> None:
        super().__init__()
        self.e_ident[:] = e_ident
        self.e_type = e_type
        self.e_machine = e_machine
        self.e_version = e_version
        self.e_entry = e_entry
        self.e_phoff = e_phoff
        self.e_shoff = e_shoff
        self.e_flags = e_flags
        self.e_ehsize = e_ehsize
        self.e_phentsize = e_phentsize
        self.e_phnum = e_phnum
        self.e_shentsize = e_shentsize
        self.e_shnum = e_shnum
        self.e_shstrndx = e_shstrndx


class ElfEhdr64(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("e_ident", (ctypes.c_ubyte * 16)),
        ("e_type", Elf64_Half),
        ("e_machine", Elf64_Half),
        ("e_version", Elf64_Word),
        ("e_entry", Elf64_Addr),
        ("e_phoff", Elf64_Off),
        ("e_shoff", Elf64_Off),
        ("e_flags", Elf64_Word),
        ("e_ehsize", Elf64_Half),
        ("e_phentsize", Elf64_Half),
        ("e_phnum", Elf64_Half),
        ("e_shentsize", Elf64_Half),
        ("e_shnum", Elf64_Half),
        ("e_shstrndx", Elf64_Half),
    ]

    def __init__(
        self,
        *,
        e_ident: bytes | bytearray,
        e_type: int,
        e_machine: int,
        e_version: int,
        e_entry: int,
        e_phoff: int,
        e_shoff: int,
        e_flags: int,
        e_ehsize: int,
        e_phentsize: int,
        e_phnum: int,
        e_shentsize: int,
        e_shnum: int,
        e_shstrndx: int,
    ) -> None:
        super().__init__()
        self.e_ident[:] = e_ident
        self.e_type = e_type
        self.e_machine = e_machine
        self.e_version = e_version
        self.e_entry = e_entry
        self.e_phoff = e_phoff
        self.e_shoff = e_shoff
        self.e_flags = e_flags
        self.e_ehsize = e_ehsize
        self.e_phentsize = e_phentsize
        self.e_phnum = e_phnum
        self.e_shentsize = e_shentsize
        self.e_shnum = e_shnum
        self.e_shstrndx = e_shstrndx


class ElfPhdr32(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("p_type", Elf32_Word),
        ("p_offset", Elf32_Off),
        ("p_vaddr", Elf32_Addr),
        ("p_paddr", Elf32_Addr),
        ("p_filesz", Elf32_Word),
        ("p_memsz", Elf32_Word),
        ("p_flags", Elf32_Word),
        ("p_align", Elf32_Word),
    ]

    def __init__(
        self,
        *,
        p_type: int,
        p_offset: int,
        p_vaddr: int,
        p_paddr: int,
        p_filesz: int,
        p_memsz: int,
        p_flags: int,
        p_align: int,
    ) -> None:
        super().__init__()
        self.p_type = p_type
        self.p_offset = p_offset
        self.p_vaddr = p_vaddr
        self.p_paddr = p_paddr
        self.p_filesz = p_filesz
        self.p_memsz = p_memsz
        self.p_flags = p_flags
        self.p_align = p_align


class ElfPhdr64(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("p_type", Elf64_Word),
        ("p_flags", Elf64_Word),
        ("p_offset", Elf64_Off),
        ("p_vaddr", Elf64_Addr),
        ("p_paddr", Elf64_Addr),
        ("p_filesz", Elf64_Xword),
        ("p_memsz", Elf64_Xword),
        ("p_align", Elf64_Xword),
    ]

    def __init__(
        self,
        *,
        p_type: int,
        p_flags: int,
        p_offset: int,
        p_vaddr: int,
        p_paddr: int,
        p_filesz: int,
        p_memsz: int,
        p_align: int,
    ) -> None:
        super().__init__()
        self.p_type = p_type
        self.p_flags = p_flags
        self.p_offset = p_offset
        self.p_vaddr = p_vaddr
        self.p_paddr = p_paddr
        self.p_filesz = p_filesz
        self.p_memsz = p_memsz
        self.p_align = p_align


class ElfShdr32(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("sh_name", Elf32_Word),
        ("sh_type", Elf32_Word),
        ("sh_flags", Elf32_Word),
        ("sh_addr", Elf32_Addr),
        ("sh_offset", Elf32_Off),
        ("sh_size", Elf32_Word),
        ("sh_link", Elf32_Word),
        ("sh_info", Elf32_Word),
        ("sh_addralign", Elf32_Word),
        ("sh_entsize", Elf32_Word),
    ]

    def __init__(
        self,
        *,
        sh_name: int,
        sh_type: int,
        sh_flags: int,
        sh_addr: int,
        sh_offset: int,
        sh_size: int,
        sh_link: int,
        sh_info: int,
        sh_addralign: int,
        sh_entsize: int,
    ) -> None:
        super().__init__()
        self.sh_name = sh_name
        self.sh_type = sh_type
        self.sh_flags = sh_flags
        self.sh_addr = sh_addr
        self.sh_offset = sh_offset
        self.sh_size = sh_size
        self.sh_link = sh_link
        self.sh_info = sh_info
        self.sh_addralign = sh_addralign
        self.sh_entsize = sh_entsize


class ElfShdr64(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("sh_name", Elf64_Word),
        ("sh_type", Elf64_Word),
        ("sh_flags", Elf64_Xword),
        ("sh_addr", Elf64_Addr),
        ("sh_offset", Elf64_Off),
        ("sh_size", Elf64_Xword),
        ("sh_link", Elf64_Word),
        ("sh_info", Elf64_Word),
        ("sh_addralign", Elf64_Xword),
        ("sh_entsize", Elf64_Xword),
    ]

    def __init__(
        self,
        *,
        sh_name: int,
        sh_type: int,
        sh_flags: int,
        sh_addr: int,
        sh_offset: int,
        sh_size: int,
        sh_link: int,
        sh_info: int,
        sh_addralign: int,
        sh_entsize: int,
    ) -> None:
        super().__init__()
        self.sh_name = sh_name
        self.sh_type = sh_type
        self.sh_flags = sh_flags
        self.sh_addr = sh_addr
        self.sh_offset = sh_offset
        self.sh_size = sh_size
        self.sh_link = sh_link
        self.sh_info = sh_info
        self.sh_addralign = sh_addralign
        self.sh_entsize = sh_entsize


class ElfDynUN32(ctypes.Union):
    _fields_: typing.ClassVar = [
        ("d_val", Elf32_Sword),
        ("d_ptr", Elf32_Addr),
    ]

    def __init__(self, *, d_val: int, d_ptr: int) -> None:
        super().__init__()
        self.d_val = d_val
        self.d_ptr = d_ptr


class ElfDyn32(ctypes.Structure):
    _anonymous_ = ("d_un",)
    _fields_: typing.ClassVar = [
        ("d_tag", Elf32_Sword),
        ("d_un", ElfDynUN32),
    ]

    def __init__(self, *, d_tag: int, d_un: ElfDynUN32) -> None:
        super().__init__()
        self.d_tag = d_tag
        self.d_un = d_un


class ElfDynUN64(ctypes.Union):
    _fields_: typing.ClassVar = [
        ("d_val", Elf64_Xword),
        ("d_ptr", Elf64_Addr),
    ]

    def __init__(self, *, d_val: int, d_ptr: int) -> None:
        super().__init__()
        self.d_val = d_val
        self.d_ptr = d_ptr


class ElfDyn64(ctypes.Structure):
    _anonymous_ = ("d_un",)
    _fields_: typing.ClassVar = [
        ("d_tag", Elf64_Sxword),
        ("d_un", ElfDynUN64),
    ]

    def __init__(self, *, d_tag: int, d_un: ElfDynUN64) -> None:
        super().__init__()
        self.d_tag = d_tag
        self.d_un = d_un


class ElfSym32(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("st_name", Elf32_Word),
        ("st_value", Elf32_Addr),
        ("st_size", Elf32_Word),
        ("st_info", ctypes.c_ubyte),
        ("st_other", ctypes.c_ubyte),
        ("st_shndx", Elf32_Half),
    ]

    def __init__(
        self,
        *,
        st_name: int,
        st_value: int,
        st_size: int,
        bind: int,
        typ: int,
        st_other: int,
        st_shndx: int,
    ) -> None:
        super().__init__()
        self.st_name = st_name
        self.st_value = st_value
        self.st_size = st_size
        self.st_info = (bind << 4) | typ
        self.st_other = st_other
        self.st_shndx = st_shndx


class ElfSym64(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("st_name", Elf64_Word),
        ("st_info", ctypes.c_ubyte),
        ("st_other", ctypes.c_ubyte),
        ("st_shndx", Elf64_Half),
        ("st_value", Elf64_Addr),
        ("st_size", Elf64_Xword),
    ]

    def __init__(
        self,
        *,
        st_name: int,
        bind: int,
        typ: int,
        st_other: int,
        st_shndx: int,
        st_value: int,
        st_size: int,
    ) -> None:
        super().__init__()
        self.st_name = st_name
        self.st_info = (bind << 4) | typ
        self.st_other = st_other
        self.st_shndx = st_shndx
        self.st_value = st_value
        self.st_size = st_size


class ElfRel64(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("r_offset", Elf64_Addr),
        ("r_info", Elf64_Xword),
        ("r_addend", Elf64_Sxword),
    ]

    def __init__(
        self,
        *,
        r_offset: int,
        r_info: int,
        r_addend: int,
    ) -> None:
        super().__init__()
        self.r_offset = r_offset
        self.r_info = r_info
        self.r_addend = r_addend


class ElfRel32(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("r_offset", Elf32_Addr),
        ("r_info", Elf32_Word),
    ]

    def __init__(self, *, r_offset: int, r_info: int) -> None:
        super().__init__()
        self.r_offset = r_offset
        self.r_info = r_info


class ElfLinkMap32(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("l_addr", Elf32_Addr),
        ("l_name", Elf32_Addr),
        ("l_ld", Elf32_Addr),
        ("l_next", Elf32_Addr),
        ("l_prev", Elf32_Addr),
    ]

    def __init__(
        self,
        *,
        l_addr: int,
        l_name: int,
        l_ld: int,
        l_next: int,
        l_prev: int,
    ) -> None:
        super().__init__()
        self.l_addr = l_addr
        self.l_name = l_name
        self.l_ld = l_ld
        self.l_next = l_next
        self.l_prev = l_prev


class ElfLinkMap64(ctypes.Structure):
    _fields_: typing.ClassVar = [
        ("l_addr", Elf64_Addr),
        ("l_name", Elf64_Addr),
        ("l_ld", Elf64_Addr),
        ("l_next", Elf64_Addr),
        ("l_prev", Elf64_Addr),
    ]

    def __init__(
        self,
        *,
        l_addr: int,
        l_name: int,
        l_ld: int,
        l_next: int,
        l_prev: int,
    ) -> None:
        super().__init__()
        self.l_addr = l_addr
        self.l_name = l_name
        self.l_ld = l_ld
        self.l_next = l_next
        self.l_prev = l_prev

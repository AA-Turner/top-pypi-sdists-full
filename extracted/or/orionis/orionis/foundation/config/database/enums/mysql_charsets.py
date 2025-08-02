from enum import Enum

class MySQLCharset(Enum):
    """
    Enumeration of supported MySQL character sets.
    Each member of this enum represents a valid character set name that can be used in MySQL database configurations.
    These character sets determine how text is stored and compared in the database.
    Attributes:
        ARMSCII8: Armenian Standard Code for Information Interchange, 8-bit.
        ASCII: US ASCII.
        BIG5: Big5 Traditional Chinese.
        BINARY: Binary pseudo charset.
        CP1250: Windows Central European.
        CP1251: Windows Cyrillic.
        CP1256: Windows Arabic.
        CP1257: Windows Baltic.
        CP850: DOS West European.
        CP852: DOS Central European.
        CP866: DOS Russian.
        CP932: SJIS for Windows Japanese.
        DEC8: DEC West European.
        EUCJPMS: UJIS for Windows Japanese.
        EUCKR: EUC-KR Korean.
        GB2312: GB2312 Simplified Chinese.
        GBK: GBK Simplified Chinese.
        GEOSTD8: GEOSTD8 Georgian.
        GREEK: ISO 8859-7 Greek.
        HEBREW: ISO 8859-8 Hebrew.
        HP8: HP West European.
        KEYBCS2: DOS Kamenicky Czech-Slovak.
        KOI8R: KOI8-R Relcom Russian.
        KOI8U: KOI8-U Ukrainian.
        LATIN1: cp1252 West European.
        LATIN2: ISO 8859-2 Central European.
        LATIN5: ISO 8859-9 Turkish.
        LATIN7: ISO 8859-13 Baltic.
        MACCE: Mac Central European.
        MACROMAN: Mac West European.
        SJIS: Shift-JIS Japanese.
        SWE7: 7bit Swedish.
        TIS620: TIS620 Thai.
        UCS2: UCS-2 Unicode.
        UJIS: EUC-JP Japanese.
        UTF16: UTF-16 Unicode.
        UTF16LE: UTF-16LE Unicode.
        UTF32: UTF-32 Unicode.
        UTF8: UTF-8 Unicode.
        UTF8MB3: UTF-8 Unicode (3-byte).
        UTF8MB4: UTF-8 Unicode (4-byte).
    """

    ARMSCII8 = "armscii8"
    ASCII = "ascii"
    BIG5 = "big5"
    BINARY = "binary"
    CP1250 = "cp1250"
    CP1251 = "cp1251"
    CP1256 = "cp1256"
    CP1257 = "cp1257"
    CP850 = "cp850"
    CP852 = "cp852"
    CP866 = "cp866"
    CP932 = "cp932"
    DEC8 = "dec8"
    EUCJPMS = "eucjpms"
    EUCKR = "euckr"
    GB2312 = "gb2312"
    GBK = "gbk"
    GEOSTD8 = "geostd8"
    GREEK = "greek"
    HEBREW = "hebrew"
    HP8 = "hp8"
    KEYBCS2 = "keybcs2"
    KOI8R = "koi8r"
    KOI8U = "koi8u"
    LATIN1 = "latin1"
    LATIN2 = "latin2"
    LATIN5 = "latin5"
    LATIN7 = "latin7"
    MACCE = "macce"
    MACROMAN = "macroman"
    SJIS = "sjis"
    SWE7 = "swe7"
    TIS620 = "tis620"
    UCS2 = "ucs2"
    UJIS = "ujis"
    UTF16 = "utf16"
    UTF16LE = "utf16le"
    UTF32 = "utf32"
    UTF8 = "utf8"
    UTF8MB3 = "utf8mb3"
    UTF8MB4 = "utf8mb4"
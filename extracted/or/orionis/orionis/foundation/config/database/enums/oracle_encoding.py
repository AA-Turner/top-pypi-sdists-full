from enum import Enum

class OracleEncoding(Enum):
    """
    Enumeration of common Oracle database character encodings.

    Each member represents a specific Oracle encoding name, typically used for database character set configuration.
    The enum values correspond to Oracle's official encoding identifiers.

    Members:
        AL32UTF8: Unicode UTF-8 (recommended)
        AR8MSWIN1256: Arabic Windows
        JA16EUC: Japanese EUC
        JA16SJIS: Japanese Shift-JIS
        KO16MSWIN949: Korean Windows
        TH8TISASCII: Thai
        TR8MSWIN1254: Turkish Windows
        WE8ISO8859P1: Western European ISO
        WE8MSWIN1252: Western European Windows
        ZHS16GBK: Simplified Chinese GBK
        ZHT16BIG5: Traditional Chinese Big5
        ZHT32EUC: Traditional Chinese EUC
        CL8MSWIN1251: Cyrillic Windows
        EE8MSWIN1250: Central European Windows
        EL8MSWIN1253: Greek Windows
        IW8MSWIN1255: Hebrew Windows
    """

    AL32UTF8 = "AL32UTF8"              # Unicode UTF-8 (recomendado)
    AR8MSWIN1256 = "AR8MSWIN1256"      # Arabic Windows
    JA16EUC = "JA16EUC"                # Japanese EUC
    JA16SJIS = "JA16SJIS"              # Japanese Shift-JIS
    KO16MSWIN949 = "KO16MSWIN949"      # Korean Windows
    TH8TISASCII = "TH8TISASCII"        # Thai
    TR8MSWIN1254 = "TR8MSWIN1254"      # Turkish Windows
    WE8ISO8859P1 = "WE8ISO8859P1"      # Western European ISO
    WE8MSWIN1252 = "WE8MSWIN1252"      # Western European Windows
    ZHS16GBK = "ZHS16GBK"              # Simplified Chinese GBK
    ZHT16BIG5 = "ZHT16BIG5"            # Traditional Chinese Big5
    ZHT32EUC = "ZHT32EUC"              # Traditional Chinese EUC
    CL8MSWIN1251 = "CL8MSWIN1251"      # Cyrillic Windows
    EE8MSWIN1250 = "EE8MSWIN1250"      # Central European Windows
    EL8MSWIN1253 = "EL8MSWIN1253"      # Greek Windows
    IW8MSWIN1255 = "IW8MSWIN1255"      # Hebrew Windows
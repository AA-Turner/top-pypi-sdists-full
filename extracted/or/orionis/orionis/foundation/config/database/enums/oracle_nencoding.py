from enum import Enum

class OracleNencoding(Enum):
    """
    Represents a specific type of Oracle encoding for NCHAR and NVARCHAR2 data types.

    This class inherits from OracleEncoding and can be extended to implement
    custom behaviors or properties related to Oracle's national character set encoding.

    Attributes:
        Inherits all attributes from OracleEncoding.

    Methods:
        Inherits all methods from OracleEncoding.
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
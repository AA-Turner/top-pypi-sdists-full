from enum import Enum

class PGSQLCharset(Enum):
    """
    Enumeration of supported PostgreSQL character encodings.
    Each member of this enum represents a valid encoding name that can be used in PostgreSQL databases.
    These encodings determine how text data is stored and interpreted in the database.
    Members:
        BIG5: Traditional Chinese encoding.
        EUC_CN: Extended Unix Code for Simplified Chinese.
        EUC_JP: Extended Unix Code for Japanese.
        EUC_KR: Extended Unix Code for Korean.
        EUC_TW: Extended Unix Code for Traditional Chinese.
        GB18030: Chinese National Standard encoding.
        GBK: Extended Guobiao encoding for Simplified Chinese.
        ISO_8859_5: ISO 8859-5 Cyrillic encoding.
        ISO_8859_6: ISO 8859-6 Arabic encoding.
        ISO_8859_7: ISO 8859-7 Greek encoding.
        ISO_8859_8: ISO 8859-8 Hebrew encoding.
        JOHAB: Korean Johab encoding.
        KOI8R: KOI8-R Russian encoding.
        KOI8U: KOI8-U Ukrainian encoding.
        LATIN1: ISO 8859-1 Western European encoding.
        LATIN2: ISO 8859-2 Central European encoding.
        LATIN3: ISO 8859-3 South European encoding.
        LATIN4: ISO 8859-4 North European encoding.
        LATIN5: ISO 8859-9 Turkish encoding.
        LATIN6: ISO 8859-10 Nordic encoding.
        LATIN7: ISO 8859-13 Baltic Rim encoding.
        LATIN8: ISO 8859-14 Celtic encoding.
        LATIN9: ISO 8859-15 Western European encoding with Euro.
        LATIN10: ISO 8859-16 South-Eastern European encoding.
        MULE_INTERNAL: Mule internal encoding.
        SJIS: Shift JIS Japanese encoding.
        SQL_ASCII: No encoding; raw bytes.
        UHC: Unified Hangul Code for Korean.
        UTF8: Unicode UTF-8 encoding.
        WIN866: Windows code page 866 (Cyrillic).
        WIN874: Windows code page 874 (Thai).
        WIN1250: Windows code page 1250 (Central European).
        WIN1251: Windows code page 1251 (Cyrillic).
        WIN1252: Windows code page 1252 (Western European).
        WIN1253: Windows code page 1253 (Greek).
        WIN1254: Windows code page 1254 (Turkish).
        WIN1255: Windows code page 1255 (Hebrew).
        WIN1256: Windows code page 1256 (Arabic).
        WIN1257: Windows code page 1257 (Baltic).
        WIN1258: Windows code page 1258 (Vietnamese).
    """

    BIG5 = "BIG5"
    EUC_CN = "EUC_CN"
    EUC_JP = "EUC_JP"
    EUC_KR = "EUC_KR"
    EUC_TW = "EUC_TW"
    GB18030 = "GB18030"
    GBK = "GBK"
    ISO_8859_5 = "ISO_8859_5"
    ISO_8859_6 = "ISO_8859_6"
    ISO_8859_7 = "ISO_8859_7"
    ISO_8859_8 = "ISO_8859_8"
    JOHAB = "JOHAB"
    KOI8R = "KOI8R"
    KOI8U = "KOI8U"
    LATIN1 = "LATIN1"
    LATIN2 = "LATIN2"
    LATIN3 = "LATIN3"
    LATIN4 = "LATIN4"
    LATIN5 = "LATIN5"
    LATIN6 = "LATIN6"
    LATIN7 = "LATIN7"
    LATIN8 = "LATIN8"
    LATIN9 = "LATIN9"
    LATIN10 = "LATIN10"
    MULE_INTERNAL = "MULE_INTERNAL"
    SJIS = "SJIS"
    SQL_ASCII = "SQL_ASCII"
    UHC = "UHC"
    UTF8 = "UTF8"
    WIN866 = "WIN866"
    WIN874 = "WIN874"
    WIN1250 = "WIN1250"
    WIN1251 = "WIN1251"
    WIN1252 = "WIN1252"
    WIN1253 = "WIN1253"
    WIN1254 = "WIN1254"
    WIN1255 = "WIN1255"
    WIN1256 = "WIN1256"
    WIN1257 = "WIN1257"
    WIN1258 = "WIN1258"

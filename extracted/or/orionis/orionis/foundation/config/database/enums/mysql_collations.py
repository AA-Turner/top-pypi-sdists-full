from enum import Enum

class MySQLCollation(Enum):
    """
    Enumeration of common MySQL collations.
    This enum provides a set of string constants representing various MySQL collations,
    including those for UTF-8, UTF-8MB4, Latin1, ASCII, UCS2, UTF16, and UTF32 character sets.
    Each member corresponds to a specific collation name as used in MySQL databases.
    Attributes:
        UTF8_GENERAL_CI: 'utf8_general_ci' - UTF-8, case-insensitive, general collation.
        UTF8_UNICODE_CI: 'utf8_unicode_ci' - UTF-8, case-insensitive, Unicode collation.
        UTF8_BIN: 'utf8_bin' - UTF-8, binary collation.
        UTF8MB4_GENERAL_CI: 'utf8mb4_general_ci' - UTF-8MB4, case-insensitive, general collation.
        UTF8MB4_UNICODE_CI: 'utf8mb4_unicode_ci' - UTF-8MB4, case-insensitive, Unicode collation.
        UTF8MB4_BIN: 'utf8mb4_bin' - UTF-8MB4, binary collation.
        LATIN1_SWEDISH_CI: 'latin1_swedish_ci' - Latin1, case-insensitive, Swedish collation.
        LATIN1_GENERAL_CI: 'latin1_general_ci' - Latin1, case-insensitive, general collation.
        LATIN1_BIN: 'latin1_bin' - Latin1, binary collation.
        ASCII_GENERAL_CI: 'ascii_general_ci' - ASCII, case-insensitive, general collation.
        ASCII_BIN: 'ascii_bin' - ASCII, binary collation.
        UCS2_GENERAL_CI: 'ucs2_general_ci' - UCS2, case-insensitive, general collation.
        UCS2_UNICODE_CI: 'ucs2_unicode_ci' - UCS2, case-insensitive, Unicode collation.
        UCS2_BIN: 'ucs2_bin' - UCS2, binary collation.
        UTF16_GENERAL_CI: 'utf16_general_ci' - UTF-16, case-insensitive, general collation.
        UTF16_UNICODE_CI: 'utf16_unicode_ci' - UTF-16, case-insensitive, Unicode collation.
        UTF16_BIN: 'utf16_bin' - UTF-16, binary collation.
        UTF32_GENERAL_CI: 'utf32_general_ci' - UTF-32, case-insensitive, general collation.
        UTF32_UNICODE_CI: 'utf32_unicode_ci' - UTF-32, case-insensitive, Unicode collation.
        UTF32_BIN: 'utf32_bin' - UTF-32, binary collation.
    Methods:
        list(): Returns a list of all collation string values defined in the enumeration.
    """

    UTF8_GENERAL_CI = "utf8_general_ci"
    UTF8_UNICODE_CI = "utf8_unicode_ci"
    UTF8_BIN = "utf8_bin"
    UTF8MB4_GENERAL_CI = "utf8mb4_general_ci"
    UTF8MB4_UNICODE_CI = "utf8mb4_unicode_ci"
    UTF8MB4_BIN = "utf8mb4_bin"
    LATIN1_SWEDISH_CI = "latin1_swedish_ci"
    LATIN1_GENERAL_CI = "latin1_general_ci"
    LATIN1_BIN = "latin1_bin"
    ASCII_GENERAL_CI = "ascii_general_ci"
    ASCII_BIN = "ascii_bin"
    UCS2_GENERAL_CI = "ucs2_general_ci"
    UCS2_UNICODE_CI = "ucs2_unicode_ci"
    UCS2_BIN = "ucs2_bin"
    UTF16_GENERAL_CI = "utf16_general_ci"
    UTF16_UNICODE_CI = "utf16_unicode_ci"
    UTF16_BIN = "utf16_bin"
    UTF32_GENERAL_CI = "utf32_general_ci"
    UTF32_UNICODE_CI = "utf32_unicode_ci"
    UTF32_BIN = "utf32_bin"
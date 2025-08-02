from enum import Enum

class PGSQLCollation(Enum):
    """
    Enumeration of common collations in PostgreSQL.
    PostgreSQL supports collations based on the operating system and locales.
    The names may vary depending on the system, but some common ones are listed here.
    Attributes:
        C: 'C' - Binary collation, fast, based on byte order.
        POSIX: 'POSIX' - Similar to 'C', binary order.
        EN_US: 'en_US' - English (United States), case-sensitive.
        EN_US_UTF8: 'en_US.utf8' - English (United States), UTF-8 encoding.
        ES_ES: 'es_ES' - Spanish (Spain).
        ES_ES_UTF8: 'es_ES.utf8' - Spanish (Spain), UTF-8 encoding.
        DE_DE: 'de_DE' - German (Germany).
        DE_DE_UTF8: 'de_DE.utf8' - German (Germany), UTF-8 encoding.
    """

    C = "C"
    POSIX = "POSIX"
    EN_US = "en_US"
    EN_US_UTF8 = "en_US.utf8"
    ES_ES = "es_ES"
    ES_ES_UTF8 = "es_ES.utf8"
    DE_DE = "de_DE"
    DE_DE_UTF8 = "de_DE.utf8"

"""
Common enums.
"""

from spotlight.core.common.base_enum import BaseEnum


class Order(BaseEnum):
    ASC = "ASC"
    DESC = "DESC"


class ComparisonOperator(BaseEnum):
    NOT_IN = "NOT_IN"
    IN = "IN"
    NOT_EQUAL = "NOT_EQUAL"
    EQUAL = "EQUAL"
    LIKE = "LIKE"
    NOT_LIKE = "NOT_LIKE"
    GTE = "GTE"
    GT = "GT"
    LTE = "LTE"
    LT = "LT"


class LogicalOperator(BaseEnum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class SqlFunction(BaseEnum):
    SUM = "SUM"
    AVG = "AVG"
    ABS = "ABS"
    AND = "AND"
    COUNT = "COUNT"
    COUNT_DISTINCT = "COUNT_DISTINCT"
    MIN = "MIN"
    MAX = "MAX"
    MEDIAN = "MEDIAN"
    COALESCE = "COALESCE"


class FieldType(BaseEnum):
    BOOLEAN = "BOOLEAN"
    DOUBLE = "DOUBLE"
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    TIMESTAMP = "TIMESTAMP"
    DATETIME = "DATETIME"


class UpdateRequestAction(BaseEnum):
    UPDATE = "UPDATE"
    COPY = "COPY"


class RuleType(BaseEnum):
    SQL = "SQL"
    SPARK = "SPARK"
    WHERE_CLAUSE = "WHERE_CLAUSE"


class RuleSeverity(BaseEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class EventType(BaseEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class IntervalType(BaseEnum):
    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"


class NotificationType(BaseEnum):
    EMAIL = "EMAIL"


class Repository(BaseEnum):
    CME = "CME"
    DTCC = "DTCC"
    ICE = "ICE"


class AssetClass(BaseEnum):
    COMMODITY = "COMMODITY"
    CREDIT = "CREDIT"
    EQUITY = "EQUITY"
    FOREX = "FOREX"
    RATES = "RATES"

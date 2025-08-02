# canonmap/services/database/mysql/utils/mysql_data_types.py

from enum import Enum
from typing import Set

class MySQLDataType(str, Enum):
    # Numeric (exact value)
    TINYINT            = "TINYINT"
    SMALLINT           = "SMALLINT"
    MEDIUMINT          = "MEDIUMINT"
    INT                = "INT"
    INTEGER            = "INTEGER"
    BIGINT             = "BIGINT"
    DECIMAL            = "DECIMAL"
    NUMERIC            = "NUMERIC"
    FLOAT              = "FLOAT"
    DOUBLE             = "DOUBLE"
    REAL               = "REAL"
    BIT                = "BIT"
    BOOL               = "BOOL"
    BOOLEAN            = "BOOLEAN"
    SERIAL             = "SERIAL"

    # Date & Time
    DATE               = "DATE"
    DATETIME           = "DATETIME"
    TIMESTAMP          = "TIMESTAMP"
    TIME               = "TIME"
    YEAR               = "YEAR"

    # Character & Binary string
    CHAR               = "CHAR"
    VARCHAR            = "VARCHAR"
    BINARY             = "BINARY"
    VARBINARY          = "VARBINARY"
    TINYTEXT           = "TINYTEXT"
    TEXT               = "TEXT"
    MEDIUMTEXT         = "MEDIUMTEXT"
    LONGTEXT           = "LONGTEXT"
    TINYBLOB           = "TINYBLOB"
    BLOB               = "BLOB"
    MEDIUMBLOB         = "MEDIUMBLOB"
    LONGBLOB           = "LONGBLOB"
    ENUM               = "ENUM"
    SET                = "SET"

    # JSON
    JSON               = "JSON"

    # Spatial (GIS)
    GEOMETRY           = "GEOMETRY"
    POINT              = "POINT"
    LINESTRING         = "LINESTRING"
    POLYGON            = "POLYGON"
    MULTIPOINT         = "MULTIPOINT"
    MULTILINESTRING    = "MULTILINESTRING"
    MULTIPOLYGON       = "MULTIPOLYGON"
    GEOMETRYCOLLECTION = "GEOMETRYCOLLECTION"


    @classmethod
    def get_default_length(cls, data_type: str) -> str:
        """Return the default length/precision string for the type, or empty if not needed."""
        defaults = {
            cls.VARCHAR.value: "(255)",
            cls.CHAR.value: "(255)",
            cls.BINARY.value: "(255)",
            cls.VARBINARY.value: "(255)",
            cls.DECIMAL.value: "(10,2)",
            cls.NUMERIC.value: "(10,2)",
            cls.FLOAT.value: "(10,2)",
            cls.DOUBLE.value: "(10,2)",
            cls.BIT.value: "(1)"
        }
        return defaults.get(data_type, "")

    @classmethod
    def get_integer_types(cls) -> Set[str]:
        """Get all integer data types that support AUTO_INCREMENT."""
        return {
            cls.TINYINT.value,
            cls.SMALLINT.value,
            cls.MEDIUMINT.value,
            cls.INT.value,
            cls.INTEGER.value,
            cls.BIGINT.value,
            cls.SERIAL.value
        }
    
    @classmethod
    def get_length_required_types(cls) -> Set[str]:
        """Get data types that typically require length specification."""
        return {
            cls.CHAR.value,
            cls.VARCHAR.value,
            cls.BINARY.value,
            cls.VARBINARY.value,
            cls.DECIMAL.value,
            cls.NUMERIC.value,
            cls.FLOAT.value,
            cls.DOUBLE.value,
            cls.BIT.value
        }
    
    @classmethod
    def get_auto_increment_compatible(cls) -> Set[str]:
        """Get data types that support AUTO_INCREMENT."""
        return cls.get_integer_types()
    
    @classmethod
    def get_primary_key_compatible(cls) -> Set[str]:
        """Get data types that can be used as primary keys."""
        # Most types can be primary keys, but some are more suitable
        return {
            cls.TINYINT.value,
            cls.SMALLINT.value,
            cls.MEDIUMINT.value,
            cls.INT.value,
            cls.INTEGER.value,
            cls.BIGINT.value,
            cls.SERIAL.value,
            cls.CHAR.value,
            cls.VARCHAR.value,
            cls.BINARY.value,
            cls.VARBINARY.value,
            cls.DATE.value,
            cls.DATETIME.value,
            cls.TIMESTAMP.value,
            cls.TIME.value,
            cls.YEAR.value
        }
    
    @classmethod
    def needs_length_specification(cls, data_type: str) -> bool:
        """Check if a data type typically needs length specification."""
        return data_type in cls.get_length_required_types()
    
    @classmethod
    def supports_auto_increment(cls, data_type: str) -> bool:
        """Check if a data type supports AUTO_INCREMENT."""
        return data_type in cls.get_auto_increment_compatible()
    
    @classmethod
    def is_suitable_primary_key(cls, data_type: str) -> bool:
        """Check if a data type is suitable for primary key."""
        return data_type in cls.get_primary_key_compatible()


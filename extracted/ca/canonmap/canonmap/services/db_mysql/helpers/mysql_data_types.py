# canonmap/services/db_mysql/helpers/mysql_data_types.py

from enum import Enum

class MySQLType(str, Enum):
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


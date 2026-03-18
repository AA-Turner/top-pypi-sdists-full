#! /usr/bin/python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import datetime
import logging
import re
from typing import Optional, List, Any, Type, Dict
from sqlalchemy import Numeric, Integer, Float, String
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.type_api import TypeEngine

logger = logging.getLogger(__name__)


class TINYINT(Integer):  # pylint: disable=no-init
    __visit_name__ = "TINYINT"


class LARGEINT(Integer):  # pylint: disable=no-init
    __visit_name__ = "LARGEINT"


class DOUBLE(Float):  # pylint: disable=no-init
    __visit_name__ = "DOUBLE"


class HLL(Numeric):  # pylint: disable=no-init
    __visit_name__ = "HLL"


class BITMAP(Numeric):  # pylint: disable=no-init
    __visit_name__ = "BITMAP"


class QUANTILE_STATE(Numeric):  # pylint: disable=no-init
    __visit_name__ = "QUANTILE_STATE"

class AGG_STATE(Numeric):  # pylint: disable=no-init
    __visit_name__ = "AGG_STATE"

class ARRAY(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "ARRAY"

    @property
    def python_type(self) -> Optional[Type[List[Any]]]:
        return list


class MAP(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "MAP"

    @property
    def python_type(self) -> Optional[Type[Dict[Any, Any]]]:
        return dict


class STRUCT(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "STRUCT"

    @property
    def python_type(self) -> Optional[Type[Any]]:
        return None


class IPV4(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "IPV4"

    @property
    def python_type(self) -> Optional[Type[str]]:
        return str


class IPV6(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "IPV6"

    @property
    def python_type(self) -> Optional[Type[str]]:
        return str


class TIME(TypeEngine):  # pylint: disable=no-init
    """Doris TIME type — only appears in query results (e.g. TIMEDIFF, MAKETIME),
    cannot be used as a column storage type."""
    __visit_name__ = "TIME"

    @property
    def python_type(self) -> Optional[Type[datetime.timedelta]]:
        return datetime.timedelta


class VARIANT(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "VARIANT"

    @property
    def python_type(self) -> Optional[Type[Any]]:
        return dict


_type_map = {
    # === Boolean ===
    "boolean": sqltypes.BOOLEAN,
    # === Integer ===
    "tinyint": TINYINT,
    "smallint": sqltypes.SMALLINT,
    "int": sqltypes.INTEGER,
    "integer": sqltypes.INTEGER,
    "bigint": sqltypes.BIGINT,
    "largeint": LARGEINT,
    # === Floating-point ===
    "float": sqltypes.FLOAT,
    "double": DOUBLE,
    # === Fixed-precision ===
    # Doris 4.x reports DECIMALV3 as "decimal" in SHOW COLUMNS.
    # DECIMALV2 is deprecated; keep for backward-compat when reading old schemas.
    "decimal": sqltypes.DECIMAL,
    "decimalv2": sqltypes.DECIMAL,
    "decimalv3": sqltypes.DECIMAL,
    # === String ===
    "varchar": sqltypes.VARCHAR,
    "char": sqltypes.CHAR,
    "json": sqltypes.JSON,
    "jsonb": sqltypes.JSON,
    "text": sqltypes.TEXT,
    "string": sqltypes.String,
    # === Date and time ===
    # Doris normalises all date variants to "date"/"datetime" in SHOW COLUMNS.
    "date": sqltypes.DATE,
    "datev1": sqltypes.DATE,
    "datev2": sqltypes.DATE,
    "datetime": sqltypes.DATETIME,
    "datetimev1": sqltypes.DATETIME,
    "datetimev2": sqltypes.DATETIME,
    "time": TIME,
    # === Structural ===
    "array": ARRAY,
    "map": MAP,
    "struct": STRUCT,
    "hll": HLL,
    "quantile_state": QUANTILE_STATE,
    "bitmap": BITMAP,
    "agg_state": AGG_STATE,
    # === Network ===
    "ipv4": IPV4,
    "ipv6": IPV6,
    # === Semi-structured ===
    "variant": VARIANT,
}

# Types that accept (length) parameter
_types_with_length = {"varchar", "char", "string"}
# Types that accept (precision, scale) parameters
_types_with_precision = {"decimal", "decimalv2", "decimalv3"}


def parse_sqltype(type_str: str) -> TypeEngine:
    type_str = type_str.strip().lower()
    match = re.match(r"^(?P<type>\w+)\s*(?:\((?P<options>.*)\))?", type_str)
    if not match:
        logger.warning(f"Could not parse type name '{type_str}'")
        return sqltypes.NULLTYPE
    type_name = match.group("type")
    options = match.group("options")

    if type_name not in _type_map:
        logger.warning(f"Did not recognize type '{type_name}'")
        return sqltypes.NULLTYPE
    type_class = _type_map[type_name]

    if options:
        options = options.strip()
        if type_name in _types_with_precision:
            parts = [p.strip() for p in options.split(",")]
            precision = int(parts[0])
            scale = int(parts[1]) if len(parts) > 1 else 0
            return type_class(precision=precision, scale=scale)
        elif type_name in _types_with_length:
            try:
                return type_class(length=int(options))
            except (ValueError, TypeError):
                return type_class()

    return type_class()

#
# This software is part of the DenodoConnect component collection.
#
# Copyright (c) 2025 Denodo Technologies (https://www.denodo.com)
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from typing import Dict, Any, List, Literal

import pyarrow
import sqlalchemy
from adbc_driver_manager.dbapi import Connection as ADBCDBAPIConnection

MetaInfoDepth = Literal["all", "catalogs", "db_schemas", "tables", "columns"]

def get_schema_meta(connection: sqlalchemy.Connection, depth: MetaInfoDepth = "db_schemas") -> Dict[str, Any]:
    adbc_con = connection.connection.driver_connection
    if not isinstance(adbc_con, ADBCDBAPIConnection):
        raise RuntimeError(f"Driver connection is meant to be a DBAPI connection from the ADBC Flight SQL "
                           f"driver package, but it is a {type(adbc_con)} instead.")
    engine = connection.engine
    engine_url = engine.url if engine is not None else None
    engine_database = engine_url.database if engine_url is not None else None
    meta = adbc_con.adbc_get_objects(catalog_filter=engine_database, depth=depth)
    all_meta = meta.read_all().to_pylist()
    if len(all_meta) != 1:
        raise RuntimeError(f"Metadata call returned more than one catalog: {[c['catalog_name'] for c in all_meta]}")
    catalog_meta = all_meta[0]
    if "catalog_db_schemas" not in catalog_meta:
        raise RuntimeError(
            f"Metadata call returned a catalog without schema info: '{catalog_meta['catalog_name']}'")
    schemas_meta = catalog_meta["catalog_db_schemas"]
    if len(schemas_meta) != 1:
        raise RuntimeError(
            f"Metadata call returned more than one schema: {[s['db_schema_name'] for s in schemas_meta]}")
    return schemas_meta[0]


def get_tables_meta(connection: sqlalchemy.Connection, depth: MetaInfoDepth = "tables") -> List[Dict[str, Any]]:
    schema_meta = get_schema_meta(connection, depth=depth)
    if "db_schema_tables" not in schema_meta:
        raise RuntimeError(f"Metadata call returned a schema without table info: '{schema_meta['db_schema_name']}'")
    tables_meta = schema_meta["db_schema_tables"]
    return tables_meta


def get_table_schema(connection: sqlalchemy.Connection, table_name: str) -> pyarrow.Schema:
    adbc_con = connection.connection.driver_connection
    if not isinstance(adbc_con, ADBCDBAPIConnection):
        raise RuntimeError(f"Driver connection is meant to be a DBAPI connection from the ADBC Flight SQL "
                           f"driver package, but it is a {type(adbc_con)} instead.")
    engine = connection.engine
    engine_url = engine.url if engine is not None else None
    engine_database = engine_url.database if engine_url is not None else None
    schema = adbc_con.adbc_get_table_schema(catalog_filter=engine_database, table_name=table_name)
    if not schema or not isinstance(schema, pyarrow.Schema):
        raise RuntimeError(f"Could not retrieve a valid Arrow schema for table {table_name}.")
    return schema

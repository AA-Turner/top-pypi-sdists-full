# src/canonmap/connectors/mysql_connector/managers/database_manager/utils/generate_schema.py

import logging
import os
import pickle
import json
import random
from collections import defaultdict
from typing import List, Any, Dict, Optional

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.database_manager.validators.requests import GenerateSchemaRequest
from canonmap.exceptions import DatabaseManagerError

logger = logging.getLogger(__name__)

# MySQL datetime types that need format inference
DATETIME_TYPES = {"datetime", "timestamp", "date", "time", "year"}

def generate_schema_util(generate_schema_request: GenerateSchemaRequest, connector: MySQLConnector) -> str:
    """
    Generate a schema file containing table structure and sample data.
    
    Args:
        generate_schema_request: The request containing schema generation parameters
        connector: MySQL connector instance
        
    Returns:
        str: Path to the generated schema file
    """
    database_name = generate_schema_request.database.name
    schema_name = generate_schema_request.schema_name
    fields_to_include = generate_schema_request.fields_to_include
    fields_to_exclude = generate_schema_request.fields_to_exclude
    num_examples = generate_schema_request.num_examples
    include_helper_fields = generate_schema_request.include_helper_fields
    save_dir = generate_schema_request.save_dir
    save_json_version = generate_schema_request.save_json_version

    # Connect to the database
    connector.connect_to_database(database_name)
    
    schema = defaultdict(dict)
    conn = connector.pool.get_connection()
    
    try:
        with conn.cursor() as cursor:
            # Fetch table/column/type info
            cursor.execute(
                "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE "
                "FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA=%s",
                (database_name,)
            )
            columns = cursor.fetchall()
            logger.info(f"Found {len(columns)} total columns in database {database_name}")

        # Filter include/exclude sets
        include_set = set()
        if fields_to_include:
            for table_field in fields_to_include:
                include_set.add((table_field.table.name, table_field.name))

        exclude_set = set()
        if fields_to_exclude:
            for table_field in fields_to_exclude:
                exclude_set.add((table_field.table.name, table_field.name))

        filtered_columns = []
        for table, col, typ in columns:
            # Validate column data
            if not table or not col or not typ:
                logger.warning(f"Skipping invalid column data: table='{table}', col='{col}', typ='{typ}'")
                continue
                
            # Skip helper fields if not included
            if not include_helper_fields and col.startswith("__") and col.endswith("__"):
                continue

            # Apply include/exclude filters
            if fields_to_include:
                if (table, col) not in include_set:
                    continue
            elif fields_to_exclude:
                if (table, col) in exclude_set:
                    continue

            filtered_columns.append((table, col, typ))

        logger.debug(f"Filtered columns: {filtered_columns}")
        
        if not filtered_columns:
            logger.warning("No columns found to process for schema generation")
            # Return empty schema
            schema_dict = dict(schema)
            os.makedirs(save_dir, exist_ok=True)
            out_path = os.path.join(save_dir, f"{schema_name}.pkl")
            with open(out_path, "wb") as f:
                pickle.dump(schema_dict, f)
            logger.info(f"Empty schema pickle written to {out_path}")
            return out_path

        # Sample data for each field
        logger.info(f"Processing {len(filtered_columns)} columns for schema generation")
        with conn.cursor() as cursor:
            for table, col, typ in filtered_columns:
                logger.debug(f"Processing column: {table}.{col} (type: {typ})")
                logger.debug(f"col variable type: {type(col)}, value: '{col}'")
                logger.debug(f"table variable type: {type(table)}, value: '{table}'")
                
                # Additional safety check
                if not isinstance(col, str) or not isinstance(table, str):
                    logger.error(f"Invalid column or table name: col={col} (type: {type(col)}), table={table} (type: {type(table)})")
                    continue
                    
                samples: List[Any] = []

                # Stratified PK-range sampling: 3/4/3 from three equal buckets
                try:
                    cursor.execute(
                        "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_KEY='PRI'",
                        (database_name, table)
                    )
                    pk_info = cursor.fetchone()
                    if not pk_info or pk_info[1].upper() not in ("INT","BIGINT","SMALLINT","MEDIUMINT","TINYINT"):
                        raise ValueError("No suitable integer PK")

                    pk_col = pk_info[0]
                    cursor.execute(f"SELECT MIN(`{pk_col}`), MAX(`{pk_col}`) FROM `{table}`")
                    min_id, max_id = cursor.fetchone()
                    
                    if min_id is None or max_id is None:
                        raise ValueError("No data in table")

                    total = max_id - min_id + 1
                    size = total // 3
                    buckets = [
                        (min_id,           min_id + size - 1, 3),
                        (min_id + size,    min_id + 2*size - 1, 4),
                        (min_id + 2*size,  max_id,             3),
                    ]

                    for start, end, want in buckets:
                        got = []
                        trials = 0
                        while len(got) < want and trials < want * 10:
                            trials += 1
                            rand_id = random.randint(start, end)
                            query = f"SELECT `{col}` FROM `{table}` WHERE `{pk_col}` >= %s AND `{col}` IS NOT NULL LIMIT 1"
                            logger.debug(f"Executing query: {query}")
                            cursor.execute(query, (rand_id,))
                            row = cursor.fetchone()
                            if row and row[0] not in got:
                                got.append(row[0])
                        samples.extend(got)
                        logger.debug(
                            f"Bucket {start}–{end}: wanted {want}, got {len(got)} after {trials} trials"
                        )
                except Exception as e:
                    logger.debug(f"Stratified sampling failed for {table}.{col}: {e}")
                    # Fallback reservoir sampling on first 10000 distinct values
                    query = f"SELECT DISTINCT `{col}` FROM `{table}` WHERE `{col}` IS NOT NULL LIMIT 10000"
                    logger.debug(f"Executing fallback query: {query}")
                    cursor.execute(query)
                    reservoir: List[Any] = []
                    for idx, row in enumerate(cursor):
                        val = row[0]
                        if idx < num_examples:
                            reservoir.append(val)
                        else:
                            j = random.randint(0, idx)
                            if j < num_examples:
                                reservoir[j] = val
                    samples = reservoir
                    logger.debug(
                        f"Used fallback reservoir sampling for {table}.{col} ({len(samples)} samples)"
                    )

                # Assemble field info
                field_info: Dict[str, Any] = {
                    "data_type": typ,
                    "data": samples
                }
                if typ.lower() in DATETIME_TYPES:
                    field_info["datetime_format"] = infer_date_format(samples)

                schema[table][col] = field_info

    except Exception as e:
        raise DatabaseManagerError(f"Failed to generate schema: {e}")
    finally:
        conn.close()

    # Persist schema
    os.makedirs(save_dir, exist_ok=True)
    out_path = os.path.join(save_dir, f"{schema_name}.pkl")
    with open(out_path, "wb") as f:
        pickle.dump(dict(schema), f)
    logger.info(f"Schema pickle written to {out_path}")

    if save_json_version:
        json_dir = os.path.dirname(save_json_version)
        if json_dir:
            os.makedirs(json_dir, exist_ok=True)
        schema_dict = json.loads(json.dumps(dict(schema), default=str))
        with open(save_json_version, "w", encoding="utf-8") as jf:
            json.dump(schema_dict, jf, indent=2)
        logger.info(f"Schema JSON written to {save_json_version}")

    return out_path


def infer_date_format(samples: List[Any]) -> Optional[str]:
    """
    Infer the date format from sample data.
    
    Args:
        samples: List of sample date/time values
        
    Returns:
        Optional[str]: Inferred date format or None if cannot be determined
    """
    if not samples:
        return None
    
    # Simple format detection - this could be enhanced with more sophisticated logic
    sample_str = str(samples[0])
    
    # Common MySQL date formats
    if len(sample_str) == 10 and sample_str.count('-') == 2:
        return "%Y-%m-%d"  # DATE
    elif len(sample_str) == 19 and sample_str.count('-') == 2 and sample_str.count(':') == 2:
        return "%Y-%m-%d %H:%M:%S"  # DATETIME
    elif len(sample_str) == 8 and sample_str.count(':') == 2:
        return "%H:%M:%S"  # TIME
    elif len(sample_str) == 4 and sample_str.isdigit():
        return "%Y"  # YEAR
    
    return None 
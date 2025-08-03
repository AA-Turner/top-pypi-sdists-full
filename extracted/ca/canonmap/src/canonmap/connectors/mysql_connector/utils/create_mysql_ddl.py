# canonmap/services/database/mysql/utils/create_mysql_ddl.py

import re
from pathlib import Path
from decimal import Decimal
from typing import Union

import pandas as pd

from canonmap.connectors.mysql_connector.managers.database_manager.validators.responses import CreateDDLResponse
from canonmap.connectors.mysql_connector.managers.table_manager.utils._clean_field_names import clean_field_names

def create_mysql_ddl(table_name: str, data: Union[str, pd.DataFrame, list, Path], save_dir=None, primary_key_field: str = None):
    """
    Generate a MySQL CREATE TABLE DDL statement from various data sources.
    
    Parameters:
        table_name (str): Desired table name (will be cleaned for MySQL).
        data: Path to a CSV file, a file-like object, a pandas DataFrame, a list of dicts, or a JSON string representing records.
        save_dir (str or Path, optional): File path to save the DDL statement.
        primary_key_field (str, optional): Name of the field to use as primary key.
    
    Returns:
        str: The CREATE TABLE statement corresponding to the data's schema.
    """
    import json
    from pathlib import Path

    # Determine DataFrame source
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, str):
        # try JSON string first
        try:
            parsed = json.loads(data)
            if isinstance(parsed, list):
                df = pd.DataFrame(parsed)
            else:
                raise ValueError
        except Exception:
            # treat as CSV path
            df = pd.read_csv(
                data,
                dtype=str,
                keep_default_na=False,
                na_values=[],
                engine='python',
                on_bad_lines='skip'
            )
    elif hasattr(data, 'read'):
        df = pd.read_csv(
            data,
            dtype=str,
            keep_default_na=False,
            na_values=[],
            engine='python',
            on_bad_lines='skip'
        )
    else:
        raise ValueError("`data` must be a pandas DataFrame, list of dicts, JSON string, or path/buffer to a CSV file.")
    
    # Clean table name to be a valid MySQL identifier
    table = table_name.strip()
    table = re.sub(r'[^0-9A-Za-z_]', '_', table)            # replace invalid chars with _
    if table == '' or table.isdigit() or re.match(r'^\d', table):
        table = 'tbl_' + table                              # prefix if starts with digit or is empty
    table = table.lower()
    # Avoid reserved word conflict
    mysql_reserved = {
        "add","all","alter","analyze","and","as","asc","between","by","create","delete","desc","distinct",
        "drop","exists","from","group","having","in","index","insert","into","join","key","like","limit",
        "not","null","on","or","order","outer","select","set","table","update","union","where"
    }
    if table in mysql_reserved:
        table += "_tbl"
    if len(table) > 64:
        table = table[:64]
    
    # Clean column names using the helper function
    col_name_map = clean_field_names(df.columns.tolist())
    
    # Prepare a list for column definitions
    column_defs = []
    # Define placeholders that indicate missing data
    missing_values = {"", None, "NULL", "null", "NA", "na", "N/A", "n/a"}
    
    for col in df.columns:
        clean_name = col_name_map[col]
        values = df[col].tolist()
        # Filter out missing placeholders for type inference
        non_null_vals = [v for v in values if v not in missing_values]
        if not non_null_vals:
            # If column is entirely empty, default to TEXT (could also be VARCHAR(1) as minimal)
            col_type = "TEXT"
        else:
            # Check for booleans (true/false, yes/no, 0/1)
            val_set = {str(v).strip().lower() for v in non_null_vals}
            boolean_vals = {"true", "false", "t", "f", "yes", "no", "y", "n", "0", "1"}
            if val_set <= boolean_vals:
                col_type = "TINYINT(1)"  # MySQL boolean
            else:
                # Check if all values are numeric (int or float) or can be numeric
                all_numeric = True
                is_integer = True
                min_val = None
                max_val = None
                max_int_digits = 0
                max_frac_digits = 0
                for val in non_null_vals:
                    s = str(val).strip()
                    # General number (int/float) regex
                    if not re.fullmatch(r'-?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', s):
                        all_numeric = False
                        break
                    # If matches, determine if it has a fractional part or exponent
                    if re.fullmatch(r'-?\d+', s):
                        # pure integer string
                        n = int(s)
                        # track min/max for range
                        if min_val is None or n < min_val: 
                            min_val = n
                        if max_val is None or n > max_val: 
                            max_val = n
                        # count significant digits of integer
                        int_len = len(s.lstrip('-').lstrip('0')) or 1
                        if int_len > max_int_digits:
                            max_int_digits = int_len
                    else:
                        # number with decimal point or exponent
                        is_integer = False
                        try:
                            dec = Decimal(s)
                        except Exception:
                            dec = Decimal(str(float(s)))  # fallback to float if Decimal fails
                        # Convert to normalized string without scientific notation
                        dec_str = format(dec, 'f')
                        if dec_str.startswith('-'):
                            dec_str = dec_str[1:]
                        if '.' in dec_str:
                            int_part, frac_part = dec_str.split('.')
                        else:
                            int_part, frac_part = dec_str, ''
                        # Count digits in int and frac parts (ignore trailing zeros in fraction)
                        int_part = int_part.lstrip('0')
                        int_len = len(int_part) if int_part != '' else 0
                        frac_len = len(frac_part.rstrip('0'))
                        if int_len == 0 and frac_len == 0:
                            # value is 0.0 or 0.000... 
                            int_len = 1
                        if int_len > max_int_digits:
                            max_int_digits = int_len
                        if frac_len > max_frac_digits:
                            max_frac_digits = frac_len
                        # track min/max as floats (for range if needed)
                        try:
                            n = float(dec)
                        except Exception:
                            n = None
                        if n is not None:
                            if min_val is None or n < min_val:
                                min_val = n
                            if max_val is None or n > max_val:
                                max_val = n
                if all_numeric:
                    # If numeric, decide between int vs decimal
                    if is_integer:
                        # Choose appropriate integer type based on range
                        signed = True
                        if min_val is not None and min_val >= 0:
                            signed = False
                        if signed:
                            # use smallest signed type that fits min_val...max_val
                            if min_val is not None and max_val is not None:
                                if min_val >= -128 and max_val <= 127:
                                    col_type = "TINYINT"
                                elif min_val >= -32768 and max_val <= 32767:
                                    col_type = "SMALLINT"
                                elif min_val >= -8388608 and max_val <= 8388607:
                                    col_type = "MEDIUMINT"
                                elif min_val >= -2147483648 and max_val <= 2147483647:
                                    col_type = "INT"
                                elif min_val >= -9223372036854775808 and max_val <= 9223372036854775807:
                                    col_type = "BIGINT"
                                else:
                                    # If out of BIGINT range, use DECIMAL with all digits
                                    col_type = f"DECIMAL({max_int_digits},0)"
                            else:
                                col_type = "INT"
                        else:
                            # all values >= 0, use unsigned types
                            if max_val is not None:
                                if max_val <= 255:
                                    col_type = "TINYINT UNSIGNED"
                                elif max_val <= 65535:
                                    col_type = "SMALLINT UNSIGNED"
                                elif max_val <= 16777215:
                                    col_type = "MEDIUMINT UNSIGNED"
                                elif max_val <= 4294967295:
                                    col_type = "INT UNSIGNED"
                                elif max_val <= 18446744073709551615:
                                    col_type = "BIGINT UNSIGNED"
                                else:
                                    col_type = f"DECIMAL({max_int_digits},0)"
                            else:
                                col_type = "INT UNSIGNED"
                    else:
                        # Numeric column with a decimal part or very large/small values
                        if max_frac_digits == 0:
                            # (This case: all_numeric true, but is_integer false could happen if scientific notation of an int)
                            # Treat as integer range in such rare case
                            col_type = "INT"  # (fallback, though we could refine similar to above int logic)
                        else:
                            # Use DECIMAL for exact representation of floats
                            precision = max_int_digits + max_frac_digits
                            if precision > 65:
                                # Too many digits for DECIMAL, use floating type
                                col_type = "DOUBLE"
                            else:
                                scale = max_frac_digits
                                col_type = f"DECIMAL({precision},{scale})"
                else:
                    # Not all values are numeric – treat as text
                    max_len = max(len(str(v)) for v in non_null_vals)
                    if max_len <= 255:
                        col_type = f"VARCHAR({max_len})"
                    elif max_len <= 65535:
                        col_type = "TEXT"
                    elif max_len <= 16777215:
                        col_type = "MEDIUMTEXT"
                    else:
                        col_type = "LONGTEXT"
        # Append the column definition with primary key constraint if specified
        if primary_key_field and col == primary_key_field:
            column_defs.append(f"  `{clean_name}` {col_type} NOT NULL PRIMARY KEY")
        else:
            column_defs.append(f"  `{clean_name}` {col_type}")
    
    # Construct the CREATE TABLE statement
    ddl = "CREATE TABLE `{}` (\n".format(table)
    ddl += ",\n".join(column_defs)
    ddl += "\n) ROW_FORMAT=DYNAMIC;"
    
    # Save to file if requested
    if save_dir:
        with open(save_dir, 'w') as f:
            f.write(ddl)

    return CreateDDLResponse(ddl=ddl, ddl_path=save_dir)
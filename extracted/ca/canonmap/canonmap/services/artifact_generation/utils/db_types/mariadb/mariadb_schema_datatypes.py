import json
import re
import warnings
from typing import Any, Dict, Tuple, Optional

import pandas as pd

from canonmap.utils.logger import setup_logger
from canonmap.services.artifact_generation.utils.date_type_helpers import DATE_FORMATS, DOMINANCE_THRESHOLD

logger = setup_logger(__name__)

def pandas_dtype_to_mariadb(dtype: Any) -> str:
    """Map pandas dtype to MariaDB-compatible SQL type."""
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DOUBLE"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    elif pd.api.types.is_timedelta64_dtype(dtype):
        return "TIME"
    elif pd.api.types.is_categorical_dtype(dtype):
        return "VARCHAR(255)"
    elif pd.api.types.is_string_dtype(dtype):
        return "TEXT"
    return "TEXT"  # Fallback


class MariaDBSchemaInferrer:
    """
    Infers MariaDB database schemas from pandas DataFrames.
    Handles date/datetime detection and JSON field identification.
    """
    
    def _detect_datetime_type_and_format(
        self,
        series: pd.Series,
        threshold: float = 0.9
    ) -> Tuple[Optional[str], Optional[str]]:
        """Detect whether a column is DATE or DATETIME based on content + pattern matching."""
        all_strs = series.dropna().astype(str)
        total_non_null = len(all_strs)
        if total_non_null == 0:
            return None, None

        # Pre-filter: only attempt date parsing if the data actually looks like dates
        # Check if a reasonable percentage of values match common date patterns
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'^\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'^\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
            r'^\d{8}$',             # YYYYMMDD
            r'^\d{1,2}/\d{1,2}/\d{2,4}',  # M/D/YY or M/D/YYYY
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',  # ISO datetime
            r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',  # YYYY-MM-DD HH:MM:SS
        ]
        
        date_like_count = 0
        for pattern in date_patterns:
            date_like_count += sum(1 for s in all_strs if re.match(pattern, s))
        
        # If less than 50% of values look like dates, don't attempt parsing
        if date_like_count / total_non_null < 0.5:
            return None, None

        # Additional filter: avoid parsing strings that look like codes/identifiers
        # Check for patterns that are likely not dates (airport codes, zip codes, etc.)
        non_date_patterns = [
            r'^[A-Z]{3}$',  # 3-letter codes (airport codes, etc.)
            r'^[A-Z0-9]{3,6}$',  # Short alphanumeric codes
            r'^\d{5}$',  # 5-digit numbers (zip codes)
            r'^\d{3}-\d{2}-\d{4}$',  # SSN format
            r'^[A-Z0-9]{2,3}\s+[A-Z0-9]{2,4}$',  # Codes with spaces
        ]
        
        non_date_count = 0
        for pattern in non_date_patterns:
            non_date_count += sum(1 for s in all_strs if re.match(pattern, s))
        
        # If more than 30% of values look like non-date codes, don't attempt parsing
        if non_date_count / total_non_null > 0.3:
            return None, None

        # Specific check for problematic patterns that could be misinterpreted as timezones
        # These patterns often contain letters and numbers that pandas might interpret as timezone codes
        problematic_patterns = [
            r'^[A-Z0-9]{1,2}[A-Z]\s+[A-Z0-9]{1,2}[A-Z]{2,3}$',  # Like "T1H 7E8", "4A RHR"
            r'^[A-Z0-9]{1,2}\s+[A-Z]{3}$',  # Like "4A LHR"
            r'^[A-Z0-9]{1,2}[A-Z]{2,3}$',  # Short alphanumeric codes ending in letters
        ]
        
        problematic_count = 0
        for pattern in problematic_patterns:
            problematic_count += sum(1 for s in all_strs if re.match(pattern, s))
        
        # If any problematic patterns are found, don't attempt parsing
        if problematic_count > 0:
            return None, None

        best_fmt: Optional[str] = None
        best_rate: float = 0.0

        # Step 1: find the format that yields the highest parse rate
        for fmt in DATE_FORMATS:
            try:
                parsed = pd.to_datetime(all_strs, format=fmt, errors="coerce")
                rate = parsed.notnull().mean()
                if rate > best_rate:
                    best_rate = rate
                    best_fmt = fmt
            except Exception:
                continue

        # Prepare a deduplicated, string-cast series for the actual parse
        unique = series.drop_duplicates().reset_index(drop=True)
        unique_str = unique.astype(str)

        # Step 2: attempt formatted parse if a good candidate exists
        if best_fmt and best_rate >= 0.5:
            try:
                dt_series = pd.to_datetime(unique_str, format=best_fmt, errors="coerce")
            except Exception:
                # fallback to generic parse
                best_fmt = None
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    warnings.simplefilter("ignore", FutureWarning)
                    try:
                        dt_series = pd.to_datetime(unique_str, errors="coerce")
                    except Exception:
                        return None, None
        else:
            # no reliable format found—do a generic parse
            best_fmt = None
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                warnings.simplefilter("ignore", FutureWarning)
                try:
                    # Only attempt generic parsing if we have a reasonable number of date-like strings
                    # and we've already passed our pre-filters
                    dt_series = pd.to_datetime(unique_str, errors="coerce")
                except Exception:
                    return None, None

        # Step 3: ensure overall parse rate meets threshold
        valid_rate = dt_series.notnull().mean()
        if valid_rate < threshold:
            return None, None

        # Step 4: if we still have no explicit format, infer a common one
        if best_fmt is None:
            if all(re.match(r"^\d{4}-\d{2}-\d{2}$", s) for s in all_strs):
                best_fmt = "%Y-%m-%d"
            elif all(re.match(r"^\d{2}/\d{2}/\d{4}$", s) for s in all_strs):
                best_fmt = "%m/%d/%Y"
            elif all(re.match(r"^\d{8}$", s) for s in all_strs):
                best_fmt = "%Y%m%d"

        # Step 5: decide DATE vs DATETIME
        non_null = dt_series.dropna()
        if (
            (non_null.dt.hour == 0).all() and
            (non_null.dt.minute == 0).all() and
            (non_null.dt.second == 0).all()
        ):
            return "DATE", best_fmt
        else:
            return "DATETIME", best_fmt

    def infer_mariadb_schema(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Infers a MariaDB schema from a DataFrame.
        Returns dict mapping each column name to:
        {
            "data_type": ...,
            "date_format_in_database": ... (optional)
        }
        """
        schema: Dict[str, Dict[str, Any]] = {}

        for col in df.columns:
            entry: Dict[str, Any] = {"data_type": None}
            series = df[col]

            if pd.api.types.is_integer_dtype(series):
                entry["data_type"] = "INT"
            elif pd.api.types.is_float_dtype(series):
                entry["data_type"] = "DOUBLE"
            elif pd.api.types.is_bool_dtype(series):
                entry["data_type"] = "BOOLEAN"
            elif pd.api.types.is_datetime64_any_dtype(series):
                entry["data_type"] = "DATETIME"
                entry["date_format_in_database"] = None
            else:
                detected_type, detected_fmt = self._detect_datetime_type_and_format(series)
                if detected_type:
                    entry["data_type"] = detected_type
                    entry["date_format_in_database"] = detected_fmt
                else:
                    entry["data_type"] = "TEXT"
                    sample_vals = series.dropna().astype(str).head(50)
                    cnt = sum(1 for v in sample_vals if _is_json_like(v))
                    if sample_vals.size and (cnt / sample_vals.size) >= DOMINANCE_THRESHOLD:
                        entry["data_type"] = "JSON"

            schema[col] = entry

        return schema


def _is_json_like(val: str) -> bool:
    try:
        json.loads(val)
        return True
    except Exception:
        return False
"""
File processing functionality for storage inventory files.
"""

from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import pyarrow as pa
import pyarrow.compute as pc

from .constants import StorageInventoryConstants
from .utils import Utils


class InventoryFileProcessor:
    """Processes file metadata from storage inventory files"""

    def __init__(self, logger):
        self.logger = logger
        self.parse_success = False

    def extract_file_info(self, key: str) -> Tuple[str, Optional[str], Optional[str]]:
        """Extract prefix, file type, and compression from a key"""
        parts = key.split("/", 1)
        if len(parts) == 1:
            prefix = ""
            filename = parts[0]
        else:
            prefix = parts[0]
            filename = parts[1].rsplit("/", 1)[-1]

        if "." in filename:
            exts = filename.lower().split(".")
            compression = None
            file_type = None

            for i in range(len(exts) - 1, 0, -1):
                if exts[i] in StorageInventoryConstants.COMPRESSION_EXTS:
                    compression = (
                        exts[i] if compression is None else f"{exts[i]}.{compression}"
                    )
                else:
                    file_type = exts[i]
                    break

            if file_type is None:
                file_type = "ambiguous_file_type"
        else:
            file_type = "ambiguous_file_type"
            compression = None

        return prefix, file_type, compression

    def enrich_metadata_table(self, arrow_table: pa.Table) -> pa.Table:
        """Add derived columns to the Arrow table"""
        # Extract file info columns
        arr = arrow_table["Key"]
        meta_cols = [[], [], []]

        for k in arr:
            p, ft, ct = self.extract_file_info(k.as_py())
            meta_cols[0].append(p)
            meta_cols[1].append(ft)
            meta_cols[2].append(ct)

        arrow_table = arrow_table.append_column("prefix", pa.array(meta_cols[0]))
        arrow_table = arrow_table.append_column("file_type", pa.array(meta_cols[1]))
        arrow_table = arrow_table.append_column(
            "compression_type", pa.array(meta_cols[2])
        )

        # Preserve original LastModifiedDate strings for fallback
        arrow_table = arrow_table.append_column(
            "LastModifiedDate_str", arrow_table["LastModifiedDate"]
        )

        # Try to parse LastModifiedDate robustly
        try:
            # Convert ISO format strings to datetime objects first

            # For parquet files "LastModifiedDate_str" is a datetime object already, so we don't need to parse it
            dates = arrow_table["LastModifiedDate_str"].to_pylist()
            if isinstance(dates[0], datetime):
                timestamps = dates
            else:
                timestamps = [
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    for ts in arrow_table["LastModifiedDate_str"].to_pylist()
                ]
            parsed = pa.array(timestamps, type=pa.timestamp("s"), safe=False)

            # Store parsed timestamps in new column
            arrow_table = arrow_table.set_column(
                arrow_table.schema.get_field_index("LastModifiedDate"),
                "LastModifiedDate_parsed",
                parsed,
            )

            self.parse_success = parsed.null_count < len(parsed)
        except Exception as e:
            self.logger.error(f"Error parsing LastModifiedDate: {e}")
            self.parse_success = False

        return arrow_table

    def create_prefix_summary(
        self, arrow_table: pa.Table, prefix: str
    ) -> Dict[str, Any]:
        """Create a summary for a specific prefix"""
        mask = pc.equal(arrow_table["prefix"], pa.scalar(prefix))  # type: ignore
        group = arrow_table.filter(mask)

        # Debug logging
        self.logger.info(f"[DEBUG] Prefix: {prefix} | Group rows: {group.num_rows}")
        lm_samples = [x.as_py() for x in group["LastModifiedDate_str"][:10]]
        self.logger.info(f"[DEBUG] Sample LastModifiedDate values: {lm_samples}")

        # Extract file stats
        sizes = group["Size"]
        file_types = set(x.as_py() for x in group["file_type"] if x.as_py())
        compressions = set(x.as_py() for x in group["compression_type"] if x.as_py())

        # Clean up file types (exclude compression types)
        file_types = sorted(
            [
                ft
                for ft in file_types
                if ft not in StorageInventoryConstants.COMPRESSION_EXTS
            ]
        )
        compressions = sorted([ct for ct in compressions if ct])

        # Handle timestamps
        parsed_col = group["LastModifiedDate_parsed"] if self.parse_success else None

        if (
            self.parse_success
            and parsed_col is not None
            and parsed_col.null_count < group.num_rows
        ):
            first_modified = str(pc.min(parsed_col).as_py())  # type: ignore
            last_modified = str(pc.max(parsed_col).as_py())  # type: ignore
        else:
            # Fallback: string min/max from original values
            lm_col_str = group["LastModifiedDate_str"]
            lm_strs = [x.as_py() for x in lm_col_str if x.as_py()]
            first_modified = min(lm_strs) if lm_strs else None
            last_modified = max(lm_strs) if lm_strs else None

        # Format timestamps
        first_modified_fmt = Utils.format_timestamp(first_modified)
        last_modified_fmt = Utils.format_timestamp(last_modified)

        # Create summary statistics
        stats = {
            "file_count": group.num_rows,
            "total_size_bytes": int(pc.sum(sizes).as_py()) if group.num_rows else 0,  # type: ignore
            "avg_file_size_bytes": (
                float(pc.mean(sizes).as_py()) if group.num_rows else None  # type: ignore
            ),
            "file_size_min": int(pc.min(sizes).as_py()) if group.num_rows else None,  # type: ignore
            "file_size_max": int(pc.max(sizes).as_py()) if group.num_rows else None,  # type: ignore
            "file_size_stddev": (
                float(pc.stddev(sizes).as_py()) if group.num_rows > 1 else None  # type: ignore
            ),
            "first_modified": first_modified_fmt,
            "last_modified": last_modified_fmt,
            "file_types": file_types if file_types else ["ambiguous_file_type"],
            "compression_types": compressions,
        }

        return stats

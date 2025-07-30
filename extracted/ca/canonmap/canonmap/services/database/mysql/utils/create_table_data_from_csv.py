from pathlib import Path
import csv
import json
from typing import Union, Optional, List, Dict, Any

import chardet

def _get_csv_encoding(file_path: Path) -> str:
    """
    Detects and returns the most likely encoding for a CSV file.
    Uses common encodings first, falls back to chardet for detection.
    """
    common_encodings = [
        "utf-8",
        "utf-8-sig",
        "latin-1",
        "ISO-8859-1",
        "windows-1252",
    ]
    
    # First, test common encodings by trying to open the file
    for enc in common_encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                f.read(4096)  # read a chunk to test decoding
            return enc
        except UnicodeDecodeError:
            continue  # try next encoding
    
    # If none of the common encodings work, use chardet
    with open(file_path, "rb") as f:
        raw_data = f.read()
        detection = chardet.detect(raw_data)
        detected_encoding = detection.get("encoding", "utf-8")  # fallback to utf-8 if chardet fails
    
    return detected_encoding



def create_table_data_from_csv(
    csv_path: Union[str, Path],
    encoding: Optional[str] = None,
    as_json: bool = False
) -> Union[List[Dict[str, Any]], str]:
    """
    Read a CSV file and return its contents as a List[dict],  
    converting empty strings and 'nan' (case-insensitive) to None.  
    If as_json=True, return a JSON string instead.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    enc = encoding or _get_csv_encoding(path)
    with path.open(encoding=enc, newline="") as f:
        reader = csv.DictReader(f)
        rows: List[Dict[str, Any]] = []
        for raw_row in reader:
            row: Dict[str, Any] = {}
            for col, val in raw_row.items():
                # skip any unexpected extra columns
                if col is None:
                    continue
                # normalize missing/empty/nan
                if val is None:
                    row[col] = None
                elif isinstance(val, str):
                    v = val.strip()
                    if v == "" or v.lower() == "nan":
                        row[col] = None
                    else:
                        row[col] = v
                else:
                    # non-str values (e.g., lists) - leave as is
                    row[col] = val
            rows.append(row)

    return json.dumps(rows) if as_json else rows
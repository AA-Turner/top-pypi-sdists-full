from typing import Optional

import pandas as pd
import chardet

from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)

def convert_csv_to_df(
        csv_path: str,
        num_rows: Optional[int] = None
) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame with automatic encoding detection.
    
    Args:
        csv_path: Path to the CSV file
        num_rows: Maximum number of rows to load
        
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    logger.info(f"Generating artifacts from CSV: {csv_path}")
    df = _load_csv(csv_path)
    if num_rows:
        logger.info(f"Using first {num_rows} rows")
        df = df.head(num_rows)
    return df

def _load_csv(csv_path: str) -> pd.DataFrame:
    """
    Load CSV file with automatic encoding detection.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded DataFrame
        
    Raises:
        UnicodeDecodeError: If no encoding can be detected
    """
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1']
    for enc in encodings:
        try:
            return pd.read_csv(csv_path, low_memory=False, encoding=enc)
        except UnicodeDecodeError:
            continue
    # fallback to chardet
    with open(csv_path, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data).get('encoding')
        if detected:
            return pd.read_csv(csv_path, low_memory=False, encoding=detected)
    raise UnicodeDecodeError("utf-8", b'', 0, 1, "Could not decode CSV file")
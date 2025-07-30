import chardet
from pathlib import Path

def get_csv_encoding(file_path: Path) -> str:
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
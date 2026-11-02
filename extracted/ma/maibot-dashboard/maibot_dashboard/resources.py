from pathlib import Path

def get_dist_path() -> Path:
    return Path(__file__).parent / "dist"

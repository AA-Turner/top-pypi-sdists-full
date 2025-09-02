from pathlib import Path
from .paths import *
def sanitize_rel_path(rel_path: str) -> list[str]:
    """
    Split a *user-supplied* relative path into parts and
    sanitise each segment with Werkzeug’s secure_filename.

    >>> sanitize_rel_path('foo/../bar/baz.txt')
    ['bar', 'baz.txt']
    """
    # Path(rel_path).parts gives you ('foo', '..', 'bar', 'baz.txt') on *all* OSes
    return [secure_filename(p)                    # strip dangerous chars
            for p in Path(rel_path).parts
            if p not in (".", "..", "", "/", "\\")]


def make_full_upload_path(root: str | Path, rel_path: str) -> Path:
    """
    Return the absolute path you will write the file to and create
    any missing parent directories in the process.
    """
    root = Path(root).expanduser().resolve()
    parts = sanitize_rel_path(rel_path)

    # Build the final path safely
    full_path: Path = root.joinpath(*parts)

    # Ensure we never escape the upload root (path traversal defence)
    if root not in full_path.parents:
        raise ValueError("Attempted path traversal outside upload directory")

    # Make parent directories (mkdir -p equivalent, cross-platform)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path


def split_rel_path(rel_path: str) -> tuple[str, str]:
    """
    'foo/bar.txt' → ('foo', 'bar.txt'), OS-agnostic.
    """
    p = Path(rel_path)
    return (str(p.parent) if p.parent != Path() else ""), p.name


def get_path_and_filename(filepath: str) -> tuple[Path, str]:
    """
    Convert a *relative* path stored in your DB into:
        absolute_path, filename_without_extension
    """
    abs_path = Path(ABS_UPLOAD_DIR, filepath).resolve()
    filename_no_ext = abs_path.stem
    return abs_path, filename_no_ext


def get_search_map(data: dict | None = None) -> tuple[dict, int, bool]:
    """
    Build a DB-friendly search dict from request JSON.
    Works unchanged on Windows, macOS, Linux.
    """
    if not data:
        return {"error": "No data provided"}, 400, False

    search_map: dict[str, str | int] = {}
    filepath = (data.get("filepath") or data.get("rel_path") or
                data.get("relpath") or data.get("relPath"))
    file_id = data.get("id") or data.get("file_id")

    if filepath:
        search_map["filepath"] = filepath

    if file_id and str(file_id).isdigit():
        search_map["id"] = int(file_id)

    if not search_map:
        return {"value": search_map,
                "message": "Missing file path or ID",
                "status_code": 400,
                "success": False}

    return search_map, 200, True

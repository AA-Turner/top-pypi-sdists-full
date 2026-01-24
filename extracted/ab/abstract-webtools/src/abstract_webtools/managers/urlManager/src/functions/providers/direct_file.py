import os
import mimetypes

DIRECT_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".mp4", ".mov", ".mkv", ".avi",
    ".mp3", ".wav", ".ogg",
    ".pdf", ".zip", ".rar", ".7z", ".gz",
}

def detect_direct_file(parsed):
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext in DIRECT_EXTS:
        return {
            "downloadable": True,
            "kind": mimetypes.guess_type(parsed.path)[0] or "file",
            "provider": None,
            "id": None,
            "direct": True,
        }
    return None

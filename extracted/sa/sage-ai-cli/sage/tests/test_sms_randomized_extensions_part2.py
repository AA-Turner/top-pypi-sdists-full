import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

RAND_IMAGES = ["png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "gif", "animated_gif", "svg", "ico", "psd", "ai", "eps", "raw", "dng"]
@pytest.mark.parametrize("ext", RAND_IMAGES)
def test_sms_bridge_file_generation_images(ext, tmp_path):
    """Verify image file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

RAND_OTHER = [
    "ttf", "otf", "woff", "woff2", "eot", "db", "sqlite", "sqlite3", "sqlitedb", "mdb", "accdb",
    "pem", "crt", "key", "pub", "asc", "gpg", "der", "pfx", "p12", "fbx", "obj", "gltf", "glb",
    "blend", "unity", "tscn", "dae", "stl", "ply", "bin", "exe", "dll", "so", "dylib", "class",
    "o", "a", "app", "apk", "ipa"
]
@pytest.mark.parametrize("ext", RAND_OTHER)
def test_sms_bridge_file_generation_other(ext, tmp_path):
    """Verify miscellaneous file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

RAND_TEXT = [
    "txt", "csv", "json", "xml", "html", "css", "md", "yaml", "yml", "ini", "conf", "sql",
    "toml", "properties", "log", "bak", "tmp", "temp", "rtf", "ascii"
]
@pytest.mark.parametrize("ext", RAND_TEXT)
def test_sms_bridge_file_generation_text(ext, tmp_path):
    """Verify text file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

RAND_VIDEO = ["mp4", "webm", "mkv", "avi", "mov", "wmv", "flv", "m4v", "3gp"]
@pytest.mark.parametrize("ext", RAND_VIDEO)
def test_sms_bridge_file_generation_video(ext, tmp_path):
    """Verify video file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

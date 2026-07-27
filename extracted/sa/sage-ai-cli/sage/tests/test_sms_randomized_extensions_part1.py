import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


RAND_ARCHIVES = ["zip", "tar", "gz", "rar", "7z", "tgz", "bz2", "xz", "dmg", "pkg", "iso", "img", "cab"]
@pytest.mark.parametrize("ext", RAND_ARCHIVES)
def test_sms_bridge_file_generation_archives(ext, tmp_path):
    """Verify archive file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

RAND_AUDIO = ["wav", "mp3", "ogg", "flac", "m4a", "opus", "aac", "wma", "mid", "midi", "amr", "aiff"]
@pytest.mark.parametrize("ext", RAND_AUDIO)
def test_sms_bridge_file_generation_audio(ext, tmp_path):
    """Verify audio file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

RAND_CODE = [
    "py", "c", "cpp", "h", "hpp", "java", "kt", "swift", "go", "rs", "sh", "bat", "ps1",
    "gd", "cs", "php", "rb", "pl", "pyw", "m", "scala", "dart", "tsx", "jsx", "lua", "r",
    "hs", "erl", "ex", "exs", "js", "ts"
]
@pytest.mark.parametrize("ext", RAND_CODE)
def test_sms_bridge_file_generation_code(ext, tmp_path):
    """Verify code file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

RAND_DOCS = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "pages", "numbers", "key"]
@pytest.mark.parametrize("ext", RAND_DOCS)
def test_sms_bridge_file_generation_docs(ext, tmp_path):
    """Verify document file extensions via SMS."""
    verify_sms_with_rubric(f"Create a file with extension {ext}", tmp_path)

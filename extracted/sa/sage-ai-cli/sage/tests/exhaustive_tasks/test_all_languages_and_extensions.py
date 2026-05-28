import pytest
from sage.tests.rubric_checker import (
    verify_cli_with_rubric,
    verify_sms_with_rubric,
    verify_website_with_rubric
)

EXTENSIONS = [
    "py", "js", "ts", "jsx", "tsx", "c", "h", "cpp", "hpp", "java", "kt", "scala",
    "swift", "go", "rs", "cs", "php", "rb", "pl", "sh", "bat", "ps1", "gd", "dart",
    "lua", "r", "hs", "erl", "ex", "exs", "hrl", "fs", "fsi", "cr", "groovy", "gvy",
    "sql", "sol", "zig", "nim", "d", "pas", "elm", "vue", "svelte", "xml", "tex",
    "toml", "ini", "csv", "dockerfile"
]

@pytest.mark.parametrize("ext", EXTENSIONS)
def test_cli_all_extensions(ext):
    """Verify code generation and rubric validation for all extensions via CLI."""
    prompt = f"Create a complete task file for {ext} extension."
    verify_cli_with_rubric(prompt)

@pytest.mark.parametrize("ext", EXTENSIONS)
def test_sms_all_extensions(ext, tmp_path):
    """Verify code generation and rubric validation for all extensions via SMS."""
    prompt = f"Create a complete task file for {ext} extension."
    verify_sms_with_rubric(prompt, tmp_path)

@pytest.mark.parametrize("ext", EXTENSIONS)
def test_website_all_extensions(ext):
    """Verify code generation and rubric validation for all extensions via Website API."""
    prompt = f"Create a complete task file for {ext} extension."
    verify_website_with_rubric(prompt)

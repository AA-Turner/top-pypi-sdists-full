"""Unit tests for flowtask.parsers.syntax.detector."""
from pathlib import Path

import pytest

from flowtask.parsers.syntax.detector import detect_format, sniff_format


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("task.json", "json"),
        ("task.yaml", "yaml"),
        ("task.yml", "yaml"),
        ("task.toml", "toml"),
        ("TASK.JSON", "json"),
        ("TASK.YAML", "yaml"),
        ("TASK.TOML", "toml"),
    ],
)
def test_detect_format_by_suffix(filename, expected):
    """detect_format returns the correct format for each supported suffix."""
    assert detect_format(Path(filename)) == expected


def test_detect_format_unknown_suffix_raises():
    """detect_format raises ValueError for unsupported extensions."""
    with pytest.raises(ValueError, match="Unsupported task file suffix"):
        detect_format(Path("task.txt"))


def test_detect_format_no_suffix_raises():
    """detect_format raises ValueError when no extension is present."""
    with pytest.raises(ValueError, match="Unsupported task file suffix"):
        detect_format(Path("taskfile"))


def test_sniff_format_json():
    """sniff_format identifies valid JSON content."""
    assert sniff_format('{"name": "demo", "steps": []}') == "json"


def test_sniff_format_yaml():
    """sniff_format identifies YAML content (not parseable as JSON)."""
    assert sniff_format("name: demo\nsteps: []\n") == "yaml"


def test_sniff_format_toml():
    """sniff_format identifies TOML content."""
    assert sniff_format('name = "demo"\n[[steps]]\n') == "toml"


def test_sniff_format_ambiguous_prefers_json():
    """A doc that is both valid JSON and valid YAML must classify as JSON."""
    # JSON is tried first; this is intentional per the spec.
    assert sniff_format('{"name": "demo", "steps": []}') == "json"


def test_sniff_format_garbage_raises():
    """sniff_format raises ValueError for content that is not valid in any format.

    Note: yaml.safe_load is extremely permissive and parses most strings as
    scalars or simple dicts. sniff_format requires a dict result from YAML
    (task definitions are always objects), so scalar YAML results fall through.
    TOML and JSON are also strict enough to reject non-conformant content.
    """
    # This string is not valid JSON, not a YAML dict, and not valid TOML.
    # yaml.safe_load returns a plain string scalar (not a dict), so it falls through.
    with pytest.raises(ValueError, match="does not parse"):
        sniff_format("this is just a plain string value with no structure")

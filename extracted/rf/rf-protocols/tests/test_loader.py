"""Tests for the .sub file loader."""

import asyncio
from pathlib import Path

import pytest

import rf_protocols
from rf_protocols import ModulationType
from rf_protocols.commands.ook import OOKCommand
from rf_protocols.loader import CodeCollection, get_codes

_BUNDLED_CODES_ROOT = Path(rf_protocols.__file__).parent / "codes"
_BUNDLED_SUB_FILES = sorted(_BUNDLED_CODES_ROOT.rglob("*.sub"))
_HONEYWELL_ROOT = _BUNDLED_CODES_ROOT / "honeywell"


def test_bundled_sub_files_exist() -> None:
    """At least one bundled .sub file ships with the package."""
    assert _BUNDLED_SUB_FILES, f"No .sub files found under {_BUNDLED_CODES_ROOT}"


@pytest.mark.parametrize(
    "sub_file",
    _BUNDLED_SUB_FILES,
    ids=[str(p.relative_to(_BUNDLED_CODES_ROOT)) for p in _BUNDLED_SUB_FILES],
)
def test_bundled_sub_file_parses(sub_file: Path) -> None:
    """Every bundled .sub file parses into a valid OOK command."""
    device_dir = sub_file.parent.relative_to(_BUNDLED_CODES_ROOT)
    codes = get_codes(str(device_dir))
    cmd = codes.load_command(sub_file.stem.upper())
    assert isinstance(cmd, OOKCommand)
    assert cmd.frequency > 0
    assert cmd.modulation == ModulationType.OOK
    assert cmd.timings
    assert len(cmd.timings) % 2 == 0


def test_get_codes_bundled_honeywell() -> None:
    """Bundled Honeywell string lights codes can be discovered and loaded."""
    codes = get_codes("honeywell/string_lights")
    assert isinstance(codes, CodeCollection)
    cmd = codes.load_command("TURN_ON")
    assert isinstance(cmd, OOKCommand)
    assert cmd.frequency == 433_920_000
    assert cmd.repeat_count == 50
    assert cmd.timings[:2] == [2000, -550]


def test_load_command_caches_results() -> None:
    """Repeated load_command calls return the same instance."""
    codes = get_codes("honeywell/string_lights")
    assert codes.load_command("TURN_ON") is codes.load_command("TURN_ON")


def test_load_command_unknown_name() -> None:
    """Requesting an unknown command name raises KeyError."""
    codes = get_codes("honeywell/string_lights")
    with pytest.raises(KeyError, match="NOPE"):
        codes.load_command("NOPE")


def test_load_command_base_dir_override() -> None:
    """Passing base_dir loads codes from an alternate location."""
    codes = get_codes("string_lights", base_dir=_HONEYWELL_ROOT)
    cmd = codes.load_command("TURN_ON")
    assert isinstance(cmd, OOKCommand)
    assert cmd.frequency == 433_920_000
    assert cmd.repeat_count == 50


def test_load_command_base_dir_accepts_str() -> None:
    """base_dir accepts a str as well as a Path."""
    codes = get_codes("string_lights", base_dir=str(_HONEYWELL_ROOT))
    assert isinstance(codes.load_command("TURN_ON"), OOKCommand)


def test_get_codes_missing_directory(tmp_path: Path) -> None:
    """get_codes raises FileNotFoundError when the directory is missing."""
    with pytest.raises(FileNotFoundError):
        get_codes("nope", base_dir=tmp_path)


def test_get_codes_rejects_path_escape() -> None:
    """Paths that resolve outside of base_dir are rejected."""
    with pytest.raises(ValueError, match="outside"):
        get_codes("../honeywell", base_dir=_HONEYWELL_ROOT / "string_lights")


async def test_async_load_command_loads_from_disk() -> None:
    """async_load_command parses the command from disk."""
    codes = get_codes("honeywell/string_lights")
    cmd = await codes.async_load_command("TURN_ON")
    assert isinstance(cmd, OOKCommand)
    assert cmd.repeat_count == 50


async def test_async_load_command_returns_cached_without_executor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cached commands bypass the executor entirely."""
    codes = get_codes("honeywell/string_lights")
    first = codes.load_command("TURN_ON")

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("executor must not be used for cached commands")

    monkeypatch.setattr(
        asyncio.AbstractEventLoop, "run_in_executor", _boom, raising=True
    )
    second = await codes.async_load_command("TURN_ON")
    assert first is second

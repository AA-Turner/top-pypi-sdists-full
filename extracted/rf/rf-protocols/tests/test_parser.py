"""Tests for :func:`parse_sub_content`."""

import pytest

from rf_protocols.commands.ook import OOKCommand
from rf_protocols.parser import parse_sub_content

_SAMPLE_SUB = """\
Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
Repeat: 7
RAW_Data: 2000 -550 450 -1000
"""


def test_parse_sub_content_parses_sample() -> None:
    """A well-formed .sub payload parses into an OOKCommand."""
    cmd = parse_sub_content(_SAMPLE_SUB)
    assert isinstance(cmd, OOKCommand)
    assert cmd.frequency == 433_920_000
    assert cmd.repeat_count == 7
    assert cmd.timings == [2000, -550, 450, -1000]


def test_parse_sub_content_rejects_non_raw_protocol() -> None:
    """Non-RAW protocols are rejected."""
    with pytest.raises(ValueError, match="Protocol"):
        parse_sub_content(_SAMPLE_SUB.replace("Protocol: RAW", "Protocol: Princeton"))


def test_parse_sub_content_rejects_non_ook_preset() -> None:
    """Non-OOK presets are rejected."""
    with pytest.raises(ValueError, match="Preset"):
        parse_sub_content(
            _SAMPLE_SUB.replace(
                "FuriHalSubGhzPresetOok650Async", "FuriHalSubGhzPreset2FSKDev238Async"
            )
        )


def test_parse_sub_content_multiline_raw_data() -> None:
    """Multiple RAW_Data lines are concatenated."""
    content = (
        "Filetype: Flipper SubGhz RAW File\n"
        "Version: 1\n"
        "Frequency: 433920000\n"
        "Preset: FuriHalSubGhzPresetOok650Async\n"
        "Protocol: RAW\n"
        "RAW_Data: 2000 -550\n"
        "RAW_Data: 450 -1000\n"
    )
    cmd = parse_sub_content(content)
    assert isinstance(cmd, OOKCommand)
    assert cmd.timings == [2000, -550, 450, -1000]
    assert cmd.repeat_count == 0


def test_parse_sub_content_rejects_odd_raw_data() -> None:
    """Odd-length RAW_Data is rejected."""
    with pytest.raises(ValueError, match="even number"):
        parse_sub_content(_SAMPLE_SUB.replace("2000 -550 450 -1000", "2000 -550 450"))

from pathlib import Path

from la_panic.panic_parser.bug_type import BugType
from la_panic.panic_parser.panic_parser import parse_panic


def test_force_reset_parse_sanity():
    file_path = Path(__file__).parent / 'crash_reports/forceReset-full.ips'
    symbols_path = Path(__file__).parent / 'mocks/symbols.txt'

    with file_path.open("r") as panic_file:
        parsed_result = parse_panic(panic_file, symbols_path)
        assert (parsed_result.bug_type == BugType.FORCE_RESET)


def test_force_reset_parse_using_symbol_renaming():
    MOCK_RENAME = "mock_address_rename"

    file_path = Path(__file__).parent / 'crash_reports/forceReset-full.ips'
    symbols_path = Path(__file__).parent / 'mocks/symbols.txt'

    with file_path.open("r") as panic_file:
        parsed_result = parse_panic(panic_file, symbols_path)
        assert (parsed_result.bug_type == BugType.FORCE_RESET)

    assert (MOCK_RENAME in f"{parsed_result.backtrace}")


def test_panic_base_sanity():
    file_path = Path(__file__).parent / 'crash_reports/panic-base.ips'
    symbols_path = Path(__file__).parent / 'mocks/symbols.txt'

    with file_path.open("r") as panic_file:
        parsed_result = parse_panic(panic_file, symbols_path)
        assert (parsed_result.bug_type == BugType.FULL)
        assert ("80.21.112" in parsed_result.xnu)


def test_panic_full_sanity():
    file_path = Path(__file__).parent / 'crash_reports/panic-full.ips'
    symbols_path = Path(__file__).parent / 'mocks/symbols.txt'

    with file_path.open("r") as panic_file:
        parsed_result = parse_panic(panic_file, symbols_path)
        assert (parsed_result.bug_type == BugType.FULL)
        assert ("42.7" in parsed_result.xnu)

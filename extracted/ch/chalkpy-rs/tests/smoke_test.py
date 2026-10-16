"""Exercise the installed extension without importing the Python SDK."""

from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import chalk_rs


def main() -> None:
    assert chalk_rs.parse_iso_date("2026-05-13") == date(2026, 5, 13)
    assert chalk_rs.parse_iso_time("12:34:56Z") == time(12, 34, 56, tzinfo=timezone.utc)
    assert chalk_rs.parse_datetime("2026-05-13T12:34:56+02:00") == datetime(
        2026, 5, 13, 12, 34, 56, tzinfo=timezone(timedelta(hours=2))
    )
    assert chalk_rs.parse_iso_duration("PT1.5S") == timedelta(seconds=1.5)
    assert chalk_rs.duration_isoformat(timedelta(seconds=1.5)) == "PT1.5S"
    assert chalk_rs.parse_duration_ms("1s") == 1000

    # Parse as source text on every interpreter to keep the native parser's
    # grammar independent of the Python running this test.
    source = (
        "lazy import json\n"
        "lazy from pathlib import Path\n"
        "lists = [[1, 2], [3]]\n"
        "flat = [*items for items in lists]\n"
        "unique = {*items for items in lists}\n"
        "merged = {**items for items in [{'a': 1}]}\n"
        "stream = (*items for items in lists)\n"
        "match 1:\n"
        "    case +1:\n"
        "        pass\n"
    )
    with TemporaryDirectory() as directory:
        path = Path(directory) / "python315.py"
        path.write_text(source, encoding="utf-8", newline="\n")
        cache = chalk_rs.AstFileParserCache([str(path)], directory)
        parsed_path, parsed_source, imports = cache.get_parsed_file(str(path))
        assert parsed_path == str(path)
        assert parsed_source == source
        assert imports["pathlib"]["Path"] == ["Path"]


if __name__ == "__main__":
    main()

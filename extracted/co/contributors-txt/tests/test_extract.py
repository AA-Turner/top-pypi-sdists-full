import json
import logging
from pathlib import Path

import pytest
from contributors_txt.extract_comment import main

HERE = Path(__file__).parent
contributors_aliases = HERE / "pylint_contributors_aliases.json"
expected_contributors_aliases = HERE / "expected_pylint_contributors_aliases.json"


def test_pylint_extraction(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    output = tmp_path / ".contributors_aliases.json"
    main(
        [
            str(HERE / "pylint_contributors.txt"),
            "-a",
            str(contributors_aliases),
            "-o",
            str(output),
        ]
    )
    with open(output, encoding="utf8") as f:
        content = json.load(f)
    with open(expected_contributors_aliases, encoding="utf8") as f:
        expected = json.load(f)
    assert content == expected

#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from pathlib import Path

import pytest

# from cwz.cmk_components import main

# @pytest.mark.parametrize(
#     "section, expected_result",
#     [

# )
# def test_main(capsys) -> None:
#    assert not main(["--requests-vcr-file=cmk-components.yaml", "owners", "notifications/asciimail"])


if __name__ == "__main__":
    # Please keep these lines - they make TDD easy and have no effect on normal test runs.
    # Just set _PYTEST_RAISES=1 and run this file from your IDE and dive into the code.
    source_file_path = (
        (base := (test_file := Path(__file__)).parents[3])
        / test_file.parent.relative_to(base / "test/unit")
        / test_file.name[5:]  # strip "test_" prefix
    ).as_posix()
    assert pytest.main(["--doctest-modules", source_file_path]) in {0, 5}
    pytest.main(["-vvsx", __file__])

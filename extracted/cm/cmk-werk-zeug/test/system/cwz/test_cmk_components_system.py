#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import json

import pytest

from cwz.cmk_components import main


@pytest.mark.parametrize(
    ("sub_command", "entities_variations"),
    [
        (
            "list",
            (([], 0),),
        ),
        (
            "config-files",
            (([], 0),),
        ),
        (
            "config",
            (([], 0),),
        ),
        (
            "paths",
            (
                (["invalid_component"], 1),
                (["ai_dev_tools"], 0),
                (["vue_framework", "plugins_oracle"], 0),
            ),
        ),
        (
            "members",
            (
                ([], 0),
                (["invalid_component"], 1),
            ),
        ),
        (
            "component",
            (
                (["invalid_path"], 1),
                (["packages/cmk-frontend-vue"], 0),
                (["tests/conftest.py"], 0),
                (["packages/cmk-plugins/cmk/plugins/netapp", "cmk/plugins"], 0),
            ),
        ),
        (
            "owners",
            (
                (["invalid_path"], 1),
                (["packages/cmk-mkp-tool"], 0),
                (["tests/conftest.py"], 0),
                (["cmk/legacy_checks", "cmk/plugins"], 0),
            ),
        ),
    ],
)
@pytest.mark.parametrize("mode", ["", "--mode=rich", "--mode=json", "--mode=script"])
def test_main(
    capsys: int, sub_command: str, entities_variations: tuple[list[str], int], mode: str
) -> None:
    """Checks for call-ability of main() with various commands and modes. Doesn't check output correctness."""
    assert entities_variations, "entities_variations must not be empty"
    for entities, expected_result in entities_variations:
        full_command = list(
            filter(
                bool,
                [
                    # "--cache-file=cmk-components-test-cache.yaml",
                    sub_command,
                    mode,
                    *entities,
                ],
            )
        )
        result = main(full_command)
        assert result == expected_result, f"command='{' '.join(full_command)}'"
        stdout, stderr = capsys.readouterr()
        if result:
            assert stderr.splitlines()[0].startswith("ERROR"), f"{stderr=}"
        else:
            assert not stderr
            if mode == "--mode=json":
                json.loads(stdout)


if __name__ == "__main__":
    # Please keep these lines - they make TDD easy and have no effect on normal test runs.
    # Just set _PYTEST_RAISES=1 and run this file from your IDE and dive into the code.
    pytest.main(["-vvsx", __file__])

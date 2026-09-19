"""The packaged policy child must dispatch without entering the ordinary CLI."""

from __future__ import annotations

import os
import subprocess

import pytest

pytestmark = pytest.mark.frozen_binary


@pytest.mark.parametrize("bundle_fixture", ["frozen_aiwatch", "frozen_runlayer"])
def test_policy_child_rejects_invalid_input_without_cli_output(
    request, tmp_path, bundle_fixture
):
    from runlayer_cli.managed_policy_publication import (
        POLICY_PUBLICATION_SENTINEL,
        PUBLICATION_REJECTED,
    )

    executable = request.getfixturevalue(bundle_fixture)
    result = subprocess.run(
        [str(executable), POLICY_PUBLICATION_SENTINEL],
        input="{}",
        text=True,
        capture_output=True,
        timeout=15,
        env={**os.environ, "HOME": str(tmp_path)},
        cwd=tmp_path,
    )

    # An unknown Typer command also exits 2, but prints an error. Empty output
    # distinguishes the native child's early rejection from that false pass.
    assert result.returncode == PUBLICATION_REJECTED
    assert result.stdout == ""
    assert result.stderr == ""

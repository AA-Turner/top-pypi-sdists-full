from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity

SHA = "a" * 40


@pytest.mark.parametrize(
    ("repo", "pr", "sha", "ordinal"),
    [
        ("owner/repo", 1, SHA, 1),
        (None, 1, SHA, 1),
        ("repo", True, SHA, 1),
        ("repo", 0, SHA, 1),
        ("repo", 1, SHA.upper(), 1),
        ("repo", 1, "short", 1),
        ("repo", 1, SHA, 0),
    ],
)
def test_rejects_malformed_fields(repo: object, pr: object, sha: object, ordinal: object) -> None:
    with pytest.raises(ValueError):
        DispatchIdentity(cast(Any, repo), cast(Any, pr), cast(Any, sha), cast(Any, ordinal))

"""A diff result records every file the diff touched, so the app can later ask
whether the config governing any of them changed."""

from pullapprove.config import ConfigModels
from pullapprove.matches import match_diff


def _diff(*paths: str) -> str:
    return "".join(
        f"diff --git a/{path} b/{path}\n@@ -0,0 +1,1 @@\n+x\n" for path in paths
    )


def test_changed_paths_are_every_file_in_the_diff_sorted():
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [{"name": "py", "paths": ["*.py"], "reviewers": ["a"]}]
            }
        }
    )

    results = match_diff(configs.compiled(), _diff("pkg/a.py", "docs/README.md"))

    # The README matched no scope; it is still a file the result depends on.
    assert results.changed_paths == ["docs/README.md", "pkg/a.py"]

from pullapprove.config import ConfigModels
from pullapprove.matches import match_diff


def test_code_match():
    # Technically there is a space missing here on the empty line
    diff = """diff --git a/LICENSE b/LICENSE
index fdddb29..314ba5d 100644
--- a/LICENSE
+++ b/LICENSE
@@ -6,7 +6,7 @@ binary, for any purpose, commercial or non-commercial, and by any
 means.

 In jurisdictions that recognize copyright laws, the author or authors
-of this software dedicate any and all copyright interest in the
+of this software dedicate any and all copyright interest! in the
 software to the public domain. We make this dedication for the benefit
 of the public at large and to the detriment of our heirs and
 successors. We intend this dedication to be an overt act of"""

    # Matches the context line above, and the +/- lines
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "legal",
                        "paths": ["LICENSE"],
                        "code": [
                            ".*copyright.*",
                        ],
                    }
                ]
            }
        }
    )
    diff_results = match_diff(configs.compiled(), diff)
    assert len(diff_results.matches.code.keys()) == 3
    assert diff_results.additions == 1  # One + line in the diff
    assert diff_results.deletions == 1  # One - line in the diff

    # Matches the +/- lines only
    configs = ConfigModels.from_configs_data(
        {
            "CODEREVIEW.toml": {
                "scopes": [
                    {
                        "name": "legal",
                        "paths": ["LICENSE"],
                        "code": [
                            r"^(\+|-).*copyright.*",
                        ],
                    }
                ]
            }
        }
    )
    diff_results = match_diff(configs.compiled(), diff)
    assert len(diff_results.matches.code.keys()) == 2
    assert diff_results.additions == 1  # One + line in the diff (same diff as above)
    assert diff_results.deletions == 1  # One - line in the diff (same diff as above)

# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import base64
import os


def test_geneva_zips_env_var() -> None:
    """
    Test that the GENEVA_ZIPS environment variable is set correctly.
    """
    os.environ["GENEVA_ZIPS"] = base64.b64encode(b'{"zips": [[]]}').decode("utf-8")
    # this loads data if GENEVA_ZIPS is set and could blow up
    import geneva  # noqa: F401

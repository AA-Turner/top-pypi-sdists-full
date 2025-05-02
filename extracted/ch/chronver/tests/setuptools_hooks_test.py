"""test setuptools_hooks

:copyright: Copyright (c) 2024 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""


def test_basic():
    from pykern import pkunit
    from chronver import setuptools_hooks
    import datetime
    import os

    with pkunit.save_chdir_work():
        with pkunit.pkexcept(LookupError):
            setuptools_hooks.version("x")
        e = "20240314.031415"
        with open("PKG-INFO", "wt") as f:
            f.write(
                f"""
Metadata-Version: 2.1
Name: x
Version: {e}
Summary: anything
"""
            )
        pkunit.pkeq(e, setuptools_hooks.version("x"))
        pkunit.pkeq(
            0,
            os.system("git init && echo x > x && git add x && git commit -m x"),
        )
        e = datetime.datetime.utcnow().strftime("%Y%m%d.%H%M%S")
        pkunit.pkok(e, setuptools_hooks.version("x"))

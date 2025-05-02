"""test chronver.pkg_info

:copyright: Copyright (c) 2024 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""


def test_basic():
    from pykern import pkunit
    from chronver import pkg_info

    with pkunit.save_chdir_work():
        a = pkg_info.version()
        pkunit.pkeq(None, a)
        e = "20240314.131830"
        with open("PKG-INFO", "wt") as f:
            f.write(
                f"""
Metadata-Version: 2.1
Name: somepkg
Version: {e}
Summary: anything
"""
            )
        pkunit.pkeq(e, pkg_info.version())

###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import pytest


def test_chained_roots_list():
    from json import dump
    from os import makedirs
    from os.path import join

    from LbEnv.Bootstrap import collect_roots
    from LbEnv.Utils.Temporary import TempDir

    with TempDir() as tmpdir:
        deps = {
            0: None,  # 0 does not contain the json
            1: [0],  # simple
            2: [1],  # 2 levels
            3: [2],  # 3 levels
            4: [],  # empty JSON
            5: [4],  # simple anding on empty JSON
            6: [2, 5],  # multi deps (does it make sense?)
            7: [8],  # chain to non-existend directory
        }
        rootdir = lambda n: join(tmpdir, f"root{n}")

        for n in deps:
            root = rootdir(n)
            etc = join(root, "etc")
            makedirs(etc)
            if deps[n] is not None:
                with open(join(etc, "chaining_infos.json"), "w") as f:
                    dump([rootdir(n) for n in deps[n]], f)

        assert list(collect_roots(rootdir(0))) == list(map(rootdir, [0]))
        assert list(collect_roots(rootdir(1))) == list(map(rootdir, [1, 0]))
        assert list(collect_roots(rootdir(2))) == list(map(rootdir, [2, 1, 0]))
        assert list(collect_roots(rootdir(3))) == list(map(rootdir, [3, 2, 1, 0]))
        assert list(collect_roots(rootdir(4))) == list(map(rootdir, [4]))
        assert list(collect_roots(rootdir(5))) == list(map(rootdir, [5, 4]))
        assert list(collect_roots(rootdir(6))) == list(map(rootdir, [6, 2, 1, 0, 5, 4]))
        assert list(collect_roots(rootdir(7))) == list(map(rootdir, [7]))
        assert list(collect_roots(rootdir(8))) == list(map(rootdir, []))


def test_search_path():
    # make sure we cannot use LbDevTools
    import sys

    try:
        import LbDevTools

        old = sys.modules["LbDevTools"]
        sys.modules["LbDevTools"] = sys.modules["LbEnv"]
    except ImportError:
        old = None

    try:
        from os.path import join

        from LbEnv.Bootstrap import search_path
        from LbEnv.Utils.Temporary import TempDir

        base = "/path/to/base"
        derived = "/path/to/derived"

        suffixes = [
            "lhcb",
            "lcg/releases",
            "lcg/app/releases",
            "lcg/external",
            "contrib",
            "cmake",
        ]

        result = list(search_path([]))
        expected = []
        assert result == expected

        result = list(search_path([base]))
        expected = [join(base, suff) for suff in suffixes]
        assert result == expected

        result = list(search_path([derived, base]))
        expected = [join(derived, suff) for suff in suffixes] + [
            join(base, suff) for suff in suffixes
        ]
        assert result == expected

        with TempDir() as tmpdir:
            sys.path.insert(0, tmpdir)
            try:
                if "LbDevTools" in sys.modules:
                    del sys.modules["LbDevTools"]

                with open(join(tmpdir, "LbDevTools.py"), "w") as f:
                    f.write('DATA_DIR = "/path/to/devtools"\n')

                result = list(search_path([base]))
                expected = [join(base, suff) for suff in suffixes] + [
                    "/path/to/devtools/cmake"
                ]
                assert result == expected

            finally:
                sys.path.pop(0)

                if "LbDevTools" in sys.modules:
                    del sys.modules["LbDevTools"]

    finally:
        if old:
            sys.modules["LbDevTools"] = old


def test_bin_path():
    from os.path import join

    from LbEnv.Bootstrap import bin_path

    base = "/path/to/base"
    derived = "/path/to/derived"

    result = list(bin_path([], "host-os", "host-flavour"))
    expected = []
    assert result == expected

    result = list(bin_path([base]))
    expected = [join(base, "bin")]
    assert result == expected

    result = list(bin_path([base], host_os="host-os"))
    expected = [join(base, "bin", "host-os"), join(base, "bin")]
    assert result == expected

    result = list(bin_path([base], host_flavour="host-flavour"))
    expected = [join(base, "bin", "host-flavour"), join(base, "bin")]
    assert result == expected

    result = list(bin_path([base], host_os="host-os", host_flavour="host-flavour"))
    expected = [
        join(base, "bin", "host-os"),
        join(base, "bin", "host-flavour"),
        join(base, "bin"),
    ]
    assert result == expected

    result = list(
        bin_path([derived, base], host_os="host-os", host_flavour="host-flavour")
    )
    expected = [
        join(derived, "bin", "host-os"),
        join(derived, "bin", "host-flavour"),
        join(derived, "bin"),
        join(base, "bin", "host-os"),
        join(base, "bin", "host-flavour"),
        join(base, "bin"),
    ]
    assert result == expected


@pytest.mark.parametrize(
    "siteroot", [None, "/some/custom/path", "/cvmfs/lhcb.cern.ch/lib"]
)
def test_siteroot(monkeypatch, capsys, siteroot):
    import LbEnv.__main__
    from LbEnv.Bootstrap import main

    # Make sure the envrioment is clean
    for var_name in ["MYSITEROOT", "VO_LHCB_SW_DIR", "VIRTUAL_ENV"]:
        monkeypatch.delenv(var_name, raising=False)

    argv = [LbEnv.__main__.__file__, "--sh"]
    if siteroot is not None:
        argv.extend(["--siteroot", siteroot])
    monkeypatch.setattr("sys.argv", argv)
    if siteroot is None:
        siteroot = "/cvmfs/lhcb.cern.ch/lib"

    main()

    out, err = capsys.readouterr()
    assert err == ""
    assert f"export MYSITEROOT={siteroot}" in out

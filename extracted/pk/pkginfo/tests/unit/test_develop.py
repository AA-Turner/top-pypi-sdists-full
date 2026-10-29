import pytest

def _make_develop(dirname):
    from pkginfo.develop import Develop
    return Develop(dirname)

def _make_develop_dir(tmp_path):
    # Synthesize a 'develop' checkout whose egg-info carries the metadata
    # of the installed package, so that the test doesn't depend on which
    # egg-info directories happen to lie within the source tree (GH #3).
    from importlib import metadata as importlib_metadata

    egg_info = tmp_path / 'pkginfo.egg-info'
    egg_info.mkdir()
    pkg_info = egg_info / 'PKG-INFO'
    pkg_info.write_text(
        importlib_metadata.distribution('pkginfo').read_text('METADATA'))
    return tmp_path

def test_develop_ctor_w_path(tmp_path):
    from tests.unit import _helpers
    develop = _make_develop(str(_make_develop_dir(tmp_path)))
    _helpers._checkDevelop(None, develop)

def test_develop_ctor_w_invalid_path():
    import warnings 
    from pkginfo.distribution import UnknownMetadataVersion

    with warnings.catch_warnings(record=True) as warned:
        develop = _make_develop('/nonesuch')

    assert(develop.metadata_version == None)
    assert(develop.name == None)
    assert(develop.version == None)

    assert len(warned) == 2
    assert str(warned[0].message).startswith('No PKG-INFO found')
    assert warned[1].category is UnknownMetadataVersion

import fmod_toolkit


def test_version():
    assert fmod_toolkit.__version__


def test_import():
    import fmod_toolkit.importer as importer

    assert importer.import_pyfmodex()

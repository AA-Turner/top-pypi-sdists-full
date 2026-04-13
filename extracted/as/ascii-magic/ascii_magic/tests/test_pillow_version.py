from ascii_magic import AsciiArt


def test_pillow_version():
    print(AsciiArt.__PILLOW_VERSION__)
    assert AsciiArt.__PILLOW_VERSION__ != '0'

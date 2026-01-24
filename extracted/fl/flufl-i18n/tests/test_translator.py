# This cannot be a doctest because of the sys._getframe() manipulations.  That
# does not play well with the way doctest executes Python code.  But see
# translator.txt for a description of how this should work in real Python code.

import pytest

from flufl.i18n._translator import Translator


# Some globals for following tests.
purple = 'porpoises'
magenta = 'monkeys'
green = 'gerbil'


class Catalog:
    """Test catalog."""

    def __init__(self):
        self.translation = None

    def gettext(self, original):
        """Return the translation."""
        return self.translation

    def charset(self):
        """Return the encoding."""
        # The default is ASCII.
        return None


@pytest.fixture
def translator():
    # We need depth=1 because we're calling the translation at the same level
    # as the locals we care about.
    return Translator(Catalog(), depth=1)


def test_locals(translator):
    # Test that locals get properly substituted.
    aqua = 'aardvarks'                          # noqa: F841
    blue = 'badgers'                            # noqa: F841
    cyan = 'cats'                               # noqa: F841
    translator.catalog.translation = '$blue and $cyan and $aqua'
    translated = translator.translate('source string')
    assert translated == 'badgers and cats and aardvarks'


def test_globals(translator):
    # Test that globals get properly substituted.
    translator.catalog.translation = '$purple and $magenta and $green'
    translated = translator.translate('source string')
    assert translated == 'porpoises and monkeys and gerbil'


def test_dict_overrides_locals(translator):
    # Test that explicit mappings override locals.
    aqua = 'aardvarks'                          # noqa: F841
    blue = 'badgers'                            # noqa: F841
    cyan = 'cats'                               # noqa: F841
    overrides = dict(blue='bats')
    translator.catalog.translation = '$blue and $cyan and $aqua'
    translated = translator.translate('source string', overrides)
    assert translated == 'bats and cats and aardvarks'


def test_globals_with_overrides(translator):
    # Test that globals with overrides get properly substituted.
    translator.catalog.translation = '$purple and $magenta and $green'
    overrides = dict(green='giraffe')
    translated = translator.translate('source string', overrides)
    assert translated == 'porpoises and monkeys and giraffe'


def test_empty_string(translator):
    # The empty string is always translated as the empty string.
    assert translator.translate('') == ''


def test_dedent(translator):
    # By default, the translated string is always dedented.
    aqua = 'aardvarks'                          # noqa: F841
    blue = 'badgers'                            # noqa: F841
    cyan = 'cats'                               # noqa: F841
    translator.catalog.translation = """\
    These are the $blue
    These are the $cyan
    These are the $aqua
    """
    for line in translator.translate('source string').splitlines():
        assert line[:5] == 'These'


def test_no_dedent(translator):
    # You can optionally suppress the dedent.
    aqua = 'aardvarks'                          # noqa: F841
    blue = 'badgers'                            # noqa: F841
    cyan = 'cats'                               # noqa: F841
    translator.catalog.translation = """\
    These are the $blue
    These are the $cyan
    These are the $aqua\
    """
    translator.dedent = False
    for line in translator.translate('source string').splitlines():
        assert line[:9] == '    These'

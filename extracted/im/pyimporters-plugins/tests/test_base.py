import zipfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserModel


def test_parser():
    with pytest.raises(TypeError) as err:
        parser = KnowledgeParserBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class KnowledgeParserBase with abstract methods parse"
        in str(err.value)
    )


def test_default_options():
    options = KnowledgeParserModel()
    assert options.project is None
    assert options.lexicon is None
    assert options.limit == 0
    assert options.lang == "en"


def test_options_validation():
    with pytest.raises(ValidationError):
        options = KnowledgeParserModel(limit=-1)
        assert options is None


def test_guess_zip():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/small.zip")
    assert zipfile.is_zipfile(source) is True
    source = Path(testdir, "data/small_zip")
    assert zipfile.is_zipfile(source) is True
    source = Path(testdir, "data/small.xml.gz")
    assert zipfile.is_zipfile(source) is False

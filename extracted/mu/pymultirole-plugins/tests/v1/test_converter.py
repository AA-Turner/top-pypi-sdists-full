import io
from typing import List, Type

import pytest
from pydantic import BaseModel, Field
from starlette.datastructures import UploadFile

from pymultirole_plugins.v1.converter import ConverterBase, ConverterParameters
from pymultirole_plugins.v1.schema import Document


def test_converter():
    with pytest.raises(TypeError) as err:
        parser = ConverterBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class ConverterBase with abstract methods convert"
        in str(err.value)
    )


def test_default_options():
    options = ConverterParameters()
    assert options is not None


class DummyParameters(ConverterParameters):
    foo: str = Field("foo", description="Foo")
    bar: int = Field(0, description="Bar")


class DummyConverter(ConverterBase):
    """Dummy converter."""

    def convert(
        self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        """Parse the input source file and return a list of documents.

        :param source: A file object containing the data.
        :param parameters: options of the converter.
        :returns: List of converted documents.
        """
        parameters: DummyParameters = parameters
        doc = Document(text=source.file.read(), metadata=parameters.dict())
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    converter = DummyConverter()
    options = DummyParameters()
    docs = converter.convert(UploadFile("dummy", io.StringIO("dummy text")), options)
    assert len(docs) == 1
    assert docs[0].text == "dummy text"
    assert docs[0].metadata == options.dict()

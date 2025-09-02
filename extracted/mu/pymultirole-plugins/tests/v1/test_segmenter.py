from typing import Type, List

import pytest
from pydantic import BaseModel, Field

from pymultirole_plugins.v1.schema import Document
from pymultirole_plugins.v1.segmenter import SegmenterBase, SegmenterParameters


def test_segmenter():
    with pytest.raises(TypeError) as err:
        parser = SegmenterBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class SegmenterBase with abstract methods segment"
        in str(err.value)
    )


def test_default_options():
    options = SegmenterParameters()
    assert options is not None


class DummyParameters(SegmenterParameters):
    foo: str = Field("foo", description="Foo")
    bar: float = Field(0.123456789, description="Bar")


class Dummysegmenter(SegmenterBase):
    """Dummy segmenter."""

    def segment(
        self, documents: List[Document], parameters: SegmenterParameters
    ) -> List[Document]:
        parameters: DummyParameters = parameters
        documents[0].sentences = [{"start": 0, "end": 1}]
        documents[0].boundaries = {
            parameters.foo: [{"name": parameters.bar, "start": 0, "end": 1}]
        }
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    segmenter = Dummysegmenter()
    options = DummyParameters()
    docs: List[Document] = segmenter.segment(
        [Document(text="This is a test document.", metadata=options.dict())], options
    )
    assert len(docs[0].sentences) == 1
    assert len(docs[0].boundaries) == 1

from typing import Type, List
import pytest
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.annotator import AnnotatorBase, AnnotatorParameters
from pymultirole_plugins.v1.schema import Document, Category


def test_annotator():
    with pytest.raises(TypeError) as err:
        parser = AnnotatorBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class AnnotatorBase with abstract methods annotate"
        in str(err.value)
    )


def test_default_options():
    options = AnnotatorParameters()
    assert options is not None


class DummyParameters(AnnotatorParameters):
    foo: str = Field("foo", description="Foo")
    bar: float = Field(0.123456789, description="Bar")


class Dummyannotator(AnnotatorBase):
    """Dummy annotator."""

    def annotate(
        self, documents: List[Document], parameters: AnnotatorParameters
    ) -> List[Document]:
        parameters: DummyParameters = parameters
        documents[0].categories = [
            Category(labelName=parameters.foo, score=parameters.bar)
        ]
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    annotator = Dummyannotator()
    options = DummyParameters()
    docs: List[Document] = annotator.annotate(
        [Document(text="This is a test document", metadata=options.dict())], options
    )
    assert len(docs[0].categories) == 1
    assert docs[0].categories[0].labelName == options.foo
    assert docs[0].categories[0].score == options.bar


def test_singleton():
    annotator1 = Dummyannotator()
    annotator2 = Dummyannotator()
    assert id(annotator2) == id(annotator1)

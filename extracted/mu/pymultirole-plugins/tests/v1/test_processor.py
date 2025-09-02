from typing import Type, List
import pytest
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorBase, ProcessorParameters
from pymultirole_plugins.v1.schema import Document, Category


def test_processor():
    with pytest.raises(TypeError) as err:
        parser = ProcessorBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class ProcessorBase with abstract methods process"
        in str(err.value)
    )


def test_default_options():
    options = ProcessorParameters()
    assert options is not None


class DummyParameters(ProcessorParameters):
    foo: str = Field("foo", description="Foo")
    bar: float = Field(0.123456789, description="Bar")


class Dummyprocessor(ProcessorBase):
    """Dummy processor."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
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
    processor = Dummyprocessor()
    options = DummyParameters()
    docs: List[Document] = processor.process(
        [Document(text="This is a test document", metadata=options.dict())], options
    )
    assert len(docs[0].categories) == 1
    assert docs[0].categories[0].labelName == options.foo
    assert docs[0].categories[0].score == options.bar

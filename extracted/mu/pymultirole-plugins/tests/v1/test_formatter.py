from typing import Type

import pytest
from pydantic import BaseModel, Field
from starlette.responses import Response, JSONResponse

from pymultirole_plugins.v1.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.v1.schema import Document


def test_formatter():
    with pytest.raises(TypeError) as err:
        parser = FormatterBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class FormatterBase with abstract methods format"
        in str(err.value)
    )


def test_default_options():
    options = FormatterParameters()
    assert options is not None


class DummyParameters(FormatterParameters):
    foo: str = Field("foo", description="Foo")
    bar: int = Field(0, description="Bar")


class DummyFormatter(FormatterBase):
    """Dummy formatter."""

    def format(self, document: Document, parameters: FormatterParameters) -> Response:
        parameters: DummyParameters = parameters
        output = {"text": document.text, "foo": parameters.foo, "bar": parameters.bar}
        return JSONResponse(content=output)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    formatter = DummyFormatter()
    options = DummyParameters()
    resp: Response = formatter.format(
        Document(text="This is a test document", metadata=options.dict()), options
    )
    assert resp.status_code == 200
    assert resp.media_type == "application/json"

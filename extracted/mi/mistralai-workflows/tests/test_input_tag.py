from pydantic import BaseModel, ConfigDict

from mistralai.workflows.conversational import (
    input_tag,
)


def test_input_tag_adds_x_input_tag_to_schema() -> None:
    @input_tag("my-custom-tag")
    class MyModel(BaseModel):
        name: str

    schema = MyModel.model_json_schema()
    assert schema.get("x-input-tag") == "my-custom-tag"


def test_input_tag_preserves_existing_json_schema_extra_dict() -> None:
    class MyModel(BaseModel):
        model_config = ConfigDict(json_schema_extra={"x-custom": "keep-me"})
        name: str

    decorated = input_tag("tagged")(MyModel)
    schema = decorated.model_json_schema()
    assert schema.get("x-input-tag") == "tagged"
    assert schema.get("x-custom") == "keep-me"


def test_input_tag_composes_with_callable_json_schema_extra() -> None:
    """When json_schema_extra is a callable, it is composed: callable runs first, then x-input-tag is added."""

    def _extra(schema: dict) -> None:
        schema["x-from-callable"] = True

    class MyModel(BaseModel):
        model_config = ConfigDict(json_schema_extra=_extra)
        name: str

    decorated = input_tag("composed")(MyModel)
    schema = decorated.model_json_schema()
    assert schema.get("x-input-tag") == "composed"
    assert schema.get("x-from-callable") is True

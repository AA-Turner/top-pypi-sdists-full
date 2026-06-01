"""Tests for BaseModel camelCase aliasing and model_config."""

from csrd.models import BaseModel, model_config


class SampleModel(BaseModel):
    first_name: str
    last_name: str
    is_active: bool = True


class SampleWithConfig(BaseModel):
    model_config = model_config
    hello_world: str = "hi"


class TestBaseModelAliasing:
    def test_camel_case_serialization(self):
        m = SampleModel(firstName="Alice", lastName="Smith")
        dumped = m.model_dump(by_alias=True)
        assert dumped == {"firstName": "Alice", "lastName": "Smith", "isActive": True}

    def test_camel_case_deserialization(self):
        m = SampleModel.model_validate({"firstName": "Bob", "lastName": "Jones"})
        assert m.first_name == "Bob"
        assert m.last_name == "Jones"

    def test_snake_case_dump(self):
        m = SampleModel(firstName="Carol", lastName="Doe")
        dumped = m.model_dump()
        assert dumped == {"first_name": "Carol", "last_name": "Doe", "is_active": True}

    def test_populate_by_name_with_config(self):
        """SampleWithConfig uses model_config with populate_by_name=True."""
        m = SampleWithConfig(hello_world="hey")
        assert m.hello_world == "hey"

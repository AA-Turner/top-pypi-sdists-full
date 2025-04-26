from connector.serializers.request import AnnotatedField
from pydantic import BaseModel


class TestSerializersAnnotatedField:
    def test_group_adds_extension(self) -> None:
        """Make sure the group parameter adds the right property extension to the JSON Schema"""

        class TestModel(BaseModel):
            name: str = AnnotatedField(group="5")

        schema = TestModel.model_json_schema()
        assert schema["properties"]["name"]["x-field_group"] == "5"

    def test_multiline_adds_extension(self) -> None:
        """Make sure the multiline parameter adds the right property extension to the JSON Schema"""

        class TestModel(BaseModel):
            name: str = AnnotatedField(multiline=True)

        schema = TestModel.model_json_schema()
        assert schema["properties"]["name"]["x-multiline"] is True

    def test_secret_adds_extension(self) -> None:
        """Make sure the secret parameter adds the right property extension to the JSON Schema"""

        class TestModel(BaseModel):
            name: str = AnnotatedField(secret=True)

        schema = TestModel.model_json_schema()
        assert schema["properties"]["name"]["x-secret"] is True

    def test_primary_adds_extension(self) -> None:
        """Make sure the primary parameter adds the right property extension to the JSON Schema"""

        class TestModel(BaseModel):
            name: str = AnnotatedField(primary=False)

        schema = TestModel.model_json_schema()
        assert schema["properties"]["name"]["x-primary"] is False

    def test_semantic_type_adds_extension(self) -> None:
        """Make sure the semantic_type parameter adds the right property extension to the JSON Schema"""

        class TestModel(BaseModel):
            name: str = AnnotatedField(semantic_type="account-id")

        schema = TestModel.model_json_schema()
        assert schema["properties"]["name"]["x-semantic"] == "account-id"

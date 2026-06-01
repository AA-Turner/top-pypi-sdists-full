"""Tests for ModelParserMixin."""

import pytest
from pydantic import BaseModel, ValidationError

from csrd.models.model_parser import ModelParserMixin


class Item(BaseModel):
    name: str
    price: float


class TestModelParserMixin:
    def setup_method(self):
        self.parser = ModelParserMixin()

    def test_apply_model_dict_to_model(self):
        result = self.parser.apply_model({"name": "Widget", "price": 9.99}, model=Item)
        assert isinstance(result, Item)
        assert result.name == "Widget"
        assert result.price == 9.99

    def test_apply_model_list_to_list_model(self):
        data = [{"name": "A", "price": 1.0}, {"name": "B", "price": 2.0}]
        result = self.parser.apply_model(data, model=list[Item])
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].name == "A"
        assert result[1].name == "B"

    def test_apply_model_no_model_passthrough(self):
        data = {"key": "value"}
        result = self.parser.apply_model(data)
        assert result == data

    def test_apply_model_none_model_passthrough(self):
        data = [1, 2, 3]
        result = self.parser.apply_model(data, model=None)
        assert result == [1, 2, 3]

    def test_apply_model_dict_expected_but_list_given(self):
        with pytest.raises(TypeError, match="Expected dict"):
            self.parser.apply_model([1, 2], model=Item)

    def test_apply_model_list_expected_but_dict_given(self):
        with pytest.raises(TypeError, match="Expected list"):
            self.parser.apply_model({"name": "X", "price": 1.0}, model=list[Item])

    def test_apply_model_validation_error(self):
        with pytest.raises(ValidationError):
            self.parser.apply_model({"name": "X"}, model=Item)  # missing price

    def test_apply_model_custom_exception(self):
        with pytest.raises(ValueError):
            self.parser.apply_model({"wrong": "data"}, model=Item, exception=ValueError)

    def test_apply_model_with_handler(self):
        def custom_handler(source, model):
            return "custom_result"

        result = self.parser.apply_model(
            {"name": "X", "price": 1.0}, model=Item, model_handler=custom_handler
        )
        assert result == "custom_result"

    def test_apply_model_with_json_source(self):
        """Test DefaultExtractor handles objects with .json() method."""

        class FakeResponse:
            def json(self):
                return {"name": "FromJSON", "price": 5.0}

        result = self.parser.apply_model(FakeResponse(), model=Item)
        assert result.name == "FromJSON"

    def test_custom_extractor(self):
        class UpperExtractor:
            def extract(self, source):
                return {k.upper(): v for k, v in source.items()}

        # Use extractor at parse time
        parser = ModelParserMixin()

        class UpperModel(BaseModel):
            NAME: str
            PRICE: float

        result = parser.apply_model(
            {"name": "test", "price": 1.0},
            model=UpperModel,
            extractor=UpperExtractor(),
        )
        assert result.NAME == "test"

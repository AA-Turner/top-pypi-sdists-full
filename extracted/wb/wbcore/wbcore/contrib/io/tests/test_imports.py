from typing import Any
from unittest.mock import patch

import pytest
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from wbcore.contrib.io.factories import ImportModel

from ..factories import ImportExportModelHandler
from ..models import Source

fake = Faker()


@pytest.fixture()
def handler(import_source):
    return ImportExportModelHandler(import_source)


def to_dict(model):
    many = []
    if model.many_relationships:
        many = [m for m in model.many_relationships.all()]

    return {
        "relationship": model.relationship,
        "import_source": model.import_source,
        "many_relationships": many,
        "number": model.number,
        "text": model.text,
        "name": model.name,
    }


@pytest.mark.django_db
class TestImportSourceModel:
    def _get_random_data(self, parser_handler_factory, relationship_id=None, object_id=None, history=False):
        res: dict[str, Any] = {
            "data": [
                {
                    "relationship": parser_handler_factory.create().id if not relationship_id else relationship_id,
                    "many_relationships": [parser_handler_factory.create().id],
                    "number": fake.pyfloat(),
                    "text": fake.paragraph(),
                    "name": fake.name(),
                    "id": object_id,
                }
            ]
        }
        if history:
            res["history"] = {"relationship": relationship_id if relationship_id else res["data"][0]["relationship"]}
        return res

    def test_init(self, import_model):
        assert import_model.id is not None

    @patch.object(Source, "generate_import_sources")
    @pytest.mark.parametrize(
        "parser_handler__handler,data_backend__passive_only",
        [
            ("wbcore.contrib.io.ImportModel", True),  # Trigger import_source
            ("wbcore.contrib.io.ImportModel", False),  # Do nothing
            ("otherapplabel.OtherModel", True),  # Do nothing
        ],
    )
    def test_import_data(self, mock_process_source, import_model, source, parser_handler, data_backend):
        source.parser_handler.add(parser_handler)
        source.save()
        content_type = ContentType.objects.get_for_model(ImportModel)
        model_name = f"{content_type.app_label}.{content_type.model}"
        nb_valid_sources = Source.objects.filter(parser_handler__handler__iexact=model_name)

        import_model.import_data()
        assert mock_process_source.call_count == nb_valid_sources.count()

    def test_model_dict_diff(self, import_model_factory, handler, import_source, parser_handler_factory):
        a11 = parser_handler_factory.create()
        a12 = parser_handler_factory.create()
        a2 = parser_handler_factory.create()
        model = import_model_factory.create(many_relationships=[a11, a12])
        comparison_model = import_model_factory.create(many_relationships=[a11, a2])

        diff_dict = handler._model_dict_diff(model, to_dict(comparison_model))
        assert diff_dict["relationship"] == comparison_model.relationship
        assert diff_dict["import_source"] == comparison_model.import_source
        assert set(diff_dict["many_relationships"]) == set([a2])
        assert diff_dict["number"] == pytest.approx(comparison_model.number, rel=10 - 6)
        assert diff_dict["text"] == comparison_model.text
        assert diff_dict["name"] == comparison_model.name

    def test_model_dict_diff_no_change(self, import_model_factory, handler, import_source, parser_handler_factory):
        a11 = parser_handler_factory.create()
        a12 = parser_handler_factory.create()
        model = import_model_factory.create(many_relationships=[a11, a12])
        comparison_model = model

        diff_dict = handler._model_dict_diff(model, to_dict(comparison_model))
        assert not diff_dict

    def test_data_changed(self, import_model_factory, handler, import_source, parser_handler_factory):
        a11 = parser_handler_factory.create()
        a12 = parser_handler_factory.create()
        a2 = parser_handler_factory.create()
        model = import_model_factory.create(many_relationships=[a11, a12], import_source=handler.import_source)
        comparison_model = import_model_factory.create(
            many_relationships=[a11, a2], import_source=handler.import_source
        )
        data = to_dict(comparison_model)
        diff_dict = handler._model_dict_diff(model, data)
        handler._data_changed(model, diff_dict, data)
        handler._data_changed(model, diff_dict, data)
        assert model.relationship == comparison_model.relationship
        assert model.import_source == comparison_model.import_source
        assert set(model.many_relationships.values_list("id", flat=True)) == set({a11.id, a12.id, a2.id})
        assert model.number == pytest.approx(comparison_model.number, rel=10 - 3)
        assert model.text == comparison_model.text
        assert model.name == comparison_model.name

    def test_data_change_only_fields(self, handler, import_source, import_model_factory):
        model = import_model_factory.create()
        comparison_model = import_model_factory.create()
        data = to_dict(comparison_model)
        diff_dict = handler._model_dict_diff(model, data)
        handler._data_changed(model, diff_dict, data, include_update_fields=["number", "text"])
        assert model.number == pytest.approx(comparison_model.number, rel=10 - 3)
        assert model.text == comparison_model.text
        assert model.name != comparison_model.name

    def test_process_wrongly_formatted_import_data(self, handler, import_source):
        with pytest.raises(KeyError):
            handler.process(dict(a=1, b="b"))

    def test_process_basic(self, handler, import_source, parser_handler_factory):
        # Create basic data and call process. We expect only one object to be created
        import_data = self._get_random_data(parser_handler_factory)
        handler.process(import_data)
        created_obj = ImportModel.objects.first()
        if not created_obj:
            raise ValueError("We expect a created object")
        assert created_obj.text == import_data["data"][0]["text"]
        assert created_obj.name == import_data["data"][0]["name"]
        assert created_obj.number == import_data["data"][0]["number"]

        # If we recall process without specifying lookup identifier, we expect a second object to be created
        handler.process(import_data)
        assert ImportModel.objects.count() == 2

        # If we generate completely new data but with a lookup pointing to the first created object, we expect its value
        # to be updated instead of created.
        new_import_data = self._get_random_data(parser_handler_factory, object_id=created_obj.pk)
        handler.process(new_import_data)
        assert ImportModel.objects.count() == 2
        created_obj.refresh_from_db()
        assert created_obj.text == new_import_data["data"][0]["text"]
        assert created_obj.name == new_import_data["data"][0]["name"]
        assert created_obj.number == new_import_data["data"][0]["number"]

        import_historical_data = self._get_random_data(
            parser_handler_factory,
            object_id=created_obj.pk,
            history=True,
            relationship_id=import_data["data"][0]["relationship"],
        )
        # Even though id is provided, we expect the history to not include this object (because get_history will return
        # a queryset without it
        handler.process(import_historical_data)
        assert ImportModel.objects.count() == 3

import pytest
from pytest import FixtureRequest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.io.factories import (
    DataBackendFactory,
    ImportSourceFactory,
    ParserHandlerFactory,
    SourceFactory,
)
from wbcore.contrib.io.models import DataBackend, ImportSource, ParserHandler
from wbcore.contrib.io.serializers import (
    ImportSourceModelSerializer,
    ParserHandlerModelSerializer,
)
from wbcore.contrib.io.viewsets import (
    DataBackendRepresentationViewSet,
    ImportSourceModelViewSet,
    ImportSourceRepresentationViewSet,
    ParserHandlerModelViewSet,
    ParserHandlerRepresentationViewSet,
    SourceModelViewSet,
    SourceRepresentationViewSet,
)

BATCH_SIZE = 3


@pytest.mark.django_db
@pytest.mark.with_db
class TestViewsets:
    @pytest.fixture
    def request_factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def super_user(self):
        return SuperUserFactory()

    @pytest.fixture
    def import_sources(self):
        return ImportSourceFactory.create_batch(BATCH_SIZE)

    @pytest.fixture
    def import_source(self, import_sources):
        return import_sources[0]

    @pytest.fixture
    def import_source_build(self):
        parser_handler = ParserHandlerFactory()
        source = SourceFactory()

        instance = ImportSourceFactory.build(parser_handler=None, source=None)

        serialized_data = ImportSourceModelSerializer(instance).data

        serialized_data["parser_handler"] = parser_handler.id
        serialized_data["source"] = source.id

        return serialized_data

    @pytest.fixture
    def sources(self):
        return SourceFactory.create_batch(BATCH_SIZE)

    @pytest.fixture
    def source(self, sources):
        return sources[0]

    @pytest.fixture
    def parser_handlers(self):
        return ParserHandlerFactory.create_batch(BATCH_SIZE)

    @pytest.fixture
    def parser_handler(self, parser_handlers):
        return parser_handlers[0]

    @pytest.fixture
    def parser_handler_build(self):
        instance = ParserHandlerFactory.build()
        return ParserHandlerModelSerializer(instance).data

    @pytest.fixture
    def data_backends(self):
        DataBackend.objects.all().delete()
        return DataBackendFactory.create_batch(BATCH_SIZE)

    @pytest.fixture
    def data_backend(self, data_backends):
        return data_backends[0]

    @pytest.mark.parametrize(
        "vs, batch",
        [
            (ImportSourceRepresentationViewSet, "import_sources"),
            (ImportSourceModelViewSet, "import_sources"),
            (SourceRepresentationViewSet, "sources"),
            (SourceModelViewSet, "sources"),
            (ParserHandlerRepresentationViewSet, "parser_handlers"),
            (ParserHandlerModelViewSet, "parser_handlers"),
        ],
    )
    def test_get(self, request_factory, super_user, vs, batch, request: FixtureRequest):
        # Arrange
        request.getfixturevalue(batch)
        get_request = request_factory.get("")
        get_request.user = super_user
        viewset = vs.as_view({"get": "list"})
        # Act
        response = viewset(get_request)
        # Assert
        assert len(response.data["results"]) == BATCH_SIZE
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "vs, instance",
        [
            (ImportSourceRepresentationViewSet, "import_source"),
            (ImportSourceModelViewSet, "import_source"),
            (SourceRepresentationViewSet, "source"),
            (SourceModelViewSet, "source"),
            (ParserHandlerRepresentationViewSet, "parser_handler"),
            (ParserHandlerModelViewSet, "parser_handler"),
            (DataBackendRepresentationViewSet, "data_backend"),
        ],
    )
    def test_retrieve(self, request_factory, super_user, vs, instance, request: FixtureRequest):
        # Arrange
        entry = request.getfixturevalue(instance)
        get_request = request_factory.get("")
        get_request.user = super_user
        viewset = vs.as_view({"get": "retrieve"})
        # We need to work with lookup_field since SourceModelViewSet uses uuid as lookup field
        lookup_field = getattr(vs, "lookup_field", "pk")
        lookup_value = getattr(entry, lookup_field)
        # Act
        response = viewset(get_request, **{lookup_field: lookup_value})
        lookup_field = "id" if lookup_field != "uuid" else "uuid"
        instance = response.data.get("instance")
        # Assert
        assert instance is not None
        assert str(instance[lookup_field]) == str(lookup_value)
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "vs, data, creatable",
        [
            (ImportSourceModelViewSet, "import_source_build", True),
            (ParserHandlerModelViewSet, "parser_handler_build", False),
        ],
    )
    def test_create(self, request_factory, super_user, vs, data, creatable, request: FixtureRequest):
        # Arrange
        build_data = request.getfixturevalue(data)
        post_request = request_factory.post("", data=build_data, format="json")
        post_request.user = super_user
        viewset = vs.as_view({"post": "create"})
        # Act
        response = viewset(post_request)
        expected_status_code = status.HTTP_201_CREATED if creatable else status.HTTP_405_METHOD_NOT_ALLOWED
        # Assert
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "vs, batch, model, deletable",
        [
            (ImportSourceModelViewSet, "import_sources", ImportSource, True),
            (ParserHandlerModelViewSet, "parser_handlers", ParserHandler, False),
        ],
    )
    def test_delete(
        self,
        request_factory,
        super_user,
        vs,
        batch,
        model,
        deletable,
        request: FixtureRequest,
    ):
        # Arrange
        entries = request.getfixturevalue(batch)
        entry_id = entries[0].id
        delete_request = request_factory.delete("", args=entry_id)
        delete_request.user = super_user
        viewset = vs.as_view({"delete": "destroy"})
        # Act
        response = viewset(delete_request, pk=entry_id)
        # Assert
        if deletable:
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert model.objects.count() == BATCH_SIZE - 1
            assert not model.objects.filter(id=entry_id).exists()
        else:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            assert model.objects.count() == BATCH_SIZE
            assert model.objects.filter(id=entry_id).exists()

    @pytest.mark.parametrize(
        "vs, entry, new_data, updatable",
        [
            (ImportSourceModelViewSet, "import_source", "import_source_build", True),
            (
                ParserHandlerModelViewSet,
                "parser_handler",
                "parser_handler_build",
                False,
            ),
        ],
    )
    def test_put(
        self,
        request_factory,
        super_user,
        vs,
        entry,
        new_data,
        updatable,
        request: FixtureRequest,
    ):
        # Arrange
        entry = request.getfixturevalue(entry)
        new_data = request.getfixturevalue(new_data)
        new_data["id"] = entry.id
        put_request = request_factory.put("", data=new_data, format="json")
        put_request.user = super_user
        viewset = vs.as_view({"put": "update"})
        # Act
        response = viewset(put_request, pk=entry.id)
        expected_status_code = status.HTTP_200_OK if updatable else status.HTTP_405_METHOD_NOT_ALLOWED
        # Assert
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "vs, entry, field, updatable",
        [
            (ImportSourceModelViewSet, "import_source", "origin", True),
            (ParserHandlerModelViewSet, "parser_handler", "parser", False),
        ],
    )
    def test_patch(
        self,
        request_factory,
        super_user,
        vs,
        entry,
        field,
        updatable,
        request: FixtureRequest,
    ):
        # Arrange
        instance = request.getfixturevalue(entry)
        old_field_data = getattr(instance, field)
        new_field_data = "Foo Bar"
        patch_request = request_factory.patch("", data={field: new_field_data})
        patch_request.user = super_user
        viewset = vs.as_view({"patch": "partial_update"})
        # Act
        response = viewset(patch_request, pk=instance.id)
        instance.refresh_from_db()
        # Assert
        if updatable:
            assert response.status_code == status.HTTP_200_OK
            assert getattr(instance, field) == new_field_data
        else:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            assert getattr(instance, field) == old_field_data

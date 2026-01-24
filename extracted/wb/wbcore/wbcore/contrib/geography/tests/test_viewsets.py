import pytest
from rest_framework import status

from wbcore.contrib.geography.factories import ContinentFactory
from wbcore.contrib.geography.models import Geography
from wbcore.contrib.geography.serializers import GeographyModelSerializer
from wbcore.contrib.geography.viewsets import (
    GeographyModelViewSet,
    GeographyRepresentationViewSet,
)


@pytest.mark.django_db
@pytest.mark.with_db
class TestViewsets:
    @pytest.fixture
    def continents(self):
        return ContinentFactory.create_batch(3)

    @pytest.fixture
    def continent(self, continents):
        return continents[0]

    @pytest.fixture
    def continent_build(self):
        instance = ContinentFactory.build()
        return GeographyModelSerializer(instance).data

    @pytest.mark.parametrize("viewset", [GeographyModelViewSet, GeographyRepresentationViewSet])
    def test_get(self, viewset, request_factory, super_user, continents):
        # Arrange
        request = request_factory.get("")
        request.user = super_user
        viewset = viewset.as_view({"get": "list"})
        # Act
        response = viewset(request)
        # Assert
        assert len(response.data["results"]) == 3
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("viewset", [GeographyModelViewSet, GeographyRepresentationViewSet])
    def test_retrieve(self, viewset, request_factory, super_user, continent):
        # Arrange
        request = request_factory.get("")
        request.user = super_user
        viewset = viewset.as_view({"get": "retrieve"})
        # Act
        response = viewset(request, pk=continent.id)
        instance = response.data.get("instance")
        # Assert
        assert instance is not None
        assert instance["id"] == continent.id
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, request_factory, super_user, continent_build):
        # Arrange
        request = request_factory.post("", data=continent_build, format="json")
        request.user = super_user
        viewset = GeographyModelViewSet.as_view({"post": "create"})
        # Act
        response = viewset(request)
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete(self, request_factory, super_user, continents):
        # Arrange
        entry_id = continents[1].id
        request = request_factory.delete("", args=entry_id)
        request.user = super_user
        viewset = GeographyModelViewSet.as_view({"delete": "destroy"})
        # Act
        response = viewset(request, pk=entry_id)
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Geography.objects.count() == 2
        assert not Geography.objects.filter(id=entry_id).exists()

    def test_put(self, request_factory, super_user, continent, continent_build):
        # Arrange
        continent_build["id"] = continent.id
        request = request_factory.put("", data=continent_build, format="json")
        request.user = super_user
        viewset = GeographyModelViewSet.as_view({"put": "update"})
        # Act
        response = viewset(request, pk=continent.id)
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, request_factory, super_user, continent):
        # Arrange
        new_field_data = "Foo Bar"
        request = request_factory.patch("", data={"name": new_field_data})
        request.user = super_user
        viewset = GeographyModelViewSet.as_view({"patch": "partial_update"})
        # Act
        response = viewset(request, pk=continent.id)
        continent.refresh_from_db()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert continent.name == new_field_data

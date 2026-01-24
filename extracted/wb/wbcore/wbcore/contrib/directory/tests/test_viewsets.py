import json

import pytest
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.factories import SuperUserFactory, UserFactory
from wbcore.contrib.authentication.models import User
from wbcore.contrib.directory.models import ClientManagerRelationship
from wbcore.test.utils import (
    get_data_from_factory,
    get_kwargs,
    get_model_factory,
)

from ..factories import (
    AddressContactFactory,
    ClientManagerRelationshipFactory,
    CompanyFactory,
    CustomerStatusFactory,
    EntryFactory,
    PersonFactory,
    SocialMediaContactFactory,
)
from ..models import Person
from ..viewsets import (
    AddressContactEntryViewSet,
    BankingContactEntryViewSet,
    ClientManagerViewSet,
    CompanyModelViewSet,
    CompanyRepresentationViewSet,
    CompanyTypeModelViewSet,
    CustomerStatusModelViewSet,
    EmailContactEntryViewSet,
    EntryModelViewSet,
    EntryRepresentationViewSet,
    PersonModelViewSet,
    PersonRepresentationViewSet,
    PositionModelViewSet,
    RelationshipModelViewSet,
    RelationshipTypeModelViewSet,
    SocialMediaContactEntryViewSet,
    SpecializationModelViewSet,
    TelephoneContactEntryViewSet,
    UserIsClientViewSet,
    UserIsManagerViewSet,
    WebsiteContactEntryViewSet,
)


@pytest.fixture
def super_user() -> User:
    return SuperUserFactory()


@pytest.fixture
def normal_user() -> User:
    return UserFactory(is_active=True, is_superuser=False)


@pytest.fixture
def api_request_factory() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestEntryModelViewSet:
    @pytest.fixture
    def entry_data(self) -> dict[str, object]:
        social_media = SocialMediaContactFactory()
        address = AddressContactFactory()
        data = model_to_dict(EntryFactory.build(), exclude=["profile_image", "signature"])
        data["social_media"] = [social_media.id]
        data["addresses"] = [address.id]
        return data

    @pytest.fixture
    def person_data(self) -> dict[str, object]:
        address = AddressContactFactory()
        data = model_to_dict(PersonFactory.build(), exclude=["profile_image", "signature"])
        data["addresses"] = [address.id]
        return data

    @pytest.fixture
    def company_data(self) -> dict[str, object]:
        address = AddressContactFactory()
        customer_status = CustomerStatusFactory()
        data = model_to_dict(CompanyFactory.build(), exclude=["profile_image", "signature"])
        data["addresses"] = [address.id]
        data["customer_status"] = customer_status.id
        data["employees"] = []
        return data

    @pytest.mark.parametrize(
        "mvs, fixture_name",
        [
            (EntryModelViewSet, "entry_data"),
            (PersonModelViewSet, "person_data"),
            (CompanyModelViewSet, "company_data"),
        ],
    )
    def test_create_entry(
        self,
        request: pytest.FixtureRequest,
        mvs: EntryModelViewSet,
        fixture_name: str,
        api_request_factory: APIRequestFactory,
        super_user: User,
    ):
        # Arrange
        data: dict[str, object] = request.getfixturevalue(fixture_name)
        wsgi_request = api_request_factory.post("", data, format="json")
        wsgi_request.user = super_user
        vs = mvs.as_view({"post": "create"})
        # Act
        response = vs(wsgi_request)
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "mvs, factory",
        [
            (EntryModelViewSet, EntryFactory),
            (PersonModelViewSet, PersonFactory),
            (CompanyModelViewSet, CompanyFactory),
        ],
    )
    def test_get_entry(
        self,
        mvs: EntryModelViewSet,
        factory,
        api_request_factory: APIRequestFactory,
        super_user: User,
    ):
        # Arrange
        entry = factory()
        wsgi_request = api_request_factory.get("")
        wsgi_request.user = super_user
        vs = mvs.as_view({"get": "retrieve"})
        # Act
        response = vs(wsgi_request, pk=entry.pk)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert not response.data.get("results")
        assert response.data["instance"]["id"] == entry.id

    @pytest.mark.parametrize(
        "mvs, factory",
        [
            (EntryModelViewSet, EntryFactory),
            (PersonModelViewSet, PersonFactory),
            (CompanyModelViewSet, CompanyFactory),
        ],
    )
    def test_get_entry_list(
        self,
        mvs: EntryModelViewSet,
        factory,
        api_request_factory: APIRequestFactory,
        super_user: User,
    ):
        # Arrange
        factory.create_batch(3)
        wsgi_request = api_request_factory.get("")
        wsgi_request.user = super_user
        vs = mvs.as_view({"get": "list"})
        # Act
        response = vs(wsgi_request)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert not response.data.get("instance")

    @pytest.mark.parametrize(
        "mvs, factory",
        [
            (EntryModelViewSet, EntryFactory),
            (PersonModelViewSet, PersonFactory),
            (CompanyModelViewSet, CompanyFactory),
        ],
    )
    def test_delete_instance(
        self,
        mvs: EntryModelViewSet,
        factory,
        api_request_factory: APIRequestFactory,
        super_user: User,
    ):
        # Arrange
        model = mvs.get_model()
        entry = factory()
        wsgi_request = api_request_factory.delete("")
        wsgi_request.user = super_user
        vs = mvs.as_view({"delete": "destroy"})
        # Act
        response = vs(wsgi_request, pk=entry.pk)
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not model.objects.filter(id=entry.id).exists()

    @pytest.mark.parametrize(
        "mvs, factory, fixture_name",
        [
            (EntryModelViewSet, EntryFactory, "entry_data"),
            (PersonModelViewSet, PersonFactory, "person_data"),
            (CompanyModelViewSet, CompanyFactory, "company_data"),
        ],
    )
    def test_update_instance(
        self,
        request: pytest.FixtureRequest,
        mvs: EntryModelViewSet,
        factory,
        fixture_name: str,
        api_request_factory: APIRequestFactory,
        super_user: User,
    ):
        # Arrange
        entry = factory()
        new_salutation = entry.salutation + "Foo Bar"
        new_data: dict[str, object] = request.getfixturevalue(fixture_name)
        new_data["id"] = entry.id
        # We check for salutation, because it is a field in all 3 tested models
        new_data["salutation"] = new_salutation
        wsgi_request = api_request_factory.put("", data=new_data, format="json")
        wsgi_request.user = super_user
        vs = mvs.as_view({"put": "update"})
        # Act
        response = vs(wsgi_request, pk=entry.pk)
        instance = response.data.get("instance")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert instance["id"] == entry.id
        assert instance["salutation"] == new_salutation
        assert instance["salutation"] != entry.salutation

    @pytest.mark.parametrize(
        "mvs, factory",
        [
            (EntryModelViewSet, EntryFactory),
            (PersonModelViewSet, PersonFactory),
            (CompanyModelViewSet, CompanyFactory),
        ],
    )
    def test_patch_instance(
        self,
        mvs: EntryModelViewSet,
        factory,
        api_request_factory: APIRequestFactory,
        super_user: User,
    ):
        # Arrange
        entry = factory()
        wsgi_request = api_request_factory.patch("", data={"salutation": "Foo Bar"})
        wsgi_request.user = super_user
        vs = mvs.as_view({"patch": "partial_update"})
        # Act
        response = vs(wsgi_request, pk=entry.id)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["salutation"] == "Foo Bar"

    @pytest.mark.parametrize(
        "viewset, factory",
        [
            (EntryRepresentationViewSet, EntryFactory),
            (PersonRepresentationViewSet, PersonFactory),
            (CompanyRepresentationViewSet, CompanyFactory),
        ],
    )
    def test_get_entry_representation_unauthorized(self, api_request_factory, viewset, factory):
        # Arrange
        entry = factory()
        wsgi_request = api_request_factory.get("")
        wsgi_request.user = UserFactory(is_active=True, is_superuser=False)
        kwargs = get_kwargs(entry, viewset, wsgi_request)
        vs = viewset.as_view({"get": "list"})
        # Act
        response = vs(wsgi_request, **kwargs)
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN


# # =====================================================================================================================
# #                                                  TESTING UTILS VIEWSETS
# # =====================================================================================================================


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestUtilsViewSets:
    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_get_utils(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        factory.create_batch(3)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_retrieve_utils(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_post_utils(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        super_user = super_user
        data = get_data_from_factory(obj, mvs, superuser=super_user, delete=True)
        request = api_request_factory.post("", data=data)
        request.user = super_user
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_delete_utils(self, api_request_factory, super_user, mvs):
        request = api_request_factory.delete("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"delete": "destroy"})
        response = vs(request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_put_utils(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        old_obj = factory()
        new_obj = factory()
        user = super_user
        data = get_data_from_factory(new_obj, mvs, superuser=user, delete=True)
        request = api_request_factory.put("", data=data)
        request.user = user
        vs = mvs.as_view({"put": "update"})
        response = vs(request, pk=old_obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == new_obj.title
        assert not response.data["instance"]["title"] == old_obj.title

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_patch_utils(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        request = api_request_factory.patch("", data={"title": "New Title"})
        request.user = super_user
        vs = mvs.as_view({"patch": "partial_update"})
        response = vs(request, pk=obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == "New Title"


# =====================================================================================================================
#                                                  TESTING RELATIONSHIP VIEWSETS
# =====================================================================================================================


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestRelationshipViewSets:
    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_retrieve(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        type = factory()
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=type.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_get(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        factory.create_batch(3)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 6
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_put(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        old_type = factory()
        non_counter_type = factory(counter_relationship=None)
        new_type = factory()
        new_type.counter_relationship = non_counter_type
        user = super_user
        data = get_data_from_factory(new_type, mvs, superuser=user, delete=True)
        request = api_request_factory.put("", data=data)
        request.user = user
        vs = mvs.as_view({"put": "update"})
        response = vs(request, pk=old_type.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == new_type.title
        assert not response.data["instance"]["title"] == old_type.title
        assert response.data["instance"]["counter_relationship"] == new_type.counter_relationship.id

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_delete(self, api_request_factory, super_user, mvs):
        request = api_request_factory.delete("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        type = factory()
        vs = mvs.as_view({"delete": "destroy"})
        response = vs(request, pk=type.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_patch(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        type = factory()
        request = api_request_factory.patch("", data={"title": "New Title"})
        request.user = super_user
        vs = mvs.as_view({"patch": "partial_update"})
        response = vs(request, pk=type.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == "New Title"

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_post(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        type = factory(counter_relationship=None)
        user = super_user
        data = get_data_from_factory(type, mvs, superuser=user, delete=True)
        json_data = json.dumps(data)
        request = api_request_factory.post("", data=json_data, content_type="application/json")
        request.user = user
        kwargs = get_kwargs(type, mvs, request)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED

    def test_relationship_list(
        self,
        api_request_factory,
        super_user,
        relationship_factory,
        relationship_type_factory,
    ):
        # Arrange
        relationship_type = relationship_type_factory(counter_relationship=None)
        request = api_request_factory.get("")
        request.user = super_user

        relationship_factory.create_batch(3, relationship_type=relationship_type)
        view = RelationshipModelViewSet.as_view({"get": "list"})
        # Act
        response = view(request).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("results")
        assert len(response.data["results"]) == 3 * 2

    def test_relationship_retrieve(self, api_request_factory, super_user, relationship_factory):
        # Arrange
        relationship = relationship_factory()
        request = api_request_factory.get("")
        request.user = super_user
        view = RelationshipModelViewSet.as_view({"get": "retrieve"})
        # Act
        response = view(request, pk=relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)["instance"]["from_entry"] == relationship.from_entry.id
        assert json.loads(response.content)["instance"]["to_entry"] == relationship.to_entry.id
        assert json.loads(response.content)["instance"]["relationship_type"] == relationship.relationship_type.id

    def test_relationship_delete(self, api_request_factory, super_user, relationship_factory):
        # Arrange
        relationship = relationship_factory()
        request = api_request_factory.delete("")
        request.user = super_user
        view = RelationshipModelViewSet.as_view({"delete": "destroy"})
        # Act
        response = view(request, pk=relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_relationship_create(self, api_request_factory, super_user, relationship_factory):
        # Arrange
        relationship = relationship_factory()
        user = super_user
        data = get_data_from_factory(relationship, RelationshipModelViewSet, superuser=user)
        request = api_request_factory.post("", data=data)
        request.user = user
        kwargs = get_kwargs(relationship, RelationshipModelViewSet, request=request, data=data)
        view = RelationshipModelViewSet.as_view({"post": "create"})
        # Act
        response = view(request, kwargs).render()
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_relationship_update(self, api_request_factory, super_user, relationship_factory):
        # Arrange
        old_relationship = relationship_factory()
        new_relationship = relationship_factory()
        user = super_user
        data = get_data_from_factory(new_relationship, RelationshipModelViewSet, superuser=user)
        request = api_request_factory.put("", data=data)
        request.user = user
        view = RelationshipModelViewSet.as_view({"put": "update"})
        # Act
        response = view(request, pk=old_relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_relationship_partial_update(self, api_request_factory, super_user, relationship_factory, person_factory):
        # Arrange
        relationship = relationship_factory()
        new_person = person_factory()
        request = api_request_factory.patch("", data={"to_entry": new_person.id})
        request.user = super_user
        view = RelationshipModelViewSet.as_view({"patch": "partial_update"})
        # Act
        response = view(request, pk=relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["to_entry"] == new_person.id


# =====================================================================================================================
#                                                  TESTING CLIENT MANAGER VIEWSETS
# =====================================================================================================================


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestClientManagerViewSet:
    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_none_qs(self, api_request_factory, normal_user, mvs):
        request = api_request_factory.get("")
        request.user = normal_user
        obj = ClientManagerRelationshipFactory()
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"get": "list"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_delete(self, api_request_factory, super_user, mvs):
        request = api_request_factory.delete("")
        request.user = super_user
        obj1 = ClientManagerRelationshipFactory()
        obj2 = ClientManagerRelationshipFactory(client=obj1.client, status=ClientManagerRelationship.Status.DRAFT)
        view = mvs.as_view({"delete": "destroy"})
        response = view(request, pk=obj2.id).render()
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_get(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        ClientManagerRelationshipFactory.create_batch(3)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_retrieve(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        obj = ClientManagerRelationshipFactory()
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.pk)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_put(self, api_request_factory, super_user, mvs):
        obj_old = ClientManagerRelationshipFactory(status=ClientManagerRelationship.Status.DRAFT)
        obj_new = ClientManagerRelationshipFactory()
        user = super_user
        data = get_data_from_factory(obj_new, mvs, superuser=user, delete=True)
        request = api_request_factory.put("", data=data)
        request.user = user
        kwargs = get_kwargs(obj_old, mvs, request, data)
        vs = mvs.as_view({"put": "update"})
        response = vs(request, pk=obj_old.id, **kwargs).render()
        assert response.status_code == status.HTTP_200_OK
        assert not obj_old.client == obj_new.client
        assert response.data["instance"]["id"] == obj_old.id
        assert response.data["instance"]["client"] == obj_new.client.id
        assert not response.data["instance"]["client"] == obj_old.client.id

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_post(self, api_request_factory, super_user, mvs):
        cmr = ClientManagerRelationshipFactory()
        user = super_user
        data = get_data_from_factory(cmr, mvs, delete=True, superuser=user)
        request = api_request_factory.post("", data=data)
        request.user = user
        kwargs = {}
        view = mvs.as_view({"post": "create"})
        response = view(request, kwargs).render()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("instance")
        assert response.data["instance"]["client"] == cmr.client.id


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestUserIsClientViewSet:
    @pytest.mark.parametrize("mvs", [UserIsClientViewSet])
    def test_get(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        obj = PersonFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=user, relationship_manager=obj)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 1
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsClientViewSet])
    def test_retrieve(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        user = Person.get_or_create_with_user(request.user)
        rel = ClientManagerRelationshipFactory(client=user)
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=rel.pk)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsClientViewSet])
    def test_delete(self, api_request_factory, super_user, mvs):
        request = api_request_factory.delete("")
        request.user = super_user
        obj = PersonFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=user, relationship_manager=obj)
        view = mvs.as_view({"delete": "destroy"})
        with pytest.raises(AttributeError):
            view(request, pk=obj.id).render()


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestUserIsManagerViewSet:
    @pytest.mark.parametrize("mvs", [UserIsManagerViewSet])
    def test_get(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        obj = EntryFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=obj, relationship_manager=user)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 1
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsManagerViewSet])
    def test_retrieve(self, api_request_factory, super_user, mvs):
        request = api_request_factory.get("")
        request.user = super_user
        obj = EntryFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=obj, relationship_manager=user)
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.pk)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsManagerViewSet])
    def test_delete(self, api_request_factory, super_user, mvs):
        request = api_request_factory.delete("")
        request.user = super_user
        obj = EntryFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=obj, relationship_manager=user)
        view = mvs.as_view({"delete": "destroy"})
        response = view(request, pk=obj.id).render()
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.with_db
@pytest.mark.viewset_tests
@pytest.mark.django_db
class TestContactViewsets:
    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
            SocialMediaContactEntryViewSet,
        ],
    )
    def test_get_propagated_contact(self, api_request_factory, super_user, mvs, internal_user_factory):
        request = api_request_factory.get("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        obj = factory(entry=internal_user_factory().profile)
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"get": "list"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        assert response.data.get("results")

    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
            SocialMediaContactEntryViewSet,
        ],
    )
    def test_post_delete_contact(self, api_request_factory, super_user, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        user = super_user
        data = get_data_from_factory(obj, mvs, delete=True, superuser=user)
        request = api_request_factory.post("", data)
        request.user = user
        kwargs = get_kwargs(obj, mvs, request=request, data=data)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("instance")

    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
            SocialMediaContactEntryViewSet,
        ],
    )
    def test_primary_deleteendpointmixin(self, api_request_factory, super_user, mvs):
        request = api_request_factory.delete("")
        request.user = super_user
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        obj.primary = False
        obj.save()
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"delete": "destroy_multiple"})
        response = vs(request=request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

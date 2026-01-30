import pytest
from dynamic_preferences.registries import global_preferences_registry
from faker import Faker
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.authentication.models import Permission, User
from wbcore.contrib.directory.models import Entry

from ..factories import (
    BankFactory,
    ClientManagerRelationshipFactory,
    EmployerEmployeeRelationshipFactory,
    PersonFactory,
)
from ..viewsets import (
    CompanyModelViewSet,
    CompanyRepresentationViewSet,
    EntryModelViewSet,
    EntryRepresentationViewSet,
    PersonModelViewSet,
    PersonRepresentationViewSet,
)

fake = Faker()


@pytest.mark.django_db
class TestEntryPermissionQueryset:
    @pytest.fixture
    def entry_fixtures(self):
        """
        Construct the different entries and theirs relationships to the base user
        """
        # True, we create a superuser
        user = UserFactory.create()

        any_person = PersonFactory.create()
        any_company = BankFactory.create()

        employer = EmployerEmployeeRelationshipFactory.create(employee=user.profile).employer
        colleague = EmployerEmployeeRelationshipFactory.create(employer=employer).employee
        client = ClientManagerRelationshipFactory.create(relationship_manager=user.profile).client

        return (
            user,
            User.objects.get(email="AnonymousUser").profile,
            any_person,
            any_company,
            employer,
            colleague,
            client,
        )

    def test_filter_for_internal_user(self, entry_fixtures):
        """
        Test that internal user can see everything
        """
        user, anonymous_profile, any_person, any_company, employer, colleague, client = entry_fixtures
        user.is_internal = True
        user.save()

        assert set(Entry.objects.filter_for_user(user)) == {
            user.profile.entry_ptr,
            anonymous_profile.entry_ptr,
            any_person.entry_ptr,
            any_company.entry_ptr,
            employer.entry_ptr,
            colleague.entry_ptr,
            client,
        }

    def test_filter_for_normal_user(self, entry_fixtures):
        """
        Test that external/normal user can see:
        - Its own profile
        - Its employer
        - Their colleagues
        - Their clients
        """
        user, anonymous_profile, any_person, any_company, employer, colleague, client = entry_fixtures
        global_preferences_registry.manager()["directory__main_company"] = employer.id

        assert set(Entry.objects.filter_for_user(user)) == {
            user.profile.entry_ptr,
            employer.entry_ptr,
            colleague.entry_ptr,
            client,
        }

    @pytest.mark.parametrize(
        "viewset_class",
        [
            EntryModelViewSet,
            EntryRepresentationViewSet,
            CompanyModelViewSet,
            CompanyRepresentationViewSet,
            PersonModelViewSet,
            PersonRepresentationViewSet,
        ],
    )
    def test_ensure_permission_for_user_on_entry_viewsets(self, entry_fixtures, viewset_class):
        user, anonymous_profile, any_person, any_company, employer, colleague, client = entry_fixtures

        request = APIRequestFactory().get("")
        request.user = user
        viewset = viewset_class(request=request)
        viewset.kwargs = dict()

        # assert for any non employee user
        assert set(viewset.get_queryset()) == set(viewset.model.objects.filter_for_user(user))

        # test for external employee
        global_preferences_registry.manager()["directory__main_company"] = employer.id
        assert set(viewset.get_queryset()) == set(viewset.model.objects.filter_for_user(user))

        # test for internal user
        user.user_permissions.add(
            Permission.objects.get(content_type__app_label="authentication", codename="is_internal_user")
        )
        assert set(viewset.get_queryset()) == set(viewset.model.objects.filter_for_user(user))

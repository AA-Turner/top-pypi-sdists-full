import pytest
from django.db import models
from django_fsm import TransitionNotAllowed
from dynamic_preferences.registries import global_preferences_registry
from pytest_mock import MockerFixture

from wbcore.contrib.authentication.factories import InternalUserFactory
from wbcore.contrib.directory.factories import ClientManagerRelationshipFactory as CMRF
from wbcore.contrib.directory.factories import (
    CompanyFactory,
    EmailContactFactory,
    EntryFactory,
    PersonFactory,
    TelephoneContactFactory,
)
from wbcore.contrib.directory.models import ClientManagerRelationship as CMR
from wbcore.contrib.directory.models import (
    Company,
    EmailContact,
    Entry,
    Person,
    RelationshipType,
    TelephoneContact,
)
from wbcore.contrib.directory.models.entries import handle_user_deactivation


@pytest.fixture
def test_person():
    return PersonFactory()


@pytest.mark.directory_model_tests
class TestSpecificModelContacts:
    def refresh_from_db(self, model_entries: list[models.Model]) -> None:
        for entry in model_entries:
            entry.refresh_from_db()

    @pytest.fixture
    def test_entry(self):
        return EntryFactory()

    @pytest.fixture
    def test_company(self):
        return CompanyFactory()

    @pytest.mark.with_db
    @pytest.mark.django_db
    @pytest.mark.parametrize("is_primary, has_duplicates", [(a, b) for a in [True, False] for b in [True, False]])
    def test_set_entry_primary_telephone(self, is_primary, has_duplicates, test_entry):
        # Arrange
        telephone_contact_a = TelephoneContactFactory(entry=test_entry, primary=is_primary)
        telephone_contact_b = TelephoneContactFactory(entry=test_entry if has_duplicates else None)
        # Act
        TelephoneContact.set_entry_primary_telephone(test_entry, telephone_contact_b.number)
        self.refresh_from_db([telephone_contact_a, telephone_contact_b])
        # Assert
        if has_duplicates:
            assert test_entry.telephones.get(primary=True) == telephone_contact_b
            assert not telephone_contact_a.primary
            assert telephone_contact_b.primary
        elif is_primary:
            assert test_entry.telephones.get(primary=True).number == telephone_contact_b.number
        else:
            number_b = telephone_contact_b.number
            assert TelephoneContact.objects.filter(entry=test_entry, number=number_b, primary=True).exists()

    @pytest.mark.with_db
    @pytest.mark.django_db
    @pytest.mark.parametrize("is_primary, has_duplicates", [(a, b) for a in [True, False] for b in [True, False]])
    def test_set_entry_primary_email(self, is_primary, has_duplicates, test_entry):
        # Arrange
        email_contact_a = EmailContactFactory(entry=test_entry, primary=is_primary)
        email_contact_b = EmailContactFactory(entry=test_entry if has_duplicates else None)
        # Act
        EmailContact.set_entry_primary_email(test_entry, email_contact_b.address)
        self.refresh_from_db([email_contact_a, email_contact_b])
        # Assert
        if has_duplicates:
            assert test_entry.emails.get(primary=True) == email_contact_b
            assert not email_contact_a.primary
            assert email_contact_b.primary
        elif is_primary:
            assert test_entry.emails.get(primary=True).address == email_contact_b.address
        else:
            address_b = email_contact_b.address
            assert EmailContact.objects.filter(entry=test_entry, address=address_b, primary=True).exists()

    @pytest.mark.with_db
    @pytest.mark.django_db
    @pytest.mark.parametrize("with_contact", (True, False))
    def test_get_primary_contact_with_db(self, with_contact: bool, test_entry):
        contact = EmailContactFactory(entry=test_entry if with_contact else None, primary=True)
        result = test_entry._primary_contact(test_entry.emails)
        assert result == contact if with_contact else result is None

    @pytest.mark.parametrize(
        "contact_method, contact_model",
        [
            ("primary_email_contact", "emails"),
            ("primary_telephone_contact", "telephones"),
            ("primary_address_contact", "addresses"),
            ("primary_website_contact", "websites"),
            ("primary_banking_contact", "banking"),
        ],
    )
    def test_get_primary_contact(self, mocker: MockerFixture, contact_method, contact_model):
        # Arrange
        entry = Entry()
        mock_contact_property = mocker.patch(
            f"wbcore.contrib.directory.models.Entry.{contact_model}", new_callable=mocker.PropertyMock
        )
        mock_contact_property.return_value.get.return_value.primary = True
        # Act
        method = getattr(entry, contact_method)()
        method()
        # Assert
        mock_contact_property.return_value.get.assert_called_once_with(primary=True)

    @pytest.mark.with_db
    @pytest.mark.django_db
    def test_get_casted_entry(self, test_person, test_company):
        # Arrange
        company_entry = Entry.objects.get(id=test_company.id)
        person_entry = Entry.objects.get(id=test_person.id)
        # Act
        casted_company_entry = company_entry.get_casted_entry()
        casted_company = test_company.get_casted_entry()
        casted_person_entry = person_entry.get_casted_entry()
        # Assert
        assert casted_company_entry == test_company
        assert casted_company == test_company
        assert casted_person_entry == test_person

    def test_delete_additional_fields(self):
        # Arrange
        entry = Entry()
        # Act
        entry.additional_fields["special_key"] = "additional fields special key"
        entry.delete_additional_fields("special_key")
        # Assert
        assert "special_key" not in entry.additional_fields.keys()

    def test_full_name(self, mocker: MockerFixture):
        # Arrange
        first_name = "Foo"
        last_name = "Bar"
        person = Person()
        mocker.patch.object(person, "first_name", first_name)
        mocker.patch.object(person, "last_name", last_name)
        # Assert
        assert person.full_name == f"{last_name} {first_name}"

    @pytest.mark.with_db
    @pytest.mark.django_db
    @pytest.mark.parametrize("with_employer", [True, False])
    def test_str_full(self, with_employer, test_person, test_company, mocker: MockerFixture):
        # Arrange
        name = f"{test_person.first_name} {test_person.last_name}"
        if with_employer:
            company_name = test_company.name
            test_person.employers.add(test_company)
            name += f'{(" (%s)" % company_name)}'
        # Assert
        assert test_person.str_full() == name

    @pytest.mark.with_db
    @pytest.mark.django_db
    def test_soft_deleted_entry_dont_show_in_queryset(self, company_factory, person_factory):
        "ensure the default queryset filter out soft deleted entries"
        person = person_factory.create()
        assert set(Person.objects.all()) == {person}
        person.delete()
        assert not Person.objects.exists()
        company = company_factory.create()
        assert set(Company.objects.all()) == {company}
        company.delete()
        assert not Company.objects.exists()

    @pytest.mark.with_db
    @pytest.mark.django_db
    def test_soft_deleted_person_doesnt_crash_user_registration(self, user_factory, email_contact_factory):
        user = user_factory(profile=None)
        email_contact_factory(address=user.email, entry__is_active=False)
        assert Person.get_or_create_with_user(user)


@pytest.mark.with_db
@pytest.mark.django_db
@pytest.mark.directory_model_tests
class TestUserDeactivation:
    @pytest.fixture
    def test_internal_profile(self):
        return InternalUserFactory().profile

    def test_main_company_removed_from_deactivated_user(self, test_internal_profile):
        # Arrange
        main_company_id = global_preferences_registry.manager()["directory__main_company"]
        main_company = Company.objects.get(id=main_company_id)
        message = handle_user_deactivation(sender=None, instance=test_internal_profile, substitute_profile=None)[0]
        # Assert
        assert message == f"Removed {main_company.computed_str} from {test_internal_profile.computed_str}'s employers"
        assert main_company not in test_internal_profile.employers.all()

    def test_no_substitute_person(self, test_internal_profile):
        # Arrange
        relationship = CMRF(relationship_manager=test_internal_profile)
        # Act
        handle_user_deactivation(sender=None, instance=test_internal_profile, substitute_profile=None)
        # Assert
        assert CMR.objects.get(id=relationship.id).status == CMR.Status.REMOVED

    @pytest.mark.parametrize("exists", [True, False])
    def test_not_approved_substitute_relationships(self, test_internal_profile, test_person, exists):
        # Arrange
        old_relationship = CMRF(relationship_manager=test_internal_profile, status=CMR.Status.PENDINGADD)
        substitute_relationship = (
            CMRF(client=old_relationship.client, relationship_manager=test_person) if exists else None
        )
        # Act
        message = handle_user_deactivation(
            sender=None, instance=test_internal_profile, substitute_profile=test_person
        )[1]
        relationship_id = substitute_relationship.id if exists else old_relationship.id
        relationship_exists = CMR.objects.filter(id=old_relationship.id).exists()
        # Assert
        assert message == f"Assigned 1 manager role(s) to {test_person.computed_str}"
        assert (not relationship_exists) if exists else relationship_exists
        assert CMR.objects.get(id=relationship_id).client.id == old_relationship.client.id
        assert CMR.objects.get(id=relationship_id).relationship_manager.id == test_person.id

    def test_approved_with_substitute_relationships(self, test_internal_profile, test_person):
        # Arrange
        old_relationship = CMRF(relationship_manager=test_internal_profile, primary=True)
        CMRF(relationship_manager=test_internal_profile)
        substitute_relationship = CMRF(
            client=old_relationship.client, relationship_manager=test_person, status=CMR.Status.PENDINGADD
        )
        # Act
        message = handle_user_deactivation(
            sender=None, instance=test_internal_profile, substitute_profile=test_person
        )[1]
        substitute_relationship.refresh_from_db()
        # Assert
        assert message == f"Assigned 2 manager role(s) to {test_person.computed_str}"
        assert substitute_relationship.client.id == old_relationship.client.id
        assert substitute_relationship.relationship_manager.id == test_person.id
        assert substitute_relationship.status == CMR.Status.APPROVED
        assert substitute_relationship.primary is True

    def test_approved_without_substitute_relationships_needs_primary(self, test_internal_profile, test_person):
        # Arrange
        old_relationship = CMRF(relationship_manager=test_internal_profile, primary=True)
        # Act
        message = handle_user_deactivation(
            sender=None, instance=test_internal_profile, substitute_profile=test_person
        )[1]
        relationship_exists = CMR.objects.filter(
            relationship_manager=test_person, client=old_relationship.client, primary=True, status=CMR.Status.APPROVED
        ).exists()
        old_relationship.refresh_from_db()
        # Assert
        assert message == f"Assigned 1 manager role(s) to {test_person.computed_str}"
        assert relationship_exists
        assert old_relationship.status == CMR.Status.REMOVED

    def test_approved_without_substitute_relationships_doesnt_need_primary(self, test_internal_profile, test_person):
        # Arrange
        old_relationship = CMRF(relationship_manager=test_internal_profile)
        CMRF(client=old_relationship.client, primary=True)
        # Act
        message = handle_user_deactivation(
            sender=None, instance=test_internal_profile, substitute_profile=test_person
        )[1]
        relationship_exists = CMR.objects.filter(
            relationship_manager=test_person, client=old_relationship.client, primary=False, status=CMR.Status.APPROVED
        ).exists()
        old_relationship.refresh_from_db()
        # Assert
        assert message == f"Assigned 1 manager role(s) to {test_person.computed_str}"
        assert relationship_exists
        assert old_relationship.status == CMR.Status.REMOVED


@pytest.mark.directory_model_tests
class TestSpecificModelsClientManagerRelationship:
    @pytest.fixture
    def test_cmr(self):
        return CMR()

    @pytest.mark.parametrize(
        "method_name, initial_status, expected_status",
        [
            ("submit", CMR.Status.DRAFT, CMR.Status.PENDINGADD),
            ("deny", CMR.Status.PENDINGADD, CMR.Status.DRAFT),
            ("denyremoval", CMR.Status.PENDINGREMOVE, CMR.Status.APPROVED),
            ("approveremoval", CMR.Status.PENDINGREMOVE, CMR.Status.REMOVED),
            ("reinstate", CMR.Status.REMOVED, CMR.Status.PENDINGADD),
        ],
    )
    def test_status_transitions(self, test_cmr, mocker: MockerFixture, method_name, initial_status, expected_status):
        # Arrange
        mocker.patch.object(test_cmr, "status", initial_status)
        mocker.patch("django_fsm.transition", return_value=None)
        # Act
        method = getattr(test_cmr, method_name)
        method()
        # Assert
        assert test_cmr.status == expected_status

    # @pytest.mark.parametrize("method_name", ["approve", "mngapprove"])
    # @pytest.mark.parametrize("is_primary", [True, False])
    # def test_approval_methods(self, client_manager_relationship_factory, method_name, is_primary):
    #     # Arrange
    #     status = CMR.Status.PENDINGADD if method_name == "approve" else CMR.Status.DRAFT
    #     test_cmr = client_manager_relationship_factory.create(status=status, primary=False)
    #     # Act
    #     method = getattr(test_cmr, method_name)
    #     method()
    #     test_cmr.save() # we need to call save because the logic of handling primary happens in the parent save method (primarymixin)
    #     # Assert
    #     assert test_cmr.status == CMR.Status.APPROVED
    #     assert test_cmr.primary

    @pytest.mark.parametrize("is_primary", [True, False])
    def test_make_primary(self, is_primary, test_cmr, mocker: MockerFixture):
        # Arrange
        mocker.patch.object(test_cmr, "primary", is_primary)
        mocker.patch.object(test_cmr, "status", CMR.Status.APPROVED)
        mocker.patch("django_fsm.transition", return_value=None)
        # Act & Assert
        if is_primary:
            with pytest.raises(TransitionNotAllowed):
                test_cmr.makeprimary()
                assert test_cmr.status == CMR.Status.APPROVED
        else:
            test_cmr.makeprimary()
            assert test_cmr.status == CMR.Status.PENDINGADD
        assert test_cmr.primary

    @pytest.mark.parametrize("is_primary", [True, False])
    @pytest.mark.parametrize("exists", [True, False])
    def test_remove(self, test_cmr, is_primary, exists, mocker: MockerFixture):
        # Arrange
        mock_path = "wbcore.contrib.directory.models.ClientManagerRelationship"
        mock_queryset = mocker.MagicMock()
        mock_queryset.filter.return_value.exists.return_value = exists
        mock_exclude = mocker.patch(f"{mock_path}.objects.exclude")
        mock_exclude.return_value = mock_queryset
        mocker.patch(f"{mock_path}.client", new_callable=mocker.PropertyMock)  # Mock client property
        mocker.patch.object(test_cmr, "primary", is_primary)
        mocker.patch.object(test_cmr, "status", CMR.Status.APPROVED)
        mocker.patch("django_fsm.transition", return_value=None)
        # Act & Assert
        if not is_primary and exists:
            test_cmr.remove()
            assert test_cmr.status == CMR.Status.PENDINGREMOVE
        else:
            with pytest.raises(TransitionNotAllowed):
                test_cmr.remove()
                assert test_cmr.status == CMR.Status.APPROVED


@pytest.mark.directory_model_tests
class TestSpecificModelsRelationships:
    def test_relationship_type_str(self, mocker: MockerFixture):
        # Arrange
        title = "Type"
        relationship_type = RelationshipType()
        mocker.patch.object(relationship_type, "title", title)
        # Act & Assert
        assert relationship_type.__str__() == title

    @pytest.mark.with_db
    @pytest.mark.django_db
    def test_relationship_str(self, relationship_factory, relationship_type_factory, person_factory):
        relationship_type = relationship_type_factory(
            title="Type",
            counter_relationship=None,
        )
        from_entry = person_factory(first_name="John", last_name="Doe")
        to_entry = person_factory(first_name="Jane", last_name="Doe")
        rel = relationship_factory(
            relationship_type=relationship_type,
            from_entry=from_entry,
            to_entry=to_entry,
        )
        assert rel.__str__() == "John Doe is Type of Jane Doe"

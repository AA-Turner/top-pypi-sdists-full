import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError
from schwifty import IBAN

from wbcore.contrib.directory.models import Entry, RelationshipType
from wbcore.contrib.directory.serializers import (
    AddressContactSerializer,
    BankingContactSerializer,
    ClientManagerModelSerializer,
    EmailContactSerializer,
    RelationshipTypeModelSerializer,
    RelationshipTypeRepresentationSerializer,
    TelephoneContactSerializer,
    WebsiteContactSerializer,
)

from ..factories import ClientManagerRelationshipFactory, PersonFactory


@pytest.mark.serializer_tests
class TestRelationshipTypeSerializers:
    @pytest.fixture
    def relationship_type(self, mocker: MockerFixture):
        relationship_type = RelationshipType()
        mocker.patch.object(relationship_type, "id", 1)
        mocker.patch.object(relationship_type, "title", "Test Type")
        return relationship_type

    @pytest.fixture
    def expected_data(self, relationship_type):
        return {"id": relationship_type.id, "title": relationship_type.title, "counter_relationship": None}

    def test_relationship_type_repr_serializer(self, mocker: MockerFixture, relationship_type, expected_data):
        serializer = RelationshipTypeRepresentationSerializer(instance=relationship_type)
        assert serializer.data == expected_data

    def test_relationship_type_model_serializer(self, mocker: MockerFixture, relationship_type, expected_data):
        serializer = RelationshipTypeModelSerializer(instance=relationship_type)
        expected_data["_counter_relationship"] = None
        assert serializer.data == expected_data


@pytest.mark.serializer_tests
@pytest.mark.with_db
@pytest.mark.django_db
class TestClientManagerSerializersNew:
    @pytest.fixture
    def manager(self):
        return PersonFactory()

    @pytest.fixture
    def client(self):
        return PersonFactory()

    @pytest.fixture
    def primary_cmr(self, manager, client):
        return ClientManagerRelationshipFactory(client=client, relationship_manager=manager, primary=True)

    def test_create_new_request(self, manager, client):
        """
        Validate method should not fail when given data for a new relationship.
        """
        data = {"client": client, "relationship_manager": manager}
        validated_data = ClientManagerModelSerializer().validate(data)
        assert validated_data == data

    def test_create_existing_request(self, primary_cmr):
        """
        Validate method should fail when given data for an already existing client manager relationship.
        """
        manager = primary_cmr.relationship_manager
        client = primary_cmr.client
        error_message = f"{manager} is already in charge of {client}."
        serializer = ClientManagerModelSerializer()
        data = {"client": client, "relationship_manager": manager, "primary": True}
        with pytest.raises(ValidationError) as exc_info:
            serializer.validate(data)
        assert exc_info.value.args[0]["non_field_errors"] == error_message

    def test_self_relationship_managers(self, manager):
        """
        Validate method should fail when client and manager are the same person.
        """
        serializer = ClientManagerModelSerializer()
        data = {"client": manager, "relationship_manager": manager}
        error_message = "Client and relationship manager cannot be the same person."
        with pytest.raises(ValidationError) as exc_info:
            serializer.validate(data)
        assert exc_info.value.args[0]["relationship_manager"] == error_message

    def test_degrade_primary_manager(self, primary_cmr):
        """
        Validate method should fail when trying to make primary manager non-primary.
        """
        manager = primary_cmr.relationship_manager
        client = primary_cmr.client
        serializer = ClientManagerModelSerializer()
        error_message = "Cannot degrade primary manager. Make a primary request for a different manager instead."
        data = {"client": client, "relationship_manager": manager, "primary": False}
        with pytest.raises(ValidationError) as exc_info:
            serializer.validate(data)
        assert exc_info.value.args[0]["primary"] == error_message


@pytest.mark.serializer_tests
class TestContactSerializersValidation:
    @pytest.fixture
    def iban(self):
        return IBAN("AD1400080001001234567890")

    @pytest.fixture
    def contact_data(self, mocker: MockerFixture):
        return {
            "AddressContact": {
                "serializer": AddressContactSerializer(),
                "data": {
                    "entry": mocker.MagicMock(spec=Entry),
                    "street": "Foo Str",
                    "street_additional": 5,
                    "zip": 22222,
                    "geography_city": "Bar City",
                },
                "error_message": "Address already in use",
                "key": "non_field_errors",
            },
            "BankingContact": {
                "serializer": BankingContactSerializer(),
                "data": {"iban": IBAN("AD1400080001001234567890"), "entry": mocker.MagicMock(spec=Entry)},
                "error_message": "IBAN already in use",
                "key": "iban",
            },
            "EmailContact": {
                "serializer": EmailContactSerializer(),
                "data": {"address": "foo@bar.com", "entry": mocker.MagicMock(spec=Entry)},
                "error_message": "E-Mail address already in use",
                "key": "address",
            },
            "TelephoneContact": {
                "serializer": TelephoneContactSerializer(),
                "data": {"number": 12345, "entry": mocker.MagicMock(spec=Entry)},
                "error_message": "Phone number already in use",
                "key": "number",
            },
            "WebsiteContact": {
                "serializer": WebsiteContactSerializer(),
                "data": {"url": "www.foo.bar", "entry": mocker.MagicMock(spec=Entry)},
                "error_message": "Website already in use",
                "key": "url",
            },
        }

    def _mock_qs(self, mocker: MockerFixture, path: str, exists=False) -> None:
        mock_filter = mocker.patch(f"{path}.objects.filter")
        mock_queryset = mocker.MagicMock()
        mock_filter.return_value = mock_queryset
        mock_queryset.exists.return_value = exists

    def test_create_invalid_email(self, mocker: MockerFixture):
        mock_path = "wbcore.contrib.directory.models.EmailContact"
        self._mock_qs(mocker, mock_path, False)
        serializer = EmailContactSerializer()
        data = {"address": "foobar.com"}
        with pytest.raises(ValidationError) as exc_info:
            serializer.validate(data)
        assert exc_info.value.args[0]["address"] == "Invalid e-mail address"

    def test_create_invalid_iban(self, mocker: MockerFixture):
        mock_path = "wbcore.contrib.directory.models.BankingContact"
        self._mock_qs(mocker, mock_path)
        serializer = BankingContactSerializer()
        data = {"entry": mocker.MagicMock(spec=Entry), "iban": "Invalid Iban"}
        with pytest.raises(ValidationError):
            serializer.validate(data)

    def test_create_invalid_bic(self, mocker: MockerFixture, iban):
        mock_path = "wbcore.contrib.directory.models.BankingContact"
        self._mock_qs(mocker, mock_path)
        serializer = BankingContactSerializer()
        data = {"entry": mocker.MagicMock(spec=Entry), "iban": iban, "swift_bic": "Invalid Bic"}
        with pytest.raises(ValidationError):
            serializer.validate(data)

    def test_invalid_phone_number(self, mocker: MockerFixture):
        mock_path = "wbcore.contrib.directory.models.TelephoneContact"
        self._mock_qs(mocker, mock_path)
        serializer = TelephoneContactSerializer()
        data = {"entry": mocker.MagicMock(spec=Entry), "number": "003A56"}
        with pytest.raises(ValidationError) as exc_info:
            serializer.validate(data)
        assert exc_info.value.args[0]["number"] == "Invalid phone number format"

    @pytest.mark.parametrize(
        "contact", ["AddressContact", "BankingContact", "EmailContact", "TelephoneContact", "WebsiteContact"]
    )
    def test_create_invalid_contact(self, contact, contact_data, mocker: MockerFixture):
        data = contact_data[contact]
        mock_path = f"wbcore.contrib.directory.models.{contact}"
        self._mock_qs(mocker, mock_path, True)
        with pytest.raises(ValidationError) as exc_info:
            data["serializer"].validate(data["data"])
        assert data["error_message"] in exc_info.value.args[0][data["key"]]

    @pytest.mark.parametrize(
        "serializer",
        [
            AddressContactSerializer(),
            BankingContactSerializer(),
            EmailContactSerializer(),
            TelephoneContactSerializer(),
            WebsiteContactSerializer(),
        ],
    )
    def test_create_without_data(self, serializer):
        data = {}
        validated_data = serializer.validate(data)
        assert data == validated_data

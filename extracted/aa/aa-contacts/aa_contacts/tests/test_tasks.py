from unittest.mock import patch
from django.test import TestCase

from esi.exceptions import HTTPNotModified

from app_utils.testdata_factories import UserMainFactory

from ..models import AllianceToken, AllianceContactLabel, AllianceContact, CorporationContact, CorporationContactLabel, CorporationToken
from ..tasks import update_alliance_contacts, update_corporation_contacts

from .utils import SimpleAttributeDict


class TestUpdateAllianceContacts(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserMainFactory()
        cls.alliance = user.profile.main_character.alliance
        token = user.token_set.first()

        cls.token = AllianceToken.objects.create(
            alliance=cls.alliance,
            token=token
        )

        cls.label_data = [
            SimpleAttributeDict({"label_id": 1, "label_name": "Test Label 1"}),
            SimpleAttributeDict({"label_id": 2, "label_name": "Test Label 2"}),
        ]

        cls.contact_data = [
            SimpleAttributeDict({
                "contact_id": 2,
                "contact_type": "corporation",
                'label_ids': [1, 2],
                'standing': 5.0
            }),
        ]

    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_token_doesnt_exist(self, mock_with_valid_tokens):
        mock_with_valid_tokens.return_value = AllianceToken.objects.all()

        self.token.delete()
        with self.assertRaises(ValueError):
            update_alliance_contacts(self.alliance.alliance_id)

    @patch("aa_contacts.tasks.AllianceContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.AllianceContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_ok(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = AllianceToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.return_value = self.label_data
        mock_get_contacts_data.return_value = self.contact_data

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 1)
        self.assertEqual(AllianceContactLabel.objects.count(), 2)

    @patch("aa_contacts.tasks.AllianceContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.AllianceContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_update(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = AllianceToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.return_value = self.label_data
        mock_get_contacts_data.return_value = self.contact_data

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 1)
        self.assertEqual(AllianceContactLabel.objects.count(), 2)

        self.label_data.pop()
        self.contact_data[0]['label_ids'].pop()

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 1)
        self.assertEqual(AllianceContactLabel.objects.count(), 1)

        mock_get_contacts_data.return_value = []

        contact = AllianceContact.objects.first()
        contact.notes = "Test"
        contact.save()

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 1)
        contact.refresh_from_db()
        self.assertEqual(contact.standing, 0.0)
        self.assertEqual(contact.labels.count(), 0)

        contact.notes = ""
        contact.save()

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 0)

    @patch("aa_contacts.tasks.AllianceContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.AllianceContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_labels_not_modified(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = AllianceToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.side_effect = HTTPNotModified(status_code=304, headers={})
        mock_get_contacts_data.return_value = self.contact_data

        AllianceContactLabel.objects.bulk_create([
            AllianceContactLabel(
                alliance=self.alliance,
                label_id=1,
                label_name="I am Groot 1",
            ),
            AllianceContactLabel(
                alliance=self.alliance,
                label_id=2,
                label_name="I am Groot 2",
            ),
            AllianceContactLabel(
                alliance=self.alliance,
                label_id=3,
                label_name="I am Groot 3",
            ),
        ])

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 1)
        self.assertEqual(AllianceContactLabel.objects.count(), 3)
        self.assertEqual(
            AllianceContactLabel.objects.get(alliance=self.alliance, label_id=1).label_name,
            "I am Groot 1"
        )
        self.assertEqual(
            AllianceContactLabel.objects.get(alliance=self.alliance, label_id=2).label_name,
            "I am Groot 2"
        )
        self.assertEqual(
            AllianceContactLabel.objects.get(alliance=self.alliance, label_id=3).label_name,
            "I am Groot 3"
        )

    @patch("aa_contacts.tasks.AllianceContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.AllianceContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_contacts_not_modified(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = AllianceToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.return_value = self.label_data
        mock_get_contacts_data.side_effect = HTTPNotModified(status_code=304, headers={})

        AllianceContact.objects.create(
            alliance=self.alliance,
            contact_id=3,
            contact_type="corporation",
            standing=3.0,
        )

        update_alliance_contacts(self.alliance.alliance_id)

        self.assertEqual(AllianceContact.objects.count(), 1)
        self.assertEqual(AllianceContactLabel.objects.count(), 2)

        contact = AllianceContact.objects.first()
        self.assertEqual(contact.contact_id, 3)

    @patch("aa_contacts.tasks.AllianceContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.AllianceContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_both_not_modified(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = AllianceToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.side_effect = HTTPNotModified(status_code=304, headers={})
        mock_get_contacts_data.side_effect = HTTPNotModified(status_code=304, headers={})

        label1 = AllianceContactLabel(
            alliance=self.alliance,
            label_id=1,
            label_name="I am Groot 1",
        )
        label1.save()

        label2 = AllianceContactLabel(
            alliance=self.alliance,
            label_id=2,
            label_name="I am Groot 2",
        )
        label2.save()

        label3 = AllianceContactLabel(
            alliance=self.alliance,
            label_id=3,
            label_name="I am Groot 3",
        )
        label3.save()

        contact: AllianceContact = AllianceContact(
            alliance=self.alliance,
            contact_id=3,
            contact_type="corporation",
            standing=3.0,
        )
        contact.save()
        contact.labels.add(label1, label2, label3)

        update_alliance_contacts(self.alliance.alliance_id)
        self.assertEqual(AllianceContact.objects.count(), 1)
        self.assertEqual(AllianceContactLabel.objects.count(), 3)
        self.assertEqual(
            AllianceContactLabel.objects.get(alliance=self.alliance, label_id=1).label_name,
            "I am Groot 1"
        )
        self.assertEqual(
            AllianceContactLabel.objects.get(alliance=self.alliance, label_id=2).label_name,
            "I am Groot 2"
        )
        self.assertEqual(
            AllianceContactLabel.objects.get(alliance=self.alliance, label_id=3).label_name,
            "I am Groot 3"
        )

        contact.refresh_from_db()
        self.assertEqual(contact.contact_id, 3)


class TestUpdateCorporationContacts(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserMainFactory()
        cls.corporation = user.profile.main_character.corporation
        token = user.token_set.first()

        cls.token = CorporationToken.objects.create(
            corporation=cls.corporation,
            token=token
        )

        cls.label_data = [
            SimpleAttributeDict({"label_id": 1, "label_name": "Test Label 1"}),
            SimpleAttributeDict({"label_id": 2, "label_name": "Test Label 2"}),
        ]

        cls.contact_data = [
            SimpleAttributeDict({
                "contact_id": 2,
                "contact_type": "alliance",
                'label_ids': [1, 2],
                'standing': 5.0
            }),
        ]

    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_token_doesnt_exist(self, mock_with_valid_tokens):
        mock_with_valid_tokens.return_value = CorporationToken.objects.all()

        self.token.delete()
        with self.assertRaises(ValueError):
            update_corporation_contacts(self.corporation.corporation_id)

    @patch("aa_contacts.tasks.CorporationContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.CorporationContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_ok(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = CorporationToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.return_value = self.label_data
        mock_get_contacts_data.return_value = self.contact_data

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 1)
        self.assertEqual(CorporationContactLabel.objects.count(), 2)

    @patch("aa_contacts.tasks.CorporationContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.CorporationContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_update(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = CorporationToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.return_value = self.label_data
        mock_get_contacts_data.return_value = self.contact_data

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 1)
        self.assertEqual(CorporationContactLabel.objects.count(), 2)

        self.label_data.pop()
        self.contact_data[0]['label_ids'].pop()

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 1)
        self.assertEqual(CorporationContactLabel.objects.count(), 1)

        mock_get_contacts_data.return_value = []

        contact = CorporationContact.objects.first()
        contact.notes = "Test"
        contact.save()

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 1)
        contact.refresh_from_db()
        self.assertEqual(contact.standing, 0.0)
        self.assertEqual(contact.labels.count(), 0)

        contact.notes = ""
        contact.save()

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 0)

    @patch("aa_contacts.tasks.CorporationContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.CorporationContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_labels_not_modified(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = CorporationToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.side_effect = HTTPNotModified(status_code=304, headers={})
        mock_get_contacts_data.return_value = self.contact_data

        CorporationContactLabel.objects.bulk_create([
            CorporationContactLabel(
                corporation=self.corporation,
                label_id=1,
                label_name="I am Groot 1",
            ),
            CorporationContactLabel(
                corporation=self.corporation,
                label_id=2,
                label_name="I am Groot 2",
            ),
            CorporationContactLabel(
                corporation=self.corporation,
                label_id=3,
                label_name="I am Groot 3",
            ),
        ])

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 1)
        self.assertEqual(CorporationContactLabel.objects.count(), 3)
        self.assertEqual(
            CorporationContactLabel.objects.get(corporation=self.corporation, label_id=1).label_name,
            "I am Groot 1"
        )
        self.assertEqual(
            CorporationContactLabel.objects.get(corporation=self.corporation, label_id=2).label_name,
            "I am Groot 2"
        )
        self.assertEqual(
            CorporationContactLabel.objects.get(corporation=self.corporation, label_id=3).label_name,
            "I am Groot 3"
        )

    @patch("aa_contacts.tasks.CorporationContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.CorporationContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_contacts_not_modified(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = CorporationToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.return_value = self.label_data
        mock_get_contacts_data.side_effect = HTTPNotModified(status_code=304, headers={})

        CorporationContact.objects.create(
            corporation=self.corporation,
            contact_id=3,
            contact_type="alliance",
            standing=3.0,
        )

        update_corporation_contacts(self.corporation.corporation_id)

        self.assertEqual(CorporationContact.objects.count(), 1)
        self.assertEqual(CorporationContactLabel.objects.count(), 2)

        contact = CorporationContact.objects.first()
        self.assertEqual(contact.contact_id, 3)

    @patch("aa_contacts.tasks.CorporationContactUpdater.get_labels_data")
    @patch("aa_contacts.tasks.CorporationContactUpdater.get_contacts_data")
    @patch("aa_contacts.tasks.group.delay")
    @patch("aa_contacts.models.ContactTokenQueryset.with_valid_tokens")
    def test_both_not_modified(self, mock_with_valid_tokens, mock_delay, mock_get_contacts_data, mock_get_labels_data):
        mock_with_valid_tokens.return_value = CorporationToken.objects.all()
        mock_delay.return_value = None

        mock_get_labels_data.side_effect = HTTPNotModified(status_code=304, headers={})
        mock_get_contacts_data.side_effect = HTTPNotModified(status_code=304, headers={})

        label1 = CorporationContactLabel(
            corporation=self.corporation,
            label_id=1,
            label_name="I am Groot 1",
        )
        label1.save()

        label2 = CorporationContactLabel(
            corporation=self.corporation,
            label_id=2,
            label_name="I am Groot 2",
        )
        label2.save()

        label3 = CorporationContactLabel(
            corporation=self.corporation,
            label_id=3,
            label_name="I am Groot 3",
        )
        label3.save()

        contact: CorporationContact = CorporationContact(
            corporation=self.corporation,
            contact_id=3,
            contact_type="alliance",
            standing=3.0,
        )
        contact.save()
        contact.labels.add(label1, label2, label3)

        update_corporation_contacts(self.corporation.corporation_id)
        self.assertEqual(CorporationContact.objects.count(), 1)
        self.assertEqual(CorporationContactLabel.objects.count(), 3)
        self.assertEqual(
            CorporationContactLabel.objects.get(corporation=self.corporation, label_id=1).label_name,
            "I am Groot 1"
        )
        self.assertEqual(
            CorporationContactLabel.objects.get(corporation=self.corporation, label_id=2).label_name,
            "I am Groot 2"
        )
        self.assertEqual(
            CorporationContactLabel.objects.get(corporation=self.corporation, label_id=3).label_name,
            "I am Groot 3"
        )

        contact.refresh_from_db()
        self.assertEqual(contact.contact_id, 3)

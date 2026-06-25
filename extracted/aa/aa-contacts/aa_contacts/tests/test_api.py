from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypeAlias
from unittest import mock

from app_utils.testdata_factories import EveCharacterFactory, UserMainFactory
from django.test import TestCase

from aa_contacts.models import (
    AllianceContact,
    AllianceToken,
    Contact,
    ContactServerLink,
    ContactToken,
    CorporationContact,
    CorporationToken,
)
from aa_contacts.tasks import update_alliance_contacts, update_corporation_contacts

if TYPE_CHECKING:
    from allianceauth.eveonline.models import (
        EveAllianceInfo,
        EveCharacter,
        EveCorporationInfo,
    )
    from celery import Task
    from django.contrib.auth.models import User

    Owner: TypeAlias = EveAllianceInfo | EveCorporationInfo

    # During type checking the mixin is a TestCase so ``self.client`` and the
    # ``assert*`` helpers resolve; at runtime it stays a plain mixin (``object``)
    # so it is not collected/run on its own.
    _MixinBase = TestCase
else:
    _MixinBase = object


class ContactApiTestMixin(_MixinBase):
    owner_type: str
    contact_model: type[Contact]
    token_model: type[ContactToken]
    update_task: Task

    contact_target: EveCharacter

    @classmethod
    def setUpTestData(cls):
        cls.contact_target = EveCharacterFactory()

    # -- owner / membership helpers ------------------------------------

    def _owner(self, user: User) -> Owner:
        return getattr(user.profile.main_character, self.owner_type)

    def _owner_id(self, owner: Owner) -> int:
        return getattr(owner, f"{self.owner_type}_id")

    def _member(self, permissions: list[str] | None = None) -> User:
        return UserMainFactory(permissions=permissions or [])

    def _make_token(self, user: User) -> ContactToken:
        return self.token_model.objects.create(
            token=user.token_set.first(),
            **{self.owner_type: self._owner(user)},
        )

    def _make_contact(self, owner: Owner, **kwargs) -> Contact:
        defaults = {
            "contact_id": self.contact_target.character_id,
            "contact_type": Contact.ContactTypeOptions.CHARACTER,
            "standing": 5.0,
        }
        defaults.update(kwargs)
        return self.contact_model.objects.create(**{self.owner_type: owner}, **defaults)

    def _make_link(self, contact: Contact, **kwargs) -> ContactServerLink:
        defaults = {"name": "Link", "url": "https://example.com"}
        defaults.update(kwargs)
        return contact.server_links.create(**defaults)

    # -- perms ---------------------------------------------------------

    @property
    def manage_perm(self) -> str:
        return f"aa_contacts.manage_{self.owner_type}_contacts"

    @property
    def view_notes_perm(self) -> str:
        return f"aa_contacts.view_{self.owner_type}_notes"

    @property
    def view_links_perm(self) -> str:
        return f"aa_contacts.view_{self.owner_type}_server_links"

    # -- urls ----------------------------------------------------------

    @property
    def url_base(self) -> str:
        return f"/contacts/api/{self.owner_type}s"

    def contacts_url(self, owner_id: int) -> str:
        return f"{self.url_base}/{owner_id}/contacts/"

    def update_url(self, owner_id: int) -> str:
        return f"{self.url_base}/{owner_id}/contacts/update"

    def contact_detail_url(self, owner_id: int, pk: int) -> str:
        return f"{self.url_base}/{owner_id}/contacts/{pk}"

    def server_links_url(self, owner_id: int, pk: int) -> str:
        return f"{self.url_base}/{owner_id}/contacts/{pk}/server-links"

    def server_link_detail_url(self, owner_id: int, pk: int, link_pk: int) -> str:
        return f"{self.url_base}/{owner_id}/contacts/{pk}/server-links/{link_pk}"

    def tokens_url(self) -> str:
        return f"{self.url_base}/tokens/"

    def token_detail_url(self, owner_id: int) -> str:
        return f"{self.url_base}/tokens/{owner_id}/"

    # == GET .../contacts/ ============================================

    def test_list_contacts_member_with_token(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.get(self.contacts_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["id"], contact.pk)

    def test_list_contacts_superuser(self):
        member = self._member()
        owner = self._owner(member)
        self._make_token(member)
        self._make_contact(owner)

        superuser = UserMainFactory(is_superuser=True)
        self.client.force_login(superuser)
        response = self.client.get(self.contacts_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_list_contacts_non_member(self):
        member = self._member()
        owner = self._owner(member)
        self._make_token(member)
        self._make_contact(owner)

        outsider = self._member()
        self.client.force_login(outsider)
        response = self.client.get(self.contacts_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 403)

    def test_list_contacts_member_without_token(self):
        user = self._member()
        owner = self._owner(user)

        self.client.force_login(user)
        response = self.client.get(self.contacts_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 404)

    # == POST .../contacts/update =====================================

    def test_update_contacts_member_with_manage(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        owner_id = self._owner_id(owner)
        self._make_token(user)

        self.client.force_login(user)
        with mock.patch.object(self.update_task, "delay") as mock_delay:
            mock_delay.return_value = None
            response = self.client.post(self.update_url(owner_id))

        self.assertEqual(response.status_code, 200)
        mock_delay.assert_called_once_with(owner_id)

    def test_update_contacts_member_without_manage(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)

        self.client.force_login(user)
        with mock.patch.object(self.update_task, "delay") as mock_delay:
            mock_delay.return_value = None
            response = self.client.post(self.update_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 403)
        mock_delay.assert_not_called()

    def test_update_contacts_non_member_with_perm(self):
        member = self._member()
        owner = self._owner(member)
        self._make_token(member)

        outsider = self._member(permissions=[self.manage_perm])
        self.client.force_login(outsider)
        with mock.patch.object(self.update_task, "delay") as mock_delay:
            mock_delay.return_value = None
            response = self.client.post(self.update_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 403)
        mock_delay.assert_not_called()

    def test_update_contacts_member_perm_without_token(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)

        self.client.force_login(user)
        with mock.patch.object(self.update_task, "delay") as mock_delay:
            mock_delay.return_value = None
            response = self.client.post(self.update_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 404)
        mock_delay.assert_not_called()

    # == PATCH .../contacts/{pk} ======================================

    def test_edit_contact_member_manage_view_notes(self):
        user = self._member(permissions=[self.manage_perm, self.view_notes_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.patch(
            self.contact_detail_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"notes": "hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        contact.refresh_from_db()
        self.assertEqual(contact.notes, "hello")

    def test_edit_contact_missing_perms(self):
        # has manage but not view_notes -> 403
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.patch(
            self.contact_detail_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"notes": "hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        contact.refresh_from_db()
        self.assertEqual(contact.notes, "")

    def test_edit_contact_no_token(self):
        user = self._member(permissions=[self.manage_perm, self.view_notes_perm])
        owner = self._owner(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.patch(
            self.contact_detail_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"notes": "hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_contact_wrong_contact(self):
        user = self._member(permissions=[self.manage_perm, self.view_notes_perm])
        owner = self._owner(user)
        self._make_token(user)

        self.client.force_login(user)
        response = self.client.patch(
            self.contact_detail_url(self._owner_id(owner), 999999),
            data=json.dumps({"notes": "hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    # == POST .../contacts/{pk}/server-links ==========================

    def test_create_server_link_member_manage(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.post(
            self.server_links_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"name": "Discord", "url": "https://discord.gg/x"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.server_links.count(), 1)
        self.assertEqual(contact.server_links.first().name, "Discord")

    def test_create_server_link_without_manage(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.post(
            self.server_links_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"name": "Discord", "url": "https://discord.gg/x"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(contact.server_links.count(), 0)

    def test_create_server_link_no_token(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.post(
            self.server_links_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"name": "Discord", "url": "https://discord.gg/x"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_create_server_link_contact_not_found(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)

        self.client.force_login(user)
        response = self.client.post(
            self.server_links_url(self._owner_id(owner), 999999),
            data=json.dumps({"name": "Discord", "url": "https://discord.gg/x"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_create_server_link_invalid_url(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.post(
            self.server_links_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"name": "Bad", "url": "not a url"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(contact.server_links.count(), 0)

    def test_create_server_link_custom_scheme(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.post(
            self.server_links_url(self._owner_id(owner), contact.pk),
            data=json.dumps({"name": "TS", "url": "ts3server://ts.example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.server_links.get().url, "ts3server://ts.example.com")

    # == PUT .../contacts/{pk}/server-links/{link_pk} =================

    def test_update_server_link(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)
        link = self._make_link(contact)

        self.client.force_login(user)
        response = self.client.put(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, link.pk),
            data=json.dumps({"name": "Updated", "url": "https://new.example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated")
        link.refresh_from_db()
        self.assertEqual(link.name, "Updated")

    def test_update_server_link_link_not_found(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.put(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, 999999),
            data=json.dumps({"name": "Updated", "url": "https://new.example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_update_server_link_without_manage(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)
        link = self._make_link(contact)

        self.client.force_login(user)
        response = self.client.put(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, link.pk),
            data=json.dumps({"name": "Updated", "url": "https://new.example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        link.refresh_from_db()
        self.assertEqual(link.name, "Link")

    def test_update_server_link_invalid_url(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)
        link = self._make_link(contact)

        self.client.force_login(user)
        response = self.client.put(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, link.pk),
            data=json.dumps({"name": "Updated", "url": "not a url"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        link.refresh_from_db()
        self.assertEqual(link.name, "Link")
        self.assertEqual(link.url, "https://example.com")

    # == DELETE .../contacts/{pk}/server-links/{link_pk} ==============

    def test_delete_server_link(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)
        link = self._make_link(contact)

        self.client.force_login(user)
        response = self.client.delete(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, link.pk),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.server_links.count(), 0)

    def test_delete_server_link_link_not_found(self):
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)

        self.client.force_login(user)
        response = self.client.delete(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, 999999),
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_server_link_without_manage(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner)
        link = self._make_link(contact)

        self.client.force_login(user)
        response = self.client.delete(
            self.server_link_detail_url(self._owner_id(owner), contact.pk, link.pk),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(contact.server_links.count(), 1)

    # == tokens =======================================================

    def test_tokens_list(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)

        self.client.force_login(user)
        response = self.client.get(self.tokens_url())

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(
            body[0][self.owner_type][f"{self.owner_type}_id"],
            self._owner_id(owner),
        )

    def test_token_single_member(self):
        user = self._member()
        owner = self._owner(user)
        self._make_token(user)

        self.client.force_login(user)
        response = self.client.get(self.token_detail_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 200)

    def test_token_single_non_member(self):
        member = self._member()
        owner = self._owner(member)
        self._make_token(member)

        outsider = self._member()
        self.client.force_login(outsider)
        response = self.client.get(self.token_detail_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 403)

    def test_token_single_no_token(self):
        user = self._member()
        owner = self._owner(user)

        self.client.force_login(user)
        response = self.client.get(self.token_detail_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 404)

    # == schema-resolver asymmetry ====================================

    def test_notes_and_links_hidden_without_view_perms(self):
        # A member with manage but neither view_notes nor view_server_links.
        user = self._member(permissions=[self.manage_perm])
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner, notes="secret")
        self._make_link(contact)

        self.client.force_login(user)
        response = self.client.get(self.contacts_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 200)
        entry = response.json()[0]
        self.assertIsNone(entry["notes"])
        self.assertEqual(entry["server_links"], [])

    def test_notes_and_links_visible_with_view_perms(self):
        user = self._member(
            permissions=[self.manage_perm, self.view_notes_perm, self.view_links_perm]
        )
        owner = self._owner(user)
        self._make_token(user)
        contact = self._make_contact(owner, notes="secret")
        self._make_link(contact)

        self.client.force_login(user)
        response = self.client.get(self.contacts_url(self._owner_id(owner)))

        self.assertEqual(response.status_code, 200)
        entry = response.json()[0]
        self.assertEqual(entry["notes"], "secret")
        self.assertEqual(len(entry["server_links"]), 1)


class PermissionsApiTest(TestCase):
    url = "/contacts/api/permissions/me"

    def test_no_permissions(self):
        user = UserMainFactory()

        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "can_manage_alliance_contacts": False,
                "can_manage_corporation_contacts": False,
            },
        )

    def test_manage_alliance_only(self):
        user = UserMainFactory(permissions=["aa_contacts.manage_alliance_contacts"])

        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "can_manage_alliance_contacts": True,
                "can_manage_corporation_contacts": False,
            },
        )

    def test_manage_corporation_only(self):
        user = UserMainFactory(permissions=["aa_contacts.manage_corporation_contacts"])

        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "can_manage_alliance_contacts": False,
                "can_manage_corporation_contacts": True,
            },
        )

    def test_manage_both(self):
        user = UserMainFactory(
            permissions=[
                "aa_contacts.manage_alliance_contacts",
                "aa_contacts.manage_corporation_contacts",
            ]
        )

        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "can_manage_alliance_contacts": True,
                "can_manage_corporation_contacts": True,
            },
        )

    def test_superuser(self):
        user = UserMainFactory(is_superuser=True)

        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "can_manage_alliance_contacts": True,
                "can_manage_corporation_contacts": True,
            },
        )


class AllianceContactApiTest(ContactApiTestMixin, TestCase):
    owner_type = "alliance"
    contact_model = AllianceContact
    token_model = AllianceToken
    update_task = update_alliance_contacts


class CorporationContactApiTest(ContactApiTestMixin, TestCase):
    owner_type = "corporation"
    contact_model = CorporationContact
    token_model = CorporationToken
    update_task = update_corporation_contacts

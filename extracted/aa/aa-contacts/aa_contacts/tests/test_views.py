from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias
from unittest import mock

from app_utils.testdata_factories import EveCharacterFactory, UserMainFactory
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from aa_contacts.models import AllianceToken, ContactToken, CorporationToken

if TYPE_CHECKING:
    from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
    from django.contrib.auth.models import User

    Owner: TypeAlias = EveAllianceInfo | EveCorporationInfo

    # During type checking the mixin is a TestCase so ``self.client`` and the
    # ``assert*`` helpers resolve; at runtime it stays a plain mixin (``object``)
    # so it is not collected/run on its own.
    _MixinBase = TestCase
else:
    _MixinBase = object


class IndexViewTest(TestCase):
    def test_index_redirects_to_react_view(self):
        user = UserMainFactory()

        self.client.force_login(user)
        response = self.client.get(reverse("aa_contacts:index"))

        self.assertRedirects(
            response,
            reverse("aa_contacts:react_view"),
            fetch_redirect_response=False,
        )

    def test_index_requires_login(self):
        response = self.client.get(reverse("aa_contacts:index"))

        self.assertEqual(response.status_code, 302)


class ReactViewTest(TestCase):
    def test_react_view_renders_template(self):
        user = UserMainFactory()

        self.client.force_login(user)
        response = self.client.get(reverse("aa_contacts:react_view"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "aa_contacts/react_base.html")

    def test_react_view_requires_login(self):
        response = self.client.get(reverse("aa_contacts:react_view"))

        self.assertEqual(response.status_code, 302)


class AddTokenTestMixin(_MixinBase):
    owner_type: str
    scope: str
    token_model: type[ContactToken]
    add_url_name: str
    # dotted path to the celery task imported into ``views``; we patch its
    # ``.delay`` so nothing is enqueued during tests.
    update_task_path: str

    # -- helpers -------------------------------------------------------

    @property
    def manage_perm(self) -> str:
        return f"aa_contacts.manage_{self.owner_type}_contacts"

    @property
    def add_url(self) -> str:
        return reverse(f"aa_contacts:{self.add_url_name}")

    def _member(self, *, manage: bool = True, character=None) -> User:
        kwargs = {
            "permissions": [self.manage_perm] if manage else [],
            "main_character__scopes": [self.scope],
        }
        if character is not None:
            kwargs["main_character__character"] = character
        return UserMainFactory(**kwargs)

    def _owner(self, user: User) -> Owner:
        return getattr(user.profile.main_character, self.owner_type)

    def _owner_id(self, owner: Owner) -> int:
        return getattr(owner, f"{self.owner_type}_id")

    def _token_pk(self, user: User) -> int:
        return user.token_set.first().pk

    def _owned_count(self, owner: Owner) -> int:
        return self.token_model.objects.filter(**{self.owner_type: owner}).count()

    # The ``@token_required`` decorator hands the chosen token to the view when
    # a ``_token`` pk is POSTed by a user that owns a valid, correctly-scoped
    # token. We replicate that token-selection POST here.
    def _post(self, user: User):
        self.client.force_login(user)
        with mock.patch(f"{self.update_task_path}.delay") as mock_delay:
            mock_delay.return_value = None
            response = self.client.post(self.add_url, {"_token": self._token_pk(user)})
        return response, mock_delay

    @staticmethod
    def _messages(response) -> list[str]:
        return [m.message for m in get_messages(response.wsgi_request)]

    # -- tests ---------------------------------------------------------

    def test_add_token_creates_token_and_triggers_update(self):
        user = self._member()
        owner = self._owner(user)

        response, mock_delay = self._post(user)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self._owned_count(owner), 1)
        mock_delay.assert_called_once_with(self._owner_id(owner))
        self.assertTrue(any("now being tracked" in m for m in self._messages(response)))

    def test_add_token_already_tracked(self):
        user = self._member()
        owner = self._owner(user)
        self.token_model.objects.create(
            token=user.token_set.first(), **{self.owner_type: owner}
        )

        response, mock_delay = self._post(user)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self._owned_count(owner), 1)
        mock_delay.assert_not_called()
        self.assertTrue(
            any("already being tracked" in m for m in self._messages(response))
        )

    def test_add_token_without_manage_permission(self):
        user = self._member(manage=False)
        owner = self._owner(user)

        response, mock_delay = self._post(user)

        # Django's ``permission_required`` redirects to login on failure.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self._owned_count(owner), 0)
        mock_delay.assert_not_called()

    def test_add_token_requires_login(self):
        response = self.client.post(self.add_url, {"_token": 1})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.token_model.objects.count(), 0)

    def test_get_without_selection_shows_token_picker(self):
        # A bare GET (no ``_token``) must not create anything: the decorator
        # renders the token-selection page instead.
        user = self._member()
        owner = self._owner(user)

        self.client.force_login(user)
        response = self.client.get(self.add_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._owned_count(owner), 0)


class AddAllianceTokenTest(AddTokenTestMixin, TestCase):
    owner_type = "alliance"
    scope = "esi-alliances.read_contacts.v1"
    token_model = AllianceToken
    add_url_name = "add_alliance_token"
    update_task_path = "aa_contacts.views.update_alliance_contacts"

    def test_add_token_character_without_alliance(self):
        char = EveCharacterFactory(corporation__create_alliance=False)
        user = self._member(character=char)

        response, task = self._post(user)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(AllianceToken.objects.count(), 0)
        task.delay.assert_not_called()
        self.assertTrue(
            any("need to be in an alliance" in m for m in self._messages(response))
        )


class AddCorporationTokenTest(AddTokenTestMixin, TestCase):
    owner_type = "corporation"
    scope = "esi-corporations.read_contacts.v1"
    token_model = CorporationToken
    add_url_name = "add_corporation_token"
    update_task_path = "aa_contacts.views.update_corporation_contacts"

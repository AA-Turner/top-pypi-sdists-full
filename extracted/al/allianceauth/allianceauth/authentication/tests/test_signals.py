from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from esi.models import Token

from allianceauth.authentication.models import (
    CharacterOwnership, OwnershipRecord, State, UserProfile,
)
from allianceauth.authentication.signals import (
    state_member_alliances_changed, state_member_characters_changed,
    state_member_corporations_changed, state_member_factions_changed,
    state_saved,
)
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils

MODULE_PATH = "allianceauth.authentication.signals"


class AuthenticationSignalsTestCase(TestCase):
    def setUp(self):
        self.member_state = AuthUtils.get_member_state()
        self.guest_state = AuthUtils.get_guest_state()
        self.user = AuthUtils.create_user("test_user")
        self.main_character = EveCharacter.objects.create(
            character_id=1001,
            character_name="Main Character",
            corporation_id=2001,
            corporation_name="Main Corp",
            corporation_ticker="MAIN",
        )
        self.alt_character = EveCharacter.objects.create(
            character_id=1002,
            character_name="Alt Character",
            corporation_id=2002,
            corporation_name="Alt Corp",
            corporation_ticker="ALT",
        )
        self.user.profile.main_character = self.main_character
        self.user.profile.state = self.member_state
        self.user.profile.save(update_fields=["main_character", "state"])

    @patch(MODULE_PATH + ".trigger_state_check")
    def test_state_membership_receivers_trigger_state_check(self, trigger_state_check):
        state = State.objects.create(name="Signal State", priority=900)
        trigger_state_check.reset_mock()

        for receiver in [
            state_member_characters_changed,
            state_member_corporations_changed,
            state_member_alliances_changed,
            state_member_factions_changed,
        ]:
            with self.subTest(receiver=receiver.__name__):
                receiver(sender=None, instance=state, action="post_add")

        state_saved(sender=State, instance=state)

        self.assertEqual(trigger_state_check.call_count, 5)

    @patch.object(UserProfile, "assign_state")
    def test_reassess_on_profile_save_reassigns_state(self, assign_state):
        self.user.profile.language = UserProfile.Language.ENGLISH

        self.user.profile.save(update_fields=["language"])

        assign_state.assert_called_once_with()

    def test_create_required_models_creates_profile_for_new_user(self):
        user = User.objects.create(username="created_by_signal")

        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_create_required_models_does_not_duplicate_existing_profile(self):
        profile_pk = self.user.profile.pk
        self.user.username = "updated_user"

        self.user.save(update_fields=["username"])

        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 1)
        self.assertEqual(self.user.profile.pk, profile_pk)

    def test_record_character_ownership_creates_ownership_and_history(self):
        Token.objects.create(
            user=self.user,
            character_id=self.alt_character.character_id,
            character_name=self.alt_character.character_name,
            character_owner_hash="owner-hash-1",
            access_token="access-token",
            refresh_token="refresh-token",
        )

        ownership = CharacterOwnership.objects.get(character=self.alt_character)

        self.assertEqual(ownership.user, self.user)
        self.assertEqual(ownership.owner_hash, "owner-hash-1")
        self.assertTrue(
            OwnershipRecord.objects.filter(
                user=self.user,
                character=self.alt_character,
                owner_hash="owner-hash-1",
            ).exists()
        )

    def test_validate_main_character_clears_profile_on_ownership_delete(self):
        ownership = CharacterOwnership.objects.create(
            character=self.main_character,
            user=self.user,
            owner_hash="owner-hash-main",
        )

        ownership.delete()
        self.user.profile.refresh_from_db()

        self.assertIsNone(self.user.profile.main_character)

    def test_validate_ownership_deletes_ownership_when_last_refreshable_token_deleted(self):
        ownership = CharacterOwnership.objects.create(
            character=self.alt_character,
            user=self.user,
            owner_hash="owner-hash-2",
        )
        token = Token.objects.create(
            user=self.user,
            character_id=self.alt_character.character_id,
            character_name=self.alt_character.character_name,
            character_owner_hash="owner-hash-2",
            access_token="access-token",
            refresh_token="refresh-token",
        )

        token.delete()

        self.assertFalse(CharacterOwnership.objects.filter(pk=ownership.pk).exists())

    def test_assign_state_on_active_change_sets_guest_state_for_inactive_user(self):
        self.user.is_active = False

        self.user.save(update_fields=["is_active"])
        self.user.profile.refresh_from_db()

        self.assertEqual(self.user.profile.state, self.guest_state)

    @patch.object(UserProfile, "assign_state")
    def test_assign_state_on_active_change_reassigns_state_when_user_reactivated(
        self, assign_state
    ):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        self.user.is_active = True
        self.user.save(update_fields=["is_active"])

        assign_state.assert_called_once_with()

    @patch.object(UserProfile, "assign_state")
    def test_check_state_on_character_update_reassesses_main_character_owner(
        self, assign_state
    ):
        self.main_character.character_name = "Renamed Main Character"

        self.main_character.save(update_fields=["character_name"])

        assign_state.assert_called_once_with()

    def test_ownership_record_creation_skips_duplicate_latest_record(self):
        CharacterOwnership.objects.create(
            character=self.alt_character,
            user=self.user,
            owner_hash="owner-hash-3",
        )
        self.assertEqual(OwnershipRecord.objects.count(), 1)

        CharacterOwnership.objects.filter(character=self.alt_character).delete()
        CharacterOwnership.objects.create(
            character=self.alt_character,
            user=self.user,
            owner_hash="owner-hash-3",
        )

        self.assertEqual(OwnershipRecord.objects.count(), 1)

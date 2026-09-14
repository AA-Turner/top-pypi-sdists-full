"""Reproduction for issue 1465:
main corporation name / Discord nickname stay stale after a corp change, even
though state and groups update.

Two halves of the problem:

1. ``EveCharacter.update_character()`` commits the new affiliation IDs in a first
    ``save()`` and only writes the cached name/ticker fields in a second ``save()``.
    The first save synchronously fires the whole state-change cascade
    (``post_save`` -> ``assign_state`` -> ``state_changed`` -> every service hook
    and every third-party receiver). Everything in that cascade therefore runs
    against a row that already has the new IDs but still has the old names.
    ``test_state_change_cascade_sees_consistent_character_row`` observes that row
    from a ``state_changed`` receiver, exactly where service hooks and third
    party apps sit.

2. Once a character is in that half-updated state, nothing repairs it.
    ``update_character_chunk`` only queues ``update_character`` when the IDs (or
    character name) differ from ESI, and the IDs already match.
    ``test_chunk_update_repairs_stale_cached_names`` starts from the exact DB
    state the reporter screenshotted and shows the periodic task leaves it alone.

Both tests assert the *desired* behaviour: they failed on the two-save
``update_character()`` and the ID-only chunk diff, and guard against regressing.
"""

from unittest.mock import patch

from allianceauth.authentication.signals import state_changed
from allianceauth.tests.auth_utils import AuthUtils
from allianceauth.utils.testing import NoSocketsTestCase

from ..models import EveAllianceInfo, EveCharacter, EveCorporationInfo
from ..tasks import update_character_chunk
from .esi_client_stub import EsiClientStub

PROVIDER_CLIENT = "allianceauth.eveonline.providers.open_api_provider._client"


class TestChunkUpdateRepairsStaleCachedNames(NoSocketsTestCase):
    """Half 2: the periodic update never repairs a row whose IDs are current
    but whose cached names are stale."""

    def test_chunk_update_repairs_stale_cached_names(self) -> None:
        # given: the corp is known and correct in the DB ...
        with patch(PROVIDER_CLIENT, EsiClientStub()):
            corp = EveCorporationInfo.objects.create_corporation(2011)
        self.assertEqual(corp.corporation_name, "LexCorp")

        # ... and the character already carries the current corporation_id
        # (matching ESI) but still has the name/ticker of the previous corp.
        # This is the state from the reporter's EveCharacter admin screenshot.
        character = EveCharacter.objects.create(
            character_id=1011,
            character_name="Lex Luthor",
            corporation_id=2011,
            corporation_name="Pator Tech School",
            corporation_ticker="PTS",
            alliance_id=None,
        )

        # when: the normal background update runs (CELERY_ALWAYS_EAGER, so any
        # queued update_character executes inline against the same stub)
        with patch(PROVIDER_CLIENT, EsiClientStub()):
            update_character_chunk([character.character_id])

        # then: the cached names should match the corp the IDs point at
        character.refresh_from_db()
        self.assertEqual(character.corporation_id, 2011)
        self.assertEqual(character.corporation_name, "LexCorp")
        self.assertEqual(character.corporation_ticker, "LC")


class TestStateChangeCascadeSeesConsistentRow(NoSocketsTestCase):
    """Half 1: the state-change cascade fired by ``update_character()`` runs
    while the DB row has new IDs and old names."""

    def setUp(self) -> None:
        with patch(PROVIDER_CLIENT, EsiClientStub()):
            self.alliance = EveAllianceInfo.objects.create_alliance(3001)
            EveCorporationInfo.objects.create_corporation(2001)  # Wayne Technologies, in 3001
            EveCorporationInfo.objects.create_corporation(2011)  # LexCorp, no alliance

        # Member state is granted by alliance, like the reporter's setup
        AuthUtils.disconnect_signals()
        AuthUtils.get_member_state().member_alliances.add(self.alliance)
        AuthUtils.connect_signals()

        # A recruit: authed while in LexCorp (not a member corp), so Guest.
        self.user = AuthUtils.create_user("bruce_wayne", disconnect_signals=True)
        self.character = AuthUtils.add_main_character_2(
            self.user,
            "Bruce Wayne",
            1001,
            corp_id=2011,
            corp_name="LexCorp",
            corp_ticker="LC",
            disconnect_signals=True,
        )
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.state.name, "Guest")

    def test_state_change_cascade_sees_consistent_character_row(self) -> None:
        # given: a probe on state_changed, which is where
        # check_service_accounts_state_changed (Discord/Mumble validate_user and
        # update_groups) and third-party apps receive the change. It only reads.
        observed: list[dict] = []

        def probe(sender, user, state, **kwargs):
            row = EveCharacter.objects.values(
                "corporation_id", "corporation_name", "corporation_ticker",
                "alliance_id", "alliance_name",
            ).get(character_id=1001)
            observed.append({"state": state.name, **row})

        state_changed.connect(probe, weak=False)
        self.addCleanup(state_changed.disconnect, probe)

        # when: ESI now reports the recruit was accepted into Wayne Technologies
        with patch(PROVIDER_CLIENT, EsiClientStub()):
            self.character.update_character()

        # then: the cascade fired once, for Guest -> Member ...
        self.assertEqual(len(observed), 1)
        seen = observed[0]
        self.assertEqual(seen["state"], "Member")
        self.assertEqual(seen["corporation_id"], 2001)
        self.assertEqual(seen["alliance_id"], 3001)

        # ... and the row it ran against should already carry the matching
        # names. Today it still says LexCorp / LC with no alliance name, which
        # is what every service hook and third-party receiver gets to act on.
        self.assertEqual(seen["corporation_name"], "Wayne Technologies")
        self.assertEqual(seen["corporation_ticker"], "WTE")
        self.assertEqual(seen["alliance_name"], "Wayne Enterprises")

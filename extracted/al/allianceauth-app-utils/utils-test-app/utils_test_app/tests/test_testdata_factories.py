from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
from app_utils.testdata_factories import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
    GroupFactory,
    StateFactory,
    UserFactory,
    UserMainFactory,
)
from app_utils.testing import NoSocketsTestCase


class TestEveAllianceInfoFactory(NoSocketsTestCase):
    def test_should_create_obj(self):
        # when
        obj = EveAllianceInfoFactory()
        # then
        self.assertIsInstance(obj, EveAllianceInfo)


class TestEveCorporationInfoFactory(NoSocketsTestCase):
    def test_should_create_obj(self):
        # when
        obj = EveCorporationInfoFactory()
        # then
        self.assertIsInstance(obj, EveCorporationInfo)


class TestEveInfoFactory(NoSocketsTestCase):
    def test_can_create_without_alliance(self):
        character = EveCharacterFactory(
            corporation=EveCorporationInfoFactory(create_alliance=False)
        )
        self.assertIsNone(character.alliance_id)


class TestGroupFactory(NoSocketsTestCase):
    def test_can_set_public(self):
        g = GroupFactory(authgroup__public=True)
        self.assertTrue(g.authgroup.public)

    def test_can_set_states(self):
        s = StateFactory()
        g = GroupFactory(authgroup__states=[s])
        self.assertIn(s, g.authgroup.states.all())


class TestStateFactory(NoSocketsTestCase):
    def test_can_create_with_defaults(self):
        # when
        state = StateFactory()
        # then
        self.assertTrue(state)

    def test_can_create_with_characters(self):
        # when
        main = EveCharacterFactory()
        state = StateFactory(member_characters=[main])
        user = UserMainFactory(main_character__character=main)
        # then
        self.assertEqual(user.profile.state, state)

    def test_can_create_with_corporations(self):
        # when
        corporation = EveCorporationInfoFactory()
        main = EveCharacterFactory(corporation=corporation)
        state = StateFactory(member_corporations=[corporation])
        user = UserMainFactory(main_character__character=main)
        # then
        self.assertEqual(user.profile.state, state)

    def test_can_create_with_alliances(self):
        # when
        corporation = EveCorporationInfoFactory()
        main = EveCharacterFactory(corporation=corporation)
        state = StateFactory(member_alliances=[corporation.alliance])
        user = UserMainFactory(main_character__character=main)
        # then
        self.assertEqual(user.profile.state, state)

    def test_can_create_with_permissions(self):
        # when
        main = EveCharacterFactory()
        perm = "groupmanagement.request_groups"
        StateFactory(member_characters=[main], permissions=[perm])
        user = UserMainFactory(main_character__character=main)
        # then
        user.has_perm(perm)


class TestUserFactory(NoSocketsTestCase):
    def test_can_create_with_defaults(self):
        # when
        user = UserFactory()
        # then
        self.assertTrue(user)

    def test_can_create_with_permission(self):
        # when
        perm = "groupmanagement.request_groups"
        user = UserFactory(permissions=[perm])
        # then
        user.has_perm(perm)

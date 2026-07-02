import requests

from django.contrib.auth.models import User
from django.test import TestCase

from allianceauth.authentication.models import EveCharacter
from app_utils.testing import (
    CacheFake,
    NoSocketsTestCase,
    SocketAccessError,
    add_new_token,
    create_eve_character,
    create_fake_user,
    create_user_from_evecharacter,
    generate_invalid_pk,
)


class TestNoSocketsTestCase(NoSocketsTestCase):
    def test_raises_exception_on_attempted_network_access(self):
        with self.assertRaises(SocketAccessError):
            requests.get("https://www.google.com")


class TestGenerateInvalidPk(TestCase):
    def test_normal(self):
        User.objects.all().delete()
        User.objects.create(username="John Doe", password="dummy")
        invalid_pk = generate_invalid_pk(User)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=invalid_pk)


class TestCreateUserFromEveCharacter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.character = EveCharacter.objects.create(
            character_id=1001,
            character_name="Bruce Wayne",
            corporation_id=2001,
            corporation_name="Wayne Tech",
            corporation_ticker="WYT",
        )

    def test_should_create_basic_user(self):
        # when
        user, character_ownership = create_user_from_evecharacter(1001)
        # then
        self.assertEqual(user.username, "Bruce_Wayne")
        self.assertEqual(character_ownership.character, self.character)
        self.assertEqual(character_ownership.user, user)

    def test_should_create_user_with_given_scope(self):
        # when
        user, character_ownership = create_user_from_evecharacter(
            1001, scopes=["dummy_scope"]
        )
        # then
        self.assertEqual(user.username, "Bruce_Wayne")
        self.assertEqual(character_ownership.character, self.character)
        self.assertEqual(character_ownership.user, user)
        self.assertTrue(user.token_set.filter(scopes__name="dummy_scope").exists())


class TestCreateFakeUser(TestCase):
    def test_should_create_fake_user(self):
        # when
        user = create_fake_user(1001, "Bruce Wayne")
        # then
        self.assertTrue(User.objects.filter(pk=user.pk).exists())
        self.assertEqual(user.username, "Bruce_Wayne")
        self.assertEqual(user.profile.main_character.character_id, 1001)
        self.assertEqual(user.profile.main_character.character_name, "Bruce Wayne")
        self.assertEqual(user.profile.main_character.corporation_id, 2001)
        self.assertEqual(user.profile.main_character.alliance_id, 3001)
        self.assertEqual(user.profile.main_character.alliance_name, "Wayne Enterprises")

    def test_should_create_fake_user_with_corporation(self):
        # when
        user = create_fake_user(
            1001,
            "Bruce Wayne",
            corporation_id=2002,
            corporation_name="Dummy corp",
            corporation_ticker="ABC",
        )
        # then
        self.assertEqual(user.profile.main_character.corporation_id, 2002)
        self.assertEqual(user.profile.main_character.corporation_name, "Dummy corp")
        self.assertEqual(user.profile.main_character.corporation_ticker, "ABC")
        self.assertIsNone(user.profile.main_character.alliance_id)

    def test_should_create_fake_user_with_permissions(self):
        # when
        user = create_fake_user(1001, "Bruce Wayne", permissions=["auth.add_group"])
        # then
        self.assertTrue(user.has_perm("auth.add_group"))


class TestAddNewToken(TestCase):
    def test_should_add_new_token(self):
        # given
        user = User.objects.create(username="Bruce Wayne")
        character = create_eve_character(1001, "Bruce Wayne")
        # when
        token = add_new_token(user, character)
        # then
        self.assertEqual(token.character_id, character.character_id)

    def test_should_add_new_token_with_scope(self):
        # given
        user = User.objects.create(username="Bruce Wayne")
        character = create_eve_character(1001, "Bruce Wayne")
        # when
        token = add_new_token(user, character, scopes=["abc"])
        # then
        self.assertEqual(token.character_id, character.character_id)
        self.assertTrue(token.scopes.filter(name="abc").exists())

    def test_should_have_same_character_owner_hash_in_additional_tokens(self):
        # given
        user = User.objects.create(username="Bruce Wayne")
        character = create_eve_character(1001, "Bruce Wayne")
        token_1 = add_new_token(user, character, scopes=["scope1"])
        # when
        token_2 = add_new_token(user, character, scopes=["scope2"])
        # then
        self.assertEqual(token_1.character_owner_hash, token_2.character_owner_hash)


class TestCacheFake(TestCase):
    def test_get_should_return_value_when_found(self):
        cache = CacheFake()
        cache.set("alpha", 5)
        got = cache.get("alpha")
        self.assertEqual(got, 5)

    def test_get_should_return_default_when_not_found(self):
        cache = CacheFake()
        cache.set("alpha", 5)
        got = cache.get("bravo", 99)
        self.assertEqual(got, 99)

    def test_delete_should_remove_key(self):
        cache = CacheFake()
        cache.set("alpha", 5)
        cache.delete("alpha")
        self.assertIsNone(cache.get("alpha"))

    def test_delete_should_ignore_when_key_does_not_exist(self):
        cache = CacheFake()
        cache.delete("alpha")

    def test_clear_should_remove_all_keys(self):
        cache = CacheFake()
        cache.set("alpha", 5)
        cache.clear()
        self.assertIsNone(cache.get("alpha"))

    def test_ttl_should_return_timeout_when_key_exists(self):
        cache = CacheFake()
        cache.set("alpha", "django", timeout=5)
        got = cache.ttl("alpha")
        self.assertEqual(got, 5)

    def test_ttl_should_return_none_when_key_does_not_exit(self):
        cache = CacheFake()
        got = cache.ttl("alpha")
        self.assertIsNone(got)

    def test_should_have_default_timeout(self):
        cache = CacheFake()
        cache.set("alpha", "django")
        got = cache.ttl("alpha")
        self.assertGreater(got, 0)

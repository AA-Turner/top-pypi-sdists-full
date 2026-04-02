from eveuniverse.helpers import (
    EveEntityNameResolver,
    dict_hash,
    get_or_create_esi_or_none,
    meters_to_au,
    meters_to_ly,
)
from eveuniverse.models import EveEntity
from eveuniverse.utils import NoSocketsTestCase

from .testdata.factories import create_eve_entity


class TestHelpers(NoSocketsTestCase):
    def test_meters_to_ly(self):
        self.assertEqual(meters_to_ly(9_460_000_000_000_000), 1)
        self.assertEqual(meters_to_ly(0), 0)
        with self.assertRaises(ValueError):
            meters_to_ly("invalid")

    def test_meters_to_au(self):
        self.assertEqual(meters_to_au(149_597_870_691), 1)
        self.assertEqual(meters_to_au(0), 0)
        with self.assertRaises(ValueError):
            meters_to_au("invalid")


class TestGetOrCreateEsiOrNone(NoSocketsTestCase):
    def test_return_obj_when_property_found(self):
        # given
        create_eve_entity(id=1001, name="Alpha", category="corporation")
        entry = {"type_id": 1001}
        # when
        obj: EveEntity = get_or_create_esi_or_none("type_id", entry, EveEntity)
        # then
        self.assertEqual(obj.id, 1001)

    def test_return_none_when_property_not_found(self):
        # given
        create_eve_entity(id=1001, name="Alpha", category="corporation")
        entry = {}
        # when
        obj = get_or_create_esi_or_none("type_id", entry, EveEntity)
        # then
        self.assertIsNone(obj)


class TestEveEntityNameResolver(NoSocketsTestCase):
    def test_to_name(self):
        # when
        resolver = EveEntityNameResolver({1: "alpha", 2: "bravo", 3: "charlie"})
        # then
        self.assertEqual(resolver.to_name(2), "bravo")
        self.assertEqual(resolver.to_name(4), "")


class TestDictHash(NoSocketsTestCase):
    def test_should_create_string(self):
        # given
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"a": 1, "b": 2, "c": 4}
        # when
        hash_1a = dict_hash(d1)
        hash_1b = dict_hash(d1)
        hash_2 = dict_hash(d2)
        # then
        self.assertIsInstance(hash_1a, str)
        self.assertEqual(hash_1a, hash_1b)
        self.assertNotEqual(hash_1a, hash_2)

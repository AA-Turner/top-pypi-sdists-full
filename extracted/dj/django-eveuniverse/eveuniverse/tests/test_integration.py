from django.test import TestCase

from eveuniverse.models import EveUniverseEntityModel


class TestPublicApi(TestCase):
    def test_should_not_break(self):
        self.assertTrue(EveUniverseEntityModel.LOAD_DOGMAS)

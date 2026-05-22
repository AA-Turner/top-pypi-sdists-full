from django.core.cache import cache
from django.db.models import QuerySet
from django.test import TestCase


def queryset_pks(queryset: QuerySet) -> set:
    """shortcut that returns the pks of the given queryset as set.
    Useful for comparing test results.
    """
    return set(queryset.values_list("pk", flat=True))


class TestCaseWithClearCache(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cache.clear()

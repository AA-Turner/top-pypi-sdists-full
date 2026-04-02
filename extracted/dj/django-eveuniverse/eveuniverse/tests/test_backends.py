from unittest.mock import patch

from celery_once import AlreadyQueued

from eveuniverse.backends import DjangoBackend
from eveuniverse.utils import NoSocketsTestCase

MODULE_PATH = "eveuniverse.backends"


@patch(MODULE_PATH + ".cache.delete", spec=True)
@patch(MODULE_PATH + ".cache.add", spec=True)
class TestDjangoBackend(NoSocketsTestCase):
    def test_should_acquire_lock(self, mock_cache_add, mock_cache_delete):
        # when
        DjangoBackend.raise_or_lock("alpha", 5)
        # then
        self.assertTrue(mock_cache_add.called)

    def test_should_raise_error_when_lock_fails(
        self, mock_cache_add, mock_cache_delete
    ):
        # given
        mock_cache_add.side_effect = AlreadyQueued(countdown=5)
        # when/then
        with self.assertRaises(AlreadyQueued):
            DjangoBackend.raise_or_lock("alpha", 5)

    def test_should_clear_lock(self, mock_cache_add, mock_cache_delete):
        # when
        DjangoBackend.clear_lock("alpha")
        # then
        self.assertTrue(mock_cache_delete.called)

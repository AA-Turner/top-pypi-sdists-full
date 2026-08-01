import os
import unittest

from abstra_internals import credentials
from abstra_internals.consts.filepaths import CREDENTIALS_FILEPATH, DOT_ABSTRA_DIR
from abstra_internals.credentials import (
    delete_credentials,
    get_credentials,
    mark_token_rejected,
    resolve_headers,
    set_credentials,
)
from tests.fixtures import clear_dir, init_dir


class CredentialsTest(unittest.TestCase):
    def setUp(self):
        self.root = init_dir()
        credentials._rejected_tokens.clear()

    def tearDown(self):
        clear_dir(self.root)
        credentials._rejected_tokens.clear()
        if "ABSTRA_API_TOKEN" in os.environ:
            del os.environ["ABSTRA_API_TOKEN"]

    def test_get_credentials_when_empty(self):
        self.assertIsNone(get_credentials())

    def test_get_credentials_when_file(self):
        self.root.joinpath(DOT_ABSTRA_DIR).mkdir(exist_ok=True)
        self.root.joinpath(CREDENTIALS_FILEPATH).write_text("test")
        self.assertEqual(get_credentials(), "test")

    def test_get_credentials_when_env(self):
        os.environ["ABSTRA_API_TOKEN"] = "test"
        self.assertEqual(get_credentials(), "test")

    def test_set_credentials(self):
        set_credentials("test")
        self.assertEqual(get_credentials(), "test")

    def test_delete_credentials(self):
        set_credentials("test")
        delete_credentials()
        self.assertIsNone(get_credentials())

    def test_resolve_headers_when_empty(self):
        self.assertIsNone(resolve_headers())

    def test_resolve_headers_with_credentials(self):
        set_credentials("test")
        self.assertEqual(resolve_headers(), {"Api-Authorization": "Bearer test"})


class RejectedCredentialsTest(unittest.TestCase):
    """The environment token always wins, except in the one case the in-place
    repair exists for: cloud-api rejected it and something newer is on disk."""

    ENV_TOKEN = "token-from-the-deployment"
    FILE_TOKEN = "token-stored-at-runtime"

    def setUp(self):
        self.root = init_dir()
        credentials._rejected_tokens.clear()

    def tearDown(self):
        clear_dir(self.root)
        credentials._rejected_tokens.clear()
        if "ABSTRA_API_TOKEN" in os.environ:
            del os.environ["ABSTRA_API_TOKEN"]

    def _write_file_token(self, token: str) -> None:
        self.root.joinpath(DOT_ABSTRA_DIR).mkdir(exist_ok=True)
        self.root.joinpath(CREDENTIALS_FILEPATH).write_text(token)

    def test_environment_wins_over_the_file(self):
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        self._write_file_token(self.FILE_TOKEN)
        self.assertEqual(get_credentials(), self.ENV_TOKEN)

    def test_file_takes_over_once_the_environment_token_is_rejected(self):
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        self._write_file_token(self.FILE_TOKEN)
        mark_token_rejected(self.ENV_TOKEN)
        self.assertEqual(get_credentials(), self.FILE_TOKEN)

    def test_rejected_environment_token_stays_when_there_is_no_file(self):
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        mark_token_rejected(self.ENV_TOKEN)
        self.assertEqual(get_credentials(), self.ENV_TOKEN)

    def test_rejected_environment_token_stays_when_the_file_is_rejected_too(self):
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        self._write_file_token(self.FILE_TOKEN)
        mark_token_rejected(self.ENV_TOKEN)
        mark_token_rejected(self.FILE_TOKEN)
        self.assertEqual(get_credentials(), self.ENV_TOKEN)

    def test_local_install_still_reads_the_file(self):
        self._write_file_token(self.FILE_TOKEN)
        self.assertEqual(get_credentials(), self.FILE_TOKEN)

    def test_empty_credentials_file_is_not_a_credential(self):
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        self._write_file_token("   \n")
        mark_token_rejected(self.ENV_TOKEN)
        self.assertEqual(get_credentials(), self.ENV_TOKEN)

    def test_storing_credentials_keeps_the_rejected_token_out_of_the_way(self):
        # The repair stores a live token while the environment still holds the
        # revoked one. Un-rejecting anything here would hand the revoked token
        # back on the next call, which 401s, re-flags it and repairs again: the
        # editor flaps instead of recovering.
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        mark_token_rejected(self.ENV_TOKEN)
        set_credentials(self.FILE_TOKEN)
        self.assertEqual(get_credentials(), self.FILE_TOKEN)

    def test_storing_a_previously_rejected_token_un_rejects_it(self):
        # cloud-api can legitimately hand back a token that was rejected before
        # (a transient 401, or the same key still being the current one), and it
        # must become usable again — but only that one.
        os.environ["ABSTRA_API_TOKEN"] = self.ENV_TOKEN
        mark_token_rejected(self.ENV_TOKEN)
        mark_token_rejected(self.FILE_TOKEN)
        set_credentials(self.FILE_TOKEN)
        self.assertEqual(get_credentials(), self.FILE_TOKEN)

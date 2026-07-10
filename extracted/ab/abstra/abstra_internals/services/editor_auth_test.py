import time
import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.services.editor_auth import (
    RENEW_THRESHOLD_SECONDS,
    EditorAuthRenewer,
)


class ImmediateThread:
    """Runs the target synchronously on start() so tests are deterministic."""

    def __init__(self, target, args=(), **kwargs):
        self._target = target
        self._args = args

    def start(self):
        self._target(*self._args)


@patch("abstra_internals.services.editor_auth.threading.Thread", ImmediateThread)
@patch("abstra_internals.services.editor_auth.save_editor_auth_token_to_file")
class TestEditorAuthRenewer(unittest.TestCase):
    def test_renews_token_near_expiration(self, mock_save):
        renew_fn = MagicMock(return_value="new-token")
        renewer = EditorAuthRenewer(renew_fn=renew_fn)

        renewer.maybe_renew("old-token", exp=time.time() + 3600)

        renew_fn.assert_called_once_with("old-token")
        self.assertEqual(renewer.fresh_token_for("old-token"), "new-token")
        mock_save.assert_called_once_with("new-token")

    def test_does_not_renew_fresh_token(self, mock_save):
        renew_fn = MagicMock(return_value="new-token")
        renewer = EditorAuthRenewer(renew_fn=renew_fn)

        renewer.maybe_renew(
            "old-token", exp=time.time() + RENEW_THRESHOLD_SECONDS + 3600
        )

        renew_fn.assert_not_called()
        self.assertIsNone(renewer.fresh_token_for("old-token"))
        mock_save.assert_not_called()

    def test_does_not_renew_expired_token(self, mock_save):
        renew_fn = MagicMock(return_value="new-token")
        renewer = EditorAuthRenewer(renew_fn=renew_fn)

        renewer.maybe_renew("old-token", exp=time.time() - 10)

        renew_fn.assert_not_called()
        mock_save.assert_not_called()

    def test_renews_only_once_per_token(self, mock_save):
        renew_fn = MagicMock(return_value="new-token")
        renewer = EditorAuthRenewer(renew_fn=renew_fn)
        exp = time.time() + 3600

        renewer.maybe_renew("old-token", exp=exp)
        renewer.maybe_renew("old-token", exp=exp)

        renew_fn.assert_called_once()

    def test_failed_renewal_is_throttled(self, mock_save):
        renew_fn = MagicMock(return_value=None)
        renewer = EditorAuthRenewer(renew_fn=renew_fn)
        exp = time.time() + 3600

        renewer.maybe_renew("old-token", exp=exp)
        renewer.maybe_renew("old-token", exp=exp)  # within retry interval

        renew_fn.assert_called_once()
        self.assertIsNone(renewer.fresh_token_for("old-token"))
        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()

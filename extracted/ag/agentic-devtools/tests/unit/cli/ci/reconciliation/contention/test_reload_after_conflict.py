"""Refresh the CAS anchor only after the contention delay."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.reconciliation.contention import reload_after_conflict


def test_delay_precedes_load():
    store = MagicMock()
    with patch("agentic_devtools.cli.ci.reconciliation.contention.wait_for_contention") as wait:
        wait.side_effect = lambda _: store.load.assert_not_called()
        assert reload_after_conflict(store, 2) is store.load.return_value
    wait.assert_called_once_with(2)
    store.load.assert_called_once()

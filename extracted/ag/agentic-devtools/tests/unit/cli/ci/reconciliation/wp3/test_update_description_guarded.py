from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.reconciliation.wp3 import description_hash, update_description_guarded


def test_updates_against_exact_body_hash() -> None:
    provider = Mock()
    provider.get_pr_description.return_value = "human context"
    result = update_description_guarded(
        provider, pr_number=1, edit="\n\nbatch summary", expected_hash=description_hash("human context")
    )
    assert result == "updated"
    provider.update_pr_description.assert_called_once()


def test_rejects_concurrent_edit_and_supports_no_change() -> None:
    provider = Mock()
    provider.get_pr_description.return_value = "changed"
    with pytest.raises(RuntimeError, match="concurrently"):
        update_description_guarded(provider, pr_number=1, edit="\nsummary", expected_hash=description_hash("old"))
    provider.get_pr_description.return_value = "same"
    assert (
        update_description_guarded(provider, pr_number=1, edit="", expected_hash=description_hash("same"))
        == "no_change"
    )
    with pytest.raises(ValueError):
        update_description_guarded(provider, pr_number=0, edit="", expected_hash="")

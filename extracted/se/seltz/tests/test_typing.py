"""Module-level calls so mypy checks the documented forms.

The client's `fields` annotation was once the generated message rather than the input
type, so every documented mapping form failed a consumer's mypy while the suite stayed
green -- `examples/` wraps its calls in unannotated functions, whose bodies mypy skips.
These are at module scope, where it does not.

Nothing here runs a request; the calls are never made.
"""

from typing import TYPE_CHECKING

from seltz import ContentOptions, Fields, Seltz
from seltz.services.search_service import FieldsInput

if TYPE_CHECKING:

    def _accepts_the_documented_forms(client: Seltz) -> None:
        client.search("q", fields={"content": True, "snippets": True})
        client.search("q", fields={"snippets": True})
        client.search("q", fields={"content": {"max_characters_per_result": 500}})
        client.search("q", fields=Fields(content=True))
        client.search(
            "q", fields=Fields(content=ContentOptions(max_characters_per_result=500))
        )

    def _refuses_a_misspelled_member(client: Seltz) -> None:
        client.search("q", fields={"contnt": True})  # type: ignore[arg-type]  # codespell:ignore

    def _refuses_a_wrong_value_type(client: Seltz) -> None:
        client.search("q", fields={"content": "yes"})  # type: ignore[arg-type]

    def _refuses_a_generated_member_name(client: Seltz) -> None:
        client.search("q", fields={"content_enabled": True})  # type: ignore[arg-type]

    _named: FieldsInput = {"content": True}

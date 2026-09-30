"""Published tool-kind payloads remain readable through the row-access cutover."""

from matrx_ai.tools.kinds.agent_ops import OfficeToolResult
from matrx_ai.tools.kinds.kind_authoring import KindCreateResult, KindDefinitionDetail
from matrx_ai.tools.kinds.kind_components import KindComponentContext
from matrx_ai.tools.kinds.kind_instances import KindInstanceDetail
from matrx_ai.tools.kinds.personal_content import NoteToolResult


def test_t13_adds_row_access_without_rejecting_legacy_visibility_payloads() -> None:
    """Every changed published shape accepts its pre-T-13 wire payload."""
    assert KindCreateResult.model_validate({"visibility": "private"}).visibility == "private"
    assert (
        KindDefinitionDetail.model_validate({"kind": {"visibility": "public"}})
        .kind.visibility
        == "public"
    )
    assert (
        KindComponentContext.model_validate({"kind": {"visibility": "link"}})
        .kind.visibility
        == "link"
    )
    assert (
        KindInstanceDetail.model_validate({"instance": {"visibility": "private"}})
        .instance.visibility
        == "private"
    )
    assert OfficeToolResult.model_validate({"action": "generate", "visibility": "public"}).visibility == "public"
    assert NoteToolResult.model_validate({"visibility": "private"}).visibility == "private"

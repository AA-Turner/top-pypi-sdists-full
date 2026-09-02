"""Kind for the ``user_secret_set`` tool result (KIND_TOOL_LEDGER,
``lead-w2f``). Implementation:
``matrx_ai/tools/implementations/user_secrets_tool.py`` — a package-hosted
tool, so it instantiates the model inline (the ``sql`` precedent) rather than
funnelling through aidream's ``stamp_result_kind``.

PLACEHOLDER tier: the receipt IS five scalars and a note. The secret VALUE
never appears — only the vault's masked ``value_hint``.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "user_secret_receipt",
    label="User Secret Receipt",
    family="user_secrets",
    example={
        "saved": True,
        "key": "GITHUB_TOKEN",
        "value_hint": "ghp_…abcd",
        "category": "custom",
        "inject_into_sandbox": True,
        "note": "Stored encrypted.",
    },
    maturity="placeholder",
)
class UserSecretReceipt(KindModel):
    saved: bool = True
    key: str = ""
    #: The vault's masked preview — never the value.
    value_hint: str | None = None
    category: str | None = None
    inject_into_sandbox: bool | None = None
    note: str | None = None


__all__ = ["UserSecretReceipt"]

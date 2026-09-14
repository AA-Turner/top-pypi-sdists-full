from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class MailTipsError(ClientValue):
    code: str | None = None
    message: str | None = None
    ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailTipsError"

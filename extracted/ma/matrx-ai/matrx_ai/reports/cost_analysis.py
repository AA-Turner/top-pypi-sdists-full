from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from matrx_utils import vcprint


@dataclass(frozen=True)
class UserRequestCostRollup:
    """Authoritative cost/usage totals for one cx_user_request, summed from its
    committed cx_request rows (parent turns AND every sub-agent under the same
    user_request_id). One user click = one cx_user_request = this total.

    Includes rows of ANY status, including ``failed`` — a provider bills us the
    instant a call starts, so a failed row that carries cost MUST be counted.
    Soft-deleted rows (``deleted_at`` set) are excluded.
    """

    user_request_id: str
    request_count: int
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    total_tokens: int
    total_cost: Decimal
    api_duration_ms: int
    tool_duration_ms: int
    total_duration_ms: int
    total_tool_calls: int


@dataclass
class ConversationCostSummary:
    conversation_id: str
    request_count: int
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    total_tokens: int
    total_cost: Decimal
    total_api_duration_ms: int
    total_duration_ms: int
    avg_api_duration_ms: float
    avg_duration_ms: float
    models_used: list[str] = field(default_factory=list)
    providers: list[str] = field(default_factory=list)

    def print_summary(self, label: str = "Conversation Cost Summary") -> None:
        total_cost_str = f"${float(self.total_cost):.6f}"
        avg_api_s = f"{self.avg_api_duration_ms / 1000:.2f}s"
        avg_total_s = f"{self.avg_duration_ms / 1000:.2f}s"
        total_api_s = f"{self.total_api_duration_ms / 1000:.1f}s"
        total_wall_s = f"{self.total_duration_ms / 1000:.1f}s"

        vcprint(
            f"\n{'=' * 60}\n"
            f"{label}\n"
            f"  Conversation: {self.conversation_id}\n"
            f"  Requests:     {self.request_count}\n"
            f"{'=' * 60}\n"
            f"  Tokens\n"
            f"    Input:      {self.input_tokens:,}\n"
            f"    Output:     {self.output_tokens:,}\n"
            f"    Cached:     {self.cached_tokens:,}\n"
            f"    Total:      {self.total_tokens:,}\n"
            f"{'=' * 60}\n"
            f"  Cost:         {total_cost_str}\n"
            f"{'=' * 60}\n"
            f"  Timing\n"
            f"    API total:  {total_api_s}  (avg {avg_api_s}/req)\n"
            f"    Wall total: {total_wall_s}  (avg {avg_total_s}/req)\n"
            f"{'=' * 60}",
            color="cyan",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "request_count": self.request_count,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cached_tokens": self.cached_tokens,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "total_api_duration_ms": self.total_api_duration_ms,
            "total_duration_ms": self.total_duration_ms,
            "avg_api_duration_ms": self.avg_api_duration_ms,
            "avg_duration_ms": self.avg_duration_ms,
            "models_used": self.models_used,
            "providers": self.providers,
        }

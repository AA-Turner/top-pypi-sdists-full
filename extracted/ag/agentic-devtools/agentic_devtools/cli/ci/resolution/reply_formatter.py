"""Structured reply formatter for thread resolution audit trail.

Generates replies with HTML markers for machine parsing and human-readable
explanations for reviewers.
"""

from __future__ import annotations

from agentic_devtools.cli.ci.resolution.models import (
    ResolutionBasis,
    ResolutionReply,
    ResolutionVerdict,
    TierResult,
)


class ReplyFormatter:
    """Builds structured replies for resolved/tentative threads.

    Replies include:
    - An HTML comment marker for programmatic identification
    - A confidence indicator
    - The tier that produced the verdict
    - A human-readable explanation
    - Model ID (for SDK tier evaluations)
    """

    def format_resolution_reply(self, result: TierResult, model_id: str | None = None) -> ResolutionReply:
        """Format a tier result into a structured reply.

        Args:
            result: The evaluation result to format.
            model_id: Optional model identifier (for SDK tier).

        Returns:
            A ResolutionReply with HTML marker and human text.
        """
        basis = result.resolution_basis.value if result.resolution_basis else "unspecified"
        html_marker = f"<!-- agdt:resolution-tier:{result.tier_name} -->"
        if result.resolution_basis:
            html_marker += f"\n<!-- agdt:resolution-basis:{basis} -->"

        # Build human-readable text
        verdict_emoji = self._verdict_emoji(result.verdict)
        confidence_indicator = f"[{result.confidence}]"

        status_text = {
            ResolutionVerdict.RESOLVE: "Thread resolved",
            ResolutionVerdict.UNRESOLVE: "Thread left open",
            ResolutionVerdict.TENTATIVE: "Tentative resolution",
        }.get(result.verdict, "Thread evaluation")

        parts: list[str] = [
            f"{verdict_emoji} **{status_text}** {confidence_indicator}",
            "",
            f"**Tier**: {result.tier_name}",
            f"**Basis**: {basis}",
            f"**Rationale**: {result.explanation}",
        ]

        if model_id:
            parts.append(f"**Model**: {model_id}")

        if result.verdict == ResolutionVerdict.TENTATIVE:
            parts.append("")
            parts.append("_This thread will be re-evaluated in subsequent iterations._")

        human_text = "\n".join(parts)

        return ResolutionReply(
            html_marker=html_marker,
            human_text=human_text,
            model_id=model_id,
            resolution_basis=result.resolution_basis,
        )

    def format_unconfirmed_commit_change_reply(
        self,
        tier_result: TierResult,
        model_id: str | None = None,
        resolution_basis: ResolutionBasis | None = None,
    ) -> str:
        """Format a reply for threads resolved by default due to HEAD change.

        Used when the SDK could not confirm resolution (unreachable, timeout,
        malformed, or ambiguous response) but HEAD has changed since the review.
        These threads are eligible for re-evaluation on subsequent runs.

        Args:
            tier_result: The tier result carrying the actual tier name,
                confidence, and explanation to include in the reply.
            model_id: Optional model identifier (for SDK tier).
            resolution_basis: Optional structured basis for the resolution.
        """
        basis = resolution_basis or tier_result.resolution_basis
        marker = "<!-- agdt:resolution-tier:unconfirmed-commit-change -->"
        parts: list[str] = [
            marker,
            f"🔄 **Thread resolved** (unconfirmed) [{tier_result.confidence}]",
            "",
            f"**Tier**: {tier_result.tier_name}",
        ]
        if basis is not None:
            parts.insert(1, f"<!-- agdt:resolution-basis:{basis.value} -->")
            parts.append(f"**Basis**: {basis.value}")
        parts.append(f"**Rationale**: {tier_result.explanation}")
        if model_id:
            parts.append(f"**Model**: {model_id}")
        parts.append("")
        parts.append("_This thread will be re-evaluated in subsequent iterations._")
        return "\n".join(parts)

    def format_abandoned_reply(self) -> str:
        """Format a reply for threads whose tentative resolution has expired."""
        return (
            "<!-- agdt:resolution-tier:abandoned -->\n"
            "⚠️ **Resolution abandoned** — manual review required.\n\n"
            "The tentative resolution for this thread has expired after reaching "
            "the maximum re-evaluation attempts. Please review manually."
        )

    def build_full_reply(self, result: TierResult, model_id: str | None = None) -> str:
        """Build the complete reply body including HTML marker and human text."""
        reply = self.format_resolution_reply(result, model_id)
        return f"{reply.html_marker}\n{reply.human_text}"

    @staticmethod
    def _verdict_emoji(verdict: ResolutionVerdict) -> str:
        """Map verdict to emoji indicator."""
        return {
            ResolutionVerdict.RESOLVE: "✅",
            ResolutionVerdict.UNRESOLVE: "❌",
            ResolutionVerdict.TENTATIVE: "🔄",
        }.get(verdict, "❓")

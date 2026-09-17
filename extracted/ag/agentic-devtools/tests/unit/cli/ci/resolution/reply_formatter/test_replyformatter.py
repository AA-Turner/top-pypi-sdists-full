"""Tests for ReplyFormatter."""

from agentic_devtools.cli.ci.resolution.models import ResolutionBasis, ResolutionVerdict, TierResult
from agentic_devtools.cli.ci.resolution.reply_formatter import ReplyFormatter


class TestReplyFormatter:
    """Tests for the reply formatter."""

    def test_format_resolve_reply(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="high",
            tier_name="outdated",
            explanation="Thread is outdated.",
        )
        reply = formatter.format_resolution_reply(result)
        assert reply.html_marker == "<!-- agdt:resolution-tier:outdated -->"
        assert "Thread resolved" in reply.human_text
        assert "[high]" in reply.human_text
        assert "**Basis**: unspecified" in reply.human_text
        assert reply.model_id is None

    def test_format_tentative_reply(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.TENTATIVE,
            confidence="low",
            tier_name="engine",
            explanation="No tier could determine.",
        )
        reply = formatter.format_resolution_reply(result)
        assert "Tentative resolution" in reply.human_text
        assert "re-evaluated" in reply.human_text

    def test_format_with_model_id(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="medium",
            tier_name="sdk_evaluation",
            explanation="SDK resolved.",
        )
        reply = formatter.format_resolution_reply(result, model_id="claude-sonnet-4.6")
        assert reply.model_id == "claude-sonnet-4.6"
        assert "claude-sonnet-4.6" in reply.human_text

    def test_format_abandoned_reply(self) -> None:
        formatter = ReplyFormatter()
        reply = formatter.format_abandoned_reply()
        assert "abandoned" in reply.lower()
        assert "manual review required" in reply.lower()
        assert "<!-- agdt:resolution-tier:abandoned -->" in reply

    def test_format_unresolve_reply(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.UNRESOLVE,
            confidence="high",
            tier_name="diff_heuristic",
            explanation="No relevant changes found.",
        )
        reply = formatter.format_resolution_reply(result)
        assert reply.html_marker == "<!-- agdt:resolution-tier:diff_heuristic -->"
        assert "Thread left open" in reply.human_text
        assert "❌" in reply.human_text
        assert "[high]" in reply.human_text
        assert reply.model_id is None

    def test_format_reply_includes_resolution_basis(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="high",
            tier_name="sdk_evaluation",
            explanation="The reviewer explicitly rejected the concern.",
            resolution_basis=ResolutionBasis.EXPLICIT_REJECTION,
        )
        reply = formatter.format_resolution_reply(result)
        assert "<!-- agdt:resolution-tier:sdk_evaluation -->" in reply.html_marker
        assert "<!-- agdt:resolution-basis:explicit_rejection -->" in reply.html_marker
        assert "**Basis**: explicit_rejection" in reply.human_text
        assert reply.resolution_basis == ResolutionBasis.EXPLICIT_REJECTION

    def test_build_full_reply(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="high",
            tier_name="outdated",
            explanation="Thread is outdated.",
        )
        full_reply = formatter.build_full_reply(result)
        assert full_reply.startswith("<!-- agdt:resolution-tier:outdated -->")
        assert "Thread resolved" in full_reply

    def test_format_unconfirmed_commit_change_reply(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="low",
            tier_name="engine_fallback",
            explanation="SDK evaluation could not produce a verdict — resolved by default due to HEAD change.",
        )
        reply = formatter.format_unconfirmed_commit_change_reply(result)
        assert "<!-- agdt:resolution-tier:unconfirmed-commit-change -->" in reply
        assert "**Thread resolved** (unconfirmed)" in reply
        assert "[low]" in reply
        assert "**Tier**: engine_fallback" in reply
        assert "HEAD change" in reply
        assert "finalized" in reply

    def test_format_unconfirmed_commit_change_reply_with_real_tier(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="medium",
            tier_name="sdk_evaluation_fallback",
            explanation="SDK fallback produced an ambiguous result.",
        )
        reply = formatter.format_unconfirmed_commit_change_reply(result, model_id="claude-sonnet-4.6")
        assert "<!-- agdt:resolution-tier:unconfirmed-commit-change -->" in reply
        assert "**Thread resolved** (unconfirmed)" in reply
        assert "[medium]" in reply
        assert "**Tier**: sdk_evaluation_fallback" in reply
        assert "SDK fallback produced an ambiguous result." in reply
        assert "**Model**: claude-sonnet-4.6" in reply
        assert "finalized" in reply

    def test_format_unconfirmed_commit_change_reply_includes_resolution_basis(self) -> None:
        formatter = ReplyFormatter()
        result = TierResult(
            verdict=ResolutionVerdict.RESOLVE,
            confidence="low",
            tier_name="sdk_evaluation_fallback",
            explanation="The reviewer rejected the concern.",
            resolution_basis=ResolutionBasis.EXPLICIT_REJECTION,
        )

        reply = formatter.format_unconfirmed_commit_change_reply(result)

        assert "<!-- agdt:resolution-tier:unconfirmed-commit-change -->" in reply
        assert "<!-- agdt:resolution-basis:explicit_rejection -->" in reply
        assert "basis=explicit_rejection" not in reply
        assert "**Basis**: explicit_rejection" in reply

"""Tests for the ``PrereqCheckResult`` dataclass."""

from pathlib import Path

from agentic_devtools.cli.speckit.scaffold_check_prereqs import PrereqCheckResult


class TestPrereqCheckResult:
    """PrereqCheckResult stores the feature dir and available docs."""

    def test_defaults_to_empty_docs(self) -> None:
        result = PrereqCheckResult(feature_dir=Path("/repo/specs/042-x"))

        assert result.available_docs == []

    def test_to_dict_returns_json_serialisable_mapping(self) -> None:
        result = PrereqCheckResult(
            feature_dir=Path("/repo/specs/042-x"),
            available_docs=["spec.md", "contracts/"],
        )

        assert result.to_dict() == {
            "FEATURE_DIR": str(Path("/repo/specs/042-x")),
            "AVAILABLE_DOCS": ["spec.md", "contracts/"],
        }

    def test_to_dict_returns_a_copy_of_available_docs(self) -> None:
        docs = ["spec.md"]
        result = PrereqCheckResult(feature_dir=Path("/repo/specs/042-x"), available_docs=docs)

        payload = result.to_dict()
        payload["AVAILABLE_DOCS"].append("mutated")  # type: ignore[attr-defined]

        assert result.available_docs == ["spec.md"]

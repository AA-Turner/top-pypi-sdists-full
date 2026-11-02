"""Unit tests for _run_review_provider_readiness."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def _document() -> dict:
    return {
        "providers": {
            "default": {"type": "local_model", "model": "default", "endpoint": "http://localhost"},
            "review": {"type": "local_model", "model": "review", "endpoint": "http://localhost"},
        },
        "workflows": {
            "pr_review": {
                "default_provider": "default",
                "nodes": {"review_files": {"provider": "review"}},
            }
        },
    }


def test__run_review_provider_readiness_short_circuits_when_default_fails() -> None:
    def _ready(document: dict) -> tuple[str, str]:
        provider_id = document["workflows"]["pr_review"]["default_provider"]
        if provider_id == "default":
            return ("unavailable", "authentication_unavailable")
        return ("ready", "ready")

    assert provider_configuration._run_review_provider_readiness(
        _document(),
        default_provider_id="default",
        review_provider_id="review",
        readiness=_ready,
    ) == ("unavailable", "authentication_unavailable", "default", "default")


def test__run_review_provider_readiness_skips_duplicate_review_preflight() -> None:
    calls: list[str] = []

    def _ready(document: dict) -> tuple[str, str]:
        calls.append(document["workflows"]["pr_review"]["default_provider"])
        return ("ready", "ready")

    result = provider_configuration._run_review_provider_readiness(
        _document(),
        default_provider_id="default",
        review_provider_id="default",
        readiness=_ready,
    )

    assert result == ("ready", "ready", "default", "default")
    assert calls == ["default"]


def test__run_review_provider_readiness_rechecks_same_provider_with_distinct_node_model() -> None:
    calls: list[tuple[str, str | None]] = []
    document = _document()
    document["workflows"]["pr_review"]["nodes"]["review_files"] = {
        "provider": "default",
        "model": "override",
    }

    def _ready(candidate: dict) -> tuple[str, str]:
        review = candidate["workflows"]["pr_review"]
        calls.append((review["default_provider"], review["nodes"]["review_files"].get("model")))
        return ("ready", "ready")

    result = provider_configuration._run_review_provider_readiness(
        document,
        default_provider_id="default",
        review_provider_id="default",
        readiness=_ready,
    )

    assert result == ("ready", "ready", "default", "override")
    assert calls == [("default", None), ("default", "override")]


def test__run_review_provider_readiness_reports_workflow_override_model_on_default_failure() -> None:
    document = _document()
    document["workflows"]["pr_review"]["model"] = "workflow-override"

    def _ready(candidate: dict) -> tuple[str, str]:
        if candidate["workflows"]["pr_review"]["default_provider"] == "default":
            return ("unavailable", "model_unavailable")
        return ("ready", "ready")

    assert provider_configuration._run_review_provider_readiness(
        document,
        default_provider_id="default",
        review_provider_id="review",
        readiness=_ready,
    ) == ("unavailable", "model_unavailable", "default", "workflow-override")


def test__run_review_provider_readiness_rechecks_same_provider_with_distinct_workflow_and_node_models() -> None:
    calls: list[tuple[str, str | None, str | None]] = []
    document = _document()
    document["workflows"]["pr_review"]["default_provider"] = "default"
    document["workflows"]["pr_review"]["model"] = "workflow-override"
    document["workflows"]["pr_review"]["nodes"]["review_files"] = {
        "provider": "default",
        "model": "node-override",
    }

    def _ready(candidate: dict) -> tuple[str, str]:
        review = candidate["workflows"]["pr_review"]
        calls.append((review["default_provider"], review.get("model"), review["nodes"]["review_files"].get("model")))
        return ("ready", "ready")

    result = provider_configuration._run_review_provider_readiness(
        document,
        default_provider_id="default",
        review_provider_id="default",
        readiness=_ready,
    )

    assert result == ("ready", "ready", "default", "node-override")
    assert calls == [("default", "workflow-override", None), ("default", "workflow-override", "node-override")]


def test__run_review_provider_readiness_uses_provider_model_for_distinct_default_preflight() -> None:
    calls: list[tuple[str, str | None]] = []
    document = _document()
    document["workflows"]["pr_review"]["nodes"]["review_files"]["model"] = "review-override"

    def _ready(candidate: dict) -> tuple[str, str]:
        review = candidate["workflows"]["pr_review"]
        calls.append(
            (
                review["default_provider"],
                review["nodes"]["review_files"].get("model"),
            )
        )
        return ("ready", "ready")

    result = provider_configuration._run_review_provider_readiness(
        document,
        default_provider_id="default",
        review_provider_id="review",
        readiness=_ready,
    )

    assert result == ("ready", "ready", "review", "review-override")
    assert calls == [("default", None), ("review", "review-override")]

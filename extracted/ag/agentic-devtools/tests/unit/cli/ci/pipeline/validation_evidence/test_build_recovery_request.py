from agentic_devtools.cli.ci.pipeline.validation_evidence import (
    RECOVERY_MARKER,
    build_recovery_request,
)


def test_builds_one_head_specific_validation_request_with_final_marker() -> None:
    head_sha = "0123456789abcdef0123456789abcdef01234567"

    request = build_recovery_request(head_sha)

    assert request.startswith("@copilot")
    assert "ONE final PR comment" in request
    assert "## Validation evidence" in request
    assert head_sha in request
    assert "or the new head SHA if you push" in request
    assert "bash scripts/targeted-checks.sh" in request
    assert "python -m pytest tests/unit/cli/ci/pipeline/validation_evidence" in request
    assert "platform" in request.lower()
    assert "python version" in request.lower()
    assert "pytest version" in request.lower()
    assert "results" in request.lower()
    assert "Do not make code changes unless validation fails" in request
    assert request.splitlines()[-1] == RECOVERY_MARKER

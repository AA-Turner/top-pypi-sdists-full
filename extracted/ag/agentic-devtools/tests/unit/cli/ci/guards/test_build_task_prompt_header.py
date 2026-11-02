from agentic_devtools.cli.ci.guards import build_task_prompt_header, validate_dispatch_identity

SHA = "b" * 40


def test_builds_header_from_identity_token() -> None:
    identity = validate_dispatch_identity("repo-name", 8, SHA, 2)

    assert build_task_prompt_header(identity).endswith(identity.token)

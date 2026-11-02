from agentic_devtools.cli.ci import guards as guards_module


def test_matches_only_supported_first_line_headers() -> None:
    token = "agdt-dispatch-repo-8-" + ("b" * 40) + "-2"
    assert guards_module._has_exact_prompt_header(f"agdt-dispatch-token: {token}\nrest", token)
    assert guards_module._has_exact_prompt_header(f"dispatch-token={token}\nrest", token)
    assert not guards_module._has_exact_prompt_header(None, token)
    assert not guards_module._has_exact_prompt_header(f"prefix agdt-dispatch-token: {token}", token)

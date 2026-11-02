from agentic_devtools.ai_providers.availability import _CANONICAL_BODY_PREFIX, render_canonical_body


def test_render_canonical_body_prefixes_required_marker() -> None:
    body = render_canonical_body({"claude-opus-5": "available"})

    assert body.startswith(_CANONICAL_BODY_PREFIX + "\n")


def test_render_canonical_body_escapes_markdown_table_cells() -> None:
    body = render_canonical_body({"model\\preview|beta\ngamma": "available"})

    assert "| model\\\\preview\\|beta gamma | available |" in body

from agentic_devtools.cli.setup.copilot_settings import _render_value


def test_returns_scalar_without_extra_indentation():
    assert _render_value(True, "    ", "\n") == "true"

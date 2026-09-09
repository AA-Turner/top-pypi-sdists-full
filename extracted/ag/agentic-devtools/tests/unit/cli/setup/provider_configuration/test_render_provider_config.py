"""Unit tests for render_provider_config."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test_render_provider_config_uses_stable_yaml_shape() -> None:
    document = {
        "providers": {"copilot_pr_review": {"type": "copilot", "model": "model-a"}},
        "workflows": {
            "pr_review": {
                "default_provider": "copilot_pr_review",
                "nodes": {"review_files": {"provider": "copilot_pr_review"}},
            }
        },
    }

    assert provider_configuration.render_provider_config(document).startswith("providers:")

"""Tests for _build_stash_push_args."""

from agentic_devtools.cli.setup.pr_workflow import _build_stash_push_args


class TestBuildStashPushArgs:
    """Tests for _build_stash_push_args."""

    def test_excludes_generated_setup_paths(self):
        """Stash push excludes agdt-generated files from the auto-stash."""
        args = _build_stash_push_args()

        assert args[:4] == ["stash", "push", "--include-untracked", "-m"]
        assert args[4] == "agdt-setup: auto-stash"
        assert args[-4] == "."
        assert args[-3:] == [
            ":(exclude).agdt/**",
            ":(exclude).github/agents/agdt.*",
            ":(exclude).github/prompts/agdt.*",
        ]

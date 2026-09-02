"""Tests for _is_agentic_devtools_tilde_backup."""

from agentic_devtools.cli.setup.script_generators.required_setup import _is_agentic_devtools_tilde_backup


class TestIsAgenticDevtoolsTildeBackup:
    """Tests for _is_agentic_devtools_tilde_backup."""

    def test_detects_exact_tilde_backups(self) -> None:
        """Exact pip backup directory names are recognised."""
        assert _is_agentic_devtools_tilde_backup("~gentic-devtools") is True
        assert _is_agentic_devtools_tilde_backup("~gentic_devtools") is True

    def test_detects_dist_info_and_dev_local_versions(self) -> None:
        """Versioned pip backups stay recognised for release and dev/local builds."""
        assert _is_agentic_devtools_tilde_backup("~gentic-devtools.dist-info") is True
        assert _is_agentic_devtools_tilde_backup("~gentic_devtools-0.2.401.dist-info") is True
        assert _is_agentic_devtools_tilde_backup("~gentic-devtools-0.2.380") is True
        assert _is_agentic_devtools_tilde_backup("~gentic-devtools-0.2.9.dev1+g1234abc.dist-info") is True
        assert _is_agentic_devtools_tilde_backup("~GENTIC_devtools-0.2.401.dist-info") is True

    def test_rejects_unrelated_tilde_prefixed_names(self) -> None:
        """The helper does not overmatch similarly named backup directories."""
        assert _is_agentic_devtools_tilde_backup("~gentic-devtoolsextra") is False
        assert _is_agentic_devtools_tilde_backup("~gentic-devtools-2-extra-1.0.dist-info") is False
        assert _is_agentic_devtools_tilde_backup("~gentic-devtools-extra-1.0.0.dist-info") is False
        assert _is_agentic_devtools_tilde_backup("~someother-package") is False
        assert _is_agentic_devtools_tilde_backup("~gentic-other") is False

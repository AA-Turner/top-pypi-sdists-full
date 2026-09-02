"""Tests for _is_agentic_devtools_distribution_name."""

from agentic_devtools.cli.setup.script_generators.required_setup import _is_agentic_devtools_distribution_name


class TestIsAgenticDevtoolsDistributionName:
    """Tests for _is_agentic_devtools_distribution_name."""

    def test_detects_bare_distribution_names(self) -> None:
        """The helper recognises the bare distribution names."""
        assert _is_agentic_devtools_distribution_name("agentic-devtools") is True
        assert _is_agentic_devtools_distribution_name("agentic_devtools") is True

    def test_detects_pip_mangled_dist_info_names(self) -> None:
        """The helper recognises pip's ~-mangled dist-info backup names."""
        assert _is_agentic_devtools_distribution_name("~gentic_devtools-0.2.380.dist-info") is True
        assert _is_agentic_devtools_distribution_name("~gentic_devtools-0.2.9.dev1+g1234abc.dist-info") is True

    def test_detects_versioned_dist_info_names(self) -> None:
        """The helper recognises versioned agentic-devtools dist-info names."""
        assert _is_agentic_devtools_distribution_name("agentic_devtools-1.0.0.dist-info") is True
        assert _is_agentic_devtools_distribution_name("agentic-devtools-0.2.9.dev1+g1234abc.dist-info") is True
        assert _is_agentic_devtools_distribution_name("AGENTIC_devtools-1.0.0.dist-info") is True

    def test_rejects_unrelated_names(self) -> None:
        """The helper leaves similarly named packages alone."""
        assert _is_agentic_devtools_distribution_name("agentic-devtools-extra-1.0.0.dist-info") is False
        assert _is_agentic_devtools_distribution_name("agentic-devtools-2-extra-1.0.dist-info") is False
        assert _is_agentic_devtools_distribution_name("agentic_devtools_extra-1.0.0.dist-info") is False
        assert _is_agentic_devtools_distribution_name("~gentic-devtools-2-extra-1.0.dist-info") is False
        assert _is_agentic_devtools_distribution_name("~gentic-devtools-extra-1.0.0.dist-info") is False

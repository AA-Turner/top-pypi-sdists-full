"""
Tests for CLI tier-name choice validation (PF-160).

Verifies `license upgrade` rejects the old tier names and accepts the four
new canonical names. `config init --license-tier` was removed along with
`config init`'s organization-creation logic -- license assignment happens
against an existing organization (`license upgrade`), not during user/CLI
setup.
"""

import argparse

import pytest

from src.cli.commands.license import LicenseCommands


def build_parser(setup_fn):
    parser = argparse.ArgumentParser()
    setup_fn(parser)
    return parser


class TestLicenseUpgradeChoices:
    @pytest.fixture
    def parser(self):
        return build_parser(LicenseCommands.setup_parser)

    @pytest.mark.parametrize("tier", ["guidance", "spark", "sprint", "velocity"])
    def test_accepts_new_tier_names(self, parser, tier):
        args = parser.parse_args(["upgrade", tier])
        assert args.tier == tier

    @pytest.mark.parametrize("tier", ["pro", "max", "unlimited"])
    def test_rejects_old_tier_names(self, parser, tier):
        with pytest.raises(SystemExit):
            parser.parse_args(["upgrade", tier])

"""Translate bounded Dockerfile escape-hatch fragments into ordinary typed operations."""

import shlex

from labqoat.compute.images.command_step import CommandStep
from labqoat.compute.images.env_step import EnvStep
from labqoat.compute.images.image_validation import ImageValidation
from labqoat.compute.images.workdir_step import WorkdirStep


class FragmentSteps:
    """Keep base and stage authority in the recipe while supporting common instruction spelling."""

    @staticmethod
    def parse(fragment: str) -> CommandStep | EnvStep | WorkdirStep:
        """Accept RUN, ENV and WORKDIR fragments with the same bounds as fluent operations."""
        ImageValidation.text(fragment)
        if "\n" in fragment or "\r" in fragment:
            raise ValueError("Dockerfile fragments must contain one instruction")
        kind, _, value = fragment.strip().partition(" ")
        if kind.upper() == "RUN" and not value.startswith(("--", "[")):
            return CommandStep((ImageValidation.text(value),))
        if kind.upper() == "WORKDIR":
            return WorkdirStep(ImageValidation.path(value))
        if kind.upper() == "ENV":
            return FragmentSteps._environment(value)
        raise ValueError("Supported Dockerfile fragments are shell RUN, ENV and WORKDIR")

    @staticmethod
    def _environment(value: str) -> EnvStep:
        """Decode literal key=value tokens without executing shell expansion."""
        tokens = shlex.split(value)
        if not 1 <= len(tokens) <= 128 or any("=" not in token for token in tokens):
            raise ValueError("ENV fragments require 1..128 key=value entries")
        pairs = [token.split("=", 1) for token in tokens]
        values = dict(pairs)
        if len(values) != len(pairs):
            raise ValueError("ENV fragments cannot repeat a key")
        return EnvStep(tuple(sorted(ImageValidation.environment(key, item) for key, item in values.items())))

r"""Contain a generic configuration."""

from __future__ import annotations

__all__ = ["Config"]

from dataclasses import dataclass

from zenpyre.utils.config.extra_fields import ExtraFieldsConfig


@dataclass(frozen=True)
class Config(ExtraFieldsConfig):
    r"""A generic configuration."""

    def __hash__(self) -> int:
        # @dataclass(frozen=True) auto-generates a fresh __hash__ for
        # every dataclass-decorated class unless __hash__ is already
        # present in that class's own body — merely inheriting one
        # does not suppress the override. Delegating here (rather than
        # repeating its logic) keeps ExtraFieldsConfig.__hash__ the
        # single authoritative implementation.
        return ExtraFieldsConfig.__hash__(self)

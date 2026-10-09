# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
from typing import Any, ClassVar, NamedTuple, Optional

LOGGER = logging.getLogger(__name__)


class TransferLimits(NamedTuple):
    """Where one direction's concurrency settings are read from, and their bounds."""

    config_key: str
    total_config_key: str
    default: int
    minimum: int
    maximum: int


class PartsTransferOptions:
    """How per-part parallelism is bounded, in whichever direction parts move.

    The rules are the same for sending parts and for receiving them: a per-asset
    cap that is the knob, a process-wide ceiling that follows the pool of asset
    workers unless configured, and the same clamping of both. What differs is only
    where the settings are read from and what their bounds are, which is the
    LIMITS each subclass sets.
    """

    LIMITS: ClassVar[TransferLimits]

    def __init__(self, concurrency: int, total_concurrency: Optional[int]):
        """Prefer the factories. Both values are required here so that no layer
        can quietly supply its own idea of a default."""
        self.concurrency = self._clamp_concurrency(concurrency)
        self._total_concurrency = total_concurrency

    @classmethod
    def defaults(cls):
        """The built-in defaults, in one place."""
        return cls(concurrency=cls.LIMITS.default, total_concurrency=None)

    @classmethod
    def of(cls, concurrency: int, total_concurrency: Optional[int] = None):
        """Explicit values, for tests and for callers that know what they want."""
        return cls(concurrency=concurrency, total_concurrency=total_concurrency)

    def resolve_total_concurrency(self, asset_pool_size: int) -> int:
        """Total parts in flight allowed across all assets.

        Never lower than the per-asset cap, and never lower than the asset pool
        size, so that adding per-part parallelism cannot reduce the concurrency
        a transfer already had.

        The asset pool size is used as given rather than clamped. Clamping it would
        break the promise above: an asset pool configured with 128 threads already
        ran 128 transfers at once, each holding one part, so capping the ceiling at
        64 would halve the concurrency this change is supposed to preserve. The bound
        on that number belongs to whoever sizes the asset pool. An explicitly
        configured ceiling is still clamped because that one is a knob with a
        documented range.
        """
        if self._total_concurrency is not None:
            return max(self._clamp_total(self._total_concurrency), self.concurrency)

        return max(asset_pool_size, self.concurrency)

    @classmethod
    def from_config(cls, config: Any):
        concurrency = config.get_int(None, cls.LIMITS.config_key)
        if concurrency is None:
            concurrency = cls.LIMITS.default

        return cls(
            concurrency=concurrency,
            total_concurrency=config.get_raw(None, cls.LIMITS.total_config_key),
        )

    def __repr__(self) -> str:
        return "%s(concurrency=%d, total_concurrency=%r)" % (
            type(self).__name__,
            self.concurrency,
            self._total_concurrency,
        )

    @classmethod
    def _clamp_total(cls, total: Any) -> int:
        try:
            value = int(total)
        except (TypeError, ValueError):
            return cls.LIMITS.default

        return max(cls.LIMITS.minimum, min(value, cls.LIMITS.maximum))

    @classmethod
    def _clamp_concurrency(cls, concurrency: Optional[int]) -> int:
        if concurrency is None:
            return cls.LIMITS.default

        try:
            concurrency = int(concurrency)
        except (TypeError, ValueError):
            LOGGER.debug(
                "Invalid S3 parts concurrency %r for %s, falling back to %d",
                concurrency,
                cls.LIMITS.config_key,
                cls.LIMITS.default,
            )
            return cls.LIMITS.default

        if concurrency < cls.LIMITS.minimum:
            LOGGER.debug(
                "S3 parts concurrency %d for %s is below the minimum, using %d",
                concurrency,
                cls.LIMITS.config_key,
                cls.LIMITS.minimum,
            )
            return cls.LIMITS.minimum

        if concurrency > cls.LIMITS.maximum:
            LOGGER.debug(
                "S3 parts concurrency %d for %s is above the maximum, using %d",
                concurrency,
                cls.LIMITS.config_key,
                cls.LIMITS.maximum,
            )
            return cls.LIMITS.maximum

        return concurrency

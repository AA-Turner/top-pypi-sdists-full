#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""UI schema for localize dates."""

from __future__ import annotations

import datetime
import re
from typing import TYPE_CHECKING, Any

from babel.dates import format_date
from babel_edtf import format_edtf
from flask import current_app
from marshmallow_utils.fields import (
    FormatDate,
    FormatDatetime,
    FormatEDTF,
    FormatTime,
)
from marshmallow_utils.fields.babel import BabelFormatField

if TYPE_CHECKING:
    from babel.core import Locale
    from marshmallow_utils.fields.babel import BabelFormatField as MixinBase
else:

    class MixinBase:
        """Localize date mixin."""


def current_default_locale() -> Any:
    """Get the Flask app's default locale."""
    return current_app.config.get("BABEL_DEFAULT_LOCALE", "en")


class LocalizedMixin(MixinBase):
    """Localize date mixin."""

    def __init__(self, *args: Any, locale: Locale | None = None, **kwargs: Any):
        """Construct."""
        super().__init__(*args, locale=locale, **kwargs)  # type: ignore[call-arg]

    @property
    def locale(self) -> Locale | str:
        """Get locale."""
        if self._locale:
            return self._locale
        if self.context and self.parent and "locale" in self.context:
            return self.context["locale"]
        return current_default_locale()

    def format_value(self, value: str) -> Any:
        """Format the value, gracefully handling exceptions."""
        try:
            return super().format_value(value)  # type: ignore[misc]
        except Exception:
            # Handle the exception gracefully
            current_app.logger.exception("Error formatting value '%s'", value)
            return f"«Error formatting value '{value}'»"


class LocalizedDate(LocalizedMixin, FormatDate):
    """Localize date field."""


class FormatTimeString(FormatTime):
    """Time formater."""

    def parse(
        self,
        value: Any,
        as_time: bool = False,
        as_date: bool = False,
        as_datetime: bool = False,
    ) -> Any:
        """Parse date value."""
        if value and isinstance(value, str) and as_time:
            match = re.match(r"^(\d|0\d|1\d|2[0-3]):(\d|[0-5]\d|60)(:(\d|[0-5]\d|60))?$", value)
            if match:
                value = datetime.time(
                    hour=int(match.group(1)),
                    minute=int(match.group(2)),
                    second=int(match.group(4)) if match.group(4) else 0,
                )

        return super().parse(value, as_time, as_date, as_datetime)


class MultilayerFormatEDTF(BabelFormatField):
    """EDTF formater."""

    def format_value(self, value: str) -> Any:
        """Format date value."""
        try:
            return format_date(self.parse(value, as_date=True), format=self._format, locale=self.locale)
        except ValueError:
            return format_edtf(value, format=self._format, locale=self.locale)

    def parse(
        self,
        value: str,
        as_time: bool = False,
        as_date: bool = False,
        as_datetime: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Parse date value."""
        _, _, _ = as_time, as_date, as_datetime
        # standard parsing is too lenient, for example returns "2000-01-01" for input "2000"
        if re.match("^[0-9]+-[0-9]+-[0-9]+", value):
            return super().parse(value, **kwargs)
        raise ValueError("Not a valid date")


class TimezoneMixin:  # i'm not sure about where this should be used
    """Add timezone info."""

    @property
    def tzinfo(self) -> Any:
        """Get timezone info."""
        from oarepo_runtime.proxies import current_timezone

        try:
            return current_timezone.get()
        except LookupError:
            return None


class LocalizedDateTime(TimezoneMixin, LocalizedMixin, FormatDatetime):
    """Localize date time field."""


class LocalizedTime(LocalizedMixin, FormatTimeString):
    """Localize time field."""


class LocalizedEDTF(LocalizedMixin, MultilayerFormatEDTF):
    """Localize EDTF field."""


class LocalizedEDTFTime(LocalizedMixin, MultilayerFormatEDTF):
    """Localize EDTF time field."""


class LocalizedEDTFInterval(LocalizedMixin, FormatEDTF):
    """Localize EDTF interval field."""


class LocalizedEDTFTimeInterval(LocalizedMixin, FormatEDTF):
    """Localize EDTF time interval field."""

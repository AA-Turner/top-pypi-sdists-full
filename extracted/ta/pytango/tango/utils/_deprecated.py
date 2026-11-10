# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Shims for names that moved to another module."""

from tango._internal.warn import warn_once
from tango.telemetry import (
    get_telemetry_tracer_provider_factory as _telemetry_get_tracer_provider_factory,
)
from tango.telemetry import (
    set_telemetry_tracer_provider_factory as _telemetry_set_tracer_provider_factory,
)


def set_telemetry_tracer_provider_factory(provider_factory):
    """
    Change the factory that will be used to create tracer providers.

    Import this function from :mod:`tango.telemetry` instead.

    .. versionadded:: 10.0.0
    .. deprecated:: 10.3.0
    """

    warn_once(
        "tango.utils.set_telemetry_tracer_provider_factory is deprecated; import it from tango.telemetry instead.",
        key="deprecated:tango.utils.set_telemetry_tracer_provider_factory",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return _telemetry_set_tracer_provider_factory(provider_factory)


def get_telemetry_tracer_provider_factory():
    """
    Get the factory that will be used to create tracer providers.

    Import this function from :mod:`tango.telemetry` instead.

    .. versionadded:: 10.0.0
    .. deprecated:: 10.3.0
    """

    warn_once(
        "tango.utils.get_telemetry_tracer_provider_factory is deprecated; import it from tango.telemetry instead.",
        key="deprecated:tango.utils.get_telemetry_tracer_provider_factory",
        category=DeprecationWarning,
        stacklevel=2,
    )
    return _telemetry_get_tracer_provider_factory()

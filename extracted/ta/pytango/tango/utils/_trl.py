# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Resolving a device TRL against a tango host, including the test override."""

from urllib.parse import urlparse, urlunparse

__TEST_CONTEXT_HOST_TRL = None


def _set_test_context_tango_host_fqtrl(host_trl):
    """For PyTango internal use only!"""
    # NOTE: we only keep one value so if multiple TestContexts are started in
    # the same process, only the latest one will be used
    if host_trl is not None:
        global __TEST_CONTEXT_HOST_TRL
        __TEST_CONTEXT_HOST_TRL = host_trl


def _clear_test_context_tango_host_fqtrl():
    """For PyTango internal use only!"""
    global __TEST_CONTEXT_HOST_TRL
    __TEST_CONTEXT_HOST_TRL = None


def _get_test_context_tango_host_fqtrl():
    """For PyTango internal use only!"""
    return __TEST_CONTEXT_HOST_TRL


def _get_device_fqtrl_if_necessary(device_trl):
    """For PyTango internal use only!"""
    if __TEST_CONTEXT_HOST_TRL:
        device_trl = _get_device_fqtrl(device_trl, __TEST_CONTEXT_HOST_TRL)
    return device_trl


def _get_device_fqtrl(device_trl, host_trl):
    parsed_device = urlparse(device_trl)
    if not _is_tango_uri_resolved(parsed_device):
        parsed_host = urlparse(host_trl)
        device_trl = _try_resolve_tango_trl(parsed_host, parsed_device)
    return device_trl


def _is_tango_uri_resolved(parsed_device):
    return parsed_device.scheme == "tango"


def _try_resolve_tango_trl(parsed_host, parsed_device):
    if not _is_valid_tango_trl(parsed_host):
        raise InvalidTangoHostTrlError(
            f"Invalid form for Tango host: {parsed_host!r}, device {parsed_device!r}. "
            f"(Override set to: {__TEST_CONTEXT_HOST_TRL})."
        )
    return _resolve_tango_trl(parsed_host, parsed_device)


def _is_valid_tango_trl(parsed_host):
    scheme_ok = parsed_host.scheme == "tango"
    hostname_ok = bool(parsed_host.hostname)
    port_ok = bool(parsed_host.port)
    path_ok = parsed_host.path == ""
    params_ok = parsed_host.params == ""
    query_ok = parsed_host.query == ""
    fragment_ok = parsed_host.fragment in ["", "dbase=no", "dbase=yes"]
    return scheme_ok and hostname_ok and port_ok and path_ok and params_ok and query_ok and fragment_ok


def _resolve_tango_trl(parsed_host, parsed_device):
    return urlunparse(
        [
            parsed_host.scheme,
            parsed_host.netloc,
            parsed_device.path,
            parsed_host.params,
            parsed_host.query,
            parsed_host.fragment,
        ]
    )


class InvalidTangoHostTrlError(ValueError):
    """Invalid Tango Resource Locator format for TANGO_HOST-like variable."""

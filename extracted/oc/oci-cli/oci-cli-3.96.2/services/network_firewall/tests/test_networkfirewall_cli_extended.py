# coding: utf-8
# Copyright (c) 2016, 2026, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import pytest

from services.network_firewall.src.oci_cli_network_firewall import networkfirewall_cli_extended


class FakeContext(object):

    def __init__(self):
        self.invocations = []

    def invoke(self, command, **kwargs):
        self.invocations.append((command, kwargs))


def _command_callback(command):
    callback = command.callback
    while getattr(callback, "__wrapped__", None) is not None:
        callback = callback.__wrapped__
    return callback


@pytest.mark.parametrize("service_type", ["TCP_SERVICE", "TCP"])
def test_service_type_dispatch_uses_tcp_service_discriminator(service_type):
    ctx = FakeContext()
    tcp_command = object()
    udp_command = object()

    networkfirewall_cli_extended._invoke_service_type_specific_command(
        ctx,
        service_type,
        tcp_command,
        udp_command,
        name="test-tcp-service"
    )

    assert ctx.invocations == [(tcp_command, {"name": "test-tcp-service"})]


@pytest.mark.parametrize("service_type", ["UDP_SERVICE", "UDP"])
def test_service_type_dispatch_uses_udp_service_discriminator(service_type):
    ctx = FakeContext()
    tcp_command = object()
    udp_command = object()

    networkfirewall_cli_extended._invoke_service_type_specific_command(
        ctx,
        service_type,
        tcp_command,
        udp_command,
        name="test-udp-service"
    )

    assert ctx.invocations == [(udp_command, {"name": "test-udp-service"})]


def test_service_type_dispatch_rejects_unknown_discriminator():
    with pytest.raises(ValueError, match="Unknown service type: BOGUS"):
        networkfirewall_cli_extended._invoke_service_type_specific_command(
            FakeContext(),
            "BOGUS",
            object(),
            object()
        )


@pytest.mark.parametrize("service_type", ["TCP_SERVICE", "TCP"])
def test_create_service_extended_routes_tcp_service_to_tcp_command(service_type):
    ctx = FakeContext()

    _command_callback(networkfirewall_cli_extended.create_service_extended)(
        ctx,
        network_firewall_policy_id="policy-id",
        type=service_type,
        description="test description",
        service_details='{"name":"test-tcp-service","type":"TCP_SERVICE","portRanges":[{"minimumPort":443,"maximumPort":443}]}',
        from_json=None
    )

    assert ctx.invocations == [(
        networkfirewall_cli_extended.networkfirewall_cli.create_service_create_tcp_service_details,
        {
            "network_firewall_policy_id": "policy-id",
            "description": "test description",
            "from_json": None,
            "port_ranges": [{"minimumPort": 443, "maximumPort": 443}],
            "name": "test-tcp-service"
        }
    )]


def test_create_service_extended_uses_service_details_type_when_top_level_type_is_absent():
    ctx = FakeContext()

    _command_callback(networkfirewall_cli_extended.create_service_extended)(
        ctx,
        network_firewall_policy_id="policy-id",
        type=None,
        description=None,
        service_details='{"name":"test-tcp-service","type":"TCP_SERVICE","portRanges":[{"minimumPort":443,"maximumPort":443}]}',
        from_json=None
    )

    assert ctx.invocations[0][0] == networkfirewall_cli_extended.networkfirewall_cli.create_service_create_tcp_service_details


@pytest.mark.parametrize("service_type", ["TCP_SERVICE", "TCP"])
def test_update_service_extended_routes_tcp_service_to_tcp_command(service_type):
    ctx = FakeContext()

    _command_callback(networkfirewall_cli_extended.update_service_extended)(
        ctx,
        network_firewall_policy_id="policy-id",
        service_name="test-tcp-service",
        type=service_type,
        description="test description",
        if_match=None,
        force=True,
        service_details='{"type":"TCP_SERVICE","portRanges":[{"minimumPort":443,"maximumPort":443}]}',
        from_json=None
    )

    assert ctx.invocations == [(
        networkfirewall_cli_extended.networkfirewall_cli.update_service_update_tcp_service_details,
        {
            "network_firewall_policy_id": "policy-id",
            "service_name": "test-tcp-service",
            "description": "test description",
            "if_match": None,
            "force": True,
            "from_json": None,
            "port_ranges": [{"minimumPort": 443, "maximumPort": 443}]
        }
    )]

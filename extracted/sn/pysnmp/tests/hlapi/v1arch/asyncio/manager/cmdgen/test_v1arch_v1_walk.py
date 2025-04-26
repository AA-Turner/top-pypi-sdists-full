import pytest
from pysnmp.hlapi.v1arch.asyncio import *
from tests.agent_context import AGENT_PORT, AgentContextManager


total_count = 212  # 267


@pytest.mark.asyncio
async def test_v1_walk():
    async with AgentContextManager():
        snmpDispatcher = SnmpDispatcher()
        objects = walk_cmd(
            snmpDispatcher,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("localhost", AGENT_PORT)),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        objects_list = [item async for item in objects]

        errorIndication, errorStatus, errorIndex, varBinds = objects_list[0]

        assert errorIndication is None
        assert errorStatus == 0
        assert len(varBinds) == 1
        assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"

        errorIndication, errorStatus, errorIndex, varBinds = objects_list[1]

        assert errorIndication is None
        assert errorStatus == 0
        assert len(varBinds) == 1
        assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysUpTime.0"

        assert len(objects_list) == total_count

        snmpDispatcher.transport_dispatcher.close_dispatcher()


@pytest.mark.asyncio
async def test_v1_walk_subtree():
    async with AgentContextManager():
        snmpDispatcher = SnmpDispatcher()
        objects = walk_cmd(
            snmpDispatcher,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("localhost", AGENT_PORT)),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "system")),
            lexicographicMode=False,
        )

        objects_list = [item async for item in objects]

        errorIndication, errorStatus, errorIndex, varBinds = objects_list[0]

        assert errorIndication is None
        assert errorStatus == 0
        assert len(varBinds) == 1
        assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysDescr.0"

        errorIndication, errorStatus, errorIndex, varBinds = objects_list[1]

        assert errorIndication is None
        assert errorStatus == 0
        assert len(varBinds) == 1
        assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"

        assert len(objects_list) == 8

        snmpDispatcher.transport_dispatcher.close_dispatcher()

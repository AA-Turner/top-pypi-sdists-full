import pytest
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.asyncio.slim import Slim
from pysnmp.hlapi.asyncio.transport import UdpTransportTarget
from pysnmp.hlapi.asyncio.auth import CommunityData
from pysnmp.hlapi.asyncio.context import ContextData
from pysnmp.proto.rfc1902 import OctetString
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from tests.agent_context import AGENT_PORT, AgentContextManager


@pytest.mark.asyncio
async def test_v1_set():
    async with AgentContextManager():
        with Slim(1) as slim:
            errorIndication, errorStatus, errorIndex, varBinds = await slim.set(
                "public",
                "localhost",
                AGENT_PORT,
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0), "Shanghai"),
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert len(varBinds) == 1
            assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysLocation.0"
            assert varBinds[0][1].prettyPrint() == "Shanghai"
            assert isinstance(varBinds[0][1], OctetString)

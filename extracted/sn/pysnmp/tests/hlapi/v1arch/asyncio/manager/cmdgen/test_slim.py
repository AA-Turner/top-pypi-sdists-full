import pytest
from pysnmp.hlapi.v1arch.asyncio import *
from tests.agent_context import AGENT_PORT, AgentContextManager
from pysnmp.proto.rfc1905 import errorStatus as pysnmp_errorStatus


@pytest.mark.asyncio
async def test_v1_get():
    async with AgentContextManager():
        with Slim(1) as slim:
            errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
                "public",
                "localhost",
                AGENT_PORT,
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                retries=0,
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert errorIndex == 0
            assert len(varBinds) == 1
            assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysDescr.0"
            assert varBinds[0][1].prettyPrint().startswith("PySNMP engine version")
            assert isinstance(varBinds[0][1], OctetString)

            name = pysnmp_errorStatus.namedValues.getName(errorStatus)
            assert name == "noError"


@pytest.mark.asyncio
async def test_v1_get_old():
    async with AgentContextManager():
        slim = Slim(1)
        errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
            "public",
            "localhost",
            AGENT_PORT,
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        assert errorIndication is None
        assert errorStatus == 0
        assert errorIndex == 0
        assert len(varBinds) == 1
        assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysDescr.0"
        assert varBinds[0][1].prettyPrint().startswith("PySNMP engine version")
        assert isinstance(varBinds[0][1], OctetString)

        slim.close()


@pytest.mark.asyncio
async def test_v1_next():
    async with AgentContextManager():
        with Slim(1) as slim:
            errorIndication, errorStatus, errorIndex, varBinds = await slim.next(
                "public",
                "localhost",  # "demo.pysnmp.com",
                AGENT_PORT,  # 161,
                ObjectType(
                    ObjectIdentity("SNMPv2-MIB", "sysDescr", 0).load_mibs("PYSNMP-MIB")
                ),
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert errorIndex == 0
            assert len(varBinds) == 1
            assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"
            assert (
                varBinds[0][1].prettyPrint() == "PYSNMP-MIB::pysnmp"
            )  # IMPORTANT: MIB is needed to resolve this name
            assert type(varBinds[0][1]).__name__ == "ObjectIdentity"


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


@pytest.mark.asyncio
@pytest.mark.parametrize("num_bulk", [1, 2, 50])
async def test_v2c_bulk(num_bulk):
    async with AgentContextManager():
        with Slim() as slim:
            errorIndication, errorStatus, errorIndex, varBinds = await slim.bulk(
                "public",
                "localhost",
                AGENT_PORT,
                0,
                num_bulk,
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                retries=0,
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert len(varBinds) == num_bulk
            assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"
            if num_bulk > 1:
                assert varBinds[1][0].prettyPrint() == "SNMPv2-MIB::sysUpTime.0"
            if num_bulk > 2:
                assert varBinds[2][0].prettyPrint() == "SNMPv2-MIB::sysContact.0"


@pytest.mark.asyncio
async def test_v2_get():
    async with AgentContextManager():
        with Slim() as slim:
            errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
                "public",
                "localhost",
                AGENT_PORT,
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert len(varBinds) == 1
            assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysDescr.0"
            assert varBinds[0][1].prettyPrint().startswith("PySNMP engine version")
            assert isinstance(varBinds[0][1], OctetString)


@pytest.mark.asyncio
async def test_v2_next():
    async with AgentContextManager():
        with Slim() as slim:
            errorIndication, errorStatus, errorIndex, varBinds = await slim.next(
                "public",
                "localhost",  # "demo.pysnmp.com",
                AGENT_PORT,  # 161,
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert errorIndex == 0
            assert len(varBinds) == 1
            assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"


@pytest.mark.asyncio
async def test_v2_set():
    async with AgentContextManager():
        with Slim() as slim:
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

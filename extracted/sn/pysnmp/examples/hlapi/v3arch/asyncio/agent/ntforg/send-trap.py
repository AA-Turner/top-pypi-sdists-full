import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    snmpEngine = SnmpEngine()
    # Example of how you might update sysUpTime
    mibBuilder = snmpEngine.get_mib_builder()
    (sysUpTime,) = mibBuilder.import_symbols("__SNMPv2-MIB", "sysUpTime")
    sysUpTime.syntax = TimeTicks(12345)  # Set uptime to 12345

    errorIndication, errorStatus, errorIndex, varBinds = await send_notification(
        snmpEngine,
        CommunityData("public", mpModel=0),
        await UdpTransportTarget.create(("demo.pysnmp.com", 162)),
        ContextData(),
        "trap",
        NotificationType(
            ObjectIdentity("NET-SNMP-EXAMPLES-MIB", "netSnmpExampleNotification")
        ).add_varbinds(
            ObjectType(
                ObjectIdentity("NET-SNMP-EXAMPLES-MIB", "netSnmpExampleHeartbeatRate"),
                1,
            )
        ),
    )

    if errorIndication:
        print(errorIndication)

    snmpEngine.close_dispatcher()


asyncio.run(run())

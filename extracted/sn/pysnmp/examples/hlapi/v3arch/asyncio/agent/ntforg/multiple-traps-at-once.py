"""
Multiple concurrent notifications
+++++++++++++++++++++++++++++++++

Send multiple SNMP notifications at once using the following options:

* SNMPv2c and SNMPv3
* with community name 'public'
* over IPv4/UDP
* send TRAP notification
* to multiple Managers
* with TRAP ID 'coldStart' specified as a MIB symbol
* include managed object information specified as var-bind objects pair

Functionally similar to:

| $ snmptrap -v1 -c public demo.pysnmp.com 1.3.6.1.4.1.20408.4.1.1.2 demo.pysnmp.com 6 432 12345 1.3.6.1.2.1.1.1.0 s "my system"
| $ snmptrap -v2c -c public demo.pysnmp.com 123 1.3.6.1.6.3.1.1.5.1

"""  #
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    # List of targets in the following format:
    # ( ( authData, transportTarget ), ... )
    TARGETS = (
        # 1-st target (SNMPv1 over IPv4/UDP)
        (
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("demo.pysnmp.com", 162)),
            ContextData(),
        ),
        # 2-nd target (SNMPv2c over IPv4/UDP)
        (
            CommunityData("public"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 162)),
            ContextData(),
        ),
    )

    snmpEngine = SnmpEngine()

    for authData, transportTarget, contextData in TARGETS:
        await send_notification(
            snmpEngine,
            authData,
            transportTarget,
            contextData,
            "trap",  # NotifyType
            NotificationType(ObjectIdentity("SNMPv2-MIB", "coldStart")).add_varbinds(
                ("1.3.6.1.2.1.1.1.0", "my name")
            ),
        )

    snmpEngine.transport_dispatcher.run_dispatcher()


asyncio.run(run())

"""
Multiple concurrent notifications
+++++++++++++++++++++++++++++++++

Send multiple SNMP notifications at once using the following options:

* SNMPv2c and SNMPv3
* with community name 'public'
* over IPv4/UDP
* send INFORM notification
* to multiple Managers
* with TRAP ID 'coldStart' specified as a MIB symbol
* include managed object information specified as var-bind objects pair

Functionally similar to:

| $ snmpinform -v2c -c public demo.pysnmp.com 123 1.3.6.1.6.3.1.1.5.1
| $ snmpinform -v3 -u usr-md5-des -l authPriv -A authkey1 -X privkey1 demo.pysnmp.com 123 1.3.6.1.6.3.1.1.5.1

"""  #
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    # List of targets in the following format:
    # ( ( authData, transportTarget ), ... )
    TARGETS = (
        # 1-st target (SNMPv2c over IPv4/UDP)
        (
            CommunityData("public"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 162)),
            ContextData(),
        ),
        # 2-nd target (SNMPv3 over IPv4/UDP)
        (
            UsmUserData("usr-md5-des", "authkey1", "privkey1"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 162)),
            ContextData(),
        ),
    )

    snmpEngine = SnmpEngine()

    for authData, transportTarget, contextData in TARGETS:
        (
            errorIndication,
            errorStatus,
            errorIndex,
            varBindTable,
        ) = await send_notification(
            snmpEngine,
            authData,
            transportTarget,
            contextData,
            "inform",  # NotifyType
            NotificationType(ObjectIdentity("SNMPv2-MIB", "coldStart")).add_varbinds(
                ("1.3.6.1.2.1.1.1.0", "my name")
            ),
        )

        if errorIndication:
            print("Notification not sent: %s" % errorIndication)
        elif errorStatus:
            print(
                "Notification Receiver returned error: %s @%s"
                % (errorStatus, errorIndex)
            )
        else:
            print("Notification delivered:")
            for name, val in varBindTable:
                print(f"{name.prettyPrint()} = {val.prettyPrint()}")

    snmpEngine.transport_dispatcher.run_dispatcher()


asyncio.run(run())

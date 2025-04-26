"""
Multiple SNMP Engines
+++++++++++++++++++++

Send SNMP notifications in behalf of multiple independent SNMP engines
using the following options:

* with a single transport dispatcher and two independent SNMP engines
* SNMPv2c and SNMPv3
* with community name 'public' or USM username usr-md5-des
* over IPv4/UDP
* send INFORM notification
* to multiple Managers
* with TRAP ID 'coldStart' specified as a MIB symbol
* include managed object information specified as var-bind objects pair

Within this script we have a single asynchronous TransportDispatcher
and a single UDP-based transport serving two independent SNMP engines.
We use a single instance of AsyncNotificationOriginator with each of
SNMP Engines to communicate INFORM notification to remote systems.

When we receive a [response] message from remote system we use
a custom message router to choose what of the two SNMP engines
data packet should be handed over. The selection criteria we
employ here is based on peer's UDP port number. Other selection
criteria are also possible.

| $ snmpinform -v2c -c public demo.pysnmp.com:1162 123 1.3.6.1.6.3.1.1.5.1
| $ snmpinform -v3 -u usr-md5-des -l authPriv -A authkey1 -X privkey1 demo.pysnmp.com 123 1.3.6.1.6.3.1.1.5.1

"""  #
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher


async def run():
    # List of targets in the following format:
    # ( ( authData, transportTarget ), ... )
    TARGETS = (
        # 1-st target (SNMPv2c over IPv4/UDP)
        (
            CommunityData("public"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 162)),  # TODO: 1162
            ContextData(),
        ),
        # 2-nd target (SNMPv3 over IPv4/UDP)
        (
            UsmUserData("usr-md5-des", "authkey1", "privkey1"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 162)),
            ContextData(),
        ),
    )

    # Instantiate the single transport dispatcher object
    transportDispatcher = AsyncioDispatcher()

    # Setup a custom data routing function to select snmpEngine by transportDomain
    transportDispatcher.register_routing_callback(
        lambda td, ta, d: ta[1] % 3 and "A" or "B"
    )

    snmpEngineA = SnmpEngine()
    snmpEngineA.register_transport_dispatcher(transportDispatcher, "A")

    snmpEngineB = SnmpEngine()
    snmpEngineB.register_transport_dispatcher(transportDispatcher, "B")

    for authData, transportTarget, contextData in TARGETS:
        # Pick one of the two SNMP engines
        snmpEngine = (
            transportTarget.get_transport_info()[1][1] % 3
            and snmpEngineA
            or snmpEngineB
        )

        errorIndication, errorStatus, errorIndex, varBinds = await send_notification(
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
            print(
                "Notification for {} not sent: {}".format(
                    snmpEngine.snmpEngineID.prettyPrint(), errorIndication
                )
            )

        elif errorStatus:
            print(
                "Notification Receiver returned error for request %s, "
                "SNMP Engine: %s @%s"
                % (snmpEngine.snmpEngineID.prettyPrint(), errorStatus, errorIndex)
            )

        else:
            print(
                "Notification for SNMP Engine %s delivered: "
                % (snmpEngine.snmpEngineID.prettyPrint())
            )

            for name, val in varBinds:
                print(f"{name.prettyPrint()} = {val.prettyPrint()}")

    transportDispatcher.run_dispatcher()


asyncio.run(run())

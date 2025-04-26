"""
Multiple SNMP engines
+++++++++++++++++++++

Send multiple SNMP GET requests to multiple peers using multiple
independent SNMP engines. Deal with peers asynchronously. SNMP options
are:

* with SNMPv1, community 'public' and
  with SNMPv2c, community 'public' and
  with SNMPv3, user 'usr-md5-des', MD5 auth and DES privacy
* over IPv4/UDP and
  over IPv6/UDP
* to an Agent at demo.pysnmp.com:161 and
  to an Agent at [::1]:161
* for instances of SNMPv2-MIB::sysDescr.0 and
  SNMPv2-MIB::sysLocation.0 MIB objects

Within this script we have a single asynchronous TransportDispatcher
and a single UDP-based transport serving two independent SNMP engines.
We use a single instance of AsyncCommandGenerator with each of
SNMP Engines to communicate GET command request to remote systems.

When we receive a [response] message from remote system we use
a custom message router to choose what of the two SNMP engines
data packet should be handed over. The selection criteria we
employ here is based on peer's UDP port number. Other selection
criteria are also possible.

"""  #
import asyncio

from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    # List of targets in the following format:
    # ( ( authData, transportTarget, varNames ), ... )
    TARGETS = (
        # 1-st target (SNMPv1 over IPv4/UDP)
        (
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("demo.pysnmp.com", 161)),
            (
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0)),
            ),
        ),
        # 2-nd target (SNMPv2c over IPv4/UDP)
        (
            CommunityData("public"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 161)),  # TODO: 1161
            (
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0)),
            ),
        ),
        # 3-nd target (SNMPv3 over IPv4/UDP)
        (
            UsmUserData("usr-md5-des", "authkey1", "privkey1"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 161)),  # TODO: 2161
            (
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0)),
            ),
        )
        # N-th target
        # ...
    )

    # Instantiate the single transport dispatcher object
    transportDispatcher = AsyncioDispatcher()

    # Setup a custom data routing function to select snmpEngine by transportDomain
    transportDispatcher.register_routing_callback(
        lambda td, ta, d: ta[1] % 3 and "A" or "B"
    )

    snmpEngineA = SnmpEngine()
    snmpEngineIDA = snmpEngineA.snmpEngineID
    print("snmpEngineA ID: %s" % snmpEngineIDA.prettyPrint())
    snmpEngineA.register_transport_dispatcher(transportDispatcher, "A")

    snmpEngineB = SnmpEngine()
    snmpEngineIDB = snmpEngineB.snmpEngineID
    print("snmpEngineB ID: %s" % snmpEngineIDB.prettyPrint())
    snmpEngineB.register_transport_dispatcher(transportDispatcher, "B")

    for authData, transportTarget, varBinds in TARGETS:
        snmpEngine = (
            transportTarget.get_transport_info()[1][1] % 3
            and snmpEngineA
            or snmpEngineB
        )

        (errorIndication, errorStatus, errorIndex, varBindTable) = await get_cmd(
            snmpEngine, authData, transportTarget, ContextData(), *varBinds
        )
        print(
            f"snmpEngine {snmpEngine.snmpEngineID.prettyPrint()}: {authData} via {transportTarget}"
        )
        print(
            "snmpEngineA" if snmpEngine.snmpEngineID == snmpEngineIDA else "snmpEngineB"
        )

        if errorIndication:
            print(errorIndication)
            return True

        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[int(errorIndex) - 1][0] or "?",
                )
            )
            return True

        else:
            for varBind in varBindTable:
                print(" = ".join([x.prettyPrint() for x in varBind]))

    transportDispatcher.run_dispatcher(5)


asyncio.run(run())

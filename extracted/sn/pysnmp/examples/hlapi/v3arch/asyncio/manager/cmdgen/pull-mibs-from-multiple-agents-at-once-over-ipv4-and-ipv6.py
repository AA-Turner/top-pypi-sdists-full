"""
Walk multiple Agents at once
++++++++++++++++++++++++++++

Iterate over MIBs of multiple SNMP Agents asynchronously using the
following options:

* with SNMPv1, community 'public' and
  with SNMPv2c, community 'public' and
  with SNMPv3, user 'usr-md5-des', MD5 auth and DES privacy
* over IPv4/UDP and
  over IPv6/UDP
* to an Agent at demo.snmplabs.com:161 and
  to an Agent at [::1]:161
* pull variables till EOM

"""  #
import asyncio

from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    # List of targets in the following format:
    # ((authData, transportTarget, varNames), ...)
    targets = (
        # 1-st target (SNMPv1 over IPv4/UDP)
        (
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("demo.pysnmp.com", 161)),
            ObjectType(ObjectIdentity("1.3.6.1.2.1")),
        ),
        # 2-nd target (SNMPv2c over IPv4/UDP)
        (
            CommunityData("public"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 161)),
            ObjectType(ObjectIdentity("1.3.6.1.4.1")),
        ),
        # 3-nd target (SNMPv3 over IPv4/UDP)
        (
            UsmUserData("usr-md5-des", "authkey1", "privkey1"),
            await UdpTransportTarget.create(("demo.pysnmp.com", 161)),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "system")),
        ),
        # 4-th target (SNMPv3 over IPv6/UDP)
        (
            UsmUserData("usr-md5-none", "authkey1"),
            await Udp6TransportTarget.create(("demo.pysnmp.com", 161)),
            ObjectType(ObjectIdentity("IF-MIB", "ifTable")),
        )
        # N-th target
        # ...
    )

    snmpEngine = SnmpEngine()

    # Submit initial GETNEXT requests and wait for responses
    for authData, transportTarget, varBind in targets:
        async for (errorIndication, errorStatus, errorIndex, varBindTable) in walk_cmd(
            snmpEngine, authData, transportTarget, ContextData(), varBind
        ):
            if errorIndication:
                print(errorIndication)
                return

            elif errorStatus:
                print(
                    "{} at {}".format(
                        errorStatus.prettyPrint(),
                        errorIndex and varBindTable[int(errorIndex) - 1][0] or "?",
                    )
                )
                return

            else:
                for varBind in varBindTable:
                    print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.transport_dispatcher.run_dispatcher()


asyncio.run(run())

"""
Walk whole MIB
++++++++++++++

Send a series of SNMP GETNEXT requests using the following options:

* with SNMPv3, user 'usr-md5-none', MD5 authentication, no privacy
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for all OIDs in IF-MIB

Functionally similar to:

| $ snmpwalk -v3 -lauthNoPriv -u usr-md5-none -A authkey1 -X privkey1 \
|            demo.pysnmp.com  IF-MIB::

"""  #
import asyncio

from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    snmpEngine = SnmpEngine()

    async for (errorIndication, errorStatus, errorIndex, varBindTable) in walk_cmd(
        snmpEngine,
        UsmUserData("usr-md5-none", "authkey1"),
        await UdpTransportTarget.create(("demo.pysnmp.com", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("IF-MIB", "ifTable")),
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

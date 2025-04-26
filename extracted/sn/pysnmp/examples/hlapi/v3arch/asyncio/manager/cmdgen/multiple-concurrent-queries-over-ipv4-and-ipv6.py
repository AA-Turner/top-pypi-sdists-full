"""
Concurrent queries
++++++++++++++++++

Send multiple SNMP GET requests at once using the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to multiple Agents at demo.pysnmp.com
* for instance of SNMPv2-MIB::sysDescr.0 MIB object
* based on asyncio I/O framework

Functionally similar to:

| $ snmpget -v2c -c public demo.pysnmp.com:161 SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public demo.pysnmp.com:161 SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public demo.pysnmp.com:161 SNMPv2-MIB::sysDescr.0

"""  #
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def getone(snmpEngine, hostname):
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        snmpEngine,
        CommunityData("public"),
        await UdpTransportTarget.create(hostname),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))


async def main():
    snmpEngine = SnmpEngine()
    await asyncio.gather(
        getone(snmpEngine, ("demo.pysnmp.com", 161)),
        getone(snmpEngine, ("demo.pysnmp.com", 161)),
        getone(snmpEngine, ("demo.pysnmp.com", 161)),
    )


asyncio.run(main())

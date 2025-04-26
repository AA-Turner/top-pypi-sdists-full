"""
SNMPv2c
+++++++

Send SNMP GET request using the following options:

  * with SNMPv2c, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.pysnmp.com:161
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v2c -c public demo.pysnmp.com SNMPv2-MIB::sysDescr.0

"""  #
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType


async def run():
    snmpEngine = SnmpEngine()
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        snmpEngine,
        CommunityData("public"),
        await UdpTransportTarget.create(("demo.pysnmp.com", 161)),
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


asyncio.run(run())

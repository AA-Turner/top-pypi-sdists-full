"""
Implementing scalar MIB objects
+++++++++++++++++++++++++++++++

Listen and respond to SNMP GET/SET/GETNEXT/GETBULK queries with
the following options:

* SNMPv2c
* with SNMP community "public"
* serving custom Managed Object Instance defined within this script
* allow read access only to the subtree where the custom MIB object resides
* over IPv4/UDP, listening at 127.0.0.1:161

The following Net-SNMP commands will walk this Agent:

| $ snmpwalk -v2c -c public 127.0.0.1 .1.3.6

"""  #
import sys
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.proto.api import v2c

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.add_transport(
    snmpEngine, udp.DOMAIN_NAME, udp.UdpTransport().open_server_mode(("127.0.0.1", 161))
)

# SNMPv2c setup

# SecurityName <-> CommunityName mapping.
config.add_v1_system(snmpEngine, "my-area", "public")

# Allow read MIB access for this user / securityModels at VACM
config.add_vacm_user(snmpEngine, 2, "my-area", "noAuthNoPriv", (1, 3, 6, 5))

# Create an SNMP context
snmpContext = context.SnmpContext(snmpEngine)

# --- create custom Managed Object Instance ---

mibBuilder = snmpContext.get_mib_instrum().get_mib_builder()

MibScalar, MibScalarInstance = mibBuilder.import_symbols(
    "SNMPv2-SMI", "MibScalar", "MibScalarInstance"
)


class MyStaticMibScalarInstance(MibScalarInstance):
    # noinspection PyUnusedLocal,PyUnusedLocal
    def getValue(self, name, **context):
        return self.getSyntax().clone(
            f"Python {sys.version} running on a {sys.platform} platform"
        )


mibBuilder.export_symbols(
    "__MY_MIB",
    MibScalar((1, 3, 6, 5, 1), v2c.OctetString()),
    MyStaticMibScalarInstance((1, 3, 6, 5, 1), (0,), v2c.OctetString()),
)

# --- end of Managed Object Instance initialization ----

# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transport_dispatcher.job_started(1)

# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.open_dispatcher()
except:
    snmpEngine.close_dispatcher()
    raise

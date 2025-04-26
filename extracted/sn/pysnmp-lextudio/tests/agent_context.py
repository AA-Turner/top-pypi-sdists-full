from pysnmp.carrier.asyncio.dgram import udp, udp6
from pysnmp.entity import config, engine
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.hlapi.asyncio import SnmpEngine
from pysnmp.proto.api import v2c


import asyncio
import time

# Set the port to 1611 instead of 161, because 161 is a
# privileged port and requires root access
AGENT_PORT = 1611


async def start_agent(
    enable_ipv6: bool = False, enable_custom_objects: bool = False
) -> SnmpEngine:
    # Create SNMP engine
    snmpEngine = engine.SnmpEngine()

    # Set up transport endpoint
    config.addTransport(
        snmpEngine,
        udp.domainName,
        udp.UdpTransport().openServerMode(("localhost", AGENT_PORT)),
    )

    if enable_ipv6:
        config.addTransport(
            snmpEngine,
            udp6.domainName,
            udp6.Udp6Transport().openServerMode(("localhost", AGENT_PORT)),
        )

    # Set up community data
    config.addV1System(snmpEngine, "public", "public")
    # Add SNMP v3 user
    config.addV3User(
        snmpEngine, "usr-none-none", config.usmNoAuthProtocol, config.usmNoPrivProtocol
    )

    config.addV3User(
        snmpEngine,
        "usr-sha-aes",
        config.usmHMACSHAAuthProtocol,
        "authkey1",
        config.usmAesCfb128Protocol,
        "privkey1",
    )

    config.addV3User(
        snmpEngine, "usr-sha-none", config.usmHMACSHAAuthProtocol, "authkey1"
    )

    # Allow read MIB access for this user / securityModels at VACM
    config.addVacmUser(snmpEngine, 1, "public", "noAuthNoPriv", (1, 3, 6), (1, 3, 6))
    config.addVacmUser(snmpEngine, 2, "public", "noAuthNoPriv", (1, 3, 6), (1, 3, 6))
    config.addVacmUser(snmpEngine, 3, "usr-none-none", "noAuthNoPriv", (1, 3, 6))
    config.addVacmUser(snmpEngine, 3, "usr-sha-none", "authNoPriv", (1, 3, 6))
    config.addVacmUser(snmpEngine, 3, "usr-sha-aes", "authPriv", (1, 3, 6))

    # Configure SNMP context
    snmpContext = context.SnmpContext(snmpEngine)

    if enable_custom_objects:
        # --- create custom Managed Object Instances ---
        mibBuilder = snmpContext.getMibInstrum().getMibBuilder()

        MibScalar, MibScalarInstance = mibBuilder.importSymbols(
            "SNMPv2-SMI", "MibScalar", "MibScalarInstance"
        )

        class SlowMibScalarInstance(MibScalarInstance):
            def getValue(self, name, idx):
                time.sleep(2)  # Add a 2-second sleep
                return self.getSyntax().clone(f"Test agent")

            def setValue(self, name, idx, value):
                print(f"SET operation received. New value: {value}")
                return self.getSyntax().clone(value)

        class NoAccessMibScalarInstance(MibScalarInstance):
            def getValue(self, name, idx):
                time.sleep(2)  # Add a 2-second sleep
                return self.getSyntax().clone(f"Test agent")

            def setValue(self, name, idx, value):
                print(f"SET operation received. New value: {value}")
                return self.getSyntax().clone(value)

        mibBuilder.exportSymbols(
            "__MY_MIB",
            MibScalar((1, 3, 6, 1, 4, 1, 60069, 9, 1), v2c.OctetString()),
            SlowMibScalarInstance(
                (1, 3, 6, 1, 4, 1, 60069, 9, 1), (0,), v2c.OctetString()
            ),
            MibScalar((1, 3, 6, 1, 4, 1, 60069, 9, 3), v2c.OctetString()).setMaxAccess(
                "not-accessible"
            ),
            MibScalar((1, 3, 6, 1, 4, 1, 60069, 9, 4), v2c.OctetString()).setMaxAccess(
                "readonly"
            ),  # PySMI <1.3.0 generates such objects
        )

        # --- end of Managed Object Instance initialization ----

    # Register SNMP Applications at the SNMP engine for particular SNMP context
    cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
    cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
    cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)
    cmdrsp.SetCommandResponder(snmpEngine, snmpContext)

    # Start the event loop
    snmpEngine.transportDispatcher.jobStarted(1)

    snmpEngine.openDispatcher()

    # Wait for the agent to start
    await asyncio.sleep(1)

    # return the engine
    return snmpEngine


class AgentContextManager:
    """
    A context manager for managing the lifecycle of an SNMP test agent.

    Usage:
    async with AgentContextManager() as agent:
        # Perform operations with the agent

    When the context is entered, the agent is started using the `start_agent()` function.
    When the context is exited, the agent's transport dispatcher is stopped and closed.

    Note: The `start_agent()` function and the `transportDispatcher` attribute are not defined in this code snippet.
    """

    def __init__(self, enable_ipv6: bool = False, enable_custom_objects: bool = False):
        self.enable_ipv6 = enable_ipv6
        self.enable_custom_objects = enable_custom_objects

    async def __aenter__(self):
        self.agent = await start_agent(self.enable_ipv6, self.enable_custom_objects)
        return self.agent

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.agent.transportDispatcher.jobFinished(1)
        self.agent.closeDispatcher()

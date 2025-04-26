"""
SNMPv3 INFORM, auth: MD5, privacy: none
+++++++++++++++++++++++++++++++++++++++

Send SNMP INFORM notification using the following options:

* SNMPv3
* with user 'usr-md5-none', auth: MD5, priv NONE
* over IPv4/UDP
* to a Manager at demo.pysnmp.com:162
* send INFORM notification
* with TRAP ID 'warmStart' specified as an OID
* include managed object information 1.3.6.1.2.1.1.5.0 = 'system name'

Functionally similar to:

| $ snmpinform -v3 -l authNoPriv -u usr-md5-none -A authkey1 demo.pysnmp.com  0 1.3.6.1.6.3.1.1.5.1 1.3.6.1.2.1.1.5.0 = 'system name'

"""  #
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntforg
from pysnmp.proto.api import v2c

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# Add USM user
config.add_v3_user(snmpEngine, "usr-md5-none", config.USM_AUTH_HMAC96_MD5, "authkey1")
config.add_target_parameters(snmpEngine, "my-creds", "usr-md5-none", "authNoPriv")

# Setup transport endpoint and bind it with security settings yielding
# a target name
config.add_transport(
    snmpEngine, udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_client_mode()
)
config.add_target_address(
    snmpEngine,
    "my-nms",
    udp.DOMAIN_NAME,
    ("127.0.0.1", 162),
    "my-creds",
    tagList="all-my-managers",
)

# Specify what kind of notification should be sent (TRAP or INFORM),
# to what targets (chosen by tag) and what filter should apply to
# the set of targets (selected by tag)
config.add_notification_target(
    snmpEngine, "my-notification", "my-filter", "all-my-managers", "inform"
)

# Allow NOTIFY access to Agent's MIB by this SNMP model (3), securityLevel
# and SecurityName
config.add_context(snmpEngine, "")
config.add_vacm_user(snmpEngine, 3, "usr-md5-none", "authNoPriv", (), (), (1, 3, 6))

# *** SNMP engine configuration is complete by this line ***

# Create Notification Originator App instance.
ntfOrg = ntforg.NotificationOriginator()


# Error/confirmation receiver
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(
    snmpEngine,
    sendRequestHandle,
    errorIndication,
    errorStatus,
    errorIndex,
    varBinds,
    cbCtx,
):
    print(
        "Notification {}, status - {}".format(
            sendRequestHandle, errorIndication and errorIndication or "delivered"
        )
    )


# Build and submit notification message to dispatcher
sendRequestHandle = ntfOrg.send_varbinds(
    snmpEngine,
    "my-notification",  # notification targets
    None,
    "",  # contextEngineId, contextName
    # var-binds: SNMPv2-MIB::coldStart, ...
    [
        (
            (1, 3, 6, 1, 6, 3, 1, 1, 4, 1, 0),
            v2c.ObjectIdentifier((1, 3, 6, 1, 6, 3, 1, 1, 5, 1)),
        ),
        ((1, 3, 6, 1, 2, 1, 1, 5, 0), v2c.OctetString("system name")),
    ],
    cbFun,
)

print("Notification %s scheduled to be sent" % sendRequestHandle)

# Run I/O dispatcher which would send pending message and process response
snmpEngine.open_dispatcher()

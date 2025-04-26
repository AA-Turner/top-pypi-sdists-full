"""
Multiple SNMP USM users
+++++++++++++++++++++++

Receive SNMP TRAP/INFORM messages with the following options:

* SNMPv3
* with USM users:

  * 'usr-md5-des', auth: MD5, priv DES, ContextEngineId: 8000000001020304
  * 'usr-md5-none', auth: MD5, priv NONE, ContextEngineId: 8000000001020304
  * 'usr-md5-aes256', auth: MD5, priv AES-256, ContextEngineId: 8000000001020304
  * 'usr-sha-aes128', auth: SHA, priv AES, ContextEngineId: 8000000001020304

* over IPv4/UDP, listening at 127.0.0.1:162
* print received data on stdout

Either of the following Net-SNMP commands will send notifications to this
receiver:

| $ snmptrap -v3 -u usr-md5-des -l authPriv -A authkey1 -X privkey1 -e 8000000001020304 127.0.0.1 123 1.3.6.1.6.3.1.1.5.1
| $ snmptrap -v3 -u usr-md5-none -l authNoPriv -A authkey1 -e 8000000001020304 127.0.0.1 123 1.3.6.1.6.3.1.1.5.1
| $ snmptrap -v3 -u usr-md5-aes256 -l authPriv -A authkey1 -x AES-256 -X privkey1 -e 8000000001020304 127.0.0.1 123 1.3.6.1.6.3.1.1.5.1
| $ snmpinform -v3 -u usr-sha-aes128 -l authPriv -a SHA -A authkey1 -x AES -X privkey1 127.0.0.1 123 1.3.6.1.6.3.1.1.5.1

Note that AES-256 is not supported by Net-SNMP. You have to use PySNMP command line tools or other SNMP software that supports AES-256.

"""  #
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.add_transport(
    snmpEngine, udp.DOMAIN_NAME, udp.UdpTransport().open_server_mode(("127.0.0.1", 162))
)

# SNMPv3/USM setup

# user: usr-md5-des, auth: MD5, priv DES, securityEngineId: 8000000001020304
# this USM entry is configured for TRAP receiving purposes
config.add_v3_user(
    snmpEngine,
    "usr-md5-des",
    config.USM_AUTH_HMAC96_MD5,
    "authkey1",
    config.USM_PRIV_CBC56_DES,
    "privkey1",
    securityEngineId=v2c.OctetString(hexValue="8000000001020304"),
)

# user: usr-md5-none, auth: MD5, priv NONE, securityEngineId: 8000000001020304
# this USM entry is configured for TRAP receiving purposes
config.add_v3_user(
    snmpEngine,
    "usr-md5-none",
    config.USM_AUTH_HMAC96_MD5,
    "authkey1",
    securityEngineId=v2c.OctetString(hexValue="8000000001020304"),
)

# user: usr-md5-aes256, auth: MD5, priv AES-256, securityEngineId: 8000000001020304
# this USM entry is configured for TRAP receiving purposes
config.add_v3_user(
    snmpEngine,
    "usr-md5-aes256",
    config.USM_AUTH_HMAC96_MD5,
    "authkey1",
    config.USM_PRIV_CFB256_AES,
    "privkey1",
    securityEngineId=v2c.OctetString(hexValue="8000000001020304"),
)

# user: usr-sha-aes128, auth: SHA, priv AES, securityEngineId: 8000000001020304
# this USM entry is configured for TRAP receiving purposes
config.add_v3_user(
    snmpEngine,
    "usr-sha-aes128",
    config.USM_AUTH_HMAC96_SHA,
    "authkey1",
    config.USM_PRIV_CFB128_AES,
    "privkey1",
)


# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    print(
        'Notification from ContextEngineId "{}", ContextName "{}"'.format(
            contextEngineId.prettyPrint(), contextName.prettyPrint()
        )
    )
    for name, val in varBinds:
        print(f"{name.prettyPrint()} = {val.prettyPrint()}")


# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transport_dispatcher.job_started(1)  # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.open_dispatcher()
except:
    snmpEngine.close_dispatcher()
    raise

"""
Listen for notifications at IPv4 & IPv6 interfaces
++++++++++++++++++++++++++++++++++++++++++++++++++

Receive SNMP TRAP messages with the following options:

* SNMPv1/SNMPv2c
* with SNMP community "public"
* over IPv4/UDP, listening at 127.0.0.1:162
* over IPv6/UDP, listening at [::1]:162
* print received data on stdout

Either of the following Net-SNMP commands will send notifications to this
receiver:

| $ snmptrap -v1 -c public 127.0.0.1 1.3.6.1.4.1.20408.4.1.1.2 127.0.0.1 1 1 123 1.3.6.1.2.1.1.1.0 s test
| $ snmptrap -v2c -c public ::1 123 1.3.6.1.6.3.1.1.5.1 1.3.6.1.2.1.1.5.0 s test

Notification Receiver below uses two different transports for communication
with Notification Originators - UDP over IPv4 and UDP over IPv6.

"""  #
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api


# noinspection PyUnusedLocal
def __callback(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.PROTOCOL_MODULES:
            pMod = api.PROTOCOL_MODULES[msgVer]

        else:
            print("Unsupported SNMP version %s" % msgVer)
            return

        reqMsg, wholeMsg = decoder.decode(
            wholeMsg,
            asn1Spec=pMod.Message(),
        )

        print(
            "Notification message from {}:{}: ".format(
                transportDomain, transportAddress
            )
        )

        reqPDU = pMod.apiMessage.get_pdu(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.SNMP_VERSION_1:
                print(
                    "Enterprise: %s"
                    % (pMod.apiTrapPDU.get_enterprise(reqPDU).prettyPrint())
                )
                print(
                    "Agent Address: %s"
                    % (pMod.apiTrapPDU.get_agent_address(reqPDU).prettyPrint())
                )
                print(
                    "Generic Trap: %s"
                    % (pMod.apiTrapPDU.get_generic_trap(reqPDU).prettyPrint())
                )
                print(
                    "Specific Trap: %s"
                    % (pMod.apiTrapPDU.get_specific_trap(reqPDU).prettyPrint())
                )
                print(
                    "Uptime: %s" % (pMod.apiTrapPDU.get_timestamp(reqPDU).prettyPrint())
                )
                varBinds = pMod.apiTrapPDU.get_varbinds(reqPDU)

            else:
                varBinds = pMod.apiPDU.get_varbinds(reqPDU)

            print("Var-binds:")

            for oid, val in varBinds:
                print(f"{oid.prettyPrint()} = {val.prettyPrint()}")

    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.register_recv_callback(__callback)

# UDP/IPv4
transportDispatcher.register_transport(
    udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_server_mode(("localhost", 162))
)

# UDP/IPv6
transportDispatcher.register_transport(
    udp6.DOMAIN_NAME, udp6.Udp6AsyncioTransport().open_server_mode(("::1", 162))
)

transportDispatcher.job_started(1)

try:
    print("This program needs to run as root/administrator to monitor port 162.")
    print("Started. Press Ctrl-C to stop")
    # Dispatcher will never finish as job#1 never reaches zero
    transportDispatcher.run_dispatcher()

except KeyboardInterrupt:
    print("Shutting down...")

finally:
    transportDispatcher.close_dispatcher()

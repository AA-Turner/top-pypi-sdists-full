"""
SET string and integer scalars (SNMPv2c)
++++++++++++++++++++++++++++++++++++++++

Perform SNMP SET operation with the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for OIDs in string form and values in form of pyasn1 objects

This script performs similar to the following Net-SNMP command:

| $ snmpset -v2c -c public -ObentU demo.pysnmp.com 1.3.6.1.2.1.1.9.1.3.1 s 'New description' 1.3.6.1.2.1.1.9.1.4.1 t 12

"""  #
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api


# Protocol version to use
# pMod = api.PROTOCOL_MODULES[api.SNMP_VERSION_1]
pMod = api.PROTOCOL_MODULES[api.SNMP_VERSION_2C]

# Build PDU
reqPDU = pMod.SetRequestPDU()
pMod.apiPDU.set_defaults(reqPDU)
pMod.apiPDU.set_varbinds(
    reqPDU,
    # A list of Var-Binds to SET
    (
        ("1.3.6.1.2.1.1.9.1.3.1", pMod.OctetString("New system description")),
        ("1.3.6.1.2.1.1.9.1.4.1", pMod.TimeTicks(12)),
    ),
)

# Build message
reqMsg = pMod.Message()
pMod.apiMessage.set_defaults(reqMsg)
pMod.apiMessage.set_community(reqMsg, "public")
pMod.apiMessage.set_pdu(reqMsg, reqPDU)


# noinspection PyUnusedLocal,PyUnusedLocal
def __callback(
    transportDispatcher, transportDomain, transportAddress, wholeMsg, reqPDU=reqPDU
):
    while wholeMsg:
        rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message())
        rspPDU = pMod.apiMessage.get_pdu(rspMsg)

        # Match response to request
        if pMod.apiPDU.get_request_id(reqPDU) == pMod.apiPDU.get_request_id(rspPDU):
            # Check for SNMP errors reported
            errorStatus = pMod.apiPDU.get_error_status(rspPDU)
            if errorStatus:
                print(errorStatus.prettyPrint())

            else:
                for oid, val in pMod.apiPDU.get_varbinds(rspPDU):
                    print(f"{oid.prettyPrint()} = {val.prettyPrint()}")

            transportDispatcher.job_finished(1)

    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.register_recv_callback(__callback)

# UDP/IPv4
transportDispatcher.register_transport(
    udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_client_mode()
)

# Pass message to dispatcher
transportDispatcher.send_message(
    encoder.encode(reqMsg), udp.DOMAIN_NAME, ("demo.pysnmp.com", 161)
)

transportDispatcher.job_started(1)

# Dispatcher will finish as job#1 counter reaches zero
transportDispatcher.run_dispatcher(3)

transportDispatcher.close_dispatcher()

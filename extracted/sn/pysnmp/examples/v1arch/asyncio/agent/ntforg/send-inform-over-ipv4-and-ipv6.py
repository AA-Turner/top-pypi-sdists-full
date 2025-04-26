"""
INFORM over multiple transports
+++++++++++++++++++++++++++++++

The following script sends SNMP INFORM notification using the following options:

* with SNMPv2c
* with community name 'public'
* over IPv4/UDP and IPv6/UDP
* send INFORM notification
* to a Manager at demo.pysnmp.com:162 and [::1]:162
* with TRAP ID 'coldStart' specified as an OID

The following Net-SNMP command will produce similar SNMP notification:

| $ snmpinform -v2c -c public udp:demo.pysnmp.com 0 1.3.6.1.6.3.1.1.5.1
| $ snmpinform -v2c -c public udp6:[::1] 0 1.3.6.1.6.3.1.1.5.1

"""  #
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto.api import v2c as pMod

# Build PDU
reqPDU = pMod.InformRequestPDU()
pMod.apiTrapPDU.set_defaults(reqPDU)

# Build message
trapMsg = pMod.Message()
pMod.apiMessage.set_defaults(trapMsg)
pMod.apiMessage.set_community(trapMsg, "public")
pMod.apiMessage.set_pdu(trapMsg, reqPDU)


# noinspection PyUnusedLocal,PyUnusedLocal
def cbRecvFun(
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
                print("INFORM message delivered, response var-binds follow")
                for oid, val in pMod.apiPDU.get_varbinds(rspPDU):
                    print(f"{oid.prettyPrint()} = {val.prettyPrint()}")
            transportDispatcher.job_finished(1)
    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.register_recv_callback(cbRecvFun)

# UDP/IPv4
transportDispatcher.register_transport(
    udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_client_mode()
)
transportDispatcher.send_message(
    encoder.encode(trapMsg), udp.DOMAIN_NAME, ("demo.pysnmp.com", 162)
)
transportDispatcher.jobStarted(1)

# UDP/IPv6
# transportDispatcher.register_transport(
#    udp6.domainName, udp6.Udp6AsyncioTransport().open_client_mode()
# )
# transportDispatcher.send_message(
#    encoder.encode(trapMsg), udp6.domainName, ('::1', 162)
# )
# transportDispatcher.job_started(1)

# Dispatcher will finish as all scheduled messages are sent
transportDispatcher.run_dispatcher(3)

transportDispatcher.close_dispatcher()

"""
Walk Agent MIB (SNMPv1)
+++++++++++++++++++++++

Perform SNMP GETNEXT operation with the following options:

* with SNMPv1, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for OID in tuple form

This script performs similar to the following Net-SNMP command:

| $ snmpwalk -v1 -c public -ObentU demo.pysnmp.com 1.3.6

"""  #
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api

# Protocol version to use
pMod = api.PROTOCOL_MODULES[api.SNMP_VERSION_1]
# pMod = api.PROTOCOL_MODULES[api.SNMP_VERSION_2C]

# SNMP table header
headVars = [pMod.ObjectIdentifier((1, 3, 6))]

# Build PDU
reqPDU = pMod.GetNextRequestPDU()
pMod.apiPDU.set_defaults(reqPDU)
pMod.apiPDU.set_varbinds(reqPDU, [(x, pMod.null) for x in headVars])

# Build message
reqMsg = pMod.Message()
pMod.apiMessage.set_defaults(reqMsg)
pMod.apiMessage.set_community(reqMsg, "public")
pMod.apiMessage.set_pdu(reqMsg, reqPDU)


# noinspection PyUnusedLocal
def cbRecvFun(
    transportDispatcher,
    transportDomain,
    transportAddress,
    wholeMsg,
    reqPDU=reqPDU,
    headVars=headVars,
):
    while wholeMsg:
        rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message())
        rspPDU = pMod.apiMessage.get_pdu(rspMsg)

        # Match response to request
        if pMod.apiPDU.get_request_id(reqPDU) == pMod.apiPDU.get_request_id(rspPDU):
            # Check for SNMP errors reported
            errorStatus = pMod.apiPDU.get_error_status(rspPDU)
            if errorStatus and errorStatus != 2:
                raise Exception(errorStatus)

            # Format var-binds table
            varBindTable = pMod.apiPDU.get_varbind_table(reqPDU, rspPDU)

            # Report SNMP table
            for tableRow in varBindTable:
                for name, val in tableRow:
                    print(
                        "from: {}, {} = {}".format(
                            transportAddress, name.prettyPrint(), val.prettyPrint()
                        )
                    )

            # Stop on EOM
            for oid, val in varBindTable[-1]:
                if not isinstance(val, pMod.Null):
                    break

            else:
                transportDispatcher.job_finished(1)
                continue

            # Generate request for next row
            pMod.apiPDU.set_varbinds(
                reqPDU, [(x, pMod.null) for x, y in varBindTable[-1]]
            )

            pMod.apiPDU.set_request_id(reqPDU, pMod.get_next_request_id())

            transportDispatcher.send_message(
                encoder.encode(reqMsg), transportDomain, transportAddress
            )

    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.register_recv_callback(cbRecvFun)

transportDispatcher.register_transport(
    udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_client_mode()
)

transportDispatcher.send_message(
    encoder.encode(reqMsg), udp.DOMAIN_NAME, ("demo.pysnmp.com", 161)
)

transportDispatcher.job_started(1)

transportDispatcher.run_dispatcher(3)

transportDispatcher.close_dispatcher()

"""
Bulk walk Agent MIB (SNMPv2c)
+++++++++++++++++++++++++++++

Perform SNMP GETBULK operation with the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for OID in tuple form
* with non-repeaters=0 and max-repeaters=25

This script performs similar to the following Net-SNMP command:

| $ snmpbulkwalk -v2c -c public -ObentU -Cn0 -Cr25 demo.pysnmp.com 1.3.6

"""  #
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto.api import v2c

# SNMP table header
headVars = [v2c.ObjectIdentifier((1, 3, 6))]

# Build PDU
reqPDU = v2c.GetBulkRequestPDU()
v2c.apiBulkPDU.set_defaults(reqPDU)
v2c.apiBulkPDU.set_non_repeaters(reqPDU, 0)
v2c.apiBulkPDU.set_max_repetitions(reqPDU, 25)
v2c.apiBulkPDU.set_varbinds(reqPDU, [(x, v2c.null) for x in headVars])

# Build message
reqMsg = v2c.Message()
v2c.apiMessage.set_defaults(reqMsg)
v2c.apiMessage.set_community(reqMsg, "public")
v2c.apiMessage.set_pdu(reqMsg, reqPDU)


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
        rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=v2c.Message())

        rspPDU = v2c.apiMessage.get_pdu(rspMsg)

        # Match response to request
        if v2c.apiBulkPDU.get_request_id(reqPDU) == v2c.apiBulkPDU.get_request_id(
            rspPDU
        ):
            # Format var-binds table
            varBindTable = v2c.apiBulkPDU.get_varbind_table(reqPDU, rspPDU)

            # Check for SNMP errors reported
            errorStatus = v2c.apiBulkPDU.get_error_status(rspPDU)
            if errorStatus and errorStatus != 2:
                errorIndex = v2c.apiBulkPDU.get_error_index(rspPDU)
                print(
                    "{} at {}".format(
                        errorStatus.prettyPrint(),
                        errorIndex and varBindTable[int(errorIndex) - 1] or "?",
                    )
                )
                transportDispatcher.job_finished(1)
                break

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
                if not isinstance(val, v2c.Null):
                    break

            else:
                transportDispatcher.job_finished(1)
                continue

            # Generate request for next row
            v2c.apiBulkPDU.set_varbinds(
                reqPDU, [(x, v2c.null) for x, y in varBindTable[-1]]
            )

            v2c.apiBulkPDU.set_request_id(reqPDU, v2c.getNextRequestID())

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

# Dispatcher will finish as job#1 counter reaches zero
transportDispatcher.run_dispatcher(3)

transportDispatcher.close_dispatcher()

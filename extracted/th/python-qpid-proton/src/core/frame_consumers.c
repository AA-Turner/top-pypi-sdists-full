#include "frame_consumers.h"

#include "core/consumers.h"

/* D.[SIo?B?BD.[SIsIo.s]D.[SIsIo]..IL..?R] */
size_t pn_amqp_decode_attach(pn_bytes_t bytes, pn_bytes_t* arg0, uint32_t* arg1, bool* arg2, bool* arg3, uint8_t* arg4, bool* arg5, uint8_t* arg6, pn_bytes_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, uint32_t* arg10, bool* arg11, pn_bytes_t* arg12, pn_bytes_t* arg13, uint32_t* arg14, pn_bytes_t* arg15, uint32_t* arg16, bool* arg17, uint32_t* arg18, uint64_t* arg19, bool* arg20, pn_bytes_t* arg21)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_string(&consumer, arg0);
            consume_uint(&consumer, arg1);
            consume_bool(&consumer, arg2);
            *arg3 = consume_ubyte(&consumer, arg4);;
            *arg5 = consume_ubyte(&consumer, arg6);;
            {
                pni_consumer_t subconsumer;
                consume_described(&consumer, &subconsumer);
                pni_consumer_t consumer = subconsumer;
                {
                    pni_consumer_t subconsumer;
                    uint32_t count;
                    consume_list(&consumer, &subconsumer, &count);
                    pni_consumer_t consumer = subconsumer;
                    consume_string(&consumer, arg7);
                    consume_uint(&consumer, arg8);
                    consume_symbol(&consumer, arg9);
                    consume_uint(&consumer, arg10);
                    consume_bool(&consumer, arg11);
                    consume_anything(&consumer);
                    consume_symbol(&consumer, arg12);
                    consume_end_list(&consumer);
                }
            }
            {
                pni_consumer_t subconsumer;
                consume_described(&consumer, &subconsumer);
                pni_consumer_t consumer = subconsumer;
                {
                    pni_consumer_t subconsumer;
                    uint32_t count;
                    consume_list(&consumer, &subconsumer, &count);
                    pni_consumer_t consumer = subconsumer;
                    consume_string(&consumer, arg13);
                    consume_uint(&consumer, arg14);
                    consume_symbol(&consumer, arg15);
                    consume_uint(&consumer, arg16);
                    consume_bool(&consumer, arg17);
                    consume_end_list(&consumer);
                }
            }
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_uint(&consumer, arg18);
            consume_ulong(&consumer, arg19);
            consume_anything(&consumer);
            consume_anything(&consumer);
            *arg20 = consume_raw(&consumer, arg21);;
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[.....D..D.[R]...] */
size_t pn_amqp_decode_attach_coordinator_caps(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_described_anything(&consumer);
            {
                pni_consumer_t subconsumer;
                consume_described(&consumer, &subconsumer);
                pni_consumer_t consumer = subconsumer;
                {
                    pni_consumer_t subconsumer;
                    uint32_t count;
                    consume_list(&consumer, &subconsumer, &count);
                    pni_consumer_t consumer = subconsumer;
                    consume_raw(&consumer, arg0);
                    consume_end_list(&consumer);
                }
            }
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[.....D.[.....R.R.RR]] */
size_t pn_amqp_decode_attach_source_props(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            {
                pni_consumer_t subconsumer;
                consume_described(&consumer, &subconsumer);
                pni_consumer_t consumer = subconsumer;
                {
                    pni_consumer_t subconsumer;
                    uint32_t count;
                    consume_list(&consumer, &subconsumer, &count);
                    pni_consumer_t consumer = subconsumer;
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_raw(&consumer, arg0);
                    consume_anything(&consumer);
                    consume_raw(&consumer, arg1);
                    consume_anything(&consumer);
                    consume_raw(&consumer, arg2);
                    consume_raw(&consumer, arg3);
                    consume_end_list(&consumer);
                }
            }
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[.....D..D.[.....RR]] */
size_t pn_amqp_decode_attach_target_props(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_described_anything(&consumer);
            {
                pni_consumer_t subconsumer;
                consume_described(&consumer, &subconsumer);
                pni_consumer_t consumer = subconsumer;
                {
                    pni_consumer_t subconsumer;
                    uint32_t count;
                    consume_list(&consumer, &subconsumer, &count);
                    pni_consumer_t consumer = subconsumer;
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_anything(&consumer);
                    consume_raw(&consumer, arg0);
                    consume_raw(&consumer, arg1);
                    consume_end_list(&consumer);
                }
            }
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[.....D..DL....] */
size_t pn_amqp_decode_attach_target_type(pn_bytes_t bytes, uint64_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_described_anything(&consumer);
            consume_described_type_anything(&consumer, arg0);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[?HIII?I] */
size_t pn_amqp_decode_begin(pn_bytes_t bytes, bool* arg0, uint16_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            *arg0 = consume_ushort(&consumer, arg1);;
            consume_uint(&consumer, arg2);
            consume_uint(&consumer, arg3);
            consume_uint(&consumer, arg4);
            *arg5 = consume_uint(&consumer, arg6);;
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[D.[sSR]] */
size_t pn_amqp_decode_close(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            {
                pni_consumer_t subconsumer;
                consume_described(&consumer, &subconsumer);
                pni_consumer_t consumer = subconsumer;
                {
                    pni_consumer_t subconsumer;
                    uint32_t count;
                    consume_list(&consumer, &subconsumer, &count);
                    pni_consumer_t consumer = subconsumer;
                    consume_symbol(&consumer, arg0);
                    consume_string(&consumer, arg1);
                    consume_raw(&consumer, arg2);
                    consume_end_list(&consumer);
                }
            }
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[R] */
size_t pn_amqp_decode_described_list_raw(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_raw(&consumer, arg0);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.R */
size_t pn_amqp_decode_described_raw(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    consume_described_raw(&consumer, arg0);
    return consumer.position;
}

/* D?L. */
size_t pn_amqp_decode_described_type_anything(pn_bytes_t bytes, bool* arg0, uint64_t* arg1)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    consume_described_maybe_type_anything(&consumer, arg0, arg1);
    return consumer.position;
}

/* D.[IoR] */
size_t pn_amqp_decode_detach(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, pn_bytes_t* arg2)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_uint(&consumer, arg0);
            consume_bool(&consumer, arg1);
            consume_raw(&consumer, arg2);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[oI?IoD?LR] */
size_t pn_amqp_decode_disposition(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint32_t* arg3, bool* arg4, bool* arg5, uint64_t* arg6, pn_bytes_t* arg7)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_bool(&consumer, arg0);
            consume_uint(&consumer, arg1);
            *arg2 = consume_uint(&consumer, arg3);;
            consume_bool(&consumer, arg4);
            consume_described_maybe_type_raw(&consumer, arg5, arg6, arg7);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* [z] */
size_t pn_amqp_decode_disposition_declared(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        uint32_t count;
        consume_list(&consumer, &subconsumer, &count);
        pni_consumer_t consumer = subconsumer;
        consume_binaryornull(&consumer, arg0);
        consume_end_list(&consumer);
    }
    return consumer.position;
}

/* [?o?oR] */
size_t pn_amqp_decode_disposition_modified(pn_bytes_t bytes, bool* arg0, bool* arg1, bool* arg2, bool* arg3, pn_bytes_t* arg4)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        uint32_t count;
        consume_list(&consumer, &subconsumer, &count);
        pni_consumer_t consumer = subconsumer;
        *arg0 = consume_bool(&consumer, arg1);;
        *arg2 = consume_bool(&consumer, arg3);;
        consume_raw(&consumer, arg4);
        consume_end_list(&consumer);
    }
    return consumer.position;
}

/* [?I?L] */
size_t pn_amqp_decode_disposition_received(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint64_t* arg3)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        uint32_t count;
        consume_list(&consumer, &subconsumer, &count);
        pni_consumer_t consumer = subconsumer;
        *arg0 = consume_uint(&consumer, arg1);;
        *arg2 = consume_ulong(&consumer, arg3);;
        consume_end_list(&consumer);
    }
    return consumer.position;
}

/* [D.[sSR]] */
size_t pn_amqp_decode_disposition_rejected(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        uint32_t count;
        consume_list(&consumer, &subconsumer, &count);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            consume_described(&consumer, &subconsumer);
            pni_consumer_t consumer = subconsumer;
            {
                pni_consumer_t subconsumer;
                uint32_t count;
                consume_list(&consumer, &subconsumer, &count);
                pni_consumer_t consumer = subconsumer;
                consume_symbol(&consumer, arg0);
                consume_string(&consumer, arg1);
                consume_raw(&consumer, arg2);
                consume_end_list(&consumer);
            }
        }
        consume_end_list(&consumer);
    }
    return consumer.position;
}

/* [z?R] */
size_t pn_amqp_decode_disposition_transactional_state(pn_bytes_t bytes, pn_bytes_t* arg0, bool* arg1, pn_bytes_t* arg2)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        uint32_t count;
        consume_list(&consumer, &subconsumer, &count);
        pni_consumer_t consumer = subconsumer;
        consume_binaryornull(&consumer, arg0);
        *arg1 = consume_raw(&consumer, arg2);;
        consume_end_list(&consumer);
    }
    return consumer.position;
}

/* D.[sSR] */
size_t pn_amqp_decode_error_condition(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_symbol(&consumer, arg0);
            consume_string(&consumer, arg1);
            consume_raw(&consumer, arg2);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[?IIII?I?II.o] */
size_t pn_amqp_decode_flow(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6, bool* arg7, uint32_t* arg8, uint32_t* arg9, bool* arg10)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            *arg0 = consume_uint(&consumer, arg1);;
            consume_uint(&consumer, arg2);
            consume_uint(&consumer, arg3);
            consume_uint(&consumer, arg4);
            *arg5 = consume_uint(&consumer, arg6);;
            *arg7 = consume_uint(&consumer, arg8);;
            consume_uint(&consumer, arg9);
            consume_anything(&consumer);
            consume_bool(&consumer, arg10);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[o?BIoI] */
size_t pn_amqp_decode_message_header(pn_bytes_t bytes, bool* arg0, bool* arg1, uint8_t* arg2, uint32_t* arg3, bool* arg4, uint32_t* arg5)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_bool(&consumer, arg0);
            *arg1 = consume_ubyte(&consumer, arg2);;
            consume_uint(&consumer, arg3);
            consume_bool(&consumer, arg4);
            consume_uint(&consumer, arg5);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[azSSSassttSIS] */
size_t pn_amqp_decode_message_properties(pn_bytes_t bytes, pn_atom_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3, pn_bytes_t* arg4, pn_atom_t* arg5, pn_bytes_t* arg6, pn_bytes_t* arg7, pn_timestamp_t* arg8, pn_timestamp_t* arg9, pn_bytes_t* arg10, uint32_t* arg11, pn_bytes_t* arg12)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_atom(&consumer, arg0);
            consume_binaryornull(&consumer, arg1);
            consume_string(&consumer, arg2);
            consume_string(&consumer, arg3);
            consume_string(&consumer, arg4);
            consume_atom(&consumer, arg5);
            consume_symbol(&consumer, arg6);
            consume_symbol(&consumer, arg7);
            consume_timestamp(&consumer, arg8);
            consume_timestamp(&consumer, arg9);
            consume_string(&consumer, arg10);
            consume_uint(&consumer, arg11);
            consume_string(&consumer, arg12);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[?S?S?I?HI..RRR] */
size_t pn_amqp_decode_open(pn_bytes_t bytes, bool* arg0, pn_bytes_t* arg1, bool* arg2, pn_bytes_t* arg3, bool* arg4, uint32_t* arg5, bool* arg6, uint16_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, pn_bytes_t* arg10, pn_bytes_t* arg11)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            *arg0 = consume_string(&consumer, arg1);;
            *arg2 = consume_string(&consumer, arg3);;
            *arg4 = consume_uint(&consumer, arg5);;
            *arg6 = consume_ushort(&consumer, arg7);;
            consume_uint(&consumer, arg8);
            consume_anything(&consumer);
            consume_anything(&consumer);
            consume_raw(&consumer, arg9);
            consume_raw(&consumer, arg10);
            consume_raw(&consumer, arg11);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* R */
size_t pn_amqp_decode_raw(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    consume_raw(&consumer, arg0);
    return consumer.position;
}

/* D.[z] */
size_t pn_amqp_decode_sasl_binary(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_binaryornull(&consumer, arg0);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[sz] */
size_t pn_amqp_decode_sasl_init(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_symbol(&consumer, arg0);
            consume_binaryornull(&consumer, arg1);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[s] */
size_t pn_amqp_decode_sasl_mechanism_symbol(pn_bytes_t bytes, pn_bytes_t* arg0)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_symbol(&consumer, arg0);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[Bz] */
size_t pn_amqp_decode_sasl_outcome(pn_bytes_t bytes, uint8_t* arg0, pn_bytes_t* arg1)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_ubyte(&consumer, arg0);
            consume_binaryornull(&consumer, arg1);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}

/* D.[I?I?Z?I?oo.D?LRooo] */
size_t pn_amqp_decode_transfer(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, uint32_t* arg2, bool* arg3, pn_bytes_t* arg4, bool* arg5, uint32_t* arg6, bool* arg7, bool* arg8, bool* arg9, bool* arg10, uint64_t* arg11, pn_bytes_t* arg12, bool* arg13, bool* arg14, bool* arg15)
{
    pni_consumer_t consumer = make_consumer_from_bytes(bytes);
    {
        pni_consumer_t subconsumer;
        consume_described(&consumer, &subconsumer);
        pni_consumer_t consumer = subconsumer;
        {
            pni_consumer_t subconsumer;
            uint32_t count;
            consume_list(&consumer, &subconsumer, &count);
            pni_consumer_t consumer = subconsumer;
            consume_uint(&consumer, arg0);
            *arg1 = consume_uint(&consumer, arg2);;
            *arg3 = consume_binarynonull(&consumer, arg4);;
            *arg5 = consume_uint(&consumer, arg6);;
            *arg7 = consume_bool(&consumer, arg8);;
            consume_bool(&consumer, arg9);
            consume_anything(&consumer);
            consume_described_maybe_type_raw(&consumer, arg10, arg11, arg12);
            consume_bool(&consumer, arg13);
            consume_bool(&consumer, arg14);
            consume_bool(&consumer, arg15);
            consume_end_list(&consumer);
        }
    }
    return consumer.position;
}


#include "frame_generators.h"

#include "core/emitters.h"

/* DL[SIoBB?DL[SIsIoR?sRnMM]?DL[SIsIoRM]nnILnnR] */
bool pn_amqp_encode_inner_attach(pni_emitter_t* emitter, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, bool arg19, uint64_t arg20, pn_bytes_t arg21, uint32_t arg22, pn_bytes_t arg23, uint32_t arg24, bool arg25, pn_bytes_t arg26, pn_bytes_t arg27, uint32_t arg28, uint64_t arg29, pn_bytes_t arg30)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_string(emitter, &compound, arg1);
        emit_uint(emitter, &compound, arg2);
        emit_bool(emitter, &compound, arg3);
        emit_ubyte(emitter, &compound, arg4);
        emit_ubyte(emitter, &compound, arg5);
        if (arg6) {
            emit_descriptor(emitter, &compound, arg7);
            for (bool small_encoding = true; ; small_encoding = false) {
                pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
                pni_compound_context compound = c;
                emit_string(emitter, &compound, arg8);
                emit_uint(emitter, &compound, arg9);
                emit_symbol(emitter, &compound, arg10);
                emit_uint(emitter, &compound, arg11);
                emit_bool(emitter, &compound, arg12);
                emit_raw(emitter, &compound, arg13);
                if (arg14) {
                    emit_symbol(emitter, &compound, arg15);
                } else {
                    emit_null(emitter, &compound);
                }
                emit_raw(emitter, &compound, arg16);
                emit_null(emitter, &compound);
                emit_multiple(emitter, &compound, arg17);
                emit_multiple(emitter, &compound, arg18);
                emit_end_list(emitter, &compound, small_encoding);
                if (encode_succeeded(emitter, &compound)) break;
            }
        } else {
            emit_null(emitter, &compound);
        }
        if (arg19) {
            emit_descriptor(emitter, &compound, arg20);
            for (bool small_encoding = true; ; small_encoding = false) {
                pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
                pni_compound_context compound = c;
                emit_string(emitter, &compound, arg21);
                emit_uint(emitter, &compound, arg22);
                emit_symbol(emitter, &compound, arg23);
                emit_uint(emitter, &compound, arg24);
                emit_bool(emitter, &compound, arg25);
                emit_raw(emitter, &compound, arg26);
                emit_multiple(emitter, &compound, arg27);
                emit_end_list(emitter, &compound, small_encoding);
                if (encode_succeeded(emitter, &compound)) break;
            }
        } else {
            emit_null(emitter, &compound);
        }
        emit_null(emitter, &compound);
        emit_null(emitter, &compound);
        emit_uint(emitter, &compound, arg28);
        emit_ulong(emitter, &compound, arg29);
        emit_null(emitter, &compound);
        emit_null(emitter, &compound);
        emit_raw(emitter, &compound, arg30);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_attach(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, bool arg19, uint64_t arg20, pn_bytes_t arg21, uint32_t arg22, pn_bytes_t arg23, uint32_t arg24, bool arg25, pn_bytes_t arg26, pn_bytes_t arg27, uint32_t arg28, uint64_t arg29, pn_bytes_t arg30)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_attach(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21, arg22, arg23, arg24, arg25, arg26, arg27, arg28, arg29, arg30)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_attach(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, bool arg19, uint64_t arg20, pn_bytes_t arg21, uint32_t arg22, pn_bytes_t arg23, uint32_t arg24, bool arg25, pn_bytes_t arg26, pn_bytes_t arg27, uint32_t arg28, uint64_t arg29, pn_bytes_t arg30)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_attach(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21, arg22, arg23, arg24, arg25, arg26, arg27, arg28, arg29, arg30);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[SIoBB?DL[SIsIoR?sRnRR]DL[R]nnI] */
bool pn_amqp_encode_inner_attach_coordinator(pni_emitter_t* emitter, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, uint64_t arg19, pn_bytes_t arg20, uint32_t arg21)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_string(emitter, &compound, arg1);
        emit_uint(emitter, &compound, arg2);
        emit_bool(emitter, &compound, arg3);
        emit_ubyte(emitter, &compound, arg4);
        emit_ubyte(emitter, &compound, arg5);
        if (arg6) {
            emit_descriptor(emitter, &compound, arg7);
            for (bool small_encoding = true; ; small_encoding = false) {
                pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
                pni_compound_context compound = c;
                emit_string(emitter, &compound, arg8);
                emit_uint(emitter, &compound, arg9);
                emit_symbol(emitter, &compound, arg10);
                emit_uint(emitter, &compound, arg11);
                emit_bool(emitter, &compound, arg12);
                emit_raw(emitter, &compound, arg13);
                if (arg14) {
                    emit_symbol(emitter, &compound, arg15);
                } else {
                    emit_null(emitter, &compound);
                }
                emit_raw(emitter, &compound, arg16);
                emit_null(emitter, &compound);
                emit_raw(emitter, &compound, arg17);
                emit_raw(emitter, &compound, arg18);
                emit_end_list(emitter, &compound, small_encoding);
                if (encode_succeeded(emitter, &compound)) break;
            }
        } else {
            emit_null(emitter, &compound);
        }
        emit_descriptor(emitter, &compound, arg19);
        for (bool small_encoding = true; ; small_encoding = false) {
            pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
            pni_compound_context compound = c;
            emit_raw(emitter, &compound, arg20);
            emit_end_list(emitter, &compound, small_encoding);
            if (encode_succeeded(emitter, &compound)) break;
        }
        emit_null(emitter, &compound);
        emit_null(emitter, &compound);
        emit_uint(emitter, &compound, arg21);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_attach_coordinator(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, uint64_t arg19, pn_bytes_t arg20, uint32_t arg21)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_attach_coordinator(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_attach_coordinator(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, uint64_t arg19, pn_bytes_t arg20, uint32_t arg21)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_attach_coordinator(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[?HIIII] */
bool pn_amqp_encode_inner_begin(pni_emitter_t* emitter, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, uint32_t arg6)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        if (arg1) {
            emit_ushort(emitter, &compound, arg2);
        } else {
            emit_null(emitter, &compound);
        }
        emit_uint(emitter, &compound, arg3);
        emit_uint(emitter, &compound, arg4);
        emit_uint(emitter, &compound, arg5);
        emit_uint(emitter, &compound, arg6);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_begin(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, uint32_t arg6)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_begin(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_begin(char* bytes, size_t size, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, uint32_t arg6)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_begin(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[c] */
bool pn_amqp_encode_inner_close(pni_emitter_t* emitter, uint64_t arg0, pn_condition_t* arg1)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_condition(emitter, &compound, arg1);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_close(pn_rwbytes_t* buffer, uint64_t arg0, pn_condition_t* arg1)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_close(&emitter, arg0, arg1)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_close(char* bytes, size_t size, uint64_t arg0, pn_condition_t* arg1)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_close(&emitter, arg0, arg1);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[] */
bool pn_amqp_encode_inner_described_empty_list(pni_emitter_t* emitter, uint64_t arg0)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_described_empty_list(pn_rwbytes_t* buffer, uint64_t arg0)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_described_empty_list(&emitter, arg0)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_described_empty_list(char* bytes, size_t size, uint64_t arg0)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_described_empty_list(&emitter, arg0);
    return make_bytes_from_emitter(emitter).size;
}

/* DLR */
bool pn_amqp_encode_inner_described_type_raw(pni_emitter_t* emitter, uint64_t arg0, pn_bytes_t arg1)
{
    pni_compound_context compound = make_compound();
    emit_described_type_raw(emitter, &compound, arg0, arg1);
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_described_type_raw(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_described_type_raw(&emitter, arg0, arg1)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_described_type_raw(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_described_type_raw(&emitter, arg0, arg1);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[I?oc] */
bool pn_amqp_encode_inner_detach(pni_emitter_t* emitter, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, pn_condition_t* arg4)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_uint(emitter, &compound, arg1);
        if (arg2) {
            emit_bool(emitter, &compound, arg3);
        } else {
            emit_null(emitter, &compound);
        }
        emit_condition(emitter, &compound, arg4);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_detach(pn_rwbytes_t* buffer, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, pn_condition_t* arg4)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_detach(&emitter, arg0, arg1, arg2, arg3, arg4)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_detach(char* bytes, size_t size, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, pn_condition_t* arg4)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_detach(&emitter, arg0, arg1, arg2, arg3, arg4);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[oIn?od] */
bool pn_amqp_encode_inner_disposition(pni_emitter_t* emitter, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, pn_disposition_t* arg5)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_bool(emitter, &compound, arg1);
        emit_uint(emitter, &compound, arg2);
        emit_null(emitter, &compound);
        if (arg3) {
            emit_bool(emitter, &compound, arg4);
        } else {
            emit_null(emitter, &compound);
        }
        emit_disposition(emitter, &compound, arg5);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_disposition(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, pn_disposition_t* arg5)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_disposition(&emitter, arg0, arg1, arg2, arg3, arg4, arg5)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_disposition(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, pn_disposition_t* arg5)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_disposition(&emitter, arg0, arg1, arg2, arg3, arg4, arg5);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[oI?I?o?DL[]] */
bool pn_amqp_encode_inner_disposition_batch(pni_emitter_t* emitter, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_bool(emitter, &compound, arg1);
        emit_uint(emitter, &compound, arg2);
        if (arg3) {
            emit_uint(emitter, &compound, arg4);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg5) {
            emit_bool(emitter, &compound, arg6);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg7) {
            emit_descriptor(emitter, &compound, arg8);
            for (bool small_encoding = true; ; small_encoding = false) {
                pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
                pni_compound_context compound = c;
                emit_end_list(emitter, &compound, small_encoding);
                if (encode_succeeded(emitter, &compound)) break;
            }
        } else {
            emit_null(emitter, &compound);
        }
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_disposition_batch(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_disposition_batch(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_disposition_batch(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_disposition_batch(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[?IIII?I?I?In?o] */
bool pn_amqp_encode_inner_flow(pni_emitter_t* emitter, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        if (arg1) {
            emit_uint(emitter, &compound, arg2);
        } else {
            emit_null(emitter, &compound);
        }
        emit_uint(emitter, &compound, arg3);
        emit_uint(emitter, &compound, arg4);
        emit_uint(emitter, &compound, arg5);
        if (arg6) {
            emit_uint(emitter, &compound, arg7);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg8) {
            emit_uint(emitter, &compound, arg9);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg10) {
            emit_uint(emitter, &compound, arg11);
        } else {
            emit_null(emitter, &compound);
        }
        emit_null(emitter, &compound);
        if (arg12) {
            emit_bool(emitter, &compound, arg13);
        } else {
            emit_null(emitter, &compound);
        }
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_flow(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_flow(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_flow(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_flow(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[?o?B?I?o?I]! */
bool pn_amqp_encode_inner_message_header(pni_emitter_t* emitter, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10)
{
    pni_compound_context compound = make_compound();
    size_t section_start = emitter->position;
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        if (arg1) {
            emit_bool(emitter, &compound, arg2);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg3) {
            emit_ubyte(emitter, &compound, arg4);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg5) {
            emit_uint(emitter, &compound, arg6);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg7) {
            emit_bool(emitter, &compound, arg8);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg9) {
            emit_uint(emitter, &compound, arg10);
        } else {
            emit_null(emitter, &compound);
        }
        if (compound.count == 0) {
            emitter->position = section_start;
            break;
        }
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_message_header(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_message_header(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_message_header(char* bytes, size_t size, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_message_header(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[azSSSass?t?tS?IS]! */
bool pn_amqp_encode_inner_message_properties(pni_emitter_t* emitter, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, pn_bytes_t arg4, pn_bytes_t arg5, pn_bytes_t arg6, pn_atom_t* arg7, pn_bytes_t arg8, pn_bytes_t arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, pn_bytes_t arg14, bool arg15, uint32_t arg16, pn_bytes_t arg17)
{
    pni_compound_context compound = make_compound();
    size_t section_start = emitter->position;
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_atom(emitter, &compound, arg1);
        emit_binaryornull(emitter, &compound, arg2, arg3);
        emit_string(emitter, &compound, arg4);
        emit_string(emitter, &compound, arg5);
        emit_string(emitter, &compound, arg6);
        emit_atom(emitter, &compound, arg7);
        emit_symbol(emitter, &compound, arg8);
        emit_symbol(emitter, &compound, arg9);
        if (arg10) {
            emit_timestamp(emitter, &compound, arg11);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg12) {
            emit_timestamp(emitter, &compound, arg13);
        } else {
            emit_null(emitter, &compound);
        }
        emit_string(emitter, &compound, arg14);
        if (arg15) {
            emit_uint(emitter, &compound, arg16);
        } else {
            emit_null(emitter, &compound);
        }
        emit_string(emitter, &compound, arg17);
        if (compound.count == 0) {
            emitter->position = section_start;
            break;
        }
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_message_properties(pn_rwbytes_t* buffer, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, pn_bytes_t arg4, pn_bytes_t arg5, pn_bytes_t arg6, pn_atom_t* arg7, pn_bytes_t arg8, pn_bytes_t arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, pn_bytes_t arg14, bool arg15, uint32_t arg16, pn_bytes_t arg17)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_message_properties(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_message_properties(char* bytes, size_t size, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, pn_bytes_t arg4, pn_bytes_t arg5, pn_bytes_t arg6, pn_atom_t* arg7, pn_bytes_t arg8, pn_bytes_t arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, pn_bytes_t arg14, bool arg15, uint32_t arg16, pn_bytes_t arg17)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_message_properties(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[SS?I?H?InnMMR] */
bool pn_amqp_encode_inner_open(pni_emitter_t* emitter, uint64_t arg0, pn_bytes_t arg1, pn_bytes_t arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_bytes_t arg9, pn_bytes_t arg10, pn_bytes_t arg11)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_string(emitter, &compound, arg1);
        emit_string(emitter, &compound, arg2);
        if (arg3) {
            emit_uint(emitter, &compound, arg4);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg5) {
            emit_ushort(emitter, &compound, arg6);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg7) {
            emit_uint(emitter, &compound, arg8);
        } else {
            emit_null(emitter, &compound);
        }
        emit_null(emitter, &compound);
        emit_null(emitter, &compound);
        emit_multiple(emitter, &compound, arg9);
        emit_multiple(emitter, &compound, arg10);
        emit_raw(emitter, &compound, arg11);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_open(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, pn_bytes_t arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_bytes_t arg9, pn_bytes_t arg10, pn_bytes_t arg11)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_open(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_open(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, pn_bytes_t arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_bytes_t arg9, pn_bytes_t arg10, pn_bytes_t arg11)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_open(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[S] */
bool pn_amqp_encode_inner_open_minimal(pni_emitter_t* emitter, uint64_t arg0, pn_bytes_t arg1)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_string(emitter, &compound, arg1);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_open_minimal(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_open_minimal(&emitter, arg0, arg1)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_open_minimal(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_open_minimal(&emitter, arg0, arg1);
    return make_bytes_from_emitter(emitter).size;
}

/* R */
bool pn_amqp_encode_inner_raw(pni_emitter_t* emitter, pn_bytes_t arg0)
{
    pni_compound_context compound = make_compound();
    emit_raw(emitter, &compound, arg0);
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_raw(pn_rwbytes_t* buffer, pn_bytes_t arg0)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_raw(&emitter, arg0)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_raw(char* bytes, size_t size, pn_bytes_t arg0)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_raw(&emitter, arg0);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[Z] */
bool pn_amqp_encode_inner_sasl_binary(pni_emitter_t* emitter, uint64_t arg0, size_t arg1, const char* arg2)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_binarynonull(emitter, &compound, arg1, arg2);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_sasl_binary(pn_rwbytes_t* buffer, uint64_t arg0, size_t arg1, const char* arg2)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_sasl_binary(&emitter, arg0, arg1, arg2)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_sasl_binary(char* bytes, size_t size, uint64_t arg0, size_t arg1, const char* arg2)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_sasl_binary(&emitter, arg0, arg1, arg2);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[szS] */
bool pn_amqp_encode_inner_sasl_init(pni_emitter_t* emitter, uint64_t arg0, pn_bytes_t arg1, size_t arg2, const char* arg3, pn_bytes_t arg4)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_symbol(emitter, &compound, arg1);
        emit_binaryornull(emitter, &compound, arg2, arg3);
        emit_string(emitter, &compound, arg4);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_sasl_init(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, size_t arg2, const char* arg3, pn_bytes_t arg4)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_sasl_init(&emitter, arg0, arg1, arg2, arg3, arg4)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_sasl_init(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, size_t arg2, const char* arg3, pn_bytes_t arg4)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_sasl_init(&emitter, arg0, arg1, arg2, arg3, arg4);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[@T[*s]] */
bool pn_amqp_encode_inner_sasl_mechanisms(pni_emitter_t* emitter, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        for (bool small_encoding = true; ; small_encoding = false) {
            pni_compound_context c = emit_array(emitter, &compound, small_encoding, arg1);
            pni_compound_context compound = c;
            emit_counted_symbols(emitter, &compound, arg2, arg3);
            emit_end_array(emitter, &compound, small_encoding);
            if (encode_succeeded(emitter, &compound)) break;
        }
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_sasl_mechanisms(pn_rwbytes_t* buffer, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_sasl_mechanisms(&emitter, arg0, arg1, arg2, arg3)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_sasl_mechanisms(char* bytes, size_t size, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_sasl_mechanisms(&emitter, arg0, arg1, arg2, arg3);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[Bz] */
bool pn_amqp_encode_inner_sasl_outcome(pni_emitter_t* emitter, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_ubyte(emitter, &compound, arg1);
        emit_binaryornull(emitter, &compound, arg2, arg3);
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_sasl_outcome(pn_rwbytes_t* buffer, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_sasl_outcome(&emitter, arg0, arg1, arg2, arg3)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_sasl_outcome(char* bytes, size_t size, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_sasl_outcome(&emitter, arg0, arg1, arg2, arg3);
    return make_bytes_from_emitter(emitter).size;
}

/* DL[I?I?Z?I?o?ond?o?o?o] */
bool pn_amqp_encode_inner_transfer(pni_emitter_t* emitter, uint64_t arg0, uint32_t arg1, bool arg2, uint32_t arg3, bool arg4, size_t arg5, const char* arg6, bool arg7, uint32_t arg8, bool arg9, bool arg10, bool arg11, bool arg12, pn_disposition_t* arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18, bool arg19)
{
    pni_compound_context compound = make_compound();
    emit_descriptor(emitter, &compound, arg0);
    for (bool small_encoding = true; ; small_encoding = false) {
        pni_compound_context c = emit_list(emitter, &compound, small_encoding, true);
        pni_compound_context compound = c;
        emit_uint(emitter, &compound, arg1);
        if (arg2) {
            emit_uint(emitter, &compound, arg3);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg4) {
            emit_binarynonull(emitter, &compound, arg5, arg6);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg7) {
            emit_uint(emitter, &compound, arg8);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg9) {
            emit_bool(emitter, &compound, arg10);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg11) {
            emit_bool(emitter, &compound, arg12);
        } else {
            emit_null(emitter, &compound);
        }
        emit_null(emitter, &compound);
        emit_disposition(emitter, &compound, arg13);
        if (arg14) {
            emit_bool(emitter, &compound, arg15);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg16) {
            emit_bool(emitter, &compound, arg17);
        } else {
            emit_null(emitter, &compound);
        }
        if (arg18) {
            emit_bool(emitter, &compound, arg19);
        } else {
            emit_null(emitter, &compound);
        }
        emit_end_list(emitter, &compound, small_encoding);
        if (encode_succeeded(emitter, &compound)) break;
    }
    return resize_required(emitter);
}

pn_bytes_t pn_amqp_encode_transfer(pn_rwbytes_t* buffer, uint64_t arg0, uint32_t arg1, bool arg2, uint32_t arg3, bool arg4, size_t arg5, const char* arg6, bool arg7, uint32_t arg8, bool arg9, bool arg10, bool arg11, bool arg12, pn_disposition_t* arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18, bool arg19)
{
    do {
        pni_emitter_t emitter = make_emitter_from_rwbytes(buffer);
        if (pn_amqp_encode_inner_transfer(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19)) {
            size_buffer_to_emitter(buffer, &emitter);
            continue;
        }
        return make_bytes_from_emitter(emitter);
    } while (true);
    /*Unreachable*/
}
size_t pn_amqp_encode_bytes_transfer(char* bytes, size_t size, uint64_t arg0, uint32_t arg1, bool arg2, uint32_t arg3, bool arg4, size_t arg5, const char* arg6, bool arg7, uint32_t arg8, bool arg9, bool arg10, bool arg11, bool arg12, pn_disposition_t* arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18, bool arg19)
{
    pni_emitter_t emitter = make_emitter_from_bytes((pn_rwbytes_t){.size=size, .start=bytes});
    pn_amqp_encode_inner_transfer(&emitter, arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19);
    return make_bytes_from_emitter(emitter).size;
}


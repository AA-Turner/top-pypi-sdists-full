
#include "proton/codec.h"
#include "proton/condition.h"
#include "proton/disposition.h"
#include "buffer.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


/* DL[SIoBB?DL[SIsIoR?sRnMM]?DL[SIsIoRM]nnILnnR] */
pn_bytes_t pn_amqp_encode_attach(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, bool arg19, uint64_t arg20, pn_bytes_t arg21, uint32_t arg22, pn_bytes_t arg23, uint32_t arg24, bool arg25, pn_bytes_t arg26, pn_bytes_t arg27, uint32_t arg28, uint64_t arg29, pn_bytes_t arg30);
size_t pn_amqp_encode_bytes_attach(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, bool arg19, uint64_t arg20, pn_bytes_t arg21, uint32_t arg22, pn_bytes_t arg23, uint32_t arg24, bool arg25, pn_bytes_t arg26, pn_bytes_t arg27, uint32_t arg28, uint64_t arg29, pn_bytes_t arg30);
/* DL[SIoBB?DL[SIsIoR?sRnRR]DL[R]nnI] */
pn_bytes_t pn_amqp_encode_attach_coordinator(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, uint64_t arg19, pn_bytes_t arg20, uint32_t arg21);
size_t pn_amqp_encode_bytes_attach_coordinator(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, pn_bytes_t arg8, uint32_t arg9, pn_bytes_t arg10, uint32_t arg11, bool arg12, pn_bytes_t arg13, bool arg14, pn_bytes_t arg15, pn_bytes_t arg16, pn_bytes_t arg17, pn_bytes_t arg18, uint64_t arg19, pn_bytes_t arg20, uint32_t arg21);
/* DL[?HIIII] */
pn_bytes_t pn_amqp_encode_begin(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, uint32_t arg6);
size_t pn_amqp_encode_bytes_begin(char* bytes, size_t size, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, uint32_t arg6);
/* DL[c] */
pn_bytes_t pn_amqp_encode_close(pn_rwbytes_t* buffer, uint64_t arg0, pn_condition_t* arg1);
size_t pn_amqp_encode_bytes_close(char* bytes, size_t size, uint64_t arg0, pn_condition_t* arg1);
/* DL[] */
pn_bytes_t pn_amqp_encode_described_empty_list(pn_rwbytes_t* buffer, uint64_t arg0);
size_t pn_amqp_encode_bytes_described_empty_list(char* bytes, size_t size, uint64_t arg0);
/* DLR */
pn_bytes_t pn_amqp_encode_described_type_raw(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1);
size_t pn_amqp_encode_bytes_described_type_raw(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1);
/* DL[I?oc] */
pn_bytes_t pn_amqp_encode_detach(pn_rwbytes_t* buffer, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, pn_condition_t* arg4);
size_t pn_amqp_encode_bytes_detach(char* bytes, size_t size, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, pn_condition_t* arg4);
/* DL[oIn?od] */
pn_bytes_t pn_amqp_encode_disposition(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, pn_disposition_t* arg5);
size_t pn_amqp_encode_bytes_disposition(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, pn_disposition_t* arg5);
/* DL[oI?I?o?DL[]] */
pn_bytes_t pn_amqp_encode_disposition_batch(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8);
size_t pn_amqp_encode_bytes_disposition_batch(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8);
/* DL[?IIII?I?I?In?o] */
pn_bytes_t pn_amqp_encode_flow(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13);
size_t pn_amqp_encode_bytes_flow(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13);
/* DL[?o?B?I?o?I]! */
pn_bytes_t pn_amqp_encode_message_header(pn_rwbytes_t* buffer, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10);
size_t pn_amqp_encode_bytes_message_header(char* bytes, size_t size, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10);
/* DL[azSSSass?t?tS?IS]! */
pn_bytes_t pn_amqp_encode_message_properties(pn_rwbytes_t* buffer, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, pn_bytes_t arg4, pn_bytes_t arg5, pn_bytes_t arg6, pn_atom_t* arg7, pn_bytes_t arg8, pn_bytes_t arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, pn_bytes_t arg14, bool arg15, uint32_t arg16, pn_bytes_t arg17);
size_t pn_amqp_encode_bytes_message_properties(char* bytes, size_t size, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, pn_bytes_t arg4, pn_bytes_t arg5, pn_bytes_t arg6, pn_atom_t* arg7, pn_bytes_t arg8, pn_bytes_t arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, pn_bytes_t arg14, bool arg15, uint32_t arg16, pn_bytes_t arg17);
/* DL[SS?I?H?InnMMR] */
pn_bytes_t pn_amqp_encode_open(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, pn_bytes_t arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_bytes_t arg9, pn_bytes_t arg10, pn_bytes_t arg11);
size_t pn_amqp_encode_bytes_open(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, pn_bytes_t arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_bytes_t arg9, pn_bytes_t arg10, pn_bytes_t arg11);
/* DL[S] */
pn_bytes_t pn_amqp_encode_open_minimal(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1);
size_t pn_amqp_encode_bytes_open_minimal(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1);
/* R */
pn_bytes_t pn_amqp_encode_raw(pn_rwbytes_t* buffer, pn_bytes_t arg0);
size_t pn_amqp_encode_bytes_raw(char* bytes, size_t size, pn_bytes_t arg0);
/* DL[Z] */
pn_bytes_t pn_amqp_encode_sasl_binary(pn_rwbytes_t* buffer, uint64_t arg0, size_t arg1, const char* arg2);
size_t pn_amqp_encode_bytes_sasl_binary(char* bytes, size_t size, uint64_t arg0, size_t arg1, const char* arg2);
/* DL[szS] */
pn_bytes_t pn_amqp_encode_sasl_init(pn_rwbytes_t* buffer, uint64_t arg0, pn_bytes_t arg1, size_t arg2, const char* arg3, pn_bytes_t arg4);
size_t pn_amqp_encode_bytes_sasl_init(char* bytes, size_t size, uint64_t arg0, pn_bytes_t arg1, size_t arg2, const char* arg3, pn_bytes_t arg4);
/* DL[@T[*s]] */
pn_bytes_t pn_amqp_encode_sasl_mechanisms(pn_rwbytes_t* buffer, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3);
size_t pn_amqp_encode_bytes_sasl_mechanisms(char* bytes, size_t size, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3);
/* DL[Bz] */
pn_bytes_t pn_amqp_encode_sasl_outcome(pn_rwbytes_t* buffer, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3);
size_t pn_amqp_encode_bytes_sasl_outcome(char* bytes, size_t size, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3);
/* DL[I?I?Z?I?o?ond?o?o?o] */
pn_bytes_t pn_amqp_encode_transfer(pn_rwbytes_t* buffer, uint64_t arg0, uint32_t arg1, bool arg2, uint32_t arg3, bool arg4, size_t arg5, const char* arg6, bool arg7, uint32_t arg8, bool arg9, bool arg10, bool arg11, bool arg12, pn_disposition_t* arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18, bool arg19);
size_t pn_amqp_encode_bytes_transfer(char* bytes, size_t size, uint64_t arg0, uint32_t arg1, bool arg2, uint32_t arg3, bool arg4, size_t arg5, const char* arg6, bool arg7, uint32_t arg8, bool arg9, bool arg10, bool arg11, bool arg12, pn_disposition_t* arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18, bool arg19);

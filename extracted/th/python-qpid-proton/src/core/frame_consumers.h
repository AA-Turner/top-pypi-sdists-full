
#include "proton/codec.h"
#include "proton/condition.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


/* D.[SIo?B?BD.[SIsIo.s]D.[SIsIo]..IL..?R] */
size_t pn_amqp_decode_attach(pn_bytes_t bytes, pn_bytes_t* arg0, uint32_t* arg1, bool* arg2, bool* arg3, uint8_t* arg4, bool* arg5, uint8_t* arg6, pn_bytes_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, uint32_t* arg10, bool* arg11, pn_bytes_t* arg12, pn_bytes_t* arg13, uint32_t* arg14, pn_bytes_t* arg15, uint32_t* arg16, bool* arg17, uint32_t* arg18, uint64_t* arg19, bool* arg20, pn_bytes_t* arg21);
/* D.[.....D..D.[R]...] */
size_t pn_amqp_decode_attach_coordinator_caps(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[.....D.[.....R.R.RR]] */
size_t pn_amqp_decode_attach_source_props(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3);
/* D.[.....D..D.[.....RR]] */
size_t pn_amqp_decode_attach_target_props(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1);
/* D.[.....D..DL....] */
size_t pn_amqp_decode_attach_target_type(pn_bytes_t bytes, uint64_t* arg0);
/* D.[?HIII?I] */
size_t pn_amqp_decode_begin(pn_bytes_t bytes, bool* arg0, uint16_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6);
/* D.[D.[sSR]] */
size_t pn_amqp_decode_close(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2);
/* D.[R] */
size_t pn_amqp_decode_described_list_raw(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.R */
size_t pn_amqp_decode_described_raw(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D?L. */
size_t pn_amqp_decode_described_type_anything(pn_bytes_t bytes, bool* arg0, uint64_t* arg1);
/* D.[IoR] */
size_t pn_amqp_decode_detach(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, pn_bytes_t* arg2);
/* D.[oI?IoD?LR] */
size_t pn_amqp_decode_disposition(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint32_t* arg3, bool* arg4, bool* arg5, uint64_t* arg6, pn_bytes_t* arg7);
/* [z] */
size_t pn_amqp_decode_disposition_declared(pn_bytes_t bytes, pn_bytes_t* arg0);
/* [?o?oR] */
size_t pn_amqp_decode_disposition_modified(pn_bytes_t bytes, bool* arg0, bool* arg1, bool* arg2, bool* arg3, pn_bytes_t* arg4);
/* [?I?L] */
size_t pn_amqp_decode_disposition_received(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint64_t* arg3);
/* [D.[sSR]] */
size_t pn_amqp_decode_disposition_rejected(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2);
/* [z?R] */
size_t pn_amqp_decode_disposition_transactional_state(pn_bytes_t bytes, pn_bytes_t* arg0, bool* arg1, pn_bytes_t* arg2);
/* D.[sSR] */
size_t pn_amqp_decode_error_condition(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2);
/* D.[?IIII?I?II.o] */
size_t pn_amqp_decode_flow(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6, bool* arg7, uint32_t* arg8, uint32_t* arg9, bool* arg10);
/* D.[o?BIoI] */
size_t pn_amqp_decode_message_header(pn_bytes_t bytes, bool* arg0, bool* arg1, uint8_t* arg2, uint32_t* arg3, bool* arg4, uint32_t* arg5);
/* D.[azSSSassttSIS] */
size_t pn_amqp_decode_message_properties(pn_bytes_t bytes, pn_atom_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3, pn_bytes_t* arg4, pn_atom_t* arg5, pn_bytes_t* arg6, pn_bytes_t* arg7, pn_timestamp_t* arg8, pn_timestamp_t* arg9, pn_bytes_t* arg10, uint32_t* arg11, pn_bytes_t* arg12);
/* D.[?S?S?I?HI..RRR] */
size_t pn_amqp_decode_open(pn_bytes_t bytes, bool* arg0, pn_bytes_t* arg1, bool* arg2, pn_bytes_t* arg3, bool* arg4, uint32_t* arg5, bool* arg6, uint16_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, pn_bytes_t* arg10, pn_bytes_t* arg11);
/* R */
size_t pn_amqp_decode_raw(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[z] */
size_t pn_amqp_decode_sasl_binary(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[sz] */
size_t pn_amqp_decode_sasl_init(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1);
/* D.[s] */
size_t pn_amqp_decode_sasl_mechanism_symbol(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[Bz] */
size_t pn_amqp_decode_sasl_outcome(pn_bytes_t bytes, uint8_t* arg0, pn_bytes_t* arg1);
/* D.[I?I?Z?I?oo.D?LRooo] */
size_t pn_amqp_decode_transfer(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, uint32_t* arg2, bool* arg3, pn_bytes_t* arg4, bool* arg5, uint32_t* arg6, bool* arg7, bool* arg8, bool* arg9, bool* arg10, uint64_t* arg11, pn_bytes_t* arg12, bool* arg13, bool* arg14, bool* arg15);

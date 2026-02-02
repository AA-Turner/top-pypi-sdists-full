from ..imports import *
LOG_INTAKE_QUEUE = get_env_val("LOG_INTAKE_QUEUE") or 'logIntakeQueue';
LOG_ENTRY_QUEUE = get_env_val("LOG_ENTRY_QUEUE") or ' logEntryQueue';
PAIR_ENTRY_QUEUE = get_env_val("PAIR_ENTRY_QUEUE") or 'pairEntryQueue';
TXN_ENTRY_QUEUE = get_env_val("TXN_ENTRY_QUEUE") or 'txnEntryQueue';
RPC_CALL_QUEUE = get_env_val("RPC_CALL_QUEUE") or 'rpcCallQueue';
TRANSACTION_CALL_QUEUE = get_env_val("TRANSACTION_CALL_QUEUE") or 'txnCallQueue';
SIGNATURE_CALL_QUEUE = get_env_val("SIGNATURE_CALL_QUEUE") or 'signatureCallQueue';
META_DATA_CALL_QUEUE = get_env_val("META_DATA_CALL_QUEUE") or 'metaDataCallQueue';
GET_SIGNATURES_CALL_QUEUE = get_env_val("GET_SIGNATURES_CALL_QUEUE") or 'getSignaturesCallQueue';
LOG_GETEM_QUEUE='queue'

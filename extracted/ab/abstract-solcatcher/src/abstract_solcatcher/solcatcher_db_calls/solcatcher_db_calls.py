from abstract_solana import *
from ..asyncUtils import *
from ..utils import *
from abstract_utilities import get_any_value,make_list

def get_all_txns(pair_id):
    transactions = call_solcatcher_db('/api/get_transactions',pair_id)
    return transactions
def process_logs(transaction):
    signature = get_any_value(transaction, 'signatures')
    if signature:
        slot = get_any_value(transaction, 'slot')
        logs = get_any_value(transaction, 'logMessages')
        program_id = '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'
        response = call_solcatcher_ts('process-logs', signature=signature, slot=slot, program_id=program_id, logs=logs)
        return signature
def get_pair(pair_id=None,mint=None,signature=None):
    try:
        raw_pair_data = call_solcatcher_db('/api/get_pair',mint=mint,pair_id=pair_id,signature=signature)
        pair_data = clean_pair_values(raw_pair_data)
        return pair_data
    except Exception as e:
        input(e)
def get_transactions(pair_id=None,txn_id=None,signature=None,log_id=None):
    try:
        raw_transactions = call_solcatcher_db('/api/get_transactions',pair_id=pair_id,txn_id=txn_id,signature=signature,log_id=log_id)
        return raw_transactions
    except Exception as e:
        input(e)
def decodeInstructionData(data):
    response = call_solcatcher_ts('decode-instruction-data', string=data,solcatcherSettings={"getResult":True,"getResponse":True})
    decodedData = get_result(response)
    return decodedData
def upsertPairData(pairData):
    response = call_solcatcher_ts('upsert-pair-by-id', pairData=pairData)
    pair_id = get_result(response)
    return pair_id
def upsert_txn(txData):
    response = call_solcatcher_ts('upsert-txn', txData=txData)
    txn_id = get_result(response)
    return txn_id
def get_if_single(obj):
    if obj and isinstance(obj,list) and len(obj)==1:
        obj = obj[0]
    return obj
def get_log_id(parsed_logs):
    if parsed_logs:
        return parsed_logs.get('id')
def get_user_address(parsed_logs):
    if parsed_logs:
        parsedLogs = parsed_logs.get('logs')
        for logData in parsedLogs:
            if logData.get('logs') and 'Instruction: Create' in logData.get('logs'):
                data = logData.get('data')
                if data:
                    decoded_data = decodeInstructionData(data[0])
                    user_address = decoded_data.get('user_address')
                    return user_address
def get_signature(address):
    genesis_signature = getGenesisSignature(address=address)
    return genesis_signature
def get_raw_log_data(signature):
    response = call_solcatcher_db('/api/fetch_any_combo',tableName='logdata',searchColumn='signature',searchValue=signature)
    raw_parsed_logs = call_solcatcher_db('/api/get_zip_rows',tableName='logdata',rows=response)
    return raw_parsed_logs
def get_log_data(signature):
    raw_parsed_logs = get_raw_log_data(signature)
    parsed_logs = get_if_single(raw_parsed_logs)
    return parsed_logs
def fetch_log_data(signature):
    transaction = get_transaction(signature)
    get_parsed_logs(transaction)
    parsed_logs = get_log_data(signature)
    return parsed_logs
def get_parsed_logs(transaction):
    raw_parsed_logs = process_logs(transaction)
    parsed_logs = get_if_single(raw_parsed_logs)
    return parsed_logs
def upsert_pair(pair_data):
    pair_id = upsertPairData(pair_data)
    return pair_id
def clean_pair_values(pair):
    pair = get_if_single(pair)
    if pair and isinstance(pair,dict):
        for key,value in pair.items():
            if isinstance(value,str):
                pair[key]= eatAll(value,['"',"'"])
    return pair
def update_log_data(logData):
    response = call_solcatcher_ts('update-logdata',logData=logData)
    log_id = get_result(response)
    return log_id
def delete_row(tableName,columnName,columnValue):
    print(f"deleting row in table {tableName} with {columnName} equaling {columnValue}")
    query = f"""START TRANSACTION;
    DELETE FROM {tableName} WHERE {columnName} = {columnValue};
    COMMIT;"""
    call_solcatcher_db('/api/query_data',query=query)

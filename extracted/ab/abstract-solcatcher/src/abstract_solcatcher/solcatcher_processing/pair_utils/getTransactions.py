import logging
import json
from abstract_utilities import get_logFile
from abstract_utilities import get_any_value
from abstract_solcatcher import *
logger = get_logFile('getTransactions')
def dump_if_json(obj):
    if not isinstance(obj, (str, bytes)):
        return json.dumps(obj)
    return obj

def create_gettransaction_table():
    """Create the gettransaction table if it does not exist."""
    query = """
    CREATE TABLE IF NOT EXISTS gettransaction (
        id SERIAL PRIMARY KEY,
        signature TEXT UNIQUE NOT NULL,
        slot INTEGER,
        program_id TEXT,
        pair_id INTEGER,
        log_id INTEGER,
        meta_id INTEGER,
        "transaction" JSONB DEFAULT '[]'::JSONB
    );
    """
    try:
        run_query(query)  # Make sure run_query is robust and handles exceptions
        logger.info("Created or confirmed existence of the gettransaction table.")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
create_gettransaction_table()

def run_query(query, values):
    logging.debug(f"Running query: {query}")
    logging.debug(f"Values: {values} (type: {type(values)})")
    return call_solcatcher_db('/api/query_data',query=query,values=values)
def fetch_transaction(signature,url_1_only=None,url_2_only=None):
    url_1_only = url_1_only if url_1_only != None else True
    url_2_only = url_2_only if url_2_only != None else False
    """
    Return raw RPC response for signatures on a specific address.
    """
    if signature:
        method = 'getTransaction'
        params = [signature,{"maxSupportedTransactionVersion":0}]
        return call_rate_limiter(method=method,params=params,url_1_only=url_1_only,url_2_only=url_2_only)

async def async_call_transaction(signature,url_1_only=None,url_2_only=None):
    """
    Return raw RPC response for signatures on a specific address.
    """
    transaction = await async_fetch_transaction(signature,url_1_only=url_1_only,url_2_only=url_2_only)
    txnData = await async_parse_program_log(transaction)
    txnData['id'] = upsert_gettransaction_to_db(txnData)
    return txnData

def call_transaction(signature,url_1_only=None,url_2_only=None):
    """
    Return raw RPC response for signatures on a specific address.
    """
    transaction = fetch_transaction(signature,url_1_only=url_1_only,url_2_only=url_2_only)
    txnData = parse_program_log(transaction)
    
    txnData['id'] = upsert_gettransaction_to_db(txnData)
    return txnData

async def async_get_transaction(signature):
    response = await run_query(query='SELECT * FROM gettransaction WHERE signature = %s',values=signature)
    return response

def get_transaction(signature):
    response = call_solcatcher_db('/api/query_data',query='SELECT * FROM gettransaction WHERE signature = %s',values=signature)
    
    return response

async def async_get_or_fetch_transaction(signature, url_1_only=None, url_2_only=None):
    try:
        txnData = get_transaction(signature)
        if not txnData:
            txnData = await async_call_transaction(signature, url_1_only=url_1_only, url_2_only=url_2_only)
        return get_transaction(signature)
    except Exception as e:
        logger.error(f"Error fetching or inserting transaction for signature {signature}: {e}")
        return None
def get_or_fetch_transaction(signature, url_1_only=None, url_2_only=True):
  
        txnData = get_transaction(signature)
        if not txnData:
            txnData = call_transaction(signature, url_1_only=url_1_only, url_2_only=url_2_only)
            input(txnData)
            upsert_gettransaction_to_db(txnData)
        return get_transaction(signature)

def upsert_gettransaction_to_db(txnData):
    """
    Insert or update transaction data in the `gettransaction` table.
    """
    query = """
        INSERT INTO gettransaction (signature, transaction, slot, program_id, pair_id, log_id, meta_id)
        VALUES (%s, %s::jsonb, %s, %s, %s, %s, %s)
        ON CONFLICT (signature)
        DO UPDATE
        SET
            transaction = EXCLUDED.transaction,
            slot = EXCLUDED.slot,
            program_id = EXCLUDED.program_id,
            pair_id = EXCLUDED.pair_id,
            log_id = EXCLUDED.log_id,
            meta_id = EXCLUDED.meta_id
        RETURNING id;
    """
    txn_id = run_query(
        query,
        (
            txnData.get('signature'),
            dump_if_json(txnData.get('transaction')),
            txnData.get('slot'),
            txnData.get('program_id'),
            txnData.get('pair_id'),
            txnData.get('log_id'),
            txnData.get('meta_id'),
        ),
    )
    return txn_id[0][0] if txn_id else None
def extract_first_value(results, key):
    """
    Extract the first value for the given key from a list of dictionaries.
    """
    if results and isinstance(results, list) and key in results[0]:
        return results[0][key]
    return None
async def get_genesis_get_transaction(address=None,mint=None,limit=1000, until=None):
    """
    Return raw RPC response for signatures on a specific address.
    """
    signature = await getOrFetchGenesisSignature(address=address, limit=limit, until=until)
    txnData = await get_or_fetch_transaction(signature)
    if txnData:
        return txnData['id']
async def async_parse_program_log(transaction):
    if not transaction:
        return {}
    signature = get_any_value(transaction, 'signatures')[0]
    slot = get_any_value(transaction, 'slot')
    logs = get_any_value(transaction, 'logMessages')
    program_id = '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'
    params = {"signature": signature, "slot": slot, "program_id": program_id, "logs": logs}
    try:
        signature = await async_call_solcatcher_ts(
            'process-logs', **params, solcatcherSettings={"getResponse": True, "getResult": True}
        )
        params['pair_id'] = extract_first_value(
            execute_query('SELECT pair_id FROM logdata WHERE signature = %s', (signature,)), 'pair_id'
        )
        params['meta_id'] = extract_first_value(
            execute_query('SELECT meta_id FROM pairs WHERE id = %s', (params['pair_id'],)), 'meta_id'
        )
    except Exception as e:
        logger.error(f"Error parsing transaction logs: {e}")
    params['transaction'] = transaction
    return params
def parse_program_log(transaction):
    if not transaction:
        return {}
    signature = get_any_value(transaction, 'signatures')[0]
    slot = get_any_value(transaction, 'slot')
    logs = get_any_value(transaction, 'logMessages')
    program_id = '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'
    params = {"signature": signature, "slot": slot, "program_id": program_id, "logs": logs}
    try:
        signature = call_solcatcher_ts(
            'process-logs', **params, solcatcherSettings={"getResponse": True, "getResult": True}
        )
        params['pair_id'] = extract_first_value(
            execute_query('SELECT pair_id FROM logdata WHERE signature = %s', (signature,)), 'pair_id'
        )
        params['meta_id'] = extract_first_value(
            execute_query('SELECT meta_id FROM pairs WHERE id = %s', (params['pair_id'],)), 'meta_id'
        )
    except Exception as e:
        logger.error(f"Error parsing transaction logs: {e}")
    params['transaction'] = transaction
    return params

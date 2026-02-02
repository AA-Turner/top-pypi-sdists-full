from .db import post_request,getZipRows
from abstract_utilities import make_list

def get_data(tableName=None,columnName=None,columnValues=None,**kwargs):
    columnName = make_list(columnName) if columnName else columnName
    columnValues = make_list(columnValues) if columnValues else columnValues
    result = post_request('fetch_any_combo',tableName=tableName,columnName=columnName,columnValues=columnValues,**kwargs)
    return result
def getZipRows(tableName=None,rows=None,schema=None):
    schema = schema or 'public'
    rows = rows or []
    result = post_request('getZipRows',tableName='pairs', rows=rows, schema=schema)
    return result
def get_all_pairs(schema='public'):
    tableName = 'pairs'
    rows = get_data(tableName=tableName,searchColumn='user_address',notNull=True)
    result = getZipRows(tableName, rows, schema='public')
    return result
def get_pair_from_id(pair_id,schema='public'):
    tableName = 'pairs'
    rows = get_data(tableName=tableName,searchColumn='id',columnValues=pair_id)
    result = getZipRows(tableName=tableName,rows=rows,schema=schema)
    return result
def get_meta_data_from_id(meta_id,schema='public'):
    tableName = 'metadata'
    rows = get_data(tableName=tableName,searchColumn='id',columnValues=meta_id)
    result = getZipRows(tableName=tableName,rows=rows,schema=schema)
    return result
def get_txns_from_pair_id(pair_id,schema='public'):
    tableName = 'transactions'
    rows = get_data(tableName=tableName,searchColumn='pair_id',columnValues=pair_id)
    result = getZipRows(tableName=tableName,rows=rows,schema=schema)
    return result
def get_genesis_txn_from_log_id(log_id,schema='public'):
    tableName = 'metadata'
    rows = get_data(tableName=tableName,searchColumn='log_id',columnValues=log_id)
    result = getZipRows(tableName=tableName,rows=rows,schema=schema)
    return result
def get_meta_data_by_mint(mint,schema='public'):
    tableName = 'metadata'
    rows = get_data(tableName=tableName,searchColumn='mint',columnValues=mint)
    result = getZipRows(tableName=tableName,rows=rows,schema=schema)
    return result
def get_assigned_account(addresses,schema='public'):
    tableName = 'wallet_account_assignments'
    assigned_account = post_request('getZipRows',columnNames = 'assigned_account',tableName=tableName, searchValues=addresses,anyValue=True)
    if assigned_account:
        assigned_account = assigned_account[0][0]  # Extract the first result
    return assigned_account
def if_signature_get_txn(obj,schema='public'):
    if not isinstance(obj,str):
        return obj
    if len(obj) ==88:
        obj = get_data(tableName='transactions', searchColumn='signature', searchValue=obj)
        obj = make_list(obj)
    return obj
def get_txns_for_pair_from_pair_id(pair_id,schema='public'):
    logs  = get_txns_from_pair_id(pair_id)
    tcns = []
    for i,log in enumerate(logs):
        signature = log['signature']
        for tcn in log['tcns']:
            tcn['signature']=signature
            tcns.append(tcn)
    return tcns

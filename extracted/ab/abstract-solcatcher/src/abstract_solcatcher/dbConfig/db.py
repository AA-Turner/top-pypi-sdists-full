import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set level to INFO or higher
import traceback,requests,psycopg2,json
from abstract_utilities import make_list,is_number
from ..asyncUtils import call_solcatcher_db,call_solcatcher_py
from abstract_apis import *
def is_mint(obj):
    len_mint = len('BhUFe1HDRxurfGGRCrDSDtVg2tcrmNXpZQHvYzAhpump')
    if len(str(obj)) == len_mint:
        return True
    return False
def is_signature(obj):
    len_mint = len('4W89xcgqqEp6Bo5pEJTReRaKkDY3dkbCuPpmQG7AAECiqgwqP7sqWAxxZb2cTkMdvuXjYj6zx7g6VFgrb7iz8c6y')
    if len(str(obj)) == len_mint:
        return True
    return False
keysConvertJS = {'log_id':'logdata', 'meta_id':'metadata','txn_id':'transactions','pair_id':'pairs'}
def get_headers():
    return {
        'Content-Type': 'application/json',
        # Add other headers if necessary
    }
def post_request(endpoint,**kwargs):
    result = call_solcatcher_db(endpoint,solcatcherSettings={"getResult":None},**kwargs)
    return get_response(result)
def get_column_names(tableName,schema='public'):
    return post_request('get_column_names',tableName=tableName,schema=schema)
def aggregate_rows(query, values=None, errorMsg='Error Fetching Rows'):
    return post_request('aggregate_rows',query=query, values=values, errorMsg=errorMsg)
def fetch_any_combo(columnNames=None, tableName=None, searchColumn=None, searchValue=None, anyValue=False,notNull=False, zipit=True):
    if tableName and columnNames==None:
        columnNames = get_column_names(tableName).get('columns')
    return post_request('fetch_any_combo',columnNames=columnNames, tableName=tableName, searchColumn=searchColumn, searchValue=searchValue, anyValue=anyValue,notNull=notNull, zipit=zipit)
def getZipRows(tableName, rows, schema='public'):
    return post_request('getZipRows',tableName=tableName,rows=rows,schema=schema)
def get_signatures(address,before=None):
    return post_request('call-signatures',address=address,before=before)
def get_all_wallet_assignments():
    return post_request('all-wallet-assignments')
def update_signatures(address,before=None):
    return post_request('update-signatures',address=address,before=before)
def assign_wallet(address):
    return post_request('assign-wallet',address=address)
def get_existing_signatures(address):
    return post_request('get-signatures',address=address)
def get_main_data_columns(main_columns,main_data):
    return post_request('get-get_main_data_columns',main_columns=main_columns,main_data=main_data)
def generate_chart(txn_history):
    return post_request('get-generate_chart',txn_history=txn_history)
def insertSignature(address):
    return post_request('get-generate_chart',txn_history=txn_history)
def get_assigned_account(address):
    query = "SELECT assigned_account FROM wallet_account_assignments WHERE address = %s;"
    assigned_account = aggregate_rows(query,(address,))
    if assigned_account:
        assigned_account = assigned_account[0][0]
    return assigned_account
def get_all_addresses_in_assigned_account(assigned_account):
    query = "SELECT address FROM wallet_account_assignments WHERE assigned_account = %s;"
    return aggregate_rows(query,(assigned_account,))
def get_all_pairs_for_addresses_in_assigned_account(addresses):
    query = "SELECT id FROM wallet_account_assignments WHERE user_address = ANY(%s);"
    return aggregate_rows(query,(addresses,))
def get_all_mints_for_addresses_in_assigned_account(ids):
    query = "SELECT mint FROM pairs WHERE id = ANY(%s);"
    return aggregate_rows(query,(ids,))
def get_all_assigned_accounts_for_address(address):
    assigned_account = get_assigned_account(address)
    if not assigned_account:
        assigned_account = update_signatures(address)
        if assigned_account:
           assigned_account = assigned_account.get('assigned_account')
    addresses = get_all_addresses_in_assigned_account(assigned_account)
    return addresses
def get_all_pairs_for_address(address):
    addresses = get_all_assigned_accounts_for_address(address)
    pair_ids = get_all_pairs_for_addresses_in_assigned_account(addresses)
    return pair_ids
def get_all_mints_for_address(address):
    pair_ids = get_all_pairs_for_address(address)
    mints = get_all_mints_for_addresses_in_assigned_account(pair_ids)
    return mints
def search_table_for_id(tableName,value):
    allPairRows = fetch_any_combo(columnNames='*', tableName=tableName,searchColumn='id',searchValue=value)
    return allPairRows
def get_all_txns_for_pair(*args,**kwargs):
    pair_id = get_pair_id(*args,**kwargs)
    allPairRows = fetch_any_combo(columnNames='*', tableName='transactions',searchColumn='pair_id',searchValue=pair_id)
    return allPairRows
def get_pair_id(*args,**kwargs):
    id = None
    for key,value in kwargs.items():
        if key == 'pair_id':
            id = value
        if key == 'pair':
            id = value.get('id')
        if key == 'mint':
            searchColumn='mint'
            searchValue=value
            rows= fetch_any_combo(columnNames='*', tableName='transactions', searchColumn=searchColumn,searchValue=searchValue)
            if rows:
                id = rows.get('id')
        if key == 'signature':
            searchColumn='signature'
            searchValue=value
            rows= fetch_any_combo(columnNames='*', tableName='transactions', searchColumn=searchColumn,searchValue=searchValue)
            if rows:
                id = rows.get('id')
    for arg in list(args):
        if is_number(arg):
            id = arg
        elif isinstance(arg,dict):
            id = arg.get('id')
        elif is_signature(arg):
            searchColumn='signature'
            searchValue=arg
            rows= fetch_any_combo(columnNames='*', tableName='transactions', searchColumn=searchColumn,searchValue=searchValue)
            if rows:
                id = rows.get('id')    
        elif is_mint(arg):
            searchColumn='mint'
            searchValue=arg
            rows= fetch_any_combo(columnNames='*', tableName='transactions', searchColumn=searchColumn,searchValue=searchValue)
            if rows:
                id = rows.get('id')
    if id:
        return id
def get_pair_by(**kwargs):
    for key,value in kwargs.items():
        if key=='pair':
            return pair
        rows= fetch_any_combo(columnNames='*', tableName='transactions', searchColumn=key,searchValue=value)
        if rows:
            if isinstance(rows,list):
                rows = rows[0]
            return rows
def get_pair_data(**kwargs):
    pair = get_pair_by(**kwargs)
    pair_id = pair.get('id')
    row = fetch_any_combo(columnNames='*', tableName='pairs',searchColumn='id',searchValue=pair_id)
    pair_column = get_column_data(row)
    pair_column['transactions']=get_all_txns_for_pair(pair_id)
    return pair_column
def get_column_data(row,exclude=['log_id']):
    new_js = {}
    exclude = make_list(exclude)
    for key,value in row[0].items():
        if key not in exclude:
            newKey = keysConvertJS.get(key)
            if newKey:
                newValue = search_table_for_id(newKey,value)
                if newValue:
                    key = newKey
                    value = newValue
            new_js[key] =value
    return new_js

def get_txns_from_pair_id(*args,**kwargs):
    pair_id = get_pair_id(*args,**kwargs)
    print(*args,**kwargs)
    return get_all_txns_for_pair(pair_id)
def get_pairs_from_user_wallets(user_wallets):
    return getZipRows('pairs', aggregate_rows('''SELECT * FROM pairs WHERE user_address = ANY(%s);''',[user_wallets]), schema='public')
def get_txns_for_pair_from_pair_id(*args,**kwargs):
    pair_id = get_pair_id(*args,**kwargs)
    logs  = get_txns_from_pair_id(pair_id)
    tcns = []
    for i,log in enumerate(logs):
        signature = log['signature']
        for tcn in log['tcns']:
            tcn['signature']=signature
            tcns.append(tcn)
    return tcns

def get_time(minutes=0, hours=0, days=0, weeks=0, years=0):
    """Calculate a UNIX timestamp for the given time offset."""
    mins = 60
    hr = 60 * mins
    day = 24 * hr
    week = 7 * day
    year = 365 * day
    timeStamp = time.time() - ((mins * minutes) + (hr * hours) + (day * days) + (week * weeks) + (year * years))
    return int(timeStamp)  # Return integer timestam


import logging
# Configure logging
logging.basicConfig(level=logging.INFO)  # Set level to INFO or higher
import traceback,requests,psycopg2,json
from abstract_utilities import make_list,is_number
from abstract_apis import *
from abstract_security import get_env_value
keysConvertJS = {'log_id':'logdata', 'meta_id':'metadata','txn_id':'transactions','pair_id':'pairs'}
from .asyncUtils import call_solcatcher_db

def call_solcatcher_db(endpoint,*args,**kwargs):
    response = call_solcatcher_db(endpoint,*args,**kwargs)
    return get_response(response)
def get_column_names(tableName,schema='public'):
    return call_solcatcher_db('get_column_names',tableName=tableName,schema=schema)
def aggregate_rows(query, values=None, errorMsg='Error Fetching Rows'):
    return call_solcatcher_db('aggregate_rows',query=query, values=values, errorMsg=errorMsg)
def fetch_any_combo(columnNames=None, tableName=None, searchColumn=None, searchValue=None, anyValue=False, zipit=True):
    if tableName and columnNames==None:
        columnNames = get_column_names(tableName).get('columns')
    return call_solcatcher_db('fetch_any_combo',columnNames=columnNames, tableName=tableName, searchColumn=searchColumn, searchValue=searchValue, anyValue=anyValue, zipit=zipit)
def getZipRows(tableName, rows, schema='public'):
    return call_solcatcher_db('getZipRows',tableName=tableName,rows=rows,schema=schema)
def get_signatures(address,before=None):
    return call_solcatcher_db('call-signatures',address=address,before=before)
def get_all_wallet_assignments():
    return call_solcatcher_db('all-wallet-assignments')
def update_signatures(address,before=None):
    return call_solcatcher_db('update-signatures',address=address,before=before)
def assign_wallet(address):
    return call_solcatcher_db('assign-wallet',address=address)
def get_existing_signatures(address):
    return call_solcatcher_db('get-signatures',address=address)
def get_main_data_columns(main_columns,main_data):
    return call_solcatcher_db('get-get_main_data_columns',main_columns=main_columns,main_data=main_data)
def generate_chart(txn_history):
    return call_solcatcher_db('get-generate_chart',txn_history=txn_history)
def insertSignature(address):
    return call_solcatcher_db('get-generate_chart',txn_history=txn_history)
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
def get_pair_id(arg=None,id=None,mint=None,signature=None,pair=None):
    if arg:
        if isinstance(arg,dict):
            pair = arg
        elif is_number(arg):
            id = arg
        else:
            mint=arg
            signature=arg
        
    if pair:
        searchColumn='id'
        id = pair.get('id')
    if mint or signature:
        if mint:
            searchColumn='mint'
            searchValue=mint
        else:
            searchColumn='signature'
            searchValue=signature
        rows= fetch_any_combo(columnNames='*', tableName='transactions', searchColumn=searchColumn,searchValue=searchValue)
        if rows:
            id = rows.get('id')    
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
    transactions = get_all_txns_for_pair(pair_id)
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

def fetch_filtered_transactions(sol_amount, operator="<", timestamp=None, timestamp_operator=None):
    """
    Fetch filtered transactions based on Solana amount and optional timestamp filtering.

    :param sol_amount: Solana amount to filter transactions by.
    :param operator: Comparison operator for sol_amount ('>', '<=', etc.). Default is '>'.
    :param timestamp: Optional timestamp for filtering transactions.
    :param timestamp_operator: Operator for timestamp comparison ('>', '<=', etc.).
    :return: List of filtered transactions.
    """
    # Validate operators
    valid_operators = [">", "<=", "=", "<", ">="]
    if operator not in valid_operators:
        raise ValueError(f"Invalid operator for sol_amount: {operator}. Must be one of {valid_operators}")
    if timestamp_operator and timestamp_operator not in valid_operators:
        raise ValueError(f"Invalid operator for timestamp: {timestamp_operator}. Must be one of {valid_operators}")

    # Start SQL query
    query = f"""
    SELECT 
        t.id AS transaction_id,
        t.signature AS transaction_signature,
        t.tcns AS transaction_details,
        p.id AS pair_id,
        p.signature AS genesis_signature,
        p.mint AS mint_address
    FROM 
        transactions t
    JOIN 
        pairs p 
    ON 
        t.pair_id = p.id
    WHERE 
        p.signature IS NOT NULL
    AND 
        t.program_id = p.program_id
    AND 
        EXISTS (
            SELECT 1
            FROM jsonb_array_elements(t.tcns) AS elem
            WHERE 
                (elem ->> 'sol_amount')::numeric {operator} %s
    """

    # Add timestamp filter if provided
    params = [sol_amount]
    if timestamp and timestamp_operator:
        query += f" AND (elem ->> 'timestamp')::bigint {timestamp_operator} %s"
        params.append(int(timestamp))  # Ensure timestamp is an integer

    # Close EXISTS clause
    query += ")"

    # Final ordering clause
    query += " ORDER BY t.updated_at DESC;"

    # Execute query
    return aggregate_rows(query, params)

def fetch_filtered_transactions(sol_amount, operator="<", timestamp=None, timestamp_operator=None):
    """
    Fetch filtered transactions based on Solana amount and optional timestamp filtering.

    :param sol_amount: Solana amount to filter transactions by.
    :param operator: Comparison operator for sol_amount ('>', '<=', etc.). Default is '>'.
    :param timestamp: Optional timestamp for filtering transactions.
    :param timestamp_operator: Operator for timestamp comparison ('>', '<=', etc.).
    :return: List of filtered transactions.
    """
    # Validate operators
    valid_operators = [">", "<=", "=", "<", ">="]
    if operator not in valid_operators:
        raise ValueError(f"Invalid operator for sol_amount: {operator}. Must be one of {valid_operators}")
    if timestamp_operator and timestamp_operator not in valid_operators:
        raise ValueError(f"Invalid operator for timestamp: {timestamp_operator}. Must be one of {valid_operators}")

    # Start SQL query
    query = f"""
    SELECT 
        t.id AS transaction_id,
        t.signature AS transaction_signature,
        t.tcns AS transaction_details,
        p.id AS pair_id,
        p.signature AS genesis_signature,
        p.mint AS mint_address
    FROM 
        transactions t
    JOIN 
        pairs p 
    ON 
        t.pair_id = p.id
    WHERE 
        p.signature IS NOT NULL
    AND 
        t.program_id = p.program_id
    AND 
        EXISTS (
            SELECT 1
            FROM jsonb_array_elements(t.tcns) AS elem
            WHERE 
                (elem ->> 'sol_amount')::numeric {operator} %s
    """

    # Add timestamp filter if provided
    params = [sol_amount]
    if timestamp and timestamp_operator:
        query += f" AND (elem ->> 'timestamp')::bigint {timestamp_operator} %s"
        params.append(int(timestamp))  # Ensure timestamp is an integer

    # Close EXISTS clause
    query += ")"

    # Final ordering clause
    query += " ORDER BY t.updated_at DESC;"

    # Execute query
    return aggregate_rows(query, params)

import time
def fetch_filtered_transactions_paginated(
    sol_amount, 
    operator="<", 
    timestamp=None, 
    timestamp_operator=None, 
    limit=50, 
    offset=0
):
    query = f"""
    SELECT 
        t.id AS transaction_id,
        t.signature AS transaction_signature,
        t.tcns AS transaction_details,
        p.id AS pair_id,
        p.signature AS genesis_signature,
        p.mint AS mint_address
    FROM 
        transactions t
    JOIN 
        pairs p 
    ON 
        t.pair_id = p.id
    WHERE 
        p.signature IS NOT NULL
    AND 
        t.program_id = p.program_id
    AND 
        EXISTS (
            SELECT 1
            FROM jsonb_array_elements(t.tcns) AS elem
            WHERE (elem ->> 'sol_amount')::numeric {operator} %s
    """

    params = [sol_amount]
    if timestamp and timestamp_operator:
        query += f" AND (elem ->> 'timestamp')::bigint {timestamp_operator} %s"
        params.append(int(timestamp))

    query += f") ORDER BY t.updated_at DESC LIMIT %s OFFSET %s;"
    params.extend([limit, offset])

    return aggregate_rows(query, params)

def get_time(minutes=0, hours=0, days=0, weeks=0, years=0):
    """Calculate a UNIX timestamp for the given time offset."""
    mins = 60
    hr = 60 * mins
    day = 24 * hr
    week = 7 * day
    year = 365 * day
    timeStamp = time.time() - ((mins * minutes) + (hr * hours) + (day * days) + (week * weeks) + (year * years))
    return int(timeStamp)  # Return integer timestamp
def ge_time(minutes=0, hours=0, days=0, weeks=0, years=0):
    """Calculate a UNIX timestamp for the given time offset."""
    mins = 60
    hr = 60 * mins
    day = 24 * hr
    week = 7 * day
    year = 365 * day
    timeStamp = time.time() - ((mins * minutes) + (hr * hours) + (day * days) + (week * weeks) + (year * years))
    return int(timeStamp)  # Return integer timestamp

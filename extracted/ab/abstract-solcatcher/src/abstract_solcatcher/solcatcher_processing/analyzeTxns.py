from dateutil import parser
from functools import lru_cache
import itertools,math
from ..dbConfig import *
from .transactionProcessor import TransactionProcessor
from abstract_utilities import make_list
from abstract_security import *
from datetime import datetime
from statistics import mean
from ..managers.metaDataManager import *
from .poolMetrics import *
metaDataMgr = metaDataManager()
tables="""token_metadata
transactions
owneraccounts
token_data
wallet_account_assignments
account_bonding_curves
transaction_signatures
metadata
useraddresses
logdata
pairs
getsignaturesforaddress
"""
def get_env_path():
    return '/home/development/finalDatabase/.env'


def get_key_value(key, path=None):
    path = path or get_env_path()
    return get_env_value(key=key, path=path)




def get_signature_placement(obj,num):
    int((num-len(str(obj)))/2)
    newStr = ''
    for i in range(int((num-len(str(obj)))/2)):
       newStr+=' ' 
    return f"{newStr}{obj}{newStr}"
def get_pairs():
    tab = '\t'
    all_pairs =get_all_pairs()
    
    for pair in reversed(all_pairs):
        processor = TransactionProcessor(pair)
        user_wallets = processor.user_wallets
        profits = processor.profits
        user_wallets = processor.user_wallets
        pair['transactions'] = processor.clean_txns(processor.all_txns)
        for wallet,values in profits.items():
            print(f"wallet: {wallet}")
            unique_txns = processor.get_sorted_unique_txns(values['txns'])
        
            print(f"{tab}{tab}txn_no{tab}{tab}{get_signature_placement('signature',94)}{tab}{tab}{get_signature_placement('amount',14)}{tab}{tab}{get_signature_placement('volume',14)}")
            for txn in unique_txns:
                sig = ""
                if txn['signature'][-1] ==  ' ':
                    sig = f"{tab}"
                print(f"{tab}{tab}{txn['txn_number']}{tab}{tab}{txn['signature']}__{sig}{tab}{tab}{get_signature_placement(txn['sol_amount'],14)}{tab}{tab}{txn['volume']}")
        input(processor.ranking())    


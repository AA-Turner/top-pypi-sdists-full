import itertools
from datetime import datetime
from abstract_utilities import make_list
from ..dbConfig import *
from ..managers.metaDataManager import *
from .poolMetrics import *
metaDataMgr = metaDataManager()
def rank_supply(supply,initial_pool_tokens):
    if supply == None or supply == 0:
        return 0
    percent_tokens_available = initial_pool_tokens/supply
    deviation = 1-percent_tokens_available
    score = 20 - abs(10 - deviation)
    if score<0:
        score = 0
    return score
def metaDataRanking(metaDataVars):
    total_score = 0
    metaDataScores = {
    'image':  ['bools',2,0],
    'uri':  ['bools',2,0],
    'symbol': ['bools',2,0],
    'name': ['bools',2,0],
    'mintAuthority': ['processed',0,2],
    'freezeAuthority': ['processed',0,2],
    'twitter':  ['bools',6,0],
    'website': ['bools',6,0],
    'isMutable': ['processed',2,0],
    'primarySaleHappened': ['processed',6,0],
    'description': ['bools',6,0],
    }
    for key,values in metaDataScores.items():
        if metaDataVars[values[0]]:
            total_score+= values[1]
        else:
           total_score+= values[-1]
    return total_score
def if_signature_get_txn(obj):
    if not isinstance(obj,str):
        return obj
    if len(obj) ==88:
        obj = fetch_any_combo(columnNames='*', tableName='transactions', searchColumn='signature', searchValue=obj)
        obj = make_list(obj)
    return obj
def rank_initial_liquidity(initial_sol_amount):
    if initial_sol_amount >=20:
        return 100
    if initial_sol_amount>=10:
        remainder = 20 - initial_sol_amount
        return 100 - (remainder*3)
    if initial_sol_amount>=5:
        remainder = 10 - initial_sol_amount
        return 70 - (remainder*4)
    if initial_sol_amount<5:
        remainder = 5 - initial_sol_amount
        return 30 - (remainder*6)
    return 0

def score_total_profits_enhanced(total_profits, num_txns, creation_time, last_significant_txn_time,
                                 norm_params, weights, decay_rate=0.1, current_time=None):
    """
    Enhanced scoring function with time decay applied to last significant transaction.
    
    :param total_profits: Total profits of the pool (float)
    :param num_txns: Number of transactions (int)
    :param creation_time: ISO formatted creation timestamp (str)
    :param last_significant_txn_time: ISO formatted last significant txn timestamp (str)
    :param norm_params: Dictionary with min and max values for normalization
    :param weights: Dictionary with weights for each metric
    :param decay_rate: Decay rate for time-based metrics (float)
    :param current_time: Current datetime object (optional)
    :return: Activity score (float)
    """
    if current_time is None:
        current_time = datetime.utcnow()
    
    # Convert timestamps to datetime objects
    creation_dt = datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%SZ')
    last_significant_dt = datetime.strptime(last_significant_txn_time, '%Y-%m-%dT%H:%M:%SZ')
    
    # Calculate time since creation and last significant transaction in days
    time_since_creation = (current_time - creation_dt).total_seconds() / 86400  # in days
    time_since_last_significant_txn = (current_time - last_significant_dt).total_seconds() / 86400  # in days
    
    # Apply time decay
    decay_creation = time_decay(time_since_creation, decay_rate)
    decay_last_significant = time_decay(time_since_last_significant_txn, decay_rate)
    
    # Normalize metrics
    V_norm = min_max_normalize(total_profits, norm_params['total_profits_min'], norm_params['total_profits_max'])
    N_norm = min_max_normalize(num_txns, norm_params['num_txns_min'], norm_params['num_txns_max'])
    C_norm = min_max_normalize(decay_creation, norm_params['creation_time_min'], norm_params['creation_time_max'])
    L_norm = min_max_normalize(decay_last_significant, norm_params['last_significant_txn_time_min'], norm_params['last_significant_txn_time_max'])
    
    # Calculate the weighted sum
    activity_score = (
        weights['V'] * V_norm +
        weights['N'] * N_norm +
        weights['C'] * C_norm +
        weights['L'] * L_norm
    )
    return activity_score
        #{'V','N','C','L'} * L_norm

class TransactionProcessor:
    def __init__(self, pair):
        """Initialize the transaction processor with a list of transactions."""
        self.pair = pair
        if 'error' not in self.pair:
            self.mint = self.get_mint()
            self.pair_id = self.pair.get('id')
            
            self.owner_address= self.get_pool_creator()
            
            self.genesis_signature = self.get_genesis_signature()
            
            self.all_txns = get_txns_for_pair_from_pair_id(self.pair_id)  # Clean and process transactions only once
            self.genesisTxn = [txn for txn in self.all_txns if txn.get('signature') == self.genesis_signature]
            self.creation_time = self.genesisTxn[0]['timestamp']
            
            self.all_txns = [txn for txn in self.all_txns if txn.get('signature') != self.genesis_signature]
            if 'error' not in self.all_txns:
                #self.genesisTxn,self.all_txns = self.separate_genesis_txn(self.pair,self.all_txns)
                self.initial_sol_amt = self.genesisTxn[0]['sol_amount']
                self.initial_token_amt = self.genesisTxn[0]['token_amount']
                self.user_wallets = self.get_all_user_wallets()
                self.total_profits = self.tally_profits()
                self.metaDataVars = metaDataMgr.processMetaData(self.mint,imageData=False)
                self.metaDataBools = self.metaDataVars.get('bools')
                self.assigned_account = get_assigned_account(self.owner_address)
                self.pool_metrics = calculateMetrics([{**self.pair,'transactions':self.all_txns}])
                self.profits = self.tally_profits(self.all_txns)
                self.total_profits = self.total_profit(self.profits) 
                self.previous_pairs = get_pairs_from_user_wallets(self.user_wallets)
        
    def ranking(self):
        supply_score = rank_supply(metaDataMgr.datas_js['supply'],self.initial_token_amt) # target 90% in pool initial; 20 pts
        metadata_score = metaDataRanking(self.metaDataVars) # target all metas in good standing; 36 pts
        initial_liquidity_score = rank_initial_liquidity(self.initial_sol_amt) # target above 20 initial sol; 100 pts
        active_time = self.pool_metrics[0].get('time_of_last_significant_txn') - self.creation_time
        dead_time = time.time() - self.pool_metrics[0].get('time_of_last_significant_txn')
        #profits_score = score_total_profits_enhanced(self.total_profits,len(self.all_txns),)# 100 pts
        previous_pairs_grades = self.rank_previous_pairs(self.previous_pairs)# 150 pts
        previous_pair_grade = sum(previous_pairs_grades)/len(previous_pairs_grades)
        total_score = supply_score+metadata_score+initial_liquidity_score
        pair_grade = total_score/(20+36+100)
        previous_pairs_grades.append(pair_grade)
        overall_grade = sum(previous_pairs_grades)/len(previous_pairs_grades)
        scores = {"active_time":active_time,"dead_time":dead_time,"supply_score":supply_score,"metadata_score":metadata_score,"initial_sol_score":initial_liquidity_score,"previour_pair_grade":previous_pair_grade,"pair_grade":pair_grade,"overall_grade":overall_grade}
        return scores
    def rank_previous_pairs(self,pairs):
        total_grades = []
        for pair in pairs:
            pair_txns = get_txns_for_pair_from_pair_id(pair['id'])
            genesisTxn,txns = self.separate_genesis_txn(pair=pair,txns=pair_txns)
            profits = self.tally_profits(txns)
            total_profits = self.total_profit(profits)
            time_alive = self.calculate_time_interval(txns)
            pool_metrics = calculateMetrics([{**pair,'transactions':pair_txns}])
            metaDataVars = metaDataMgr.processMetaData(pair.get('mint'),imageData=False)
            metadata_score = metaDataRanking(metaDataVars)
            metaDataBools = metaDataVars.get('bools')
            metaDataprocessed = metaDataVars.get('processed')
            supply_score = rank_supply(metaDataprocessed['supply'],genesisTxn[0]['token_amount'])
            initial_liquidity_score = rank_initial_liquidity(genesisTxn[0]['sol_amount'])
            total_score = supply_score+metadata_score+initial_liquidity_score
            grade = total_score/(20+36+100)
            scores = {"supply_score":supply_score,"metadata_score":metadata_score,"initial_sol_score":initial_liquidity_score}
            total_grades.append(grade)
        return total_grades
    def get_total_profits(self,txns=None):
        if txns:
            return self.tally_profits(txns)
        if hasattr(self,'total_profits'):
            return self.total_profits
        self.total_profits = self.tally_profits()
        return self.total_profits
    def get_all_user_wallets(self,txns=None):
        if txns:
            total_profits = self.get_total_profits(txns)
            return list(total_profits.keys())
        if hasattr(self,'user_wallets'):
            return self.user_wallets
        total_profits = self.get_total_profits()
        self.user_wallets = list(total_profits.keys())
        return self.user_wallets
    def get_mint(self,pair=None):
        if pair:
            mint = pair.get('mint')
            return mint
        if hasattr(self,'mint'):
            return self.mint
        self.mint = self.pair.get('mint')
        return self.mint
    def get_genesis_txn(self,pair=None):
        if pair:
            genesisTxn,_ = self.separate_genesis_txn(pair)
            return genesisTxn
        if hasattr(self,'genesisTxn'):
            return self.genesisTxn
        self.genesisTxn,self.all_txns = self.separate_genesis_txn()
        return self.genesisTxn
    def get_all_txns(self,pair=None):
        if pair:
            _,all_txns = self.separate_genesis_txn(pair)
            return all_txns
        if hasattr(self,'all_txns'):
            return self.all_txns
        self.genesisTxn,self.all_txns = self.separate_genesis_txn()
        return self.all_txns
    def get_initial_sol_amt(self,pair=None):
        genesisTxn = self.get_genesis_txn(pair)
        if pair:
            return self.get_total_sol_volume(genesisTxn)
        if hasattr(self,'initial_sol_amt'):
           return self.initial_sol_amount 
        genesis_txns = self.get_genesis_signature(pair)
        self.initial_sol_amt = self.get_total_sol_volume(genesis_txns)
        return self.initial_sol_amt 
    def get_initial_token_amt(self,pair=None):
        genesisTxn = self.get_genesis_txn(pair)
        if pair:
            return self.get_total_token_volume(genesisTxn)
        if hasattr(self,'initial_token_amt'):
           return self.initial_token_amount 
        genesis_txns = self.get_genesis_signature(pair)
        self.initial_token_amt = self.get_total_token_volume(genesis_txns)
        return self.initial_token_amt 
    def get_txns(self,txns=None):
        if not txns:
            if hasattr(self,'all_txns'):
                return self.all_txns        
        return if_signature_get_txn(txns)
    def get_pool_creator(self,pair=None):
        if pair:
            return pair.get('user_addres')
        if hasattr(self,'user_addres'):
           return self.owner_address 
        self.owner_address = self.pair.get('user_addres')
        return self.owner_address 
    def get_genesis_signature(self,pair=None):
        if pair:
            return pair.get('signature')
        if hasattr(self,'signature'):
           return self.genesis_signature 
        self.genesis_signature = self.pair.get('signature')
        return self.genesis_signature
    def get_pair_creation_time(self,pair=None):
        if pair:
            return pair.get('creation_time')
        if hasattr(self,'creation_time'):
           return self.creation_time 
        self.creation_time = self.pair.get('creation_time')
        return self.creation_time
    def get_all_pair_txns(self,pair=None):
        pair = pair or self.pair
        pair_txns = get_txns_for_pair_from_pair_id(pair)
        unique_txns = self.remove_duplicates(pair_txns)
        sorted_txns = self.sort_txns_by_time(unique_txns)
        return sorted_txns
    def clean_txns(self, txns):
        """Clean, sort, and enumerate transactions."""
        unique_txns = self.remove_duplicates(txns)
        sorted_txns = self.sort_txns_by_time(unique_txns)
        enumerated_txns = self.enumerate_txns(sorted_txns)
        return enumerated_txns

    def remove_duplicates(self, transactions):
        """Remove duplicates from transactions using a composite key."""
        key_fields = ['invocation_number', 'isbuy', 'log_id', 'mint', 'timestamp', 'user_address', 'signature']
        seen_keys = set()
        unique_transactions = []
        for txn in transactions:
            composite_key = '-'.join(str(txn.get(field)) for field in key_fields)
            if composite_key not in seen_keys:
                seen_keys.add(composite_key)
                unique_transactions.append(txn)
        return unique_transactions

    def sort_txns_by_time(self, txns):
        """Sort transactions by their timestamp."""
        timestamp_format = '%a, %d %b %Y %H:%M:%S %Z'
        return sorted(txns, key=lambda x: x['timestamp'])

    def enumerate_txns(self, txns):
        """Assign an enumeration to each transaction."""
        for i, txn in enumerate(txns):
            txn['txn_number'] = i
        return txns

    def calculate_time_interval(self,txns=None):
        """Calculate the interval between the first and last transaction."""
        txns = self.get_txns(txns)
        if len(txns) < 2:
            return None
        timestamp_format = '%a, %d %b %Y %H:%M:%S %Z'
        first_time = txns[0]['timestamp']
        last_time = txns[-1]['timestamp']
        return (last_time - first_time) / 60  # Return interval in minutes
    
    def get_token_amounts(self,txns=None):
        """Calculate net SOL amounts for each transaction."""
        txns = self.get_txns(txns)
        return [float(txn['token_amountui']) * (1 if txn['is_buy'] else -1) for txn in txns]

    def get_token_volume_amounts(self,txns=None):
        """Calculate absolute volume amounts for each transaction."""
        txns = self.get_txns(txns)
        return [abs(token) for token in self.get_token_amounts(txns)]

    def get_total_token_volume(self,txns=None):
        """Return the total volume of SOL amounts."""
        txns = self.get_txns(txns)
        return sum(semetaDataMgrlf.get_token_volume_amounts(txns))
    
    def get_net_token_amount(self,txns=None):
        """Return the net amount of SOL."""
        txns = self.get_txns(txns)
        return sum(self.get_token_amounts(txns))
    
    def get_sol_amounts(self,txns=None):
        """Calculate net SOL amounts for each transaction."""
        txns = self.get_txns(txns)
        return [float(txn['sol_amount']) * (1 if txn['is_buy'] else -1) for txn in txns]

    def get_sol_volume_amounts(self,txns=None):
        """Calculate absolute volume amounts for each transaction."""
        txns = self.get_txns(txns)
        return [abs(sol) for sol in self.get_sol_amounts(txns)]
    
    def get_total_sol_volume(self,txns=None):
        """Return the total volume of SOL amounts."""
        txns = self.get_txns(txns)
        return sum(self.get_sol_volume_amounts(txns))

    def get_net_sol_amount(self,txns=None):
        """Return the net amount of SOL."""
        txns = self.get_txns(txns)
        return sum(self.get_sol_amounts(txns))

    def separate_genesis_txn(self, pair=None,txns=None):
        """Separate the 'genesis' transaction from all other transactions."""
        txns = self.get_txns(txns)
        pair=pair or self.pair
        
        genesis_signature = pair.get('signature')
        all_txns = [txn for txn in txns if txn.get('signature') != genesis_signature]
        genesis_txns = [txn for txn in txns if txn.get('signature') == genesis_signature]

        return genesis_txns, self.clean_txns(all_txns)

    def get_sorted_unique_txns(self, signatures):
        """Get unique sorted transactions by a list of signatures."""
        wallet_txns = [self.get_txn_by_signature(sig) for sig in signatures]
        wallet_txns = [txn for txn in wallet_txns if txn]  # Filter None values
        txn_numbers = [txn['txn_number'] for txn in wallet_txns]
        sol_amounts = [abs(sol) for sol in self.get_sol_amounts()]
        sol_volumes = [abs(sol_amounts[i]) + abs(sol_amounts[i - 1]) if i > 0 else abs(sol_amounts[i]) for i in range(len(sol_amounts))]
        keys = ['signature', 'sol_amount', 'volume','txn_number']
        combined = [dict(zip(keys, values)) for values in zip(signatures, sol_amounts, sol_volumes,txn_numbers)]
        return combined

    def total_profit(self, profits):
        """Calculate total profit from a list of profits."""
        return sum([values['profits']['sol'] for key, values in profits.items()])

    def get_txn_by_signature(self, signature,txns=None):
        """Find and return a transaction by its signature."""
        txns = self.get_txns(txns)
        for txn in txns:
            if txn.get('signature') == signature:
                return txn
        return None

    def tally_profits(self,txns=None):
        """Organize and calculate profit, volume, and transaction data for each user."""
        txns = self.get_txns(txns)
        txnData_js = {}
        for txn in txns:
            user = txn['user_address']
            if user not in txnData_js:
                txnData_js[user] = {
                    "profits": {"sol": 0, "token": 0},
                    "avgPrice": {'token_amount': 0, 'sol': 0, "avg": 0},
                    "volume": {"sell": 0, "buy": 0, "total": 0},
                    "txns": []
                }
            solAmt = float(txn['sol_amount'])
            tknAmt = float(txn['token_amount'])
            txnData_js[user]["volume"]["total"] += solAmt

            if txn.get('isbuy'):
                txnData_js[user]["volume"]["buy"] += solAmt
                txnData_js[user]["profits"]["sol"] -= solAmt
            else:
                txnData_js[user]["volume"]["sell"] += solAmt
                txnData_js[user]["profits"]["sol"] += solAmt

            txnData_js[user]["avgPrice"]['token_amount'] += tknAmt
            txnData_js[user]["avgPrice"]['sol'] += solAmt
            txnData_js[user]["avgPrice"]["avg"] = (
                (txnData_js[user]["avgPrice"]['sol'] or 1) /
                (txnData_js[user]["avgPrice"]['token_amount'] or 1)
            )
            txnData_js[user]["txns"].append(txn['signature'])

        return txnData_js

    def get_price(self, virtual_sol_reserves, virtual_token_reserves):
        """Calculate price using reserves (this is a placeholder)."""
        if not virtual_sol_reserves or not virtual_token_reserves:
            return 0
        return virtual_sol_reserves / virtual_token_reserves



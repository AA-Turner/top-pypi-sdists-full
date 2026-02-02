from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from abstract_pandas import get_df
import math,time
from datetime import datetime
from statistics import mean
from abstract_utilities import make_list
def calculate_metrics(pool, current_time, significance_multiplier=2):
    transactions = pool['transactions']
    if not transactions:
        return {
            'pool_id': pool['id'],
            'total_volume': 0,
            'time_since_last_txn': float('inf'),
            'high_trade': 0,
            'average_trade': 0,
            'last_significant_trade': 0
        }
    total_volume = sum(txn['sol_amount'] for txn in transactions)
    timestamps = [txn['timestamp'] for txn in transactions]
    last_txn_time = max(timestamps)
    time_since_last_txn = (current_time - last_txn_time) / 86400  # in days
    high_trade_volume = max(txn['sol_amount'] for txn in transactions)
    average_trade_volume = mean(txn['sol_amount'] for txn in transactions)
    
    # Determine significance threshold
    significance_threshold = significance_multiplier * average_trade_volume
    last_significant_txn = transactions[-1]
    last_significant_volume = last_significant_txn['sol_amount']
    last_significant_txn_time = last_significant_txn['timestamp']
    last_significant_txn_id=last_significant_txn['signature']
    # Identify the last significant transaction
    significant_transactions = [txn for txn in transactions if txn['sol_amount'] >= significance_threshold]
    if significant_transactions:
        last_significant_txn = max(significant_transactions, key=lambda x: x['timestamp'])
        last_significant_volume = last_significant_txn['sol_amount']
        last_significant_txn_time=last_significant_txn['timestamp']
        last_significant_txn_id=last_significant_txn['signature']
    else:
        last_significant_volume = 0  # No significant transactions
    
    return {
        'pool_id': pool['id'],
        'total_volume': total_volume,
        'high_trade': high_trade_volume,
        'average_trade': average_trade_volume,
        'time_since_last_txn': time_since_last_txn,
        'time_of_last_txn':last_txn_time,
        'last_significant_txn':last_significant_txn_id,
        'last_significant_trade': last_significant_volume,
        'time_of_last_significant_txn':last_significant_txn_time,
    }

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 0.5  # Neutral value if no variation
    return (value - min_val) / (max_val - min_val)

def normalize_recency(time_since, min_time, max_time):
    if max_time == min_time:
        return 1  # All recencies are the same
    normalized = 1 - (time_since - min_time) / (max_time - min_time)
    return max(0, min(normalized, 1))  # Clamp between 0 and 1

def normalize_lstra(last_significant_volume, average_trade_volume, max_cap=5):
    if average_trade_volume == 0:
        return 0  # Avoid division by zero
    ratio = last_significant_volume / average_trade_volume
    ratio_clipped = min(ratio, max_cap)
    lstra_norm = ratio_clipped / max_cap
    return lstra_norm


def get_normalization_params(pools_metrics):
    pools_metrics = make_list(pools_metrics)
    volumes = [metrics['total_volume'] for metrics in pools_metrics]
    highs = [metrics['high_trade'] for metrics in pools_metrics]
    averages = [metrics['average_trade'] for metrics in pools_metrics]
    recencies = [metrics['time_since_last_txn'] for metrics in pools_metrics]
    
    # Handle cases where there might be no transactions
    volumes = [v for v in volumes if not math.isinf(v)]
    highs = [h for h in highs if not math.isinf(h)]
    averages = [a for a in averages if not math.isinf(a)]
    recencies = [t for t in recencies if not math.isinf(t)]
    
    return {
        'volume_min': min(volumes) if volumes else 0,
        'volume_max': max(volumes) if volumes else 1,
        'high_min': min(highs) if highs else 0,
        'high_max': max(highs) if highs else 1,
        'average_min': min(averages) if averages else 0,
        'average_max': max(averages) if averages else 1,
        'recency_min': min(recencies) if recencies else 0,
        'recency_max': max(recencies) if recencies else 1
    }

def calculate_activity_score(metrics, norm_params, weights):
    V_norm = normalize(metrics['total_volume'], norm_params['volume_min'], norm_params['volume_max'])
    H_norm = normalize(metrics['high_trade'], norm_params['high_min'], norm_params['high_max'])
    A_norm = normalize(metrics['average_trade'], norm_params['average_min'], norm_params['average_max'])
    T_rev_norm = normalize_recency(metrics['time_since_last_txn'], norm_params['recency_min'], norm_params['recency_max'])
    
    activity_score = (
        weights['V'] * V_norm +
        weights['H'] * H_norm +
        weights['A'] * A_norm +
        weights['R'] * T_rev_norm
    )
    
    return activity_score

def calculateMetrics(pools):
    current_time = time.time()
    
    # Step 1: Calculate metrics for each pool
    pools_metrics = [calculate_metrics(pool, current_time) for pool in make_list(pools)]
    
    # Step 2: Get normalization parameters
    norm_params = get_normalization_params(pools_metrics)
    
    # Step 3: Define weights
    weights = {
        'V': 0.3,  # Total Volume
        'H': 0.3, # High Trade Volume
        'A': 0.20, # Average Trade Volume
        'R': 0.20,   # Recency
    }
    
    # Step 4: Calculate activity scores
    for metrics in pools_metrics:
        score = calculate_activity_score(metrics, norm_params, weights)
        metrics['activity_score'] = score
        #print(f"Pool ID: {metrics['pool_id']}, Activity Score: {score:.2f}")
    
    # Optional: Determine if pool is active based on a threshold
    threshold = 0.5  # Example threshold
    all_metrics = {}
    for metrics in pools_metrics:
        metrics["is_active"]='Active' if metrics['activity_score'] >= threshold else 'Inactive'
        #print(f"Pool ID: {metrics['pool_id']}, Status: {metrics['is_active']}")

    return pools_metrics
# Assume you have a labeled dataset
# df contains columns: total_volume, time_since_last_txn, high_trade, average_trade, is_active
def machine_learn_it(pools):
    # Step 1: Calculate metrics for each pool
    metrics = calculateMetrics(pools)
    
    # Step 2: Convert metrics to DataFrame
    df = get_df(metrics)  # Ensure get_df returns a pandas DataFrame
    print(df.head())  # Inspect the DataFrame
    
    # Step 3: Check for missing values
    if df.isnull().values.any():
        print("Data contains missing values. Handling missing data...")
        df = df.dropna()  # or use imputation strategies
    
    # Step 4: Define features and target
    X = df[['total_volume', 'time_since_last_txn', 'high_trade', 'average_trade']]
    y = df['is_active']
    
    # Step 5: Check class distribution
    print(y.value_counts())
    
    # Step 6: Ensure both classes are present
    if len(y.unique()) < 2:
        print("Only one class present in y. Cannot perform classification.")
        return None
    
    # Step 7: Perform train-test split with stratification
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, shuffle=True, stratify=y
        )
    except ValueError as e:
        print(f"Error during train_test_split: {e}")
        # Handle the error, possibly by adjusting test_size or train_size
        return None
    
    # Step 8: Initialize and train the model
    model = LogisticRegression(max_iter=1000)  # Increased max_iter if needed
    try:
        model.fit(X_train, y_train)
    except Exception as e:
        print(f"Error during model training: {e}")
        return None
    
    # Step 9: Make predictions and evaluate
    try:
        predictions = model.predict(X_test)
        report = classification_report(y_test, predictions)
        print(report)
        return report
    except Exception as e:
        print(f"Error during prediction or evaluation: {e}")
        return None

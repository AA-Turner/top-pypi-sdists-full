import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel

# ----------------------------------------------------------------------------
# 1. Setup and Data Loading
# ----------------------------------------------------------------------------

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load dataset
data = pd.read_csv('ukraine_maize_2010.csv')

# Define key columns and parameters
target_column = 'Yield (tn per ha)'
# Rename target column to 'Yield' for convenience
data.rename(columns={target_column: 'Yield'}, inplace=True)
target_column = 'Yield'

year_column = 'Harvest Year'
region_column = 'Region'
common_columns = ["Country", "Region", "Crop", "Area", "Season", "Area (ha)", "Production (tn)"]

# Convert region to categorical and add region_ID
data[region_column] = data[region_column].astype("category")
data["region_ID"] = data[region_column].cat.codes

# Drop rows with NaN values
data = data.dropna()

# Define features (will refine after scikit-learn feature selection)
features = data.drop(columns=[target_column, 'Country', region_column, year_column] + common_columns)

# Sort the years for chronological splitting
years = sorted(data[year_column].unique())

# ----------------------------------------------------------------------------
# 2. Feature Selection with SelectFromModel
# ----------------------------------------------------------------------------

print("Running feature selection using RandomForest & SelectFromModel...")

rf_for_fs = RandomForestRegressor(
    n_estimators=500,
    n_jobs=-1,
    max_depth=5,
    random_state=42
)
X_all = features.values
y_all = data[target_column].values
rf_for_fs.fit(X_all, y_all)

selector = SelectFromModel(rf_for_fs, threshold="median", prefit=True)
mask = selector.get_support()
selected_feature_names = features.columns[mask].tolist()

# Ensure region_ID is included (if needed)
if "region_ID" not in selected_feature_names:
    selected_feature_names.append("region_ID")

selected_features = list(selected_feature_names)
print("Selected features:", selected_features)

# Save the selected features
pd.DataFrame(selected_features, columns=["Selected_Features"]).to_csv("output/selected_features.csv", index=False)

# ----------------------------------------------------------------------------
# 3. Random Forest Model Evaluation
# ----------------------------------------------------------------------------

def evaluate_model(train_data, test_data, return_predictions=False):
    """
    Trains a Random Forest model and evaluates on the test set.
    """
    X_train = train_data[selected_features]
    y_train = train_data[target_column]
    X_test = test_data[selected_features]
    y_test = test_data[target_column]

    model = RandomForestRegressor(
        n_estimators=500,
        n_jobs=-1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    if return_predictions:
        return rmse, r2, mae, y_test.tolist(), predictions.tolist()
    else:
        return rmse, r2, mae

# ----------------------------------------------------------------------------
# 4. Baseline Performance (Yearly Hold-Out, Sequential)
# ----------------------------------------------------------------------------

def evaluate_baseline(year):
    """
    Train on all data except `year`; test on `year`.
    Returns metrics plus observed & predicted for plotting.
    """
    train_data = data[data[year_column] != year]
    test_data = data[data[year_column] == year]
    rmse, r2, mae, observed, predicted = evaluate_model(train_data, test_data, return_predictions=True)
    return year, rmse, r2, mae, observed, predicted

def calculate_baseline_performance():
    """
    Runs a year-based hold-out for each year in `years`, sequentially.
    """
    observed_yields = []
    predicted_yields = []
    metrics_by_year = {}

    # Sequential loop over years
    baseline_results = []
    for yr in tqdm(years, desc="Baseline Performance"):
        baseline_results.append(evaluate_baseline(yr))

    # Aggregate results
    for year, rmse, r2, mae, observed, predicted in baseline_results:
        observed_yields.extend(observed)
        predicted_yields.extend(predicted)
        mape = np.mean(np.abs((np.array(observed) - np.array(predicted)) / np.array(observed))) * 100
        metrics_by_year[year] = {"RMSE": rmse, "R2": r2, "MAE": mae, "MAPE": mape}

    years_list = list(metrics_by_year.keys())
    return metrics_by_year, observed_yields, predicted_yields, years_list

# ----------------------------------------------------------------------------
# 5. Plotting Functions
# ----------------------------------------------------------------------------

def plot_observed_vs_predicted():
    """
    Scatter plot of all observed vs. predicted yields across years.
    Also prints overall R2, MAE, RMSE, and MAPE.
    """
    metrics_by_year, observed, predicted, _ = calculate_baseline_performance()
    # Calculate overall metrics
    r2 = r2_score(observed, predicted)
    mae = mean_absolute_error(observed, predicted)
    rmse = np.sqrt(mean_squared_error(observed, predicted))
    mape = np.mean(np.abs((np.array(observed) - np.array(predicted)) / np.array(observed))) * 100
    print(f"Overall -> R2: {r2:.3f}, MAE: {mae:.3f}, RMSE: {rmse:.3f}, MAPE: {mape:.2f}%")

    plt.figure(figsize=(8, 6))
    plt.scatter(observed, predicted, alpha=0.6)
    plt.plot([min(observed), max(observed)],
             [min(observed), max(observed)],
             color='red', linestyle='--')
    plt.xlabel("Observed Yield")
    plt.ylabel("Predicted Yield")

    # Annotate metrics
    metrics_text = (
        f"$R^2$: {r2:.2f}\n"
        f"MAE: {mae:.2f}\n"
        f"RMSE: {rmse:.2f}\n"
        f"MAPE: {mape:.2f}%"
    )
    plt.text(0.05, 0.95, metrics_text,
             transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle="round,pad=0.3",
                       edgecolor="black",
                       facecolor="lightgray"))

    plt.grid()
    plt.savefig("output/random_forest_observed_vs_predicted.png", dpi=300)
    plt.close()

    return metrics_by_year

def plot_metrics_by_year(metrics_by_year):
    """
    Line plots of RMSE, R2, MAE, and MAPE by year.
    """
    years_sorted = sorted(metrics_by_year.keys())
    rmse_values = [metrics_by_year[y]["RMSE"] for y in years_sorted]
    r2_values = [metrics_by_year[y]["R2"] for y in years_sorted]
    mae_values = [metrics_by_year[y]["MAE"] for y in years_sorted]
    mape_values = [metrics_by_year[y]["MAPE"] for y in years_sorted]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Error Metrics by Year (Random Forest)", fontsize=16)

    # RMSE
    axes[0, 0].plot(years_sorted, rmse_values, marker='o')
    axes[0, 0].set_title("RMSE by Year")
    axes[0, 0].set_xlabel("Year")
    axes[0, 0].set_ylabel("RMSE")
    axes[0, 0].grid()

    # R2
    axes[0, 1].plot(years_sorted, r2_values, marker='o')
    axes[0, 1].set_title("$R^2$ by Year")
    axes[0, 1].set_xlabel("Year")
    axes[0, 1].set_ylabel("$R^2$")
    axes[0, 1].grid()

    # MAE
    axes[1, 0].plot(years_sorted, mae_values, marker='o')
    axes[1, 0].set_title("MAE by Year")
    axes[1, 0].set_xlabel("Year")
    axes[1, 0].set_ylabel("MAE")
    axes[1, 0].grid()

    # MAPE
    axes[1, 1].plot(years_sorted, mape_values, marker='o')
    axes[1, 1].set_title("MAPE by Year")
    axes[1, 1].set_xlabel("Year")
    axes[1, 1].set_ylabel("MAPE (%)")
    axes[1, 1].grid()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("output/random_forest_metrics_by_year.png", dpi=300)
    plt.close()

# ----------------------------------------------------------------------------
# 6. Run the Baseline, Plot, and Save Results
# ----------------------------------------------------------------------------

# Generate baseline scatter plot & retrieve metrics-by-year
metrics_by_year = plot_observed_vs_predicted()
plot_metrics_by_year(metrics_by_year)

print("All done! Check the 'output' folder for figures and CSV files.")

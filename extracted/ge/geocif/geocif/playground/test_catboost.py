import pandas as pd
import numpy as np
import multiprocessing as mp
import os
np.int = np.int32
np.float = np.float64
np.bool = np.bool_
from catboost import CatBoostRegressor
from boruta import BorutaPy
from sklearn.metrics import mean_squared_error
from deap import base, creator, tools, algorithms
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from pygam import LinearGAM, s, l

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load dataset
data = pd.read_csv('ukraine_maize_2010.csv')

# Define key columns and parameters
target_column = 'Yield (tn per ha)'

# Rename target_column to Yield
data.rename(columns={target_column: 'Yield'}, inplace=True)
target_column = 'Yield'

year_column = 'Harvest Year'
region_column = 'Region'
common_columns = ["Country", "Region", "Crop", "Area", "Season", "Area (ha)", "Production (tn)"]

# Add a region_ID column that is a unique integer for each region and of categorical type
data[region_column] = data[region_column].astype("category")
data["region_ID"] = data[region_column].cat.codes

# Drop rows with NaN values
data = data.dropna()

features = data.drop(columns=[target_column, 'Country', region_column, year_column] + common_columns)
selected_features = features.columns.tolist()

# Temporal split years and regions
years = sorted(data[year_column].unique())
regions = data[region_column].unique()
total_regions = len(regions)


def evaluate_model(train_data, test_data, model_type='catboost', return_predictions=False):

    if model_type == 'catboost':
        X_train, y_train = train_data[selected_features], train_data[target_column]
        X_test, y_test = test_data[selected_features], test_data[target_column]

        # Define monotonic constraints: +1 for features with "NDVI" or "ESI", 0 for others
        monotone_constraints = [
            1 if "NDVI" in feature or "ESI" in feature else 0
            for feature in selected_features
        ]

        # Initialize CatBoostRegressor with monotonic constraints
        model = CatBoostRegressor(
            iterations=3500, depth=6, random_strength=0.5,
            reg_lambda=0.1, learning_rate=0.01, loss_function="RMSE",
            silent=True,
            random_seed=42,
            cat_features=["region_ID"],
        )

    elif model_type == 'gam':
        # Define base names for features to include in the GAM model
        required_features = ['AUC_NDVI', 'PRCPTOT', 'TG']
        selected_spline_features = []

        # Find closest matches for required features in selected_features
        for base_feature in required_features:
            # Find features that start with the required base name (e.g., "PRCPTOT" or "TG")
            matches = [feat for feat in features.columns if feat.startswith(base_feature)]

            if matches:
                # Use the first match found; alternatively, you could select based on specific criteria
                selected_spline_features.append(matches)
            else:
                raise ValueError(f"No match found in selected_features for required base feature: {base_feature}")

        # Prepare the train and test sets
        X_train, y_train = train_data[selected_spline_features], train_data[target_column]
        X_test, y_test = test_data[selected_spline_features], test_data[target_column]

        # Initialize the LinearGAM model with splines for each feature in selected_spline_features
        model = LinearGAM(
            sum([s(selected_features.index(feature)) for feature in selected_spline_features])
        )
    else:
        raise ValueError("Unsupported model type. Use 'catboost' or 'gam'.")

    # Fit the model
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Calculate evaluation metrics
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    # Optionally return observed and predicted values for plotting
    if return_predictions:
        return rmse, r2, mae, y_test.tolist(), predictions.tolist()
    else:
        return rmse, r2, mae


# Calculate number of CPUs to use (75% of total)
cpu_count = max(1, int(0.75 * os.cpu_count()))

# Function to evaluate baseline performance for a specific year
def evaluate_baseline(year, model_type='catboost'):
    # Split the data into train and test sets based on the specified year
    train_data = data[data[year_column] != year]
    test_data = data[data[year_column] == year]

    # Evaluate model performance for the specified model type
    if model_type == 'catboost':
        rmse, r2, mae, observed, predicted = evaluate_model(train_data, test_data, model_type='catboost', return_predictions=True)
    elif model_type == 'gam':
        rmse, r2, mae, observed, predicted = evaluate_model(train_data, test_data, model_type='gam', return_predictions=True)
    else:
        raise ValueError("Invalid model_type. Choose either 'catboost' or 'gam'.")

    # Return all metrics along with observed and predicted values for further processing
    return year, rmse, r2, mae, observed, predicted


# Parallelized Baseline Performance Calculation
# Update calculate_baseline_performance to filter for years 2001-2021 and calculate metrics
def calculate_baseline_performance(model_type='catboost'):
    observed_yields = []
    predicted_yields = []
    metrics_by_year = {}

    try:
        with mp.Pool(processes=max(1, int(0.75 * os.cpu_count()))) as pool:
            baseline_performance = list(
                tqdm(
                    pool.imap_unordered(lambda year: evaluate_baseline(year, model_type=model_type), years),
                    desc="Baseline Performance",
                    total=len(years),
                    leave=False
                )
            )
    except Exception as e:
        # If multiprocessing fails, run sequentially
        print(f"Multiprocessing failed with error: {e}. Running sequentially.")
        baseline_performance = [
            evaluate_baseline(year, model_type=model_type) for year in tqdm(years, desc="Baseline Performance")
        ]

    # Process results to save metrics and gather observed/predicted values
    for year, rmse, r2, mae, observed, predicted in baseline_performance:
        observed_yields.extend(observed)
        predicted_yields.extend(predicted)

        # Calculate MAPE for each year
        mape = np.mean(np.abs((np.array(observed) - np.array(predicted)) / np.array(observed))) * 100
        metrics_by_year[year] = {"RMSE": rmse, "R2": r2, "MAE": mae, "MAPE": mape}

    years_list = list(metrics_by_year.keys())

    return metrics_by_year, observed_yields, predicted_yields, years_list


from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
# Plot observed vs predicted scatter plot with error metrics from 2001-2021
def plot_observed_vs_predicted(model_type='catboost'):
    metrics_by_year, observed, predicted, years_list = calculate_baseline_performance(model_type=model_type)

    # Calculate overall metrics
    r2 = r2_score(observed, predicted)
    mae = mean_absolute_error(observed, predicted)
    rmse = np.sqrt(mean_squared_error(observed, predicted))
    mape = np.mean(np.abs((np.array(observed) - np.array(predicted)) / np.array(observed))) * 100
    print(r2, mae, rmse, mape)

    # Scatter plot with color mapping based on years
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(observed, predicted, cmap='viridis', alpha=0.6)
    plt.plot([min(observed), max(observed)], [min(observed), max(observed)], color='red', linestyle='--', label=None)
    plt.xlabel("Observed Yield (tn per ha)")
    plt.ylabel("Predicted Yield (tn per ha)")

    # Add colorbar with integer labels for years
    # cbar = plt.colorbar(scatter)
    # cbar.set_label('Year')
    #
    # # Set colorbar ticks to integer years
    # unique_years = sorted(list(set(years_list)))
    # cbar.set_ticks(unique_years)
    # cbar.set_ticklabels(unique_years)

    # Annotate overall metrics
    metrics_text = f"$R^2$: {r2:.2f}\nMAE: {mae:.2f}\nRMSE: {rmse:.2f}\nMAPE: {mape:.2f}%"
    plt.text(0.05, 0.95, metrics_text, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgray"))

    plt.grid()
    plt.savefig(f"output/{model_type}_observed_vs_predicted_yield_scatter.png", dpi=300)

    return metrics_by_year



# Plot MAPE, R2, RMSE, and MAE by year (2001-2021) using subplots
def plot_metrics_by_year(metrics_by_year, model_type='catboost'):
    years = sorted(metrics_by_year.keys())
    rmse_values = [metrics_by_year[year]["RMSE"] for year in years]
    r2_values = [metrics_by_year[year]["R2"] for year in years]
    mae_values = [metrics_by_year[year]["MAE"] for year in years]
    mape_values = [metrics_by_year[year]["MAPE"] for year in years]

    # Create subplots for each metric
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Error Metrics by Year - {model_type.upper()}", fontsize=16)

    # RMSE subplot
    axes[0, 0].plot(years, rmse_values, marker='o')
    axes[0, 0].set_title("RMSE by Year")
    axes[0, 0].set_xlabel("Year")
    axes[0, 0].set_ylabel("RMSE")
    axes[0, 0].grid()

    # R2 subplot
    axes[0, 1].plot(years, r2_values, marker='o')
    axes[0, 1].set_title("$R^2$ by Year")
    axes[0, 1].set_xlabel("Year")
    axes[0, 1].set_ylabel("$R^2$")
    axes[0, 1].grid()

    # MAE subplot
    axes[1, 0].plot(years, mae_values, marker='o')
    axes[1, 0].set_title("MAE by Year")
    axes[1, 0].set_xlabel("Year")
    axes[1, 0].set_ylabel("MAE")
    axes[1, 0].grid()

    # MAPE subplot
    axes[1, 1].plot(years, mape_values, marker='o')
    axes[1, 1].set_title("MAPE by Year")
    axes[1, 1].set_xlabel("Year")
    axes[1, 1].set_ylabel("MAPE (%)")
    axes[1, 1].grid()

    # Save and display
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"output/{model_type}_metrics_by_year.png", dpi=300)


# Evaluate performance with selected regions added from the test year
# Evaluate model performance with selected regions added from the test year
def evaluate_with_selected_regions(selected_regions, test_year):
    """
    Evaluates model performance with selected regions included in training data for a specific test year.

    Parameters:
        selected_regions (list): Regions to add to training data for the test year.
        test_year (int): The year for testing model performance.

    Returns:
        tuple: RMSE, R^2, and MAE of the model evaluated on the excluded test data.
    """
    test_data = data[data[year_column] == test_year]
    train_data_base = data[data[year_column] != test_year]

    for region in selected_regions:
        region_data = test_data[test_data[region_column] == region]
        train_data_base = pd.concat([train_data_base, region_data], ignore_index=True)

    test_data_excluded = test_data[~test_data[region_column].isin(selected_regions)]
    if test_data_excluded.empty:
        return None, None, None  # Ensure this returns three values

    # Evaluate model and return RMSE, R2, and MAE
    rmse, r2, mae = evaluate_model(train_data_base, test_data_excluded)
    return rmse, r2, mae


# Fitness Function for DEAP GA
# Updated Fitness Function to track improvements in R^2 and MAE
def fitness(individual, baseline_performance, max_regions):
    selected_regions = [regions[i] for i in range(len(regions)) if individual[i] == 1]

    # Penalize if the number of selected regions exceeds max_regions
    if len(selected_regions) > max_regions:
        return -np.inf, -np.inf, -np.inf

    # Return a very low score if no regions are selected
    if not selected_regions:
        return -np.inf, -np.inf, -np.inf

    # Sequentially calculate improvements for selected regions
    rmse_improvements = []
    r2_improvements = []
    mae_improvements = []

    for year in years:
        baseline_rmse, baseline_r2, baseline_mae, _ = baseline_performance[year]
        rmse, r2, mae = evaluate_with_selected_regions(selected_regions, year)

        if rmse is None or r2 is None or mae is None:
            return -np.inf, -np.inf, -np.inf

        rmse_improvements.append(baseline_rmse - rmse)
        r2_improvements.append(r2 - baseline_r2)
        mae_improvements.append(baseline_mae - mae)

    # Calculate average improvements
    avg_rmse_improvement = sum(rmse_improvements) / len(years)
    avg_r2_improvement = sum(r2_improvements) / len(years)
    avg_mae_improvement = sum(mae_improvements) / len(years)

    return avg_rmse_improvement, avg_r2_improvement, avg_mae_improvement


# Genetic Algorithm with DEAP, enforcing max regions selected
# Genetic Algorithm with DEAP, tracking RMSE, R^2, and MAE improvements
def genetic_algorithm(max_regions, generations=10, population_size=20, mutation_prob=0.1, crossover_prob=0.5):
    baseline_performance = calculate_baseline_performance()[0]

    # Create DEAP components
    if "FitnessMax" not in creator.__dict__:
        creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0, 1.0))
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, len(regions))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", fitness, baseline_performance=baseline_performance, max_regions=max_regions)
    toolbox.register("mate", tools.cxUniform, indpb=crossover_prob)
    toolbox.register("mutate", tools.mutFlipBit, indpb=mutation_prob)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Initialize population
    population = toolbox.population(n=population_size)
    rmse_history = []
    r2_history = []
    mae_history = []

    # Run the genetic algorithm with progress bar
    for gen in tqdm(range(generations), desc="GA Generations"):
        offspring = algorithms.varAnd(population, toolbox, cxpb=crossover_prob, mutpb=mutation_prob)
        fits = map(toolbox.evaluate, offspring)

        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=len(population))

        # Log the best fitness for each generation for each metric
        best_individual = tools.selBest(population, k=1)[0]
        rmse_history.append(best_individual.fitness.values[0])
        r2_history.append(best_individual.fitness.values[1])
        mae_history.append(best_individual.fitness.values[2])

    # Save genetic algorithm results to CSV
    ga_df = pd.DataFrame({
        "Generation": range(len(rmse_history)),
        "Best_RMSE_Improvement": rmse_history,
        "Best_R2_Improvement": r2_history,
        "Best_MAE_Improvement": mae_history
    })
    ga_df.to_csv(f"output/genetic_algorithm_n_{max_regions}.csv", index=False)

    return rmse_history, r2_history, mae_history


def plot_improvement_history(rmse_history, r2_history, mae_history, max_regions):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(rmse_history)), rmse_history, marker='o')
    plt.xlabel('Generation')
    plt.ylabel('Average RMSE Improvement')
    plt.title(f"RMSE Improvement History (n={max_regions})")
    plt.grid()
    plt.savefig(f"output/{max_regions}_rmse_improvement.png", dpi=300)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(r2_history)), r2_history, marker='o')
    plt.xlabel('Generation')
    plt.ylabel('Average R^2 Improvement')
    plt.title(f"R^2 Improvement History (n={max_regions})")
    plt.grid()
    plt.savefig(f"output/{max_regions}_r2_improvement.png", dpi=300)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(mae_history)), mae_history, marker='o')
    plt.xlabel('Generation')
    plt.ylabel('Average MAE Improvement')
    plt.title(f"MAE Improvement History (n={max_regions})")
    plt.grid()
    plt.savefig(f"output/{max_regions}_mae_improvement.png", dpi=300)


# Main function to find optimal regions with max selection constraint
def find_optimal_regions(n):

    if n == 1:
        baseline_performance = calculate_baseline_performance()[0]
        best_region, best_improvement = None, -np.inf

        for region in tqdm(regions, desc=f"Finding optimal region for n={n}", leave=False):
            total_improvement = 0
            valid = True

            for test_year in years:  # Use selected_years instead of years
                improvement = baseline_performance[test_year]["RMSE"] - \
                              evaluate_with_selected_regions([region], test_year)[0]
                if improvement is None:
                    valid = False
                    break
                total_improvement += improvement

            avg_improvement = total_improvement / len(years) if valid else -np.inf
            if valid and avg_improvement > best_improvement:
                best_region = region
                best_improvement = avg_improvement

        return [best_region], [best_improvement]
    else:
        optimal_regions, rmse_history, r2_history, mae_history = genetic_algorithm(n)
        plot_improvement_history(rmse_history, r2_history, mae_history, n)

        return optimal_regions, rmse_history[-1], r2_history[-1], mae_history[-1]

# Generate GAM plots
#metrics_by_year, _, _ = calculate_baseline_performance(model_type='gam')
#plot_observed_vs_predicted(model_type='gam')
#plot_metrics_by_year(metrics_by_year, model_type='gam')

# Feature Selection with BorutaPy using random forest as estimator
rf_for_boruta = RandomForestRegressor(n_estimators=500, n_jobs=8, max_depth=5, random_state=1)
boruta_selector = BorutaPy(rf_for_boruta, n_estimators='auto', random_state=42, verbose=True)
boruta_selector.fit(features.values, data[target_column].values)
selected_features = features.columns[boruta_selector.support_].tolist()
selected_features += ["region_ID"]
print("Selected features:", selected_features)

# Save selected features to CSV
pd.DataFrame(selected_features, columns=["Selected_Features"]).to_csv("output/selected_features.csv", index=False)

# Scatter plot for baseline model
metrics_by_year = plot_observed_vs_predicted()
plot_metrics_by_year(metrics_by_year)

# List of n values
n_values = [1, int(0.05 * total_regions), int(0.1 * total_regions), int(0.2 * total_regions),
            int(0.5 * total_regions), int(0.9 * total_regions), total_regions]
n_values = [n for n in n_values if n > 0]
n_values = sorted(list(set(n_values)))

# Dictionary to store results for each n value
results = {}

# Run optimization for each value of n and store results
n_values = [1, int(0.05 * total_regions), int(0.1 * total_regions), int(0.2 * total_regions), int(0.5 * total_regions), int(0.9 * total_regions), total_regions]
n_values = sorted(list(set(n for n in n_values if n > 0)))

for n in n_values:
    print(f"\nRunning optimization for n = {n} regions...")
    optimal_regions, final_rmse_improvement, final_r2_improvement, final_mae_improvement = find_optimal_regions(n)
    results[n] = {
        'Optimal_Regions': optimal_regions,
        'Final_RMSE_Improvement': final_rmse_improvement,
        'Final_R2_Improvement': final_r2_improvement,
        'Final_MAE_Improvement': final_mae_improvement
    }

# Save final results to CSV
results_df = pd.DataFrame({
    "n": list(results.keys()),
    "Optimal_Regions": [result['Optimal_Regions'] for result in results.values()],
    "Final_RMSE_Improvement": [result['Final_RMSE_Improvement'] for result in results.values()],
    "Final_R2_Improvement": [result['Final_R2_Improvement'] for result in results.values()],
    "Final_MAE_Improvement": [result['Final_MAE_Improvement'] for result in results.values()]
})
results_df.to_csv('output/region_optimization_results.csv', index=False)

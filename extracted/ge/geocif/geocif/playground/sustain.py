import numpy as np
from sustainbench import get_dataset
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt


# Step 1: Download and Load the Crop Yield Dataset using SustainBench
def load_data(country='usa'):
    print(f"Downloading dataset for {country}...")
    dataset = get_dataset(dataset='crop_yield', split_scheme=country, download=True)

    # Extract training, validation, and testing subsets
    train_data = dataset.get_subset('train')
    val_data = dataset.get_subset('val')
    test_data = dataset.get_subset('test')

    # Extract features and labels along with the year information
    X = np.array([x['x'] for x in train_data] + [x['x'] for x in val_data] + [x['x'] for x in test_data])
    y = np.array([x['y'] for x in train_data] + [x['y'] for x in val_data] + [x['y'] for x in test_data])
    years = np.array([x['year'] for x in train_data] + [x['year'] for x in val_data] + [x['year'] for x in test_data])

    return X, y, years


# Step 2: Rolling-Origin Temporal Validation
def hybrid_model_rolling_validation(X, y, years, min_train_year, max_year):
    results = []

    # Iterate through each test year after the initial training window
    for test_year in range(min_train_year + 1, max_year + 1):
        # Define training and testing indices
        train_indices = np.where((years >= min_train_year) & (years < test_year))[0]
        test_indices = np.where(years == test_year)[0]

        print(f"Training on years: {min_train_year} to {test_year - 1}")
        print(f"Testing on year: {test_year}")
        print(f"Shape of train set: {train_indices.shape}")
        print(f"Shape of test set: {test_indices.shape}")

        # Prepare the training and testing sets
        X_train = X[train_indices]
        y_train = y[train_indices]
        X_test = X[test_indices]
        y_test = y[test_indices]

        # Step 1: Train Random Forest Model
        rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        rf_model.fit(X_train, y_train)
        rf_pred_test = rf_model.predict(X_test)

        # Step 2: Use RF predictions as inputs for Gaussian Process
        rf_pred_train = rf_model.predict(X_train)
        X_train_gp = rf_pred_train.reshape(-1, 1)
        X_test_gp = rf_pred_test.reshape(-1, 1)

        # Define the Gaussian Process kernel
        kernel = C(1.0, (1e-3, 1e3)) * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e2))
        gp_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, random_state=42)

        # Train Gaussian Process Model
        gp_model.fit(X_train_gp, y_train)
        gp_pred_test, gp_std_test = gp_model.predict(X_test_gp, return_std=True)

        # Evaluate the model using MAPE
        mape_rf = mean_absolute_percentage_error(y_test, rf_pred_test) * 100
        mape_gp = mean_absolute_percentage_error(y_test, gp_pred_test) * 100

        print(f"MAPE for Random Forest: {mape_rf:.2f}%")
        print(f"MAPE for Hybrid Gaussian Process: {mape_gp:.2f}%")

        # Store the results
        results.append({
            'test_year': test_year,
            'mape_rf': mape_rf,
            'mape_gp': mape_gp
        })

    return results


# Main Function
if __name__ == "__main__":
    # Load the data for USA as an example
    X, y, years = load_data(country='usa')

    # Define the minimum training year and the maximum year for testing
    min_train_year = min(years)
    max_year = max(years)

    # Run the rolling-origin temporal validation
    results = hybrid_model_rolling_validation(X, y, years, min_train_year, max_year)

    # Plot the results
    test_years = [result['test_year'] for result in results]
    mape_rf = [result['mape_rf'] for result in results]
    mape_gp = [result['mape_gp'] for result in results]

    plt.figure(figsize=(12, 6))
    plt.plot(test_years, mape_rf, label="Random Forest MAPE", marker='o', color='blue')
    plt.plot(test_years, mape_gp, label="Hybrid GP MAPE", marker='o', color='red')
    plt.xlabel("Test Year")
    plt.ylabel("MAPE (%)")
    plt.title("Rolling-Origin Temporal Validation: Random Forest vs. Hybrid GP")
    plt.legend()
    plt.show()

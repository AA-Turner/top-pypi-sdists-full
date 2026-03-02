import cavapy
cavapy_results = cavapy.get_climate_data(country="Togo", variables=["pr"], num_processes=1, cordex_domain="AFR-22", rcp="rcp26", gcm="MPI", rcm="REMO", years_up_to=2030, obs=False, bias_correction=True, historical=False)

tasmax = cavapy_results["tasmax"]

# Make sure dims follow CF convention expected by xclim
if "latitude" in tasmax.dims:
    tasmax = tasmax.rename({"latitude": "lat", "longitude": "lon"})

# xclim health-checks look for a frequency hint
tasmax = tasmax.assign_attrs(freq="D")

# Compute annual TX90p relative to 1981-2010 baseline
tx90p_ys = tx90p(
    tasmax=tasmax,
    base_period=(1981, 2010),
    freq="YS"      # yearly sums
)


breakpoint()
import geopandas as gpd
from pathlib import Path


shp_path = Path(r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\wolayita_dissolved.shp")
gdf = gpd.read_file(shp_path)

# Add ADM1_NAME as title-case copy of W_NAME
gdf["ADM1_NAME"] = (
    gdf["W_NAME"]
      .str.title()          # make “Title Case”
      .str.replace(r"\s+", " ", regex=True)  # collapse double-spaces, just in case
      .str.strip()          # trim leading/trailing spaces
)

# Save out (overwrite shapefile or write a new one)
gdf.to_file(shp_path.with_stem(shp_path.stem), driver="ESRI Shapefile")

breakpoint()
from graphviz import Source

# Read your dot file
with open(r'D:\\Users\\ritvik\\projects\\geocif\\geocif\\playground\\aa.dot', 'r', encoding='utf-8') as f:
    src = f.read()

# Render and save
s = Source(src)
s.render(r'D:\Users\ritvik\projects\GEOGLAM\Code\Code\plots\aa', format='png', cleanup=True)



breakpoint()
import geopandas as gpd
import pandas as pd
from pathlib import Path


# 1.  Read data
dg   = gpd.read_file(r"/gpfs/data1/cmongp1/GEOGLAM/risk/Maize_1 (1).gpkg")
df1  = pd.read_csv(r"/gpfs/data1/cmongp1/GEOGLAM/risk/crRiskIndicator_Maize_1_Gauss5_2000-2020.csv",
                   dtype={'UID': str})

# 2.  Join & keep wanted columns
merged = (
    dg.merge(
        df1[['UID', 'Cntry_Code', 'varRatio']],
        on=['UID', 'Cntry_Code'],
        how='left'
    )
    .dropna(subset=['varRatio'])
)

# 3.  Shorten column names to <=10 characters

# 4.  Re-project to something Shapefile-friendly
merged = merged.to_crs(epsg=4326)

# 5.  Write the Shapefile (folder path only, driver inferred)
out_dir = Path(r"/gpfs/data1/cmongp1/GEOGLAM/risk/output")

# Drop rows in merged where 'risk', 'yvrRsk', 'clim_risk', 'climCh_risk' is NA
#merged = merged.dropna(subset=['risk', 'yvrRsk', 'clim_risk', 'climCh_risk'])
#merged['geometry'] = merged.geometry.simplify(0.01, preserve_topology=True)
merged.to_file(out_dir, driver='ESRI Shapefile', index=False)

breakpoint()
breakpoint()
import geopandas as gpd
import pandas as pd
from pathlib import Path


# 1.  Read data
dg   = gpd.read_file(r"/gpfs/data1/cmongp1/GEOGLAM/risk/Maize_1 (1).gpkg")
df1  = pd.read_csv(r"/gpfs/data1/cmongp1/GEOGLAM/risk/Maize_1_Gauss5_2000-2020_modDFall.csv",
                   dtype={'UID': str})

# 2.  Join & keep wanted columns
merged = (
    dg.merge(
        df1[['UID', 'Cntry_Code', 'yvrRsk', 'risk', 'clim_risk', 'climCh_risk']],
        on=['UID', 'Cntry_Code'],
        how='left'
    )
    .dropna(subset=['risk', 'yvrRsk', 'clim_risk', 'climCh_risk'])
)

# 3.  Shorten column names to <=10 characters

# 4.  Re-project to something Shapefile-friendly
merged = merged.to_crs(epsg=4326)

# 5.  Write the Shapefile (folder path only, driver inferred)
out_dir = Path(r"/gpfs/data1/cmongp1/GEOGLAM/risk/output_risk")

# Drop rows in merged where 'risk', 'yvrRsk', 'clim_risk', 'climCh_risk' is NA
merged = merged.dropna(subset=['risk', 'yvrRsk', 'clim_risk', 'climCh_risk'])
merged['geometry'] = merged.geometry.simplify(0.01, preserve_topology=True)
merged.to_file(out_dir, driver='ESRI Shapefile', index=False)

breakpoint()
import geopandas as gpd
import pandas as pd
from pathlib import Path


# 1.  Read data
dg   = gpd.read_file(r"/gpfs/data1/cmongp1/GEOGLAM/risk/Maize_1 (1).gpkg")
df1  = pd.read_csv(r"/gpfs/data1/cmongp1/GEOGLAM/risk/crRiskIndicator_Maize_1_Gauss5_2000-2020 (2).csv",
                   dtype={'UID': str})

# 2.  Join & keep wanted columns
merged = (
    dg.merge(
        df1[['UID', 'Cntry_Code', 'yvrRsk', 'risk', 'clim_risk', 'climCh_risk']],
        on=['UID', 'Cntry_Code'],
        how='left'
    )
    .dropna(subset=['risk', 'yvrRsk', 'clim_risk', 'climCh_risk'])
)

# 3.  Shorten column names to <=10 characters

# 4.  Re-project to something Shapefile-friendly
merged = merged.to_crs(epsg=4326)

# 5.  Write the Shapefile (folder path only, driver inferred)
out_dir = Path(r"/gpfs/data1/cmongp1/GEOGLAM/risk/output_risk")

# Drop rows in merged where 'risk', 'yvrRsk', 'clim_risk', 'climCh_risk' is NA
merged = merged.dropna(subset=['risk', 'yvrRsk', 'clim_risk', 'climCh_risk'])
merged['geometry'] = merged.geometry.simplify(0.01, preserve_topology=True)
merged.to_file(out_dir, driver='ESRI Shapefile', index=False)
breakpoint()

dg = gpd.read_file(r"C:\Users\ritvik\Downloads\Maize_1 (1).gpkg")
#df = pd.read_csv(r"C:\Users\ritvik\Downloads\Maize_1_Gauss5_2000-2020_modDFvar (1).csv", dtype={'UID': str})
df1 = pd.read_csv(r"C:\Users\ritvik\Downloads\crRiskIndicator_Maize_1_Gauss5_2000-2020 (2).csv", dtype={'UID': str})

# Assuming 'geometry' is the column containing the geometry in the GeoDataFrame dg
merged_df = dg.merge(df1[['UID', 'Cntry_Code', 'yvrRsk','risk','clim_risk','climCh_risk']], on=['UID', 'Cntry_Code'], how='left')
# Keep only the varRatio column and the geometry column from the merged GeoDataFrame
final_gdf = merged_df[['UID', 'Cntry_Code', 'yvrRsk','risk','clim_risk','climCh_risk', 'geometry']]

# drop rows where 'varRatio' is NaN
final_gdf = final_gdf.dropna(subset=['risk','yvrRsk', 'clim_risk','climCh_risk'])
# Save the final GeoDataFrame to a new GeoPackage
final_gdf.to_file(r"C:\Users\ritvik\Downloads\output_risk.shp")

# Output top 10 rows as a csv with geometry
#final_gdf.head(10).to_csv(r"C:\Users\ritvik\Downloads\output_top10.csv", index=False)

breakpoint()
#######################
DATA_DIR = Path(r"C:\Users\ritvik\Downloads\exported_all_db")

# Grab all maize CSV files (skip 'models.csv')
csv_paths = sorted(DATA_DIR.glob("*_maize.csv"))

dfs = []
for fp in csv_paths:
    df = pd.read_csv(fp)
    # Build the 'Country Region' column
    df["Country Region"] = (
        df["Country"].str.strip() + "_" + df["Region"].str.strip()
    ).str.replace(r"\s+", "_", regex=True).str.lower()
    dfs.append(df)

# Concatenate everything
df = pd.concat(dfs, ignore_index=True)

# --- 1. Read data ---
dg = gpd.read_file(r"D:\Users\ritvik\projects\GEOGLAM\safrica.shp")
# df = pd.read_csv(r"D:\Users\ritvik\projects\GEOGLAM\geocif_march_2025.csv")

# --- 2. Create the new "Country Region" column ---
dg['Country Region'] = (
    dg.apply(
        lambda row: (
            f"{row['ADMIN0']} {row['ADMIN2']}"
            if pd.notnull(row['ADMIN2'])
            else f"{row['ADMIN0']} {row['ADMIN1']}"
        ),
        axis=1
    )
    .str.lower()
    .str.replace(' ', '_')
)

# --- 3. Merge shapefile with CSV ---
merged = dg.merge(df, left_on='Country Region', right_on='Country Region', how='right')

# Compute '% Anomaly (2013-2017)' and '% Anomaly (2018-2022)' as (value - mean) / mean * 100
merged['% Anomaly (2013-2017)'] = (
    merged["Predicted Yield (tn per ha)"] - merged['Median Yield (tn per ha) (2013-2017)']
) / merged['Median Yield (tn per ha) (2013-2017)'] * 100
merged['% Anomaly (2018-2022)'] = (
    merged["Predicted Yield (tn per ha)"] - merged['Median Yield (tn per ha) (2018-2022)']
) / merged['Median Yield (tn per ha) (2018-2022)'] * 100


# --- 4. Rename columns ---
merged.rename(
    columns={
        '% Anomaly (2013-2017)': '2013_2017',
        '% Anomaly (2018-2022)': '2018_2022'
    },
    inplace=True
)

# Optional: Write out merged shapefile
merged.to_file(r"D:\Users\ritvik\projects\GEOGLAM\safrica_geocif_may_2025.shp")

# Output to CSV and exclude geometry
merged.drop(columns='geometry').to_csv(r"D:\Users\ritvik\projects\GEOGLAM\safrica_geocif_may_2025.csv", index=False)

breakpoint()
# --- 5. Plot ---
fig, ax = plt.subplots(1, 2, figsize=(20, 10))

# Reduce horizontal space between subplots
plt.subplots_adjust(wspace=0.05)

# Shared color normalization
norm = mpl.colors.Normalize(vmin=-40, vmax=40)

# Plot the anomaly maps (no country boundaries)
merged.plot(
    column='2013_2017',
    cmap='BrBG',
    norm=norm,
    ax=ax[0],
    legend=False
)
ax[0].set_title('Maize Yield Forecast % Anomaly (2013-2017)')
ax[0].axis('off')

merged.plot(
    column='2018_2022',
    cmap='BrBG',
    norm=norm,
    ax=ax[1],
    legend=False
)
ax[1].set_title('Maize Yield Forecast % Anomaly (2018-2022)')
ax[1].axis('off')

# Create a single horizontal colorbar
sm = mpl.cm.ScalarMappable(norm=norm, cmap='BrBG')
sm.set_array([])
cbar = fig.colorbar(
    sm,
    ax=ax.ravel().tolist(),
    orientation='horizontal',
    fraction=0.05,
    pad=0.05,
    extend='both'
)
cbar.set_label('% Anomaly')

plt.savefig(r"D:\Users\ritvik\projects\GEOGLAM\maize_yield_forecast_anomaly.png", dpi=300)



breakpoint()
from great_tables import GT, html
import pandas as pd

# Data from the user-provided table
data = {
    "province": ["Bagmati", "Koshi", "Madhesh", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"],
    "2023 prediction": [3.738, 3.708, 3.583, 3.726, 3.291, 3.124, 2.607],
    "Avg (2018-2022) - MOA": [3.858, 3.712, 3.668, 3.764, 3.771, 3.371, 3.399],
    "2024 prediction": [3.807, 3.666, 3.691, 3.757, 3.427, 2.827, 2.567],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a styled table
styled_table = (
    GT(df)
    .tab_header(
        title="Predictions and Historical Averages by Province",
        subtitle="Yield predictions for 2023, averages from 2018-2022, and predictions for 2024"
    )
    .cols_label(
        province="Province",
        **{
            "2023 prediction": html("2023<br>Prediction"),
            "Avg (2018-2022) - MOA": html("Avg<br>(2018-2022)<br>MOA"),
            "2024 prediction": html("2024<br>Prediction")
        }
    )
    .cols_width(
        province="2%",  # Narrow province column
        **{
            "2023 prediction": "4%",
            "Avg (2018-2022) - MOA": "5%",
            "2024 prediction": "4%"
        }
    )
)

# Save as a PDF
styled_table.save(
    file="predictions_table.pdf",
    scale=1.0,  # Keep the scale reasonable
    web_driver="chrome",  # Requires Chrome installed
    window_size=(1200, 800),  # Adjust window size to make the table compact
)

print("Table saved as predictions_table.pdf")

breakpoint()
import pandas as pd
import numpy as np
import os
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.linear_model import LinearRegression
from numpy.polynomial import Polynomial

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load dataset
data = pd.read_csv('ukraine_maize_2010.csv')

# Define key columns and parameters
target_column = 'Yield (tn per ha)'
data.rename(columns={target_column: 'Yield'}, inplace=True)
target_column = 'Yield'
year_column = 'Harvest Year'
region_column = 'Region'
common_columns = ["Country", "Region", "Crop", "Area", "Season", "Area (ha)", "Production (tn)"]

# Add a region_ID column as a unique integer identifier
data[region_column] = data[region_column].astype("category")
data["region_ID"] = data[region_column].cat.codes

# Drop rows with NaN values
data = data.dropna()

# Extract feature columns
features = data.drop(columns=[target_column, 'Country', region_column, year_column] + common_columns)
selected_features = features.columns.tolist()

# Helper function for detrending
def detrend_data(data, method='none', aggregation='none'):
    detrended_data = data.copy()

    if method == 'difference':
        # Year-over-year differencing
        if aggregation == 'none':
            detrended_data[target_column] = detrended_data[target_column].diff()
        else:
            detrended_data[target_column] = detrended_data.groupby(region_column if aggregation == 'oblast' else None)[target_column].diff()
        detrended_data.dropna(subset=[target_column], inplace=True)

    elif method == 'linear':
        regions = data[region_column].unique()
        detrended_yield = []

        for region in regions if aggregation != 'national' else [None]:
            region_data = data if region is None else data[data[region_column] == region]
            X = region_data[[year_column]].values
            y = region_data[target_column].values
            model = LinearRegression().fit(X, y)
            trend = model.predict(X)
            detrended_yield.extend(y - trend)

        detrended_data[target_column] = detrended_yield

    elif method == 'quad':
        regions = data[region_column].unique()
        detrended_yield = []

        for region in regions if aggregation != 'national' else [None]:
            region_data = data if region is None else data[data[region_column] == region]
            X = region_data[year_column].values
            y = region_data[target_column].values
            p = Polynomial.fit(X, y, deg=2)
            trend = p(X)
            detrended_yield.extend(y - trend)

        detrended_data[target_column] = detrended_yield

    elif method == 'none':
        return detrended_data

    else:
        raise ValueError("Invalid detrending method. Use 'difference', 'linear', 'quad', or 'none'.")

    return detrended_data

# Define CatBoost evaluation function
def evaluate_model(train_data, test_data):
    X_train, y_train = train_data[selected_features], train_data[target_column]
    X_test, y_test = test_data[selected_features], test_data[target_column]

    model = CatBoostRegressor(
        iterations=2500, depth=6, random_strength=0.5,
        reg_lambda=0.1, learning_rate=0.01, loss_function="RMSE",
        silent=True, random_seed=42, cat_features=["region_ID"]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    return rmse, r2, mae

# Evaluate all combinations of detrending methods and aggregation levels
def evaluate_all_combinations():
    methods = ['difference', 'linear', 'quad', 'none']
    aggregations = ['none', 'oblast', 'national']
    results = []

    for method in methods:
        for aggregation in aggregations:
            print(f"Evaluating combination: Detrending Method = {method}, Aggregation Level = {aggregation}")
            for year in tqdm(years, desc=f"Yearly Evaluation for {method}-{aggregation}"):
                detrended_data = detrend_data(data, method=method, aggregation=aggregation)

                # Split data into train and test sets
                train_data = detrended_data[detrended_data[year_column] != year]
                test_data = detrended_data[detrended_data[year_column] == year]

                # Evaluate the model
                rmse, r2, mae = evaluate_model(train_data, test_data)

                # Store the results
                results.append((method, aggregation, year, rmse, r2, mae))

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results, columns=["Method", "Aggregation", "Year", "RMSE", "R2", "MAE"])
    return results_df

# Main execution
years = sorted(data[year_column].unique())
results_df = evaluate_all_combinations()

# Save results to CSV
results_df.to_csv("output/detrending_evaluation_results_combinations.csv", index=False)

# Plot comparison of detrending methods and aggregation levels
def plot_comparison(results_df):
    metrics = ["RMSE", "R2", "MAE"]

    for metric in metrics:
        plt.figure(figsize=(12, 6))
        for method in ['difference', 'linear', 'quad', 'none']:
            for aggregation in ['none', 'oblast', 'national']:
                subset = results_df[(results_df["Method"] == method) & (results_df["Aggregation"] == aggregation)]
                plt.plot(subset["Year"], subset[metric], marker='o', label=f"{method}-{aggregation}")

        plt.xlabel("Year")
        plt.ylabel(metric)
        plt.title(f"Comparison of Detrending Methods and Aggregation Levels ({metric} by Year)")
        plt.legend()
        plt.grid()
        plt.savefig(f"output/detrending_comparison_{metric.lower()}.png", dpi=300)
        plt.show()

# Plot results
plot_comparison(results_df)

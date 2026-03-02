import geopandas as gpd
import pygmt
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import os
filtered_shapefile_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\filtered_shapefile5.shp"

if not os.path.isfile(filtered_shapefile_path):

    # Load the shapefile using GeoPandas
    shapefile_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\adm_shapefile.shp"
    gdf = gpd.read_file(shapefile_path, engine="pyogrio")

    # Only keep one row per ADMIN0
    gdf = gdf.drop_duplicates(subset="ADMIN0")

    sh2_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\Level_1.shp"
    gdf2 = gpd.read_file(sh2_path, engine="pyogrio")

    # Subset gdf2 to USA, Pakistan and Afghanistan
    gdf2 = gdf2[gdf2["ADM0_NAME"].isin(["United States of America"])]

    # Exclude Alska and Hawaii from the USA
    gdf2 = gdf2[~gdf2["ADM1_NAME"].isin(["Alaska", "Hawaii"])]

    # Now combine all the states into one polygon
    gdf2 = gdf2.dissolve(by="ADM0_NAME")
    gdf2 = gdf2.reset_index()

    # Rename ADM0_NAME to ADMIN0 for consistency
    gdf2.rename(columns={"ADM0_NAME": "ADMIN0"}, inplace=True)

    # Only keep ADMIN0 and geometry columns in gdf and gdf2
    gdf = gdf[["ADMIN0", "geometry"]]
    gdf2 = gdf2[["ADMIN0", "geometry"]]

    # Merge gdf and gdf2
    import pandas as pd
    gdf = pd.concat([gdf, gdf2], ignore_index=True)

    # Save the filtered shapefile as a temporary file

    gdf.to_file(filtered_shapefile_path)
else:
    gdf = gpd.read_file(filtered_shapefile_path, engine="pyogrio")

# Create the global map with highlighted countries
fig = pygmt.Figure()

# Define the region of interest and projection
# fig.basemap(region="g", projection="R12c/20", frame=True)
fig.basemap(region=[-135, 60, -35, 53], projection="Q12c", frame=True)

# Use the coast function to draw land and water
fig.coast(land="lightgray", water="lightcyan")

# Highlight the countries using the filtered shapefile
fig.plot(data=filtered_shapefile_path, pen="0.35p,black")

# Add hatches to Pakistan and Afghanistan
gdf_filled = gdf[gdf["ADMIN0"].isin(["Pakistan", "Afghanistan"])]
for _, row in gdf_filled.iterrows():
    fill_gdf = gpd.GeoDataFrame([row], columns=gdf.columns)
    with pygmt.helpers.GMTTempFile() as tmpfile:
        fill_gdf.to_file(tmpfile.name, driver="GeoJSON")
        fig.plot(data=tmpfile.name, pen="0.35p,black", fill="black@50+h")

# Save the figure
fig.savefig("global_choropleth_highlighted_v1.png", dpi=1000)

# Show the figure
fig.show()

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
def create_map_with_ticks():
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})

    # Add features to the map
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE)

    # Set the extent (min_lon, max_lon, min_lat, max_lat)
    ax.set_extent([-120, -70, 25, 50], crs=ccrs.PlateCarree())

    # Customize ticks to mimic GMT style
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    import matplotlib.ticker as mticker

    ax.set_xticks([-120, -110, -100, -90, -80, -70], crs=ccrs.PlateCarree())
    ax.set_yticks([25, 30, 35, 40, 45, 50], crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(number_format='g', degree_symbol='', dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='g', degree_symbol='')

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # Adding gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.xlocator = mticker.FixedLocator([-120, -110, -100, -90, -80, -70])
    gl.ylocator = mticker.FixedLocator([25, 30, 35, 40, 45, 50])

    # Display the map
    plt.show()


create_map_with_ticks()

breakpoint()
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap, Normalize
import matplotlib.pyplot as plt
import matplotlib as mpl

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.cm import ScalarMappable

fig, ax = plt.subplots(figsize=(3, 0.5))

colors = ["red", "cyan", "darkgreen"]
cmap = ListedColormap(colors)
norm = Normalize(vmin=2.5, vmax=5.5)
cb = fig.colorbar(
    mappable=ScalarMappable(norm=norm, cmap=cmap),
    cax=ax,
    ticks=[3.5, 4.5],
    ticklocation="top",
    orientation="horizontal",
    drawedges=True,
)
cb.solids.set(edgecolor="white", linewidth=5)
cb.outline.set_visible(False)
cb.dividers.set(linewidth=1, alpha=0.6)
cb.ax.tick_params(width=1, length=10, color="k")
plt.setp(cb.ax.xaxis.get_ticklines(), alpha=0.6)
cb.set_ticklabels([3.5, 4.5], alpha=0.6, color="k", fontsize=15, fontfamily="Arial")
plt.savefig(r"D:\Users\ritvik\projects\GEOGLAM\Output\fao\output\ml\db\aa.png")
breakpoint()
fig, ax = plt.subplots(figsize=(6, 1), layout="constrained")
cmap = ListedColormap(["red", "cyan", "slategrey"])
norm = mpl.colors.Normalize(vmin=5, vmax=10)
sm = ScalarMappable(norm=Normalize(2.5, 5.5), cmap=cmap)
fig.colorbar(sm, cmap=cmap, ticks=[3.5, 4.5], cax=ax, orientation="horizontal", label="Colorbar")
plt.show()
cb = plt.colorbar(
    sm, cmap=cmap, ticks=[3.5, 4.5], cax=ax, orientation="horizontal", label="Colorbar"
)

# Add number on top of the colorbar

breakpoint()
df = pd.read_csv(
    r"D:\Users\ritvik\projects\GEOGLAM\Output\fao\output\ml\analysis\April-16-2024\aa.csv"
)
# Initialize the Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(14, 10))

# Plot the predicted yield as a dot and the CI as a vertical line for each region
for i in range(len(df)):
    ax.plot([i, i], [df["Lower CI"][i], df["Upper CI"][i]], color="gray")  # CI line
    ax.plot(i, df["Predicted"][i], "ko")  # Predicted yield dot
    ax.plot(i, df["Median"][i], "ro")  # Median yield differently colored dot

# Add labels and title
ax.set_xticks(range(len(df)))
ax.set_xticklabels(df["Region"], rotation=90)
ax.set_ylabel("Yield (tn per ha)")
ax.set_title("Predicted and Median Yields with Confidence Intervals per Region")

# Show the plot with a tight layout
plt.tight_layout()
plt.show()
breakpoint()

from osgeo import ogr

driver = ogr.GetDriverByName("FileGDB")

ds = driver.Open(r"C:\Users\ritvik\Downloads\Admin_1_Regions.gdb", 0)

breakpoint()


import numpy as np

import geopandas as gpd

dg_ewcm_geoglam = gpd.read_file(
    r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\EWCM_Level_1.shp",
    engine="pyogrio",
)

dg_ewcm_fewsnet = gpd.read_file(
    r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\hvstat_shape (1).gpkg",
    engine="pyogrio",
)

# Only select thiose rows in dg_ewcm_fewsnet where ADMIN2 is not None
dg_ewcm_fewsnet = dg_ewcm_fewsnet[dg_ewcm_fewsnet["ADMIN2"].notnull()]

# Find countries in dg_ewcm_fewsnet
countries = dg_ewcm_fewsnet[dg_ewcm_fewsnet["ADMIN0"].notnull()]["ADMIN0"].unique()

# Restrict dg_ewcm_geoglam to countries in dg_ewcm_fewsnet
dg_ewcm_geoglam = dg_ewcm_geoglam[dg_ewcm_geoglam["ADM0_NAME"].isin(countries)]
# Find polygons that exist in dg_ewcm_geoglam but not in dg_ewcm_fewsnet
# print("GEOGLAM but not in FEWSNET", dg_ewcm_geoglam[~dg_ewcm_geoglam.geometry.isin(dg_ewcm_fewsnet.geometry)])
a1 = dg_ewcm_geoglam[~dg_ewcm_geoglam.geometry.isin(dg_ewcm_fewsnet.geometry)]
# Find polygons that exist in dg_ewcm_fewsnet but not in dg_ewcm_geoglam
# print("FEWSNET but not in GEOGLAM", dg_ewcm_fewsnet[~dg_ewcm_fewsnet.geometry.isin(dg_ewcm_geoglam.geometry)])
a2 = dg_ewcm_fewsnet[~dg_ewcm_fewsnet.geometry.isin(dg_ewcm_geoglam.geometry)]

# Remove geometry from a1 and a2
a1 = a1.drop(columns=["geometry"])
a2 = a2.drop(columns=["geometry"])

# Output to disk
a1.to_csv(r"D:\Users\ritvik\projects\GEOGLAM\in_geoglam_but_not_in_fewsnet.csv", index=False)
a2.to_csv(r"D:\Users\ritvik\projects\GEOGLAM\in_fewsnet_but_not_in_geoglam.csv", index=False)
breakpoint()


def compute_h_index(values):
    # Sort the citations array in descending order
    sorted_value = np.sort(values)[::-1]
    # Iterate through the sorted citations to find the h-index
    h_index = 0
    for i, value in enumerate(sorted_value, start=1):
        if value >= i:
            h_index = value
        else:
            break

    return h_index


# Example usage
citations = np.array([3.1, 0.56, 10.02, 2.35, 5.60])
h_index = compute_h_index(citations)
print(f"The h-index is: {h_index}")

breakpoint()
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import matplotlib.pyplot as plt

# Generate synthetic data
np.random.seed(0)
X = np.random.normal(size=(100, 4))
y = np.random.binomial(1, 0.5, size=100)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple RandomForest model
model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Plot with default font sizes
# Beeswarm plot
shap.summary_plot(shap_values[1], X_test, plot_type="dot")

# Waterfall plot for a single prediction
sample_idx = 0  # Example index for demonstration
shap.plots.waterfall(shap_values[1][sample_idx], max_display=10)

# Adjust font sizes globally for subsequent plots
plt.rcParams.update({"font.size": 8})  # Adjust the font size as needed

# Beeswarm plot with adjusted font size
shap.summary_plot(shap_values[1], X_test, plot_type="dot")

# Waterfall plot with adjusted font size for a single prediction
shap.plots.waterfall(shap_values[1][sample_idx], max_display=10)

# Reset matplotlib font settings to default if needed
plt.rcParams.update(plt.rcParamsDefault)

breakpoint()


def plot_dekads():
    # Correcting the generation of dekad start dates
    start_date = pd.Timestamp(year=2021, month=1, day=1)
    dekad_starts = []

    for month in range(1, 13):  # Loop through each month
        for day in [1, 11, 21]:
            dekad_date = pd.Timestamp(year=2021, month=month, day=day)
            dekad_starts.append(dekad_date)

    # Remove the extra dekad start if it goes beyond the year
    if dekad_starts[-1] > pd.Timestamp(year=2021, month=12, day=31):
        dekad_starts.pop()

    fig, ax = plt.subplots(figsize=(20, 3))

    color_nov_to_apr = "lightblue"  # Light blue for Nov 1 to Apr 30
    color_default = "lightgray"  # Light gray for the rest of the year

    for i, date in enumerate(dekad_starts):
        if date.month >= 11 or date.month <= 4:
            facecolor = color_nov_to_apr
        else:
            facecolor = color_default

        # Adding squares with specified face color and white border
        ax.add_patch(
            patches.Rectangle((i, 0.5), 1, 1, edgecolor="white", facecolor=facecolor, linewidth=2)
        )

        # Non-rotated annotations, slightly increased size
        annotation = f"D{i + 1}"
        ax.text(
            i + 0.5,
            0.35,
            annotation,
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xlim(0, len(dekad_starts))
    ax.set_ylim(0, 1.75)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("whitesmoke")
    # plt.title('Dekad Start Dates with White Borders', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_dekads_with_arrows():
    # Correctly generating dekad start dates
    start_date = pd.Timestamp(year=2021, month=1, day=1)
    dekad_starts = []

    for month in range(1, 13):  # Loop through each month
        for day in [1, 11, 21]:
            dekad_date = pd.Timestamp(year=2021, month=month, day=day)
            dekad_starts.append(dekad_date)

    # Adjust if the last date exceeds the year
    if dekad_starts[-1] > pd.Timestamp(year=2021, month=12, day=31):
        dekad_starts.pop()

    # Plotting with annotations, colored squares, and arrows
    fig, ax = plt.subplots(figsize=(20, 4))  # Increased figure height to accommodate arrows

    color_nov_to_apr = "lightblue"  # Light blue for Nov 1 to Apr 30
    color_default = "lightgray"  # Light gray for the rest of the year

    for i, date in enumerate(dekad_starts):
        facecolor = color_nov_to_apr if date.month >= 11 or date.month <= 4 else color_default
        # Draw the rectangles with specified face color and white border
        ax.add_patch(
            patches.Rectangle((i, 0.5), 1, 1, edgecolor="white", facecolor=facecolor, linewidth=2)
        )
        # Add annotation
        ax.text(
            i + 0.5,
            0.35,
            f"D{i + 1}",
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
        )

    # Drawing arrows from center to center, maintaining vertical positions
    # The vertical positions remain the same as before (-0.2, -0.6, -1.0) for visual consistency
    arrow_starts_ends = [
        (7.5, -0.2, 6.5, -0.2),
        (7.5, -0.6, 5.5, -0.6),
        (7.5, -1.0, 4.5, -1.0),
    ]

    for x_start, y_start, x_end, y_end in arrow_starts_ends:
        ax.annotate(
            "",
            xy=(x_end, y_end),
            xycoords="data",
            xytext=(x_start, y_start),
            textcoords="data",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        )

    ax.set_xlim(0, len(dekad_starts))
    ax.set_ylim(-1.25, 1.75)  # Adjusted to accommodate arrows
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("whitesmoke")
    # plt.title('Dekad Start Dates with Centered Arrows', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_dekads_v2():
    # Correctly generating dekad start dates
    start_date = pd.Timestamp(year=2021, month=1, day=1)
    dekad_starts = []

    for month in range(1, 13):  # Loop through each month
        for day in [1, 11, 21]:
            dekad_date = pd.Timestamp(year=2021, month=month, day=day)
            dekad_starts.append(dekad_date)

    # Adjust if the last date exceeds the year
    if dekad_starts[-1] > pd.Timestamp(year=2021, month=12, day=31):
        dekad_starts.pop()

    # Plotting with increased space for annotations
    fig, ax = plt.subplots(
        figsize=(20, 4)
    )  # Adjusted figure size for clarity and additional spacing

    color_nov_to_apr = "lightblue"  # Light blue for Nov 1 to Apr 30
    color_default = "lightgray"  # Light gray for the rest of the year

    for i, date in enumerate(dekad_starts):
        facecolor = color_nov_to_apr if date.month >= 11 or date.month <= 4 else color_default
        # Draw the rectangles with specified face color and white border
        ax.add_patch(
            patches.Rectangle((i, 0.5), 1, 1, edgecolor="white", facecolor=facecolor, linewidth=2)
        )
        # Add "D" annotation
        ax.text(
            i + 0.5,
            0.35,
            f"D{i + 1}",
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
        )
        # Further increase space and then add date annotation
        ax.text(
            i + 0.5,
            0.1,
            date.strftime("%b %d"),
            ha="center",
            va="top",
            fontsize=8,
            fontstyle="italic",
        )

    ax.set_xlim(0, len(dekad_starts))
    ax.set_ylim(-0.5, 1.75)  # Adjusted to better accommodate the increased spacing
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("whitesmoke")
    # plt.title('Dekad Start Dates with Increased Space for Annotations', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_dekads()
    plot_dekads_v2()
    plot_dekads_with_arrows()

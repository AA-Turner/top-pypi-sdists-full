import geopandas as gpd
import palettable as pal
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import glob
import os

# 1. Specify the directory containing your .dta files:
data_dir =  r"C:\Users\ritvik\Downloads\maize_yield\maize_yield"

# 2. Use glob to find all .dta files in that directory:
dta_files = glob.glob(os.path.join(data_dir, "*.dta"))

# 3. Read each .dta file into a pandas DataFrame and store in a list:
dataframes = [pd.read_stata(f) for f in dta_files]

# 4. Concatenate them all into one DataFrame (row-wise):
merged_df = pd.concat(dataframes, ignore_index=True)

# Replace null values in PROD98CQ with those in PROD columns
merged_df['PROD98CQ'] = merged_df['PROD98CQ'].fillna(merged_df['PROD'])
merged_df['YEAR'] = merged_df['YEAR'].fillna(merged_df['year'])

# Drop rows where AREAH is 0
merged_df = merged_df[merged_df['AREAH'] != 0]

merged_df['ZONE'] = merged_df['ZONE'].astype(int)
merged_df['DIST'] = merged_df['DIST'].astype(int)

# create a column called W_CODE which is set up as follows
# create a string by converting ZONE column to string and append 0
# to the left of the string to make it 2 characters long
# then do the same with DIST column
# finally concatenate the two strings
merged_df['W_CODE'] = merged_df['ZONE'].astype(str).str.zfill(2) + merged_df['DIST'].astype(str).str.zfill(2)

merged_df['W_CODE'] = '7' + merged_df['W_CODE']

# Remove the .0 at the end of the string in W_CODE
merged_df['W_CODE'] = merged_df['W_CODE'].str.replace('.0', '')
merged_df['W_CODE'] = merged_df['W_CODE'].astype(int)

dg = gpd.read_file(r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\wolayita_dissolved.shp")
dg = dg[['W_CODE', 'W_NAME']]

# Merge the two dataframes on W_CODE
merged_df = pd.merge(merged_df, dg, on='W_CODE', how='left')

# Remove rows where PROD98CQ or AREAH are null
merged_df = merged_df.dropna(subset=['PROD98CQ', 'AREAH'])

# Compte yield column
merged_df['yield'] = merged_df['PROD98CQ'] / merged_df['AREAH']
merged_df.to_csv(r'D:\Users\ritvik\projects\GEOGLAM\Output\crop_condition\March_27_2025\plots\EWCM\kabele.csv', index=False)
breakpoint()
# Add a histogram showing distribution of yields, use separate line and color for each 5-year period
# Create a new column 'Year Group' which groups years into 5-year periods
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Group years into 5-year periods
merged_df['Year Group'] = pd.cut(
    merged_df['YEAR'],
    bins=range(2005, 2026, 5),
    right=False
)

# 2. Create a FacetGrid with one facet per Year Group
g = sns.FacetGrid(
    merged_df,
    col="Year Group",
    col_wrap=2,
    height=4,
    sharex=True,
    sharey=True
)

# 3. Map an ECDF plot to each facet
#    'skyblue' is used for consistency with your original color choice
g.map(sns.ecdfplot, 'yield', color='skyblue')

# 4. Add vertical/horizontal lines, annotations, etc. in each facet
for ax, year_group in zip(g.axes.flatten(), g.col_names):
    # -- Subset data for this particular facet
    subset = merged_df[merged_df['Year Group'] == year_group]

    # -- Vertical line at yield=16
    ax.axvline(x=16, color='red', linestyle='--')

    # -- Annotate the line at yield=16
    ax.annotate(
        '16 QQ/ha',
        xy=(16, 0.8),  # x=16, y=0.8 in data coordinates (cumulative fraction)
        xytext=(5, 0),  # offset the text to the right by 5 points
        textcoords='offset points',
        rotation=90,
        color='red',
        ha='center',
        va='center',
        fontsize=9
    )

    # -- Horizontal lines for quintiles on the y-axis (20%, 40%, 60%, 80%)
    for q in [0.2, 0.4, 0.6, 0.8]:
        ax.axhline(y=q, color='green', linestyle='--')
        # (Optional) label each horizontal line:
        # ax.text(ax.get_xlim()[1]*0.9, q, f"{int(q*100)}%",
        #         va='center', ha='right', color='green', fontsize=9)

    # -- Number of observations in top-right corner
    n_obs = len(subset)
    ax.text(
        0.95, 0.95,
        f"N = {n_obs}",
        transform=ax.transAxes,
        ha='right',
        va='top',
        fontsize=9,
        color='black'
    )

# 5. Common title
plt.subplots_adjust(top=0.9)
g.fig.suptitle("Yield Distribution at Kabele Level (ECDF)", fontsize=16)

plt.show()

# Find the percentage of values below 16 QQ/ha and Year Group 2015-2020 or 2020-2025
#below_16 = merged_df[(merged_df['yield'] < 16) & (merged_df['YEAR'] >=2015) & (merged_df['YEAR'] < 2025)]
#breakpoint()
#below_16_pct = below_16.mean() * 100
#print(f"Percentage of yields below 16 QQ/ha at Kabele level: {below_16_pct:.2f}%")


# Create a heatmap showing the number of unique FA's per DIST and YEAR combination
# Group by DIST and YEAR, then count the number of unique FA's
df_fa_counts = merged_df.groupby(['DIST', 'YEAR'])['FA'].nunique().reset_index(name='FA_Count')

# Pivot the data so that rows = DIST, columns = YEAR, values = FA_Count
df_fa_pivot = df_fa_counts.pivot(index='DIST', columns='YEAR', values='FA_Count')

# Change year column to type int
df_fa_pivot.columns = df_fa_pivot.columns.astype(int)

# Create the heatmap

plt.figure(figsize=(12, 8))
sns.heatmap(
    df_fa_pivot,
    cmap='viridis',       # color map; try 'coolwarm' or others
    annot=True,           # show numeric values in each cell
    fmt="g",            # format numbers (2 decimal places)
    linewidths=.5         # line width between cells
)
plt.show()

# create a new dataframe which computes average yield by W_NAME for each year, do a weighted average using FWEIGHT column
df_avg_yield = merged_df.groupby(['W_NAME', 'YEAR']).apply(lambda x: np.average(x['yield'], weights=x['FWEIGHT'])).reset_index(name='yield')

# Add a histogram showing distribution of yields, use separate line and color for each 5-year period
# Create a new column 'Year Group' which groups years into 5-year periods
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Create custom bins and labels so that the last group is 2020-2021
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Define custom bins so that the last group is labeled 2020–2021
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Define custom bins so that the last group is labeled 2020–2021
df_avg_yield['Year Group'] = pd.cut(
    df_avg_yield['YEAR'],
    bins=[2005, 2010, 2015, 2020, 2022],  # stops at 2022 so the label reads "2020–2021"
    labels=['2005–2009', '2010–2014', '2015–2019', '2020–2021'],
    right=False
)

# 2. Create a FacetGrid by Year Group
g = sns.FacetGrid(
    df_avg_yield,
    col='Year Group',
    col_wrap=2,
    height=4,
    sharex=True,
    sharey=True
)

# 3. Map an ECDF plot (instead of histogram) in each facet
g.map_dataframe(sns.ecdfplot, x='yield')

# 4. Add lines and annotations to each facet
for i, ax in enumerate(g.axes.flatten()):
    # Subset the data for the current Year Group
    year_group = g.col_names[i]
    subset = df_avg_yield[df_avg_yield['Year Group'] == year_group]

    # -- Vertical line at yield=16
    ax.axvline(x=16, color='red', linestyle='--')
    # Annotate that line near the top of the plot
    ax.annotate(
        "16 QQ/ha",
        xy=(16, 0.8),  # (x=16, y=0.8 in data coords for the y-axis)
        xytext=(5, 0),
        textcoords='offset points',
        rotation=90,
        color='red',
        ha='center',
        va='center',
        fontsize=9
    )

    # -- Horizontal lines at 20%, 40%, 60%, 80% (quintiles in terms of fraction)
    for q in [0.2, 0.4, 0.6, 0.8]:
        ax.axhline(y=q, color='green', linestyle='--')

    # -- Number of observations in the top-right corner
    n_obs = len(subset)
    ax.text(
        0.95, 0.95,
        f"N = {n_obs}",
        transform=ax.transAxes,
        ha='right',
        va='top',
        fontsize=9,
        color='black'
    )

# 5. Overall title
plt.subplots_adjust(top=0.9)
g.fig.suptitle("Yield Distribution at Woreda Level (ECDF)", fontsize=16)

plt.show()

# Find the percentage of values below 16 QQ/ha
below_16 = df_avg_yield['yield'] < 16
below_16 = df_avg_yield[(df_avg_yield['yield'] < 16) & (df_avg_yield['YEAR'] >=2015) & (df_avg_yield['YEAR'] < 2025)]
breakpoint()
below_16_pct = below_16.mean() * 100
print(f"Percentage of yields below 16 QQ/ha: {below_16_pct:.2f}%")

breakpoint()
# Change W_NAME column to title case
df_avg_yield['W_NAME'] = df_avg_yield['W_NAME'].str.title()

# Change YEAR to int
df_avg_yield['YEAR'] = df_avg_yield['YEAR'].astype(int)

# Convert to a format where each YEAR is converted to int and becomes a column and yield is the value
df_avg_yield = df_avg_yield.pivot(index='W_NAME', columns='YEAR', values='yield')

# Remove YEAR as column name and W_NAME as index name
df_avg_yield.index.name = None
df_avg_yield.columns.name = None

df_avg_yield.to_csv('wolayita_yields_v8.csv')
breakpoint()
# Compare wolayita_yields_v2.csv with wolayita_yields.csv
# 1. Load the two CSV files
df_v1 = pd.read_csv('wolayita_yields.csv')
df_v2 = pd.read_csv('wolayita_yields_v2.csv')

# 2. Check if the two DataFrames are equal
print(df_v1.equals(df_v2))

breakpoint()
# 5. (Optional) Inspect the merged DataFrame
print(merged_df.head())
print(len(merged_df))
merged_df.to_csv('merged_df.csv', index=False)
breakpoint()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import geopandas as gpd
dg = gpd.read_file(r"D:\Users\ritvik\projects\GEOGLAM\wolayita.shp")
dg = dg[dg['Z_NAME'] == "Wolayita"]

# Dissolve on W_NAME column
dg = dg.dissolve(by="W_NAME")

# save to disk
dg.to_file(r"D:\Users\ritvik\projects\GEOGLAM\Input\countries\wolayita\wolayita_dissolved.shp")

breakpoint()
# 1. Load the dataset
df = pd.read_csv('merged_df.csv')

# 2. Ensure we have a 'yield' column.
#    If not present, we compute yield as Maize_Production / Maize_Area.
if 'yield' not in df.columns:
    if 'PROD98CQ' in df.columns and 'AREAH' in df.columns:
        # Compute yield in tonnes per hectare (or adjust unit if needed)
        df['yield'] = df['PROD98CQ'] / df['AREAH']
    else:
        raise ValueError("The required columns to compute yield are missing.")

# 3. Calculate percentage of missing data for yield
missing_pct_yield = df['yield'].isnull().mean() * 100
print(f"Percentage of missing data for yield: {missing_pct_yield:.2f}%")

# 4. Check if some years have more or less data
#    Count the number of records for each year
year_counts = df['YEAR'].value_counts().sort_index()
print("\nNumber of records per year:")
print(year_counts)

# 5. Plot histogram of yield distributions by year
import seaborn as sns

# Instead of looping and plotting histograms, we can use a boxplot
plt.figure(figsize=(12, 8))

sns.boxplot(x='YEAR', y='yield', data=df)

# Add labels and title
plt.xlabel("")
plt.ylabel("Yield")

plt.show()


# Group by YEAR and get size (number of rows)
df_year_counts = df.groupby('YEAR').size().reset_index(name='Count')
# Sort by YEAR if you want ascending year order
df_year_counts.sort_values(by='YEAR', inplace=True)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_year_counts, x='YEAR', y='Count', color='skyblue', edgecolor='black')

plt.xlabel("")
plt.ylabel("Number of Yield Records")
plt.xticks(rotation=45)  # Rotate x labels if needed
plt.tight_layout()       # Adjust layout to avoid clipping
plt.show()


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Group by FA and YEAR, then calculate the mean yield
fa_year_yield = df.groupby(['FA', 'YEAR'])['yield'].mean().reset_index()

# 2. Pivot so rows = FA, columns = YEAR, values = average yield
fa_year_pivot = fa_year_yield.pivot(index='FA', columns='YEAR', values='yield')

# 3. Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    fa_year_pivot,
    cmap='viridis',       # color map; try 'coolwarm' or others
    annot=False,           # show numeric values in each cell
    fmt=".2f",            # format numbers (2 decimal places)
    linewidths=.5         # line width between cells
)

plt.title("Heatmap of Average Yield by FA and YEAR")
plt.xlabel("YEAR")
plt.ylabel("FA")
plt.tight_layout()
plt.show()

breakpoint()


# --- Read and preprocess your main shapefile ---
dg = gpd.read_file(r"D:\Users\ritvik\projects\GEOGLAM\safrica.shp")

# remove rows where both ADMIN1 and ADMIN2 are null
dg = dg.dropna(subset=["ADMIN1", "ADMIN2"], how="all")

# if ADMIN2 is not null then replace ADMIN1 with ADMIN2 values
dg["ADMIN1"] = dg["ADMIN2"].combine_first(dg["ADMIN1"])

# --- Read your CSV and merge on ADMIN1 ---
df = pd.read_csv(r"C:\Users\ritvik\Downloads\geocif.csv")

dg = dg.merge(
    df[["ADMIN1", 'Predicted Yield (tn per ha)',
        'Median Yield (tn per ha) (2013-2017)', 'Predicted/Median']],
    on="ADMIN1",
    how="left"
)

# --- Create a dissolved national boundary GeoDataFrame ---
boundary_gdf = dg.dissolve(by="ADMIN0")

# --- Colormap and normalization setup ---
cmap = pal.colorbrewer.get_map("BrBG", "diverging", 11).mpl_colormap
norm = mcolors.TwoSlopeNorm(vmin=-40, vcenter=0, vmax=40)

# --- First map: Predicted/Median ---
fig, ax = plt.subplots(figsize=(10, 6))

# 1) Plot the main layer
dg.plot(
    column="Predicted/Median",
    cmap=cmap,
    norm=norm,
    legend=True,
    ax=ax,
    edgecolor='gray',
    linewidth=0.2,
    legend_kwds={
        "shrink": 0.5,
        "pad": 0.002,
        "orientation": "horizontal"
    }
)

url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

world = gpd.read_file(url)
world =  world[world['ADMIN'].isin(['South Africa', 'Angola', 'Malawi', 'Zambia'])]

# 2) Plot the dissolved national boundaries on top
world.plot(
    ax=ax,
    color="none",       # No fill
    edgecolor="black",  # Outline color
    linewidth=0.5
)

ax.set_title("Maize Yield Forecast % Anomaly")
plt.axis("off")
plt.tight_layout()
plt.savefig("aa.png", dpi=300)
plt.close()


# --- Second map: Median Yield (2013-2017) ---
# fig, ax = plt.subplots(figsize=(10, 6))
#
# # 1) Plot the main layer
# dg.plot(
#     column="Median Yield (tn per ha) (2013-2017)",
#     cmap=cmap,
#     legend=True,
#     ax=ax,
#     legend_kwds={
#         "shrink": 0.5,
#         "pad": 0.002,
#         "orientation": "horizontal"
#     }
# )
#
# # 2) Plot the dissolved national boundaries on top
# boundary_gdf.plot(
#     ax=ax,
#     color="none",
#     edgecolor="black",
#     linewidth=1
# )
#
# ax.set_title("Median Maize Yield (2013-2017)")
# plt.axis("off")
# plt.tight_layout()
# plt.show()
# plt.close()

breakpoint()

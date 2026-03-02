import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read the CSV
df = pd.read_csv(r"C:\Users\ritvik\Downloads\ET_AgStats.csv")

# 2. Filter for the crop "Maize (Corn)"
df = df[df['DNL_SourceCrop'] == 'Maize (Corn)']

# 3. Remove rows where "Area Planted: ha" is "NA" or "NC"
df = df[df['Area Planted: ha'] != 'NA']
df = df[df['Area Planted: ha'] != 'NC']

df = df[df['Yield: MT/ha'] != 'NA']
df = df[df['Yield: MT/ha'] != 'NC']
df = df[df['Yield: MT/ha'] != '#REF!']

# Remove rows where Admin 2 is null
df = df.dropna(subset=['Admin 2'])
df = df.dropna(subset=['Yield: MT/ha'])

# 4. Convert "Area Planted: ha" to float by removing commas
df['Area Planted: ha'] = (
    df['Area Planted: ha']
    .str.replace(',', '', regex=False)
    .astype(float)
)

df['Yield: MT/ha'] = (
    df['Yield: MT/ha']
    .str.replace(',', '', regex=False)
    .astype(float)
)

# 5. Group by [region, season] to calculate z-scores
grouped = df.groupby(['Admin 2', 'Season'])
anomalies_list = []

for (region, season), group_data in grouped:
    mean_area = group_data['Area Planted: ha'].mean()
    std_area = group_data['Area Planted: ha'].std()

    # Avoid division by zero
    if std_area == 0:
        group_data['Z_score'] = 0
    else:
        group_data['Z_score'] = (group_data['Area Planted: ha'] - mean_area) / std_area

    # Flag anomalies if abs(z-score) > 3
    group_data['Anomaly'] = group_data['Z_score'].apply(lambda x: 'Yes' if abs(x) > 3 else 'No')

    anomalies_list.append(group_data)

# 6. Concatenate grouped data back together
df_analyzed = pd.concat(anomalies_list)

# 7. Filter to see only anomalies
df_anomalies = df_analyzed[df_analyzed['Anomaly'] == 'Yes']

# 8. Print full dataset with anomaly flags and the subset of anomalies
print("All data with anomaly flags:")
print(df_analyzed)

print("\nDetected anomalies:")
print(df_anomalies)
df_anomalies.to_csv(r"df_anomalies_v2.csv", index=False)

# 11. Distribution of "Yield: MT/ha"

plt.figure(figsize=(8, 5))
sns.histplot(df['Yield: MT/ha'], kde=True, bins=30)
plt.title('Distribution of Yield (MT/ha)')
plt.xlabel('Yield (MT/ha)')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# count number of values where yield < 1
low_yield = df[df['Yield: MT/ha'] < 1].shape[0]
total = df.shape[0]
print(f"Number of records with yield < 1: {low_yield} / {total}")
breakpoint()
# 9. Bar chart of number of anomalies per Season
anomalies_by_season = df_anomalies['Season'].value_counts()
plt.figure(figsize=(8, 5))
anomalies_by_season.plot(kind='bar')
plt.title('Number of Anomalies per Season')
plt.xlabel('Season')
plt.ylabel('Count of Anomalies')
plt.tight_layout()
plt.show()

# 10. Heatmap of anomalies by Region (rows) and Year (columns)

# Ensure "Year" is numeric for pivoting
df_anomalies['Year'] = pd.to_numeric(df_anomalies['Year'], errors='coerce')

# Count how many anomalies per (region, year)
heatmap_data = df_anomalies.groupby(['Admin 1', 'Year']).size().unstack(fill_value=0)

# Plot the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    cmap='Blues',
    fmt='d'
)
plt.title('Number of Anomalies by Region and Year')
plt.xlabel('Year')
plt.ylabel('Region')
plt.tight_layout()
plt.show()



import ee
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

# Initialize EE
ee.Initialize(project='ee-rit')

# 1. Load your region polygons (ADM3 level)
regions = ee.FeatureCollection('projects/ee-rit/assets/wolayita')

# 2. Load your crop mask and HLS collections
crop_mask = ee.Image('projects/ee-rit/assets/shabari_maize').eq(1)
LAND_HLS   = "NASA/HLS/HLSL30/v002"
SENT_HLS   = "NASA/HLS/HLSS30/v002"
CLOUD_PROP = 'CLOUD_COVERAGE'
CLOUD_MAX  = 30
BANDS      = ['B3', 'B4', 'B5']  # green, red, nir

hls = (
    ee.ImageCollection(LAND_HLS).filter(ee.Filter.lt(CLOUD_PROP, CLOUD_MAX)).select(BANDS)
).merge(
    ee.ImageCollection(SENT_HLS).filter(ee.Filter.lt(CLOUD_PROP, CLOUD_MAX)).select(BANDS)
)

# 3. Function: for a given region feature, return a FC of (year, ADM3_EN, mean_NDVI)
years = ee.List.sequence(2013, datetime.datetime.now().year)
def stats_for_region(feat):
    def stats_for_year(y):
        y = ee.Number(y)
        # composite and NDVI
        img = hls.filterDate(ee.Date.fromYMD(y,4,1), ee.Date.fromYMD(y,8,31)).median()
        ndvi = img.normalizedDifference(['B5','B4']).rename('NDVI')
        # mask to cropland
        ndvi = ndvi.updateMask(crop_mask)
        # mean over this feature
        max_ndvi = ndvi.reduceRegion(
            ee.Reducer.max(),
            geometry=feat.geometry(),
            scale=30,
            maxPixels=1e13
        ).get('NDVI')
        return ee.Feature(None, {
            'ADM3_EN':    feat.get('ADM3_EN'),
            'year':       y,
            'max_NDVI':  max_ndvi
        })
    return ee.FeatureCollection(years.map(stats_for_year))

# 4. Build the full collection and fetch
fc = regions.map(stats_for_region).flatten()
data = fc.getInfo()['features']
df = pd.DataFrame([f['properties'] for f in data])
df['year']       = df['year'].astype(int)
df['max_NDVI']  = pd.to_numeric(df['max_NDVI'], errors='coerce')

# 5. Pivot to matrix: rows=ADM3_EN, cols=year
mat = df.pivot(index='ADM3_EN', columns='year', values='mean_NDVI')

# 6. Plot heatmap

plt.figure(figsize=(12, 10))

# Draw heatmap with annotations, two decimal places
sns.heatmap(
    mat,
    annot=True,
    fmt=".2f",
    cbar_kws={'label': 'Mean NDVI'},
    linewidths=0.5,      # optional: grid lines between cells
    linecolor='gray'     # optional: grid line color
)

plt.title('Apr–Aug Mean NDVI by ADM3_EN and Year')
plt.xlabel('')
plt.ylabel('Woreda')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

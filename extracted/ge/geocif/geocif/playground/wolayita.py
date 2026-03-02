import ee
import geemap
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# 1. Initialize Earth Engine
ee.Initialize(project="ee-rit")

# 2. Load your study region
region = ee.FeatureCollection('projects/ee-rit/assets/wolayita')

# 3. Load your cropland‐mask raster (1=crop, other values = non‐crop)
crop_mask = ee.Image('projects/ee-rit/assets/shabari_maize').rename('cropMask')

# 4. Define & merge the two HLS collections, selecting only B3,B4,B5 and filtering clouds
LAND_HLS   = "NASA/HLS/HLSL30/v002"
SENT_HLS   = "NASA/HLS/HLSS30/v002"
CLOUD_PROP = 'CLOUD_COVERAGE'
CLOUD_MAX  = 30
BANDS      = ['B3', 'B4', 'B5']  # green, red, nir

hls = (
    ee.ImageCollection(LAND_HLS)
      .filter(ee.Filter.lt(CLOUD_PROP, CLOUD_MAX))
      .select(BANDS)
).merge(
    ee.ImageCollection(SENT_HLS)
      .filter(ee.Filter.lt(CLOUD_PROP, CLOUD_MAX))
      .select(BANDS)
)

# 5. Compute annual median GCVI & NDVI over Apr–Aug, masking only pixels == 1
def annual_stats(year):
    year = ee.Number(year)
    start = ee.Date.fromYMD(year, 4, 1)
    end   = ee.Date.fromYMD(year, 8, 31)

    # 5.1 median composite
    img = hls.filterDate(start, end).median()

    # 5.2 compute indices
    gcvi = img.expression(
        '(nir/green) - 1',
        {'nir':   img.select('B5'),
         'green': img.select('B3')}
    ).rename('GCVI')
    ndvi = img.normalizedDifference(['B5', 'B4']).rename('NDVI')
    indices = gcvi.addBands(ndvi)

    # 5.3 build binary mask (pixel==1)
    mask_binary = crop_mask.eq(1)

    # 5.4 apply mask & reduce to median
    masked = indices.updateMask(mask_binary)
    stats = masked.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=region.geometry(),
        scale=30,
        maxPixels=1e13
    )

    return ee.Feature(None, {
        'year':        year,
        'median_GCVI': stats.get('GCVI'),
        'median_NDVI': stats.get('NDVI')
    })

# 6. Build the collection & pull into pandas
years = ee.List.sequence(2013, datetime.datetime.now().year)
fc    = ee.FeatureCollection(years.map(annual_stats))

data = fc.getInfo()['features']
df   = pd.DataFrame([f['properties'] for f in data])
df['year'] = df['year'].astype(int)

# 7. Coerce to numeric and drop years without data
df['median_GCVI'] = pd.to_numeric(df['median_GCVI'], errors='coerce')
df['median_NDVI'] = pd.to_numeric(df['median_NDVI'], errors='coerce')
df_valid = df.dropna(subset=['median_GCVI','median_NDVI']).sort_values('year')

# 8. Export to Drive
ee.batch.Export.table.toDrive(
    collection=fc,
    description='HLS_CropMask_Medians_AprAug',
    folder='EarthEngineOutputs',
    fileNamePrefix='hls_crop_medians_apr_aug',
    fileFormat='CSV'
).start()

# 9. Plot bar charts
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax1.bar(df_valid['year'], df_valid['median_GCVI'])
ax1.set_title('Median GCVI by Year (Apr–Aug)')
ax1.set_ylabel('GCVI')

ax2.bar(df_valid['year'], df_valid['median_NDVI'])
ax2.set_title('Median NDVI by Year (Apr–Aug)')
ax2.set_ylabel('NDVI')
ax2.set_xlabel('Year')

plt.tight_layout()
plt.show()

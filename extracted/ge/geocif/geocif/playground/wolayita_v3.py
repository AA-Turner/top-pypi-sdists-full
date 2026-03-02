import ee
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from tqdm import tqdm
import math

# -----------------------------------------------------------------------------
# SETTINGS: choose one
# -----------------------------------------------------------------------------
MODE = "sample"       # "sample" = raw pixel draws; "percentile" = server‐side max‐NDVI heatmap

YEARS  = list(range(2013, datetime.datetime.now().year + 1))
MONTHS = [4, 5, 6, 7, 8]  # Apr–Aug (used only in sample mode)
SAMPLES_PER_COMBO = 500   # for MODE="sample"
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# 1. Initialize & Constants
# -----------------------------------------------------------------------------
ee.Initialize(project='ee-rit')

REGIONS   = ee.FeatureCollection('projects/ee-rit/assets/wolayita')
CROP_MASK = ee.Image('projects/ee-rit/assets/shabari_maize').eq(1)
HLS = (
    ee.ImageCollection("NASA/HLS/HLSL30/v002")
      .filter(ee.Filter.lt('CLOUD_COVERAGE', 100))
      .select(['B3','B4','B5'])
).merge(
    ee.ImageCollection("NASA/HLS/HLSS30/v002")
      .filter(ee.Filter.lt('CLOUD_COVERAGE', 100))
      .select(['B3','B4','B5'])
)

# -----------------------------------------------------------------------------
# 2. Inline yield values (tn per ha) for ADM3_EN from 2004 to 2021
# -----------------------------------------------------------------------------
yield_dict = {
    'Bolossa Bonibe': {2008:12.10, 2009:15.45, 2010:10.12, 2011:15.68, 2012:10.94,
                       2013:24.82, 2014:20.33, 2015:12.20, 2017:11.47, 2021:12.53},
    'Bolossa Sore':   {2004:17.54, 2005:18.24, 2006:17.88, 2007:20.97, 2008:12.10,
                       2009:18.68, 2010:18.55, 2012:16.83, 2013:18.95, 2014:20.75,
                       2015:19.92, 2016:12.92, 2017:11.24, 2018:19.96, 2019:20.21,
                       2020:28.06, 2021:27.20},
    'Damot Gale':     {2004:13.81, 2005:15.88, 2006:15.57, 2007:24.63, 2008:10.07,
                       2009:17.67, 2010:14.72, 2011:6.03,  2012:23.06, 2013:23.52,
                       2014:25.07, 2015:22.12, 2016:27.19, 2017:20.45, 2018:19.96,
                       2019:20.20, 2020:28.06, 2021:29.77},
    'Damot Pulasa':   {2008:11.55, 2009:14.44, 2010:11.92, 2011:12.21, 2012:12.91,
                       2013:26.50, 2014:24.08, 2015:12.99, 2016:7.73,  2017:20.45,
                       2018:19.96, 2019:39.52, 2020:28.06, 2021:9.32},
    'Damot Sore':     {2008:8.51,  2009:12.36, 2010:12.23, 2011:21.52, 2012:18.03,
                       2013:16.06, 2014:17.79, 2015:26.63, 2016:17.36, 2017:20.45,
                       2018:8.49,  2019:21.28, 2021:14.99},
    'Damot Woyide':   {2004:18.89, 2005:12.35, 2006:12.11, 2007:14.42, 2008:16.56,
                       2009:19.32, 2010:8.98,  2012:22.04, 2013:23.37, 2014:21.44,
                       2015:23.79, 2016:22.25, 2017:19.60, 2018:19.87, 2019:15.12,
                       2020:28.06, 2021:14.06},
    'Deguna Fanigo':  {2008:10.60, 2009:16.29, 2010:21.87, 2011:18.46, 2012:17.38,
                       2013:27.01, 2014:16.38, 2015:17.25, 2016:22.06, 2017:27.30,
                       2018:28.83, 2019:14.99, 2020:34.81, 2021:30.95},
    'Humbo':          {2004:23.50, 2005:16.38, 2006:16.06, 2007:13.51, 2008:10.33,
                       2009:17.99, 2010:14.83, 2011:7.56,  2012:27.13, 2013:16.62,
                       2014:13.70, 2015:14.28, 2016:19.61, 2017:17.82, 2018:27.96,
                       2019:16.03, 2020:12.45, 2021:23.16},
    'Kindo Didaye':   {2008:11.13, 2009:18.47, 2010:10.92, 2011:12.21, 2012:27.17,
                       2015:20.22, 2016:16.98, 2018:17.68},
    'Kindo Koyisha':  {2004:14.51, 2005:13.04, 2006:12.78, 2007:23.89, 2008:12.10,
                       2009:12.77, 2010:19.19, 2012:15.28, 2013:19.41, 2014:20.47,
                       2015:20.61, 2016:13.79, 2017:20.26, 2018:22.40, 2019:22.49,
                       2020:22.96, 2021:24.39},
    'Ofa':            {2004:27.61, 2005:10.39, 2006:10.19, 2007:19.48, 2009:5.62,
                       2010:17.77, 2011:16.99, 2012:19.59, 2013:17.59, 2014:9.26,
                       2015:25.25, 2016:23.82, 2017:14.18, 2018:19.96, 2019:20.32,
                       2021:20.47},
    'Sodo Zuriya':    {2004:6.39,  2005:7.75,  2006:7.59,  2007:11.11, 2008:18.66,
                       2009:17.86, 2010:14.61, 2011:20.24, 2012:15.88, 2013:22.42,
                       2014:22.62, 2015:33.23, 2016:21.68, 2017:20.63, 2018:11.16,
                       2019:19.82, 2020:16.35, 2021:19.69}
}
df_yield = (
    pd.DataFrame.from_dict(yield_dict, orient='index')
      .reset_index().rename(columns={'index':'ADM3_EN'})
      .melt(id_vars='ADM3_EN', var_name='year', value_name='yield')
      .dropna(subset=['yield'])
)
df_yield['year'] = df_yield['year'].astype(int)

# -----------------------------------------------------------------------------
# 2A. MODE="sample": raw‐pixel sampling
# -----------------------------------------------------------------------------
def fetch_ndvi_samples(regions_fc, hls_ic, crop_mask, years, months, n_samples):
    rows = []
    feats = regions_fc.getInfo().get('features', [])
    for feat in feats:
        name = feat['properties'].get('ADM3_EN')
        geom = ee.Feature(feat).geometry()
        for y in tqdm(years, desc="years", leave=False):
            for m in tqdm(months, desc="months", leave=False):
                coll = hls_ic.filterDate(
                    ee.Date.fromYMD(y, m, 1),
                    ee.Date.fromYMD(y, m, 1).advance(1, 'month')
                )
                if coll.size().getInfo() == 0:
                    continue
                ndvi = (
                    coll.median()
                        .normalizedDifference(['B5', 'B4'])
                        .rename('NDVI')
                        .updateMask(crop_mask)
                )
                samples = ndvi.sample(
                    region=geom,
                    scale=30,
                    numPixels=n_samples,
                    seed=42
                ).getInfo().get('features', [])
                for s in samples:
                    rows.append({
                        'ADM3_EN': name,
                        'year':    y,
                        'month':   m,
                        'ndvi':    s['properties'].get('NDVI')
                    })
    return pd.DataFrame(rows, columns=['ADM3_EN', 'year', 'month', 'ndvi'])

# -----------------------------------------------------------------------------
# 2B. MODE="percentile": server‐side max‐NDVI heatmap
# -----------------------------------------------------------------------------
def fetch_ndvi_max(regions_fc, hls_ic, crop_mask, years):
    rows = []
    for y in tqdm(years, desc="years"):
        img = hls_ic.filterDate(f'{y}-04-01', f'{y}-08-31').median()
        ndvi = (
            img.normalizedDifference(['B5', 'B4'])
               .rename('NDVI')
               .updateMask(crop_mask)
        )
        stats_fc = ndvi.reduceRegions(
            collection=regions_fc,
            reducer=ee.Reducer.max().setOutputs(['max_NDVI']),
            scale=30,
            tileScale=8
        ).map(lambda f: f.set('year', y))
        for feat in stats_fc.getInfo().get('features', []):
            props = feat['properties']
            val = props.get('max_NDVI')
            max_ndvi = np.nan if val is None else float(val)
            rows.append({
                'ADM3_EN':  props.get('ADM3_EN'),
                'year':     int(props.get('year')),
                'max_NDVI': max_ndvi
            })
    return pd.DataFrame(rows, columns=['ADM3_EN', 'year', 'max_NDVI'])

# -----------------------------------------------------------------------------
# 3. Run selected mode and plot
# -----------------------------------------------------------------------------
if MODE == "sample":
    df = fetch_ndvi_samples(REGIONS, HLS, CROP_MASK, YEARS, MONTHS, SAMPLES_PER_COMBO)
    if df.empty:
        raise ValueError("No samples -- check your mask/region.")
    sns.catplot(
        x='month', y='ndvi', col='year',
        data=df.dropna(subset=['ndvi']), kind='box',
        col_wrap=4, sharey=True,
        height=3.5, aspect=1
    ).fig.suptitle("Monthly NDVI Distributions by Year and Woreda", y=1.02)
    plt.show()

elif MODE == "percentile":
    # 3.1 Fetch max‐NDVI
    dfm = fetch_ndvi_max(REGIONS, HLS, CROP_MASK, YEARS)
    if dfm.empty:
        raise ValueError("No max‐NDVI values -- check your mask/region.")

    # 3.2 Heatmap: Max NDVI
    mat_ndvi = dfm.pivot(index='ADM3_EN', columns='year', values='max_NDVI')
    plt.figure(figsize=(12,10))
    sns.heatmap(mat_ndvi, annot=True, fmt=".2f", linewidths=0.5,
                linecolor='gray', cbar_kws={'label':'Max NDVI'})
    plt.title('Apr–Aug Max NDVI by Woreda and Year')
    plt.xlabel('Year'); plt.ylabel('Woreda'); plt.xticks(rotation=45)
    plt.tight_layout(); plt.show()

    # 3.3 Heatmap: Yield
    mat_yield = df_yield.pivot(index='ADM3_EN', columns='year', values='yield')
    plt.figure(figsize=(12,10))
    sns.heatmap(mat_yield, annot=True, fmt=".2f", linewidths=0.5,
                linecolor='gray', cbar_kws={'label':'Yield (tn/ha)'})
    plt.title('Crop Yield by Woreda and Year')
    plt.xlabel('Year'); plt.ylabel('Woreda'); plt.xticks(rotation=45)
    plt.tight_layout(); plt.show()

    # 3.4 Scatter: one subplot per region (max 5 per row)
    df_merge = pd.merge(df_yield, dfm, on=['ADM3_EN','year'], how='outer')
    regions = sorted(df_merge['ADM3_EN'].unique())
    n_regions = len(regions)
    ncols = 5
    nrows = math.ceil(n_regions / ncols)
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(5*ncols, 4*nrows),
                             sharex=True, sharey=True)
    axes = axes.flatten()
    for ax, region in zip(axes, regions):
        sub = df_merge[df_merge['ADM3_EN'] == region]
        sns.scatterplot(data=sub, x='yield', y='max_NDVI', ax=ax)
        ax.set_title(region)
        ax.set_xlabel('Yield (tn/ha)')
        ax.set_ylabel('Max NDVI')
    for ax in axes[len(regions):]:
        ax.set_visible(False)
    plt.tight_layout()
    plt.show()

else:
    raise ValueError(f"Unknown MODE={MODE!r}")

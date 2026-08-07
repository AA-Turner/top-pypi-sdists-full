PHENOLOGICAL_STAGES = [1, 2, 3]
dict_indices = {
    "GD4": ["Cold", "Growing degree days (sum of Tmean > 4 C)"],
    "CFD": ["Cold", "Maximum number of consecutive frost days (Tmin < 0 C)"],
    "FD": ["Cold", "Number of Frost Days (Tmin < 0C)"],
    "HD17": ["Cold", "Heating degree days (sum of Tmean < 17 C)"],
    "ID": ["Cold", "Number of sharp Ice Days (Tmax < 0C)"],
    "CSDI": ["Cold", "Cold-spell duration index"],
    "TG10p": ["Cold", "Percentage of days when Tmean < 10th percentile"],
    "TN10p": ["Cold", "Percentage of days when Tmin < 10th percentile"],
    "TXn": ["Cold", "Minimum daily maximum temperature"],
    "TNn": ["Cold", "Minimum daily minimum temperature"],
    "CDD": ["Drought", "Maximum consecutive dry days (Precip < 1mm)"],
    # Total (not necessarily consecutive) dry-day count — the direct complement
    # of RR1 (wet days >= 1mm). Computed directly with numpy (_cid_dry_days in
    # indices.py); not an ECAD/ETCCDI catalog index.
    "DD": ["Drought", "Number of dry days (Precip < 1mm)"],
    # SPI3/SPI6 temporarily disabled while we test detrended-target training
    # independently. Re-enable + rebuild once we know whether trend-anchoring
    # was the primary failure mode for 2016 DF (over-forecast) — if yes, SPI
    # is likely redundant; if no, come back with cached-icclim rebuild.
    # "SPI3": ["Drought", "Standardized Precipitation Index (3 month scale)"],
    # "SPI6": ["Drought", "Standardized Precipitation Index (6 month scale)"],
    "SU": ["Heat", "Number of Summer Days (Tmax > 25C)"],
    "TR": ["Heat", "Number of Tropical Nights (Tmin > 20C)"],
    "WSDI": ["Heat", "Warm-spell duration index"],
    "TG90p": ["Heat", "Percentage of days when Tmean > 90th percentile"],
    "TN90p": ["Heat", "Percentage of days when Tmin > 90th percentile"],
    "TX90p": ["Heat", "Percentage of days when Tmax > 90th percentile"],
    "TXx": ["Heat", "Maximum daily maximum temperature"],
    "TNx": ["Heat", "Maximum daily minimum temperature"],
    "CSU": ["Heat", "Maximum number of consecutive summer days (Tmax >25 C)"],
    # Killing degree days — accumulated heat stress: sum of daily Tmax excess
    # above 32 C (sum of max(0, Tmax - 32)). The heat-side complement to GD4
    # (growing DD, Tmean>4) and HD17 (heating DD, Tmean<17). Not an ECAD index;
    # computed directly with numpy (_cid_killing_degree_days in indices.py).
    "KDD": ["Heat", "Killing degree days (sum of Tmax - 32C for Tmax > 32C)"],
    "PRCPTOT": ["Rain", "Total precipitation during Wet Days"],
    "RR1": ["Rain", "Number of Wet Days (precip >= 1 mm)"],
    "SDII": ["Rain", "Average precipitation during Wet Days (SDII)"],
    "CWD": ["Rain", "Maximum consecutive wet days (Precip >= 1mm)"],
    "R10mm": ["Rain", "Number of heavy precipitation days (Precip >=10mm)"],
    "R20mm": ["Rain", "Number of very heavy precipitation days (Precip >= 20mm)"],
    "RX1day": ["Rain", "Maximum 1-day precipitation"],
    "RX5day": ["Rain", "Maximum 5-day precipitation"],
    "R75p": ["Rain", "Days with RR > 75th percentile of daily amounts (wet days)"],
    "R75pTOT": [
        "Rain",
        "Precipitation fraction due to very wet days (> 75th percentile)",
    ],
    "R95p": ["Rain", "Days with RR > 95th percentile of daily amounts (very wet days)"],
    "R95pTOT": [
        "Rain",
        "Precipitation fraction due to very wet days (> 95th percentile)",
    ],
    "R99p": [
        "Rain",
        "Days with RR > 99th percentile of daily amounts (extremely wet days)",
    ],
    "R99pTOT": [
        "Rain",
        "Precipitation fraction due to very wet days (> 99th percentile)",
    ],
    "TG": ["Temperature", "Mean of daily mean temperature"],
    "TN": ["Temperature", "Mean of daily minimum temperature"],
    "TX": ["Temperature", "Mean of daily maximum temperature"],
    "DTR": ["Temperature", "Mean Diurnal Temperature Range"],
    "ETR": ["Temperature", "Intra-period extreme temperature range"],
    "vDTR": ["Temperature", "Mean day-to-day variation in Diurnal Temperature Range"],
    "CD": [
        "Compound",
        "Days with TG < 25th percentile of daily mean temperature and RR <25th percentile of daily precipitation sum",
    ],
    "CW": [
        "Compound",
        "Days with TG < 25th percentile of daily mean temperature and RR >75th percentile of daily precipitation sum",
    ],
    "WD": [
        "Compound",
        "Days with TG > 75th percentile of daily mean temperature and RR <25th percentile of daily precipitation sum",
    ],
    "WW": [
        "Compound",
        "Days with TG > 75th percentile of daily mean temperature and RR >75th percentile of daily precipitation sum",
    ],
    "SD": ["Snow", "Mean of daily snow depth"],
    "SD1": ["Snow", "Number of days with snow depth >= 1 cm"],
    "SD5cm": ["Snow", "Number of days with snow depth >= 5 cm"],
    "SD50cm": ["Snow", "Number of days with snow depth >= 50 cm"],
}

dict_ndvi = {
    "MEAN_NDVI": ["VI", "Mean NDVI"],
    "MAX_NDVI": ["VI", "Maximum NDVI"],
    "MIN_NDVI": ["VI", "Minimum NDVI"],
    "STD_NDVI": ["VI", "Standard deviation of NDVI"],
    "AUC_NDVI": ["VI", "Area under the curve of NDVI"],
}

dict_etref = {
    "MEAN_ETREF": ["ETREF", "Mean reference ET"],
    "MAX_ETREF":  ["ETREF", "Maximum reference ET"],
    "MIN_ETREF":  ["ETREF", "Minimum reference ET"],
    "STD_ETREF":  ["ETREF", "Standard deviation of reference ET"],
    "AUC_ETREF":  ["ETREF", "Area under the curve of reference ET"],
    "SUM_ETREF":  ["ETREF", "Total reference ET over period"],
}

dict_gcvi = {
    "MEAN_GCVI": ["VI", "Mean GCVI"],
    "MAX_GCVI": ["VI", "Maximum GCVI"],
    "MIN_GCVI": ["VI", "Minimum GCVI"],
    "STD_GCVI": ["VI", "Standard deviation of GCVI"],
    "AUC_GCVI": ["VI", "Area under the curve of GCVI"],
}

dict_esi4wk = {
    "MEAN_ESI4WK": ["ESI", "Mean ESI 4WK"],
    "MAX_ESI4WK": ["ESI", "Maximum ESI 4WK"],
    "MIN_ESI4WK": ["ESI", "Minimum ESI 4WK"],
    "STD_ESI4WK": ["ESI", "Standard deviation of ESI 4WK"],
    "AUC_ESI4WK": ["ESI", "Area under the curve of ESI 4WK"],
    # Drought depth/duration/spread encodings of ESI 4WK. MIN alone captures
    # only the single worst instant; these encode how LOW and how LONG ESI
    # stays depressed, which screens far stronger for poppy yield (leakage-safe
    # LOOCV: MIN+AUCDEF ~0.42 vs MIN ~0.22). Percentiles (P05..P30) are robust
    # drought-depth; AUCDEF<t>/FRACLO<t> are fixed-threshold deficit/duration
    # (pure per-window functions -> leakage-free, unlike region-climatology
    # thresholds); high percentiles + CV/IQR/RANGE are low-r "might still help
    # nonlinearly" candidates. Thresholds (30/40/50) sit around the ESI
    # distribution (~p10/p25/median for the poppy AOI). All computed by the
    # generic aggregators in indices.aggregate_eo_values.
    #"P05_ESI4WK":  ["ESI", "5th percentile of ESI 4WK"],
    #"P10_ESI4WK":  ["ESI", "10th percentile of ESI 4WK"],
    #"P20_ESI4WK":  ["ESI", "20th percentile of ESI 4WK"],
    #"P30_ESI4WK":  ["ESI", "30th percentile of ESI 4WK"],
    #"P70_ESI4WK":  ["ESI", "70th percentile of ESI 4WK"],
    #"P90_ESI4WK":  ["ESI", "90th percentile of ESI 4WK"],
    #"AUCDEF40_ESI4WK": ["ESI", "Mean deficit of ESI 4WK below 40 (integrated drought)"],
    #"AUCDEF50_ESI4WK": ["ESI", "Mean deficit of ESI 4WK below 50 (integrated drought)"],
    #"FRACLO30_ESI4WK": ["ESI", "Fraction of window with ESI 4WK below 30"],
    #"FRACLO40_ESI4WK": ["ESI", "Fraction of window with ESI 4WK below 40"],
    #"CV_ESI4WK":    ["ESI", "Coefficient of variation of ESI 4WK"],
    #"IQR_ESI4WK":   ["ESI", "Interquartile range of ESI 4WK"],
    #"RANGE_ESI4WK": ["ESI", "Range (max-min) of ESI 4WK"],
}

dict_hindex = {
    # Trimmed 2026-07-09 to keep only H-INDEX_Precip. The Tmax/Tmin/Tmean
    # variants collapse to TXx/TNx/TG (identical values in Brazil DF 2016
    # diagnostic across every stage window -- h-index on Celsius temp
    # returns the max as long as the window has more than a few days).
    # The NDVI/GCVI/ESI variants have scale-dependent semantics (input
    # NDVI is not on 0-1, so h-index returns values in the 4-6 range that
    # depend on the input scaling convention, not a well-defined
    # h-index property). Precip stays: N days with rain >= N mm captures
    # a genuinely distinct intensity-frequency tradeoff not encoded by
    # any other CID, and was the top-selected H-INDEX at 540 gOMP picks
    # in the Brazil maize July_09 13h03 run.
    "H-INDEX_Precip": ["h-Index", "h-Index of Precipitation"],
}

# AlphaEarth Foundations satellite embeddings (64 bands, annual)
dict_aef = {
    f"AEF_{i}": ["AEF", f"AlphaEarth Foundation embedding band {i}"]
    for i in range(1, 65)
}

# Global Aridity Index (Zomer 2022) — static per-region climatology of
# MA-Precip / MA-ET0 (higher = wetter, lower = more arid). One value per
# admin region (no time dimension), extracted by geoprepare's process_aridity.
dict_aridity = {
    "AI": ["Aridity", "Global Aridity Index (MA-P / MA-ET0, Zomer 2022; higher = wetter)"]
}

# SoilGrids 2.0 static soil properties — depth-weighted rooting-zone means
# (geoprepare process_soilgrids; depth from geobase [SOILGRIDS] depth_cm).
# One value per admin region, no time dimension; native SoilGrids units.
dict_soilgrids = {
    "SOIL_SAND": ["Soil", "SoilGrids sand fraction, rooting-zone mean (g/kg)"],
    "SOIL_CLAY": ["Soil", "SoilGrids clay fraction, rooting-zone mean (g/kg)"],
    "SOIL_SOC": ["Soil", "SoilGrids soil organic carbon, rooting-zone mean (dg/kg)"],
    "SOIL_BDOD": ["Soil", "SoilGrids bulk density, rooting-zone mean (cg/cm^3)"],
}
# index name -> raw column in the merged geoprepare CSV
soilgrids_col_map = {
    "SOIL_SAND": "soil_sand",
    "SOIL_CLAY": "soil_clay",
    "SOIL_SOC": "soil_soc",
    "SOIL_BDOD": "soil_bdod",
}
aridity_col_map = {"AI": "aridity"}

# Static per-region EO features (no time/stage dimension). These are NOT
# emitted as staged CID rows by cid/indices.py — geocif joins the raw
# geomerge columns onto the wide ML frame post-pivot as bare stage-less
# columns (geocif._add_static_eo_features) and force-includes them in
# create_feature_names, gated by use_cids.
dict_static_eo = {**dict_aridity, **dict_soilgrids}
STATIC_EO_COL_MAP = {**aridity_col_map, **soilgrids_col_map}

# FLDAS forecast variables (5 variables × 6 lead times, monthly resolution)
FLDAS_VARIABLES = [
    "SoilMoist_tavg", "TotalPrecip_tavg", "Tair_tavg", "Evap_tavg", "TWS_tavg"
]
FLDAS_LEADS = list(range(6))

dict_fldas = {}
fldas_col_map = {}  # index_name → raw column name in merged CSV

for _var in FLDAS_VARIABLES:
    for _lead in FLDAS_LEADS:
        _key = f"MEAN_FLDAS_{_var}_LEAD{_lead}"
        dict_fldas[_key] = ["FLDAS", f"Mean FLDAS {_var} (lead {_lead})"]
        fldas_col_map[_key] = f"fldas_{_var.lower()}_lead{_lead}"

# NOAA S2S forecast variables (2 variables × 6 lead times, monthly resolution)
# Multi-model mean of ECCC, ECMWF, NCEP, UKMO ensembles
S2S_VARIABLES = ["t2m", "tprate"]
S2S_LEADS = list(range(1, 7))  # 1-based: [1, 2, 3, 4, 5, 6]

dict_s2s = {}
s2s_col_map = {}  # index_name → raw column name in merged CSV

for _var in S2S_VARIABLES:
    for _lead in S2S_LEADS:
        _key = f"MEAN_S2S_{_var}_LEAD{_lead}"
        dict_s2s[_key] = ["S2S", f"Mean S2S {_var} (lead {_lead})"]
        s2s_col_map[_key] = f"s2s_{_var}_lead{_lead}"

# Engineered aggregate features (computed from raw leads, not read from CSV)
# Precipitation: sum across leads; Temperature/SoilMoist/Evap/TWS: mean across leads
FLDAS_AGG_FEATURES = {
    "SUM_FLDAS_TotalPrecip": ["FLDAS", "Sum of FLDAS precip forecast (all leads)"],
    "AVG_FLDAS_SoilMoist": ["FLDAS", "Mean FLDAS soil moisture (all leads)"],
    "AVG_FLDAS_Tair": ["FLDAS", "Mean FLDAS air temperature (all leads)"],
    "AVG_FLDAS_Evap": ["FLDAS", "Mean FLDAS evaporation (all leads)"],
    "AVG_FLDAS_TWS": ["FLDAS", "Mean FLDAS terrestrial water storage (all leads)"],
}
S2S_AGG_FEATURES = {
    "SUM_S2S_tprate": ["S2S", "Sum of S2S precipitation rate forecast (all leads)"],
    "AVG_S2S_t2m": ["S2S", "Mean S2S 2m temperature forecast (all leads)"],
}

# Forecast revision features (within-year change between consecutive init months)
FLDAS_REV_FEATURES = {
    f"REV_FLDAS_{_var}": ["FLDAS", f"Within-year forecast revision ({_var})"]
    for _var in FLDAS_VARIABLES
}
S2S_REV_FEATURES = {
    f"REV_S2S_{_var}": ["S2S", f"Within-year forecast revision ({_var})"]
    for _var in S2S_VARIABLES
}

# Multi-year Mean Absolute Revision (static per-region reliability)
FLDAS_MAR_FEATURES = {
    f"MAR_FLDAS_{_var}": ["FLDAS", f"Multi-year mean absolute revision ({_var})"]
    for _var in FLDAS_VARIABLES
}
S2S_MAR_FEATURES = {
    f"MAR_S2S_{_var}": ["S2S", f"Multi-year mean absolute revision ({_var})"]
    for _var in S2S_VARIABLES
}

# Separate engineered feature dicts — NOT merged into dict_fldas/dict_s2s
# because compute_eo_indices iterates those and expects "LEAD" in the name.
dict_fldas_engineered = {**FLDAS_AGG_FEATURES, **FLDAS_REV_FEATURES, **FLDAS_MAR_FEATURES}
dict_s2s_engineered = {**S2S_AGG_FEATURES, **S2S_REV_FEATURES, **S2S_MAR_FEATURES}

# ENSO teleconnection scalars: one value per harvest year, broadcast to every
# region (no geospatial join). Two indices, five prev-year + four curr-year
# windows each. Bracket a Southern-Hemisphere summer safra: prev-year covers
# pre-planting through El-Nino onset; curr-year covers early growth through
# grain fill. Sourced from CPC (ONI) and PSL (MEI v2) via geocif.cid.enso.
# Both indices have ~1-month operational lag, so they're usable for the
# 2026 forecast (see enso.py docstring for URL sources and update cadence).
ENSO_PREV_ONI = ["JJA", "ASO", "SON", "OND", "NDJ"]
ENSO_CURR_ONI = ["DJF", "JFM", "FMA", "MAM"]
ENSO_PREV_MEI = ["JJ", "AS", "SO", "ON", "ND"]
ENSO_CURR_MEI = ["DJ", "JF", "FM", "MA"]

dict_enso = {}
enso_col_map = {}  # index_name → raw column name added by enso.get_enso_frame

for _s in ENSO_PREV_ONI:
    _k = f"ONI_prev_{_s}"
    dict_enso[_k] = ["ENSO", f"Oceanic Nino Index, {_s} of preceding year"]
    enso_col_map[_k] = _k
for _s in ENSO_CURR_ONI:
    _k = f"ONI_curr_{_s}"
    dict_enso[_k] = ["ENSO", f"Oceanic Nino Index, {_s} of harvest year"]
    enso_col_map[_k] = _k
for _s in ENSO_PREV_MEI:
    _k = f"MEI_prev_{_s}"
    dict_enso[_k] = ["ENSO", f"Multivariate ENSO Index v2, {_s} of preceding year"]
    enso_col_map[_k] = _k
for _s in ENSO_CURR_MEI:
    _k = f"MEI_curr_{_s}"
    dict_enso[_k] = ["ENSO", f"Multivariate ENSO Index v2, {_s} of harvest year"]
    enso_col_map[_k] = _k

# USDA NASS QuickStats Crop Condition Index (CCI). Weekly state-level obs are
# collapsed to a MONTHLY MEAN per (state, year, month) in cid.cci.get_cci_frame,
# joined per (adm1_name, year, Month) in indices.preprocess_input_df, then
# aggregated over each stage window like the EO CIDs. US state-level, corn
# (maize) / soybean only; all map to the single 'cci' column.
dict_cci = {
    "MEAN_CCI": ["CCI", "Crop Condition Index (NASS QuickStats), stage mean of monthly means"],
    "MAX_CCI":  ["CCI", "Crop Condition Index (NASS QuickStats), stage max of monthly means"],
    "MIN_CCI":  ["CCI", "Crop Condition Index (NASS QuickStats), stage min of monthly means"],
}

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
}

dict_hindex = {
    "H-INDEX_NDVI": ["h-Index", "h-Index of NDVI"],
    "H-INDEX_GCVI": ["h-Index", "h-Index of GCVI"],
    "H-INDEX_ESI4WK": ["h-Index", "h-Index of ESI 4WK"],
    "H-INDEX_Tmax": ["h-Index", "h-Index of Tmax"],
    "H-INDEX_Tmin": ["h-Index", "h-Index of Tmin"],
    "H-INDEX_Tmean": ["h-Index", "h-Index of Tmean"],
    "H-INDEX_Precip": ["h-Index", "h-Index of Precipitation"],
}

# AlphaEarth Foundations satellite embeddings (64 bands, annual)
dict_aef = {
    f"AEF_{i}": ["AEF", f"AlphaEarth Foundation embedding band {i}"]
    for i in range(1, 65)
}

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

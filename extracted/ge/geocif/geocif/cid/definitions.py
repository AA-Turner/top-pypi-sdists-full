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

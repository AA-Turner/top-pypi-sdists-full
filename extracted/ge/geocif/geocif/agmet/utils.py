import os
import numpy as np
import pandas as pd
from datetime import datetime


dict_vars = {
    "lst": ["Land surface temperature", r"$^\circ$C", "MODIS LST", ""],
    "GDD": [
        "Growing degree days",
        r"$^\circ$C",
        "Growing Degree days: computed from NOAA CPC temperature",
        "",
    ],
    "cGDD": [
        "Cumulative growing degree days",
        r"$^\circ$C",
        "Growing Degree days: computed from NOAA CPC temperature",
        "",
    ],
    "ndvi": ["NDVI", "", "NDVI: UMD GLAM system", "NDVI"],
    "gcvi": ["GCVI", "", "GCVI: UMD GLAM system", ""],
    "yearly_ndvi": ["NDVI", "", "NDVI: UMD GLAM system", ""],
    "yearly_gcvi": ["GCVI", "", "GCVI: UMD GLAM system", ""],
    "cNDVI": [r"$\Sigma\ NDVI$", "", ""],
    "aucNDVI": ["AUC NDVI", "", ""],
    "lai": ["Leaf area index", r"$m^2/m^2$", "", ""],
    "fpar": ["Fraction of PAR", "%", "", ""],
    "et_daily": ["Evap. anomaly", "%", "", ""],
    "esi_12wk": ["Evaporative Stress Index", "", ""],
    "esi_4wk": ["Evaporative Stress Index", "", "", "Índice de Evapotranspiración"],
    "chirps": ["Precipitation", "mm", "Precipitation: CHIRPS", ""],
    "daily_precip": ["Precipitation", "mm", "Precipitation: CHIRPS", ""],
    "cumulative_precip": ["Precipitation", "mm", "Precipitation: CHIRPS", ""],
    "ncep2_min": ["Temperature (min)", r"$^\circ$C", "Temperature: NCEP2", ""],
    "ncep2_mean": ["Temperature (mean)", r"$^\circ$C", "Temperature: NCEP2", ""],
    "ncep2_max": ["Temperature (max)", r"$^\circ$C", "Temperature: NCEP2", ""],
    "ncep2_precip": ["Precipitation (NCEP)", "mm", "Precipitation: NCEP2", ""],
    "cpc_tmin": [
        "Min. Temperature",
        r"$^\circ$C",
        "Temperature: NOAA CPC",
        "Temperatura Mínima",
    ],
    "cpc_tmax": [
        "Max. Temperature",
        r"$^\circ$C",
        "Temperature: NOAA CPC",
        "Temperatura Máxima",
    ],
    "cpc_precip": ["Precipitation", "mm", "Precipitation: NOAA CPC", ""],
    "daymet_tmin": [
        "Min. Temperature",
        r"$^\circ$C",
        "Temperature: Daymet V4",
        "Temperatura Mínima",
    ],
    "daymet_tmax": [
        "Max. Temperature",
        r"$^\circ$C",
        "Temperature: Daymet V4",
        "Temperatura Máxima",
    ],
    "daymet_prcp": ["Precipitation", "mm", "Precipitation: Daymet V4", ""],
    "chirts_era5_tmin": [
        "Min. Temperature",
        r"$^\circ$C",
        "Temperature: CHIRTS-ERA5",
        "Temperatura Mínima",
    ],
    "chirts_era5_tmax": [
        "Max. Temperature",
        r"$^\circ$C",
        "Temperature: CHIRTS-ERA5",
        "Temperatura Máxima",
    ],
    "soil_moisture_as1": ["Soil moisture (surface)", "mm", "", "Humedad Superficial"],
    "soil_moisture_as2": ["Soil moisture (sub-surface)", "mm", "", ""],
    "nsidc_surface": ["Soil moisture (surface)", "mm", "", "Humedad Superficial"],
    "nsidc_rootzone": ["Soil moisture (sub-surface)", "mm", "", ""],
    "fldas_tair_tavg": ["Air Temperature (FLDAS)", r"$^\circ$C", "FLDAS NMME Forecast", ""],
    "fldas_totalprecip_tavg": ["Precipitation (FLDAS)", "mm/day", "FLDAS NMME Forecast", ""],
    "fldas_soilmoist_tavg": ["Soil Moisture (FLDAS)", r"m$^3$/m$^3$", "FLDAS NMME Forecast", ""],
    "agera5_snow_thickness_lwe": ["Snow thickness (LWE)", "mm", "AgERA5", ""],
    "etref": ["Reference ET", "mm/day", "NOAA PSL RefET (NCEP)", ""],
}


CROP_ABBREV = {
    "maize": "mz", "winter_wheat": "ww", "spring_wheat": "sw",
    "soybean": "sb", "soybeans": "sb", "rice": "rc",
    "millet": "ml", "sorghum": "sr", "teff": "tf", "wheat": "ww",
}


def get_crop_abbrev(crop):
    """Return the short abbreviation for a crop name (e.g. 'maize' → 'mz')."""
    return CROP_ABBREV.get(crop.lower().strip(), crop)


def get_crop_name(crop):
    """
    This function takes a crop abbreviation or full name and returns the display name.
    Args:
        crop ():

    Returns:

    """
    lookup = {
        "ww": "Winter Wheat",
        "sw": "Spring Wheat",
        "mz": "Maize",
        "sb": "Soybean",
        "maize": "Maize",
        "wheat": "Wheat",
        "winter_wheat": "Winter Wheat",
        "spring_wheat": "Spring Wheat",
        "soybean": "Soybean",
        "soybeans": "Soybean",
        "rice": "Rice",
        "sorghum": "Sorghum",
        "millet": "Millet",
        "barley": "Barley",
        "teff": "Teff",
        "cassava": "Cassava",
        "groundnut": "Groundnut",
        "groundnuts": "Groundnut",
        "sesame": "Sesame",
        "cotton": "Cotton",
        "sugarcane": "Sugarcane",
        "potato": "Potato",
        "potatoes": "Potato",
        "beans": "Beans",
        "cowpea": "Cowpea",
        "sunflower": "Sunflower",
    }
    result = lookup.get(crop.lower().strip())
    if result:
        return result
    # Fallback: title-case the crop name
    return crop.replace("_", " ").title()


def sliding_mean(data_array, window=5):
    """
    This function takes an array of numbers and smoothes them out.
    Smoothing is useful for making plots a little easier to read.
    Args:
        data_array ():
        window ():

    Returns:

    """
    # Return without change if window size is zero
    if window == 0:
        return data_array

    data_array = np.array(data_array)
    new_list = []
    for i in range(len(data_array)):
        indices = range(max(i - window + 1, 0), min(i + window + 1, len(data_array)))
        avg = 0
        for j in indices:
            avg += data_array[j]
        avg /= float(len(indices))
        new_list.append(avg)

    return np.array(new_list)


def get_model_frequency(frequency):
    """

    Args:
        frequency ():

    Returns:

    """
    if frequency == "daily":
        return 1
    elif frequency == "weekly":
        return 7
    elif frequency == "dekad":
        return 10
    elif frequency == "monthly":
        return 30
    elif frequency == "biweekly":
        return 14
    else:
        raise ValueError(f"Invalid frequency {frequency}")


def _get_date_range(start_date, end_date, interval="daily"):
    """
    This function generates a date range based on the interval
    Args:
        start_date ():
        end_date ():
        interval ():

    Returns:

    """
    # Check if start and end date(s) are of type datetime
    if not isinstance(start_date, pd.Timestamp):
        start_date = pd.Timestamp(start_date)
    if not isinstance(end_date, pd.Timestamp):
        end_date = pd.Timestamp(end_date)

    # Generate date range based on interval
    if interval == "daily":
        dates = pd.date_range(start_date, end_date, freq="D")
    elif interval == "weekly":
        dates = pd.date_range(start_date, end_date, freq="W")
    elif interval == "dekad":
        dates = pd.date_range(start_date, end_date, freq="10D")
    elif interval == "monthly":
        dates = pd.date_range(start_date, end_date, freq="M")
    elif interval == "biweekly":
        dates = pd.date_range(start_date, end_date, freq="2W")
    elif interval in ["peak_season", "full_season"]:
        # get first date and peak/last date of season
        dates = pd.date_range(start_date, end_date, periods=2)
    else:
        raise ValueError(f"Invalid interval {interval}")

    # Insert start date at the beginning of the list
    dates = dates.insert(0, start_date)

    # If end_date is a different interval than the current last item in dates,
    # then insert end_date into the list
    if dates[-1].month != end_date.month:
        dates = dates.insert(len(dates), end_date)

    return dates


def get_date_range(start_date, end_date, interval="dekad", get_doy=True):
    """

    Args:
        start_date ():
        end_date ():
        interval ():
        get_doy ():

    Returns:

    """
    dates = _get_date_range(start_date, end_date, interval)

    # convert dates to day of year
    if get_doy:
        dates = [date.day_of_year for date in dates]

    return dates


def get_datetime_from_doy(year, doy):
    """

    Args:
        year ():
        doy ():

    Returns:

    """
    import datetime

    return datetime.datetime(year, 1, 1) + datetime.timedelta(doy - 1)


def get_doys(full_season, interval="dekad", exclude_future=True):
    """

    Args:
        full_season ():
        interval ():
        exclude_future ():

    Returns:

    """
    # Get start and end date, format is [year, month, day of year]
    start_year, start_doy = full_season[0][0], full_season[0][2]
    end_year, end_doy = full_season[-1][0], full_season[-1][2]

    # convert from [year, month, day of year] to datetime
    start_date = get_datetime_from_doy(start_year, start_doy)
    end_date = get_datetime_from_doy(end_year, end_doy)

    if exclude_future:
        if end_date > datetime.today():
            end_date = datetime.today()

    # get list of julian days between start and end date for which model will be run, default is dekad
    doys = get_date_range(start_date, end_date, interval=interval)

    return doys


def year_range(start, stop):
    """

    Args:
        start ():
        stop ():

    Returns:

    """
    if stop < start:
        stop += 365

    i = start
    while i < stop:
        yield (i - 1) % 365 + 1
        i += 1

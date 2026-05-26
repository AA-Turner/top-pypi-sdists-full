import numpy as np
from typing import Union
from tqdm.rich import tqdm

from geocif import utils
from geocif.progress import pbar as _pbar


def add_stage_information(df, method, label=""):
    """

    Args:
        df:
        method:

    Returns:

    """
    # Hack: Drop rows where Stage is the string nan
    df = df[df['Stage'] != 'nan']
    # Drop rows where all values are NaN
    df = df.dropna(how='all')

    # Change to type string
    df["Stage"] = df["Stage"].astype(str)

    df["Stage_ID"] = df["Stage"]

    def _stage_range(x):
        if x.startswith(("PS", "IS")):
            return x
        return "_".join([x.split("_")[0], x.split("_")[-1]])

    def _start_stage(x):
        if x.startswith(("PS", "IS")):
            return 0
        return int(x.split("_")[0])

    def _end_stage(x):
        if x.startswith(("PS", "IS")):
            return 0
        return int(x.split("_")[-1])

    df["Stage Range"] = df["Stage"].apply(_stage_range)
    df["Starting Stage"] = df["Stage"].apply(_start_stage)
    df["Ending Stage"] = df["Stage"].apply(_end_stage)

    # Create a column called Stage Names that applies utils.dict_growth_stages
    # to the Starting Stage and Ending Stage
    if "dekad" in method:
        stage_dict = utils.dict_growth_stages
        stage_dict_end = utils.dict_growth_stages_end
    elif "biweekly" in method:
        stage_dict = utils.dict_growth_stages_biweekly
        stage_dict_end = utils.dict_growth_stages_biweekly_end
    elif "monthly" in method:
        stage_dict = utils.dict_growth_stages_monthly
        stage_dict_end = utils.dict_growth_stages_monthly_end
    # Wrap around for stages beyond the dictionary length
    n = len(stage_dict)
    wrap_start = lambda x: stage_dict[((x - 1) % n) + 1] if x > 0 else "Pre-Season"
    wrap_end = lambda x: stage_dict_end[((x - 1) % n) + 1] if x > 0 else "Pre-Season"

    # Pre-season rows get their Stage_ID as Stage Names (e.g., "PS_9")
    is_ps = df["Stage"].str.startswith("PS") | df["Stage"].str.startswith("IS")
    df["Stage Names"] = (
        df["Starting Stage"].map(wrap_start) + " - " + df["Ending Stage"].map(wrap_end)
    )
    df.loc[is_ps, "Stage Names"] = df.loc[is_ps, "Stage"]

    df["Percentage Season"] = float("nan")

    # Group by Region and Harvest Year
    grouped = df.groupby(["Region", "Harvest Year"])

    # Loop through groups with tqdm
    desc = f"Computing Percentage Season ({label})" if label else "Computing Percentage Season"
    for (region, year), group in _pbar(grouped, desc=desc):
        idx = group.index
        n = len(group)
        df.loc[idx, "Percentage Season"] = [i * 100.0 / n for i in range(n)]

    return df


def remove_duplicates(arrays):
    """

    Args:
        arrays:

    Returns:

    """
    seen = set()
    unique_arrays = []
    for arr in arrays:
        # Convert array to a tuple which is hashable and can be added to a set
        arr_tuple = tuple(arr)
        if arr_tuple not in seen:
            unique_arrays.append(arr)
            seen.add(arr_tuple)

    return unique_arrays


def get_n_percent(arrays, n):
    """

    Args:
        arrays:
        n:

    Returns:

    """
    # Calculate the number of elements corresponding to n percent
    num_elements = int(len(arrays) * (n / 100))

    # Select the first and last element of arrays
    selected_elements = [arrays[0]]

    # Now select n% of the elements in between equally spaced
    # Determine the step to equally space selected elements
    if num_elements > 1:
        step = max(1, len(arrays) // (num_elements - 1))
    else:
        step = len(arrays)  # Prevent division by zero if num_elements is 1

    # Select elements using the computed step, ensuring the last element is included
    for i in range(0, len(arrays), step):
        if len(selected_elements) < num_elements:
            selected_elements.append(arrays[i])

    selected_elements.append(arrays[-1])

    return selected_elements


def find_matching_elements(original_arrays, start_elements):
    """

    Args:
        original_arrays:
        start_elements:

    Returns:

    """
    matches = []

    # Check if the beginning of each array in the original list matches any in the start_elements
    for original in original_arrays:
        for start in start_elements:
            # Check if the original array starts with the same elements as start
            if np.array_equal(original[: len(start)], start):
                matches.append(original)

    return matches


def select_stages_for_ml(stages_features, method="latest", n=100):
    """
    Given a list of numpy arrays that represents stages for which features are available,
    select the latest stage and all the stages that start with the latest stage
    Args:
        stages_features:
        method:
        n:

    Returns:

    """
    latest_stage = stages_features[0]

    selected_stages = []
    if method == "latest":
        # Find the longest array in the list of arrays
        selected_stages = [max(stages_features, key=len)]

        # Only select those arrays in the list of arrays that are starting with latest_stage
        # for stage in stages_features:
        #     if stage[0] == latest_stage[0]:
        #         selected_stages.append(stage)
    elif method == "fraction":
        # Filter arrays with exactly 2 elements
        two_element_arrays = []
        for arr in stages_features:
            if len(arr) == 2:
                two_element_arrays.append(arr)

        start_elements = get_n_percent(two_element_arrays, n)
        start_elements = remove_duplicates(start_elements)

        # Find all arrays in the original list that start with any of the start_elements
        selected_stages = find_matching_elements(stages_features, start_elements)

    return selected_stages


def get_stage_information_dict(stage_str, method):
    """
    e.g. stage_str is 'GD4_8_7_6_5_4_3_2_1_37_36_35_34_33_32'
    Returns a dictionary with the following
    {
        "Stage_ID": "GD4_8_7_6_5_4_3_2_1_37_36_35_34_33_32",
        "Stage Range": "8_32",
        "Starting Stage": 8,
        "Ending Stage": 32,
        "Stage Names": "Mar 11 - Nov 6",
    }
    based on the utils.dict_growth_stages dictionary
    Args:
        stage_str:

    Returns:

    """
    stage_info = {}

    stage_info["Stage_ID"] = stage_str

    parts = stage_str.split("_")

    # Pre-season / forecast-only in-season: Stage_ID is "PS_N" or "IS_N".
    # Column looks like "MEAN_FLDAS_SoilMoist_tavg_LEAD0_PS_4" or "_IS_3".
    ps_idx = next((i for i, p in enumerate(parts) if p in ("PS", "IS")), None)
    if ps_idx is not None:
        cid = "_".join(parts[:ps_idx])
        stage_id = "_".join(parts[ps_idx:])  # "PS" or "PS_4"
        lead_idx = next((i for i, p in enumerate(parts) if p.startswith("LEAD")), None)
        lead_str = ""
        if lead_idx is not None:
            lead_str = f" {parts[lead_idx]}"
        return {
            "Stage_ID": stage_id,
            "CID": cid,
            "Stage Range": stage_id,
            "Starting Stage": 0,
            "Ending Stage": 0,
            "Stage Name": f"Pre-Season{lead_str}",
        }

    # Find where numeric stage numbers begin.
    # AEF_N has a numeric band suffix that is part of the CID name, so skip it.
    skip = 2 if parts[0] == "AEF" else 1
    first_stage_idx = next(
        (i for i in range(skip, len(parts)) if parts[i].isdigit()),
        len(parts),
    )
    cid = "_".join(parts[:first_stage_idx])
    stage_parts = parts[first_stage_idx:]
    start_stage = stage_parts[0] if stage_parts else "0"
    end_stage = stage_parts[-1] if stage_parts else "0"

    # For FLDAS MEAN_FLDAS_<var>_LEAD<N>_... features, the label must describe
    # a single target month = end_stage + N (mod 12). At runtime the FLDAS
    # branch in compute_eo_indices uses only the LATEST init-month row in the
    # cumulative stage window, and lead-N targets month init+N per FF2 STM
    # §6.1.1 / Figures 23-29. Non-FLDAS features keep the stage range unshifted.
    fldas_lead = None
    if parts[0] == "MEAN" and len(parts) >= 2 and parts[1] in ("FLDAS", "S2S"):
        lead_idx = next((i for i, p in enumerate(parts) if p.startswith("LEAD")), None)
        if lead_idx is not None:
            try:
                fldas_lead = int(parts[lead_idx][len("LEAD"):])
            except ValueError:
                fldas_lead = 0
        else:
            fldas_lead = 0

    # Exclude cid from the stage_str string
    stage_info["Stage_ID"] = "_".join(stage_parts)

    stage_info["CID"] = cid
    stage_info["Stage Range"] = "_".join([start_stage, end_stage])

    stage_info["Starting Stage"] = int(start_stage)
    stage_info["Ending Stage"] = int(end_stage)

    if "dekad" in method:
        stage_dict = utils.dict_growth_stages
        stage_dict_end = utils.dict_growth_stages_end
    elif "biweekly" in method:
        stage_dict = utils.dict_growth_stages_biweekly
        stage_dict_end = utils.dict_growth_stages_biweekly_end
    elif "monthly" in method:
        stage_dict = utils.dict_growth_stages_monthly
        stage_dict_end = utils.dict_growth_stages_monthly_end
    # Wrap around for stages beyond the dictionary length
    n = len(stage_dict)
    if fldas_lead is not None:
        # Single-month FLDAS label: target = init_month + lead (mod 12).
        # For forward stages (e.g. monthly), numeric_parts[-1] == end_stage
        # is the chronologically-latest month. For reverse stages (e.g.
        # monthly_r), the window grows backward so numeric_parts[0] ==
        # start_stage is the chronologically-latest month. We want the
        # latest because compute_eo_indices picks max(time) within the
        # stage window.
        init_month = int(start_stage) if "_r" in method else int(end_stage)
        target = (((init_month - 1) + fldas_lead) % n) + 1
        stage_info["Stage Name"] = (
            stage_dict[target] + "-" + stage_dict_end[target]
        )
    else:
        stage_info["Stage Name"] = (
            stage_dict[(((int(start_stage) - 1)) % n) + 1] + "-" +
            stage_dict_end[(((int(end_stage) - 1)) % n) + 1]
        )

    return stage_info


def update_feature_names(df, method):
    elements = df.columns

    # Dictionary to store the results
    stages_info = {}

    for element in elements:
        # Splitting each element by '_'
        parts = element.split("_")

        # fldas_lead tracks the FLDAS forecast lead time (None for non-FLDAS
        # features). For FLDAS we must shift the label window by lead months
        # because each row's Lead-N targets month init+N, not init (per
        # FLDAS-Forecast V2 STM §6.1.1 and Figures 23-29).
        fldas_lead = None

        # AEF_N has a numeric band suffix that is part of the CID name
        if parts[0] == "AEF" and len(parts) >= 2:
            cid = "_".join(parts[:2])  # AEF_1, AEF_2, ...
            stage_parts = parts[2:]
        elif parts[0] in ("AVG", "SUM", "REV", "MAR") and len(parts) >= 2 and parts[1] in ("FLDAS", "S2S"):
            # Engineered features: AVG_FLDAS_SoilMoist_PS_9
            # Find PS/IS marker to split CID name from stage
            ps_idx = next((i for i, p in enumerate(parts) if p in ("PS", "IS")), None)
            if ps_idx is not None:
                cid = "_".join(parts[:ps_idx])
                stage_parts = parts[ps_idx:]
            else:
                cid = "_".join(parts)
                stage_parts = []
        elif parts[0] == "MEAN" and len(parts) >= 2 and parts[1] in ("FLDAS", "S2S"):
            # MEAN_FLDAS_SoilMoist_tavg_LEAD0_1_2_3
            # Find LEADn token to split CID name from stage numbers
            lead_idx = next((i for i, p in enumerate(parts) if p.startswith("LEAD")), None)
            if lead_idx is not None:
                cid = "_".join(parts[:lead_idx + 1])
                stage_parts = parts[lead_idx + 1:]
                # Extract integer lead from "LEAD3" -> 3 so the label can
                # shift by the forecast-target offset.
                try:
                    fldas_lead = int(parts[lead_idx][len("LEAD"):])
                except ValueError:
                    fldas_lead = 0
            else:
                cid = "_".join(parts[:2])
                stage_parts = parts[2:]
                fldas_lead = 0
        elif len(parts) >= 2 and parts[1].isdigit():
            cid = parts[0]
            stage_parts = parts[1:]
        elif len(parts) >= 3:
            cid = "_".join(parts[:2])
            stage_parts = parts[2:]
        else:
            continue

        # Pre-season / forecast-only in-season: stage_parts is ["PS", "4"] or ["IS", "3"].
        if stage_parts and stage_parts[0] in ("PS", "IS"):
            stage_id = "_".join(stage_parts)
            lead_idx = next((i for i, p in enumerate(cid.split("_")) if p.startswith("LEAD")), None)
            lead_label = ""
            if lead_idx is not None:
                lead_label = f" {cid.split('_')[lead_idx]}"
            prefix = "Pre-Season" if stage_parts[0] == "PS" else "In-Season"
            new_column_name = f"{cid} {prefix}{lead_label}"
            stages_info[element] = (cid, stage_id, stage_id, new_column_name)
            continue

        # Filtering stage_parts to only keep numeric stages
        numeric_parts = [part for part in stage_parts if part.isdigit()]

        # if numeric_parts is empty, skip this element
        if not numeric_parts:
            continue

        # The starting stage is the first numeric part
        start_stage = numeric_parts[0]

        # The ending stage is the last numeric part
        end_stage = numeric_parts[-1]

        # Convert starting and ending stage using utils.dict_growth_stages
        if "dekad" in method:
            stage_dict = utils.dict_growth_stages
            stage_dict_end = utils.dict_growth_stages_end
        elif "biweekly" in method:
            stage_dict = utils.dict_growth_stages_biweekly
            stage_dict_end = utils.dict_growth_stages_biweekly_end
        elif "monthly" in method:
            stage_dict = utils.dict_growth_stages_monthly
            stage_dict_end = utils.dict_growth_stages_monthly_end
        # Wrap around for stages beyond the dictionary length (e.g. stage 13 → month 1)
        n = len(stage_dict)
        if fldas_lead is not None:
            # FLDAS features are now single-month: the runtime uses ONLY the
            # latest init-month row in the cumulative stage window (see
            # compute_eo_indices FLDAS branch). The label therefore describes
            # a single target month = init_month + lead (mod 12), not a range.
            # For forward stages the latest month is numeric_parts[-1]
            # (end_stage); for reverse ``_r`` stages the window grows backward
            # in time so the latest month is numeric_parts[0] (start_stage).
            init_month = int(numeric_parts[0]) if "_r" in method else int(numeric_parts[-1])
            target = (((init_month - 1) + fldas_lead) % n) + 1
            start_stage = stage_dict[target]
            end_stage = stage_dict_end[target]
        else:
            start_stage = stage_dict[(((int(start_stage) - 1)) % n) + 1]
            end_stage = stage_dict_end[(((int(end_stage) - 1)) % n) + 1]

        new_column_name = f"{cid} {start_stage}-{end_stage}"

        # Saving the result in the dictionary
        stages_info[element] = (cid, start_stage, end_stage, new_column_name)

    # For each column in df, check if it exists in stages_info, and
    # replace it with the new column name
    # Precompute the rename mapping outside the loop
    rename_mapping = {}
    for column in df.columns:
        if column in stages_info:
            _, _, _, new_column_name = stages_info[column]
            rename_mapping[column] = new_column_name

    # Apply all renames at once
    df.rename(columns=rename_mapping, inplace=True)

    return df


def convert_stage_string(stage_info: Union[str, np.ndarray], to_array: bool = True) -> Union[np.ndarray, str]:
    """
    Converts a string of stage information to a numpy array or vice versa.

    Args:
        stage_info: A string of stages separated by underscores or a numpy array of stages e.g. '13_12_11'
        to_array: A boolean indicating the direction of conversion. If True, converts string to numpy array e.g. array([13, 12, 11])
                  If False, converts numpy array to string.

    Returns:
        A numpy array of stages if to_array is True, or a string of stages if to_array is False.

    Raises:
        ValueError: If the input format is incorrect.
    """
    if to_array:
        if not isinstance(stage_info, str):
            raise ValueError("Expected a string for stage_info when to_array is True.")
        try:
            stages = np.array([int(stage) for stage in stage_info.split("_")])
        except ValueError:
            raise ValueError("Stage info string should contain integers separated by underscores.")
    else:
        if not isinstance(stage_info, np.ndarray):
            raise ValueError("Expected a numpy array for stage_info when to_array is False.")
        stages = "_".join(map(str, stage_info))

    return stages


def select_single_calendar_period_features(df):
    """Keep only columns whose stage span is a SINGLE calendar period
    (start == end). Stricter than ``select_single_time_period_features``,
    which keeps 2-stage spans like vDTR_7_6 (Jun+Jul).

    Under method = monthly, "single calendar period" = one calendar month.
    Under biweekly/dekad it's one biweek / one dekad.

    Examples (monthly method):
        vDTR_7           → keep  (renamed to "vDTR Jul 1-Jul 31")
        vDTR_7_7         → keep  (same)
        vDTR_7_6         → drop  (Jun-Jul cumulative span)
        vDTR_7_6_5       → drop  (May-Jul span)
        SoilMoist_PS_4   → drop  (Pre-Season aggregate)
        SoilMoist_IS_3   → drop  (In-Season aggregate)
        AEF_5            → keep  (spatial embedding, no stage)
        MEAN_FLDAS_*     → keep  (FLDAS forecasts; handled specially elsewhere)
        Region, lag_1    → keep  (categorical / lag, no stage suffix)

    Apply PRE-rename — column names still have ``_`` separators so the
    numeric reasoning is clean.
    """
    def is_single_calendar_period(col: str) -> bool:
        # Whitelisted prefixes that never follow the stage convention
        if col.startswith("AEF_") or col.startswith("MEAN_FLDAS_"):
            return True
        # Pre-Season / In-Season aggregates are multi-period by construction
        if "_PS_" in col or "_IS_" in col or col.endswith("_PS") or col.endswith("_IS"):
            return False
        # Collect trailing numeric tokens (the stage span)
        parts = col.split("_")
        trailing_nums = []
        for p in reversed(parts):
            if p.isdigit():
                trailing_nums.append(int(p))
            else:
                break
        if not trailing_nums:
            # No trailing numbers → not a stage feature. Let the CID/Index
            # filter decide whether to drop (e.g. Region, lag_1 survive).
            return True
        return len(set(trailing_nums)) == 1  # single calendar period iff all equal

    keep = [c for c in df.columns if is_single_calendar_period(c)]
    return df[keep]


def select_single_time_period_features(df):
    """
    Only select those features that span a single time-period
    e.g. vDTR_7_6 is ok but vDTR_7_6_5 is not
    Args:
        df: A DataFrame containing features with time-periods in their names

    Returns:

    """
    import re

    pattern_two_numbers = r'^\D*\d+_\d+\D*$'  # Pattern for exactly two numbers separated by an underscore
    pattern_no_numbers = r'^[^\d_]+$'  # Pattern for columns with no numbers

    # Filter columns based on the patterns
    # AEF columns (spatial embeddings) are always kept — they don't follow
    # the time-period naming convention.
    filtered_columns_combined = [
        col for col in df.columns
        if re.match(pattern_two_numbers, col)
        or re.match(pattern_no_numbers, col)
        or col.startswith("AEF_")
        or col.startswith("MEAN_FLDAS_")
    ]

    # Create a new DataFrame with the filtered columns
    df = df[filtered_columns_combined]

    return df

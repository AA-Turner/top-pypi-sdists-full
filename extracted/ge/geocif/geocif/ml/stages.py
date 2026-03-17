import numpy as np
from typing import Union
from tqdm import tqdm

from geocif import utils


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
    df["Stage Range"] = df["Stage"].apply(
        lambda x: "_".join([x.split("_")[0], x.split("_")[-1]])
    )

    # Create a column with starting stage and ending stage
    # Stage looks like this: 13_12_11
    # Starting Stage will look like this: 13
    # Ending Stage will look like this: 11
    df["Starting Stage"] = df["Stage"].apply(lambda x: int(x.split("_")[0]))
    df["Ending Stage"] = df["Stage"].apply(lambda x: int(x.split("_")[-1]))

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
    wrap_start = lambda x: stage_dict[((x - 1) % n) + 1]
    wrap_end = lambda x: stage_dict_end[((x - 1) % n) + 1]
    df["Stage Names"] = (
        df["Starting Stage"].map(wrap_start) + " - " + df["Ending Stage"].map(wrap_end)
    )

    df["Percentage Season"] = float("nan")

    # Group by Region and Harvest Year
    grouped = df.groupby(["Region", "Harvest Year"])

    # Loop through groups with tqdm
    desc = f"Computing Percentage Season ({label})" if label else "Computing Percentage Season"
    for (region, year), group in tqdm(grouped, desc=desc):
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
    # AEF_N has a numeric band suffix that is part of the CEI name
    if parts[0] == "AEF":
        cei = "_".join(parts[:2])  # AEF_1, AEF_2, ...
        start_stage = parts[2]
        stage_parts = parts[2:]
    elif parts[1].isdigit():
        cei = parts[0]
        start_stage = parts[1]
        stage_parts = parts[1:]
    else:
        cei = "_".join(parts[:2])
        start_stage = parts[2]
        stage_parts = parts[2:]
    end_stage = parts[-1]

    # Exclude cei from the stage_str string
    stage_info["Stage_ID"] = "_".join(stage_parts)

    stage_info["CEI"] = cei
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
    stage_info["Stage Name"] = (
        stage_dict[((int(start_stage) - 1) % n) + 1] + "-" +
        stage_dict_end[((int(end_stage) - 1) % n) + 1]
    )

    return stage_info


def update_feature_names(df, method):
    elements = df.columns

    # Dictionary to store the results
    stages_info = {}

    for element in elements:
        # Splitting each element by '_'
        parts = element.split("_")

        # AEF_N has a numeric band suffix that is part of the CEI name
        if parts[0] == "AEF" and len(parts) >= 2:
            cei = "_".join(parts[:2])  # AEF_1, AEF_2, ...
            stage_parts = parts[2:]
        elif len(parts) >= 2 and parts[1].isdigit():
            cei = parts[0]
            stage_parts = parts[1:]
        elif len(parts) >= 3:
            cei = "_".join(parts[:2])
            stage_parts = parts[2:]
        else:
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
        start_stage = stage_dict[((int(start_stage) - 1) % n) + 1]
        end_stage = stage_dict_end[((int(end_stage) - 1) % n) + 1]

        new_column_name = f"{cei} {start_stage}-{end_stage}"

        # Saving the result in the dictionary
        stages_info[element] = (cei, start_stage, end_stage, new_column_name)

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

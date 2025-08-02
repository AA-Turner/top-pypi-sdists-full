import argparse
import os
from datetime import datetime, timedelta

import numpy as np
import polars as pl
from mary_elizabeth_utils.utils.logger import setup_colored_logger

from data_config import (
    register_configs,
    register_periods,
)

logger = setup_colored_logger(__name__)

# Set a global seed for reproducibility
np.random.seed(42)

# Constants
CENTURY_18 = 18
CENTURY_19 = 19
CENTURY_20 = 20
YEAR_1937 = 1937
MINIMUM_ADULT_AGE = 18
YOUNG_ADULT_AGE = 25
FEBRUARY = 2
MINIMUM_PARENT_AGE = 15
MAXIMUM_PARENT_AGE = 50
MAXIMUM_FAMILY_SIZE = 10
CHILD_PARENT_PROBABILITY = 0.8
MINIMUM_EDUCATION_AGE = 16
EARLY_EDUCATION_AGE = 20
PROB = 0.8

# Global caches
ADDRESS_CACHE = {}
PNR_CACHE = {}
FAMILIE_ID_CACHE = {}
FAMILIE_ID_HISTORY = {}
RECNUM_CACHE = {}


def get_or_create_recnum(pnr, year):
    key = (pnr, year)
    if key not in RECNUM_CACHE:
        RECNUM_CACHE[key] = np.random.randint(1000000, 9999999)
    return RECNUM_CACHE[key]


def generate_realistic_birth_date(year):
    month = np.random.randint(1, 13)
    if month in [4, 6, 9, 11]:
        day = np.random.randint(1, 31)
    elif month == FEBRUARY:
        day = np.random.randint(1, 29)
    else:
        day = np.random.randint(1, 32)
    return datetime(year, month, day)


def get_appropriate_marital_status(age):
    if age < MINIMUM_ADULT_AGE:
        return "U"
    elif age < YOUNG_ADULT_AGE:
        return np.random.choice(["U", "G"], p=[0.8, 0.2])
    else:
        return np.random.choice(["U", "G", "F", "E"], p=[0.3, 0.5, 0.1, 0.1])


def generate_parent_age(child_birth_year):
    return child_birth_year - np.random.randint(20, 45)  # Parents are 20-45 years older than child


def ensure_shared_address(data):
    familie_addresses = {}
    for row in data.iter_rows(named=True):
        if row["FAMILIE_ID"] not in familie_addresses:
            familie_addresses[row["FAMILIE_ID"]] = row["ADDRESS"]
        else:
            data = data.with_columns(
                pl.when(pl.col("FAMILIE_ID") == row["FAMILIE_ID"])
                .then(familie_addresses[row["FAMILIE_ID"]])
                .otherwise(pl.col("ADDRESS"))
                .alias("ADDRESS")
            )
    return data


def check_age_consistency(birth_year, current_year, age):
    return current_year - birth_year == age


def check_parent_child_age_difference(parent_birth_year, child_birth_year):
    age_difference = child_birth_year - parent_birth_year
    return MINIMUM_PARENT_AGE <= age_difference <= MAXIMUM_PARENT_AGE


def check_family_size(familie_id, data):
    family_size = data.filter(pl.col("FAMILIE_ID") == familie_id).shape[0]
    return family_size <= MAXIMUM_FAMILY_SIZE  # Adjust the maximum family size as needed


def generate_improved_data(register_configs, num_records, year):
    data = {}
    for register, config in register_configs.items():
        register_data = generate_register_data(config, num_records, year)

        if register == "BEF":
            register_data = improve_bef_data(register_data, year)

        data[register] = register_data

    return data


def improve_bef_data(bef_data, year):
    bef_data = bef_data.with_columns(
        [
            pl.col("FOED_DAG")
            .map_elements(lambda x: generate_realistic_birth_date(x.year))
            .alias("FOED_DAG"),
            (pl.lit(year) - pl.col("FOED_DAG").dt.year()).alias("ALDER"),
        ]
    )

    bef_data = bef_data.with_columns(
        [
            pl.col("ALDER").map_elements(get_appropriate_marital_status).alias("CIVST"),
            pl.struct(["PNR", "ALDER", "CIVST"])
            .map_elements(lambda x: generate_familie_id(x["PNR"], x["ALDER"], x["CIVST"]))
            .alias("FAMILIE_ID"),
        ]
    )

    # Ensure shared address for shared FAMILIE_ID
    bef_data = ensure_shared_address(bef_data)

    # Check family size
    family_sizes = (
        bef_data.group_by("FAMILIE_ID")
        .agg(pl.count())
        .filter(pl.col("count") > MAXIMUM_FAMILY_SIZE)
    )
    large_families = family_sizes["FAMILIE_ID"]

    bef_data = bef_data.with_columns(
        [
            pl.when(pl.col("FAMILIE_ID").is_in(large_families))
            .then(
                pl.struct(["PNR", "ALDER", "CIVST"]).map_elements(
                    lambda x: generate_familie_id(x["PNR"], x["ALDER"], x["CIVST"])
                )
            )
            .otherwise(pl.col("FAMILIE_ID"))
            .alias("FAMILIE_ID")
        ]
    )

    return bef_data


def generate_register_data(config, num_records, year):
    data = {}
    for col, col_config in config.items():
        if col_config["type"] == "pnr":
            data[col] = pl.Series(
                [
                    get_or_create_pnr(
                        generate_realistic_birth_date(year - np.random.randint(0, 100)),
                        np.random.choice(["M", "K"]),
                    )
                    for _ in range(num_records)
                ]
            )
        elif col_config["type"] == "date":
            data[col] = pl.Series(
                [
                    generate_realistic_birth_date(
                        np.random.randint(
                            col_config["start"].year, min(col_config["end"].year, year) + 1
                        )
                    )
                    for _ in range(num_records)
                ]
            )
        # Add other column types as needed

    return pl.DataFrame(data)


def generate_data(config, num_records, year, parent_birth_years=None):
    data = {}
    for col, col_config in config.items():
        data[col] = generate_column_data(col, col_config, num_records, year, parent_birth_years)

    # Add FAMILIE_ID if not present
    if "FAMILIE_ID" not in data:
        if "PNR" in data and "ALDER" in data and "CIVST" in data:
            data["FAMILIE_ID"] = pl.Series(
                [
                    get_or_create_familie_id(data["PNR"][i], data["ALDER"][i], data["CIVST"][i])
                    for i in range(num_records)
                ]
            ).cast(pl.Utf8)
        else:
            data["FAMILIE_ID"] = pl.Series(
                [generate_familie_id() for _ in range(num_records)]
            ).cast(pl.Utf8)

    df = pl.DataFrame(data)
    if df.is_empty():
        return pl.DataFrame({col: [] for col in config.keys()})
    return df


def generate_column_data(col, col_config, num_records, year, parent_birth_years):
    if col == "FOED_DAG" and parent_birth_years is not None:
        return generate_birth_dates(num_records, year)
    elif col == "HFAUDD" and parent_birth_years is not None:
        return generate_education_levels(parent_birth_years, year, num_records)
    elif col == "HF_VFRA" and parent_birth_years is not None:
        return generate_education_dates(parent_birth_years, year, num_records)
    elif col_config["type"] == "choice":
        return generate_choice_data(col_config, num_records)
    elif col_config["type"] == "int":
        return generate_int_data(col_config, num_records)
    elif col_config["type"] == "float":
        return generate_float_data(col_config, num_records)
    elif col_config["type"] == "date":
        return generate_date_data(col_config, num_records, year)
    elif col_config["type"] == "pnr":
        return generate_pnr_data(col_config, num_records, year)
    elif col_config["type"] == "string":
        return generate_string_data(col_config, num_records)
    else:
        raise ValueError(f"Unknown column type for {col}: {col_config['type']}")


def generate_birth_dates(num_records, year):
    return pl.Series(
        [
            datetime(year - np.random.randint(0, 5), 1, 1)
            + timedelta(days=np.random.randint(0, 365))
            for _ in range(num_records)
        ]
    ).cast(pl.Date)


def generate_education_levels(parent_birth_years, year, num_records):
    return pl.Series(
        [
            generate_education_level(parent_birth_year, year)
            for parent_birth_year in parent_birth_years[:num_records]
        ]
    ).cast(pl.Utf8)


def generate_education_dates(parent_birth_years, year, num_records):
    return pl.Series(
        [
            generate_education_date(parent_birth_year, year)
            for parent_birth_year in parent_birth_years[:num_records]
        ]
    ).cast(pl.Date)


def generate_choice_data(col_config, num_records):
    return pl.Series(np.random.choice(col_config["options"], num_records)).cast(pl.Utf8)


def generate_int_data(col_config, num_records):
    return pl.Series(np.random.randint(col_config["min"], col_config["max"], num_records)).cast(
        pl.Int64
    )


def generate_float_data(col_config, num_records):
    return pl.Series(np.random.normal(col_config["mean"], col_config["std"], num_records)).cast(
        pl.Float64
    )


def generate_date_data(col_config, num_records, year):
    start = max(col_config["start"], datetime(year, 1, 1))
    end = min(col_config["end"], datetime(year, 12, 31))
    if start >= end:
        return pl.Series([start] * num_records).cast(pl.Date)
    else:
        return pl.Series(
            [
                start + timedelta(seconds=np.random.randint(0, int((end - start).total_seconds())))
                for _ in range(num_records)
            ]
        ).cast(pl.Date)


def generate_pnr_data(col_config, num_records, year):
    return pl.Series(
        [
            get_or_create_pnr(
                datetime(year - np.random.randint(0, 100), 1, 1), np.random.choice(["M", "K"])
            )
            for _ in range(num_records)
        ]
    ).cast(pl.Utf8)


def generate_string_data(col_config, num_records):
    return pl.Series(
        [
            f"{col_config['prefix']}{np.random.randint(col_config['min'], col_config['max'])}"
            for _ in range(num_records)
        ]
    ).cast(pl.Utf8)


def generate_education_level(birth_year, current_year):
    age = current_year - birth_year
    if age < MINIMUM_EDUCATION_AGE:
        return "10"  # Basic school
    elif age < EARLY_EDUCATION_AGE:
        return np.random.choice(["10", "20", "30"], p=[0.3, 0.5, 0.2])
    elif age < YOUNG_ADULT_AGE:
        return np.random.choice(["20", "30", "35", "40"], p=[0.3, 0.3, 0.2, 0.2])
    else:
        return np.random.choice(
            ["20", "30", "35", "40", "50", "60", "70"], p=[0.1, 0.2, 0.2, 0.2, 0.15, 0.1, 0.05]
        )


def generate_education_date(birth_year, current_year):
    education_level = generate_education_level(birth_year, current_year)
    if education_level == "10":
        edu_year = birth_year + 16
    elif education_level in ["20", "30"]:
        edu_year = birth_year + np.random.randint(18, 22)
    elif education_level in ["35", "40"]:
        edu_year = birth_year + np.random.randint(21, 26)
    else:
        edu_year = birth_year + np.random.randint(24, 30)
    return datetime(min(edu_year, current_year), 1, 1) + timedelta(days=np.random.randint(0, 365))


def get_or_create_pnr(birth_date, gender):
    key = (birth_date, gender)
    if key not in PNR_CACHE:
        PNR_CACHE[key] = generate_pnr(birth_date, gender)
    return PNR_CACHE[key]


def generate_pnr(birth_date, gender):
    day = birth_date.day
    month = birth_date.month
    year = birth_date.year % 100
    century = birth_date.year // 100

    if century == CENTURY_18:
        seventh_digit = np.random.randint(5, 8)
    elif century == CENTURY_19:
        if birth_date.year < YEAR_1937:
            seventh_digit = np.random.randint(0, 4)
        else:
            seventh_digit = np.random.randint(4, 10)
    elif century == CENTURY_20:
        seventh_digit = np.random.randint(0, 4)
    else:  # 21st century
        seventh_digit = np.random.randint(4, 10)

    last_three_digits = np.random.randint(0, 999)
    last_digit = (
        last_three_digits
        if (gender == "K" and last_three_digits % 2 == 0)
        or (gender == "M" and last_three_digits % 2 == 1)
        else last_three_digits + 1
    )

    return f"{day:02d}{month:02d}{year:02d}-{seventh_digit}{last_digit:03d}"


def generate_familie_id(pnr=None, age=None, marital_status=None):
    if age is not None and marital_status is not None:
        if age >= MINIMUM_ADULT_AGE and marital_status in ["G", "P"]:  # Married or Partnership
            new_id = f"F{np.random.randint(1000000, 9999999):07d}"
            if pnr:
                FAMILIE_ID_CACHE[pnr] = new_id
            return new_id
        elif age < MINIMUM_ADULT_AGE or (age < YOUNG_ADULT_AGE and marital_status == "U"):
            return None  # Will be filled later with parents' FAMILIE_ID

    return f"F{np.random.randint(1000000, 9999999):07d}"


def get_or_create_familie_id(pnr, age, marital_status):
    if pnr not in FAMILIE_ID_CACHE:
        if age < YOUNG_ADULT_AGE and marital_status == "U":  # Unmarried and under 25
            # 80% chance to be part of parents' family
            if np.random.random() < PROB:
                FAMILIE_ID_CACHE[pnr] = None  # Will be filled later with parents' FAMILIE_ID
            else:
                FAMILIE_ID_CACHE[pnr] = generate_familie_id(pnr, age, marital_status)
        else:
            FAMILIE_ID_CACHE[pnr] = generate_familie_id(pnr, age, marital_status)
    return FAMILIE_ID_CACHE[pnr]


def update_familie_id(pnr, year, new_familie_id):
    if pnr not in FAMILIE_ID_HISTORY:
        FAMILIE_ID_HISTORY[pnr] = {}
    FAMILIE_ID_HISTORY[pnr][year] = new_familie_id


def get_familie_id(pnr, year):
    if pnr in FAMILIE_ID_HISTORY:
        return max((y, id) for y, id in FAMILIE_ID_HISTORY[pnr].items() if y <= year)[1]
    return None


def handle_family_change(pnr, year, event_type):
    if event_type in ["divorce", "death"]:
        new_familie_id = generate_familie_id(pnr, get_age(pnr, year), "U")
        update_familie_id(pnr, year, new_familie_id)
    elif event_type == "child_moving_out":
        if get_age(pnr, year) >= MINIMUM_ADULT_AGE:
            new_familie_id = generate_familie_id(pnr, get_age(pnr, year), "U")
            update_familie_id(pnr, year, new_familie_id)


def generate_shared_recnum(num_records):
    recnums = set()
    while len(recnums) < num_records:
        recnums.add(np.random.randint(1000000, 9999999))
    return pl.Series(list(recnums)).cast(pl.Int64)


def get_age(pnr, year):
    birth_year = int(pnr[4:6])
    birth_year += 1900 if birth_year >= 00 else 2000
    return year - birth_year


def generate_consistent_data(register_configs, num_records, year):
    # Generate BEF data first as it's the main demographic register
    bef_data = generate_data(register_configs["BEF"], num_records, year)
    if bef_data is None or bef_data.is_empty():
        print("Failed to generate BEF data. Aborting.")
        return {}

    # Generate parent birth years
    parent_birth_years = [
        year - np.random.randint(MINIMUM_PARENT_AGE, MAXIMUM_PARENT_AGE) for _ in range(num_records)
    ]

    # Use BEF data to generate consistent data for other registers
    data = {"BEF": bef_data}

    # Generate data for registers that require RECNUM
    recnum_registers = ["LPR_DIAG", "LPR_SKSOPR", "LPR_ADM"]
    shared_recnum = generate_shared_recnum(num_records)
    for register in recnum_registers:
        if register in register_configs:
            config = register_configs[register]
            register_data = generate_data(config, num_records, year)
            if register_data is not None and not register_data.is_empty():
                register_data = register_data.with_columns(
                    shared_recnum[: len(register_data)].alias("RECNUM")
                )
                data[register] = register_data

    # Generate data for other registers
    for register, config in register_configs.items():
        if register not in ["BEF"] + recnum_registers:
            if register == "UDDF":
                # Generate UDDF data for all individuals in BEF
                uddf_data = generate_data(
                    config, len(bef_data), year, parent_birth_years=parent_birth_years
                )
                if uddf_data is not None and not uddf_data.is_empty():
                    uddf_data = uddf_data.with_columns(bef_data["PNR"])
                    uddf_data = uddf_data.with_columns(
                        [
                            pl.when(pl.col("HF_VFRA") > pl.col("HF_VTIL"))
                            .then(pl.col("HF_VTIL"))
                            .otherwise(pl.col("HF_VFRA"))
                            .alias("HF_VFRA")
                        ]
                    )
                    data[register] = uddf_data
            else:
                register_data = generate_data(config, num_records, year)
                if register_data is not None and not register_data.is_empty():
                    if "PNR" in register_data.columns:
                        bef_pnrs = bef_data["PNR"].sample(
                            n=len(register_data), with_replacement=True
                        )
                        register_data = register_data.with_columns(bef_pnrs.alias("PNR"))
                    if "FAMILIE_ID" in register_data.columns:
                        bef_familie_ids = bef_data["FAMILIE_ID"].sample(
                            n=len(register_data), with_replacement=True
                        )
                        register_data = register_data.with_columns(
                            bef_familie_ids.alias("FAMILIE_ID")
                        )
                    data[register] = register_data

    return data


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic data for registers.")
    parser.add_argument("--force", action="store_true", help="Force regeneration of all data")
    parser.add_argument("--registers", nargs="+", help="Specific registers to process")
    parser.add_argument("--years", nargs="+", type=int, help="Specific years to process")
    args = parser.parse_args()

    base_dir = "data/generated"
    os.makedirs(base_dir, exist_ok=True)

    registers_to_process = args.registers if args.registers else register_configs.keys()

    for year in args.years if args.years else range(2000, 2024):
        logger.info(f"Generating data for year {year}")

        num_records = 1000  # Adjust as needed
        year_data = generate_consistent_data(register_configs, num_records, year)

        for register in registers_to_process:
            if register not in register_configs:
                logger.warning(f"Configuration for register '{register}' not found. Skipping.")
                continue

            if year not in register_periods.get(register, [year]):
                logger.info(
                    f"Skipping {register} for year {year} as it's not in the specified periods."
                )
                continue

            register_dir = os.path.join(base_dir, register.lower())
            os.makedirs(register_dir, exist_ok=True)

            file_name = f"{register.lower()}_{year}.parquet"
            file_path = os.path.join(register_dir, file_name)

            if args.force or not os.path.exists(file_path):
                # Save the data to a parquet file
                if (
                    register in year_data
                    and year_data[register] is not None
                    and not year_data[register].is_empty()
                ):
                    try:
                        year_data[register].write_parquet(file_path)
                        logger.info(f"Generated and saved {file_name}")
                    except Exception as e:
                        logger.error(f"Failed to write {file_name}. Error: {e!s}")
                else:
                    logger.warning(f"No data generated for {register} {year}. Skipping.")
            else:
                logger.info(f"Data for {register} {year} already exists. Skipping.")

    logger.info("Data generation complete.")


if __name__ == "__main__":
    main()

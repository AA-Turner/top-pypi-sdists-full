import logging
from collections.abc import Callable

import polars as pl


def check_required_columns(
    df: pl.LazyFrame | None, required_columns: list[str], data_name: str
) -> None:
    """
    Check if the DataFrame contains all required columns.

    Args:
        df (Optional[pl.LazyFrame]): The DataFrame to check.
        required_columns (List[str]): List of required column names.
        data_name (str): Name of the data source for logging purposes.

    Raises:
        ValueError: If df is None or if any required columns are missing.
    """
    if df is None:
        raise ValueError(f"{data_name} data is None")
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns in {data_name} data: {', '.join(missing_columns)}"
        )


def check_missing_values(
    df: pl.LazyFrame, table_name: str, logger: logging.Logger | None = None
) -> None:
    """
    Check for missing values in the DataFrame and log the results.

    Args:
        df (pl.LazyFrame): The LazyFrame to check for missing values.
        table_name (str): The name of the table being checked.
        logger (Optional[logging.Logger]): Logger to use for logging messages.

    Raises:
        ValueError: If the DataFrame is empty.
    """
    if df.select(pl.len()).collect().item() == 0:
        raise ValueError(f"The DataFrame for {table_name} is empty.")

    missing_counts = df.select(
        [pl.col(col).null_count().alias(f"{col}_null_count") for col in df.collect_schema().names()]
    ).collect()
    total_rows = df.select(pl.len()).collect().item()

    log_message(logger, f"Missing value report for {table_name}:", "info")
    for column, count in zip(df.collect_schema().names(), missing_counts.row(0), strict=False):
        if count > 0:
            percentage = (count / total_rows) * 100
            log_message(
                logger, f"  {column}: {count} missing values ({percentage:.2f}%)", "warning"
            )


def check_outliers(
    df: pl.LazyFrame,
    table_name: str,
    numeric_columns: dict[str, list[str]],
    logger: logging.Logger | None = None,
) -> None:
    if table_name not in numeric_columns:
        log_message(
            logger,
            f"No numeric columns defined for {table_name}, skipping outlier detection",
            "info",
        )
        return

    columns_to_check = numeric_columns[table_name]
    if not columns_to_check:
        log_message(logger, f"No numeric columns to check for {table_name}", "info")
        return

    available_columns = set(df.collect_schema().names())
    log_message(logger, f"Outlier report for {table_name}:", "info")
    for column in columns_to_check:
        if column not in available_columns:
            log_message(logger, f"Column {column} not found in {table_name}, skipping", "warning")
            continue

        try:
            col_type = df.collect_schema()[column]
            if col_type in [pl.Date, pl.Datetime]:
                log_message(logger, f"Skipping outlier detection for date column: {column}", "info")
                continue

            q1, q3 = (
                df.select(
                    [
                        pl.col(column).quantile(0.25).alias("q1"),
                        pl.col(column).quantile(0.75).alias("q3"),
                    ]
                )
                .collect()
                .row(0)
            )
            iqr = q3 - q1
            lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outliers = df.filter((pl.col(column) < lower_bound) | (pl.col(column) > upper_bound))
            outlier_count = outliers.select(pl.len()).collect().item()
            if outlier_count > 0:
                log_message(logger, f"  {column}: {outlier_count} outliers detected", "warning")
        except Exception as e:
            log_message(logger, f"Error checking outliers for column {column}: {e}", "error")


def check_logical_consistency(
    df: pl.LazyFrame,
    table_name: str,
    rules: dict[str, Callable[[pl.LazyFrame], pl.Expr]] | None = None,
    logger: logging.Logger | None = None,
) -> None:
    """
    Check logical consistency of the DataFrame based on provided rules and log the results.

    Args:
        df (pl.LazyFrame): The LazyFrame to check for logical consistency.
        table_name (str): The name of the table being checked.
        rules (Optional[Dict[str, Callable[[pl.LazyFrame], pl.Expr]]]): Dictionary of rule names and their corresponding check functions.
        logger (Optional[logging.Logger]): Logger to use for logging messages.
    """
    if rules is None:
        rules = {}
        # Example: Add some default rules for certain tables
        if table_name == "Person":
            rules["invalid_birth_dates"] = lambda df: pl.col("birth_date") > pl.date(2023, 1, 1)

    if not rules:
        log_message(logger, f"No consistency rules defined for {table_name}", "warning")
        return

    log_message(logger, f"Logical consistency report for {table_name}:", "info")
    for rule_name, rule_func in rules.items():
        try:
            inconsistent_count = df.filter(rule_func(df)).select(pl.len()).collect().item()
            if inconsistent_count > 0:
                log_message(
                    logger,
                    f"  {rule_name}: {inconsistent_count} inconsistencies detected",
                    "warning",
                )
        except Exception as e:
            log_message(logger, f"Error checking consistency rule '{rule_name}': {e}", "error")


def log_message(logger: logging.Logger | None, message: str, level: str = "info") -> None:
    """
    Logs a message using either the provided logger or the logging module.

    Args:
        logger (Optional[logging.Logger]): Logger to use for logging messages.
        message (str): The message to log.
        level (str): The logging level ('info', 'warning', 'error').
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    log_func = getattr(logger, level, logger.info)
    log_func(message)

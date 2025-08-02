import polars as pl

from ..config.config import Config
from ..utils.caching import cache_result
from ..utils.logger import setup_colored_logger

logger = setup_colored_logger(__name__)


@cache_result("cache")
def create_cohorts(
    tables: dict[str, pl.LazyFrame], config: Config, icd10_codes: dict[str, str]
) -> tuple[pl.LazyFrame, pl.LazyFrame]:
    severe_chronic_cases = identify_severe_chronic_cases(tables, icd10_codes)
    logger.info(
        f"Identified {severe_chronic_cases.select(pl.count()).collect().item()} severe chronic cases"
    )

    exposed_group = create_exposed_group(severe_chronic_cases, tables)
    logger.info(f"Created exposed group with schema: {exposed_group.collect_schema()}")

    unexposed_pool = create_unexposed_group(tables)
    logger.info(f"Created unexposed pool with schema: {unexposed_pool.collect_schema()}")

    exposed_cohort, unexposed_cohort = match_cohorts(exposed_group, unexposed_pool)

    logger.info(f"Exposed cohort schema: {exposed_cohort.collect_schema()}")
    logger.info(f"Unexposed cohort schema: {unexposed_cohort.collect_schema()}")

    logger.info(f"Identified {exposed_cohort.select(pl.count()).collect().item()} exposed children")
    logger.info(
        f"Identified {unexposed_cohort.select(pl.count()).collect().item()} unexposed children"
    )

    return exposed_cohort, unexposed_cohort


@cache_result("cache")
def identify_severe_chronic_cases(
    tables: dict[str, pl.LazyFrame], icd10_codes: dict[str, str]
) -> pl.LazyFrame:
    diagnosis_df = tables.get("Diagnosis")
    if diagnosis_df is None:
        raise ValueError("Diagnosis table not found")

    return diagnosis_df.filter(
        (pl.col("diagnosis_code").is_in(icd10_codes.keys()))
        & (pl.col("diagnosis_date").is_between(pl.date(2000, 1, 1), pl.date(2018, 12, 31)))
    )


@cache_result("cache")
def create_exposed_group(
    severe_chronic_cases: pl.LazyFrame, tables: dict[str, pl.LazyFrame | None]
) -> pl.LazyFrame:
    child_df = tables.get("Child")
    if child_df is None:
        logger.warning("Child table not found, using severe chronic cases as exposed group")
        return severe_chronic_cases.select(
            [
                pl.col("person_id").alias("child_id"),
                pl.col("diagnosis_date").alias("index_date"),
                pl.lit(None).cast(pl.Utf8).alias("family_id"),
            ]
        ).unique()

    available_columns = set(child_df.collect_schema().names())
    join_columns = []
    select_columns = []

    if "child_id" in available_columns:
        join_columns.append(("person_id", "child_id"))
        select_columns.append(pl.col("child_id"))
    else:
        logger.warning("'child_id' not found in Child table, using 'person_id' instead")
        join_columns.append(("person_id", "person_id"))
        select_columns.append(pl.col("person_id").alias("child_id"))

    if "family_id" in available_columns:
        select_columns.append(pl.col("family_id"))
    else:
        logger.warning("'family_id' not found in Child table, using null values")
        select_columns.append(pl.lit(None).cast(pl.Utf8).alias("family_id"))

    if "birth_date" in available_columns:
        join_condition = (pl.col("diagnosis_date") - pl.col("birth_date")) <= pl.duration(
            days=5 * 365
        )
    else:
        logger.warning("'birth_date' not found in Child table, not applying age filter")
        join_condition = pl.lit(True)

    exposed_children = severe_chronic_cases.join(
        child_df,
        left_on=[col[0] for col in join_columns],
        right_on=[col[1] for col in join_columns],
        how="left",
    ).filter(join_condition)

    select_columns.append(pl.col("diagnosis_date").alias("index_date"))

    return exposed_children.select(select_columns).unique()


@cache_result("cache")
def create_unexposed_group(tables: dict[str, pl.LazyFrame]) -> pl.LazyFrame:
    child_df = tables.get("Child")
    if child_df is None:
        raise ValueError("Child table not found")

    return (
        child_df.filter(pl.col("birth_date").is_between(pl.date(1995, 1, 1), pl.date(2018, 12, 31)))
        .select([pl.col("family_id"), pl.col("child_id"), pl.col("birth_date")])
        .unique()
    )


@cache_result("cache")
def match_cohorts(
    exposed_group: pl.LazyFrame, unexposed_pool: pl.LazyFrame
) -> tuple[pl.LazyFrame, pl.LazyFrame]:
    matched_unexposed = (
        exposed_group.join(
            unexposed_pool,
            on=["birth_date"],  # Add more matching criteria as needed
            how="left",
        )
        .filter(pl.col("family_id_right").is_not_null())
        .select(
            [
                pl.col("family_id_right").alias("family_id"),
                pl.col("child_id_right").alias("child_id"),
                pl.col("index_date"),
            ]
        )
    )

    return exposed_group, matched_unexposed

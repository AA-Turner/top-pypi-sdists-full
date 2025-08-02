import logging
from dataclasses import dataclass
from typing import Any

import polars as pl
from polars import Date, Float32, Float64, Int32, Utf8

from ..data.validation import check_required_columns

logger = logging.getLogger(__name__)


@dataclass
class DiagnosisData:
    lpr_diag: pl.LazyFrame | None
    lpr_adm: pl.LazyFrame | None
    priv_diag: pl.LazyFrame | None
    priv_adm: pl.LazyFrame | None
    psyk_diag: pl.LazyFrame | None
    psyk_adm: pl.LazyFrame | None


def create_table(
    df: pl.LazyFrame | None,
    columns: list[tuple[str, str, Any]],
    required_columns: list[str],
    data_name: str,
) -> pl.LazyFrame | None:
    """
    Create a table with specified columns from the input DataFrame.

    Args:
        df (Optional[pl.LazyFrame]): Input DataFrame.
        columns (List[Tuple[str, str, pl.DataType]]): List of (original_name, new_name, data_type) tuples.
        required_columns (List[str]): List of required column names.
        data_name (str): Name of the data source for logging purposes.

    Returns:
        Optional[pl.LazyFrame]: Created table, or None if input is None.

    Raises:
        ValueError: If required columns are missing.
    """
    if df is None:
        return None

    available_columns = set(df.collect_schema().names())
    missing_columns = set(required_columns) - available_columns
    if missing_columns:
        logger.warning(f"Missing columns in {data_name} data: {', '.join(missing_columns)}")

    valid_columns = [
        (orig, new, dtype) for orig, new, dtype in columns if orig in available_columns
    ]

    if not valid_columns:
        logger.warning(f"No valid columns found for {data_name} data")
        return None

    return df.select([pl.col(col[0]).alias(col[1]).cast(col[2]) for col in valid_columns])


def create_person_table(
    bef_data: pl.LazyFrame | None,
    dod_data: pl.LazyFrame | None,
    dodsaars_data: pl.LazyFrame | None,
    dodsaasg_data: pl.LazyFrame | None,
) -> pl.LazyFrame | None:
    if bef_data is None:
        return None

    # Get the available columns from bef_data
    available_columns = set(bef_data.collect_schema().names())

    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("FOED_DAG", "birth_date", Date),
        ("KOEN", "gender", Utf8),
    ]

    # Add optional columns if they are available
    optional_columns = [
        ("KOM", "municipality_code", Utf8),
        ("IE_TYPE", "origin_type", Utf8),
        ("STATSB", "citizenship", Utf8),
        ("OPR_LAND", "country_of_origin", Utf8),
        ("BOP_VFRA", "residence_start_date", Date),
        ("CIV_VFRA", "civil_status_date", Date),
        ("CIVST", "civil_status", Utf8),
        ("ALDER", "age", Int32),
        ("FAMILIE_ID", "family_id", Utf8),
        ("PLADS", "family_role", Utf8),
        ("MOR_ID", "mother_id", Utf8),
        ("FAR_ID", "father_id", Utf8),
        ("AEGTE_ID", "spouse_id", Utf8),
        ("FAMILIE_TYPE", "family_type", Utf8),
        ("ANTPERSF", "family_size", Int32),
        ("ANTBOERNF", "number_of_children", Int32),
        ("HUSTYPE", "household_type", Utf8),
    ]

    for col in optional_columns:
        if col[0] in available_columns:
            columns.append(col)

    required_columns = [col[0] for col in columns]
    person_table = create_table(bef_data, columns, required_columns, "BEF")

    if (
        person_table is not None
        and dod_data is not None
        and dodsaars_data is not None
        and dodsaasg_data is not None
    ):
        death_columns: list[tuple[str, str, Any]] = [
            ("PNR", "person_id", Utf8),
            ("DODDATO", "death_date", Date),
        ]

        # Add optional death-related columns if they are available
        optional_death_columns = [
            ("C_DODSMAADE", "death_manner", Utf8),
            ("C_DOD1", "primary_cause", Utf8),
            ("C_DOD2", "secondary_cause1", Utf8),
            ("C_DOD3", "secondary_cause2", Utf8),
            ("C_DOD4", "secondary_cause3", Utf8),
            ("C_DODTILGRUNDL_ACME", "underlying_cause", Utf8),
        ]

        for col in optional_death_columns:
            if (
                col[0] in dod_data.collect_schema().names()
                or col[0] in dodsaars_data.collect_schema().names()
                or col[0] in dodsaasg_data.collect_schema().names()
            ):
                death_columns.append(col)

        death_required_columns = [col[0] for col in death_columns]

        combined_death_data = dod_data.join(dodsaars_data, on="PNR", how="outer").join(
            dodsaasg_data, on="PNR", how="outer"
        )

        death_table = create_table(
            combined_death_data, death_columns, death_required_columns, "Death"
        )

        if death_table is not None:
            person_table = person_table.join(death_table, on="person_id", how="left")

    return person_table


def create_birth_table(ftbarn_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    columns: list[tuple[str, str, Any]] = [
        ("PNR", "child_id", Utf8),
        ("FOED_DAG", "birth_date", Date),
        ("KOEN", "gender", Utf8),
        ("VAEGT_BARN", "birth_weight", Float32),
        ("LAENGDE_BARN", "birth_length", Float32),
        ("MOR1", "mother_id", Utf8),
        ("FAR1", "father_id", Utf8),
        ("MOR_ALDER", "mother_age", Int32),
        ("FAR_ALDER", "father_age", Int32),
        ("FLERFOLD", "multiple_birth", Utf8),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(ftbarn_data, columns, required_columns, "FTBARN")


def create_disability_table(handic_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("FUNK_VURD", "functional_assessment", Utf8),
        ("MAAL_KEY", "target_group_key", Utf8),
        ("MODT_YDELSE_KODE", "service_code", Utf8),
        ("YDELSE_START", "service_start_date", Date),
        ("YDELSE_SLUT", "service_end_date", Date),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(handic_data, columns, required_columns, "HANDIC")


def create_child_table(mfr_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    if mfr_data is None:
        logger.error("MFR data is missing, cannot create Child table")
        return None

    columns: list[tuple[str, str, Any]] = [
        ("CPR_BARN", "child_id", Utf8),
        ("FAMILIE_ID", "family_id", Utf8),
        ("FOEDSELSDATO", "birth_date", Date),
        ("KOEN_BARN", "gender", Utf8),
        ("VAEGT_BARN", "birth_weight", Float32),
        ("LAENGDE_BARN", "birth_length", Float32),
        ("GESTATIONSALDER_BARN", "gestational_age", Int32),
    ]
    required_columns = [col[0] for col in columns]
    child_table = create_table(mfr_data, columns, required_columns, "MFR")

    if child_table is not None:
        logger.info(
            f"Created Child table with {child_table.select(pl.count()).collect().item()} rows"
        )
    else:
        logger.error("Failed to create Child table")

    return child_table


def link_children_to_parents(child_table: pl.LazyFrame, person_table: pl.LazyFrame) -> pl.LazyFrame:
    return child_table.join(
        person_table.select(["person_id", "mother_id", "father_id"]),
        left_on="child_id",
        right_on="person_id",
    )


def prepare_income_data(
    income_table: pl.LazyFrame, parent_child_links: pl.LazyFrame
) -> pl.LazyFrame:
    return (
        income_table.join(
            parent_child_links,
            left_on="person_id",
            right_on=["mother_id", "father_id"],
            how="inner",
        )
        .group_by(["child_id", "year"])
        .agg([pl.col("total_income").sum().alias("parental_total_income")])
    )


def create_diagnosis_table(data: DiagnosisData) -> pl.LazyFrame | None:
    if all(df is None for df in [data.lpr_diag, data.priv_diag, data.psyk_diag]):
        logger.warning("All diagnosis data sources are missing")
        return None

    dfs = []

    if data.lpr_diag is not None and data.lpr_adm is not None:
        lpr = data.lpr_diag.join(data.lpr_adm, on="RECNUM", how="inner")
        dfs.append(lpr)

    if data.priv_diag is not None and data.priv_adm is not None:
        priv = data.priv_diag.join(data.priv_adm, on="RECNUM", how="inner")
        dfs.append(priv)

    if data.psyk_diag is not None and data.psyk_adm is not None:
        psyk = data.psyk_diag.join(data.psyk_adm, on="RECNUM", how="inner")
        dfs.append(psyk)

    if not dfs:
        logger.warning("No valid diagnosis data combinations found")
        return None

    combined_data = pl.concat(dfs)

    columns: list[tuple[str, str, Any]] = [
        ("RECNUM", "diagnosis_id", Utf8),
        ("PNR", "person_id", Utf8),
        ("C_DIAG", "diagnosis_code", Utf8),
        ("C_DIAGTYPE", "diagnosis_type", Utf8),
        ("D_INDDTO", "diagnosis_date", Date),
        ("C_AFD", "hospital_department", Utf8),
        ("C_SGH", "hospital_code", Utf8),
        ("C_SPEC", "speciality", Utf8),
        ("C_PATTYPE", "patient_type", Utf8),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(combined_data, columns, required_columns, "Diagnosis")


def create_employment_table(
    ind_data: pl.LazyFrame | None, idan_data: pl.LazyFrame | None, akm_data: pl.LazyFrame | None
) -> pl.LazyFrame | None:
    if ind_data is None or idan_data is None or akm_data is None:
        logger.warning("One or more required data sources for employment table are missing")
        return None

    # Join data from different registers
    combined_data = ind_data.join(idan_data, on="PNR", how="outer").join(
        akm_data, on="PNR", how="outer"
    )

    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("ARBGNR", "employer_id", Utf8),
        ("ARBNR", "workplace_id", Utf8),
        ("STILL", "job_type", Utf8),
        ("SOCIO13", "socioeconomic_status", Utf8),
        ("year", "year", Int32),
        ("JOBKAT", "job_category", Utf8),
        ("JOBLON", "job_salary", Float64),
        ("CVRNR", "company_cvr", Utf8),
        ("LOENMV_13", "wage_income", Float64),
        ("PERINDKIALT_13", "total_income", Float64),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(combined_data, columns, required_columns, "Employment")


def create_education_table(uddf_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    if uddf_data is None:
        return None

    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("HFAUDD", "education_code", Utf8),
        ("HF_VFRA", "education_start_date", Date),
        ("HF_VTIL", "education_end_date", Date),
        ("INSTNR", "institution_code", Utf8),
        ("year", "data_year", Int32),
    ]
    required_columns = [col[0] for col in columns]

    uddf_table = create_table(uddf_data, columns, required_columns, "UDDF")

    if uddf_table is not None:
        # Sort by person_id and education_end_date to get the latest education for each person
        uddf_table = uddf_table.sort(["person_id", "education_end_date"], descending=[False, True])

        # Keep only the latest education record for each person
        uddf_table = uddf_table.group_by("person_id").agg([pl.all().first()])

    return uddf_table


def create_education_details_table(udfk_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("FAGKODE", "subject_code", Utf8),
        ("KLASSETYPE", "class_type", Utf8),
        ("KLTRIN", "grade_level", Utf8),
        ("SKOLEAAR", "school_year", Utf8),
        ("GRUNDSKOLEKARAKTER", "grade", Float32),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(udfk_data, columns, required_columns, "UDFK")


def create_migration_table(vnds_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("HAEND_DATO", "event_date", Date),
        ("INDUD_KODE", "migration_code", Utf8),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(vnds_data, columns, required_columns, "VNDS")


def create_medication_table(lmdb_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    columns: list[tuple[str, str, Any]] = [
        ("PNR12", "person_id", Utf8),
        ("ATC", "atc_code", Utf8),
        ("EKSD", "prescription_date", Date),
        ("VOLUMEN", "volume", Float32),
        ("STYRKE", "strength", Float32),
        ("PAKSTR", "package_size", Int32),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(lmdb_data, columns, required_columns, "LMDB")


def create_healthcare_table(
    lpr_adm: pl.LazyFrame | None,
    priv_adm: pl.LazyFrame | None,
    psyk_adm: pl.LazyFrame | None,
    lpr_sksopr: pl.LazyFrame | None,
    priv_sksopr: pl.LazyFrame | None,
) -> pl.LazyFrame | None:
    if all(df is None for df in [lpr_adm, priv_adm, psyk_adm]):
        logger.warning("All healthcare data sources are missing")
        return None

    dfs = []

    if lpr_adm is not None:
        dfs.append(lpr_adm)

    if priv_adm is not None:
        dfs.append(priv_adm)

    if psyk_adm is not None:
        dfs.append(psyk_adm)

    combined_data = pl.concat(dfs)

    if lpr_sksopr is not None:
        combined_data = combined_data.join(lpr_sksopr, on="RECNUM", how="left")

    if priv_sksopr is not None:
        combined_data = combined_data.join(priv_sksopr, on="RECNUM", how="left")

    columns: list[tuple[str, str, Any]] = [
        ("RECNUM", "event_id", Utf8),
        ("PNR", "person_id", Utf8),
        ("D_INDDTO", "admission_date", Date),
        ("D_UDDTO", "discharge_date", Date),
        ("C_PATTYPE", "patient_type", Utf8),
        ("C_KONTAARS", "contact_reason", Utf8),
        ("C_SPEC", "speciality", Utf8),
        ("V_SENGDAGE", "bed_days", Int32),
        ("C_SGH", "hospital_code", Utf8),
        ("C_AFD", "department_code", Utf8),
        ("C_OPR", "procedure_code", Utf8),
        ("D_ODTO", "procedure_date", Date),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(combined_data, columns, required_columns, "Healthcare")


def create_time_table(start_year: int, end_year: int) -> pl.LazyFrame:
    """
    Create a time dimension table.

    Args:
        start_year (int): Start year of the time range.
        end_year (int): End year of the time range.

    Returns:
        pl.LazyFrame: Time dimension table.
    """
    dates = pl.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31", interval="1d")
    return pl.DataFrame(
        {
            "date": dates,
            "year": dates.dt.year(),
            "month": dates.dt.month(),
            "quarter": dates.dt.quarter(),
            "is_pre_treatment": pl.lit(True),
        }
    ).lazy()


def create_socioeconomic_status_table(
    ind_data: pl.LazyFrame | None, uddf_data: pl.LazyFrame | None
) -> pl.LazyFrame | None:
    if ind_data is None:
        return None
    columns: list[tuple[str, str, Any]] = [
        ("FAMILIE_ID", "family_id", Utf8),
        ("year", "year", Int32),
        ("SOCIO13", "socioeconomic_status", Utf8),
        ("PERINDKIALT_13", "total_income", Float64),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(ind_data, columns, required_columns, "IND")


def create_treatment_period_table(
    diagnosis_df: pl.LazyFrame | None, child_df: pl.LazyFrame | None
) -> pl.LazyFrame | None:
    if diagnosis_df is None or child_df is None:
        return None
    check_required_columns(diagnosis_df, ["person_id", "diagnosis_date"], "Diagnosis")
    check_required_columns(child_df, ["child_id", "family_id"], "Child")

    return diagnosis_df.join(child_df, left_on="person_id", right_on="child_id").select(
        [
            pl.col("family_id").cast(Utf8),
            pl.col("diagnosis_date").alias("treatment_start_date").cast(Date),
            (pl.col("diagnosis_date") - pl.duration(days=365))
            .alias("pre_treatment_start")
            .cast(Date),
            pl.col("diagnosis_date").alias("pre_treatment_end").cast(Date),
            (pl.col("diagnosis_date") + pl.duration(days=365 * 5))
            .alias("post_treatment_end")
            .cast(Date),
        ]
    )


def create_person_child_table(
    bef_data: pl.LazyFrame | None, child_df: pl.LazyFrame | None
) -> pl.LazyFrame | None:
    if bef_data is None or child_df is None:
        return None
    check_required_columns(bef_data, ["PNR", "FM_MARK"], "BEF")
    check_required_columns(child_df, ["child_id"], "Child")

    return bef_data.join(child_df, left_on="PNR", right_on="child_id").select(
        [
            pl.col("PNR").alias("person_id").cast(Utf8),
            pl.col("child_id").cast(Utf8),
            pl.col("FM_MARK").alias("relationship_type").cast(Utf8),
        ]
    )


def create_person_family_table(
    bef_data: pl.LazyFrame | None, family_df: pl.LazyFrame | None
) -> pl.LazyFrame | None:
    if bef_data is None or family_df is None:
        return None
    check_required_columns(bef_data, ["PNR", "FAMILIE_ID", "PLADS"], "BEF")
    check_required_columns(family_df, ["family_id"], "Family")

    return bef_data.join(family_df, left_on="FAMILIE_ID", right_on="family_id").select(
        [
            pl.col("PNR").alias("person_id").cast(Utf8),
            pl.col("FAMILIE_ID").alias("family_id").cast(Utf8),
            pl.col("PLADS").alias("role").cast(Utf8),
        ]
    )


def create_person_year_income_table(ind_data: pl.LazyFrame | None) -> pl.LazyFrame | None:
    columns: list[tuple[str, str, Any]] = [
        ("PNR", "person_id", Utf8),
        ("year", "year", Int32),
        ("PERINDKIALT_13", "total_income", Float64),
        ("LOENMV_13", "wage_income", Float64),
        ("ERHVERVSINDK_13", "business_income", Float64),
    ]
    required_columns = [col[0] for col in columns]
    return create_table(ind_data, columns, required_columns, "IND")

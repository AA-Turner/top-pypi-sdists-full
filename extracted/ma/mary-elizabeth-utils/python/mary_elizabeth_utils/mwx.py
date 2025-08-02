import csv
import logging
from pathlib import Path

import polars as pl
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Configure rich logging
logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("rich")


class Config:
    def __init__(self):
        self.DATA_DIR = Path("data/generated")
        self.ICD10_CODES_FILE = Path("data/icd10.csv")
        self.START_YEAR = 2000
        self.END_YEAR = 2018
        self.MAX_AGE = 5


def load_icd10_codes(config: Config) -> dict[str, str]:
    icd10_codes = {}
    file_path = config.ICD10_CODES_FILE
    logger.debug(f"Loading ICD10 codes from: {file_path}")
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            codes = row["ICD10-codes"].split(";")
            for code_item in codes:
                code = code_item.strip()
                if "-" in code:
                    start, end = code.split("-")
                    icd10_codes[start] = row["Diagnoses"]
                    icd10_codes[end] = row["Diagnoses"]
                else:
                    icd10_codes[code] = row["Diagnoses"]
    return icd10_codes


def load_register_data(base_path: Path, register_name: str, years: list[int]) -> pl.LazyFrame:
    dfs = []
    for year in years:
        file_path = base_path / register_name.lower() / f"{register_name.lower()}_{year}.parquet"
        if file_path.exists():
            df = pl.scan_parquet(file_path)
            df = df.with_columns(pl.lit(year).alias("year"))
            dfs.append(df)
    return pl.concat(dfs)


def preprocess_data(config: Config) -> dict[str, pl.LazyFrame]:
    years = list(range(config.START_YEAR, config.END_YEAR + 1))

    data = {
        "BEF": load_register_data(config.DATA_DIR, "bef", years),
        "LPR_DIAG": load_register_data(config.DATA_DIR, "lpr_diag", years),
        "LPR_ADM": load_register_data(config.DATA_DIR, "lpr_adm", years),
        "MFR": load_register_data(config.DATA_DIR, "mfr", years),
        "UDDF": load_register_data(
            config.DATA_DIR, "uddf", [2022]
        ),  # Load only the latest UDDF data
    }

    return data


def identify_children(
    bef_data: pl.LazyFrame, mfr_data: pl.LazyFrame, config: Config
) -> pl.LazyFrame:
    child_data = (
        bef_data.join(mfr_data, left_on="PNR", right_on="CPR_BARN")
        .filter(
            (
                pl.col("FOED_DAG")
                .dt.year()
                .is_between(config.START_YEAR - config.MAX_AGE, config.END_YEAR)
            )
            & (pl.col("FOED_DAG").dt.year() + pl.col("ALDER") >= config.START_YEAR)
            & (pl.col("FOED_DAG").dt.year() + pl.col("ALDER") <= config.END_YEAR)
        )
        .select(["PNR", "FOED_DAG", "KOEN", "MOR_ID", "FAR_ID"])
    )
    return child_data


def prepare_education_data(uddf_data: pl.LazyFrame) -> pl.LazyFrame:
    return (
        uddf_data.sort(["PNR", "HF_VFRA"], descending=[False, True])
        .group_by("PNR")
        .agg([pl.col("HFAUDD").first().alias("HFAUDD"), pl.col("HF_VFRA").first().alias("HF_VFRA")])
    )


def get_education_at_birth(
    birth_date: pl.Expr, education_dates: pl.Expr, education_levels: pl.Expr
) -> pl.Expr:
    return (
        pl.when(education_dates.is_not_null() & education_levels.is_not_null())
        .then(
            education_levels.list.eval(
                pl.element().filter(pl.element().cast(pl.Date) <= birth_date)
            )
            .list.first()
            .fill_null("Unknown")
        )
        .otherwise("Unknown")
    )


def link_parent_education(
    child_data: pl.LazyFrame, education_data: pl.LazyFrame, parent_id_col: str, result_col: str
) -> pl.LazyFrame:
    joined_data = child_data.join(education_data, left_on=parent_id_col, right_on="PNR", how="left")

    return joined_data.with_columns(
        [
            pl.when(pl.col("HFAUDD").is_null() | pl.col("HF_VFRA").is_null())
            .then(pl.lit("Unknown"))
            .otherwise(
                pl.when(pl.col("HF_VFRA") <= pl.col("FOED_DAG"))
                .then(pl.col("HFAUDD"))
                .otherwise(pl.lit("Unknown"))
            )
            .alias(result_col)
        ]
    ).drop(["HFAUDD", "HF_VFRA"])


def link_children_to_parents(
    child_data: pl.LazyFrame, bef_data: pl.LazyFrame, uddf_data: pl.LazyFrame
) -> pl.LazyFrame:
    education_data = prepare_education_data(uddf_data)

    # Link mother's education
    children_with_mother_edu = link_parent_education(
        child_data, education_data, "MOR_ID", "MOR_UDDANNELSE"
    )

    # Link father's education
    children_with_parents_edu = link_parent_education(
        children_with_mother_edu, education_data, "FAR_ID", "FAR_UDDANNELSE"
    )

    return children_with_parents_edu


def link_children_to_health_records(
    child_data: pl.LazyFrame, lpr_diag_data: pl.LazyFrame, lpr_adm_data: pl.LazyFrame
) -> pl.LazyFrame:
    # Join LPR_DIAG with LPR_ADM
    lpr_combined = lpr_diag_data.join(lpr_adm_data, on="RECNUM")

    # Now join the combined LPR data with child data
    return child_data.join(lpr_combined, on="PNR")


def create_exposed_unexposed_groups(
    linked_data: pl.LazyFrame, icd_codes: dict[str, str]
) -> tuple[pl.LazyFrame, pl.LazyFrame]:
    exposed = linked_data.filter(pl.col("C_DIAG").is_in(icd_codes.keys()))
    unexposed = linked_data.filter(~pl.col("C_DIAG").is_in(icd_codes.keys()))
    return exposed, unexposed


def main():
    config = Config()

    with console.status("[bold green]Loading ICD10 codes...") as status:
        icd_codes = load_icd10_codes(config)
        status.update("[bold green]ICD10 codes loaded successfully")

    try:
        with console.status("[bold green]Preprocessing data...") as status:
            data = preprocess_data(config)
            status.update("[bold green]Data preprocessing completed")
    except Exception as e:
        logger.error(f"[bold red]Error during data preprocessing: {e}")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task("[cyan]Identifying children...", total=None)
        child_data = identify_children(data["BEF"], data["MFR"], config)
        progress.update(task1, completed=True)

        task2 = progress.add_task("[cyan]Preparing education data...", total=None)
        education_data = prepare_education_data(data["UDDF"])
        progress.update(task2, completed=True)

        task3 = progress.add_task("[cyan]Linking parents' education...", total=None)
        try:
            children_with_mother_edu = link_parent_education(
                child_data, education_data, "MOR_ID", "MOR_UDDANNELSE"
            )
            children_with_parents = link_parent_education(
                children_with_mother_edu, education_data, "FAR_ID", "FAR_UDDANNELSE"
            )
            progress.update(task3, completed=True)
        except Exception as e:
            logger.error(f"[bold red]Error when linking parents' education: {e}")
            console.print_exception(show_locals=True)
            return

        task4 = progress.add_task("[cyan]Linking children to health records...", total=None)
        children_with_health_records = link_children_to_health_records(
            children_with_parents, data["LPR_DIAG"], data["LPR_ADM"]
        )
        progress.update(task4, completed=True)

        task5 = progress.add_task("[cyan]Creating exposed and unexposed groups...", total=None)
        exposed_group, unexposed_group = create_exposed_unexposed_groups(
            children_with_health_records, icd_codes
        )
        progress.update(task5, completed=True)

    console.print("\n[bold green]Results:")

    total_children = child_data.select(pl.n_unique("PNR")).collect().item()
    console.print(f"Total eligible children: {total_children}")

    try:
        exposed_count = exposed_group.select(pl.n_unique("PNR")).collect().item()
        console.print(f"Children in exposed group: {exposed_count}")
    except Exception as e:
        logger.error(f"[bold red]Error calculating exposed group: {e}")
        console.print("[yellow]Exposed group count unavailable")

    try:
        unexposed_count = unexposed_group.select(pl.n_unique("PNR")).collect().item()
        console.print(f"Children in unexposed group: {unexposed_count}")
    except Exception as e:
        logger.error(f"[bold red]Error calculating unexposed group: {e}")
        console.print("[yellow]Unexposed group count unavailable")

    # Debug information
    console.print("\n[bold cyan]Debug Information:")
    console.print(f"ICD Codes count: {len(icd_codes)}")
    console.print("Children with health records schema:")
    console.print(children_with_health_records.schema)

    # Sample data from children_with_health_records
    sample_data = children_with_health_records.limit(5).collect()
    console.print("\nSample data from children_with_health_records:")
    console.print(sample_data)


if __name__ == "__main__":
    main()

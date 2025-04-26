#!/usr/bin/env python3
"""
Alacorder collects case detail PDFs from Alacourt.com and processes them into data
tables suitable for research purposes.
"""

import locale
import multiprocessing
import re
import time
from contextlib import suppress
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from threading import Thread
from typing import Annotated, Any, ClassVar, Optional, cast

import bs4
import fitz
import polars as pl
import typer
import xlsxwriter
from docxtpl import DocxTemplate
from rich.console import Console
from rich.progress import MofNCompleteColumn, Progress
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    RadioButton,
    RadioSet,
    SelectionList,
    Static,
    TabbedContent,
)
from textual.widgets import Select as SelectWidget

try:
    __version__ = version("alacorder")
except PackageNotFoundError:
    __version__ = ""

# Configure polars.
pl.Config.set_fmt_str_lengths(100)
pl.Config.set_tbl_formatting("NOTHING")
pl.Config.set_tbl_dataframe_shape_below(active=True)
pl.Config.set_tbl_hide_column_data_types(active=True)

console = Console()
app = typer.Typer(
    help=(
        "Alacorder collects case detail PDFs from Alacourt.com and "
        "processes them into data tables suitable for research purposes."
    ),
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    add_completion=False,
)


class BadFileError(Exception):
    """Raised when a bad path is given."""


class InvalidAlacourtCredentialsError(Exception):
    """Raised when Alacourt login fails."""


class ConfigurationError(Exception):
    """Raised when class is not configured for attempted use case."""


class WrongPageError(Exception):
    """Raised when page cannot be read because it has not been navigated to."""


def write(
    output: dict[str, pl.DataFrame] | pl.DataFrame,
    path: str | Path,
    *,
    log: bool = False,
) -> None:
    """
    Write each value in `output` dict {'name': pl.DataFrame} to path. If
    exporting multiple tables, extension must be .xlsx. Otherwise,
    write() supports .xlsx, .csv, .json, and .parquet.
    """

    def _write(
        output: dict[str, pl.DataFrame] | pl.DataFrame, path: str | Path
    ) -> None:
        if isinstance(output, pl.DataFrame):
            output = {"table": output}
        if isinstance(path, str):
            path = Path(path)
        if isinstance(path, Path):
            path = path.resolve()
        if len(output) > 1 and path.suffix != ".xlsx":
            msg = "Multitable export must write to .xlsx."
            raise BadFileError(msg)
        if path.suffix not in (".xlsx", ".csv", ".json", ".parquet"):
            msg = (
                "Unsupported output file extension. Repeat with .csv,"
                " .json, or .parquet output file."
            )
            raise BadFileError(msg)
        if path.suffix == ".xlsx":
            with xlsxwriter.Workbook(path) as workbook:
                for sheet in output:
                    output[sheet].write_excel(
                        workbook=workbook,
                        worksheet=sheet,
                        autofit=True,
                        float_precision=2,
                    )
        if path.suffix in (".parquet", ".json", ".csv"):
            output_df = next(iter(output.values()))
            if path.suffix == ".parquet":
                output_df.write_parquet(path, compression="brotli")
            if path.suffix == ".json":
                output_df.write_json(path)
            if path.suffix == ".csv":
                output_df.write_csv(path)
        return None

    if log:
        with console.status("Writing to output path…"):
            _write(output, path)
    else:
        _write(output, path)
    return None


def extract_text(path: str | Path) -> str:
    """From path, return full text of PDF as string."""
    try:
        doc = fitz.open(path)
    except (FileNotFoundError, fitz.FileDataError):
        return ""
    text = ""
    for pg in doc:
        text += " \n ".join(
            x[4].replace("\n", " ") for x in pg.get_text(option="blocks")
        )
    return re.sub(r"(<image\:.+?>)", "", text).strip()


def read(
    source: str | list[str | Path] | Path | pl.DataFrame, *, all_sheets: bool = False
) -> pl.DataFrame | dict[str, pl.DataFrame] | str:
    """Read input into pl.DataFrame. If directory, reads PDFs into archive df."""

    output: pl.DataFrame | dict[str, pl.DataFrame] | str | Path

    if isinstance(source, str):
        source = Path(source)
    if isinstance(source, Path):
        source = source.resolve()
        if not source.exists():
            msg = "No file at provided path."
            raise BadFileError(msg)
        if source.is_file():
            match source.suffix:
                case ".xlsx":
                    if all_sheets:
                        output = pl.read_excel(
                            source,
                            sheet_id=0,
                            engine_options={"ignore_errors": True},
                            read_options={
                                "dtypes": {
                                    "AIS / Unique ID": pl.Utf8,
                                    "AIS": pl.Utf8,
                                }
                            },
                        )
                    else:
                        output = pl.read_excel(
                            source,
                            engine_options={"ignore_errors": True},
                            read_options={
                                "dtypes": {
                                    "AIS / Unique ID": pl.Utf8,
                                    "AIS": pl.Utf8,
                                }
                            },
                        )
                case ".json":
                    output = pl.read_json(source)
                case ".csv":
                    output = pl.read_csv(
                        source,
                        ignore_errors=True,
                        dtypes={
                            "AIS / Unique ID": pl.Utf8,
                            "AIS": pl.Utf8,
                        },
                    )
                case ".parquet":
                    output = pl.read_parquet(source)
                case ".txt":
                    with source.open() as file:
                        output = file.read()
                case ".pdf":
                    output = extract_text(source)
                case _:
                    msg = "File extension not supported."
                    raise BadFileError(msg)
        elif source.is_dir():
            paths: list[str] = [str(path) for path in source.rglob("**/*.pdf")]
            all_text = []
            progress_bar = Progress(
                *Progress.get_default_columns(), MofNCompleteColumn()
            )
            with progress_bar as bar, multiprocessing.Pool() as pool:
                for text in bar.track(
                    pool.imap(extract_text, paths),
                    description="Reading PDFs…",
                    total=len(paths),
                ):
                    all_text.append(text)  # noqa: PERF402
            output = pl.DataFrame(
                {"Timestamp": time.time(), "AllPagesText": all_text, "Path": paths}
            )
    if isinstance(source, list):
        source = [Path(path).resolve() for path in source]
        all_text = []
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as bar, multiprocessing.Pool() as pool:
            for text in bar.track(
                pool.imap(extract_text, source),
                description="Reading PDFs…",
                total=len(source),
            ):
                all_text += [text]
        output = pl.DataFrame(
            {"Timestamp": time.time(), "AllPagesText": all_text, "Path": source}
        )
    if isinstance(source, pl.DataFrame):
        output = source
    if isinstance(output, pl.DataFrame):
        if "CaseNumber" not in output.columns and "AllPagesText" in output.columns:
            output = output.with_columns(
                pl.concat_str(
                    [
                        pl.col("AllPagesText").str.extract(
                            r"(County: )(\d{2})", group_index=2
                        ),
                        pl.lit("-"),
                        pl.col("AllPagesText").str.extract(
                            r"(\w{2}\-\d{4}\-\d{6}\.\d{2})"
                        ),
                    ]
                ).alias("CaseNumber")
            )
        if "AllPagesText" in output.columns and "CaseNumber" in output.columns:
            output = output.unique("CaseNumber")
    assert not isinstance(output, Path)
    return output


class AlacourtDriver:
    """
    Automates Alacourt party search results and case PDF retrieval. Initialize
    with path to download directory, then call login() before searching.
    """

    # config
    def __init__(
        self: "AlacourtDriver",
        source_path: str | Path | None = None,
        *,
        headless: bool = True,
        customer_id: str | None = None,
        user_id: str | None = None,
        password: str | None = None,
    ) -> None:
        """
        Create AlacourtDriver object from download directory path and
        Alacourt credentials.
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        if source_path is not None:
            if isinstance(source_path, str):
                source_path = Path(source_path)
            if isinstance(source_path, Path):
                source_path = source_path.resolve()
            options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": str(source_path),
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True,
                },
            )
        else:
            options.add_experimental_option(
                "prefs",
                {
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True,
                },
            )
        with console.status("Starting WebDriver (requires Google Chrome)…"):
            self.driver = webdriver.Chrome(options=options)
        self.source_path: Path | None = source_path
        self.headless = headless
        self.party_search_queue: pl.DataFrame | None = None
        self.case_number_queue: pl.DataFrame | None = None
        self.party_search_queue_path: Path | None = None
        self.case_number_queue_path: Path | None = None
        self.output: Path | None = None
        self.cID = customer_id
        self.uID = user_id
        self.pwd = password
        if customer_id is not None and user_id is not None and password is not None:
            self.login(customer_id, user_id, password)

    def login(
        self: "AlacourtDriver",
        customer_id: str | None = None,
        user_id: str | None = None,
        password: str | None = None,
        *,
        log: bool = True,
    ) -> bool:
        """Login to Alacourt using provided credentials."""

        def _login(
            driver: webdriver.chrome.webdriver.WebDriver,
            customer_id: str,
            user_id: str,
            password: str,
        ) -> bool:
            driver.get("https://v2.alacourt.com")
            customer_id_box = driver.find_element(By.ID, "ContentPlaceHolder_txtCusid")
            user_id_box = driver.find_element(By.ID, "ContentPlaceHolder_txtUserId")
            pwd_box = driver.find_element(By.ID, "ContentPlaceHolder_txtPassword")
            login_button = driver.find_element(By.ID, "ContentPlaceHolder_btLogin")
            customer_id_box.send_keys(customer_id)
            user_id_box.send_keys(user_id)
            pwd_box.send_keys(password)
            login_button.click()
            WebDriverWait(driver, 5).until(EC.staleness_of(login_button))
            continue_button = driver.find_elements(
                By.ID, "ContentPlaceHolder_btnContinueLogin"
            )
            if len(continue_button) > 0:
                continue_button[0].click()
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "btnLogOff"))
                )
            except Exception as exc:
                msg = "Invalid Alacourt credentials."
                raise InvalidAlacourtCredentialsError(msg) from exc
            return True

        if customer_id is not None:
            self.cID = customer_id
        if user_id is not None:
            self.uID = user_id
        if password is not None:
            self.pwd = password

        if self.cID is None or self.uID is None or self.pwd is None:
            msg = "Must enter Alacourt credentials to login."
            raise ConfigurationError(msg)

        if log:
            with console.status("Logging in to Alacourt…"):
                return _login(self.driver, self.cID, self.uID, self.pwd)
        else:
            return _login(self.driver, self.cID, self.uID, self.pwd)

    # party search
    def set_party_search_queue(
        self: "AlacourtDriver", queue: str | Path | pl.DataFrame
    ) -> None:
        """Set path to Party Search queue spreadsheet."""
        if isinstance(queue, pl.DataFrame):
            self.party_search_queue_path = None
            self.party_search_queue = queue
        if isinstance(queue, str):
            queue = Path(queue).resolve()
        if isinstance(queue, Path):
            if queue.is_file():
                self.party_search_queue_path = queue
                queue_df = read(queue)
                assert isinstance(queue_df, pl.DataFrame)
                self.party_search_queue = queue_df
            else:
                msg = "Could not read input."
                raise BadFileError(msg)
        assert isinstance(self.party_search_queue, pl.DataFrame)
        for column in ["Retrieved", "Timestamp", "CaseCount"]:
            if column not in self.party_search_queue.columns:
                self.party_search_queue = self.party_search_queue.with_columns(
                    pl.lit("").alias(column)
                )
        pscols = [
            "NAME",
            "PARTY_TYPE",
            "SSN",
            "DOB",
            "COUNTY",
            "DIVISION",
            "CASE_YEAR",
            "NO_RECORDS",
            "FILED_BEFORE",
            "FILED_AFTER",
        ]
        col_dict = {}
        for column in self.party_search_queue.columns:
            d = {re.sub(" ", "_", column.upper()): column}
            col_dict.update(d)
        for key in col_dict:
            if key in pscols:
                self.party_search_queue = self.party_search_queue.with_columns(
                    pl.col(col_dict[key]).alias("TEMP_" + key)
                )
        temp_pscols = [f"TEMP_{column}" for column in pscols]
        for column in temp_pscols:
            if column not in self.party_search_queue.columns:
                self.party_search_queue = self.party_search_queue.with_columns(
                    pl.lit("").alias(column)
                )
        for column in self.party_search_queue.columns:
            self.party_search_queue = self.party_search_queue.with_columns(
                pl.when(pl.col(column) is None)
                .then(pl.lit(""))
                .otherwise(pl.col(column))
                .alias(column)
            )
        return None

    def set_party_search_output(
        self: "AlacourtDriver", output_path: str | Path
    ) -> None:
        """Set path to Party Search output spreadsheet."""
        self.output = Path(output_path).resolve()
        return None

    def party_search(
        self: "AlacourtDriver",
        name: str = "",
        party_type: str = "",
        ssn: str = "",
        dob: str = "",
        county: str = "",
        division: str = "",
        case_year: str = "",
        filed_before: str = "",
        filed_after: str = "",
        no_records: str = "",
        *,
        criminal_only: bool = False,
    ) -> None:
        """Alacourt Party Search with fields provided."""
        self.driver.implicitly_wait(10)
        try:
            if "frmIndexSearchForm" not in self.driver.current_url:
                self.driver.get("https://v2.alacourt.com/frmIndexSearchForm.aspx")
        except Exception:
            self.driver.get("https://v2.alacourt.com/frmIndexSearchForm.aspx")

        if "frmlogin" in self.driver.current_url:
            self.login(log=False)
            self.driver.get("https://v2.alacourt.com/frmIndexSearchForm.aspx")

        # locators
        party_name_box = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$txtName"
        )
        ssn_box = self.driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtSSN")
        dob_box = self.driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtDOB")
        plaintiffs_pt_select = self.driver.find_element(
            By.ID, "ContentPlaceHolder1_rdlPartyType_0"
        )
        defendants_pt_select = self.driver.find_element(
            By.ID, "ContentPlaceHolder1_rdlPartyType_1"
        )
        all_pt_select = self.driver.find_element(
            By.ID, "ContentPlaceHolder1_rdlPartyType_2"
        )
        division_select = Select(
            self.driver.find_element(
                By.ID,
                "ContentPlaceHolder1_UcddlDivisions1_ddlDivision",
            )
        )
        county_select = Select(
            self.driver.find_element(By.ID, "ContentPlaceHolder1_ddlCounties")
        )
        case_year_select = Select(
            self.driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ddlCaseYear")
        )
        no_records_select = Select(
            self.driver.find_element(
                By.NAME, "ctl00$ContentPlaceHolder1$ddlNumberOfRecords"
            )
        )
        filed_before_box = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$txtFrom"
        )
        filed_after_box = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$txtTo"
        )
        search_button = self.driver.find_element(By.ID, "searchButton")

        # set fields
        if name != "" and name is not None:
            party_name_box.send_keys(name.replace("\n", "").strip())
        if ssn != "" and ssn is not None:
            ssn_box.send_keys(ssn.replace("\n", "").strip())
        if dob != "" and dob is not None:
            dob_box.send_keys(dob.replace("\n", "").strip())
        if party_type == "Plaintiffs":
            plaintiffs_pt_select.click()
        if party_type == "Defendants":
            defendants_pt_select.click()
        if party_type == "ALL":
            all_pt_select.click()
        if division == "" and not criminal_only:
            division = "All Divisions"
        if criminal_only:
            division = "Criminal Only"
        division_select.select_by_visible_text(division)
        if county != "":
            county_select.select_by_visible_text(county)
        if case_year != "":
            case_year_select.select_by_visible_text(str(case_year))
        if filed_before != "":
            filed_before_box.send_keys(filed_before.replace("\n", "").strip())
        if filed_after != "":
            filed_after_box.send_keys(filed_after.replace("\n", "").strip())
        if no_records != "":
            no_records_select.select_by_visible_text(str(no_records))
        else:
            no_records_select.select_by_visible_text("1000")

        search_button.click()

        # wait for table
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_dg"))
        )
        return None

    def read_results_page(self: "AlacourtDriver") -> pl.DataFrame:
        """Read current Party Search results page."""
        if "frmIndexSearchList" not in self.driver.current_url:
            msg = "Try again on party search results page."
            raise WrongPageError(msg)
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        table = soup.find("table", {"id": "ContentPlaceHolder1_dg"})
        assert isinstance(table, bs4.element.Tag)
        rows = table.find_all("tr")
        rows_text = []
        clean_rows = []
        for row in rows:
            cells = row.find_all("td")
            cells = [cell.text for cell in cells]
            rows_text += [cells]
        for row in rows_text:
            if len(row) > 10:
                clean_rows += [row]
        df = pl.DataFrame({"Row": clean_rows})
        if df.shape[0] > 0:
            df = df.select(
                pl.col("Row").list.get(0).alias("County"),
                pl.col("Row").list.get(16).alias("CaseNumber"),
                pl.col("Row").list.get(6).alias("Name"),
                pl.col("Row").list.get(7).alias("JID"),
                pl.col("Row").list.get(8).alias("OriginalCharge"),
                pl.col("Row").list.get(9).alias("Bond"),
                pl.col("Row").list.get(10).alias("DOB"),
                pl.col("Row").list.get(11).alias("Sex"),
                pl.col("Row").list.get(12).alias("Race"),
                pl.col("Row").list.get(13).alias("CourtActionDate"),
                pl.col("Row").list.get(15).alias("SSN"),
            )
        else:
            return pl.DataFrame()
        df = df.filter(pl.col("CaseNumber").is_not_null())
        return df

    def read_all_results(self: "AlacourtDriver") -> pl.DataFrame:
        """Read all current Party Search results pages."""
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        try:
            pages_element = soup.find("td", {"id": "ContentPlaceHolder1_dg_tcPageXofY"})
            assert isinstance(pages_element, bs4.element.Tag)
            total_pages = int(pages_element.text.split()[-1])
        except Exception:
            total_pages = 1
        df = self.read_results_page()
        for i in range(2, total_pages + 1):
            table = self.driver.find_element(By.ID, "ContentPlaceHolder1_dg")
            page_select = Select(
                self.driver.find_element(By.ID, "ContentPlaceHolder1_dg_ddlPages")
            )
            page_select.select_by_visible_text(str(i))
            WebDriverWait(self.driver, 10).until(EC.staleness_of(table))
            table = self.driver.find_element(By.ID, "ContentPlaceHolder1_dg")
            df = pl.concat([df, self.read_results_page()])
        return df

    def start_party_search_queue(
        self: "AlacourtDriver",
        queue: str | Path | pl.DataFrame | None = None,
        output_path: str | Path | None = None,
        *,
        criminal_only: bool = False,
    ) -> pl.DataFrame:
        """
        From `queue`, conduct Party Search and record results tables to `output_path`.
        """
        if self.cID is None or self.uID is None or self.pwd is None:
            msg = "Must login to Alacourt before starting queue."
            raise ConfigurationError(msg)
        if queue is not None:
            self.set_party_search_queue(queue)
        elif self.party_search_queue is None:
            msg = "Must set party search queue to start."
            raise ConfigurationError(msg)
        assert isinstance(self.party_search_queue, pl.DataFrame)
        if output_path is not None:
            self.set_party_search_output(output_path)
        try:
            assert isinstance(self.output, str | Path)
            results_df = read(self.output)
            assert isinstance(results_df, pl.DataFrame)
            for column in results_df.columns:
                results_df = results_df.with_columns(pl.col(column).cast(pl.Utf8))
            console.print("Appending to existing table at output path.")
        except Exception:
            results_df = pl.DataFrame()
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as bar:
            for i, r in enumerate(
                bar.track(
                    self.party_search_queue.rows(named=True),
                    description="Party searching…",
                )
            ):
                if r["Retrieved"] in ("", None):
                    try:
                        self.party_search(
                            name=r["TEMP_NAME"],
                            party_type=r["TEMP_PARTY_TYPE"],
                            ssn=r["TEMP_SSN"],
                            dob=r["TEMP_DOB"],
                            county=r["TEMP_COUNTY"],
                            division=r["TEMP_DIVISION"],
                            case_year=r["TEMP_CASE_YEAR"],
                            filed_before=r["TEMP_FILED_BEFORE"],
                            filed_after=r["TEMP_FILED_AFTER"],
                            no_records=r["TEMP_NO_RECORDS"],
                            criminal_only=criminal_only,
                        )
                        df = self.read_all_results()
                    except Exception as exc:
                        console.print(exc)
                        self.reconnect()
                        self.party_search(
                            name=r["TEMP_NAME"],
                            party_type=r["TEMP_PARTY_TYPE"],
                            ssn=r["TEMP_SSN"],
                            dob=r["TEMP_DOB"],
                            county=r["TEMP_COUNTY"],
                            division=r["TEMP_DIVISION"],
                            case_year=r["TEMP_CASE_YEAR"],
                            filed_before=r["TEMP_FILED_BEFORE"],
                            filed_after=r["TEMP_FILED_AFTER"],
                            no_records=r["TEMP_NO_RECORDS"],
                            criminal_only=criminal_only,
                        )
                        df = self.read_all_results()
                    if len(df) > 0:
                        df = df.with_columns(pl.lit(r["TEMP_NAME"]).alias("Search"))
                    else:
                        df = df.with_columns(
                            pl.Series(name="Search", dtype=pl.Utf8, values=[])
                        )
                    for column in ["Retrieved", "Timestamp", "Destination"]:
                        if column in results_df.columns:
                            if len(df) > 0:
                                df = df.with_columns(pl.lit("").alias(column))
                            else:
                                df = df.with_columns(
                                    pl.Series(name=column, dtype=pl.Utf8, values=[])
                                )
                    if df.shape[0] > 1:
                        results_df = pl.concat([results_df, df])
                    self.party_search_queue[i, "Retrieved"] = "Y"
                    self.party_search_queue[i, "CaseCount"] = df.shape[0]
                    self.party_search_queue[i, "Timestamp"] = time.time()
                    if self.party_search_queue_path is not None and i % 10 == 0:
                        write_queue = self.party_search_queue.select(
                            pl.exclude(
                                "TEMP_NAME",
                                "TEMP_PARTY_TYPE",
                                "TEMP_SSN",
                                "TEMP_DOB",
                                "TEMP_COUNTY",
                                "TEMP_DIVISION",
                                "TEMP_CASE_YEAR",
                                "TEMP_FILED_BEFORE",
                                "TEMP_FILED_AFTER",
                                "TEMP_NO_RECORDS",
                            )
                        ).with_columns(
                            pl.col("CaseCount").cast(pl.Int64, strict=False),
                            pl.col("Timestamp").cast(pl.Float64, strict=False),
                        )
                        write({"queue": write_queue}, self.party_search_queue_path)
                    if self.output is not None and i % 10 == 0:
                        write({"results": results_df}, self.output)
            if self.party_search_queue_path is not None:
                write_queue = self.party_search_queue.select(
                    pl.exclude(
                        "TEMP_NAME",
                        "TEMP_PARTY_TYPE",
                        "TEMP_SSN",
                        "TEMP_DOB",
                        "TEMP_COUNTY",
                        "TEMP_DIVISION",
                        "TEMP_CASE_YEAR",
                        "TEMP_FILED_BEFORE",
                        "TEMP_FILED_AFTER",
                        "TEMP_NO_RECORDS",
                    )
                ).with_columns(
                    pl.col("CaseCount").cast(pl.Int64, strict=False),
                    pl.col("Timestamp").cast(pl.Float64, strict=False),
                )
                write({"queue": write_queue}, self.party_search_queue_path)
            if self.output is not None:
                write({"results": results_df}, self.output)
        return results_df

    # case number search
    def set_case_number_queue(
        self: "AlacourtDriver", queue: str | Path | pl.DataFrame
    ) -> None:
        """Set case number queue."""
        if self.cID is None or self.uID is None or self.pwd is None:
            msg = "Must login to Alacourt before starting queue."
            raise ConfigurationError(msg)
        read_df: pl.DataFrame | dict[str, pl.DataFrame] | str | Path | None
        if isinstance(queue, pl.DataFrame):
            read_df = queue
        if isinstance(queue, str):
            queue = Path(queue).resolve()
        if isinstance(queue, Path):
            self.case_number_queue_path = queue
            read_df = read(queue)
        assert isinstance(read_df, pl.DataFrame)
        self.case_number_queue = read_df
        for column in ["Retrieved", "Timestamp", "Destination"]:
            if column not in self.case_number_queue.columns:
                self.case_number_queue = self.case_number_queue.with_columns(
                    pl.lit("").alias(column)
                )
        if (
            "CaseNumber" not in self.case_number_queue.columns
            and "Case Number" in self.case_number_queue.columns
        ):
            self.case_number_queue = self.case_number_queue.with_columns(
                pl.col("Case Number").alias("CaseNumber")
            )
        return None

    def case_number_search(
        self: "AlacourtDriver", case_number: str = "", *, download: bool = True
    ) -> bool:
        """
        Use Alacourt Case Lookup to search for a case by number. If `download`
        is true, will also download case detail PDF. Returns False if case
        detail is unavailable.
        """
        self.driver.get("https://v2.alacourt.com/frmcaselookupform.aspx")

        if "frmlogin" in self.driver.current_url:
            self.login(log=False)
            self.driver.get("https://v2.alacourt.com/frmcaselookupform.aspx")

        county_select = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$ddlCounty"
        )
        division_select = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$ddlDivision"
        )
        case_year_select = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$ddlCaseYear"
        )
        case_number_input = self.driver.find_element(
            By.NAME, "ctl00$ContentPlaceHolder1$txtCaseNumber"
        )
        case_extension_select = Select(
            self.driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ddlExt")
        )
        # fmt: off
        cmap = pl.DataFrame(
            {
                "Selection": [
                    "94 - ARDMORE", "93 - ATHENS", "04 - AUTAUGA", "05 - BALDWIN",
                    "06 - BARBOUR - CLAYTON", "69 - BARBOUR - EUFAULA", "89 - BERRY",
                    "07 - BIBB", "08 - BLOUNT", "87 - BRUNDIDGE MUNICIPAL COURT",
                    "09 - BULLOCK", "10 - BUTLER", "11 - CALHOUN", "12 - CHAMBERS",
                    "13 - CHEROKEE", "90 - CHEROKEE", "14 - CHILTON", "15 - CHOCTAW",
                    "16 - CLARKE", "17 - CLAY", "18 - CLEBURNE", "19 - COFFEE - ELBA",
                    "71 - COFFEE - ENTERPRISE", "20 - COLBERT", "21 - CONECUH",
                    "22 - COOSA", "23 - COVINGTON", "24 - CRENSHAW", "25 - CULLMAN",
                    "26 - DALE", "27 - DALLAS", "28 - DeKALB", "29 - ELMORE",
                    "30 - ESCAMBIA", "31 - ETOWAH", "32 - FAYETTE", "33 - FRANKLIN",
                    "34 - GENEVA", "35 - GREENE", "36 - HALE", "37 - HENRY",
                    "38 - HOUSTON", "39 - JACKSON", "68 - JEFFERSON - BESSEMER",
                    "01 - JEFFERSON - BIRMINGHAM", "40 - LAMAR", "41 - LAUDERDALE",
                    "42 - LAWRENCE", "43 - LEE", "44 - LIMESTONE", "82 - LIVINGSTON",
                    "45 - LOWNDES", "46 - MACON", "47 - MADISON", "48 - MARENGO",
                    "49 - MARION", "50 - MARSHALL", "92 - MILLBROOK", "02 - MOBILE",
                    "51 - MONROE", "03 - MONTGOMERY", "52 - MORGAN", "53 - PERRY",
                    "80 - PHENIX CITY", "54 - PICKENS", "55 - PIKE", "88 - PRATTVILLE",
                    "56 - RANDOLPH", "57 - RUSSELL", "58 - SHELBY",
                    "59 - ST. CLAIR - ASHVILLE", "75 - ST. CLAIR - PELL CITY",
                    "81 - SUMITON MUNICIPAL COURT", "60 - SUMTER",
                    "74 - TALLADEGA - SYLACAUGA", "61 - TALLADEGA - TALLADEGA",
                    "70 - TALLAPOOSA - ALEX CITY", "62 - TALLAPOOSA - DADEVILLE",
                    "63 - TUSCALOOSA", "64 - WALKER", "65 - WASHINGTON",
                    "95 - WETUMPKA MUNICIPAL COURT", "66 - WILCOX", "67 - WINSTON"
                ],
                "CountyNumber": [
                    "94", "93", "04", "05", "06", "69", "89", "07", "08", "87", "09",
                    "10", "11", "12", "13", "90", "14", "15", "16", "17", "18", "19",
                    "71", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "68",
                    "01", "40", "41", "42", "43", "44", "82", "45", "46", "47", "48",
                    "49", "50", "92", "02", "51", "03", "52", "53", "80", "54", "55",
                    "88", "56", "57", "58", "59", "75", "81", "60", "74", "61", "70",
                    "62", "63", "64", "65", "95", "66", "67"
                ],
                 "County": [
                    "ARDMORE", "ATHENS", "AUTAUGA", "BALDWIN", "BARBOUR - CLAYTON",
                    "BARBOUR - EUFAULA", "BERRY", "BIBB", "BLOUNT",
                    "BRUNDIDGE MUNICIPAL COURT", "BULLOCK", "BUTLER", "CALHOUN",
                    "CHAMBERS", "CHEROKEE", "CHEROKEE", "CHILTON", "CHOCTAW", "CLARKE",
                    "CLAY", "CLEBURNE", "COFFEE - ELBA", "COFFEE - ENTERPRISE",
                    "COLBERT", "CONECUH", "COOSA", "COVINGTON", "CRENSHAW",
                    "CULLMAN", "DALE", "DALLAS", "DeKALB", "ELMORE", "ESCAMBIA",
                    "ETOWAH", "FAYETTE", "FRANKLIN", "GENEVA", "GREENE", "HALE",
                    "HENRY", "HOUSTON", "JACKSON", "JEFFERSON - BESSEMER",
                    "JEFFERSON - BIRMINGHAM", "LAMAR", "LAUDERDALE", "LAWRENCE", "LEE",
                    "LIMESTONE", "LIVINGSTON", "LOWNDES", "MACON", "MADISON", "MARENGO",
                    "MARION", "MARSHALL", "MILLBROOK", "MOBILE", "MONROE", "MONTGOMERY",
                    "MORGAN", "PERRY", "PHENIX CITY", "PICKENS", "PIKE", "PRATTVILLE",
                    "RANDOLPH", "RUSSELL", "SHELBY", "ST. CLAIR - ASHVILLE",
                    "ST. CLAIR - PELL CITY", "SUMITON MUNICIPAL COURT", "SUMTER",
                    "TALLADEGA - SYLACAUGA", "TALLADEGA - TALLADEGA",
                    "TALLAPOOSA - ALEX CITY", "TALLAPOOSA - DADEVILLE", "TUSCALOOSA",
                    "WALKER", "WASHINGTON", "WETUMPKA MUNICIPAL COURT", "WILCOX",
                    "WINSTON"
                ],
            }
        )
        dmap = pl.DataFrame(
            {
                "Code": [
                    "CC", "CS", "CV", "DC", "DR", "DV",
                    "EQ", "JU", "MC", "SM", "TP", "TR"
                ],
                "Selection": [
                    "CC - CIRCUIT-CRIMINAL", "CS - CHILD SUPPORT", "CV - CIRCUIT-CIVIL",
                    "DC - DISTRICT-CRIMINAL", "DR - DOMESTIC RELATIONS",
                    "DV - DISTRICT-CIVIL", "EQ - EQUITY-CASES", "JU - JUVENILE",
                    "MC - MUNICIPAL-CRIMINAL", "SM - SMALL CLAIMS",
                    "TP - MUNICIPAL-PARKING", "TR - TRAFFIC"
                ],
            }
        )
        # fmt: on
        county_number = case_number[0:2]
        division_code = case_number[3:5]
        case_year = case_number[6:10]
        six_digit = case_number[11:17]
        extension = case_number[18:20] if len(case_number) >= 20 else "00"
        try:
            county = (
                cmap.filter(pl.col("CountyNumber") == county_number)
                .select("Selection")
                .to_series()[0]
            )
        except Exception:
            return False
        division = (
            dmap.filter(pl.col("Code") == division_code)
            .select("Selection")
            .to_series()[0]
        )
        county_select.send_keys(county)
        division_select.send_keys(division)
        case_year_select.send_keys(case_year)
        case_number_input.send_keys(six_digit)
        case_extension_select.select_by_visible_text(extension)
        search_button = self.driver.find_element(By.ID, "searchButton")
        search_button.click()
        try:
            WebDriverWait(self.driver, 20).until(EC.staleness_of(search_button))
        except Exception:
            self.reconnect()
            self.driver.get("https://v2.alacourt.com/frmcaselookupform.aspx")
            county_select = self.driver.find_element(
                By.NAME, "ctl00$ContentPlaceHolder1$ddlCounty"
            )
            division_select = self.driver.find_element(
                By.NAME, "ctl00$ContentPlaceHolder1$ddlDivision"
            )
            case_year_select = self.driver.find_element(
                By.NAME, "ctl00$ContentPlaceHolder1$ddlCaseYear"
            )
            case_number_input = self.driver.find_element(
                By.NAME, "ctl00$ContentPlaceHolder1$txtCaseNumber"
            )
            case_extension_select = Select(
                self.driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ddlExt")
            )
            county_select.send_keys(county)
            division_select.send_keys(division)
            case_year_select.send_keys(case_year)
            case_number_input.send_keys(six_digit)
            case_extension_select.select_by_visible_text(extension)
            search_button = self.driver.find_element(By.ID, "searchButton")
            search_button.click()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(search_button))
        if (
            "NoCaseDetails" in self.driver.current_url
            or "frmAuthenticate" in self.driver.current_url
            or "frmError" in self.driver.current_url
        ):
            return False
        if download:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.ID, "ContentPlaceHolder1_lnkPrint")
                    )
                )
            except Exception:
                return False
            self.driver.find_element(By.ID, "ContentPlaceHolder1_lnkPrint").click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "divPrintCase"))
            )
            self.driver.find_element(By.ID, "btnPrintCase").click()
            time.sleep(0.5)
        return True

    def start_case_number_queue(
        self: "AlacourtDriver",
        queue: str | Path | pl.DataFrame | None = None,
        *,
        verify: bool = True,
        pre_verify: bool = False,
    ) -> None:
        """
        From a table with 'Case Number' or 'CaseNumber' column, download cases
        to `AlacourtDriver.source_path`.
        """
        if pre_verify:
            if isinstance(queue, pl.DataFrame | str | Path):
                self.set_case_number_queue(queue)
            elif self.case_number_queue is None:
                msg = "Must set case number queue to start."
                raise ConfigurationError(msg)
            self.verify_downloads()
        loop = True
        while loop:
            if isinstance(queue, pl.DataFrame | str | Path):
                self.set_case_number_queue(queue)
            elif self.case_number_queue is None:
                msg = "Must set case number queue to start."
                raise ConfigurationError(msg)
            assert isinstance(self.case_number_queue, pl.DataFrame)
            progress_bar = Progress(
                *Progress.get_default_columns(), MofNCompleteColumn()
            )
            with progress_bar as bar:
                for i, r in enumerate(
                    bar.track(
                        self.case_number_queue.rows(named=True),
                        description="Fetching cases…",
                    )
                ):
                    if r["Retrieved"] in ("", None):
                        try:
                            success = self.case_number_search(r["CaseNumber"])
                        except Exception:
                            self.reconnect()
                            success = self.case_number_search(r["CaseNumber"])
                        if success:
                            self.case_number_queue[i, "Retrieved"] = "Y"
                            self.case_number_queue[i, "Timestamp"] = time.time()
                            self.case_number_queue[i, "Destination"] = str(
                                self.source_path
                            )
                        else:
                            self.case_number_queue[i, "Retrieved"] = "PDF Not Available"
                            self.case_number_queue[i, "Timestamp"] = time.time()
                        if self.case_number_queue_path is not None and i % 10 == 0:
                            write_queue = self.case_number_queue.with_columns(
                                pl.col("Timestamp").cast(pl.Float64, strict=False)
                            )
                            write(
                                {"queue": write_queue},
                                self.case_number_queue_path,
                            )
                if self.case_number_queue_path is not None:
                    write_queue = self.case_number_queue.with_columns(
                        pl.col("Timestamp").cast(pl.Float64, strict=False)
                    )
                    write(
                        {"queue": write_queue},
                        self.case_number_queue_path,
                    )
            if verify:
                self.verify_downloads()
                remaining = self.case_number_queue.filter(
                    pl.col("Retrieved").is_null() | pl.col("Retrieved").eq("")
                ).shape[0]
                loop = remaining > 0
            else:
                loop = False
        return None

    def reconnect(
        self: "AlacourtDriver", wait: int = 20, max_attempt: int = 10
    ) -> None:
        """
        Attempt to reconnect to Alacourt after `wait` seconds, up to
        `max_attempt` times before raising an exception.
        """
        successfully_reconnected = False
        i = 0
        while not successfully_reconnected:
            try:
                successfully_reconnected = self.login(log=False)
            except Exception:
                i += 1
                if i == max_attempt:
                    break
                time.sleep(wait)
        if not successfully_reconnected:
            msg = f"Failed to reconnect to Alacourt after {max_attempt} attempts."
            raise ConnectionError(msg)
        return None

    def verify_downloads(
        self: "AlacourtDriver", queue: str | Path | pl.DataFrame | None = None
    ) -> pl.DataFrame:
        """
        Read case numbers from all cases in `source_path`, and correct
        `AlacourtDriver.case_number_queue` to accurately reflect progress.
        """
        if isinstance(queue, pl.DataFrame | str | Path):
            self.set_case_number_queue(queue)
        elif not isinstance(self.case_number_queue, pl.DataFrame):
            msg = "Must set case number queue to verify."
            raise ConfigurationError(msg)
        if self.source_path is None:
            msg = "Must set download directory to verify."
            raise ConfigurationError(msg)
        with console.status("Verifying downloads…"):
            time.sleep(2)
            pdfs = self.source_path.rglob("**/*.pdf")
            with multiprocessing.Pool() as pool:
                case_numbers = pool.map(case_number_from_path, pdfs)
            case_numbers = [cnum for cnum in case_numbers if cnum is not None]
        assert isinstance(self.case_number_queue, pl.DataFrame)
        self.case_number_queue = (
            self.case_number_queue.with_columns(
                pl.when(
                    pl.col("CaseNumber").is_in(case_numbers).not_()
                    & pl.col("Retrieved").ne("PDF Not Available")
                )
                .then(pl.lit(""))
                .otherwise(pl.col("Retrieved"))
                .alias("Retrieved")
            )
            .with_columns(
                pl.when(pl.col("CaseNumber").is_in(case_numbers))
                .then(pl.lit("Y"))
                .otherwise(pl.col("Retrieved"))
                .alias("Retrieved")
            )
            .sort("Retrieved", descending=True)
        )
        if self.case_number_queue_path is not None:
            write({"queue": self.case_number_queue}, self.case_number_queue_path)
        remaining = self.case_number_queue.filter(
            pl.col("Retrieved").is_null() | pl.col("Retrieved").eq("")
        ).shape[0]
        if remaining > 0:
            console.print(f"{remaining} cases remaining after download verification.")
        else:
            console.print("All cases have been downloaded to destination path.")
        return self.case_number_queue


class ADOCDriver:
    """Collect inmate search results from the ADOC website."""

    def __init__(
        self: "ADOCDriver",
        output_path: str | Path | None = None,
        *,
        headless: bool = True,
    ) -> None:
        """Create ADOCDriver object."""
        self.output: Path | None
        if output_path is not None:
            self.output = Path(output_path).resolve()
        else:
            self.output = None
        self.queue_path: Path | None = None
        self.queue: pl.DataFrame | None = None
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        with console.status("Starting WebDriver (requires Google Chrome)…"):
            self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://doc.alabama.gov/inmatesearch")

    def crawl(
        self: "ADOCDriver", output_path: str | Path | None = None
    ) -> pl.DataFrame:
        """Collect all inmates in ADOC Inmate Search."""
        if output_path is not None:
            self.output = Path(output_path).resolve()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        results = pl.DataFrame()
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as bar:
            for letter in bar.track(alphabet, description="Crawling ADOC…"):
                self.driver.get("https://doc.alabama.gov/inmatesearch")
                self.driver.find_element(By.ID, "MainContent_txtLName").send_keys(
                    letter
                )
                self.driver.find_element(By.ID, "MainContent_btnSearch").click()
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.ID, "MainContent_gvInmateResults")
                    )
                )
                soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
                try:
                    pages_element = soup.find(
                        "span", {"id": "MainContent_gvInmateResults_lblPages"}
                    )
                    assert isinstance(pages_element, bs4.element.Tag)
                    total_pages = int(pages_element.text)
                except Exception:
                    total_pages = 1
                for _ in range(1, total_pages + 1):
                    soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
                    table = soup.find("table", {"id": "MainContent_gvInmateResults"})
                    assert isinstance(table, bs4.element.Tag)
                    rows = table.find_all("tr")
                    rows_text = []
                    for row in rows:
                        cells = [cell.text for cell in row.find_all("td")]
                        rows_text += [cells]
                    df = (
                        pl.DataFrame({"Row": rows_text})
                        .filter(pl.col("Row").list.len() > 3)
                        .select(
                            pl.col("Row").list.get(0).alias("AIS"),
                            pl.col("Row")
                            .list.get(1)
                            .str.replace_all("\n", "")
                            .str.strip_chars()
                            .alias("Name"),
                            pl.col("Row").list.get(2).alias("Sex"),
                            pl.col("Row").list.get(3).alias("Race"),
                            pl.col("Row")
                            .list.get(4)
                            .cast(pl.Int64, strict=False)
                            .alias("BirthYear"),
                            pl.col("Row")
                            .list.get(5)
                            .str.strip_chars()
                            .alias("Institution"),
                            pl.col("Row")
                            .list.get(6)
                            .str.strip_chars()
                            .str.to_date("%m/%d/%Y", strict=False)
                            .alias("ReleaseDate"),
                            pl.col("Row").list.get(7).str.strip_chars().alias("Code"),
                        )
                    )
                    results = pl.concat([results, df])
                    table_selenium = self.driver.find_element(
                        By.ID, "MainContent_gvInmateResults"
                    )
                    if total_pages > 1:
                        self.driver.find_element(
                            By.ID,
                            "MainContent_gvInmateResults_btnNext",
                        ).click()
                        WebDriverWait(self.driver, 10).until(
                            EC.staleness_of(table_selenium)
                        )
                if self.output not in (None, ""):
                    assert isinstance(self.output, Path)
                    write({"results": results}, self.output)
        return results

    def search(
        self: "ADOCDriver", ais: str = "", first_name: str = "", last_name: str = ""
    ) -> None:
        """Search ADOC Inmate Search with provided fields."""
        if self.driver.current_url != "https://doc.alabama.gov/InmateSearch":
            self.driver.get("https://doc.alabama.gov/InmateSearch")
        ais_box = self.driver.find_element(By.ID, "MainContent_txtAIS")
        first_name_box = self.driver.find_element(By.ID, "MainContent_txtFName")
        last_name_box = self.driver.find_element(By.ID, "MainContent_txtLName")
        search_button = self.driver.find_element(By.ID, "MainContent_btnSearch")
        ais_box.send_keys(ais)
        first_name_box.send_keys(first_name)
        last_name_box.send_keys(last_name)
        search_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "MainContent_lblMessage"))
        )

    def select_result(self: "ADOCDriver", index: int = 0) -> bool:
        """
        Select result at index from ADOC Inmate Search results table page.
        Returns false if no result at index.
        """
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        urls = soup.find_all(
            "a",
            {"id": re.compile(r"MainContent_gvInmateResults_lnkInmateName_\d+")},
        )
        try:
            self.driver.find_element(By.ID, urls[index]["id"]).click()
        except Exception:
            return False
        else:
            return True

    def read_results_page(self: "ADOCDriver") -> dict[str, pl.DataFrame] | None:
        """Read current Inmate History page from ADOC Inmate Search."""
        cmap = pl.from_records(
            [
                ("ARDMORE", ["94"]),
                ("ATHENS", ["93"]),
                ("AUTAUGA", ["04"]),
                ("BALDWIN", ["05"]),
                ("BARBOUR", ["06", "69"]),
                ("BARBOUR - CLAYTON", ["06"]),
                ("BARBOUR - EUFAULA", ["69"]),
                ("BERRY", ["89"]),
                ("BIBB", ["07"]),
                ("BLOUNT", ["08"]),
                ("BRUNDIDGE MUNICIPAL COURT", ["87"]),
                ("BULLOCK", ["09"]),
                ("BUTLER", ["10"]),
                ("CALHOUN", ["11"]),
                ("CHAMBERS", ["12"]),
                ("CHEROKEE", ["13", "90"]),
                ("CHILTON", ["14"]),
                ("CHOCTAW", ["15"]),
                ("CLARKE", ["16"]),
                ("CLAY", ["17"]),
                ("CLEBURNE", ["18"]),
                ("COFFEE", ["19", "71"]),
                ("COLBERT", ["20"]),
                ("CONECUH", ["21"]),
                ("COOSA", ["22"]),
                ("COVINGTON", ["23"]),
                ("CRENSHAW", ["24"]),
                ("CULLMAN", ["25"]),
                ("DALE", ["26"]),
                ("DALLAS", ["27"]),
                ("DEKALB", ["28"]),
                ("ELMORE", ["29"]),
                ("ESCAMBIA", ["30"]),
                ("ETOWAH", ["31"]),
                ("FAYETTE", ["32"]),
                ("FRANKLIN", ["33"]),
                ("GENEVA", ["34"]),
                ("GREENE", ["35"]),
                ("HALE", ["36"]),
                ("HENRY", ["37"]),
                ("HOUSTON", ["38"]),
                ("JACKSON", ["39"]),
                ("JEFFERSON", ["01"]),
                ("BESSEMER", ["68"]),
                ("LAMAR", ["40"]),
                ("LAUDERDALE", ["41"]),
                ("LAWRENCE", ["42"]),
                ("LEE", ["43"]),
                ("LIMESTONE", ["44"]),
                ("LIVINGSTON", ["82"]),
                ("LOWNDES", ["45"]),
                ("MACON", ["46"]),
                ("MADISON", ["47"]),
                ("MARENGO", ["48"]),
                ("MARION", ["49"]),
                ("MARSHALL", ["50"]),
                ("MILLBROOK", ["92"]),
                ("MOBILE", ["02"]),
                ("MONROE", ["51"]),
                ("MONTGOMERY", ["03"]),
                ("MORGAN", ["52"]),
                ("PERRY", ["53"]),
                ("PHENIX CITY", ["80"]),
                ("PICKENS", ["54"]),
                ("PIKE", ["55"]),
                ("PRATTVILLE", ["88"]),
                ("RANDOLPH", ["56"]),
                ("RUSSELL", ["57"]),
                ("SHELBY", ["58"]),
                ("ST. CLAIR", ["59", "75"]),
                ("SUMITON MUNICIPAL COURT", ["81"]),
                ("SUMTER", ["60"]),
                ("TALLADEGA", ["74", "61"]),
                ("TALLAPOOSA", ["70", "62"]),
                ("TUSCALOOSA", ["63"]),
                ("WALKER", ["64"]),
                ("WASHINGTON", ["65"]),
                ("WETUMPKA MUNICIPAL COURT", ["95"]),
                ("WILCOX", ["66"]),
                ("WINSTON", ["67"]),
            ],
            ("CommitCounty", "CountyNumbers"),
        )
        if "InmateHistory" not in self.driver.current_url:
            return None
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        # inmate details
        name_element = soup.find("span", {"id": "MainContent_DetailsView2_Label1"})
        assert isinstance(name_element, bs4.element.Tag)
        name = name_element.text
        ais_element = soup.find("span", {"id": "MainContent_DetailsView2_Label2"})
        assert isinstance(ais_element, bs4.element.Tag)
        ais = ais_element.text
        institution_element = soup.find(
            "span", {"id": "MainContent_DetailsView2_Label3"}
        )
        assert isinstance(institution_element, bs4.element.Tag)
        institution = institution_element.text.strip()
        details_table_text_element = soup.find(
            "table", {"id": "MainContent_DetailsView1"}
        )
        assert isinstance(details_table_text_element, bs4.element.Tag)
        details_text = details_table_text_element.text
        race = (
            race_match.group(1)
            if (race_match := re.search(r"Race\:(.)", details_text))
            else ""
        )
        sex = (
            sex_match.group(1)
            if (sex_match := re.search(r"Sex\:(.)", details_text))
            else ""
        )
        hair_color = (
            hair_color_match.group(1)
            if (hair_color_match := re.search(r"Hair Color\:([A-Z]+)", details_text))
            else ""
        )
        eye_color = (
            eye_color_match.group(1)
            if (eye_color_match := re.search(r"Eye Color\:([A-Z]+)", details_text))
            else ""
        )
        height = (
            height_match.group(1)
            if (height_match := re.search(r"Height\:(.+)", details_text))
            else ""
        )
        weight = (
            weight_match.group(1)
            if (weight_match := re.search(r"Weight\:(.+)", details_text))
            else ""
        )
        birth_year = (
            birth_year_match.group(1)
            if (birth_year_match := re.search(r"Birth Year\:(.+)", details_text))
            else ""
        )
        custody = (
            custody_match.group(1).strip()
            if (custody_match := re.search(r"Custody\n\n(.+)", details_text))
            else ""
        )
        aliases = "; ".join(
            [
                re.sub(r'"|,', "", cell.text).strip()
                for cell in soup.find_all(
                    "span",
                    {"id": re.compile(r"MainContent_lvAlias_AliasLabel0_\d")},
                )
            ]
        )
        aliases = re.sub("No known Aliases", "", aliases)
        scars_marks_tattoos = "; ".join(
            [
                re.sub(r'"|,', "", cell.text).strip()
                for cell in soup.find_all(
                    "span",
                    {"id": re.compile(r"MainContent_lvScars_descriptLabel_\d")},
                )
            ]
        )
        scars_marks_tattoos = re.sub(
            "No known scars marks or tattoos", "", scars_marks_tattoos
        )
        inmate_details_df = pl.DataFrame(
            {
                "Name": [name],
                "AIS": [ais],
                "Institution": [institution],
                "Race": [race],
                "Sex": [sex],
                "HairColor": [hair_color],
                "EyeColor": [eye_color],
                "Height": [height],
                "Weight": [int(weight)],
                "BirthYear": [int(birth_year)],
                "Custody": [custody],
                "Aliases": [aliases],
                "ScarsMarksTattoos": [scars_marks_tattoos],
            }
        )
        # black header "Sentences" tables
        black_tables = soup.find_all(
            "table",
            {"id": re.compile(r"MainContent_gvSentence_GridView1_\d+")},
        )
        black_tables_df = pl.DataFrame()
        for i, black_table in enumerate(black_tables):
            rows = black_table.find_all("tr")
            table_list = []
            for row in rows:
                table_list += [[cell.text for cell in row.find_all("td")]]
            df = (
                pl.DataFrame({"Row": table_list})
                .select(
                    pl.lit(ais).alias("AIS"),
                    pl.lit(name).alias("Name"),
                    pl.lit(i + 1).alias("TableNo").cast(pl.Int64, strict=False),
                    pl.col("Row")
                    .list.get(0)
                    .str.replace_all(r"\n", "")
                    .alias("CaseNo"),
                    pl.col("Row")
                    .list.get(1)
                    .str.replace_all(r"\n", "")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("Sentenced"),
                    pl.col("Row")
                    .list.get(2)
                    .str.replace_all(r"\n", "")
                    .str.strip_chars()
                    .alias("Offense"),
                    pl.col("Row").list.get(3).str.replace_all(r"\n", "").alias("Term"),
                    pl.col("Row")
                    .list.get(4)
                    .str.replace_all(r"\n", "")
                    .cast(pl.Int64, strict=False)
                    .alias("JailCredit"),
                    pl.col("Row")
                    .list.get(5)
                    .str.replace_all(r"\n", "")
                    .cast(pl.Int64, strict=False)
                    .alias("PreTimeServed"),
                    pl.col("Row")
                    .list.get(6)
                    .str.replace_all(r"\n", "")
                    .str.strip_chars()
                    .alias("Type"),
                    pl.col("Row")
                    .list.get(7)
                    .str.replace_all(r"\n", "")
                    .str.strip_chars()
                    .alias("CommitCounty"),
                )
                .filter(pl.col("CaseNo").is_not_null())
                .join(cmap, on="CommitCounty", how="left")
                .with_columns(
                    pl.when(pl.col("CountyNumbers").is_not_null())
                    .then(
                        pl.map(
                            (pl.col("CountyNumbers"), pl.col("CaseNo")),
                            lambda ctys_case: ", ".join(  # type: ignore
                                [
                                    f"{cty}-"
                                    f"{m.group(1) if (m := re.search(r'([A-Z]{2})', ctys_case[1][0])) else ''}"  # noqa: E501
                                    f"-{m.group(1) if (m := re.search(r'(\d.+)', ctys_case[1][0])) else ''}"  # noqa: E501
                                    for cty in ctys_case[0][0]
                                ]
                            ),
                            return_dtype=pl.Utf8,
                        ),
                    )
                    .alias("CaseNoFmt")
                )
                .drop("CountyNumbers")
            )
            black_tables_df = pl.concat([black_tables_df, df])
        # blue header tables
        table = soup.find("table", {"id": "MainContent_gvSentence"})
        assert isinstance(table, bs4.element.Tag)
        rows = table.find_all("tr")
        blue_tables_df = pl.DataFrame()
        start_blue_row = False
        table_no = 0
        for row in rows:
            if "SUFAdmit" in row.text:
                start_blue_row = True
                table_no += 1
            elif start_blue_row and "Case No." not in row.text:
                cells = [cell.text for cell in row.find_all("td")]
                df = pl.DataFrame({"TableNo": [table_no], "Row": [cells]})
                blue_tables_df = pl.concat([blue_tables_df, df])
            elif "Case No." in row.text:
                start_blue_row = False
        blue_tables_df = blue_tables_df.select(
            pl.lit(name).alias("Name"),
            pl.lit(ais).alias("AIS"),
            pl.col("TableNo"),
            pl.col("Row").list.get(0).str.strip_chars().alias("SUF"),
            pl.col("Row")
            .list.get(1)
            .str.to_date("%m/%d/%Y", strict=False)
            .alias("AdmitDate"),
            pl.col("Row").list.get(2).alias("TotalTerm"),
            pl.col("Row").list.get(3).alias("TimeServed"),
            pl.col("Row").list.get(4).alias("JailCredit").cast(pl.Int64, strict=False),
            pl.col("Row").list.get(5).str.strip_chars().alias("GoodTimeReceived"),
            pl.col("Row").list.get(6).str.strip_chars().alias("GoodTimeRevoked"),
            pl.col("Row")
            .list.get(7)
            .str.to_date("%m/%d/%Y", strict=False)
            .alias("MinReleaseDate"),
            pl.col("Row")
            .list.get(8)
            .str.to_date("%m/%d/%Y", strict=False)
            .alias("ParoleConsiderationDate"),
            pl.col("Row").list.get(9).str.strip_chars().alias("ParoleStatus"),
        )
        return {
            "InmateDetails": inmate_details_df,
            "BlueTables": blue_tables_df,
            "BlackTables": black_tables_df,
        }

    def set_output_path(self: "ADOCDriver", output_path: str | Path) -> None:
        """Set results output path for start_queue()."""
        self.output = Path(output_path).resolve()

    def set_queue(
        self: "ADOCDriver",
        queue: str | Path | pl.DataFrame,
        output_path: str | Path | None = None,
    ) -> None:
        """
        Set queue from dataframe or spreadsheet with "Last Name", "First
        Name", and "AIS" columns.
        """
        if isinstance(queue, str):
            queue = Path(queue)
        if isinstance(output_path, str):
            output_path = Path(output_path)
        if isinstance(output_path, Path):
            output_path = output_path.resolve()
            self.set_output_path(output_path)
        if isinstance(queue, Path):
            self.queue_path = queue.resolve()
            read_df = read(queue)
            assert isinstance(read_df, pl.DataFrame)
            self.queue = read_df
        if isinstance(queue, pl.DataFrame):
            if output_path is not None:
                self.queue_path = output_path
            else:
                self.queue_path = None
            self.queue = queue
        assert isinstance(self.queue, pl.DataFrame)
        for column in ["Retrieved", "Timestamp"]:
            if column not in self.queue.columns:
                self.queue = self.queue.with_columns(pl.lit("").alias(column))
        for column in self.queue.columns:
            if re.sub(" ", "_", column).upper() in ["LAST_NAME", "FIRST_NAME", "AIS"]:
                self.queue = self.queue.with_columns(
                    pl.col(column).alias(f"TEMP_{re.sub(' ', '_', column).upper()}")
                )
        if (
            "TEMP_LAST_NAME" not in self.queue.columns
            and "TEMP_FIRST_NAME" not in self.queue.columns
            and "Name" in self.queue.columns
        ):
            self.queue = self.queue.with_columns(
                pl.col("Name").str.extract(r"([A-Z]+)").alias("TEMP_LAST_NAME"),
                pl.col("Name").str.extract(r" ([A-Z]+)").alias("TEMP_FIRST_NAME"),
            )
        for column in ["TEMP_LAST_NAME", "TEMP_FIRST_NAME", "TEMP_AIS"]:
            if column not in self.queue.columns:
                self.queue = self.queue.with_columns(pl.lit("").alias(column))

    def start_queue(
        self: "ADOCDriver",
        queue: str | Path | pl.DataFrame | None = None,
        output_path: str | Path | None = None,
    ) -> dict[str, pl.DataFrame]:
        """ADOC Inmate Search for each in `queue`, and save results to `output_path`."""
        if queue is not None:
            self.set_queue(queue)
        else:
            msg = "Must set queue to start."
            raise ConfigurationError(msg)
        assert isinstance(self.queue, pl.DataFrame)
        if output_path is not None:
            self.set_output_path(output_path)
            assert isinstance(self.output, Path)
            try:
                inmate_details = pl.read_excel(
                    self.output,
                    sheet_name="inmate-details",
                    engine_options={"ignore_errors": True},
                ).with_columns(pl.col("AIS").cast(pl.Utf8))
                blue_tables = pl.read_excel(
                    self.output,
                    sheet_name="blue-tables",
                    engine_options={"ignore_errors": True},
                ).with_columns(
                    pl.col("AIS").cast(pl.Utf8),
                    pl.col("TableNo").cast(pl.Int64, strict=False),
                    pl.col("AdmitDate").str.to_date("%Y-%m-%d", strict=False),
                    pl.col("MinReleaseDate").str.to_date("%Y-%m-%d", strict=False),
                    pl.col("ParoleConsiderationDate").str.to_date(
                        "%Y-%m-%d", strict=False
                    ),
                )
                black_tables = pl.read_excel(
                    self.output,
                    sheet_name="black-tables",
                    engine_options={"ignore_errors": True},
                ).with_columns(
                    pl.col("AIS").cast(pl.Utf8),
                    pl.col("TableNo").cast(pl.Int64, strict=False),
                    pl.col("Sentenced").str.to_date("%Y-%m-%d", strict=False),
                )
                console.print("Appending to existing tables at output path.")
            except Exception:
                inmate_details = pl.DataFrame()
                blue_tables = pl.DataFrame()
                black_tables = pl.DataFrame()
        else:
            inmate_details = pl.DataFrame()
            blue_tables = pl.DataFrame()
            black_tables = pl.DataFrame()
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as bar:
            for i, r in enumerate(
                bar.track(self.queue.rows(named=True), description="Searching ADOC…")
            ):
                if r["Retrieved"] in (None, ""):
                    self.search(
                        ais=r["TEMP_AIS"],
                        first_name=r["TEMP_FIRST_NAME"],
                        last_name=r["TEMP_LAST_NAME"],
                    )
                    if self.select_result(0):
                        results = self.read_results_page()
                        assert isinstance(results, dict)
                        inmate_details = pl.concat(
                            [inmate_details, results["InmateDetails"]]
                        )
                        blue_tables = pl.concat([blue_tables, results["BlueTables"]])
                        black_tables = pl.concat([black_tables, results["BlackTables"]])
                        self.queue[i, "Retrieved"] = "Y"
                        self.queue[i, "Timestamp"] = time.time()
                    else:
                        self.queue[i, "Retrieved"] = "NO RESULTS"
                        self.queue[i, "Timestamp"] = time.time()
                    if self.output is not None and i % 10 == 0:
                        write(
                            {
                                "inmate-details": inmate_details,
                                "blue-tables": blue_tables,
                                "black-tables": black_tables,
                            },
                            self.output,
                        )
                    if self.queue_path is not None and i % 10 == 0:
                        write_queue = self.queue.select(
                            pl.exclude("TEMP_LAST_NAME", "TEMP_FIRST_NAME", "TEMP_AIS")
                        ).with_columns(
                            pl.col("Timestamp").cast(pl.Float64, strict=False)
                        )
                        write({"queue": write_queue}, self.queue_path)
            if self.output is not None:
                write(
                    {
                        "inmate-details": inmate_details,
                        "blue-tables": blue_tables,
                        "black-tables": black_tables,
                    },
                    self.output,
                )
            if self.queue_path is not None:
                write_queue = self.queue.select(
                    pl.exclude("TEMP_LAST_NAME", "TEMP_FIRST_NAME", "TEMP_AIS")
                ).with_columns(pl.col("Timestamp").cast(pl.Float64, strict=False))
                write({"queue": write_queue}, self.queue_path)
        return {
            "inmate-details": inmate_details,
            "blue-tables": blue_tables,
            "black-tables": black_tables,
        }


class Cases:
    """
    From a case archive or directory of PDF cases, create, manipulate, and
    export data tables.
    """

    def __init__(self: "Cases", archive: str | Path | pl.DataFrame | None) -> None:
        """Create Cases object from archive or directory path."""
        self.archive: Path | pl.DataFrame | None
        if isinstance(archive, str):
            archive = Path(archive)
        if isinstance(archive, Path):
            archive = archive.resolve()
            if archive.is_dir():
                self.archive = archive
                self.is_read = False
            elif archive.is_file():
                with console.status("Reading input…"):
                    read_df = read(archive)
                    if isinstance(read_df, str):
                        read_df = pl.DataFrame(
                            {
                                "AllPagesText": [read_df],
                                "CaseNumber": [get_case_number(read_df)],
                                "Path": [archive],
                            }
                        )
                    assert isinstance(read_df, pl.DataFrame)
                    self.archive = read_df
                self.is_read = True
            else:
                msg = "Could not read input."
                raise BadFileError(msg)

        if isinstance(archive, pl.DataFrame):
            self.archive = archive
            self.is_read = True
        self._cases: pl.DataFrame | None = None
        self._fees: pl.DataFrame | None = None
        self._filing_charges: pl.DataFrame | None = None
        self._disposition_charges: pl.DataFrame | None = None
        self._sentences: pl.DataFrame | None = None
        self._enforcement: pl.DataFrame | None = None
        self._financial_history: pl.DataFrame | None = None
        self._settings: pl.DataFrame | None = None
        self._case_action_summary: pl.DataFrame | None = None
        self._witnesses: pl.DataFrame | None = None
        self._attorneys: pl.DataFrame | None = None
        self._images: pl.DataFrame | None = None
        self._restitution: pl.DataFrame | None = None
        self._linked_cases: pl.DataFrame | None = None
        self._continuances: pl.DataFrame | None = None
        self._parties: pl.DataFrame | None = None
        self._central_disbursement_division: pl.DataFrame | None = None
        return None

    def __repr__(self: "Cases") -> str:
        """Return string representation of Cases object."""
        if self.is_read:
            assert isinstance(self.archive, pl.DataFrame)
            return self.archive.select("CaseNumber").__str__()
        if not self.is_read:
            return f"Unread directory: {self.archive}"

    def read(self: "Cases") -> pl.DataFrame:
        """Read input into pl.DataFrame. If directory, reads PDFs into archive df."""
        assert isinstance(self.archive, str | Path | pl.DataFrame)
        read_df = read(self.archive)
        assert isinstance(read_df, pl.DataFrame)
        self.archive = read_df
        self.is_read = True
        return self.archive

    def cases(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make case information table."""
        if debug:
            self._cases = None
        # if previously called with debug=True, reset
        if isinstance(self._cases, pl.DataFrame) and "D999RAW" in self._cases.columns:
            self._cases = None
        if isinstance(self._cases, pl.DataFrame):
            return self._cases
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        case_types = {
            "CS": "Child Support",
            "CV": "Circuit Civil",
            "CC": "Circuit Criminal",
            "DV": "District Civil",
            "DC": "District Criminal",
            "DR": "Domestic Relations",
            "EQ": "Equity Cases",
            "MC": "Municipal Criminal",
            "TP": "Municipal Traffic",
            "SM": "Small Claims",
            "TR": "Traffic",
        }
        with console.status("Parsing cases table…"):
            cases = (
                self.archive.with_columns(
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                        group_index=1,
                    )
                    .str.replace("Case Number:", "", literal=True)
                    .str.replace(r"C$", "")
                    .str.strip_chars()
                    .alias("Name"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)(SSN\:)(.{0,100})(Alias 1)", group_index=2)
                    .str.replace("\n", "")
                    .str.strip_chars()
                    .alias("Alias"),
                    pl.col("AllPagesText")
                    .str.extract(r"Alias 2: (.+)")
                    .str.strip_chars()
                    .alias("Alias2"),
                    pl.col("AllPagesText")
                    .str.extract(r"(\d{2}/\d{2}/\d{4})(?:.{0,5}DOB:)", group_index=1)
                    .str.replace(r"[^\d/]", "")  # _all
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("DOB"),
                    pl.concat_str(
                        [
                            pl.col("AllPagesText").str.extract(
                                r"(County: )(\d{2})", group_index=2
                            ),
                            pl.lit("-"),
                            pl.col("AllPagesText").str.extract(
                                r"(\w{2}\-\d{4}\-\d{6}\.\d{2})"
                            ),
                        ]
                    ).alias("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"(Phone: )(.+)", group_index=2)
                    .str.replace_all(r"[^0-9]", "")
                    .str.slice(0, 10)
                    .str.replace(r"(.{3}0000000)", "")
                    .alias("RE_Phone"),
                    pl.col("AllPagesText")
                    .str.extract(r"(B|W|H|A)/(?:F|M)")
                    .alias("Race"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?:B|W|H|A)/(F|M)")
                    .alias("Sex"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?:Address 1:)(.+)(?:Phone)*?", group_index=1)
                    .str.replace(r"(Phone.+)", "")
                    .str.strip_chars()
                    .alias("Address1"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?:Address 2:)(.+)")
                    .str.strip_chars()
                    .alias("Address2"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?:Zip: )(.+)", group_index=1)
                    .str.replace(r"[A-Za-z\:\s]+", "")
                    .str.strip_chars()
                    .alias("ZipCode"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?:City: )(.*)(?:State: )(.*)", group_index=1)
                    .str.strip_chars()
                    .alias("City"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?:City: )(.*)(?:State: )(.*)", group_index=2)
                    .str.strip_chars()
                    .alias("State"),
                    pl.col("AllPagesText")
                    .str.extract(r"(Total:.+\-?\$[^\n]*)")
                    .str.replace_all(r"[^0-9|\.|\s|\$]", "")
                    .str.extract_all(r"\s\-?\$\d+\.\d{2}")
                    .alias("TOTALS"),
                    pl.col("AllPagesText")
                    .str.extract(r"(ACTIVE[^\n]+D999[^\n]+)")
                    .str.extract_all(r"\-?\$\d+\.\d{2}")
                    .list.get(-1)
                    .str.replace(r"[\$\s]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("D999RAW"),
                    pl.col("AllPagesText")
                    .str.extract(r"Related Cases: (.+)")
                    .str.strip_chars()
                    .alias("RelatedCases"),
                    pl.col("AllPagesText")
                    .str.extract(r"Filing Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("FilingDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Case Initiation Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("CaseInitiationDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Arrest Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ArrestDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Offense Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("OffenseDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Indictment Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("IndictmentDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Youthful Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("YouthfulDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"(\d+)\s*\n\s*Youthful Date:")
                    .str.strip_chars()
                    .alias("ALInstitutionalServiceNum"),
                    pl.col("AllPagesText")
                    .str.extract(r"Alacourt\.com (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("Retrieved"),
                    pl.col("AllPagesText")
                    .str.extract(r"Jury Demand: ([A-Za-z]+)")
                    .alias("JuryDemand"),
                    pl.col("AllPagesText")
                    .str.extract(r"Grand Jury Court Action:(.+)")
                    .str.replace(r"Inpatient.+", "")
                    .str.strip_chars()
                    .alias("GrandJuryCourtAction"),
                    pl.col("AllPagesText")
                    .str.extract(r"Inpatient Treatment Ordered: (YES|NO)")
                    .alias("InpatientTreatmentOrdered"),
                    pl.col("AllPagesText")
                    .str.extract(r"Trial Type: ([A-Z\s]+)")
                    .str.replace(r"\n?\s*[PS]$", "")
                    .str.strip_chars()
                    .alias("TrialType"),
                    pl.col("AllPagesText")
                    .str.extract(r"Case Number: (.+)\s*\n*\s*County:")
                    .str.strip_chars()
                    .alias("County"),
                    pl.col("AllPagesText")
                    .str.extract(r"Judge: (.+)")
                    .str.rstrip("T")
                    .str.strip_chars()
                    .alias("Judge"),
                    pl.col("AllPagesText")
                    .str.extract(r"Probation Office \#: ([0-9\-]+)")
                    .alias("ProbationOffice#"),
                    pl.col("AllPagesText")
                    .str.extract(r"Defendant Status: ([A-Z\s]+)")
                    .str.rstrip("J")
                    .str.replace(r"\n", " ")
                    .str.replace(r"\s+", " ")
                    .str.strip_chars()
                    .alias("DefendantStatus"),
                    pl.col("AllPagesText")
                    .str.extract(r"([^0-9]+) Arresting Agency Type:")
                    .str.replace(r"^\-.+", "")
                    .str.replace(r"County\:", "")
                    .str.replace(r"Defendant Status\:", "")
                    .str.replace(r"Judge\:", "")
                    .str.replace(r"Trial Type\:", "")
                    .str.replace(r"Probation Office \#\:", "")
                    .str.strip_chars()
                    .alias("ArrestingAgencyType"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+) City Code/Name")
                    .str.strip_chars()
                    .alias("CityCodeName"),
                    pl.col("AllPagesText")
                    .str.extract(r"Arresting Officer: (.+)")
                    .str.strip_chars()
                    .alias("ArrestingOfficer"),
                    pl.col("AllPagesText")
                    .str.extract(r"Grand Jury: (.+)")
                    .str.strip_chars()
                    .alias("GrandJury"),
                    pl.col("AllPagesText")
                    .str.extract(r"Probation Office Name: ([A-Z0-9]+)")
                    .alias("ProbationOfficeName"),
                    pl.col("AllPagesText")
                    .str.extract(r"Traffic Citation \#: (.+)")
                    .str.strip_chars()
                    .alias("TrafficCitation#"),
                    pl.col("AllPagesText")
                    .str.extract(r"DL Destroy Date: (.+?)Traffic Citation #:")
                    .str.strip_chars()
                    .alias("DLDestroyDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Previous DUI Convictions: (\d{3})")
                    .str.strip_chars()
                    .cast(pl.Int64, strict=False)
                    .alias("PreviousDUIConvictions"),
                    pl.col("AllPagesText")
                    .str.extract(r"Case Initiation Type: ([A-Z\s]+)")
                    .str.rstrip("J")
                    .str.strip_chars()
                    .alias("CaseInitiationType"),
                    pl.col("AllPagesText")
                    .str.extract(r"Domestic Violence: (YES|NO)")
                    .alias("DomesticViolence"),
                    pl.col("AllPagesText")
                    .str.extract(r"Agency ORI: (.+)")
                    .str.replace(r"\n", "")
                    .str.replace_all(r"\s+", " ")
                    .str.strip_chars()
                    .alias("AgencyORI"),
                    pl.col("AllPagesText")
                    .str.extract(r"Driver License N°: (.+)")
                    .str.strip_chars()
                    .alias("DriverLicenseNo"),
                    pl.col("AllPagesText")
                    .str.extract(r"([X\d]{3}-[X\d]{2}-[X\d]{4})")
                    .alias("SSN"),
                    pl.col("AllPagesText")
                    .str.extract(r"([A-Z0-9]{11}?) State ID:")
                    .alias("StateID"),
                    pl.col("AllPagesText")
                    .str.extract(r"Weight: (\d*)", group_index=1)
                    .cast(pl.Int64, strict=False)
                    .alias("Weight"),
                    pl.col("AllPagesText")
                    .str.extract(r"Height ?: (\d'\d{2}\")")
                    .alias("Height"),
                    pl.col("AllPagesText")
                    .str.extract(r"Eyes/Hair: (\w{3})/(\w{3})", group_index=1)
                    .alias("Eyes"),
                    pl.col("AllPagesText")
                    .str.extract(r"Eyes/Hair: (\w{3})/(\w{3})", group_index=2)
                    .alias("Hair"),
                    pl.col("AllPagesText")
                    .str.extract(r"Country: (\w*+)")
                    .str.replace(r"(Enforcement|Party)", "")
                    .str.strip_chars()
                    .alias("Country"),
                    pl.col("AllPagesText")
                    .str.extract(r"(\d\d?/\d\d?/\d\d\d\d) Warrant Issuance Date:")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("WarrantIssuanceDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Warrant Action Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("WarrantActionDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Warrant Issuance Status: (\w+)")
                    .str.replace(r"Description", "")
                    .str.strip_chars()
                    .alias("WarrantIssuanceStatus"),
                    pl.col("AllPagesText")
                    .str.extract(r"Warrant Action Status: (\w+)")
                    .str.replace(r"Description", "")
                    .str.strip_chars()
                    .alias("WarrantActionStatus"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"Warrant Location Date: (.+?)Warrant Location Status:"
                    )
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("WarrantLocationDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Warrant Location Status: (\w+)")
                    .str.replace(r"Description", "")
                    .str.strip_chars()
                    .alias("WarrantLocationStatus"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Number Of Warrants: (.+?)(Number|Orgin)",
                        group_index=1,
                    )
                    .str.extract(
                        r"(ALIAS WARRANT|BENCH WARRANT"
                        r"|FAILURE TO PAY WARRANT|PROBATION WARRANT)"
                    )
                    .alias("WarrantIssuanceDescription"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Number Of Warrants: (.+?)(Number|Orgin)",
                        group_index=1,
                    )
                    .str.extract(
                        r"(WARRANT RECALLED|WARRANT DELAYED"
                        r"|WARRANT RETURNED|WARRANT SERVED)"
                    )
                    .alias("WarrantActionDescription"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Number Of Warrants: (.+?)(Number|Orgin)",
                        group_index=1,
                    )
                    .str.extract(r"(CLERK'S OFFICE|LAW ENFORCEMENT)")
                    .alias("WarrantLocationDescription"),
                    pl.col("AllPagesText")
                    .str.extract(r"Number Of Warrants: (\d{3}\s\d{3})")
                    .str.strip_chars()
                    .alias("NumberOfWarrants"),
                    pl.col("AllPagesText")
                    .str.extract(r"Bond Type: (\w+)")  # +
                    .str.replace(r"Bond", "")
                    .str.strip_chars()
                    .alias("BondType"),
                    pl.col("AllPagesText")
                    .str.extract(r"Bond Type Desc: ([A-Z\s]+)")
                    .str.strip_chars()
                    .alias("BondTypeDesc"),
                    pl.col("AllPagesText")
                    .str.extract(r"([\d\.]+) Bond Amount:")
                    .cast(pl.Float64, strict=False)
                    .alias("BondAmount"),
                    pl.col("AllPagesText")
                    .str.extract(r"Bond Company: ([A-Z0-9]+)")
                    .str.rstrip("S")
                    .alias("BondCompany"),
                    pl.col("AllPagesText")
                    .str.extract(r"Surety Code: (.+)")
                    .str.replace(r"Release.+", "")
                    .str.strip_chars()
                    .alias("SuretyCode"),
                    pl.col("AllPagesText")
                    .str.extract(r"Release Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("BondReleaseDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Failed to Appear Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("FailedToAppearDate"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"Bondsman Process Issuance: ([^\n]*?) Bondsman Process Return:"
                    )
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("BondsmanProcessIssuance"),
                    pl.col("AllPagesText")
                    .str.extract(r"Bondsman Process Return: (.+)")
                    .str.replace(r"Number.+", "")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("BondsmanProcessReturn"),
                    pl.col("AllPagesText")
                    .str.extract(r"([\n\s/\d]*?) Appeal Court:")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("AppealDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"([A-Z\-\s]+) Appeal Case Number")
                    .str.strip_chars()
                    .alias("AppealCourt"),
                    pl.col("AllPagesText")
                    .str.extract(r"Orgin Of Appeal: ([A-Z\-\s]+)")
                    .str.rstrip("L")
                    .str.strip_chars()
                    .alias("OriginOfAppeal"),
                    pl.col("AllPagesText")
                    .str.extract(r"Appeal To Desc: ([A-Z\-\s]+)")
                    .str.replace(r"[\s\n]+[A-Z0-9]$", "")
                    .str.replace(r" \w$", "")
                    .str.replace(r"^\w$", "")
                    .str.strip_chars()
                    .alias("AppealToDesc"),
                    pl.col("AllPagesText")
                    .str.extract(r"Appeal Status: ([A-Z\-\s]+)")
                    .str.rstrip("A")
                    .str.replace_all(r"\n", "")
                    .str.strip_chars()
                    .alias("AppealStatus"),
                    pl.col("AllPagesText")
                    .str.extract(r"Appeal To: (\w*) Appeal")
                    .str.strip_chars()
                    .alias("AppealTo"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+)LowerCourt Appeal Date:")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("LowerCourtAppealDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Disposition Type Of Appeal: ([^A-Za-z]+)")
                    .str.replace_all(r"[\n\s:\-]", "")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("DispositionDateOfAppeal"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"Disposition Date Of Appeal: (.+?) Disposition Type Of Appeal"
                    )
                    .str.strip_chars()
                    .alias("DispositionTypeOfAppeal"),
                    pl.col("AllPagesText")
                    .str.extract(r"Number of Subponeas: (\d{3})")
                    .str.replace_all(r"[^0-9]", "")
                    .str.strip_chars()
                    .cast(pl.Int64, strict=False)
                    .alias("NumberOfSubpoenas"),
                    pl.col("AllPagesText")
                    .str.extract(r"Updated By: (\w{3})")
                    .str.strip_chars()
                    .alias("AdminUpdatedBy"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+)Transfer to Admin Doc Date:")
                    .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("TransferToAdminDocDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+)Transfer Reason:")
                    .str.strip_chars()
                    .alias("TransferReason"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Administrative Information.+?Last Update:"
                        r" (\d\d?/\d\d?/\d\d\d\d)"
                    )
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("AdminLastUpdate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Transfer Desc: (.+)")
                    .str.replace(r"\d\d/\d\d/\d\d\d\d.+", "")
                    .str.replace(r"Transfer.+", "")
                    .str.strip_chars()
                    .alias("TransferDesc"),
                    pl.col("AllPagesText")
                    .str.extract(r"Date Trial Began but No Verdict \(TBNV1\): ([^\n]+)")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("TBNV1"),
                    pl.col("AllPagesText")
                    .str.extract(r"Date Trial Began but No Verdict \(TBNV2\): ([^\n]+)")
                    .str.replace(r"Financial", "")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("TBNV2"),
                    pl.col("AllPagesText")
                    .str.extract(r"Appeal Case Number: (.+)")
                    .str.strip_chars()
                    .alias("AppealCaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"Continuance Date\s*\n*\s*(\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ContinuanceDate"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"Continuance Reason\s*\n*\s*"
                        r"([A-Z0-9]{2}/[A-Z0-9]{2}/[A-Z0-9]{4})"
                    )
                    .alias("ContinuanceReason"),
                    pl.col("AllPagesText")
                    .str.extract(r"Description:(.+?)Number of Previous Continuances:")
                    .str.strip_chars()
                    .alias("ContinuanceDescription"),
                    pl.col("AllPagesText")
                    .str.extract(r"Number of Previous Continuances:\s*\n*\s(\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("NumberOfPreviousContinuances"),
                    pl.col("AllPagesText")
                    .str.contains(r"(?s)Fee Sheet (.+Total:[^\n]+)")
                    .alias("HasFeeSheet"),
                )
                # blank county
                .with_columns(
                    pl.when(pl.col("County").eq("") | pl.col("County").is_null())
                    .then(
                        pl.col("AllPagesText").str.extract(
                            r"\w\w-\d\d\d\d-\d\d\d\d\d\d\.\d\d (.+?) Case Number"
                        )
                    )
                    .otherwise(pl.col("County"))
                    .alias("County")
                )
                .with_columns(
                    pl.col("CaseNumber")
                    .str.extract(r"([A-Z]{2})")
                    .map_dict(case_types)
                    .alias("Type")
                )
                # TR only fields
                .with_columns(
                    pl.col("AllPagesText")
                    .str.extract(r"Suspension Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SuspensionDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Speed: (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("Speed"),
                    pl.col("AllPagesText")
                    .str.extract(r"Completion Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("CompletionDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Clear Date: (\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ClearDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"Speed Limit: (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("SpeedLimit"),
                    pl.col("AllPagesText")
                    .str.extract(
                        (
                            r"Blood Alcohol Content: Completion Date: ?"
                            r"(\d\d?/\d\d?/\d\d\d\d)? (\d+\.\d\d\d)"
                        ),
                        group_index=2,
                    )
                    .cast(pl.Float64, strict=False)
                    .alias("BloodAlcoholContent"),
                    pl.col("AllPagesText")
                    .str.extract(r"Ticket Number: (.+)")
                    .str.strip_chars()
                    .alias("TicketNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"Rule 20: (.+?) Clear Date:")
                    .str.strip_chars()
                    .alias("Rule20"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)Collection Status: (.+?) \d\d?/\d\d?/\d\d\d\d")
                    .str.replace(r"\n", "")
                    .str.replace_all(r"\s+", " ")
                    .str.strip_chars()
                    .str.replace(r"DOB:.+", "")
                    .alias("CollectionStatus"),
                    pl.col("AllPagesText")
                    .str.extract(r"Tag Number: (.+?) Vehicle Desc:")
                    .str.strip_chars()
                    .alias("VehicleDesc"),
                    pl.col("AllPagesText")
                    .str.extract(r"Vehicle State: (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("VehicleState"),
                    pl.col("AllPagesText")
                    .str.extract(r"Driver License Class: (.+)")
                    .str.replace(r"/.+", "")
                    .str.strip_chars()
                    .alias("DriverLicenseClass"),
                    pl.col("AllPagesText")
                    .str.extract(r"Commercial Vehicle: (YES|NO|UNKNOWN)")
                    .alias("CommercialVehicle"),
                    pl.col("AllPagesText")
                    .str.extract(r"([A-Z0-9]+) Tag Number:")
                    .alias("TagNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"Vehicle Year: (.+?) ?Vehicle State:")
                    .str.strip_chars()
                    .alias("VehicleYear"),
                    pl.col("AllPagesText")
                    .str.extract(r"(YES|NO) Passengers Present:")
                    .alias("PassengersPresent"),
                    pl.col("AllPagesText")
                    .str.extract(r"Commercial Driver License Required: (YES|NO)")
                    .alias("CommercialDriverLicenseRequired"),
                    pl.col("AllPagesText")
                    .str.extract(r"Hazardous Materials: (YES|NO)")
                    .alias("HazardousMaterials"),
                )
                .with_columns(
                    pl.when(pl.col("D999RAW").is_null())
                    .then(pl.lit(0))
                    .otherwise(pl.col("D999RAW"))
                    .alias("D999")
                )
                # non-criminal fields
                .with_columns(
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)[A-Z]{2}-\d{4}-\d{6}\.\d\d\s*\n([^\n]+)")
                    .str.replace_all(r"(\s+)", " ")
                    .str.strip_chars()
                    .alias("Style"),
                    pl.col("AllPagesText")
                    .str.extract(r"Filed: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("FiledDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"(\d+) No of Plaintiffs:")
                    .cast(pl.Int64, strict=False)
                    .alias("NoOfPlaintiffs"),
                    pl.col("AllPagesText")
                    .str.extract(r"No of Defendants: (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("NoOfDefendants"),
                    pl.col("AllPagesText")
                    .str.extract(r"Case Status: (.+)")
                    .str.strip_chars()
                    .alias("CaseStatus"),
                    pl.col("AllPagesText")
                    .str.extract(r"Track: (.+)")
                    .str.strip_chars()
                    .alias("Track"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+) Case Type:")
                    .str.replace(r"Filed: (\d\d/\d\d/\d\d\d\d)?", "")
                    .str.strip_chars()
                    .alias("CaseType"),
                    pl.col("AllPagesText")
                    .str.extract(r"Appellate Case: (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("AppellateCase"),
                    pl.col("AllPagesText")
                    .str.extract(r"Damage Amt: ([\d\.]+)")
                    .cast(pl.Float64, strict=False)
                    .alias("DamageAmt"),
                    pl.col("AllPagesText")
                    .str.extract(r"([\d\.]+) Punitive Damages:")
                    .cast(pl.Float64, strict=False)
                    .alias("PunitiveDamages"),
                    pl.col("AllPagesText")
                    .str.extract(r"([\d\.]+) Compensatory Damages:")
                    .cast(pl.Float64, strict=False)
                    .alias("CompensatoryDamages"),
                    pl.col("AllPagesText")
                    .str.extract(r"General Damages: ([\d\.]+)")
                    .cast(pl.Float64, strict=False)
                    .alias("GeneralDamages"),
                    pl.col("AllPagesText")
                    .str.extract(r"No Damages: (.+)")
                    .str.strip_chars()
                    .alias("NoDamages"),
                    pl.col("AllPagesText")
                    .str.extract(r"Payment Frequency: (\w) ")
                    .str.strip_chars()
                    .alias("PaymentFrequency"),
                    pl.col("AllPagesText")
                    .str.extract(r"Cost Paid By: (.+)")
                    .str.strip_chars()
                    .alias("CostPaidBy"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+) Court Action Code:")
                    .str.strip_chars()
                    .alias("CourtActionCode"),
                    pl.col("AllPagesText")
                    .str.extract(r"Num of Trial days: (.+)")
                    .str.strip_chars()
                    .cast(pl.Int64, strict=False)
                    .alias("NumOfTrialDays"),
                    pl.col("AllPagesText")
                    .str.extract(r"Court Action Desc: (.+?) Court Action Date")
                    .str.strip_chars()
                    .alias("CourtActionDesc"),
                    pl.col("AllPagesText")
                    .str.extract(r"Judgment For: (.+?)Num")
                    .str.strip_chars()
                    .alias("JudgmentFor"),
                    pl.col("AllPagesText")
                    .str.extract(r"Disposition Judge:(.+)")
                    .str.replace(r"Minstral.+", "")
                    .str.strip_chars()
                    .alias("DispositionJudge"),
                    pl.col("AllPagesText")
                    .str.extract(r"Minstral: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("Minstral"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+) Comment 1:")
                    .str.strip_chars()
                    .alias("Comment1"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+) Comment 2:")
                    .str.strip_chars()
                    .alias("Comment2"),
                    pl.col("AllPagesText")
                    .str.extract(r"Orgin of Case: (.+)")
                    .str.strip_chars()
                    .alias("OriginOfCase"),
                    pl.col("AllPagesText")
                    .str.extract(r"Support: (.+)")
                    .str.strip_chars()
                    .alias("Support"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+) UIFSA:")
                    .str.strip_chars()
                    .alias("UIFSA"),
                    pl.col("AllPagesText")
                    .str.extract(r"ADC: (.+)")
                    .str.strip_chars()
                    .alias("ADC"),
                    pl.col("AllPagesText")
                    .str.extract(r"Contempt: (.+)")
                    .str.strip_chars()
                    .alias("Contempt"),
                    pl.col("AllPagesText")
                    .str.extract(r"Legal Separation: (.+)")
                    .str.strip_chars()
                    .alias("LegalSeparation"),
                    pl.col("AllPagesText")
                    .str.extract(r"Annulment: (.+)")
                    .str.strip_chars()
                    .alias("Annulment"),
                    pl.col("AllPagesText")
                    .str.extract(r"(.+)Modification:")
                    .str.strip_chars()
                    .alias("DNATest"),
                    pl.col("AllPagesText")
                    .str.extract(r"Arrearage: (.+?)Garnishment:")
                    .str.strip_chars()
                    .alias("Arrearage"),
                    pl.col("AllPagesText")
                    .str.extract(r"Paternity: (.)")
                    .alias("Paternity"),
                    pl.col("AllPagesText")
                    .str.extract(r"Imcome Withholding Order: (.+?) Paternity:")
                    .alias("IncomeWithholdingOrder"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Department of Human Resources(.+?)(Parties|Settings)",
                        group_index=1,
                    )
                    .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("FirstDate"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)Orgin of Case:[^\n]+\n([^\n]+)")
                    .str.extract(r"([A-Z]-[A-Z]+)")
                    .alias("Custody"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Department of Human Resources(.+?)(Parties|Settings)",
                        group_index=1,
                    )
                    .str.extract(r"\d\d?/\d\d?/\d\d\d\d (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("NoOfChildren"),
                )
                # mask random names from non-criminal fields
                .with_columns(
                    pl.when(
                        pl.col("Type").is_in(
                            [
                                "Child Support",
                                "Equity Cases",
                                "Small Claims",
                                "District Civil",
                                "Circuit Civil",
                                "District Civil",
                                "Domestic Relations",
                            ]
                        )
                    )
                    .then(pl.lit(None))
                    .otherwise(pl.col("Name"))
                    .alias("Name")
                )
                # clean columns, unnest totals
                .with_columns(
                    pl.col("RE_Phone")
                    .str.replace_all(r"[^0-9]|2050000000", "")
                    .alias("CLEAN_Phone"),
                    pl.concat_str([pl.col("Address1"), pl.lit(" "), pl.col("Address2")])
                    .str.replace_all(
                        r"JID: \w{3} Hardship.*|Defendant Information.*", ""
                    )
                    .str.strip_chars()
                    .alias("StreetAddress"),
                    pl.col("Name"),
                    pl.col("TOTALS")
                    .list.get(0)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalAmtDue"),
                    pl.col("TOTALS")
                    .list.get(1)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalAmtPaid"),
                    pl.col("TOTALS")
                    .list.get(2)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalBalance"),
                    pl.col("TOTALS")
                    .list.get(3)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalAmtHold"),
                )
                .with_columns(
                    pl.when(pl.col("CLEAN_Phone").str.n_chars() < 7)
                    .then(None)
                    .otherwise(pl.col("CLEAN_Phone"))
                    .alias("Phone"),
                )
                .with_columns(
                    pl.when(pl.col("HasFeeSheet").not_())
                    .then(pl.lit(None))
                    .otherwise(pl.col("D999"))
                    .alias("D999")
                )
                .filter(pl.col("CaseNumber").is_not_null())
                .fill_null("")
            )
            if not debug:
                cases = cases.select(
                    "Retrieved",
                    "Type",
                    "CaseNumber",
                    "Style",
                    "Name",
                    "Alias",
                    "Alias2",
                    "DOB",
                    "Race",
                    "Sex",
                    "TotalAmtDue",
                    "TotalAmtPaid",
                    "TotalBalance",
                    "TotalAmtHold",
                    "D999",
                    "BondAmount",
                    "Phone",
                    "StreetAddress",
                    "City",
                    "State",
                    "ZipCode",
                    "County",
                    "Country",
                    "SSN",
                    "Weight",
                    "Height",
                    "Eyes",
                    "Hair",
                    "FilingDate",
                    "CaseInitiationDate",
                    "ArrestDate",
                    "SuspensionDate",
                    "Speed",
                    "CompletionDate",
                    "OffenseDate",
                    "IndictmentDate",
                    "YouthfulDate",
                    "ALInstitutionalServiceNum",
                    "JuryDemand",
                    "GrandJuryCourtAction",
                    "InpatientTreatmentOrdered",
                    "TrialType",
                    "Judge",
                    "DefendantStatus",
                    "RelatedCases",
                    "ArrestingAgencyType",
                    "CityCodeName",
                    "ArrestingOfficer",
                    "ClearDate",
                    "SpeedLimit",
                    "BloodAlcoholContent",
                    "TicketNumber",
                    "Rule20",
                    "CollectionStatus",
                    "GrandJury",
                    "ProbationOffice#",
                    "ProbationOfficeName",
                    "TrafficCitation#",
                    "DLDestroyDate",
                    "PreviousDUIConvictions",
                    "VehicleDesc",
                    "VehicleState",
                    "DriverLicenseClass",
                    "CommercialVehicle",
                    "TagNumber",
                    "VehicleYear",
                    "PassengersPresent",
                    "CommercialDriverLicenseRequired",
                    "HazardousMaterials",
                    "CaseInitiationType",
                    "DomesticViolence",
                    "AgencyORI",
                    "WarrantIssuanceDate",
                    "WarrantActionDate",
                    "WarrantLocationDate",
                    "WarrantIssuanceStatus",
                    "WarrantActionStatus",
                    "WarrantLocationStatus",
                    "WarrantIssuanceDescription",
                    "WarrantActionDescription",
                    "WarrantLocationDescription",
                    "NumberOfWarrants",
                    "BondType",
                    "BondTypeDesc",
                    "BondCompany",
                    "SuretyCode",
                    "BondReleaseDate",
                    "FailedToAppearDate",
                    "BondsmanProcessIssuance",
                    "BondsmanProcessReturn",
                    "AppealDate",
                    "AppealCourt",
                    "LowerCourtAppealDate",
                    "OriginOfAppeal",
                    "AppealToDesc",
                    "AppealStatus",
                    "AppealTo",
                    "DispositionDateOfAppeal",
                    "DispositionTypeOfAppeal",
                    "NumberOfSubpoenas",
                    "AdminUpdatedBy",
                    "AdminLastUpdate",
                    "TransferToAdminDocDate",
                    "TransferDesc",
                    "TransferReason",
                    "TBNV1",
                    "TBNV2",
                    "DriverLicenseNo",
                    "StateID",
                    "AppealCaseNumber",
                    "ContinuanceDate",
                    "ContinuanceReason",
                    "ContinuanceDescription",
                    "NumberOfPreviousContinuances",
                    "FiledDate",
                    "NoOfPlaintiffs",
                    "NoOfDefendants",
                    "CaseStatus",
                    "Track",
                    "CaseType",
                    "AppellateCase",
                    "DamageAmt",
                    "PunitiveDamages",
                    "CompensatoryDamages",
                    "GeneralDamages",
                    "NoDamages",
                    "PaymentFrequency",
                    "CostPaidBy",
                    "CourtActionCode",
                    "NumOfTrialDays",
                    "CourtActionDesc",
                    "JudgmentFor",
                    "DispositionJudge",
                    "Minstral",
                    "Comment1",
                    "Comment2",
                    "FirstDate",
                    "OriginOfCase",
                    "Support",
                    "UIFSA",
                    "ADC",
                    "Contempt",
                    "LegalSeparation",
                    "Annulment",
                    "DNATest",
                    "Arrearage",
                    "Paternity",
                    "IncomeWithholdingOrder",
                    "Custody",
                    "NoOfChildren",
                )
        self._cases = cases
        return self._cases

    def fees(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make fee sheets table."""
        if debug:
            self._fees = None
        # if previously called with debug=True, reset
        if isinstance(self._fees, pl.DataFrame) and "FeeSheet" in self._fees.columns:
            self._fees = None
        if isinstance(self._fees, pl.DataFrame):
            return self._fees
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing fee sheets…"):
            df = (
                self.archive.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)Fee Sheet (.+Total:[^\n]+)")
                    .str.replace(
                        (
                            r"\s*\n\s*Admin Fee Balance Garnish Party Amount Due Fee"
                            r" Code Payor Amount Paid"
                        ),
                        "",
                    )
                    .str.replace(r"^\s*\n", "")
                    .str.replace(
                        "Fee Status Amount Hold Payee Admin Fee Balance Garnish"
                        " Party Amount Due Fee Code Payor Amount Paid",
                        "",
                    )
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.replace_all(r"\.\s*\n\s*", ".")
                    .str.strip_chars()
                    .str.split("\n")
                    .alias("FeeSheet"),
                )
                .explode("FeeSheet")
                .with_columns(pl.col("FeeSheet").str.strip_chars())
                # non-total rows
                .with_columns(
                    pl.col("FeeSheet")
                    .str.extract(r"^(I?N?ACTIVE|Total:)")
                    .alias("FeeStatus"),
                    pl.col("FeeSheet")
                    .str.extract(r"^(I?N?ACTIVE)?\s*([YN])", group_index=2)
                    .alias("AdminFee"),
                    pl.col("FeeSheet")
                    .str.extract(
                        r"^(I?N?ACTIVE)?\s*([YN])?[\$\d\.,\s\-]+([A-Z0-9]{4})",
                        group_index=3,
                    )
                    .alias("FeeCode"),
                    pl.col("FeeSheet")
                    .str.extract(
                        r"([A-Z0-9]{4}) \d* ?\-?\$[\d,]+\.\d\d (I?N?ACTIVE)?\s*[YN]?\s",
                        group_index=1,
                    )
                    .alias("Payor"),
                    pl.col("FeeSheet")
                    .str.extract(
                        (
                            r"([A-Z0-9]{4})\s*([A-Z0-9]+)\s*([A-Z0-9]{4})"
                            r" \d* ?\-?\$[\d,]+\.\d\d (I?N?ACTIVE)?\s*[YN]?\s"
                        ),
                        group_index=2,
                    )
                    .alias("Payee"),
                    pl.col("FeeSheet")
                    .str.extract(
                        r" (\d*) ?\-?\$[\d,]+\.\d\d (I?N?ACTIVE)?\s*[YN]?\s",
                        group_index=1,
                    )
                    .cast(pl.Int64, strict=False)
                    .alias("GarnishParty"),
                    pl.col("FeeSheet")
                    .str.extract(
                        r"^(I?N?ACTIVE)?\s*([YN]?) (\-?\$[\d,]+\.\d\d)",
                        group_index=3,
                    )
                    .str.replace(",", "")
                    .str.replace(r"\$", "")
                    .cast(pl.Float64, strict=False)
                    .alias("AmountDue"),
                    pl.col("FeeSheet")
                    .str.extract(
                        r"^(I?N?ACTIVE)?\s*([YN]?) (\-?\$[\d,]+\.\d\d)"
                        r" (\-?\$[\d,]+\.\d\d)",
                        group_index=4,
                    )
                    .str.replace(",", "")
                    .str.replace(r"\$", "")
                    .cast(pl.Float64, strict=False)
                    .alias("AmountPaid"),
                    pl.col("FeeSheet")
                    .str.extract(r"(\-?\$[\d,]+\.\d\d)$")
                    .str.replace(",", "")
                    .str.replace(r"\$", "")
                    .cast(pl.Float64, strict=False)
                    .alias("Balance"),
                    pl.col("FeeSheet")
                    .str.extract(
                        (
                            r"^(I?N?ACTIVE)?\s*([YN]?) (\-?\$[\d,]+\.\d\d)"
                            r" (\-?\$[\d,]+\.\d\d) (\-?\$[\d,]+\.\d\d)"
                        ),
                        group_index=5,
                    )
                    .str.replace(",", "")
                    .str.replace(r"\$", "")
                    .cast(pl.Float64, strict=False)
                    .alias("AmountHold"),
                )
                # total rows
                .with_columns(
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(r"(\-?\$[\d,]+\.\d\d)")
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountDue"))
                    .alias("AmountDue"),
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"(\-?\$[\d,]+\.\d\d) (\-?\$[\d,]+\.\d\d)",
                            group_index=2,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountPaid"))
                    .alias("AmountPaid"),
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"(\-?\$[\d,]+\.\d\d) (\-?\$[\d,]+\.\d\d)"
                            r" (\-?\$[\d,]+\.\d\d)",
                            group_index=3,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("Balance"))
                    .alias("Balance"),
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            (
                                r"(\-?\$[\d,]+\.\d\d) (\-?\$[\d,]+\.\d\d)"
                                r" (\-?\$[\d,]+\.\d\d)"
                                r" (\-?\$[\d,]+\.\d\d)"
                            ),
                            group_index=4,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountHold"))
                    .alias("AmountHold"),
                )
                # total rows shift blank amount due
                .with_columns(
                    pl.when(
                        pl.col("FeeSheet").str.contains(
                            r"Total:\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d$"
                        )
                    )
                    .then(None)
                    .otherwise(pl.col("AmountDue"))
                    .alias("AmountDue"),
                    pl.when(
                        pl.col("FeeSheet").str.contains(
                            r"Total:\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d$"
                        )
                    )
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"Total:\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)$",
                            group_index=1,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountPaid"))
                    .alias("AmountPaid"),
                    pl.when(
                        pl.col("FeeSheet").str.contains(
                            r"Total:\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d$"
                        )
                    )
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"Total:\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)$",
                            group_index=2,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("Balance"))
                    .alias("Balance"),
                    pl.when(
                        pl.col("FeeSheet").str.contains(
                            r"Total:\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d\s*\-?\$\d+\.\d\d$"
                        )
                    )
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"Total:\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)$",
                            group_index=3,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountHold"))
                    .alias("AmountHold"),
                )
                # add total column
                .with_columns(
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(pl.lit("Total:"))
                    .otherwise(None)
                    .alias("Total")
                )
                .with_columns(
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(None)
                    .otherwise(pl.col("FeeStatus"))
                    .alias("FeeStatus")
                )
                # if no admin fee and no fee status
                .with_columns(
                    pl.when(
                        pl.col("AdminFee").is_null()
                        & pl.col("FeeStatus").is_null()
                        & pl.col("Total").is_null()
                    )
                    .then(
                        pl.col("FeeSheet").str.extract(
                            r"[A-Z0-9]{4} ([A-Z0-9]{4})", group_index=1
                        )
                    )
                    .otherwise(pl.col("Payor"))
                    .alias("Payor"),
                    pl.when(
                        pl.col("AdminFee").is_null()
                        & pl.col("FeeStatus").is_null()
                        & pl.col("Total").is_null()
                    )
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(r"(\-?\$\d+\.\d\d)")
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountDue"))
                    .alias("AmountDue"),
                    pl.when(
                        pl.col("AdminFee").is_null()
                        & pl.col("FeeStatus").is_null()
                        & pl.col("Total").is_null()
                    )
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)", group_index=2
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountPaid"))
                    .alias("AmountPaid"),
                    pl.when(
                        pl.col("AdminFee").is_null()
                        & pl.col("FeeStatus").is_null()
                        & pl.col("Total").is_null()
                    )
                    .then(
                        pl.col("FeeSheet")
                        .str.extract(
                            r"(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)\s*(\-?\$\d+\.\d\d)",
                            group_index=3,
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                    )
                    .otherwise(pl.col("AmountHold"))
                    .alias("AmountHold"),
                )
            )
            if not debug:
                df = df.select(
                    "CaseNumber",
                    "Total",
                    "FeeStatus",
                    "AdminFee",
                    "FeeCode",
                    "Payor",
                    "Payee",
                    "AmountDue",
                    "AmountPaid",
                    "Balance",
                    "AmountHold",
                    "GarnishParty",
                )
            df = df.filter(pl.col("Balance").is_not_null())
        self._fees = df
        return self._fees

    def filing_charges(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make filing charges table."""
        if debug:
            self._filing_charges = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._filing_charges, pl.DataFrame)
            and "FilingCharges" in self._filing_charges.columns
        ):
            self._filing_charges = None
        # if already made, return
        if isinstance(self._filing_charges, pl.DataFrame):
            return self._filing_charges
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing filing charges…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract(
                    r"(?s)Filing Charges(.+?)"
                    r"(?:Disposition Charges|Sentences|Enforcement|Financial)"
                )
                .str.replace(
                    (
                        r"\n\s*# Code Description Cite Type Description Category ID"
                        r" Class\s*\n\s*"
                    ),
                    "",
                )
                .str.replace_all(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                .str.strip_chars()
                .alias("FilingCharges"),
                pl.col("AllPagesText")
                .str.extract(
                    r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                    group_index=1,
                )
                .str.replace("Case Number:", "", literal=True)
                .str.replace(r"C$", "")
                .str.strip_chars()
                .alias("Name"),
            ).drop_nulls("FilingCharges")
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("FilingCharges").map_elements(
                            lambda x: re.split(
                                (
                                    r"(?m)(ALCOHOL|BOND FORFEITURE|CONSERVATION"
                                    r"|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH"
                                    r"|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL"
                                    r"|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET"
                                    r"|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)"
                                    r"|BUSINESS|JUVENILE)\s*$"
                                ),
                                x,
                            )
                        )
                    )
                    .filter(pl.col("FilingCharges").list.len() > 0)
                    .drop_nulls("FilingCharges")
                    # Some charges only have ID and Code, e.g. ["001 WECN"].
                    # The split doesn't work for these charges with list length 1.
                    # Expr below sets Charge and Category correctly for those fields.
                    .with_columns(
                        pl.when(pl.col("FilingCharges").list.len() > 1)
                        .then(
                            pl.col("FilingCharges").map_elements(lambda x: x[::2][:-1])
                        )
                        .otherwise(pl.col("FilingCharges"))
                        .alias("Charge"),
                        pl.when(pl.col("FilingCharges").list.len() > 1)
                        .then(pl.col("FilingCharges").map_elements(lambda x: x[1::2]))
                        .otherwise(pl.Series([[""]]))
                        .alias("Category"),
                    )
                    .explode("Charge", "Category")
                    .with_columns(
                        pl.col("Charge").str.replace_all("\n", "").str.strip_chars()
                    )
                    .with_columns(
                        pl.col("Charge").str.extract(r"(\d+)").alias("#"),
                        pl.col("Charge").str.extract(r"\d+ ([A-Z0-9/]+)").alias("Code"),
                        pl.col("Charge")
                        .str.extract(
                            r"\d+ [A-Z0-9/]+ (.+?) [A-Z0-9]{3}-[A-Z0-9]{3}-"
                            r" *[A-Z0-9]{1,3}"
                        )
                        .str.replace(r"([\s-]+)$", "")
                        .str.strip_chars()
                        .alias("Description"),
                        pl.col("Charge")
                        .str.extract(
                            r"([A-Z0-9]{3}-[A-Z0-9]{3}-"
                            r" *[A-Z0-9]{1,3}\.?\s*\d*\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?)"
                        )
                        .str.replace_all(" ", "")
                        .str.replace(r"[A-Z]+$", "")
                        .alias("Cite"),
                        pl.col("Charge")
                        .str.extract(
                            r"(BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION)$"
                        )
                        .alias("TypeDescription"),
                    )
                    .drop_nulls("Charge")
                    .with_columns(
                        pl.when(pl.col("Description").is_null())
                        .then(
                            pl.col("Charge").str.extract(
                                (
                                    r"\d+ [A-Z0-9]+ (.+?) (BOND|FELONY"
                                    r"|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION)$"
                                ),
                                group_index=1,
                            )
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # replace stray \ with escape \\
                    .with_columns(pl.col("Description").str.replace(r"\\", "\\\\"))
                    # fix CFR cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Description").str.contains(r"\d+ CFR \d+")
                        )
                        .then(
                            pl.col("Description")
                            .str.extract(r"(\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)?)")
                            .str.replace(r"\. ", ".")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Description").str.contains(r"\d+ CFR \d+")
                        )
                        .then(
                            pl.col("Description").str.replace(
                                r"\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)?", ""
                            )
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix ACT XXXX-XX cite
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(ACT \d+-\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix PSC-.+ cite
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(PSC-\d[^\s]+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix SCR-\d+ cite
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(SCR-\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix 760-\d+ cite
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.extract(r"((DPS)? 760-X-.+)")
                            .str.replace("- ", "-")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix XXX-XXX$ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(\d+-\d[^\s]+$)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix RULE 32 cites and descriptions
                    .with_columns(
                        pl.when(pl.col("Description").str.contains("RULE 32"))
                        .then(pl.lit("RULE 32"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Description").str.contains("RULE 32"))
                        .then(pl.lit("RULE 32-FELONY"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix PROBATION REV cites and descriptions
                    .with_columns(
                        pl.when(pl.col("Description").str.contains("PROBATION REV"))
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Description").str.contains("PROBATION REV"))
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix COMMUNITY CORRECTION cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains(
                                "COMMUNITY CORRECTION REVOC"
                            )
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Description").str.contains(
                                "COMMUNITY CORRECTION REVOC"
                            )
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REVOC"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix OTHER NON MOVING VIO cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains("OTHER NON MOVING VIO")
                        )
                        .then(pl.lit("OTHER NON MOVING VIO"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MC cites at end of description
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.extract(r"(\d+\s*-\s*\d+\s*-\s*\d+$)")
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.replace(r"(\d+\s*-\s*\d+\s*-\s*\d+$)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix 000.000 cites at end of description
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(\d+\.\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.replace(r"(\d+\.\d+)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix PRE-CONV HABEAS CORPUS cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains("PRE-CONV HABEAS CORPUS")
                        )
                        .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Description").str.contains("PRE-CONV HABEAS CORPUS")
                        )
                        .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix HABEAS CORPUS cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains("HABEAS CORPUS")
                            & pl.col("Description").str.contains("PRE-CONV").not_()
                        )
                        .then(pl.lit("HABEAS CORPUS"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Description").str.contains("HABEAS CORPUS")
                            & pl.col("Description").str.contains("PRE-CONV").not_()
                        )
                        .then(pl.lit("HABEAS CORPUS"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix TRAFFIC/MISC missing description
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Charge").str.contains("TRAFFIC/MISC")
                        )
                        .then(pl.lit("TRAFFIC/MISC"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix BOND FORF
                    .with_columns(
                        pl.when(pl.col("Charge").str.contains("BOND FORF-MISD"))
                        .then(pl.lit("BOND FORF-MISD"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(pl.col("Charge").str.contains("BOND FORF-MISD"))
                        .then(pl.lit("BOND FORT"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix MUN- cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains(" MUN-")
                        )
                        .then(
                            pl.col("Charge")
                            .str.extract(r"(MUN-.+?) MISDEMEANOR$")
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains(" MUN-")
                        )
                        .then(
                            pl.col("Description")
                            .str.replace(r"MUN-.+", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix MUN-ICI-
                    .with_columns(
                        pl.when(pl.col("Cite") == "MUN-ICI-")
                        .then(pl.lit("MUN-ICI-PAL"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix HSV- cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains(" HSV-")
                        )
                        .then(
                            pl.col("Charge")
                            .str.extract(
                                r"(HSV-.+?) (MISDEMEANOR|VIOLATION)$",
                                group_index=1,
                            )
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains(" HSV-")
                        )
                        .then(
                            pl.col("Description")
                            .str.replace(r"(HSV-.+)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix ORD-AM cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains("ORD-AM")
                        )
                        .then(
                            pl.col("Charge").str.extract(
                                r"(ORD-AM.+?) (MISDEMEANOR|VIOLATION)"
                            )
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains("ORD-AM")
                        )
                        .then(
                            pl.col("Description")
                            .str.replace(r"(ORD-AM.+)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix missing description when cite is ---------
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Charge").str.contains("----")
                        )
                        .then(
                            pl.col("Charge").str.extract(r"---- (.+)").str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MUNICIPAL ORDINANCE extra stuff in description
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains("MUNICIPAL ORDINANCE")
                        )
                        .then(pl.lit("MUNICIPAL ORDINANCE"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MUNICIPAL cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains("MUNICIPAL")
                        )
                        .then(pl.col("Charge").str.extract(r"(MUNICIPAL)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix ACT\d+-\d+, SEC \d cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains(r"ACT\d+")
                        )
                        .then(pl.col("Charge").str.extract(r"(ACT\d+-\d+, SEC \d)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix PSC cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Charge").str.contains(r" PSC ")
                        )
                        .then(pl.col("Charge").str.extract(r" (PSC) "))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix RESERVED cites
                    .with_columns(
                        pl.when(
                            pl.col("Charge").str.contains("RESERVED")
                            & pl.col("Cite").is_null()
                        )
                        .then(pl.lit("RESERVED"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Charge").str.contains("RESERVED")
                            & pl.col("Description").is_null()
                        )
                        .then(
                            pl.col("Charge")
                            .str.extract(r"RESERVED (.+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # remove extra stuff from description
                    .with_columns(
                        pl.col("Description")
                        .str.replace(r"-+ +-+", "")
                        .str.replace(r"ADJUDICATIO +N", "")
                        .str.replace(r"(ACT \d+-\d+)", "")
                        .str.replace(r"(PSC-\d[^\s]+)", "")
                        .str.replace(r"(SCR-\d+)", "")
                        .str.replace(r"((DPS)? 760-X-.+)", "")
                        .str.replace(r"(\d+-\d[^\s]+$)", "")
                        .str.replace(r"^, FELONY SEC \d+", "")
                        .str.strip_chars()
                    )
                    # get ID column
                    .with_columns(
                        pl.col("Description").str.extract(r"^([ASCP]) ").alias("ID"),
                        pl.col("Description")
                        .str.replace(r"^([ASCP]) ", "")
                        .alias("Description"),
                    )
                    # fill null to prevent null bools
                    .fill_null("")
                    .with_columns(
                        pl.col("Charge").str.contains("FELONY").alias("Felony"),
                        (
                            pl.col("Description").str.contains(
                                r"(A ATT|ATT-|ATTEMPT|S SOLICIT"
                                r"|CONSP|SOLICITATION|COMPLICITY|"
                                r"CONSPIRACY|SOLICIT[^I]*[^O]*[^N]*)"
                            )
                            & pl.col("Description").str.contains(r"COMPUTER").not_()
                        ).alias("ASCNonDisqualifying"),
                        (
                            pl.col("Code").str.contains(
                                r"(OSUA|EGUA|MAN1|MAN2|MANS|ASS1|ASS2|KID1|KID2|HUT1"
                                r"|HUT2|BUR1|BUR2|TOP1|TOP2|TP2D|TP2G|TPCS|TPCD|TPC1"
                                r"|TET2|TOD2|ROB1|ROB2|ROB3|FOR1|FOR2|FR2D|MIOB|TRAK"
                                r"|TRAG|VDRU|VDRY|TRAO|TRFT|TRMA|TROP|CHAB|WABC|ACHA"
                                r"|ACAL|TER1|TFT2|TLP1|TLP2|BIGA|BAC1|ACBL)"
                            )
                            | pl.col("Cite").str.contains(
                                r"026-015-003$|008-016-017|13A-008-0?0?2\.1|13A-008-0?10\.4"
                                r"|13A-010-15[34]|13A-010-171|13A-010-19[45]|13A-010-196\(C\)"
                                r"|13A-010-19[789]|13A-010-200"
                            )
                        ).alias("CERVCode"),
                        (
                            pl.col("Code").str.contains(
                                r"(RAP1|RAP2|SOD1|SOD2|STSA|SXA1|SXA2|ECHI|SX12|CSSC"
                                r"|FTCS|MURD|MRDI|MURR|FMUR|PMIO|POBM|MIPR|POMA|INCE"
                                r"|SX2F|CSSC|ESOC|TMCS|PSMF|CM\d\d|CMUR|OLDD)"
                            )
                            | pl.col("Cite").str.contains(
                                r"13A-006-066|13A-006-067|13A-006-069\.?1?|13A-006-12[1-5]"
                                r"|13A-012-19[267]|13A-012-200\.2|13A-013-003"
                            )
                        ).alias("PardonCode"),
                        # NOTE: It appears capital murder is not a permanently
                        # disqualifying conviction.
                        # pl.col("Code")  noqa: ERA001
                        # .str.contains(r"(CM\d\d|CMUR|OLDD)")
                        # .alias("PermanentCode"),
                        pl.lit(False).alias("PermanentCode"),  # noqa: FBT003
                    )
                    # include all drug trafficking charges based on cite
                    .with_columns(
                        pl.when(
                            pl.col("Code").str.contains(r"^TR")
                            & pl.col("Cite").str.contains(r"13A-012-231")
                        )
                        .then(pl.lit(value=True))
                        .otherwise(pl.col("CERVCode"))
                        .alias("CERVCode")
                    )
                    .with_columns(
                        (
                            pl.col("CERVCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Felony")
                        ).alias("CERVCharge"),
                        (
                            pl.col("PardonCode")
                            # & pl.col("Description").str.contains("CAPITAL").not_()
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Felony")
                        ).alias("PardonToVoteCharge"),
                        (
                            pl.col("PermanentCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Felony")
                        ).alias("PermanentCharge"),
                    )
                )
                if not debug:
                    df = df.select(
                        "Name",
                        "CaseNumber",
                        "#",
                        "Code",
                        "ID",
                        "Description",
                        "Cite",
                        "TypeDescription",
                        "Category",
                        "Felony",
                        "CERVCharge",
                        "PardonToVoteCharge",
                        "PermanentCharge",
                    )
                df = df.with_columns(
                    pl.concat_str(
                        [
                            pl.col("CaseNumber"),
                            pl.lit(" - "),
                            pl.col("#"),
                            pl.lit(" "),
                            pl.col("Cite"),
                            pl.lit(" "),
                            pl.col("Description"),
                            pl.lit(" "),
                            pl.col("TypeDescription"),
                        ]
                    ).alias("ChargesSummary")
                )
            else:
                columns = [
                    "Name",
                    "CaseNumber",
                    "#",
                    "Code",
                    "ID",
                    "Description",
                    "Cite",
                    "TypeDescription",
                    "Category",
                    "Felony",
                    "CERVCharge",
                    "PardonToVoteCharge",
                    "PermanentCharge",
                    "ChargesSummary",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._filing_charges = df
        return self._filing_charges

    def disposition_charges(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make disposition charges table."""
        if debug:
            self._disposition_charges = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._disposition_charges, pl.DataFrame)
            and "Row" in self._disposition_charges.columns
        ):
            self._disposition_charges = None
        if isinstance(self._disposition_charges, pl.DataFrame):
            return self._disposition_charges
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing disposition charges…"):
            df = (
                self.archive.select("AllPagesText", "CaseNumber")
                .select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)Disposition Charges (.+?)"
                        r" (Sentences|Enforcement|Financial)"
                    )
                    .str.replace(
                        r"# Code Court Action Category Cite Court Action Date\s*\n\s*",
                        "",
                    )
                    .str.replace(
                        r"Type Description Description Class ID\s*\n\s*",
                        "",
                    )
                    .str.replace_all(r"(..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+)", "")
                    .str.replace(r"^\s*\n\s*", "")
                    .str.replace(r"\s*\n$", "")
                    .alias("DispositionCharges"),
                    pl.col("AllPagesText")
                    .str.extract(r"(Total:.+\-?\$[^\n]*)")
                    .str.replace_all(r"[^0-9|\.|\s|\$]", "")
                    .str.extract_all(r"\s\-?\$\d+\.\d{2}")
                    .list.get(2)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalBalance"),
                    pl.col("AllPagesText")
                    .str.extract(r"(ACTIVE[^\n]+D999[^\n]+)")
                    .str.extract_all(r"\-?\$\d+\.\d{2}")
                    .list.get(-1)
                    .str.replace(r"[\$\s]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("D999"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                        group_index=1,
                    )
                    .str.replace("Case Number:", "", literal=True)
                    .str.replace(r"C$", "")
                    .str.strip_chars()
                    .alias("Name"),
                    pl.col("AllPagesText")
                    .str.contains(r"(?s)Fee Sheet (.+Total:[^\n]+)")
                    .alias("HasFeeSheet"),
                )
                .drop_nulls("DispositionCharges")
            )
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("DispositionCharges").map_elements(
                            lambda x: re.split(r"(?m)^\s*(\d{3}) ", x)
                        )
                    )
                    .select(
                        pl.col("Name"),
                        pl.col("CaseNumber"),
                        pl.col("DispositionCharges")
                        .map_elements(lambda x: x[::2][1:])
                        .alias("Row"),
                        pl.col("DispositionCharges")
                        .map_elements(lambda x: x[1::2])
                        .alias("#"),
                        pl.col("TotalBalance"),
                        pl.col("D999"),
                        pl.col("HasFeeSheet"),
                    )
                    .explode("Row", "#")
                    .with_columns(
                        pl.col("Row").str.replace_all("\n", " ").str.strip_chars()
                    )
                    .with_columns(
                        pl.col("Row").str.extract(r"([A-Z0-9/]+)").alias("Code"),
                        pl.col("Row")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("CourtActionDate"),
                        pl.col("Row")
                        .str.extract(
                            r"(BOUND|GUILTY PLEA|NOT GUILTY/INSAN E|WAIVED TO GJ"
                            r"|DISMISSED W/CONDITION S|DISMISSED/N OL PROS"
                            r" W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ"
                            r"|TIME LAPSED|NOL PROSS"
                            r"|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N"
                            r"|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST"
                            r" MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST"
                            r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE"
                            r" OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE"
                            r" \(\.50 CASE\)|FINAL FORFEITURE \(\.50"
                            r" CASE\)|DISMISSED|FORFEITURE|TRANSFERRE|REMANDED"
                            r"|WAIVED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\."
                            r" FORF\. SET ASIDE|COND\. FORF\.|OTHER"
                            r"|PROBATION NT REVOKE|PROBATION/S|NO PROBABLE CAUSE"
                            r"|PETITION GRANTED|PROBATION TERMINATED|ANCTION"
                            r"|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED"
                            r" \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)"
                            r"|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)"
                        )
                        .str.replace(r" \)", ")")
                        .str.replace(r"\d\d?/\d\d?/\d\d\d\d ", "")
                        .str.replace(
                            r"N OL PROS W/CONDITION S", "NOL PROS W/CONDITIONS"
                        )
                        .str.replace("INSAN E", "INSANE")
                        .str.replace("CONDITION S", "CONDITIONS")
                        .str.replace("PROBATION/S", "PROBATION/SANCTION")
                        .str.replace("ADJUDICATIO N", "ADJUDICATION")
                        .str.replace("TRANSFERRE", "TRANSFERRED")
                        .str.replace("BOUND", "BOUND OVER GJ")
                        .str.replace("DOCKETED", "DOCKETED BY MISTAKE")
                        .alias("CourtAction"),
                        pl.col("Row")
                        .str.extract(
                            r"([A-Z0-9]{3}-[A-Z0-9]{3}-"
                            r" *[A-Z0-9]{1,3}\.?\s*\d*\(?[A-Z0-9]*\)?"
                            r"\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?\d?/?\d?)"
                        )
                        .str.replace_all(" ", "")
                        .str.replace(r"[A-Z/]+$", "")
                        .alias("Cite"),
                        pl.col("Row")
                        .str.extract(
                            r"([A-Z0-9]{3}-[A-Z0-9]{3}-"
                            r" *[A-Z0-9]{1,3}\.?\s*\d*\(?[A-Z0-9]*\)?"
                            r"\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?\d?/?\d?.+)"
                        )
                        .str.replace(r"^[A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+", "")
                        .str.replace(r"\d\(.\)\(?.?\)?", "")
                        .str.replace(
                            r"^(BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION)",
                            "",
                        )
                        .str.strip_chars()
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(
                            (
                                r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|GJ|GUILTY PLEA"
                                r"|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED"
                                r" W/CONDITION S"
                                r"|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED"
                                r" PRELIM\."
                                r" FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED"
                                r"|INDICTED PRIOR TO ADJUDICATIO N|DISMISSED|TRANSFERED"
                                r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS"
                                r" ENTRY TO"
                                r" EXPLAIN \)|OTHER \(MUST"
                                r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d?"
                                r" MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET"
                                r" ASIDE"
                                r" \(\.50 CASE\)|FINAL FORFEITURE \(\.50"
                                r" CASE\)|FORFEITURE"
                                r"|TRANSFER|REMANDED|WAIVED|ACQUITTED|WITHDRAWN"
                                r"|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\."
                                r" FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|NO"
                                r" PROBABLE"
                                r" CAUSE|PETITION GRANTED|PROBATION TERMINATED|FINAL"
                                r" FORF\."
                                r" SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70"
                                r" CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION"
                                r" REVOKED|PRETRIAL DIVERSION|YOUTHFUL"
                                r" OFFENDER)\s+(ALCOHOL"
                                r"|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG"
                                r"|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL"
                                r" ORDINANCE|MUNICIPAL"
                                r"|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET"
                                r"|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS"
                                r"|JUVENILE)\s+(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)"
                                r"(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)"
                            ),
                            group_index=4,
                        )
                        .str.strip_chars()
                        .alias("DescriptionFirstLine"),
                        pl.col("Row")
                        .str.extract(
                            (
                                r"(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC"
                                r"|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE"
                                r"|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX"
                                r" OFFENSE|TRAFFIC"
                                r"|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)"
                                r"|BUSINESS|JUVENILE)\s*"
                                r"(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)"
                            ),
                            group_index=2,
                        )
                        .alias("TypeDescription"),
                        pl.col("Row")
                        .str.extract(
                            r"(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC"
                            r"|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE"
                            r"|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC"
                            r"|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)"
                            r"|BUSINESS|JUVENILE)"
                        )
                        .alias("Category"),
                    )
                    # fix DescriptionFirstLine when another field is missing
                    .with_columns(
                        pl.when(pl.col("DescriptionFirstLine").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(
                                (
                                    r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|GJ|GUILTY PLEA"
                                    r"|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED"
                                    r" W/CONDITION S"
                                    r"|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED"
                                    r" PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL"
                                    r" PROSS|CONVICTED"
                                    r"|INDICTED PRIOR TO ADJUDICATIO N|TRANSFERED"
                                    r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST"
                                    r" MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST"
                                    r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS"
                                    r" ENTRY\)|FINAL"
                                    r" BOND FORF\.|FORFEITURE SET ASIDE \(\.50"
                                    r" CASE\)|FINAL FORFEITURE \(\.50"
                                    r" CASE\)|DISMISSED|FORFEITURE|TRANSFER"
                                    r"|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION"
                                    r" DENIED"
                                    r"|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER"
                                    r"|PROBATION NT REVOKE|PROBATION/S|NO PROBABLE"
                                    r" CAUSE|PETITION GRANTED|PROBATION TERMINATED"
                                    r"|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION"
                                    r" NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED"
                                    r" \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL"
                                    r" DIVERSION|YOUTHFUL OFFENDER)\s+(ALCOHOL|BOND"
                                    r" FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG"
                                    r"|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL"
                                    r" ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY"
                                    r"|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC"
                                    r" \(PUBLIC SERVICE"
                                    r" COMMISSION\)|BUSINESS|JUVENILE)\s+"
                                    r"(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)"
                                ),
                                group_index=3,
                            )
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("DescriptionFirstLine"))
                        .alias("DescriptionFirstLine")
                    )
                    .with_columns(
                        pl.when(pl.col("DescriptionFirstLine").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(
                                (
                                    r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|GJ|GUILTY PLEA"
                                    r"|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED"
                                    r" W/CONDITION S"
                                    r"|DISMISSED/N OL PROS W/CONDITION S|TRANSFERED"
                                    r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS"
                                    r" ENTRY TO EXPLAIN \)|OTHER \(MUST"
                                    r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS"
                                    r" ENTRY\)|FINAL"
                                    r" BOND FORF\.|FORFEITURE SET ASIDE \(\.50"
                                    r" CASE\)|FINAL"
                                    r" FORFEITURE \(\.50 CASE\)|TIME LAPSED PRELIM\."
                                    r" FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED"
                                    r"|INDICTED PRIOR TO ADJUDICATIO"
                                    r" N|DISMISSED|FORFEITURE"
                                    r"|TRANSFER|REMANDED|ACQUITTED|WITHDRAWN|PETITION"
                                    r" DENIED"
                                    r"|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER"
                                    r"|PROBATION NT REVOKE|PROBATION/S|ANCTION|NO"
                                    r" PROBABLE CAUSE"
                                    r"|PETITION GRANTED|PROBATION TERMINATED|FINAL"
                                    r" FORF\. SET ASIDE"
                                    r"|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)"
                                    r"|PROBATION REVOKED \(\.70 CASE\)|PROBATION"
                                    r" REVOKED"
                                    r"|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)\s+"
                                    r"(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)"
                                    r"(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)"
                                ),
                                group_index=3,
                            )
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("DescriptionFirstLine"))
                        .alias("DescriptionFirstLine")
                    )
                    .with_columns(
                        pl.when(pl.col("DescriptionFirstLine").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(
                                (
                                    r"(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC"
                                    r"|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL"
                                    r" ORDINANCE"
                                    r"|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX"
                                    r" OFFENSE|TRAFFIC"
                                    r"|DOCKET|REVENUE – PSC \(PUBLIC SERVICE"
                                    r" COMMISSION\)|BUSINESS|JUVENILE)\s+"
                                    r"(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)"
                                    r"(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)"
                                ),
                                group_index=3,
                            )
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("DescriptionFirstLine"))
                        .alias("DescriptionFirstLine")
                    )
                    .with_columns(
                        pl.when(pl.col("DescriptionFirstLine").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(
                                (
                                    r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|WAIVED TO"
                                    r" GJ|GUILTY"
                                    r" PLEA|NOT GUILTY/INSAN E|GJ|DISMISSED"
                                    r" W/CONDITION S"
                                    r"|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED"
                                    r" PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS"
                                    r"|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N"
                                    r"|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST"
                                    r" MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST"
                                    r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS"
                                    r" ENTRY\)|FINAL"
                                    r" BOND FORF\.|FORFEITURE SET ASIDE \(\.50"
                                    r" CASE\)|FINAL FORFEITURE \(\.50"
                                    r" CASE\)|DISMISSED|FORFEITURE|TRANSFER"
                                    r"|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION"
                                    r" DENIED"
                                    r"|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER"
                                    r"|PROBATION NT REVOKE|PROBATION/S|ANCTION"
                                    r"|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION"
                                    r" TERMINATED"
                                    r"|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT"
                                    r" REVOKED"
                                    r" \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)"
                                    r"|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL"
                                    r" OFFENDER)\s+"
                                    r"(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)"
                                ),
                                group_index=2,
                            )
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("DescriptionFirstLine"))
                        .alias("DescriptionFirstLine")
                    )
                    # clean DescriptionFirstLine
                    .with_columns(
                        pl.when(
                            pl.col("DescriptionFirstLine").is_in(
                                [
                                    "CONSERVATION",
                                    "TO GJ",
                                    "PROPERTY",
                                    "DRUG",
                                    "PERSONAL",
                                    "FELONY",
                                    "ANCTION    DRUG",
                                    "MISDEMEANOR",
                                ]
                            )
                            | pl.col("DescriptionFirstLine").str.contains(
                                r"\d\d/\d\d/\d\d\d\d"
                            )
                        )
                        .then(pl.lit(None))
                        .otherwise(pl.col("DescriptionFirstLine"))
                        .alias("DescriptionFirstLine")
                    )
                    # if description is in two lines, concat
                    .with_columns(
                        pl.when(pl.col("DescriptionFirstLine").is_not_null())
                        .then(
                            pl.concat_str(
                                [
                                    pl.col("DescriptionFirstLine"),
                                    pl.lit(" "),
                                    pl.col("Description"),
                                ]
                            )
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # replace stray \ with escape \\
                    # remove TypeDescription at beginning of desc
                    # remove (PUBLIC SERVICE COMMISSION)
                    .with_columns(
                        pl.col("Description")
                        .str.replace(r"\\", "\\\\")
                        .str.replace(
                            (
                                r"^(BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION"
                                r"|\(PUBLIC SERVICE COMMISSION\))"
                            ),
                            "",
                        )
                        .str.strip_chars()
                    )
                    # fix CFR cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(r"\d+ CFR \d+")
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"(\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)?)")
                            .str.replace(r"\. ", ".")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(r"\d+ CFR \d+")
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)? (.+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix ACT XXXX-XX cite, description
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(r"(ACT \d+-\d+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(r"(ACT \d+-\d+)")
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"ACT \d+-\d+ (.+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix PSC-.+ cite, description
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.extract(r"(PSC-\d[^\s]+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(r"(PSC-\d[^\s]+)")
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"PSC-\d[^\s]+ (.+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix SCR-\d+ cite
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Row").str.extract(r"(SCR-\d+)").str.strip_chars())
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(r"(SCR-\d+)")
                        )
                        .then(
                            pl.col("Row").str.extract(r"SCR-\d+ (.+)").str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix 760-\d+ cite
                    .with_columns(
                        pl.when(pl.col("Row").str.contains(r"(760-X-)"))
                        .then(
                            pl.col("Row")
                            .str.extract(r"((DPS)? 760-X- ?[^\s]+)")
                            .str.replace("- ", "-")
                            .str.replace_all(" ", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Row").str.contains(r"(760-X-)"))
                        .then(
                            pl.col("Row")
                            .str.extract(r"760-X-[^\s]+(.+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix XXX-XXX$ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(\d+-\d[^\s]+$)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix ORD- \d+-\d+ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Row").str.extract(r"(ORD- \d+-\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix HSV- OR-D \d+-\d+ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Row").str.extract(r"(HSV- OR-D \d+-\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix \d\d\d-\d\d\d([A-Z0-9]) cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Row").str.extract(r"(\d+-\d+\([A-Z0-9]\))"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix PSC-\d\.\d-\d+ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Row").str.extract(r"(PSC-\d+\.\d+-\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix \d+-\d+ -\d+ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(r"(\d+-\d+ -\d+)")
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix \d+\.\d+ cites
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Row").str.extract(r"(\d+\.\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix MUNICIPAL cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("MUNICIPAL MUNICIPAL")
                        )
                        .then(pl.col("Row").str.extract(r"(MUNICIPAL)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # fix RULE 32 cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains("RULE 32")
                            | (
                                pl.col("Row").str.contains("RULE 32")
                                & pl.col("Description").is_null()
                            )
                        )
                        .then(pl.lit("RULE 32"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Description").str.contains("RULE 32")
                            | (
                                pl.col("Row").str.contains("RULE 32")
                                & pl.col("Description").is_null()
                            )
                        )
                        .then(pl.lit("RULE 32-FELONY"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix PROBATION REV cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Row").str.contains("PROBATION REV")
                            & (pl.col("Cite").is_null() | pl.col("Cite").eq(""))
                        )
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Row").str.contains("PROBATION REV")
                            & (
                                pl.col("Description").is_null()
                                | pl.col("Description").eq("")
                            )
                        )
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix COMMUNITY CORRECTION cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Row").str.contains("COMMUNITY CORRECTION REVOC")
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Row").str.contains("COMMUNITY CORRECTION REVOC")
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REVOC"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix OTHER NON MOVING VIO cites and descriptions
                    .with_columns(
                        pl.when(pl.col("Row").str.contains("OTHER NON MOVING VIO"))
                        .then(pl.lit("OTHER NON MOVING VIO"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MC cites at end of description
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.extract(r"(\d+\s*-\s*\d+\s*-\s*\d+$)")
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.replace(r"(\d+\s*-\s*\d+\s*-\s*\d+$)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix 000.000 cites at end of description
                    .with_columns(
                        pl.when(pl.col("Cite").is_null())
                        .then(pl.col("Description").str.extract(r"(\d+\.\d+)"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Cite").is_null())
                        .then(
                            pl.col("Description")
                            .str.replace(r"(\d+\.\d+)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix PRE-CONV HABEAS CORPUS cites and descriptions
                    .with_columns(
                        pl.when(pl.col("Row").str.contains("PRE-CONV HABEAS CORPUS"))
                        .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(pl.col("Row").str.contains("PRE-CONV HABEAS CORPUS"))
                        .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix HABEAS CORPUS cites and descriptions
                    .with_columns(
                        pl.when(
                            pl.col("Row").str.contains("HABEAS CORPUS")
                            & pl.col("Row").str.contains("PRE-CONV").not_()
                        )
                        .then(pl.lit("HABEAS CORPUS"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Row").str.contains("HABEAS CORPUS")
                            & pl.col("Row").str.contains("PRE-CONV").not_()
                        )
                        .then(pl.lit("HABEAS CORPUS"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix TRAFFIC/MISC missing description
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("TRAFFIC/MISC")
                        )
                        .then(pl.lit("TRAFFIC/MISC"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MUN- cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(" MUN-")
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"(MUN-.+?) MISDEMEANOR$")
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(" MUN-")
                        )
                        .then(
                            pl.col("Description")
                            .str.replace(r"MUN-.+", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix HSV- cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(" HSV-")
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(
                                r"(HSV-.+?) (MISDEMEANOR|VIOLATION)$",
                                group_index=1,
                            )
                            .str.replace_all(" ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains(" HSV-")
                        )
                        .then(
                            pl.col("Description")
                            .str.replace(r"(HSV-.+)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix ORD-AM cites
                    .with_columns(
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("ORD-AM")
                        )
                        .then(
                            pl.col("Row").str.extract(
                                r"(ORD-AM.+?) (MISDEMEANOR|VIOLATION)"
                            )
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("ORD-AM")
                        )
                        .then(
                            pl.col("Description")
                            .str.replace(r"(ORD-AM.+)", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix MUNICIPAL ORDINANCE extra stuff in description
                    .with_columns(
                        pl.when(
                            pl.col("Description").str.contains("MUNICIPAL ORDINANCE")
                        )
                        .then(pl.lit("MUNICIPAL ORDINANCE"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix BOND FORT missing description, cite
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(r"BOND FORT")
                        )
                        .then(pl.lit("BOND FORF-FELONY"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(r"BOND FORT")
                        )
                        .then(pl.lit("BOND FORT"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix PT-RL F/CN missing description
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(r"PT-RL F/CN")
                        )
                        .then(pl.lit("PT-RL F/CN"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix - - (Description) missing
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(r" -+ +-+ +")
                        )
                        .then(pl.col("Row").str.extract(r"-+ +-+ +(.+)"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix missing description when cite is ---------
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("----")
                        )
                        .then(pl.col("Row").str.extract(r"---- (.+)").str.strip_chars())
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix RESERVED cites
                    .with_columns(
                        pl.when(
                            pl.col("Row").str.contains("RESERVED")
                            & pl.col("Cite").is_null()
                        )
                        .then(pl.lit("RESERVED"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Row").str.contains("RESERVED")
                            & pl.col("Description").is_null()
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"RESERVED (.+)")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # fix SECTION \d\d-\d? cites
                    .with_columns(
                        pl.when(
                            pl.col("Row").str.contains("SECTION")
                            & pl.col("Description").is_null()
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"SECTION \d\d-\d* (.+)")
                            .str.replace(r"^\s*MISDEMEANOR \d+", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Row").str.contains("SECTION")
                            & pl.col("Cite").is_null()
                        )
                        .then(
                            pl.col("Row")
                            .str.extract(r"(SECTION \d+-\s*(MISDEMEANOR)?\s*\d+)")
                            .str.replace(" MISDEMEANOR ", "")
                        )
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix misc -\.?\d+ descriptions
                    .with_columns(
                        pl.when(pl.col("Description").is_null())
                        .then(
                            pl.col("Row")
                            .str.extract(r"[-\.]\d+(.+?)$")
                            .str.strip_chars()
                            .str.replace(r"^\([A-Z0-9]\)", "")
                            .str.replace(r"^\([A-Z0-9]\)", "")
                            .str.replace(r"^\.\d+", "")
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix "PSC" cite and description
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(r" PSC ")
                        )
                        .then(pl.lit("PSC"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(r" PSC ")
                        )
                        .then(pl.col("Row").str.extract(r" PSC (.+)").str.strip_chars())
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    )
                    # missing TypeDescriptions caused by another missing field
                    .with_columns(
                        pl.when(pl.col("TypeDescription").is_null())
                        .then(
                            pl.col("Row").str.extract(
                                r"(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)"
                            )
                        )
                        .otherwise(pl.col("TypeDescription"))
                        .alias("TypeDescription")
                    )
                    # fix MISCELLANEOUS FILING
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("MISCELLANEOUS FILING")
                        )
                        .then(pl.lit("MISCELLANEOUS FILING"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix SHOW CAUSE DKT/HEARING
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("SHOW CAUSE DKT/HEARING")
                        )
                        .then(pl.lit("SHOW CAUSE DKT/HEARING"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix BOND HEARING
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("BOND HEARING")
                        )
                        .then(pl.lit("BOND HEARING"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MUNICIPAL ORDINANCE
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(
                                "MUNICIPAL MUNICIPAL ORDINANCE"
                            )
                        )
                        .then(pl.lit("MUNICIPAL ORDINANCE"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    )
                    # fix MUN- OR-D 13-4
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("MUN- OR-D 13-4")
                        )
                        .then(pl.lit("NOISE - LOUD & EXCESS"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("MUN- OR-D 13-4")
                        )
                        .then(pl.lit("MUN- OR-D 13-4"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # fix ACT2001-312, SEC 5
                    .with_columns(
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("ACT2001-312")
                        )
                        .then(pl.lit("OBSTRUCT JUSTICE BY FALSE ID"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("ACT2001-312")
                        )
                        .then(pl.lit("ACT2001-312, SEC 5"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    )
                    # Fix ugly -- -- from cite in description
                    # and hanging N in ADJUDICATIO N
                    .with_columns(
                        pl.col("Description")
                        .str.replace(r"-+ +-+", "")
                        .str.replace("ADJUDICATIO N", "")
                        .str.replace(r"\s+N$", "")
                        .str.replace(r"^ORDINANCE (VIOLATION|MISDEMEANOR)\s+", "")
                        .str.replace(r"^, FELONY SEC \d+", "")
                        .str.strip_chars()
                    )
                    # fix MUN-ICI-
                    .with_columns(
                        pl.when(pl.col("Cite").eq("MUN-ICI-"))
                        .then(pl.lit("MUN-ICI-PAL"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite")
                    )
                    # remove null rows
                    .drop_nulls("Row")
                    # add ID column
                    .with_columns(
                        pl.col("Row")
                        .str.extract(r"\d\d/\d\d/\d\d\d\d ([ASCP]) ")
                        .alias("ID")
                    )
                    # remove ID from description
                    .with_columns(pl.col("Description").str.replace(r"^\w ", ""))
                    # fill null to prevent null bools
                    .fill_null("")
                    # charge sort
                    .with_columns(
                        pl.col("CourtAction")
                        .str.contains(r"GUILTY|CONVICTED")
                        .alias("Conviction"),
                        pl.col("Row").str.contains("FELONY").alias("Felony"),
                        (
                            pl.col("Description").str.contains(
                                r"(A ATT|ATT-|ATTEMPT|S SOLICIT|CONSP|SOLICITATION"
                                r"|COMPLICITY|CONSPIRACY|SOLICIT[^I]*[^O]*[^N]*)"
                            )
                            & pl.col("Description").str.contains(r"COMPUTER").not_()
                        ).alias("ASCNonDisqualifying"),
                        (
                            pl.col("Code").str.contains(
                                r"(OSUA|EGUA|MAN1|MAN2|MANS|ASS1|ASS2|KID1|KID2|HUT1"
                                r"|HUT2|BUR1|BUR2|TOP1|TOP2|TP2D|TP2G|TPCS|TPCD|TPC1"
                                r"|TET2|TOD2|ROB1|ROB2|ROB3|FOR1|FOR2|FR2D|MIOB|TRAK"
                                r"|TRAG|VDRU|VDRY|TRAO|TRFT|TRMA|TROP|CHAB|WABC|ACHA"
                                r"|ACAL|TER1|TFT2|TLP1|TLP2|BIGA|BAC1|ACBL)"
                            )
                            | pl.col("Cite").str.contains(
                                r"026-015-003$|008-016-017|13A-008-0?0?2\.1|13A-008-0?10\.4"
                                r"|13A-010-15[34]|13A-010-171|13A-010-19[45]"
                                r"|13A-010-196\(C\)|13A-010-19[789]|13A-010-200"
                            )
                        ).alias("CERVCode"),
                        (
                            pl.col("Code").str.contains(
                                r"(RAP1|RAP2|SOD1|SOD2|STSA|SXA1|SXA2|ECHI|SX12|CSSC"
                                r"|FTCS|MURD|MRDI|MURR|FMUR|PMIO|POBM|MIPR|POMA|INCE"
                                r"|SX2F|CSSC|ESOC|TMCS|PSMF|CM\d\d|CMUR|OLDD)"
                            )
                            | pl.col("Cite").str.contains(
                                r"13A-006-066|13A-006-067|13A-006-069\.?1?|13A-006-12[1-5]"
                                r"|13A-012-19[267]|13A-012-200\.2|13A-013-003"
                            )
                        ).alias("PardonCode"),
                        (
                            # NOTE: It appears capital murder is not a permanently
                            # disqualifying conviction.
                            # pl.col("Code").str.contains(r"(CM\d\d|CMUR|OLDD)")  noqa
                            # | pl.col("Description").str.contains("CAPITAL")
                            pl.lit(False)  # noqa
                        ).alias("PermanentCode"),
                    )
                    # include all drug trafficking charges based on cite
                    .with_columns(
                        pl.when(
                            pl.col("Code").str.contains(r"^TR")
                            & pl.col("Cite").str.contains(r"13A-012-231")
                        )
                        .then(pl.lit(value=True))
                        .otherwise(pl.col("CERVCode"))
                        .alias("CERVCode")
                    )
                    .with_columns(
                        pl.when(pl.col("Conviction").is_null())
                        .then(pl.lit(value=False))
                        .otherwise(pl.col("Conviction"))
                        .alias("Conviction")
                    )
                    .with_columns(
                        (
                            pl.col("CERVCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Felony")
                        ).alias("CERVCharge"),
                        (
                            pl.col("PardonCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Felony")
                        ).alias("PardonToVoteCharge"),
                        (
                            pl.col("PermanentCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Felony")
                        ).alias("PermanentCharge"),
                        (
                            pl.col("CERVCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Conviction")
                            & pl.col("Felony")
                        ).alias("CERVConviction"),
                        (
                            pl.col("PardonCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Conviction")
                            & pl.col("Felony")
                        ).alias("PardonToVoteConviction"),
                        (
                            pl.col("PermanentCode")
                            & pl.col("ASCNonDisqualifying").not_()
                            & pl.col("Conviction")
                            & pl.col("Felony")
                        ).alias("PermanentConviction"),
                    )
                    .with_columns(
                        pl.when(pl.col("Conviction").not_())
                        .then(pl.lit(None))
                        .otherwise(pl.col("CERVConviction"))
                        .alias("CERVConviction"),
                        pl.when(pl.col("Conviction").not_())
                        .then(pl.lit(None))
                        .otherwise(pl.col("PardonToVoteConviction"))
                        .alias("PardonToVoteConviction"),
                        pl.when(pl.col("Conviction").not_())
                        .then(pl.lit(None))
                        .otherwise(pl.col("PermanentConviction"))
                        .alias("PermanentConviction"),
                    )
                    .with_columns(
                        pl.when(pl.col("D999").is_null())
                        .then(pl.lit(0.0))
                        .otherwise(pl.col("D999"))
                        .alias("D999"),
                        pl.when(pl.col("TotalBalance").is_null())
                        .then(pl.lit(0.0))
                        .otherwise(pl.col("TotalBalance"))
                        .alias("TotalBalance"),
                    )
                    .with_columns(
                        pl.when(
                            pl.col("CERVConviction")
                            | pl.col("PardonToVoteConviction")
                            | pl.col("PermanentConviction")
                        )
                        .then(pl.col("TotalBalance") - pl.col("D999"))
                        .otherwise(None)
                        .alias("PaymentToRestore")
                    )
                    .with_columns(
                        pl.when(pl.col("HasFeeSheet").not_())
                        .then(pl.lit(None))
                        .otherwise(pl.col("TotalBalance"))
                        .alias("TotalBalance")
                    )
                )
                if not debug:
                    df = df.select(
                        "Name",
                        "CaseNumber",
                        "#",
                        "Code",
                        "ID",
                        "Description",
                        "Cite",
                        "TypeDescription",
                        "Category",
                        "CourtAction",
                        "CourtActionDate",
                        "TotalBalance",
                        "PaymentToRestore",
                        "Conviction",
                        "Felony",
                        "CERVCharge",
                        "PardonToVoteCharge",
                        "PermanentCharge",
                        "CERVConviction",
                        "PardonToVoteConviction",
                        "PermanentConviction",
                    )
                df = (
                    df.with_columns(
                        pl.col("CourtActionDate")
                        .dt.to_string("%Y-%m-%d")
                        .alias("CourtActionDateStr")
                    )
                    .fill_null("")
                    .with_columns(
                        pl.concat_str(
                            [
                                pl.col("CaseNumber"),
                                pl.lit(" - "),
                                pl.col("#"),
                                pl.lit(" "),
                                pl.col("Cite"),
                                pl.lit(" "),
                                pl.col("Description"),
                                pl.lit(" "),
                                pl.col("TypeDescription"),
                                pl.lit(" "),
                                pl.col("CourtAction"),
                                pl.lit(" "),
                                pl.col("CourtActionDateStr"),
                            ]
                        ).alias("ChargesSummary")
                    )
                    .drop("CourtActionDateStr")
                )
            else:
                columns = [
                    "Name",
                    "CaseNumber",
                    "#",
                    "Code",
                    "ID",
                    "Description",
                    "Cite",
                    "TypeDescription",
                    "Category",
                    "CourtAction",
                    "CourtActionDate",
                    "TotalBalance",
                    "PaymentToRestore",
                    "Conviction",
                    "Felony",
                    "CERVCharge",
                    "PardonToVoteCharge",
                    "PermanentCharge",
                    "CERVConviction",
                    "PardonToVoteConviction",
                    "PermanentConviction",
                    "ChargesSummary",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._disposition_charges = df
        return self._disposition_charges

    def sentences(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make sentences table."""
        if debug:
            self._sentences = None
        # If previously called with debug=True, reset
        if (
            isinstance(self._sentences, pl.DataFrame)
            and "Sentence" in self._sentences.columns
        ):
            self._sentences = None
        if isinstance(self._sentences, pl.DataFrame):
            return self._sentences
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing sentences…"):
            df = (
                self.archive.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(?s)(Sentence \d+ .+? \*Key)")
                    .alias("Sentence"),
                )
                .explode("Sentence")
                .drop_nulls("Sentence")
                .with_columns(
                    pl.col("Sentence").str.replace_all(
                        r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", ""
                    )
                )
                .with_columns(
                    # sentence
                    pl.col("Sentence")
                    .str.extract(r"^Sentence (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("Sentence#"),
                    pl.col("Sentence")
                    .str.extract(r"Last Update: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("LastUpdate"),
                    pl.col("Sentence")
                    .str.extract(r"Updated By: (\w+)")
                    .alias("UpdatedBy"),
                    pl.col("Sentence")
                    .str.extract(r"Probation Revoke: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ProbationRevoke"),
                    pl.col("Sentence")
                    .str.extract(r"License Susp Period: (.+)")
                    .str.replace(r"\d\d?/\d\d?/\d\d\d\d", "")
                    .str.strip_chars()
                    .alias("LicenseSuspPeriod"),
                    pl.col("Sentence")
                    .str.extract(
                        (
                            r"License Susp Period: (\d+ Years, \d+ Months, \d+"
                            r" Days\.)?\s*\n\s*(\d\d/\d\d/\d\d\d\d)?\s*\n?\s*(\d+"
                            r" Years, \d+ Months, \d+ Days\.)?"
                        ),
                        group_index=2,
                    )
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ProbationBeginDate"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)([^\n]+)\n\s*Probation Begin Date:")
                    .str.replace(r"License.+", "")
                    .str.strip_chars()
                    .alias("JailCreditPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Probation Period: (.+)")
                    .str.strip_chars()
                    .alias("ProbationPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence Provisions: (\w+)")
                    .str.replace("Requrements", "")
                    .alias("SentenceProvisions"),
                    pl.col("Sentence")
                    .str.extract(r"Requrements Completed: (YES|NO|UNKNOWN)")
                    .alias("RequirementsCompleted"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SentenceDate"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence Start Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SentenceStartDate"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence End Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SentenceEndDate"),
                    # monetary
                    pl.col("Sentence")
                    .str.extract(r"Costs: (.+?)Fine")
                    .str.strip_chars()
                    .alias("Costs"),
                    pl.col("Sentence")
                    .str.extract(
                        r"(?s)Alias Warrant:.+?\n\s*(\w+)\s*\n\s*Drug Docket Fees"
                    )
                    .alias("DrugUserFee"),  # don't ask me why
                    pl.col("Sentence")
                    .str.extract(r"WC Fee 85%: (.+)", group_index=1)
                    .str.strip_chars()
                    .alias("DrugDocketFees"),  # don't ask me why
                    pl.col("Sentence")
                    .str.extract(r"Jail Fee: (.+)")
                    .str.strip_chars()
                    .alias("JailFee"),
                    pl.col("Sentence")
                    .str.extract(r"Demand Reduction Hearing: (.+)")
                    .str.strip_chars()
                    .alias("DemandReductionHearing"),
                    pl.col("Sentence")
                    .str.extract(r"Fine Imposed: (.+)")
                    .str.strip_chars()
                    .cast(pl.Float64, strict=False)
                    .alias("FineImposed"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)License Suspension Fee:[^\n]*\n\s*([^\n]+)")
                    .str.extract(r"([\d\.+]+)")
                    .str.strip_chars()
                    .cast(pl.Float64, strict=False)
                    .alias("FineSuspended"),  # don't ask me why
                    pl.col("Sentence")
                    .str.extract(r"(.+) Amt Over Minimum CVF:")
                    .str.strip_chars()
                    .alias("AliasWarrant"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)Drug User Fee:\s*\n(.+?)\s*\n\s*Subpoena:")
                    .str.replace_all(" ", "")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("PrelimHearing"),
                    pl.col("Sentence")
                    .str.extract(r"Crime History Fee: (.+)")
                    .str.strip_chars()
                    .alias("CrimeHistoryFee"),
                    pl.col("Sentence")
                    .str.extract(
                        r"(?s)License Suspension Fee: ([^\n]+)\n([^\n]+)\n([^\n]+)",
                        group_index=2,
                    )
                    .str.extract(r"([A-Z])")
                    .alias("Fine"),
                    pl.col("Sentence")
                    .str.extract(
                        r"(?s)License Suspension Fee: ([^\n]+)\n([^\n]+)\n([^\n]+)",
                        group_index=3,
                    )
                    .str.replace(r"WC.+", "")
                    .str.strip_chars()
                    .alias("CrimeVictimsFee"),
                    pl.col("Sentence")
                    .str.extract(r"(.+) WC Fee 85%:")
                    .str.strip_chars()
                    .alias("WCFee85%"),
                    pl.col("Sentence")
                    .str.extract(r"SX10: (.+)")
                    .str.strip_chars()
                    .alias("SX10"),
                    pl.col("Sentence")
                    .str.extract(r"License Suspension Fee: (.+)")
                    .str.strip_chars()
                    .alias("LicenseSuspensionFee"),
                    pl.col("Sentence")
                    .str.extract(r"Municipal Court: (.+)")
                    .str.strip_chars()
                    .alias("MunicipalCourt"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)WC Fee 85%:\s*\n([^\n]+)")
                    .str.replace(r"Demand.+", "")
                    .str.strip_chars()
                    .alias("WCFeeDA"),
                    pl.col("Sentence")
                    .str.extract(r"Immigration Fine:(.+)")
                    .str.replace(" Fine Imposed.+", "")
                    .str.strip_chars()
                    .alias("ImmigrationFine"),
                    # confinement
                    pl.col("Sentence")
                    .str.extract(r"Imposed Confinement Period: (.+)")
                    .str.strip_chars()
                    .alias("ImposedConfinementPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Total Confinement Period: (.+)")
                    .str.strip_chars()
                    .alias("TotalConfinementPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Suspended Confinement Period (.+)")
                    .str.strip_chars()
                    .alias("SuspendedConfinementPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Boot Camp: (.+)")
                    .str.strip_chars()
                    .alias("BootCamp"),
                    pl.col("Sentence")
                    .str.extract(r"Penitentiary: (.+)")
                    .str.strip_chars()
                    .alias("Penitentiary"),
                    pl.col("Sentence")
                    .str.extract(r"Life Without Parole: (.+)")
                    .str.strip_chars()
                    .alias("LifeWithoutParole"),
                    pl.col("Sentence")
                    .str.extract(r"Death: (.+)Life")
                    .str.strip_chars()
                    .alias("Death"),
                    pl.col("Sentence")
                    .str.extract(r"Life: (.+)Jail")
                    .str.strip_chars()
                    .alias("Life"),
                    pl.col("Sentence")
                    .str.extract(r"Jail: (.+)")
                    .str.strip_chars()
                    .alias("Jail"),
                    pl.col("Sentence")
                    .str.extract(r"Electronic Monitoring:(.+)Reverse")
                    .str.strip_chars()
                    .str.extract(r"^([^\s]+)")
                    .alias("ElectronicMonitoring"),
                    pl.col("Sentence")
                    .str.extract(r"Consecutive Sentence:(.+)")
                    .str.strip_chars()
                    .alias("ConsecutiveSentence"),
                    pl.col("Sentence")
                    .str.extract(r"Chain Gang: (.+)")
                    .str.strip_chars()
                    .alias("ChainGang"),
                    pl.col("Sentence")
                    .str.extract(r"Electronic Monitoring:(.+)Reverse")
                    .str.strip_chars()
                    .str.extract(r"^[^\s]+ (.+)")
                    .alias("ReverseSplit"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Coterminous Sentence")
                    .str.strip_chars()
                    .alias("CoterminousSentence"),
                    # programs
                    pl.col("Sentence")
                    .str.extract(r"Jail Diversion:(.+?)Alcoholics")
                    .str.strip_chars()
                    .alias("JailDiversion"),
                    pl.col("Sentence")
                    .str.extract(r"Informal Probation:(.+)")
                    .str.strip_chars()
                    .alias("InformalProbation"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Dui School:")
                    .str.strip_chars()
                    .alias("DocDrugProgram"),
                    pl.col("Sentence")
                    .str.extract(r"Dui School:(.+?)Defensive")
                    .str.strip_chars()
                    .alias("DuiSchool"),
                    pl.col("Sentence")
                    .str.extract(r"Defensive Driving Shcool:(.+)")
                    .str.strip_chars()
                    .str.replace(r"Doc Drug Program:.*", "")
                    .alias("DefensiveDrivingSchool"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Community Service:")
                    .str.strip_chars()
                    .cast(pl.Int64, strict=False)
                    .alias("CommunityServiceHrs"),
                    pl.col("Sentence")
                    .str.extract(r"Bad Check School:(.+)")
                    .str.strip_chars()
                    .alias("BadCheckSchool"),
                    pl.col("Sentence")
                    .str.extract(r"Drug Court:(.+)")
                    .str.strip_chars()
                    .alias("CourtReferralProgram"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)Drug Court:[^\n]*\n([^\n]+)")
                    .str.extract(r"(X)")
                    .alias("DocCommunityCorrections"),
                    # enhanced
                    pl.col("Sentence")
                    .str.extract(r"Drug Near Project: (.+?) Drugs")
                    .alias("DrugNearProject"),
                    pl.col("Sentence")
                    .str.extract(r"Habitual Offender: (.+)")
                    .str.strip_chars()
                    .alias("HabitualOffender"),
                    pl.col("Sentence")
                    .str.extract(r"Drug:(.+?)Drug")
                    .str.strip_chars()
                    .alias("Drug"),
                    pl.col("Sentence")
                    .str.extract(r"Sex Offender Community Notification:(.+)")
                    .str.strip_chars()
                    .alias("SexOffenderCommunityNotification"),
                    pl.col("Sentence")
                    .str.extract(r"Drug Code:(.+)")
                    .str.strip_chars()
                    .alias("DrugCode"),
                    pl.col("Sentence")
                    .str.extract(r"Victim DOB: (.+)")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("VictimDOB"),
                    pl.col("Sentence")
                    .str.extract(r"Drugs Near School:(.+)")
                    .str.strip_chars()
                    .alias("DrugsNearSchool"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Drug Volume:")
                    .str.strip_chars()
                    .cast(pl.Float64, strict=False)
                    .alias("DrugVolume"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)([^\n]+)\n\s*Victim DOB")
                    .str.strip_chars()
                    .alias("DrugMeasureUnit"),
                    pl.col("Sentence")
                    .str.extract(r"(.+) Habitual Offender Number:")
                    .alias("HabitualOffenderNumber"),
                )
            )
            if not debug:
                df = df.select(
                    "CaseNumber",
                    "Sentence#",
                    "RequirementsCompleted",
                    "SentenceProvisions",
                    "JailCreditPeriod",
                    "SentenceDate",
                    "SentenceStartDate",
                    "SentenceEndDate",
                    "ProbationPeriod",
                    "ProbationBeginDate",
                    "ProbationRevoke",
                    "LicenseSuspPeriod",
                    "LastUpdate",
                    "UpdatedBy",
                    "Costs",
                    "Fine",
                    "FineImposed",
                    "FineSuspended",
                    "ImmigrationFine",
                    "CrimeVictimsFee",
                    "CrimeHistoryFee",
                    "LicenseSuspensionFee",
                    "DrugUserFee",
                    "WCFee85%",
                    "MunicipalCourt",
                    "JailFee",
                    "DrugDocketFees",
                    "WCFeeDA",
                    "AliasWarrant",
                    "SX10",
                    "PrelimHearing",
                    "DemandReductionHearing",
                    "ImposedConfinementPeriod",
                    "SuspendedConfinementPeriod",
                    "TotalConfinementPeriod",
                    "Penitentiary",
                    "LifeWithoutParole",
                    "BootCamp",
                    "Jail",
                    "Life",
                    "Death",
                    "ReverseSplit",
                    "ElectronicMonitoring",
                    "ConsecutiveSentence",
                    "CoterminousSentence",
                    "ChainGang",
                    "JailDiversion",
                    "InformalProbation",
                    "DuiSchool",
                    "DefensiveDrivingSchool",
                    "DocDrugProgram",
                    "BadCheckSchool",
                    "CourtReferralProgram",
                    "CommunityServiceHrs",
                    "DrugNearProject",
                    "SexOffenderCommunityNotification",
                    "DrugsNearSchool",
                    "HabitualOffender",
                    "HabitualOffenderNumber",
                    "VictimDOB",
                    "Drug",
                    "DrugCode",
                    "DrugVolume",
                    "DrugMeasureUnit",
                )
        self._sentences = df
        return self._sentences

    def enforcement(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make enforcement table."""
        if isinstance(self._enforcement, pl.DataFrame):
            return self._enforcement
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing enforcement…"):
            df = (
                self.archive.select("CaseNumber", "AllPagesText")
                # get all fields
                .with_columns(
                    pl.col("AllPagesText")
                    .str.extract_all(r"Payor: (.+?)Enforcement")
                    .alias("Payor"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Payor: .+?Enforcement Status: (.+)")
                    .alias("EnforcementStatus"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Amount Due: (.+)")
                    .alias("AmountDue"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Due Date:(.+?)Last")
                    .alias("DueDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Over/Under Paid:(.+?)D999")
                    .alias("OverUnderPaid"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(?s)D999([^\n]+?)\n\s*PreTrial:(.+?)PreTrail")
                    .alias("PreTrial"),
                    pl.col("AllPagesText")
                    .str.extract_all(
                        r"(?s)Pre Terms Date:[\s\n]*([^\n]+)[\s\n]*Delinquent:"
                        r"(.+?)Delinquent"
                    )
                    .alias("Delinquent"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Warrant Mailer:(.+?)Warrant Mailer")
                    .alias("WarrantMailer"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Last Paid Date:(.+)")
                    .alias("LastPaidDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"TurnOver Date:(.+)")
                    .alias("TurnOverDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"PreTrail Date:(.+)")
                    .alias("PreTrialDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Delinquent Date:(.+?)DA Mailer")
                    .alias("DelinquentDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Warrant Mailer Date: (.+?)Last Update")
                    .alias("WarrantMailerDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(.+)Amount Paid:")
                    .alias("AmountPaid"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Frequency:(.+)")
                    .alias("Frequency"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(.+)TurnOver Amt: (.+)")
                    .alias("TurnOverAmt"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"PreTrial Terms: (.+)")
                    .alias("PreTrialTerms"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"DA Mailer: (.+)")
                    .alias("DAMailer"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Warrant Mailer Date:.+?Last Update: (.+)")
                    .alias("LastUpdate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Placement Status:(.+)")
                    .alias("PlacementStatus"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Balance:(.+)")
                    .alias("Balance"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Frequency Amt:(.+)")
                    .alias("FrequencyAmt"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(?s)D999 Amt: +([^\n]+)\n\s*PreTrial:")
                    .alias("D999Amt"),
                    pl.col("AllPagesText")
                    .str.extract_all(
                        r"(?s)Pre Terms Date:[\s\n]*([^\n]+)[\s\n]*Delinquent:"
                    )
                    .alias("PreTermsDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(?s)DA Mailer Date: ([^\n]+)\n\s*Warrant Mailer")
                    .alias("DAMailerDate"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"Warrant Mailer Date:.+?Updated By:(.+)")
                    .alias("UpdatedBy"),
                )
                .with_columns(pl.col("Payor").list.len().alias("payor_count"))
                # correct mismatched counts
                .with_columns(
                    pl.when(pl.col("OverUnderPaid").list.len() > pl.col("payor_count"))
                    .then(pl.col("OverUnderPaid").list.head(pl.col("payor_count")))
                    .otherwise(pl.col("OverUnderPaid"))
                    .alias("OverUnderPaid"),
                    pl.when(pl.col("WarrantMailer").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)DA Mailer Date:([^\n]+?)\n\s*Warrant"
                            r" Mailer(.+?)Warrant Mailer"
                        )
                    )
                    .otherwise(pl.col("WarrantMailer"))
                    .alias("WarrantMailer"),
                    pl.when(pl.col("TurnOverDate").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)(Enforcement|Updated By)([^\n]+?)\n\s*TurnOver"
                            r" Date:([^\n]+)"
                        )
                    )
                    .otherwise(pl.col("TurnOverDate"))
                    .alias("TurnOverDate"),
                    pl.when(pl.col("PreTrialDate").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)D999[^\n]+?\n\s*[^\n]+PreTrail Date:([^\n]+)"
                        )
                    )
                    .otherwise(pl.col("PreTrialDate"))
                    .alias("PreTrialDate"),
                    pl.when(
                        pl.col("DelinquentDate").list.len() != pl.col("payor_count")
                    )
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)Pre Terms Date:[^\n]+?\n\s*[^\n]+Delinquent"
                            r" Date(.+?)DA Mailer"
                        )
                    )
                    .otherwise(pl.col("DelinquentDate"))
                    .alias("DelinquentDate"),
                    pl.when(
                        pl.col("WarrantMailerDate").list.len() != pl.col("payor_count")
                    )
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)DA Mailer Date:[^\n]+?\n\s*[^\n]+Warrant Mailer"
                            r" Date(.+?)Last"
                        )
                    )
                    .otherwise(pl.col("WarrantMailerDate"))
                    .alias("WarrantMailerDate"),
                    pl.when(
                        pl.col("payor_count").eq(0)
                        & pl.col("Frequency").list.len().eq(1)
                    )
                    .then(None)
                    .otherwise(pl.col("Frequency"))
                    .alias("Frequency"),
                    pl.when(pl.col("TurnOverAmt").list.len() > pl.col("payor_count"))
                    .then(
                        pl.col("TurnOverAmt").map_elements(
                            lambda amts: [amt for amt in amts if "Alacourt" not in amt]
                        )
                    )
                    .otherwise(pl.col("TurnOverAmt"))
                    .alias("TurnOverAmt"),
                    pl.when(pl.col("PreTrialTerms").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)D999[^\n]+?\n\s*[^\n]+PreTrial Terms([^\n]+)"
                        )
                    )
                    .otherwise(pl.col("PreTrialTerms"))
                    .alias("PreTrialTerms"),
                    pl.when(pl.col("DAMailer").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)Pre Terms Date:[^\n]+?\n\s*[^\n]+DA Mailer"
                            r" Date:([^\n]+?)"
                        )
                    )
                    .otherwise(pl.col("DAMailer"))
                    .alias("DAMailer"),
                    pl.when(pl.col("LastUpdate").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"(?s)DA Mailer Date:[^\n]+?\n\s*[^\n]+Last"
                            r" Update:([^\n]+?)"
                        )
                    )
                    .otherwise(pl.col("LastUpdate"))
                    .alias("LastUpdate"),
                    pl.when(pl.col("DAMailerDate").list.len() != pl.col("payor_count"))
                    .then(
                        pl.col("AllPagesText").str.extract_all(r"DA Mailer Date: (.+)")
                    )
                    .otherwise(pl.col("DAMailerDate"))
                    .alias("DAMailerDate"),
                    pl.when(pl.col("UpdatedBy").list.len() > pl.col("payor_count"))
                    .then(pl.col("UpdatedBy").list.head(pl.col("payor_count")))
                    .otherwise(pl.col("UpdatedBy"))
                    .alias("UpdatedBy"),
                )
                # correct still mismatched counts
                .with_columns(
                    pl.when(
                        pl.col("WarrantMailerDate").list.len() != pl.col("payor_count")
                    )
                    .then(
                        pl.col("AllPagesText").str.extract_all(
                            r"Warrant Mailer Date: (.+)"
                        )
                    )
                    .otherwise(pl.col("WarrantMailerDate"))
                    .alias("WarrantMailerDate")
                )
                .drop("AllPagesText")
                .explode(
                    "Payor",
                    "AmountDue",
                    "DueDate",
                    "OverUnderPaid",
                    "PreTrial",
                    "Delinquent",
                    "WarrantMailer",
                    "EnforcementStatus",
                    "LastPaidDate",
                    "TurnOverDate",
                    "PreTrialDate",
                    "DelinquentDate",
                    "WarrantMailerDate",
                    "AmountPaid",
                    "Frequency",
                    "TurnOverAmt",
                    "PreTrialTerms",
                    "DAMailer",
                    "LastUpdate",
                    "PlacementStatus",
                    "Balance",
                    "FrequencyAmt",
                    "D999Amt",
                    "PreTermsDate",
                    "DAMailerDate",
                    "UpdatedBy",
                )
                .with_columns(
                    pl.col("Payor").str.extract(r"Payor: ([^\s]+)"),
                    pl.col("AmountDue")
                    .str.extract(r"(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("DueDate")
                    .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("OverUnderPaid")
                    .str.extract(r"(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("PreTrial").str.extract(r"PreTrial: (.+) PreTrail"),
                    pl.col("Delinquent").str.extract(r"Delinquent: (.+) Delinquent"),
                    pl.col("WarrantMailer").str.extract(
                        r"Warrant Mailer: (.+) Warrant Mailer"
                    ),
                    pl.col("EnforcementStatus")
                    .str.extract(r"Enforcement Status: (.+)")
                    .str.strip_chars()
                    .str.replace_all(r"\s+", " ")
                    .str.replace(r"RECEIPTING,$", "RECEIPTING, DA TURNOVE"),
                    pl.col("LastPaidDate")
                    .str.extract(r"Last Paid Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("TurnOverDate")
                    .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("PreTrialDate")
                    .str.extract(r"PreTrail Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("DelinquentDate")
                    .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("WarrantMailerDate")
                    .str.extract(r"Warrant Mailer Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("AmountPaid")
                    .str.extract(r"(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("Frequency")
                    .str.extract(r"Frequency: (.+)")
                    .str.strip_chars(),
                    pl.col("TurnOverAmt")
                    .str.extract(r"TurnOver Amt: *(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("PreTrialTerms").str.extract(r"PreTrial Terms: *([^\s]+)"),
                    pl.col("DAMailer").str.extract(
                        r"DA Mailer: *([^\s]+) DA Mailer Date"
                    ),
                    pl.col("LastUpdate")
                    .str.extract(r"Last Update: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("PlacementStatus")
                    .str.extract(r"Placement Status: (.+)")
                    .str.strip_chars(),
                    pl.col("Balance")
                    .str.extract(r"(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("FrequencyAmt")
                    .str.extract(r"(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("D999Amt")
                    .str.extract(r"(\-?\$[0-9,]+\s*\.\s*\d\d)")
                    .str.replace_all(r"\$|\s|,", "")
                    .cast(pl.Float64, strict=False),
                    pl.col("PreTermsDate")
                    .str.extract(r"Pre Terms Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("DAMailerDate")
                    .str.extract(r"DA Mailer Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False),
                    pl.col("UpdatedBy").str.extract(r"Updated By: ([^\s]+)"),
                )
                .drop("payor_count")
                .filter(pl.col("Payor").is_not_null())
            )
        self._enforcement = df
        return self._enforcement

    def settings(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make settings table."""
        if debug:
            self._settings = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._settings, pl.DataFrame)
            and "Settings" in self._settings.columns
        ):
            self._settings = None
        if isinstance(self._settings, pl.DataFrame):
            return self._settings
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing settings…"):
            df = (
                self.archive.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"Description\:\s*\n\s*(?s)Settings(.+?)Court Action")
                    .str.split("\n")
                    .alias("Settings"),
                )
                .explode("Settings")
                .with_columns(pl.col("Settings").str.strip_chars())
                .filter(pl.col("Settings").str.contains(r"^DOB|SSN").not_())
                .filter(pl.col("Settings").str.contains(r"00/00").not_())
                .filter(
                    pl.col("Settings").str.contains(r"^\d\d?/\d\d?/\d\d\d\d").not_()
                )
                .filter(pl.col("Settings").str.contains(r"[A-Z]"))
                .filter(pl.col("Settings").str.contains("Date").not_())
                .filter(pl.col("Settings").is_not_null())
                .filter(pl.col("Settings").str.contains(r"[a-z]").not_())
                .with_columns(
                    pl.col("CaseNumber"),
                    pl.col("Settings")
                    .str.extract(r"^(\d) ")
                    .cast(pl.Int64, strict=False)
                    .alias("Number"),
                    pl.col("Settings")
                    .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("Date"),
                    pl.col("Settings")
                    .str.extract(r"\d\d?/\d\d?/\d\d\d\d (\d\d\d)")
                    .alias("Que"),
                    pl.col("Settings")
                    .str.extract(
                        r"\d\d?/\d\d?/\d\d\d\d \d\d\d (\d\d?\:\d\d (AM|PM)?)",
                        group_index=1,
                    )
                    .alias("Time"),
                    pl.col("Settings")
                    .str.extract(
                        r"\d\d?/\d\d?/\d\d\d\d \d\d\d \d\d?\:\d\d (AM|PM)?(.+)",
                        group_index=2,
                    )
                    .str.strip_chars()
                    .alias("Description"),
                )
                .filter(pl.col("Date").is_not_null())
            )
            if not debug:
                df = df.select(
                    "CaseNumber",
                    "Number",
                    "Date",
                    "Que",
                    "Time",
                    "Description",
                )
        self._settings = df
        return self._settings

    def case_action_summary(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make case action summary table."""
        if debug:
            self._case_action_summary = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._case_action_summary, pl.DataFrame)
            and "Row" in self._case_action_summary.columns
        ):
            self._case_action_summary = None
        if isinstance(self._case_action_summary, pl.DataFrame):
            return self._case_action_summary
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing case action summaries…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract(r"(?s)Case Action Summary(.+?) (?:Date|END OF THE REPORT)")
                .str.replace(r"\s*\n\s*Operator\s*", "")
                .alias("CAS"),
            ).drop_nulls("CAS")
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("CAS").map_elements(
                            lambda x: re.split(r"(\d\d?/\d\d?/\d\d\d\d)\s*\n", x)
                        )
                    )
                    .select(
                        pl.col("CaseNumber"),
                        pl.col("CAS").map_elements(lambda x: x[::2][:-1]).alias("Row"),
                        pl.col("CAS").map_elements(lambda x: x[1::2]).alias("Date"),
                    )
                    .explode("Row", "Date")
                    .with_columns(
                        pl.col("Row")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.strip_chars()
                    )
                    .with_columns(
                        pl.col("CaseNumber"),
                        pl.col("Date").str.to_date("%m/%d/%Y", strict=False),
                        pl.col("Row")
                        .str.extract(r"^(\w |\w\w\w |\w\w\w\d\d\d )")
                        .str.strip_chars()
                        .alias("Operator"),
                        pl.col("Row")
                        .str.extract(
                            (
                                r"(?s)^(\w |\w\w\w |\w\w\w\d\d\d )?(.+?) ([A-Z0-9-]+)"
                                r" (\d\d?:\d\d [AP]M)"
                            ),
                            group_index=2,
                        )
                        .str.replace("\n", "")
                        .str.strip_chars()
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(
                            (
                                r"(?s)^(\w |\w\w\w |\w\w\w\d\d\d )?(.+?) ([A-Z0-9-]+)"
                                r" (\d\d?:\d\d [AP]M)"
                            ),
                            group_index=3,
                        )
                        .alias("Code"),
                        pl.col("Row")
                        .str.extract(
                            (
                                r"(?s)^(\w |\w\w\w |\w\w\w\d\d\d )?(.+?) ([A-Z0-9-]+)"
                                r" (\d\d?:\d\d [AP]M)"
                            ),
                            group_index=4,
                        )
                        .alias("Time"),
                    )
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Date",
                        "Operator",
                        "Description",
                        "Code",
                        "Time",
                    )
                df = df.filter(pl.col("Description").is_not_null())
            else:
                columns = [
                    "CaseNumber",
                    "Date",
                    "Operator",
                    "Description",
                    "Code",
                    "Time",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._case_action_summary = df
        return self._case_action_summary

    def financial_history(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make financial history table."""
        if debug:
            self._financial_history = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._financial_history, pl.DataFrame)
            and "Row" in self._financial_history.columns
        ):
            self._financial_history = None
        if isinstance(self._financial_history, pl.DataFrame):
            return self._financial_history
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing financial history…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract(
                    r"(?s)Financial History(.+?)"
                    r"(Requesting Party|Date:|END OF THE REPORT)",
                    group_index=1,
                )
                .str.replace_all(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                .str.replace(
                    (
                        r"(?s)\s*\n Description From Party To Party Admin"
                        r" Fee\s*\n\s*Money Type\s*\n\s*Reason Disbursement"
                        r" Accoun\s*\n\s*Transaction Batch\s*\n\s*Operator\s*\n\s*"
                    ),
                    "",
                )
                .str.replace(
                    (
                        r"(?s)\s*Transaction Date\s*\n\s*Attorney Receipt Number"
                        r" Amount Description From Party To Party Admin"
                        r" Fee\s*\n\s*Money Type\s*\n\s*Reason Disbursement"
                        r" Accoun\s*\n\s*Transaction Batch\s*\n\s*Operator\s*\n\s*"
                    ),
                    "",
                )
                .str.replace(r"(?s)\s*\n\s*SJIS Witness List\s*\n\s*", "")
                .alias("FinancialHistory"),
            ).drop_nulls("FinancialHistory")
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("FinancialHistory").map_elements(
                            lambda x: re.split(r"(\d\d/\d\d/\d\d\d\d)", x)
                        )
                    )
                    .with_columns(
                        pl.col("FinancialHistory")
                        .map_elements(lambda x: x[::2][1:])
                        .alias("Row"),
                        pl.col("FinancialHistory")
                        .map_elements(lambda x: x[1::2])
                        .alias("TransactionDate"),
                    )
                    .explode("Row", "TransactionDate")
                    .with_columns(
                        pl.col("Row")
                        .str.replace_all("\n", "")
                        .str.replace_all(" +", " ")
                        .str.replace_all(r"\. ", ".")
                        .str.strip_chars()
                        .str.replace(r"CHANGED ?\w?$", "")
                        .str.replace(r"DELETED$", "")
                        .str.replace(r"CHECK ?\w?$", "")
                        .str.replace(r" \w$", "")
                        .str.strip_chars(),
                        pl.col("TransactionDate").str.to_date("%m/%d/%Y", strict=False),
                    )
                    .with_columns(
                        pl.col("Row")
                        .str.extract(r"(.+?) \$")
                        .str.replace("REMITTANC E", "REMITTANCE")
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(r"(\-?\$[\d,]+\.\d+)")
                        .str.replace_all(r",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                        .alias("Amount"),
                        pl.col("Row")
                        .str.extract(r"(\-?\$[\d,]+\.\d+) ([^\s]{4})", group_index=2)
                        .alias("FromParty"),
                        pl.col("Row")
                        .str.extract(
                            r"(\-?\$[\d,]+\.\d+) ([^\s]{4}) ([^\s]{3,4})",
                            group_index=3,
                        )
                        .alias("ToParty"),
                        pl.col("Row")
                        .str.extract(r" (Y|N) ([^\s]{4}) (\d{8,})", group_index=1)
                        .alias("AdminFee"),
                        pl.col("Row")
                        .str.extract(r" ([^\s]{4}) (\d{8,})", group_index=1)
                        .alias("DisbursementAccount"),
                        pl.col("Row").str.extract(r"(\d{8,})").alias("ReceiptNumber"),
                        pl.col("Row")
                        .str.extract(r"(\d{8,}) (\d+)", group_index=2)
                        .alias("TransactionBatch"),
                        pl.col("Row")
                        .str.extract(r"(\w{3})( \w)?$", group_index=1)
                        .alias("Operator"),
                    )
                    .with_columns(
                        pl.col("Description").str.extract(r" (\w)$").alias("Reason")
                    )
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "TransactionDate",
                        "Description",
                        "DisbursementAccount",
                        "TransactionBatch",
                        "ReceiptNumber",
                        "Amount",
                        "FromParty",
                        "ToParty",
                        "AdminFee",
                        "Reason",
                        "Operator",
                    )
            else:
                columns = [
                    "CaseNumber",
                    "TransactionDate",
                    "Description",
                    "DisbursementAccount",
                    "TransactionBatch",
                    "ReceiptNumber",
                    "Amount",
                    "FromParty",
                    "ToParty",
                    "AdminFee",
                    "Reason",
                    "Operator",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
            self._financial_history = df
        return self._financial_history

    def witnesses(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make witnesses table."""
        if debug:
            self._witnesses = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._witnesses, pl.DataFrame)
            and "Row" in self._witnesses.columns
        ):
            self._witnesses = None
        if isinstance(self._witnesses, pl.DataFrame):
            return self._witnesses
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing witnesses tables…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract(
                    r"(?s)SJIS Witness List\s*\n\s*Date"
                    r" Issued\s*\n\s*Subpoena(.+?)"
                    r"(?:Date:|END OF THE REPORT)"
                )
                .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                .str.replace(r"Requesting Party Witness # Name", "")
                .str.replace(
                    r"Date Served Service Type Attorney Issued Type Date Issued", ""
                )
                .alias("Witnesses"),
            ).drop_nulls("Witnesses")
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("Witnesses").map_elements(
                            lambda x: re.split(r"( [A-Z0-9]{4}\s*\n)", x)
                        )
                    )
                    .select(
                        pl.col("CaseNumber"),
                        pl.col("Witnesses")
                        .map_elements(lambda x: x[::2][:-1])
                        .alias("Row"),
                        pl.col("Witnesses")
                        .map_elements(lambda x: x[1::2])
                        .alias("Witness#"),
                    )
                    .explode("Row", "Witness#")
                    .with_columns(
                        pl.col("Witness#").str.replace("\n", "").str.strip_chars(),
                        pl.col("Row")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.replace_all("\n", "")
                        .str.replace_all(r"\s+", " ")
                        .str.strip_chars(),
                    )
                    .filter(pl.col("Row").str.contains(r"[A-Za-z0-9]"))
                    .with_columns(
                        pl.col("Row")
                        .str.extract(
                            r"(.+?)( [A-Z]?\d\d\d|$|\d\d/\d\d/\d\d\d\d)",
                            group_index=1,
                        )
                        .str.replace(
                            r"SERVED PERSONALLY |OTHER |CERTIFIED MAIL "
                            r"|PROCESS SERVER ",
                            "",
                        )
                        .str.strip_chars()
                        .alias("Name"),
                        pl.col("Row")
                        .str.extract(
                            r"(SERVED PERSONALLY|OTHER|CERTIFIED MAIL|PROCESS SERVER)"
                        )
                        .alias("ServiceType"),
                        pl.col("Row")
                        .str.extract(r" ([A-Z]?\d\d\d)")
                        .alias("RequestingParty"),
                        pl.col("Row")
                        .str.extract(
                            r" [A-Z]?\d\d\d (SHERIFF|VIDEO|PROCESS"
                            r" SERVER|CERTIFIED|OTHER)"
                        )
                        .alias("IssuedType"),
                        pl.col("Row")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d) \d\d/\d\d/\d\d\d\d")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DateServed"),
                        pl.col("Row")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)$")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DateIssued"),
                    )
                    .filter(pl.col("Witness#").is_not_null())
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Witness#",
                        "Name",
                        "RequestingParty",
                        "DateIssued",
                        "IssuedType",
                        "DateServed",
                        "ServiceType",
                    )
            else:
                columns = [
                    "CaseNumber",
                    "Witness#",
                    "Name",
                    "RequestingParty",
                    "DateIssued",
                    "IssuedType",
                    "DateServed",
                    "ServiceType",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
            self._witnesses = df
        return self._witnesses

    def attorneys(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make attorneys table."""
        if debug:
            self._attorneys = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._attorneys, pl.DataFrame)
            and "Attorneys" in self._attorneys.columns
        ):
            self._attorneys = None
        if isinstance(self._attorneys, pl.DataFrame):
            return self._attorneys
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing attorneys tables…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract_all(
                    r"(?s)Attorney Code\s*\n\s*(.+?)(Warrant|Financial|Alt Name)"
                )
                .alias("Attorneys"),
            ).filter(pl.col("Attorneys").list.len() > 0)
            if df.shape[0] > 0:
                df = (
                    df.explode("Attorneys")
                    .with_columns(
                        pl.col("Attorneys")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.replace(
                            r"\s+Number Type of Counsel Name Phone Email Attorney"
                            r" Code\s+",
                            "",
                        )
                        .str.replace(r"Attorney Code +\n", "")
                        .str.replace(r"Attorney Code", "")
                        .str.replace(r"(Warrant|Alt Name|Financial)", "")
                        .map_elements(lambda x: re.split(r"(\s[A-Z0-9']{6}\s+\n)", x))
                    )
                    .with_columns(
                        pl.col("Attorneys")
                        .map_elements(lambda x: x[::2][:-1])
                        .alias("Row"),
                        pl.col("Attorneys")
                        .map_elements(lambda x: x[1::2])
                        .alias("AttorneyCode"),
                    )
                    .explode("Row", "AttorneyCode")
                    .with_columns(
                        pl.col("Row").str.replace_all("\n", "").str.strip_chars()
                    )
                    .filter(
                        pl.col("Row")
                        .str.replace(r"Attorney|Prosecutor", "")
                        .str.contains(r"[a-z]")
                        .not_()
                    )
                    .with_columns(
                        pl.col("CaseNumber"),
                        pl.col("Row")
                        .str.extract(r"(Attorney \d+|Prosecutor \d+)$")
                        .alias("Number"),
                        pl.col("AttorneyCode").str.strip_chars(),
                        pl.col("Row").str.extract(r"^(\w-\w+)").alias("TypeOfCounsel"),
                        pl.col("Row")
                        .str.extract(
                            r"^(\w-\w+)?(.+?) ([^\s]+\s*@|\(\d)", group_index=2
                        )
                        .str.strip_chars()
                        .alias("Name"),
                        pl.col("Row")
                        .str.extract(
                            r"([^\s]+\s*@\s*[^\.]+\s*\.\s*[^\s]+)",
                            group_index=1,
                        )
                        .str.replace_all(r" ", "")
                        .alias("Email"),
                        pl.col("Row")
                        .str.extract(
                            r"(\(\d\d\d\) \d\d\d-\d\d\d\d) (Attorney \d+|Prosecutor"
                            r" \d+)",
                            group_index=1,
                        )
                        .alias("Phone"),
                    )
                    # fix P-PUBLIC with DEFENDER in name
                    .with_columns(
                        pl.when(pl.col("TypeOfCounsel") == "P-PUBLIC")
                        .then(
                            pl.col("Name")
                            .str.replace(r"^DEFENDER ", "")
                            .str.strip_chars()
                        )
                        .otherwise(pl.col("Name"))
                        .alias("Name"),
                        pl.when(pl.col("TypeOfCounsel") == "P-PUBLIC")
                        .then(pl.lit("P-PUBLIC DEFENDER"))
                        .otherwise(pl.col("TypeOfCounsel"))
                        .alias("TypeOfCounsel"),
                    )
                    # fix S-PRO with SE in name
                    .with_columns(
                        pl.when(pl.col("TypeOfCounsel") == "S-PRO")
                        .then(pl.col("Name").str.replace(r"^SE ", "").str.strip_chars())
                        .otherwise(pl.col("Name"))
                        .alias("Name"),
                        pl.when(pl.col("TypeOfCounsel") == "S-PRO")
                        .then(pl.lit("S-PRO SE"))
                        .otherwise(pl.col("TypeOfCounsel"))
                        .alias("TypeOfCounsel"),
                    )
                    # fix missing PRO SE names
                    .with_columns(
                        pl.when(
                            pl.col("Name").is_null()
                            & pl.col("Row").str.contains("PRO SE")
                        )
                        .then(pl.lit("PRO SE"))
                        .otherwise(pl.col("Name"))
                        .alias("Name")
                    )
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Number",
                        "AttorneyCode",
                        "TypeOfCounsel",
                        "Name",
                        "Email",
                        "Phone",
                    )
            else:
                columns = [
                    "CaseNumber",
                    "Number",
                    "AttorneyCode",
                    "TypeOfCounsel",
                    "Name",
                    "Email",
                    "Phone",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
            self._attorneys = df
        return self._attorneys

    def images(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make images table."""
        if debug:
            self._images = None
        # if previously called with debug=True, reset
        if isinstance(self._images, pl.DataFrame) and "Row" in self._images.columns:
            self._images = None
        if isinstance(self._images, pl.DataFrame):
            return self._images
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing images tables…"):
            df = (
                self.archive.with_columns(
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)Images(.+)(END OF THE REPORT|.$)")
                    .str.replace(r"\n Pages\s*", "")
                    .alias("Images")
                )
            ).drop_nulls("Images")
            if df.shape[0] > 0:
                df = (
                    df.select(
                        pl.col("CaseNumber"),
                        pl.col("Images").map_elements(
                            lambda x: re.split(r"(\d\d?:\d\d:\d\d [AP]M)", x)
                        ),
                    )
                    .select(
                        pl.col("CaseNumber"),
                        pl.col("Images")
                        .map_elements(lambda x: x[::2][:-1])
                        .alias("Row"),
                        pl.col("Images").map_elements(lambda x: x[1::2]).alias("Time"),
                    )
                    .explode("Row", "Time")
                    .with_columns(
                        pl.col("Row")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.replace(r"Date: Description Doc# Title  \n Images", "")
                        .str.replace_all(r"\n", " ")
                        .str.strip_chars(),
                        pl.col("Time").str.strip_chars(),
                    )
                    .with_columns(
                        pl.col("CaseNumber"),
                        pl.col("Row")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Date"),
                        pl.col("Time"),
                        pl.col("Row")
                        .str.extract(r"\d+ [^0-9]+ (\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("Doc#"),
                        pl.col("Row")
                        .str.extract(r"\d+ ([^0-9]+)")
                        .str.strip_chars()
                        .alias("Title"),
                        pl.col("Row")
                        .str.extract(r"(?s)\d+ [^0-9]+ \d+ (.+) \d\d?/\d\d?/\d\d\d\d$")
                        .str.strip_chars()
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(r"^(\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("Pages"),
                    )
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Date",
                        "Time",
                        "Doc#",
                        "Title",
                        "Description",
                        "Pages",
                    )
                df = df.drop_nulls("Date")
            else:
                columns = [
                    "CaseNumber",
                    "Date",
                    "Time",
                    "Doc#",
                    "Title",
                    "Description",
                    "Pages",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._images = df
        return self._images

    def restitution(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make restitution table."""
        if debug:
            self._restitution = None
        # if previously called with debug=True, reset
        if (
            isinstance(self._restitution, pl.DataFrame)
            and "RestitutionRaw" in self._restitution.columns
        ):
            self._restitution = None
        if isinstance(self._restitution, pl.DataFrame):
            return self._restitution
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing restitution tables…"):
            df = (
                self.archive.select("CaseNumber", "AllPagesText")
                .select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(?s)Restitution (.+?) (Programs|Split)")
                    .alias("RestitutionRaw"),
                )
                .explode("RestitutionRaw")
                .with_columns(
                    pl.col("RestitutionRaw")
                    .str.replace("Restitution", "")
                    .str.replace("Programs", "")
                    .str.replace("Split", "")
                    .str.replace(r"Recipient Description Amount\s*\n", "")
                    .str.replace(r"Restitution\s*\n", "")
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.replace(r"(?s)Linked Cases.+", "")
                    .str.replace(r"(?s)Enhanced.+", "")
                    .str.replace(r"(?s)Chain Gang.+", "")
                    .str.strip_chars()
                    .str.split("\n")
                    .alias("Restitution")
                )
                .explode("Restitution")
                .filter(pl.col("Restitution") != "")
                .with_columns(pl.col("Restitution").str.strip_chars())
                .filter(pl.col("Restitution").str.contains(r"^\w \d+ \d+\.\d\d"))
                .with_columns(
                    pl.col("CaseNumber"),
                    pl.col("Restitution").str.extract(r"^(\w) ").alias("Restitution"),
                    pl.col("Restitution")
                    .str.extract(r"^\w ([^\s]+) ")
                    .cast(pl.Int64, strict=False)
                    .alias("Description"),
                    pl.col("Restitution")
                    .str.extract(r"\w [^\s]+ (\d+\.\d\d)")
                    .cast(pl.Float64, strict=False)
                    .alias("Amount"),
                    pl.col("Restitution")
                    .str.extract(r"\w [^\s]+ \d+\.\d\d ([A-Z0-9]+)")
                    .alias("Recipient"),
                )
            )
            if not debug:
                df = df.select(
                    "CaseNumber",
                    "Recipient",
                    "Restitution",
                    "Description",
                    "Amount",
                )
        self._restitution = df
        return self._restitution

    def linked_cases(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make linked cases table."""
        if debug:
            self._linked_cases = None
        if (
            isinstance(self._linked_cases, pl.DataFrame)
            and "LinkedCases" in self._linked_cases.columns
        ):
            self._linked_cases = None
        if isinstance(self._linked_cases, pl.DataFrame):
            return self._linked_cases
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing linked cases tables…"):
            df = (
                self.archive.select("CaseNumber", "AllPagesText")
                .select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract_all(
                        r"(?s)Linked Cases\s*\n\s*Sentencing Number Case Type Case Type"
                        r" Description CaseNumber(.+?)Enforcement|Sentence"
                    )
                    .alias("LinkedCases"),
                )
                .explode("LinkedCases")
                .with_columns(
                    pl.col("LinkedCases")
                    .str.replace("Sentence", "")
                    .str.replace(r"Sentencing.+", "")
                    .str.replace("Linked Cases", "")
                    .str.replace("Enforcement", "")
                    .str.replace(r"(?s)\d\s*\n\s*Last Update.+", "")
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.strip_chars()
                    .str.split("\n")
                )
                .explode("LinkedCases")
                .with_columns(
                    pl.when(pl.col("LinkedCases") == "")
                    .then(None)
                    .otherwise(pl.col("LinkedCases"))
                    .alias("LinkedCases")
                )
                .with_columns(pl.col("LinkedCases").str.strip_chars())
                .with_columns(
                    pl.col("CaseNumber"),
                    pl.col("LinkedCases")
                    .str.extract(r"^(\d+) ")
                    .cast(pl.Int64, strict=False)
                    .alias("SentencingNumber"),
                    pl.col("LinkedCases").str.extract(r"^\d+ (\w) ").alias("CaseType"),
                    pl.col("LinkedCases")
                    .str.extract(r"\d+ \w ([A-Z]+)")
                    .alias("CaseTypeDescription"),
                    pl.col("LinkedCases")
                    .str.extract(
                        r"\d+ \w [A-Z]+ (\d\d-\w\w-\d\d\d\d-\d\d\d\d\d\d\.\d\d)"
                    )
                    .alias("LinkedCaseNumber"),
                )
                .drop_nulls("LinkedCaseNumber")
            )
            if not debug:
                df = df.select(
                    "CaseNumber",
                    "SentencingNumber",
                    "CaseType",
                    "CaseTypeDescription",
                    "LinkedCaseNumber",
                )
        self._linked_cases = df
        return self._linked_cases

    def continuances(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make continuances table."""
        if debug:
            self._continuances = None
        if (
            isinstance(self._continuances, pl.DataFrame)
            and "Continuances" in self._continuances.columns
        ):
            self._continuances = None
        if isinstance(self._continuances, pl.DataFrame):
            return self._continuances
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing continuances…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract(
                    r"(?s)Continuances.+?Comments[\s\n]*(.+?)\s*\n\s*"
                    r"(?:Court Action|Parties)"
                )
                .str.replace(r"(?s)Parties.+", "")
                .str.replace(r"(?s)Charges.+", "")
                .str.replace_all(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                .alias("Continuances"),
            ).drop_nulls("Continuances")
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("Continuances").map_elements(
                            lambda x: re.split(
                                r"(\d\d?/\d\d?/\d\d\d\d \d\d?:\d\d?:\d\d [AP]M)",
                                x,
                            )
                        )
                    )
                    .with_columns(
                        pl.col("Continuances")
                        .map_elements(lambda x: x[::2][1:])
                        .alias("Row"),
                        pl.col("Continuances")
                        .map_elements(lambda x: x[1::2])
                        .alias("DateTime"),
                    )
                    .explode("Row", "DateTime")
                    .with_columns(
                        pl.col("Row").str.replace_all("\n", "").str.strip_chars()
                    )
                    .with_columns(
                        pl.col("DateTime")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Date"),
                        pl.col("DateTime")
                        .str.extract(r"(\d\d:\d\d:\d\d [AP]M)")
                        .alias("Time"),
                        pl.col("Row").str.extract(r"^(\w+)").alias("Code"),
                        pl.col("Row")
                        .str.extract(r"^\w+ (.+) \w+$")
                        .str.strip_chars()
                        .alias("Comments"),
                        pl.col("Row").str.extract(r"(\w+)$").alias("Operator"),
                    )
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Date",
                        "Time",
                        "Code",
                        "Comments",
                        "Operator",
                    )
            else:
                columns = ["CaseNumber", "Date", "Time", "Code", "Comments", "Operator"]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._continuances = df
        return self._continuances

    def parties(self: "Cases", *, debug: bool = False) -> pl.DataFrame:
        """Make parties table."""
        if debug:
            self._parties = None
        if (
            isinstance(self._parties, pl.DataFrame)
            and "Parties" in self._parties.columns
        ):
            self._parties = None
        if isinstance(self._parties, pl.DataFrame):
            return self._parties
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing parties…"):
            df = (
                self.archive.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)Parties(.+)")
                    .str.replace(r"(?s)(Case Action Summary.+)", "")
                    .alias("Parties"),
                )
                .drop_nulls("Parties")
                .filter(pl.col("Parties").str.contains("Name:"))
            )
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("Parties")
                        .str.extract_all(r"(Party \d+ - .+)")
                        .alias("PartyDescription"),
                        pl.col("Parties")
                        .str.extract_all(r"Alt Name: (.+)")
                        .alias("AltName"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Name:")
                        .map_elements(
                            lambda names: [
                                name for name in names if "Alt Name:" not in name
                            ]
                        )
                        .alias("Name"),
                        pl.col("Parties")
                        .str.extract_all(r"(?s)\n\s*([^\n]+?Name: )?Type: ([^\n]+)")
                        .alias("Type"),
                        pl.col("Parties").str.extract_all(r"(.+)Index:").alias("Index"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Party:")
                        .map_elements(
                            lambda parties: [
                                party
                                for party in parties
                                if "Cost Against" not in party
                            ]
                        )
                        .alias("Party"),
                        pl.col("Parties")
                        .str.extract_all(r"(?s)Party:.+?Address 1: ([^\n]+)")
                        .alias("Address1"),
                        pl.col("Parties")
                        .str.extract_all(r"(?s)Party:.+?Phone: ([^\n]+)")
                        .alias("Phone"),
                        pl.col("Parties")
                        .str.extract_all(r"(?s)Address 1: (.+?) Address 2: ([^\n]+)")
                        .alias("Address2"),
                        pl.col("Parties")
                        .str.extract_all(r"JID:(.+?)Hardship")
                        .alias("JID"),
                        pl.col("Parties")
                        .str.extract_all(r"Hardship:(.+)")
                        .alias("Hardship"),
                        pl.col("Parties")
                        .str.extract_all(r"DOB:(.+)")
                        .map_elements(
                            lambda dobs: [dob for dob in dobs if "Phone" not in dob]
                        )
                        .alias("DOB"),
                        pl.col("Parties").str.extract_all(r"City:(.+)").alias("City"),
                        pl.col("Parties").str.extract_all(r"Race:(.+)").alias("Race"),
                        pl.col("Parties").str.extract_all(r"SSN:(.+)").alias("SSN"),
                        pl.col("Parties")
                        .str.extract_all(r"Country:(.+)")
                        .alias("Country"),
                        pl.col("Parties").str.extract_all(r"Sex:(.+)").alias("Sex"),
                        pl.col("Parties").str.extract_all(r"Zip:(.+)").alias("Zip"),
                        pl.col("Parties")
                        .str.extract_all(r"State: (.+)")
                        .alias("State"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Court Action:")
                        .alias("CourtAction"),
                        pl.col("Parties")
                        .str.extract_all(r"Court Action Date: (.+)")
                        .alias("CourtActionDate"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Amount of Judgement:")
                        .alias("AmountOfJudgement"),
                        pl.col("Parties")
                        .str.extract_all(r"(?s)([^\n]+)\n[^\n]*Warrant Action Date:")
                        .alias("CourtActionFor"),
                        pl.col("Parties")
                        .str.extract_all(r"Cost Against Party: (.+)")
                        .alias("CostAgainstPartyOtherCost"),
                        pl.col("Parties")
                        .str.extract_all(r"Reissue:(.+)")
                        .alias("ReissueIssued"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Issued Type:")
                        .alias("IssuedType"),
                        pl.col("Parties")
                        .str.extract_all(r"Reissue Type: (.+)")
                        .alias("ReissueType"),
                        pl.col("Parties")
                        .str.extract_all(r"(?m)^\s*Return: (.+)")
                        .alias("ReturnReturnType"),
                        pl.col("Parties")
                        .str.extract_all(r"Served: (.+)")
                        .alias("Served"),
                        pl.col("Parties")
                        .str.extract_all(r"Served:(.+?)Service Type (.+)")
                        .alias("ServiceType"),
                        pl.col("Parties")
                        .str.extract_all(r"Service On:(.+)")
                        .alias("ServiceOn"),
                        pl.col("Parties")
                        .str.extract_all(r"(?m)^\s*Answer: (.+)")
                        .alias("AnswerAnswerType"),
                        pl.col("Parties")
                        .str.extract_all(r"Notice of No Service:(.+)")
                        .alias("NoticeOfNoService"),
                        pl.col("Parties")
                        .str.extract_all(r"Notice of No Answer: (.+)")
                        .alias("NoticeOfNoAnswer"),
                        pl.col("Parties")
                        .str.extract_all(r"Served By: (.+)")
                        .alias("ServedBy"),
                        pl.col("Parties")
                        .str.extract_all(r"Comment: (.+)")
                        .alias("Comment"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Warrant Action Date: (.+)")
                        .alias("WarrantActionDate"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Warrant Action Status:(.+)")
                        .alias("WarrantActionStatusStatusDescription"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Exemptions:(.+)")
                        .alias("Exemptions"),
                        pl.col("Parties")
                        .str.extract_all(r"(.+)Date Satisfied:(.+)")
                        .alias("DateSatisfied"),
                        pl.col("Parties")
                        .str.extract_all(
                            r"(?s)Date Satisfied:[^\n]+\n([^\n]+)Arrest Date:([^\n]+)"
                        )
                        .alias("ArrestDate"),
                    )
                    .with_columns(
                        pl.when(
                            pl.col("PartyDescription").list.len()
                            != pl.col("Comment").list.len()
                        )
                        .then(
                            pl.col("Parties").str.extract_all(
                                r"(?s)Comment: ([^\n]+?)\s*\n\s*State"
                            )
                        )
                        .otherwise(pl.col("Comment"))
                        .alias("Comment"),
                        pl.when(
                            pl.col("PartyDescription").list.len()
                            != pl.col("IssuedType").list.len()
                        )
                        .then(
                            pl.col("IssuedType").list.head(
                                pl.col("PartyDescription").list.len()
                            )
                        )
                        .otherwise(pl.col("IssuedType"))
                        .alias("IssuedType"),
                        pl.when(
                            pl.col("PartyDescription").list.len()
                            != pl.col("ReissueType").list.len()
                        )
                        .then(
                            pl.col("ReissueType").list.head(
                                pl.col("PartyDescription").list.len()
                            )
                        )
                        .otherwise(pl.col("ReissueType"))
                        .alias("ReissueType"),
                    )
                    .with_columns(
                        pl.when(
                            pl.col("PartyDescription").list.len()
                            != pl.col("Comment").list.len()
                        )
                        .then(
                            pl.col("Parties")
                            .str.extract_all(r"Comment: (.+)")
                            .list.head(pl.col("PartyDescription").list.len())
                        )
                        .otherwise(pl.col("Comment"))
                        .alias("Comment")
                    )
                    .drop("Parties")
                    .explode(
                        "PartyDescription",
                        "AltName",
                        "Name",
                        "Type",
                        "Index",
                        "Party",
                        "Address2",
                        "JID",
                        "Hardship",
                        "DOB",
                        "City",
                        "Race",
                        "SSN",
                        "Country",
                        "Sex",
                        "Zip",
                        "State",
                        "CourtAction",
                        "CourtActionDate",
                        "AmountOfJudgement",
                        "Address1",
                        "Phone",
                        "CourtActionFor",
                        "CostAgainstPartyOtherCost",
                        "ReissueIssued",
                        "IssuedType",
                        "ReissueType",
                        "ReturnReturnType",
                        "Served",
                        "ServiceType",
                        "ServiceOn",
                        "AnswerAnswerType",
                        "NoticeOfNoService",
                        "NoticeOfNoAnswer",
                        "ServedBy",
                        "Comment",
                        "WarrantActionDate",
                        "WarrantActionStatusStatusDescription",
                        "Exemptions",
                        "DateSatisfied",
                        "ArrestDate",
                    )
                    .select(
                        pl.col("CaseNumber"),
                        pl.col("PartyDescription")
                        .str.extract(r"Party (\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("Party#"),
                        pl.col("PartyDescription")
                        .str.replace("Alt Name:", "")
                        .str.replace("DOB:", "")
                        .str.strip_chars(),
                        pl.col("Party").str.extract(r"(.+)Party:").str.strip_chars(),
                        pl.col("Name").str.extract(r"(.+)Name:").str.strip_chars(),
                        pl.col("AltName")
                        .str.extract(r"Alt Name: (.+)")
                        .str.strip_chars(),
                        pl.col("Type").str.extract(r"Type: (.+)").str.strip_chars(),
                        pl.col("Index").str.extract(r"(.+)Index:").str.strip_chars(),
                        pl.col("JID")
                        .str.extract(r"JID: (.+?)Hardship")
                        .str.strip_chars(),
                        pl.col("Hardship")
                        .str.extract(r"Hardship: (.+)")
                        .str.strip_chars(),
                        pl.col("Address1")
                        .str.extract(r"Address 1: (.+)Phone:")
                        .str.strip_chars(),
                        pl.col("Address2")
                        .str.extract(r"Address 2: (.+)")
                        .str.strip_chars(),
                        pl.col("City").str.extract(r"City: (.+)").str.strip_chars(),
                        pl.col("State")
                        .str.extract(r"State: (\w\w) ")
                        .str.strip_chars(),
                        pl.col("Country")
                        .str.extract(r"Country: (.+)")
                        .str.strip_chars(),
                        pl.col("Zip").str.extract(r"Zip: (.+)").str.strip_chars(),
                        pl.col("Phone").str.extract(r"Phone: (.+)").str.strip_chars(),
                        pl.col("SSN").str.extract(r"SSN: (.+)").str.strip_chars(),
                        pl.col("DOB")
                        .str.extract(r"DOB: (.+)")
                        .str.strip_chars()
                        .str.to_date("%m/%d/%Y", strict=False),
                        pl.col("Race").str.extract(r"Race:(.+?)SSN").str.strip_chars(),
                        pl.col("Sex").str.extract(r"Sex: (.+)").str.strip_chars(),
                        pl.col("CourtAction")
                        .str.replace(r"Court Action Date: (\d\d/\d\d/\d\d\d\d)?", "")
                        .str.replace("Court Action:", "")
                        .str.strip_chars(),
                        pl.col("CourtActionDate")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False),
                        pl.col("AmountOfJudgement")
                        .str.extract(r"(\-?\$[\d,]+\.\d\d)")
                        .str.replace(r"\$", "")
                        .str.replace(",", "")
                        .cast(pl.Float64, strict=False),
                        pl.col("CourtActionFor")
                        .str.extract(r"(?s)(.+)\s*\n\s*Warrant Action Date:")
                        .str.replace(r"State.+", "")
                        .str.replace(r"JID.+", "")
                        .str.replace(r"Notice.+", "")
                        .str.replace(r"Comment.+", "")
                        .str.replace(r"\d\d/\d\d/\d\d\d\d", "")
                        .str.strip_chars(),
                        pl.col("CostAgainstPartyOtherCost")
                        .str.extract(
                            r"(\-?\$[\d,]+\.\d+) (\-?\$[\d,]+\.\d+)", group_index=1
                        )
                        .str.replace(r",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                        .alias("OtherCost"),
                        pl.col("CostAgainstPartyOtherCost")
                        .str.extract(
                            r"(\-?\$[\d,]+\.\d+) (\-?\$[\d,]+\.\d+)", group_index=2
                        )
                        .str.replace(",", "")
                        .str.replace(r"\$", "")
                        .cast(pl.Float64, strict=False)
                        .alias("CostAgainstParty"),
                        pl.col("ReissueIssued")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d) \d\d/\d\d/\d\d\d\d")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Reissue"),
                        pl.col("ReissueIssued")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d) Issued:")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Issued"),
                        pl.col("IssuedType")
                        .str.extract(r"(.+) Issued Type:")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.strip_chars(),
                        pl.col("ReissueType")
                        .str.extract(r"Reissue Type: (.+)")
                        .str.strip_chars(),
                        pl.col("ReturnReturnType")
                        .str.extract(r"Return: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Return"),
                        pl.col("ReturnReturnType")
                        .str.extract(r"Return Type: (.+?)Return:")
                        .str.strip_chars()
                        .alias("ReturnType"),
                        pl.col("ReturnReturnType")
                        .str.replace(r"Return:.+?Return Type:", "")
                        .str.extract(r"Return: (.+?)Return Type:")
                        .str.strip_chars()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Return2"),
                        pl.col("ReturnReturnType")
                        .str.replace(r"Return:.+?Return Type:", "")
                        .str.extract(r"Return Type: (.+)")
                        .str.strip_chars()
                        .alias("ReturnType2"),
                        pl.col("Served")
                        .str.extract(r"Served: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False),
                        pl.col("ServiceType")
                        .str.extract(r"Service Type (.+?)Service On")
                        .str.strip_chars(),
                        pl.col("ServiceOn").str.extract(
                            r"Service On: (.+?) Served By:"
                        ),
                        pl.col("AnswerAnswerType")
                        .str.extract(r"Answer: (\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Answer"),
                        pl.col("AnswerAnswerType")
                        .str.extract(r"Answer Type: (.+?) Notice of No Service:")
                        .alias("AnswerType"),
                        pl.col("NoticeOfNoService")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("NoticeOfNoService"),
                        pl.col("NoticeOfNoAnswer")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("NoticeOfNoAnswer"),
                        pl.col("ServedBy")
                        .str.extract(r"Served By: (.+)")
                        .str.strip_chars(),
                        pl.col("Comment")
                        .str.extract(r"Comment: (.+)")
                        .str.strip_chars(),
                        pl.col("WarrantActionDate")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False),
                        pl.col("WarrantActionStatusStatusDescription")
                        .str.extract(r"Warrant Action Status: (.+)")
                        .str.strip_chars()
                        .alias("WarrantActionStatus"),
                        pl.col("WarrantActionStatusStatusDescription")
                        .str.extract(r"Status Description: (.+?)Warrant Action Status:")
                        .alias("StatusDescription"),
                        pl.col("Exemptions")
                        .str.extract(r"Exemptions: (.+)")
                        .str.strip_chars(),
                        pl.col("DateSatisfied")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False),
                        pl.col("ArrestDate")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False),
                    )
                    .select(
                        "CaseNumber",
                        "Party#",
                        "PartyDescription",
                        "Party",
                        "Name",
                        "Type",
                        "Index",
                        "AltName",
                        "Hardship",
                        "JID",
                        "Address1",
                        "Address2",
                        "City",
                        "State",
                        "Country",
                        "Zip",
                        "Phone",
                        "SSN",
                        "DOB",
                        "Sex",
                        "Race",
                        "CourtAction",
                        "CourtActionDate",
                        "AmountOfJudgement",
                        "CourtActionFor",
                        "Exemptions",
                        "CostAgainstParty",
                        "OtherCost",
                        "DateSatisfied",
                        "Comment",
                        "ArrestDate",
                        "WarrantActionDate",
                        "WarrantActionStatus",
                        "StatusDescription",
                        "Issued",
                        "IssuedType",
                        "Reissue",
                        "ReissueType",
                        "Return",
                        "ReturnType",
                        "Return2",
                        "ReturnType2",
                        "Served",
                        "ServiceType",
                        "ServiceOn",
                        "ServedBy",
                        "Answer",
                        "AnswerType",
                        "NoticeOfNoAnswer",
                        "NoticeOfNoService",
                    )
                )
            else:
                columns = [
                    "CaseNumber",
                    "Party#",
                    "PartyDescription",
                    "Party",
                    "Name",
                    "Type",
                    "Index",
                    "AltName",
                    "Hardship",
                    "JID",
                    "Address1",
                    "Address2",
                    "City",
                    "State",
                    "Country",
                    "Zip",
                    "Phone",
                    "SSN",
                    "DOB",
                    "Sex",
                    "Race",
                    "CourtAction",
                    "CourtActionDate",
                    "AmountOfJudgement",
                    "CourtActionFor",
                    "Exemptions",
                    "CostAgainstParty",
                    "OtherCost",
                    "DateSatisfied",
                    "Comment",
                    "ArrestDate",
                    "WarrantActionDate",
                    "WarrantActionStatus",
                    "StatusDescription",
                    "Issued",
                    "IssuedType",
                    "Reissue",
                    "ReissueType",
                    "Return",
                    "ReturnType",
                    "Return2",
                    "ReturnType2",
                    "Served",
                    "ServiceType",
                    "ServiceOn",
                    "ServedBy",
                    "Answer",
                    "AnswerType",
                    "NoticeOfNoAnswer",
                    "NoticeOfNoService",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._parties = df
        return self._parties

    def central_disbursement_division(
        self: "Cases", *, debug: bool = False
    ) -> pl.DataFrame:
        """Make Alabama Central Disbursement Division table."""
        if debug:
            self._central_disbursement_division = None
        if (
            isinstance(self._central_disbursement_division, pl.DataFrame)
            and "Parties" in self._central_disbursement_division.columns
        ):
            self._central_disbursement_division = None
        if isinstance(self._central_disbursement_division, pl.DataFrame):
            return self._central_disbursement_division
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Parsing Alabama Central Disbursement Division tables…"):
            df = self.archive.select(
                pl.col("CaseNumber"),
                pl.col("AllPagesText")
                .str.extract(
                    r"(?s)Alabama Central Disbursement Division(.+?)"
                    r"(Requesting Party|Date:)",
                    group_index=1,
                )
                .str.replace(
                    r"  \n Description From Party To Party Emp Party Reason"
                    r" Disbursement Accoun  \n Transaction Batch  \n Operator  \n ",
                    "",
                )
                .str.replace_all(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                .str.replace(r"\s*\n\s*$", "")
                .alias("ACDD"),
            ).drop_nulls("ACDD")
            if df.shape[0] > 0:
                df = (
                    df.with_columns(
                        pl.col("ACDD").map_elements(
                            lambda x: re.split(r"(\d\d?/\d\d?/\d\d\d\d)", x)
                        )
                    )
                    .with_columns(
                        pl.col("ACDD").map_elements(lambda x: x[::2][1:]).alias("Row"),
                        pl.col("ACDD")
                        .map_elements(lambda x: x[1::2])
                        .alias("TransactionDate"),
                    )
                    .explode("Row", "TransactionDate")
                    .with_columns(
                        pl.col("Row")
                        .str.replace_all("\n", "")
                        .str.replace_all(r"\s+", " ")
                        .str.strip_chars(),
                        pl.col("TransactionDate").str.to_date("%m/%d/%Y", strict=False),
                    )
                    .select(
                        pl.col("CaseNumber"),
                        pl.col("TransactionDate"),
                        pl.col("Row").str.extract(r"(.+?) \$").alias("Description"),
                        pl.col("Row")
                        .str.extract(
                            r"\-?\$([0-9\.,]+) ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)",
                            group_index=5,
                        )
                        .alias("DisbursementAccoun"),
                        pl.col("Row")
                        .str.extract(
                            r"\-?\$([0-9\.,]+) ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)"
                            r" ([^\s]+) ([^\s]+)",
                            group_index=7,
                        )
                        .alias("TransactionBatch"),
                        pl.col("Row")
                        .str.extract(
                            r"\-?\$([0-9\.,]+) ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)"
                            r" ([^\s]+)",
                            group_index=6,
                        )
                        .alias("ReceiptNumber"),
                        pl.col("Row")
                        .str.extract(r"(\-?\$[0-9\.,]+)")
                        .str.replace(r"\$", "")
                        .str.replace(",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("Amount"),
                        pl.col("Row")
                        .str.extract(r"(\-?\$[0-9\.,]+) ([^\s]+)", group_index=2)
                        .alias("FromParty"),
                        pl.col("Row")
                        .str.extract(
                            r"(\-?\$[0-9\.,]+) ([^\s]+) ([^\s]+)", group_index=3
                        )
                        .alias("ToParty"),
                        pl.col("Row")
                        .str.extract(
                            r"(\-?\$[0-9\.,]+) ([^\s]+) ([^\s]+) ([^\s]+)",
                            group_index=4,
                        )
                        .alias("EmpParty"),
                        pl.col("Row")
                        .str.extract(
                            r"(\-?\$[0-9\.,]+) ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)"
                            r" ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)",
                            group_index=9,
                        )
                        .alias("Reason"),
                        pl.col("Row")
                        .str.extract(
                            r"\-?\$([0-9\.,]+) ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)"
                            r" ([^\s]+) ([^\s]+) ([^\s]+)",
                            group_index=8,
                        )
                        .alias("Operator"),
                    )
                )
            else:
                columns = [
                    "CaseNumber",
                    "TransactionDate",
                    "Description",
                    "DisbursementAccoun",
                    "TransactionBatch",
                    "ReceiptNumber",
                    "Amount",
                    "FromParty",
                    "ToParty",
                    "EmpParty",
                    "Reason",
                    "Operator",
                ]
                df = pl.DataFrame()
                for column in columns:
                    df = df.with_columns(pl.Series().alias(column))
        self._central_disbursement_division = df
        return self._central_disbursement_division

    def tables(self: "Cases", *, debug: bool = False) -> dict[str, pl.DataFrame]:
        """Make all tables and return dict."""
        return {
            "cases": self.cases(debug=debug),
            "filing-charges": self.filing_charges(debug=debug),
            "disposition-charges": self.disposition_charges(debug=debug),
            "fees": self.fees(debug=debug),
            "sentences": self.sentences(debug=debug),
            "enforcement": self.enforcement(debug=debug),
            "financial-history": self.financial_history(debug=debug),
            "witnesses": self.witnesses(debug=debug),
            "attorneys": self.attorneys(debug=debug),
            "settings": self.settings(debug=debug),
            "restitution": self.restitution(debug=debug),
            "linked-cases": self.linked_cases(debug=debug),
            "continuances": self.continuances(debug=debug),
            "case-action-summary": self.case_action_summary(debug=debug),
            "images": self.images(debug=debug),
            "parties": self.parties(debug=debug),
            "central_disbursement_division": self.central_disbursement_division(
                debug=debug
            ),
        }

    def summary(self: "Cases", pairs: str | Path | pl.DataFrame) -> pl.DataFrame:
        """
        Summarize charges and fees by impact on voting rights using a filled pairs
        template.
        """
        if isinstance(pairs, str):
            pairs = Path(pairs).resolve()
        if isinstance(pairs, Path):
            pairs = cast(pl.DataFrame, read(pairs))
        pairs = cast(pl.DataFrame, pairs)

        # People with no cases found are filtered out here, and added at the end.
        zero_cases = pairs.filter(pl.col("CaseCount") == 0)
        pairs = pairs.filter(pl.col("CaseCount") > 0)

        if not self.is_read:
            self.read()

        cases = self.cases()
        dch = self.disposition_charges()
        fch = self.filing_charges()

        with console.status("Creating summary…"):
            cases = cases.select(
                "CaseNumber", "Name", "DOB", "Race", "Sex"
            ).with_columns(
                pl.col("Race").cast(pl.Utf8, strict=False),
                pl.col("Sex").cast(pl.Utf8, strict=False),
            )
            fch = (
                fch.join(pairs, on="Name", how="outer")
                .group_by("AIS / Unique ID")
                .all()
                .select(
                    pl.col("AIS / Unique ID"),
                    pl.col("CERVCharge")
                    .list.count_match(element=True)
                    .alias("CERVChargesCount"),
                    pl.col("PardonToVoteCharge")
                    .list.count_match(element=True)
                    .alias("PardonToVoteChargesCount"),
                    pl.col("PermanentCharge")
                    .list.count_match(element=True)
                    .alias("PermanentChargesCount"),
                    pl.col("ChargesSummary")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip_chars()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("FilingCharges"),
                )
            )
            conv = (
                dch.filter("Conviction")
                .join(pairs, on="Name", how="outer")
                .group_by("AIS / Unique ID")
                .all()
                .select(
                    pl.col("AIS / Unique ID"),
                    pl.col("Conviction")
                    .list.count_match(element=True)
                    .alias("ConvictionCount"),
                    pl.col("CERVConviction")
                    .list.count_match(element=True)
                    .alias("CERVConvictionCount"),
                    pl.col("PardonToVoteConviction")
                    .list.count_match(element=True)
                    .alias("PardonToVoteConvictionCount"),
                    pl.col("PermanentConviction")
                    .list.count_match(element=True)
                    .alias("PermanentConvictionCount"),
                    pl.col("PaymentToRestore"),
                    pl.col("ChargesSummary")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip_chars()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("Convictions"),
                )
                .with_columns(
                    pl.when(
                        pl.col("CERVConvictionCount").gt(0)
                        & pl.col("PardonToVoteConvictionCount").eq(0)
                        & pl.col("PermanentConvictionCount").eq(0)
                    )
                    .then(pl.col("PaymentToRestore").list.sum())
                    .otherwise(None)
                    .alias("PaymentToRestore")
                )
            )
            vrr = (
                dch.filter(
                    pl.col("CERVConviction")
                    | pl.col("PardonToVoteConviction")
                    | pl.col("PermanentConviction")
                )
                .join(pairs, on="Name", how="outer")
                .group_by("AIS / Unique ID")
                .all()
                .select(
                    pl.col("AIS / Unique ID"),
                    pl.col("ChargesSummary")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip_chars()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("DisqualifyingConvictions"),
                )
            )
            cases = (
                cases.join(pairs, on="Name", how="outer")
                .group_by("AIS / Unique ID")
                .all()
                .join(fch, on="AIS / Unique ID", how="left")
                .join(conv, on="AIS / Unique ID", how="left")
                .join(vrr, on="AIS / Unique ID", how="left")
                .with_columns(
                    pl.col("CaseNumber").list.len().alias("CaseCount"),
                    pl.col("CaseNumber")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip_chars()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("Cases"),
                )
                .with_columns(
                    pl.when(
                        pl.col("CERVConvictionCount").eq(0)
                        & pl.col("PardonToVoteConvictionCount").eq(0)
                        & pl.col("PermanentConvictionCount").eq(0)
                        & pl.col("Cases").str.lengths().gt(0)
                    )
                    .then(statement=True)
                    .otherwise(statement=False)
                    .alias("EligibleToVote"),
                    pl.when(
                        pl.col("CERVConvictionCount").gt(0)
                        & pl.col("PardonToVoteConvictionCount").eq(0)
                        & pl.col("PermanentConvictionCount").eq(0)
                    )
                    .then(statement=True)
                    .otherwise(statement=False)
                    .alias("NeedsCERV"),
                    pl.when(
                        pl.col("PardonToVoteConvictionCount").gt(0)
                        & pl.col("PermanentConvictionCount").eq(0)
                    )
                    .then(statement=True)
                    .otherwise(statement=False)
                    .alias("NeedsPardon"),
                    pl.when(pl.col("PermanentConvictionCount").gt(0))
                    .then(statement=True)
                    .otherwise(statement=False)
                    .alias("PermanentlyDisqualified"),
                )
                .with_columns(
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("EligibleToVote"))
                    .alias("EligibleToVote"),
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("NeedsCERV"))
                    .alias("NeedsCERV"),
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("NeedsPardon"))
                    .alias("NeedsPardon"),
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("PermanentlyDisqualified"))
                    .alias("PermanentlyDisqualified"),
                )
                .select(
                    pl.col("AIS / Unique ID"),
                    pl.col("Name").list.first(),
                    pl.col("DOB").list.first(),
                    pl.col("Race").list.first(),
                    pl.col("Sex").list.first(),
                    pl.col("PaymentToRestore"),
                    pl.col("EligibleToVote"),
                    pl.col("NeedsCERV"),
                    pl.col("NeedsPardon"),
                    pl.col("PermanentlyDisqualified"),
                    pl.col("ConvictionCount"),
                    pl.col("CERVChargesCount"),
                    pl.col("CERVConvictionCount"),
                    pl.col("PardonToVoteChargesCount"),
                    pl.col("PardonToVoteConvictionCount"),
                    pl.col("PermanentChargesCount"),
                    pl.col("PermanentConvictionCount"),
                    pl.col("CaseCount"),
                    pl.col("DisqualifyingConvictions"),
                    pl.col("Convictions"),
                    pl.col("FilingCharges"),
                    pl.col("Cases"),
                )
                .sort("Name")
            )
            if len(zero_cases) > 0:
                zero_cases = zero_cases.select(
                    "AIS / Unique ID", "Name", pl.col("CaseCount").cast(pl.UInt32)
                )
                for column in cases.columns:
                    if column not in zero_cases.columns:
                        zero_cases = zero_cases.with_columns(pl.lit(None).alias(column))
                zero_cases = zero_cases.select(
                    "AIS / Unique ID",
                    "Name",
                    "DOB",
                    "Race",
                    "Sex",
                    "PaymentToRestore",
                    "EligibleToVote",
                    "NeedsCERV",
                    "NeedsPardon",
                    "PermanentlyDisqualified",
                    "ConvictionCount",
                    "CERVChargesCount",
                    "CERVConvictionCount",
                    "PardonToVoteChargesCount",
                    "PardonToVoteConvictionCount",
                    "PermanentChargesCount",
                    "PermanentConvictionCount",
                    "CaseCount",
                    "DisqualifyingConvictions",
                    "Convictions",
                    "FilingCharges",
                    "Cases",
                )
                cases = pl.concat((cases, zero_cases))

        if "Search" in pairs.columns:
            cases = (
                cases.join(
                    pairs.select("AIS / Unique ID", "Search").unique("AIS / Unique ID"),
                    on="AIS / Unique ID",
                    how="left",
                )
                .with_columns(
                    pl.when(pl.col("Search").is_not_null() & pl.col("Search").ne(""))
                    .then(pl.col("Search"))
                    .otherwise(pl.col("Name"))
                    .alias("Name")
                )
                .drop("Search")
            )

        self._summary = cases
        self._pairs = pairs
        return self._summary

    def pairs_template(self: "Cases") -> pl.DataFrame:
        """Create empty pairs template for summary() pairs parameter."""
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        with console.status("Creating template…"):
            names = (
                self.archive.with_columns(
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                        group_index=1,
                    )
                    .str.replace("Case Number:", "", literal=True)
                    .str.replace(r"C$", "")
                    .str.strip_chars()
                    .alias("Name"),
                    pl.col("AllPagesText")
                    .str.extract(r"(\d{2}/\d{2}/\d{4})(?:.{0,5}DOB:)", group_index=1)
                    .str.replace_all(r"[^\d/]", "")
                    .str.strip_chars()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("DOB"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)(SSN:)(.{0,100})(Alias 1)", group_index=2)
                    .str.strip_chars()
                    .alias("Alias"),
                )
                .group_by("Name")
                .agg("CaseNumber", "Alias", "DOB")
                .select(
                    pl.lit("").alias("AIS / Unique ID"),
                    pl.col("Name"),
                    pl.col("Alias").list.get(0),
                    pl.col("DOB").list.get(0),
                    pl.col("CaseNumber").list.len().alias("CaseCount"),
                    pl.col("CaseNumber").list.join(", ").alias("Cases"),
                )
                .sort("Name")
            )
        self._pairs_template = names
        return self._pairs_template

    def autopair(
        self: "Cases",
        party_search_results: pl.DataFrame,
        unique_id_map: pl.DataFrame | None = None,
        unique_id_column: str | None = None,
    ) -> pl.DataFrame:
        """
        Fill pairs template using party search results. If `party_search_queue` and
        `unique_id_column` are not provided, sequential integers will be used to
        populate the "AIS / Unique ID" column.
        """
        if unique_id_map is not None:
            if unique_id_column is None:
                for column in unique_id_map.columns:
                    if column in ("AIS / Unique ID", "AIS", "Unique ID"):
                        unique_id_column = column
                        break
                if unique_id_column is None:
                    msg = "Must specify Unique ID column."
                    raise ValueError(msg)
            unique_id_map = unique_id_map.select(
                "Name", pl.col(unique_id_column).alias("AIS / Unique ID")
            ).rename({"Name": "Search"})
        else:
            unique_id_map = (
                party_search_results.select("Search")
                .unique("Search")
                .with_row_count("AIS / Unique ID")
            )

        cases = (
            self.cases()
            .select("Name", "DOB", "CaseNumber")
            .join(party_search_results, on="CaseNumber")
        )

        pairs = (
            cases.join(unique_id_map, on="Search")
            .group_by("Name", "DOB")
            .all()
            .select(
                pl.col("AIS / Unique ID").list.first(),
                pl.col("Name"),
                pl.col("DOB"),
                pl.col("CaseNumber").list.len().alias("CaseCount"),
                pl.col("Search").list.first(),
                pl.col("CaseNumber").list.join(", ").alias("Cases"),
            )
            .sort("Name")
        )

        pairs = pl.concat(
            [
                pairs,
                unique_id_map.join(cases, how="anti", on="Search").select(
                    pl.col("AIS / Unique ID"),
                    pl.col("Search").alias("Name"),
                    pl.lit(None, dtype=pl.Date).alias("DOB"),
                    pl.lit(0, dtype=pl.UInt32).alias("CaseCount"),
                    pl.col("Search"),
                    pl.lit(None, dtype=pl.Utf8).alias("Cases"),
                ),
            ]
        )

        return pairs

    def write_tables(self: "Cases", path: str | Path) -> dict[str, pl.DataFrame]:
        """
        Write all made tables to output path. If multiple tables, file
        extension must be .xlsx. Otherwise, .csv, .parquet, and .json
        are also supported.
        """
        all_tables = {
            "cases": self._cases,
            "filing-charges": self._filing_charges,
            "disposition-charges": self._disposition_charges,
            "fees": self._fees,
            "sentences": self._sentences,
            "enforcement": self._enforcement,
            "financial-history": self._financial_history,
            "witnesses": self._witnesses,
            "attorneys": self._attorneys,
            "settings": self._settings,
            "restitution": self._restitution,
            "linked-cases": self._linked_cases,
            "continuances": self._continuances,
            "case-action-summary": self._case_action_summary,
            "images": self._images,
            "parties": self._parties,
            "central-disbursement-division": self._central_disbursement_division,
        }
        only_df_vars = {}
        for x in all_tables:
            if isinstance(all_tables[x], pl.DataFrame):
                only_df_vars.update({x: all_tables[x]})
        output_dict = cast(dict[str, pl.DataFrame], only_df_vars)
        write(output_dict, path, log=True)
        return output_dict

    def write_archive(self: "Cases", path: str | Path) -> pl.DataFrame:
        """
        Write case archive to output path. Supports .xlsx, .parquet,
        and .csv. Parquet export recommended.
        """
        if not self.is_read:
            self.read()
        assert isinstance(self.archive, pl.DataFrame)
        columns = [
            column
            for column in ["CaseNumber", "Path", "Timestamp", "AllPagesText"]
            if column in self.archive.columns
        ]
        out = self.archive.select(columns)
        write({"archive": out}, path, log=True)
        return out

    def write_summary_docs(
        self: "Cases",
        pairs: str | Path | pl.DataFrame,
        output_dir: str | Path,
        template_path: str | Path | None = None,
        *,
        include_ais: bool = False,
        include_dob: bool = True,
        include_race_sex: bool = True,
    ) -> None:
        """
        Create a docx summary in `output_dir` for each unique
        identifier in `pairs`.
        """
        # Read pairs and check paths.
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)
        output_dir = output_dir.resolve()
        if not isinstance(pairs, pl.DataFrame):
            pairs = read(pairs)  # type: ignore
        assert isinstance(pairs, pl.DataFrame)
        if not output_dir.is_dir():
            output_dir.mkdir()
        if (
            "AIS / Unique ID" not in pairs.columns
            or "Name" not in pairs.columns
            or "DOB" not in pairs.columns
            or "Cases" not in pairs.columns
        ):
            msg = "Pairs table missing one or more columns: AIS / Unique ID, Name, DOB."
            raise BadFileError(msg)

        # Group pairs by UID.
        pairs = (
            pairs.group_by("AIS / Unique ID")
            .all()
            .with_columns(
                pl.col("Name").list.first(),
                pl.col("DOB").list.first(),
                pl.col("Cases").list.join(", "),
            )
        )

        self.cases()
        self.disposition_charges()
        assert self._cases is not None
        assert self._disposition_charges is not None

        if template_path is None:
            doc = DocxTemplate(f"{Path(__file__).parent}/template.docx")
        else:
            doc = DocxTemplate(template_path)

        locale.setlocale(locale.LC_ALL, "")  # set locale for number formatting
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as bar:
            for pair in bar.track(
                pairs.iter_rows(named=True),
                total=pairs.shape[0],
                description="Writing…",
            ):
                name = pair["Name"]
                case_nums = pair["Cases"].split(", ")

                if include_ais:
                    ais = str(pair["AIS / Unique ID"])
                    ais_label = "AIS #"
                else:
                    ais = ""
                    ais_label = ""

                cases = self._cases.filter(pl.col("CaseNumber").is_in(case_nums))
                charges = self._disposition_charges.filter(
                    pl.col("CaseNumber").is_in(case_nums)
                )

                if include_race_sex:
                    sex_label = "SEX"
                    try:
                        sex = cases.filter(pl.col("Sex").is_not_null())[0, "Sex"]
                    except IndexError:
                        sex = ""
                    race_label = "RACE"
                    try:
                        race = cases.filter(pl.col("Race").is_not_null())[0, "Race"]
                    except IndexError:
                        race = ""
                else:
                    sex_label = ""
                    sex = ""
                    race_label = ""
                    race = ""

                if include_dob:
                    try:
                        dob = cases.filter(pl.col("DOB").is_not_null())[
                            0, "DOB"
                        ].strftime("%Y-%m-%d")
                    except IndexError:
                        dob = ""
                    dob_label = "DOB"
                else:
                    dob = ""
                    dob_label = ""

                needs_cerv = str(charges["CERVConviction"].any()).upper()
                needs_pardon = str(charges["PardonToVoteConviction"].any()).upper()
                permanently_disqualified = str(
                    charges["PermanentConviction"].any()
                ).upper()
                balance = "$" + locale.format_string(
                    "%.2f", cases["TotalBalance"].sum(), grouping=True
                )
                payment_to_restore = "$" + locale.format_string(
                    "%.2f",
                    (
                        charges.filter(pl.col("CERVConviction"))
                        .unique("CaseNumber")["PaymentToRestore"]
                        .sum()
                    ),
                    grouping=True,
                )
                conviction_ct = str(charges.filter("Conviction").shape[0])
                disq_conv_ct = str(
                    charges.filter(
                        pl.col("CERVConviction") | pl.col("PardonToVoteConviction")
                    ).shape[0]
                )
                case_ct = str(cases.shape[0])
                table = (
                    charges.group_by("CaseNumber")
                    .agg(
                        pl.col("TotalBalance").first(),
                        pl.col("ChargesSummary"),
                        pl.col("CERVConviction").any(),
                        pl.col("PardonToVoteConviction").any(),
                        pl.col("PermanentConviction").any(),
                        pl.col("Conviction").any(),
                        pl.col("Felony").any(),
                    )
                    .with_columns(
                        pl.col("TotalBalance")
                        .map_elements(
                            lambda x: "$"
                            + locale.format_string("%.2f", x, grouping=True),
                            return_dtype=pl.Utf8,
                        )
                        .alias("Balance"),
                        pl.col("ChargesSummary")
                        .list.join("\n")
                        .str.replace_all(
                            r"(\d\d-\w\w-\d\d\d\d-\d\d\d\d\d\d\.\d\d - )", ""
                        )
                        .alias("Charges"),
                    )
                    .fill_null("")
                    .with_columns(
                        pl.when(
                            pl.col("CERVConviction")
                            | pl.col("PardonToVoteConviction")
                            | pl.col("PermanentConviction")
                        )
                        .then(pl.concat_str([pl.lit("*"), pl.col("CaseNumber")]))
                        .otherwise(pl.col("CaseNumber"))
                        .alias("CaseNumber"),
                        pl.when(pl.col("Balance").str.contains(r"\.\d$"))
                        .then(pl.concat_str(pl.col("Balance"), pl.lit("0")))
                        .otherwise(pl.col("Balance"))
                        .alias("Balance"),
                    )
                    .sort("Felony", descending=True)
                    .sort("Conviction", descending=True)
                    .sort("CERVConviction", descending=True)
                    .sort("PardonToVoteConviction", descending=True)
                    .sort("PermanentConviction", descending=True)
                    .select(
                        pl.exclude(
                            "Conviction",
                            "CERVConviction",
                            "PardonToVoteConviction",
                            "PermanentConviction",
                            "ChargesSummary",
                            "TotalBalance",
                        )
                    )
                    .to_dicts()
                )
                context = {
                    "name": name,
                    "sexlabel": sex_label,
                    "sex": sex,
                    "racelabel": race_label,
                    "race": race,
                    "dob": dob,
                    "doblabel": dob_label,
                    "aislabel": ais_label,
                    "ais": ais,
                    "cerv": needs_cerv,
                    "pard": needs_pardon,
                    "perm": permanently_disqualified,
                    "balance": balance,
                    "ptr": payment_to_restore,
                    "tot_conv": conviction_ct,
                    "tot_disq_conv": disq_conv_ct,
                    "tot_cases": case_ct,
                    "table": table,
                }
                doc.render(context)
                doc.save(f"{output_dir}/{name}.docx")


class Case(Cases):
    """From a case PDF path, create, manipulate, and export data tables."""

    def __init__(self: "Case", path: Path | str) -> None:
        """Create a Case object."""
        if isinstance(path, str):
            path = Path(path)
        path = path.resolve()
        if path.suffix != ".pdf":
            msg = "File at path must be a case PDF."
            raise BadFileError(msg)
        Cases.__init__(self, path)
        return None


# ┬┌┐┌┌┬┐┌─┐┬─┐┌─┐┌─┐┌─┐┌─┐┌─┐
# ││││ │ ├┤ ├┬┘├┤ ├─┤│  ├┤ └─┐
# ┴┘└┘ ┴ └─┘┴└─└  ┴ ┴└─┘└─┘└─┘
# Invoke CLI with `alacorder` or `python -m alacorder`.
# Invoke TUI with `alacorder launch`.


class AlacorderApp(App):
    """Textual user interface."""

    TITLE = "Alacorder"
    try:
        CSS_PATH: ClassVar[str] = f"{Path(__file__).parent}/tui.tcss"
    except NameError:
        CSS_PATH = "tui.tcss"
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+q", "quit_app", "Quit")
    ]

    def compose(self: "AlacorderApp") -> ComposeResult:
        """Generate initial app widgets."""
        yield Header()
        yield Footer()
        with TabbedContent(
            "Scrape Alacourt",
            "Scrape ADOC",
            "Make Tables",
            "Archive Tools",
            "Pairing Tools",
            "About",
        ):
            with ScrollableContainer(id="scrape-alacourt-container"):
                yield Static(
                    "Scrape party search results or case PDFs from Alacourt.",
                    classes="header",
                )
                yield Static(
                    "[bold]Queue Path:[/bold] [gray](path to table with Name or Case"
                    " Number column)[/gray]"
                )
                yield Input(
                    placeholder="File must be .xlsx, .csv, .json, or .parquet",
                    classes="input",
                    id="scrape-alacourt-queue",
                )
                yield Static(
                    "[bold]Output Path:[/bold] [gray](path to output table or case"
                    " directory)[/gray]"
                )
                yield Input(
                    placeholder="Path to directory or file with supported extension",
                    classes="input",
                    id="scrape-alacourt-output",
                )
                with Horizontal():
                    with RadioSet(classes="input", id="scrape-alacourt-radioset"):
                        yield RadioButton(
                            "Collect case numbers from name list.",
                            classes="input",
                            id="party-search-radio",
                        )
                        yield RadioButton(
                            "Collect case PDFs from case number list.",
                            classes="input",
                            id="fetch-cases-radio",
                        )
                    yield Checkbox(
                        "Show Browser", id="alacourt-show-browser", classes="input"
                    )
                with Horizontal(id="party-search-options"):
                    yield Checkbox(
                        "Only search criminal cases",
                        id="criminal-only",
                        classes="input",
                    )
                with Horizontal(id="fetch-cases-options"):
                    yield Checkbox("Verify case downloads", id="verify", value=True)
                    yield Checkbox("Pre-verify case downloads", id="pre-verify")
                yield Static("[bold]Alacourt Credentials:[/bold]")
                with Horizontal(id="login-container"):
                    yield Input(
                        placeholder="Customer ID",
                        classes="login-input input",
                        id="customer-id",
                    )
                    yield Input(
                        placeholder="User ID", classes="login-input input", id="user-id"
                    )
                    yield Input(
                        placeholder="Password",
                        classes="login-input input",
                        password=True,
                        id="password",
                    )
                yield Button("Start", id="start-alacourt", classes="input start")
            with ScrollableContainer(id="scrape-adoc-container"):
                yield Static("Scrape the ADOC website's inmate list.", classes="header")
                with Horizontal():
                    with RadioSet(id="adoc-radioset"):
                        yield RadioButton(
                            "Collect all inmates from ADOC Inmate Search.",
                            id="crawl-adoc-radio",
                        )
                        yield RadioButton(
                            "Collect inmate details from list of names.",
                            id="search-adoc-radio",
                        )
                    yield Checkbox("Show Browser", id="adoc-show-browser")
                with Container(id="hidden-adoc-search"):
                    yield Static("Queue Path:")
                    yield Input(
                        placeholder="File must be .xlsx, .csv, .json, or .parquet",
                        id="adoc-queue-path",
                        classes="input",
                    )
                yield Static("Output Path:")
                yield Input(
                    placeholder="File must be .xlsx, .csv, .json, or .parquet",
                    id="adoc-output-path",
                    classes="input",
                )
                yield Button("Start", id="start-adoc", classes="input start")
            with ScrollableContainer(id="make-tables-container"):
                yield Static(
                    "Make data tables from a case directory or archive.",
                    classes="header",
                )
                yield Static("Input Path:")
                yield Input(
                    placeholder=(
                        "Directory with PDF cases or case archive (.xlsx, .csv, .json,"
                        " .parquet)"
                    ),
                    id="tables-input-path",
                    classes="input",
                )
                yield Static("Output Path:")
                yield Input(
                    placeholder="File must be .xlsx, .csv, .json, or .parquet",
                    id="tables-output-path",
                    classes="input",
                )
                yield SelectWidget(
                    [
                        ("All Tables", "all"),
                        ("Case Information", "cases"),
                        ("Filing Charges", "filing-charges"),
                        ("Disposition Charges", "disposition-charges"),
                        ("Fees", "fees"),
                        ("Attorneys", "attorneys"),
                        ("Case Action Summary", "case-action-summary"),
                        ("Financial History", "financial-history"),
                        ("Images", "images"),
                        ("Sentences", "sentences"),
                        ("Enforcement", "enforcement"),
                        ("Settings", "settings"),
                        ("Witnesses", "witnesses"),
                        ("Restitution", "restitution"),
                        ("Linked Cases", "linked-cases"),
                        ("Continuances", "continuances"),
                        ("Parties", "parties"),
                        (
                            "Central Disbursement Division",
                            "central-disbursement-division",
                        ),
                    ],
                    id="tables-select",
                    prompt="Select a table export option.",
                )
                yield Button("Start", id="start-tables", classes="input start")
            with ScrollableContainer(id="archive-tools-container"):
                yield Static(
                    "Manage and archive directories of PDF cases.", classes="header"
                )
                with RadioSet(id="archive-tools-radioset"):
                    yield RadioButton(
                        "Create a case text archive from a directory of PDF cases.",
                        id="make-archive-radio",
                    )
                    yield RadioButton(
                        "Rename all cases in a directory to [u]CaseNumber.pdf[/u] and"
                        " remove duplicates.",
                        id="rename-cases-radio",
                    )
                with Container():
                    yield Static("Directory Path:")
                    yield Input(
                        placeholder="Path to directory with PDF cases",
                        id="archive-tools-directory-path",
                        classes="input",
                    )
                with Container(id="archive-tools-output-container"):
                    yield Static("Output Path:")
                    yield Input(
                        placeholder=(
                            "Output file path (.xlsx, .csv, .json, or .parquet)"
                        ),
                        id="archive-tools-output-path",
                        classes="input",
                    )
                yield Button("Start", id="start-archive-tools", classes="input start")
            with ScrollableContainer(id="pairing-tools-container"):
                yield Static(
                    "Use pairing tables to summarize case information.",
                    classes="header",
                )
                with RadioSet(id="pairing-tools-radioset", classes="input"):
                    yield RadioButton(
                        "Automatically fill pairing template with party search"
                        " results.",
                        id="autopair-radio",
                    )
                    yield RadioButton(
                        "Create blank pairing template.", id="make-template-radio"
                    )
                    yield RadioButton(
                        "Create a voting rights summary spreadsheet from pairs and case"
                        " archive.",
                        id="make-summary-radio",
                    )
                    yield RadioButton(
                        "Create document summaries from a template.",
                        id="make-documents-radio",
                    )
                    yield RadioButton(
                        "Automatically filter party search results by matching DOBs to"
                        " inmate list.",
                        id="autofilter-radio",
                    )
                with Container(id="pairing-tools-input-container"):
                    yield Static("Input Path:")
                    yield Input(
                        placeholder="Path to case directory or archive",
                        id="pairing-tools-input-path",
                        classes="input",
                    )
                with Container(id="pairing-tools-inmates-container", classes="hidden"):
                    yield Static("ADOC Inmates List Path:")
                    yield Input(
                        placeholder="Path to ADOC Inmate Search results file",
                        id="pairing-tools-inmates-path",
                        classes="input",
                    )
                with Container(id="pairing-tools-psq-container", classes="hidden"):
                    yield Static("Party Search Queue Path (optional):")
                    yield Input(
                        placeholder=(
                            "Path to party search queue (.xlsx, .csv, .json,"
                            " .parquet)"
                        ),
                        id="pairing-tools-psq-path",
                        classes="input",
                    )
                with Container(id="pairing-tools-psr-container", classes="hidden"):
                    yield Static("Party Search Results Path:")
                    yield Input(
                        placeholder=(
                            "Path to party search results (.xlsx, .csv, .json,"
                            " .parquet)"
                        ),
                        id="pairing-tools-psr-path",
                        classes="input",
                    )
                with Container(id="pairing-tools-pairs-container", classes="hidden"):
                    yield Static("Pairs Path:")
                    yield Input(
                        placeholder=(
                            "Path to pairs template file (.xlsx, .csv, .json, .parquet)"
                        ),
                        id="pairing-tools-pairs-path",
                        classes="input",
                    )
                yield Static("Output Path:")
                yield Input(
                    placeholder="Path to output file or directory",
                    id="pairing-tools-output-path",
                    classes="input",
                )
                with Horizontal(id="template-options", classes="hidden"):
                    with RadioSet(id="template-radioset", classes="input"):
                        yield RadioButton(
                            "Use the default template.", id="default-template-radio"
                        )
                        yield RadioButton(
                            "Use a custom template.",
                            id="custom-template-radio",
                        )
                    yield SelectionList(
                        ("AIS #", "include-ais"),
                        ("DOB", "include-dob"),
                        ("Race/Sex", "include-race-sex"),
                        id="make-documents-field-select",
                        classes="input",
                    )
                with Container(id="custom-template-container", classes="hidden"):
                    yield Static("Custom Template Path:")
                    yield Input(
                        placeholder="Path to .docx template",
                        id="pairing-tools-custom-template-path",
                    )
                yield Button("Start", id="start-pairing-tools", classes="input start")
            with ScrollableContainer(id="about-container"):
                yield Static(
                    "[bright_red]┏┓[/bright_red][orange3]┓ [/orange3]"
                    "[bright_yellow]┏┓[/bright_yellow][green]┏┓[/green]"
                    "[deep_sky_blue1]┏┓[/deep_sky_blue1][green]┳┓[/green]"
                    "[bright_yellow]┳┓[/bright_yellow][orange3]┏┓[/orange3]"
                    "[bright_red]┳┓[/bright_red]\n"
                    "[bright_red]┣┫[/bright_red][orange3]┃ [/orange3]"
                    "[bright_yellow]┣┫[/bright_yellow][green]┃ [/green]"
                    "[deep_sky_blue1]┃┃[/deep_sky_blue1][green]┣┫[/green]"
                    "[bright_yellow]┃┃[/bright_yellow][orange3]┣ [/orange3]"
                    "[bright_red]┣┫[/bright_red]\n"
                    "[bright_red]┛┗[/bright_red][orange3]┗┛[/orange3]"
                    "[bright_yellow]┛┗[/bright_yellow][green]┗┛[/green]"
                    "[deep_sky_blue1]┗┛[/deep_sky_blue1][green]┛┗[/green]"
                    "[bright_yellow]┻┛[/bright_yellow][orange3]┗┛[/orange3]"
                    "[bright_red]┛┗[/bright_red]\n"
                    f"[bold][bright_white]Alacorder {__version__}[/bold]\n"
                    "©2023 Sam Robson[/bright_white]",
                    id="version",
                )

    def on_mount(self: "AlacorderApp") -> None:
        """Run after composing elements to finish initializing application."""
        self.query_one(
            "#make-documents-field-select", expect_type=SelectionList
        ).border_title = "Include selected fields:"
        self.query_one(
            "#template-radioset", expect_type=RadioSet
        ).border_title = "Microsoft Word Templates"

    def on_button_pressed(self: "AlacorderApp", event: Button.Pressed) -> None:
        """Handle button press."""
        match event.button.id:
            case "start-alacourt":
                queue_path: Path | None = Path(
                    self.query_one("#scrape-alacourt-queue", expect_type=Input).value
                )
                output_path: Path | None = Path(
                    self.query_one("#scrape-alacourt-output", expect_type=Input).value
                )
                party_search = self.query_one(
                    "#party-search-radio", expect_type=RadioButton
                ).value
                fetch_cases = self.query_one(
                    "#fetch-cases-radio", expect_type=RadioButton
                ).value
                show_browser = self.query_one(
                    "#alacourt-show-browser", expect_type=Checkbox
                ).value
                customer_id = self.query_one("#customer-id", expect_type=Input).value
                user_id = self.query_one("#user-id", expect_type=Input).value
                password = (self.query_one("#password", expect_type=Input).value,)
                criminal_only = (
                    self.query_one("#criminal-only", expect_type=Checkbox).value,
                )
                verify = self.query_one("#verify", expect_type=Checkbox).value
                pre_verify = self.query_one("#pre-verify", expect_type=Checkbox).value

                config = {
                    "queue-path": queue_path,
                    "output-path": output_path,
                    "party-search": party_search,
                    "fetch-cases": fetch_cases,
                    "show-browser": show_browser,
                    "customer-id": customer_id,
                    "user-id": user_id,
                    "password": password,
                    "criminal-only": criminal_only,
                    "verify": verify,
                    "pre-verify": pre_verify,
                }

                pass_validation = True

                # Queue path checks
                if queue_path is None:
                    self.notify(
                        "Queue Path cannot be left blank.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-queue", expect_type=Input
                    ).add_class("error")
                elif not queue_path.is_file():
                    self.notify(
                        "Could not locate file at Queue Path.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-queue", expect_type=Input
                    ).add_class("error")
                elif queue_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "Queue Path file extension must be .xlsx, .csv, .json, or"
                        " .parquet.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-queue", expect_type=Input
                    ).add_class("error")
                else:
                    self.query_one(
                        "#scrape-alacourt-queue", expect_type=Input
                    ).remove_class("error")

                # Output path checks
                if output_path is None:
                    self.notify(
                        "Output Path field cannot be left blank.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-output", expect_type=Input
                    ).add_class("error")
                elif party_search and (
                    output_path.is_dir()
                    or output_path not in (".xlsx", ".csv", ".json", ".parquet")
                ):
                    self.notify(
                        "Output Path must be file with .xlsx, .csv, .json, or .parquet"
                        " extension.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-output", expect_type=Input
                    ).add_class("error")
                elif fetch_cases and not output_path.is_dir():
                    self.notify(
                        "Output Path must be valid directory.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-output", expect_type=Input
                    ).add_class("error")
                else:
                    self.query_one(
                        "#scrape-alacourt-output", expect_type=Input
                    ).remove_class("error")

                # Radio button check
                if not fetch_cases and not party_search:
                    self.notify(
                        "Collection mode must be selected.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one(
                        "#scrape-alacourt-radioset", expect_type=RadioSet
                    ).add_class("error")
                else:
                    self.query_one(
                        "#scrape-alacourt-radioset", expect_type=RadioSet
                    ).remove_class("error")

                # Credential checks
                if not customer_id.isnumeric() or customer_id == "":
                    self.notify(
                        "Customer ID must be a valid number.",
                        title="Error",
                        severity="error",
                    )
                    pass_validation = False
                    self.query_one("#customer-id", expect_type=Input).add_class("error")
                else:
                    self.query_one("#customer-id", expect_type=Input).remove_class(
                        "error"
                    )
                if user_id == "":
                    self.notify("User ID left blank.", title="Error", severity="error")
                    pass_validation = False
                    self.query_one("#user-id", expect_type=Input).add_class("error")
                else:
                    self.query_one("#user-id", expect_type=Input).remove_class("error")
                if password == "":
                    self.notify("Password left blank.", title="Error", severity="error")
                    pass_validation = False
                    self.query_one("#password", expect_type=Input).add_class("error")
                else:
                    self.query_one("#password", expect_type=Input).remove_class("error")

                if pass_validation:
                    thread = Thread(
                        target=self.start_alacourt_driver,
                        name="scrape-alacourt-thread",
                        args=[config],
                    )
                    thread.start()
                    self.exit()
            case "start-adoc":
                queue_path = Path(
                    self.query_one("#adoc-queue-path", expect_type=Input).value
                ).resolve()
                output_path = Path(
                    self.query_one("#adoc-output-path", expect_type=Input).value
                ).resolve()
                crawl_adoc = self.query_one(
                    "#crawl-adoc-radio", expect_type=RadioButton
                ).value
                search_adoc = self.query_one(
                    "#search-adoc-radio", expect_type=RadioButton
                ).value
                show_browser = self.query_one(
                    "#adoc-show-browser", expect_type=Checkbox
                ).value

                config = {
                    "queue-path": queue_path,
                    "output-path": output_path,
                    "crawl-adoc": crawl_adoc,
                    "search-adoc": search_adoc,
                    "show-browser": show_browser,
                }

                pass_validation = True

                # radio button check
                if not search_adoc and not crawl_adoc:
                    self.notify(
                        "Must select collection mode.", title="Error", severity="error"
                    )
                    self.query_one("#adoc-radioset", expect_type=RadioSet).add_class(
                        "error"
                    )
                    pass_validation = False
                else:
                    self.query_one("#adoc-radioset", expect_type=RadioSet).remove_class(
                        "error"
                    )

                # queue path check
                if search_adoc and (
                    queue_path.suffix not in (".xlsx", ".csv", ".json", ".parquet")
                    or not queue_path.is_file()
                ):
                    self.notify(
                        "Must provide Queue Path with .xlsx, .csv, .json, or .parquet"
                        " extension.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#adoc-queue-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                else:
                    self.query_one("#adoc-queue-path", expect_type=Input).remove_class(
                        "error"
                    )

                # output path checks
                if search_adoc and output_path.suffix != ".xlsx":
                    self.notify(
                        "Output Path must be .xlsx to collect inmate details.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#adoc-output-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                elif crawl_adoc and output_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "Output Path must be .xlsx, .csv, .json, or .parquet.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#adoc-output-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                else:
                    self.query_one("#adoc-output-path", expect_type=Input).remove_class(
                        "error"
                    )

                if pass_validation:
                    thread = Thread(
                        target=self.start_adoc_driver, args=[config], name="adoc"
                    )
                    thread.start()
                    self.exit()
            case "start-tables":
                input_path: Path | None = Path(
                    self.query_one("#tables-input-path", expect_type=Input).value
                ).resolve()
                output_path = Path(
                    self.query_one("#tables-output-path", expect_type=Input).value
                ).resolve()
                table = self.query_one("#tables-select", expect_type=SelectWidget).value

                config = {
                    "input-path": input_path,
                    "output-path": output_path,
                    "table": table,
                }

                pass_validation = True

                # input path checks
                if input_path is None:
                    self.notify(
                        "Input Path cannot be left blank.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#tables-input-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                elif not input_path.is_file() and not input_path.is_dir():
                    self.notify(
                        "Input Path could not be located.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#tables-input-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                elif input_path.is_file() and input_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "Input file must have .xlsx, .csv, .json, or .parquet"
                        " extension.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#tables-input-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                else:
                    self.query_one(
                        "#tables-input-path", expect_type=Input
                    ).remove_class("error")
                # output path checks
                if output_path.suffix != ".xlsx" and table == "all":
                    self.notify(
                        "Output Path must have .xlsx extension to export all tables at"
                        " once.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#tables-output-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                elif output_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "Output Path must have .xlsx, .csv, .json, or .parquet"
                        " extension.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one("#tables-output-path", expect_type=Input).add_class(
                        "error"
                    )
                    pass_validation = False
                else:
                    self.query_one(
                        "#tables-output-path", expect_type=Input
                    ).remove_class("error")
                # table select check
                if table is None:
                    self.notify("Must select a table.", title="Error", severity="error")
                    self.query_one(
                        "#tables-select", expect_type=SelectWidget
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#tables-select", expect_type=SelectWidget
                    ).remove_class("error")

                if pass_validation:
                    thread = Thread(
                        target=self.make_tables, args=[config], name="tables"
                    )
                    thread.start()
                    self.exit()
            case "start-archive-tools":
                directory_path = Path(
                    self.query_one(
                        "#archive-tools-directory-path", expect_type=Input
                    ).value
                ).resolve()
                output_path = Path(
                    self.query_one(
                        "#archive-tools-output-path", expect_type=Input
                    ).value
                ).resolve()
                make_archive = self.query_one(
                    "#make-archive-radio", expect_type=RadioButton
                ).value
                rename_cases = self.query_one(
                    "#rename-cases-radio", expect_type=RadioButton
                ).value
                config = {
                    "directory-path": directory_path,
                    "output-path": output_path,
                    "make-archive": make_archive,
                    "rename-cases": rename_cases,
                }

                pass_validation = True

                # radio set check
                if not make_archive and not rename_cases:
                    self.notify(
                        "Must select an archive tool.", title="Error", severity="error"
                    )
                    self.query_one(
                        "#archive-tools-radioset", expect_type=RadioSet
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#archive-tools-radioset", expect_type=RadioSet
                    ).remove_class("error")

                # directory path check
                if not directory_path.is_dir():
                    self.notify(
                        "Must provide a valid case directory path.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#archive-tools-directory-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#archive-tools-directory-path", expect_type=Input
                    ).remove_class("error")

                # output path check
                if make_archive and output_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "Must provide Output Path with .xlsx, .csv, .json, or .parquet"
                        " extension.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#archive-tools-output-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#archive-tools-output-path", expect_type=Input
                    ).remove_class("error")

                if pass_validation:
                    thread = Thread(
                        target=self.start_archive_tools,
                        args=[config],
                        name="archive-tools",
                    )
                    thread.start()
                    self.exit()
            case "start-pairing-tools":
                fields_selected = self.query_one(
                    "#make-documents-field-select", expect_type=SelectionList
                ).selected  # type: ignore
                autopair = self.query_one(
                    "#autopair-radio", expect_type=RadioButton
                ).value
                make_template = self.query_one(
                    "#make-template-radio", expect_type=RadioButton
                ).value
                make_summary = self.query_one(
                    "#make-summary-radio", expect_type=RadioButton
                ).value
                make_documents = self.query_one(
                    "#make-documents-radio", expect_type=RadioButton
                ).value
                autofilter = self.query_one(
                    "#autofilter-radio", expect_type=RadioButton
                ).value
                input_path = (
                    Path(
                        self.query_one(
                            "#pairing-tools-input-path", expect_type=Input
                        ).value
                    ).resolve()
                    if self.query_one(
                        "#pairing-tools-input-path", expect_type=Input
                    ).value
                    != ""
                    else None
                )
                inmates_path = (
                    Path(
                        self.query_one(
                            "#pairing-tools-inmates-path", expect_type=Input
                        ).value
                    ).resolve()
                    if self.query_one("#pairing-tools-inmates-path", expect_type=Input)
                    != ""
                    else None
                )
                pairs_path = (
                    Path(
                        self.query_one(
                            "#pairing-tools-pairs-path", expect_type=Input
                        ).value
                    ).resolve()
                    if self.query_one(
                        "#pairing-tools-pairs-path", expect_type=Input
                    ).value
                    != ""
                    else None
                )
                psr_path = (
                    Path(value).resolve()
                    if (
                        value := self.query_one(
                            "#pairing-tools-psr-path", expect_type=Input
                        ).value
                    )
                    != ""
                    else None
                )
                psq_path = (
                    Path(value).resolve()
                    if (
                        value := self.query_one(
                            "#pairing-tools-psq-path", expect_type=Input
                        ).value
                    )
                    != ""
                    else None
                )
                template_path = (
                    Path(
                        self.query_one(
                            "#pairing-tools-custom-template-path", expect_type=Input
                        ).value
                    ).resolve()
                    if self.query_one(
                        "#pairing-tools-custom-template-path", expect_type=Input
                    ).value
                    != ""
                    else None
                )
                output_path = (
                    Path(
                        self.query_one(
                            "#pairing-tools-output-path", expect_type=Input
                        ).value
                    ).resolve()
                    if self.query_one(
                        "#pairing-tools-output-path", expect_type=Input
                    ).value
                    != ""
                    else None
                )
                default_template = self.query_one(
                    "#default-template-radio", expect_type=RadioButton
                ).value
                custom_template = self.query_one(
                    "#custom-template-radio", expect_type=RadioButton
                ).value
                include_ais = "include-ais" in fields_selected
                include_dob = "include-dob" in fields_selected
                include_race_sex = "include-race-sex" in fields_selected

                config = {
                    "autopair": autopair,
                    "make-template": make_template,
                    "make-summary": make_summary,
                    "make-documents": make_documents,
                    "autofilter": autofilter,
                    "input-path": input_path,
                    "inmates-path": inmates_path,
                    "pairs-path": pairs_path,
                    "psq-path": psq_path,
                    "psr-path": psr_path,
                    "template-path": template_path,
                    "output-path": output_path,
                    "default-template": default_template,
                    "custom-template": custom_template,
                    "include-ais": include_ais,
                    "include-dob": include_dob,
                    "include-race-sex": include_race_sex,
                }
                pass_validation = True

                # radio set check
                if (
                    not autopair
                    and not make_template
                    and not make_summary
                    and not make_documents
                    and not autofilter
                ):
                    self.notify("Must select a tool.", title="Error", severity="error")
                    self.query_one(
                        "#pairing-tools-radioset", expect_type=RadioSet
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#pairing-tools-radioset", expect_type=RadioSet
                    ).remove_class("error")

                # input path checks
                if autofilter:
                    pass
                elif input_path is None:
                    self.notify(
                        "Input Path cannot be left blank.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#pairing-tools-input-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                elif not input_path.is_file() and not input_path.is_dir():
                    self.notify(
                        "Could not locate file or directory at Input Path.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#pairing-tools-input-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                elif input_path.is_file() and input_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "File must have .xlsx, .csv, .json, or .parquet extension.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#pairing-tools-input-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#pairing-tools-input-path", expect_type=Input
                    ).remove_class("error")
                # output path check
                if output_path is None:
                    self.notify(
                        "Output Path cannot be left blank.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#pairing-tools-output-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                elif output_path.is_file() and output_path.suffix not in (
                    ".xlsx",
                    ".csv",
                    ".json",
                    ".parquet",
                ):
                    self.notify(
                        "Output Path file extension must be .xlsx, .csv, .json, or"
                        " .csv.",
                        title="Error",
                        severity="error",
                    )
                    self.query_one(
                        "#pairing-tools-output-path", expect_type=Input
                    ).add_class("error")
                    pass_validation = False
                else:
                    self.query_one(
                        "#pairing-tools-output-path", expect_type=Input
                    ).remove_class("error")
                # mode specific checks
                if autopair:
                    # party search queue path check
                    if psq_path is not None and (
                        not psq_path.is_file()
                        or psq_path.suffix not in (".xlsx", ".csv", ".json", ".parquet")
                    ):
                        self.notify(
                            "Party Search Queue Path must point to a file with .xlsx, "
                            ".csv, .json, or .parquet extension."
                        )
                        self.query_one(
                            "#pairing-tools-psq-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    else:
                        self.query_one(
                            "#pairing-tools-psq-path", expect_type=Input
                        ).remove_class("error")
                    # party search results path check
                    if psr_path is None or (
                        not psr_path.is_file()
                        or psr_path.suffix
                        not in (
                            ".xlsx",
                            ".csv",
                            ".json",
                            ".parquet",
                        )
                    ):
                        self.notify(
                            "Must provide Party Search Results Path with .xlsx, .csv,"
                            " .json, or .parquet extension.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-psr-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    else:
                        self.query_one(
                            "#pairing-tools-psr-path", expect_type=Input
                        ).remove_class("error")
                    # output path checks
                    if output_path is None:
                        pass
                    elif not output_path.is_dir() and output_path.suffix not in (
                        ".xlsx",
                        ".csv",
                        ".json",
                        ".parquet",
                    ):
                        self.notify(
                            "Output Path must be a file.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-output-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                if make_summary or make_documents:
                    if pairs_path is None:
                        self.notify(
                            "Pairs Path cannot be left blank.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-pairs-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    elif not pairs_path.is_file() or pairs_path.suffix not in (
                        ".xlsx",
                        ".csv",
                        ".json",
                        ".parquet",
                    ):
                        self.notify(
                            "Must provide Pairs Path with .xlsx, .csv, .json, or"
                            " .parquet extension.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-pairs-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    else:
                        self.query_one(
                            "#pairing-tools-pairs-path", expect_type=Input
                        ).remove_class("error")
                if make_documents:
                    if not default_template and not custom_template:
                        self.notify(
                            "Must select a template choice.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#template-radioset", expect_type=RadioSet
                        ).add_class("error")
                        pass_validation = False
                    else:
                        self.query_one(
                            "#template-radioset", expect_type=RadioSet
                        ).remove_class("error")
                    if custom_template:
                        if template_path is None:
                            self.notify(
                                "Custom Template Path cannot be left blank.",
                                title="Error",
                                severity="error",
                            )
                            self.query_one(
                                "#pairing-tools-custom-template-path", expect_type=Input
                            ).add_class("error")
                            pass_validation = False
                        elif (
                            template_path.suffix
                            not in (".xlsx", ".csv", ".json", ".parquet")
                            or not template_path.is_file()
                        ):
                            self.notify(
                                "Must provide path to custom template (.docx).",
                                title="Error",
                                severity="error",
                            )
                            self.query_one(
                                "#pairing-tools-custom-template-path", expect_type=Input
                            ).add_class("error")
                            pass_validation = False
                        else:
                            self.query_one(
                                "#pairing-tools-custom-template-path", expect_type=Input
                            ).remove_class("error")
                if autofilter:
                    if inmates_path is None:
                        self.notify(
                            "ADOC Inmates List Path cannot be left blank.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-inmates-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    elif not inmates_path.is_file():
                        self.notify(
                            "Could not locate file at ADOC Inmates List Path.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-inmates-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    elif inmates_path.suffix not in (
                        ".xlsx",
                        ".csv",
                        ".json",
                        ".parquet",
                    ):
                        self.notify(
                            "ADOC Inmates List Path must have file extension .xlsx,"
                            " .csv, .json, or .parquet.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-inmates-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    else:
                        self.query_one(
                            "#pairing-tools-inmates-path", expect_type=Input
                        ).remove_class("error")
                    if psr_path is None or (
                        not psr_path.is_file()
                        or psr_path.suffix
                        not in (
                            ".xlsx",
                            ".csv",
                            ".json",
                            ".parquet",
                        )
                    ):
                        self.notify(
                            "Must provide Party Search Results Path with .xlsx, .csv,"
                            " .json, or .parquet extension.",
                            title="Error",
                            severity="error",
                        )
                        self.query_one(
                            "#pairing-tools-psr-path", expect_type=Input
                        ).add_class("error")
                        pass_validation = False
                    else:
                        self.query_one(
                            "#pairing-tools-psr-path", expect_type=Input
                        ).remove_class("error")

                if pass_validation:
                    thread = Thread(
                        target=self.start_pairing_tools,
                        args=[config],
                        name="pairing-tools",
                    )
                    thread.start()
                    self.exit()

    def on_radio_set_changed(self: "AlacorderApp", event: RadioSet.Changed) -> None:
        """Handle radio button change."""
        match event.pressed.id:
            case "fetch-cases-radio":
                self.query_one(
                    "#party-search-options", expect_type=Horizontal
                ).styles.display = "block"
                self.query_one(
                    "#fetch-cases-options", expect_type=Horizontal
                ).styles.display = "none"
            case "party-search-radio":
                self.query_one(
                    "#party-search-options", expect_type=Horizontal
                ).styles.display = "none"
                self.query_one(
                    "#fetch-cases-options", expect_type=Horizontal
                ).styles.display = "block"
            case "search-adoc-radio":
                self.query_one(
                    "#hidden-adoc-search", expect_type=Container
                ).styles.display = "block"
                self.query_one(
                    "#adoc-output-path", expect_type=Input
                ).placeholder = "File must be .xlsx"
            case "crawl-adoc-radio":
                self.query_one(
                    "#hidden-adoc-search", expect_type=Container
                ).styles.display = "none"
                self.query_one(
                    "#adoc-output-path", expect_type=Input
                ).placeholder = "File must be .xlsx, .csv, .json, or .parquet"
            case "make-archive-radio":
                self.query_one(
                    "#archive-tools-output-container", expect_type=Container
                ).styles.display = "block"
            case "rename-cases-radio":
                self.query_one(
                    "#archive-tools-output-container", expect_type=Container
                ).styles.display = "none"
            case "autopair-radio":
                self.query_one(
                    "#pairing-tools-input-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-psr-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-psq-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-inmates-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-pairs-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-output-path", expect_type=Input
                ).placeholder = "Path to output file (.xlsx, .csv, .parquet, .json)"
                self.query_one("#template-options", expect_type=Horizontal).add_class(
                    "hidden"
                )
                self.query_one(
                    "#custom-template-container", expect_type=Container
                ).add_class("hidden")
            case "make-template-radio":
                self.query_one(
                    "#pairing-tools-input-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-psr-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-psq-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-inmates-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-pairs-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-output-path", expect_type=Input
                ).placeholder = "Path to output file (.xlsx, .csv, .parquet, .json)"
                self.query_one("#template-options", expect_type=Horizontal).add_class(
                    "hidden"
                )
                self.query_one(
                    "#custom-template-container", expect_type=Container
                ).add_class("hidden")
            case "make-summary-radio":
                self.query_one(
                    "#pairing-tools-input-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-psr-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-psq-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-inmates-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-pairs-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-output-path", expect_type=Input
                ).placeholder = "Path to output file (.xlsx, .csv, .parquet, .json)"
                self.query_one("#template-options", expect_type=Horizontal).add_class(
                    "hidden"
                )
                self.query_one(
                    "#custom-template-container", expect_type=Container
                ).add_class("hidden")
            case "make-documents-radio":
                self.query_one(
                    "#pairing-tools-input-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-inmates-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-psr-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-psq-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-pairs-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-output-path", expect_type=Input
                ).placeholder = "Path to output directory"
                self.query_one(
                    "#template-options", expect_type=Horizontal
                ).remove_class("hidden")
                if self.query_one(
                    "#custom-template-radio", expect_type=RadioButton
                ).value:
                    self.query_one(
                        "#custom-template-container", expect_type=Container
                    ).remove_class("hidden")
                else:
                    self.query_one(
                        "#custom-template-container", expect_type=Container
                    ).add_class("hidden")
            case "default-template-radio":
                self.query_one(
                    "#custom-template-container", expect_type=Container
                ).add_class("hidden")
            case "custom-template-radio":
                self.query_one(
                    "#custom-template-container", expect_type=Container
                ).remove_class("hidden")
            case "autofilter-radio":
                self.query_one(
                    "#pairing-tools-input-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-inmates-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-psr-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-psq-container", expect_type=Container
                ).remove_class("hidden")
                self.query_one(
                    "#pairing-tools-pairs-container", expect_type=Container
                ).add_class("hidden")
                self.query_one("#template-options", expect_type=Horizontal).add_class(
                    "hidden"
                )
                self.query_one(
                    "#custom-template-container", expect_type=Container
                ).add_class("hidden")
                self.query_one(
                    "#pairing-tools-output-path", expect_type=Input
                ).placeholder = "Path to output file (.xlsx, .csv, .parquet, .json)"

    def action_quit_app(self: "AlacorderApp") -> None:
        """Event handler to quit app."""
        self.exit()

    def start_alacourt_driver(self: "AlacorderApp", config: dict[str, Any]) -> None:
        """Start Alacourt Driver."""
        if config["fetch-cases"]:
            driver = AlacourtDriver(
                config["output-path"], headless=not config["show-browser"]
            )
            driver.login(config["customer-id"], config["user-id"], config["password"])
            driver.start_case_number_queue(
                config["queue-path"],
                verify=config["verify"],
                pre_verify=config["pre-verify"],
            )
        elif config["party-search"]:
            driver = AlacourtDriver(headless=not config["show-browser"])
            driver.login(config["customer-id"], config["user-id"], config["password"])
            driver.start_party_search_queue(
                config["queue-path"],
                config["output-path"],
                criminal_only=config["criminal-only"],
            )
        console = Console()
        console.print("[green]Task succeeded.[/green]")

    def start_adoc_driver(self: "AlacorderApp", config: dict[str, Any]) -> None:
        """Start ADOC Driver."""
        driver = ADOCDriver(headless=not config["show-browser"])
        if config["crawl-adoc"]:
            driver.crawl(config["output-path"])
        elif config["search-adoc"]:
            driver.start_queue(config["queue-path"], config["output-path"])
        console = Console()
        console.print("[green]Task succeeded.[/green]")

    def make_tables(self: "AlacorderApp", config: dict[str, Any]) -> None:
        """Make tables."""
        cases = Cases(config["input-path"])
        match config["table"]:
            case "all":
                cases.tables()
            case "cases":
                cases.cases()
            case "disposition-charges":
                cases.disposition_charges()
            case "filing-charges":
                cases.filing_charges()
            case "fees":
                cases.fees()
            case "attorneys":
                cases.attorneys()
            case "case-action-summary":
                cases.case_action_summary()
            case "financial-history":
                cases.financial_history()
            case "images":
                cases.images()
            case "sentences":
                cases.sentences()
            case "enforcement":
                cases.enforcement()
            case "settings":
                cases.settings()
            case "witnesses":
                cases.witnesses()
            case "restitution":
                cases.restitution()
            case "linked-cases":
                cases.linked_cases()
            case "continuances":
                cases.continuances()
            case "parties":
                cases.parties()
            case "central-disbursement-division":
                cases.central_disbursement_division()
        cases.write_tables(config["output-path"])
        console = Console()
        console.print("[green]Task succeeded.[/green]")

    def start_archive_tools(self: "AlacorderApp", config: dict[str, Any]) -> None:
        """Start archive tools."""
        cases = Cases(config["directory-path"])
        if config["make-archive"]:
            cases.read()
            cases.write_archive(config["output-path"])
        elif config["rename-cases"]:
            rename_cases(config["directory-path"])
        console = Console()
        console.print("[green]Task succeeded.[/green]")

    def start_pairing_tools(self: "AlacorderApp", config: dict[str, Any]) -> None:
        """Start pairing tools."""
        console = Console()
        if config["autopair"]:
            autopair(
                config["input-path"],
                config["psr-path"],
                config["output-path"],
                config["psq-path"],
            )
            console.print("[green]Task succeeded.[/green]")
        elif config["make-template"]:
            cases = Cases(config["input-path"])
            cases.read()
            write({"pairs-template": cases.pairs_template()}, config["output-path"])
            console.print("[green]Task succeeded.[/green]")
        elif config["make-summary"]:
            cases = Cases(config["input-path"])
            cases.read()
            write(
                {"summary": cases.summary(config["pairs-path"])}, config["output-path"]
            )
            console.print("[green]Task succeeded.[/green]")
        elif config["make-documents"]:
            cases = Cases(config["input-path"])
            cases.read()
            if config["custom-template"]:
                cases.write_summary_docs(
                    config["pairs-path"],
                    config["output-path"],
                    config["template-path"],
                    include_ais=config["include-ais"],
                    include_dob=config["include-dob"],
                    include_race_sex=config["include-race-sex"],
                )
                console.print("[green]Task succeeded.[/green]")
            elif config["default-template"]:
                cases.write_summary_docs(
                    config["pairs-path"],
                    config["output-path"],
                    None,
                    include_ais=config["include-ais"],
                    include_dob=config["include-dob"],
                    include_race_sex=config["include-race-sex"],
                )
                console.print("[green]Task succeeded.[/green]")
        elif config["autofilter"]:
            autofilter(
                config["inmates-path"], config["psr-path"], config["output-path"]
            )
            console.print("[green]Task succeeded.[/green]")


@app.command()
def launch() -> None:
    """Launch textual user interface."""
    tui = AlacorderApp()
    tui.run()


@app.command(no_args_is_help=True)
def party_search(
    queue_path: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to queue table with one or more columns: 'Name', 'Party Type',"
                " 'SSN', 'DOB', 'County', 'Division', 'Case Year', 'Filed Before',"
                " 'Filed After', 'No Records'."
            ),
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to output results table. Will attempt to append to existing table"
                " at output path."
            ),
            show_default=False,
        ),
    ],
    customer_id: Annotated[
        str,
        typer.Option(
            "--customer-id",
            "-c",
            help="Customer ID for Alacourt login.",
            prompt="Customer ID",
            show_default=False,
        ),
    ],
    user_id: Annotated[
        str,
        typer.Option(
            "--user-id",
            "-u",
            help="User ID for Alacourt login.",
            prompt="User ID",
            show_default=False,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            help="Password for Alacourt login.",
            prompt="Password",
            hide_input=True,
            show_default=False,
        ),
    ],
    *,
    criminal_only: Annotated[
        bool,
        typer.Option(
            "--criminal-only",
            help="Only search criminal cases.",
            show_default=False,
        ),
    ] = False,
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
) -> None:
    """
    Collect results from Alacourt Party Search into a table at `output_path`.
    Input `queue_path` table from .xlsx, .csv, .json, or .parquet with
    columns corresponding to Alacourt Party Search fields: 'Name', 'Party
    Type', 'SSN', 'DOB', 'County', 'Division', 'Case Year', 'Filed
    Before', 'Filed After', 'No Records'.
    """
    headless = not show_browser

    if queue_path.suffix not in (".xlsx", ".csv", ".json", ".parquet"):
        msg = (
            "Queue path file extension not supported. Retry with .xlsx, .csv,"
            " .json, or .parquet."
        )
        raise BadFileError(msg)
    if output_path.suffix not in (".xlsx", ".csv", ".json", ".parquet"):
        msg = (
            "Output path file extension not supported. Retry with .xlsx, .csv,"
            " .json, or .parquet."
        )
        raise BadFileError(msg)

    driver = AlacourtDriver(headless=headless)
    driver.login(customer_id, user_id, password)
    driver.start_party_search_queue(
        queue_path, output_path, criminal_only=criminal_only
    )


@app.command(no_args_is_help=True)
def fetch_cases(
    queue_path: Annotated[
        Path,
        typer.Argument(
            help="Path to queue table with 'Case Number' column.",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to output directory. PDFs will populate directory as they "
                "download."
            ),
            show_default=False,
        ),
    ],
    customer_id: Annotated[
        str,
        typer.Option(
            "--customer-id",
            "-c",
            help="Customer ID for Alacourt login.",
            prompt="Customer ID",
            show_default=False,
        ),
    ],
    user_id: Annotated[
        str,
        typer.Option(
            "--user-id",
            "-u",
            help="User ID for Alacourt login.",
            prompt="User ID",
            show_default=False,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            help="Password for Alacourt login.",
            prompt="Password",
            hide_input=True,
            show_default=False,
        ),
    ],
    *,
    verify: Annotated[
        bool,
        typer.Option(
            help="Verify successful case downloads and reattempt failed downloads."
        ),
    ] = True,
    pre_verify: Annotated[
        bool,
        typer.Option(
            help="Check output directory for already downloaded cases before starting."
        ),
    ] = False,
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
) -> None:
    """
    From a queue table with 'Case Number' or 'CaseNumber' column, download
    case detail PDFs to directory at `output_path`.
    """
    headless = not show_browser

    if queue_path.suffix not in (".xlsx", ".csv", ".json", ".parquet"):
        msg = (
            "Queue path file extension not supported. Retry with .xlsx, .csv,"
            " .json, or .parquet."
        )
        raise BadFileError(msg)

    if not output_path.is_dir():
        output_path.mkdir()

    driver = AlacourtDriver(output_path, headless=headless)
    driver.login(customer_id, user_id, password)
    driver.start_case_number_queue(queue_path, verify=verify, pre_verify=pre_verify)


@app.command(no_args_is_help=True)
def crawl_adoc(
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
    *,
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
) -> None:
    """
    Collect full inmates list from ADOC Inmate Search and write to table at
    `output_path` (.xlsx, .csv, .json, .parquet).
    """
    headless = not show_browser

    driver = ADOCDriver(output_path, headless=headless)
    driver.crawl(output_path)


@app.command(no_args_is_help=True)
def search_adoc(
    queue_path: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to queue table with 'First Name', 'Last Name', and 'AIS' columns."
            ),
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
    *,
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
) -> None:
    """
    Search ADOC using queue with 'First Name', 'Last Name', and 'AIS' columns
    to retrieve sentencing information from ADOC. Record table to
    `output_path`.
    """
    headless = not show_browser

    driver = ADOCDriver(output_path, headless=headless)
    driver.start_queue(queue_path, output_path)


@app.command(no_args_is_help=True)
def make_archive(
    directory_path: Annotated[
        Path,
        typer.Argument(help="Path to PDF case directory.", show_default=False),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output archive (recommend .parquet).",
            show_default=False,
        ),
    ],
) -> None:
    """Create case text archive from directory of case detail PDFs."""
    cases = Cases(directory_path)
    cases.write_archive(output_path)


@app.command(no_args_is_help=True)
def make_table(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="Path to input case directory or archive.", show_default=False
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to output table (.xlsx, .csv, .json, .parquet). `All` table"
                " export must output to .xlsx."
            ),
            show_default=False,
        ),
    ],
    table: Annotated[
        str,
        typer.Option(
            "--table",
            "-t",
            help=(
                "Output table selection: all, cases, filing-charges,"
                " disposition-charges, fees, attorneys, case-action-summary,"
                " financial-history, images, sentences, enforcement, settings,"
                " witnesses, restitution, linked-cases, continuances, parties,"
                " central-disbursement-division."
            ),
            show_default=True,
        ),
    ] = "all",
) -> None:
    """Create table at `output_path` from archive or directory at `input_path`."""
    output: pl.DataFrame | dict[str, pl.DataFrame]

    if table == "all" and output_path.suffix != ".xlsx":
        msg = (
            "Must select a table to export using --table flag. Options: cases,"
            " filing-charges, disposition-charges, fees, attorneys,"
            " case-action-summary, financial-history, images, sentences, enforcement,"
            " settings, witnesses, restitution, linked-cases, continuances, parties,"
            " central-disbursement-division."
        )
        raise ConfigurationError(msg)

    cases = Cases(input_path)
    cases.read()

    match table:
        case "all":
            output = cases.tables()
        case "cases":
            output = cases.cases()
        case "fees":
            output = cases.fees()
        case "filing-charges":
            output = cases.filing_charges()
        case "disposition-charges":
            output = cases.disposition_charges()
        case "attorneys":
            output = cases.attorneys()
        case "case-action-summary":
            output = cases.case_action_summary()
        case "financial-history":
            output = cases.financial_history()
        case "images":
            output = cases.images()
        case "sentences":
            output = cases.sentences()
        case "enforcement":
            output = cases.enforcement()
        case "settings":
            output = cases.settings()
        case "witnesses":
            output = cases.witnesses()
        case "restitution":
            output = cases.restitution()
        case "linked-cases":
            output = cases.linked_cases()
        case "continuances":
            output = cases.continuances()
        case "parties":
            output = cases.parties()
        case "central-disbursement-division":
            output = cases.central_disbursement_division()
        case _:
            msg = (
                "Invalid table selection. Options: all, cases, filing-charges,"
                " disposition-charges, fees, attorneys, case-action-summary,"
                " financial-history, images, sentences, enforcement, settings,"
                " witnesses, restitution, linked-cases, continuances, parties,"
                " central-disbursement-division."
            )
            raise ConfigurationError(msg)

    write(output, output_path, log=True)


@app.command(no_args_is_help=True)
def make_summary(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="Path to input case directory or archive.", show_default=False
        ),
    ],
    pairs_path: Annotated[
        Path,
        typer.Argument(
            help="Path to filled pairs template or party search results table.",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
) -> None:
    """
    Create voting rights summary grouped by person using a completed name/AIS
    pairing template (use make-template to create empty template).
    """
    cases = Cases(input_path)
    output = cases.summary(pairs_path)
    write({"summary": output}, output_path)


@app.command(no_args_is_help=True)
def make_template(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="Path to input case directory or archive.", show_default=False
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
) -> None:
    """
    Create empty pairing template to be used as input for make-summary to
    create a voting rights summary grouped by person instead of by case.
    """
    cases = Cases(input_path)
    output = cases.pairs_template()
    write({"pairs-template": output}, output_path)


def rename_case(path: Path) -> None:
    """Rename a case PDF to its case number."""
    doc = fitz.open(path)
    text = " \n ".join(
        x[4].replace("\n", " ") for x in doc[0].get_text(option="blocks")
    )
    county = re.search(r"County: (\d\d)", str(text))
    short = re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", str(text))
    if short and not county:
        cnum = short.group(1)
    elif short and county:
        cnum = f"{county.group(1)}-{short.group(1)}"
    else:
        cnum = path.name
    path.rename(f"{path.parent}/{cnum}.pdf")


def case_number_from_path(path: Path) -> str | None:
    doc = fitz.open(path)
    text = " \n ".join(
        x[4].replace("\n", " ") for x in doc[0].get_text(option="blocks")
    )
    county = re.search(r"County: (\d\d)", str(text))
    short = re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", str(text))
    if short and not county:
        cnum = short.group(1)
    elif short and county:
        cnum = f"{county.group(1)}-{short.group(1)}"
    else:
        cnum = None
    return cnum


@app.command(no_args_is_help=True)
def rename_cases(
    input_directory: Annotated[
        Path,
        typer.Argument(help="Directory to rename cases within.", show_default=False),
    ],
) -> None:
    """
    Rename all cases in a directory to full case number. Duplicates will be
    removed.
    """
    paths = list(input_directory.rglob("**/*.pdf"))
    progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
    with progress_bar as bar, multiprocessing.Pool() as pool:
        for _ in bar.track(
            pool.imap(rename_case, paths),
            description="Renaming PDFs…",
            total=len(paths),
        ):
            pass


@app.command(no_args_is_help=True)
def make_documents(
    archive: Annotated[
        Path,
        typer.Argument(
            help="PDF directory or case archive to pull data from.", show_default=False
        ),
    ],
    pairs: Annotated[
        Path, typer.Argument(help="Complete pairs template path.", show_default=False)
    ],
    output_dir: Annotated[
        Path,
        typer.Argument(help="Directory to write .docx files to.", show_default=False),
    ],
    template: Annotated[
        Optional[Path],
        typer.Option(
            "--template",
            "-t",
            help="Path to optional custom .docx template.",
            show_default=False,
        ),
    ] = None,
    *,
    ais: Annotated[
        bool,
        typer.Option(
            "--ais / --no-ais", help="Include AIS # in output files.", show_default=True
        ),
    ] = False,
    dob: Annotated[
        bool,
        typer.Option(
            "--dob / --no-dob", help="Include DOB in output files.", show_default=True
        ),
    ] = True,
    race_sex: Annotated[
        bool,
        typer.Option(
            "--race-sex / --no-race-sex",
            help="Include Race and Sex in output files.",
            show_default=True,
        ),
    ] = True,
) -> None:
    """
    Make .docx summaries with voting rights information for each unique identifier in
    `pairs` at `output_dir`.
    """
    cases = Cases(archive)
    cases.write_summary_docs(
        pairs, output_dir, template_path=template, include_ais=ais, include_dob=dob
    )


@app.command(no_args_is_help=True)
def autopair(
    archive: Annotated[
        Path,
        typer.Argument(
            help="PDF directory or case archive to pull data from.", show_default=False
        ),
    ],
    party_search_results: Annotated[
        Path,
        typer.Argument(
            help="Party search results table with 'Search' and 'Name' columns.",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xlsx, .csv, .parquet, .json).",
            show_default=False,
        ),
    ],
    ais_source: Annotated[
        Optional[Path],
        typer.Option(
            "--ais-source",
            help=(
                "Path to party search queue or other table with 'Name' column and "
                "'AIS', 'Unique ID', or 'AIS / Unique ID' column."
            ),
        ),
    ],
) -> None:
    """
    Automatically generate filled pairs template from party search results table with
    'Search' and 'Name' columns.
    """
    cases = Cases(archive)
    results = cast(pl.DataFrame, read(party_search_results))

    key_col = None
    ais = None

    if ais_source is not None:
        ais = cast(pl.DataFrame, read(ais_source))
        for column in ais.columns:
            if column in ("AIS / Unique ID", "AIS", "Unique ID"):
                key_col = column
                break
        if key_col is None:
            msg = (
                f"Table at '{ais_source}' does not have a 'AIS / Unique ID', 'AIS', or "
                "'Unique ID' column."
            )
            raise ValueError(msg)

    pairs = cases.autopair(results, unique_id_map=ais, unique_id_column=key_col)

    write(pairs, output_path, log=True)


@app.command(no_args_is_help=True)
def autofilter(
    inmates_list: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to inmates list from `crawl-adoc` output with 'Name' and"
                " 'BirthYear' columns."
            ),
            show_default=False,
        ),
    ],
    party_search_results: Annotated[
        Path,
        typer.Argument(
            help="Path to party search results to filter.", show_default=False
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Output table path (.xlsx, .csv, .json, .parquet).", show_default=False
        ),
    ],
) -> pl.DataFrame:
    """
    Automatically filter `party_search_results` using crawl-adoc outputs, so that cases
    with mismatching DOBs are removed.
    """
    inmates = read(inmates_list)
    assert isinstance(inmates, pl.DataFrame)
    if "Name" not in inmates.columns or "BirthYear" not in inmates.columns:
        msg = "One or more columns missing from `inmates_list`: 'Name', 'BirthYear'."
        raise BadFileError(msg)

    psr = read(party_search_results)
    assert isinstance(psr, pl.DataFrame)
    if "Search" not in psr.columns or "DOB" not in psr.columns:
        msg = "'Search' column missing from `party_search_results`."
        raise BadFileError(msg)

    match psr["DOB"].dtype:
        case pl.Utf8:
            psr = psr.with_columns(
                pl.col("DOB")
                .str.extract(r"(\d\d\d\d)")
                .cast(pl.Int64, strict=False)
                .alias("ActualBirthYear")
            )
        case pl.Date:
            psr = psr.with_columns(pl.col("DOB").dt.year().alias("ActualBirthYear"))
        case _:
            msg = "DOB column must be string or date type."
            raise BadFileError(msg)

    inmates = inmates.select(
        pl.col("Name").alias("NameMatch"),
        pl.col("BirthYear").alias("ExpectedBirthYear"),
    )
    psr = (
        psr.with_columns(pl.col("Search").alias("NameMatch"))
        .join(inmates, on="NameMatch", how="left")
        .filter(pl.col("ActualBirthYear") == pl.col("ExpectedBirthYear"))
        .select(pl.exclude("ActualBirthYear", "ExpectedBirthYear", "NameMatch"))
    )
    write({"filtered-party-search-results": psr}, output_path)
    return psr


def version_callback(*, value: bool) -> None:
    """Print version."""
    if value:
        console.print(
            "\n[bright_red]┏┓[/bright_red][orange3]┓ [/orange3]"
            "[bright_yellow]┏┓[/bright_yellow][green]┏┓[/green]"
            "[deep_sky_blue1]┏┓[/deep_sky_blue1][green]┳┓[/green]"
            "[bright_yellow]┳┓[/bright_yellow][orange3]┏┓[/orange3]"
            "[bright_red]┳┓[/bright_red]\n"
            "[bright_red]┣┫[/bright_red][orange3]┃ [/orange3]"
            "[bright_yellow]┣┫[/bright_yellow][green]┃ [/green]"
            "[deep_sky_blue1]┃┃[/deep_sky_blue1][green]┣┫[/green]"
            "[bright_yellow]┃┃[/bright_yellow][orange3]┣ [/orange3]"
            "[bright_red]┣┫[/bright_red]\n"
            "[bright_red]┛┗[/bright_red][orange3]┗┛[/orange3]"
            "[bright_yellow]┛┗[/bright_yellow][green]┗┛[/green]"
            "[deep_sky_blue1]┗┛[/deep_sky_blue1][green]┛┗[/green]"
            "[bright_yellow]┻┛[/bright_yellow][orange3]┗┛[/orange3]"
            "[bright_red]┛┗[/bright_red]\n"
            f"[bold][bright_white]Alacorder {__version__}[/bold]\n"
            "(c) 2023 Sam Robson[/bright_white]\n"
        )
        raise typer.Exit()


@app.callback()
def main(
    *,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        help="Show the version and exit.",
    ),
) -> None:
    """Invoke CLI options."""


if __name__ == "__main__":
    app()


# ┌─┐┌─┐┌┬┐  ┌─┐┬ ┬┌┐┌┌─┐┌┬┐┬┌─┐┌┐┌┌─┐
# │ ┬├┤  │   ├┤ │ │││││   │ ││ ││││└─┐
# └─┘└─┘ ┴   └  └─┘┘└┘└─┘ ┴ ┴└─┘┘└┘└─┘
# Get functions return a field from the full case text of a PDF.
# Call read(path) to get case text from PDF.


def get_name(text: str) -> str:
    """Get Name field from case text."""
    if match := re.search(
        r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{0,100})(Case Number)*",
        text,
    ):
        return (
            match.group(1).strip()
            if re.search(r"(DC|CC|TR|TP)\-\d{4}-\d{6}\.\d{2}", text)
            else ""
        )
    else:
        return ""


def get_alias(text: str) -> str:
    """Get Alias field from case text."""
    if match := re.search(r"(?s)(SSN\:)(.{0,100})(Alias 1)", text):
        return match.group(2).strip()
    else:
        return ""


def get_alias2(text: str) -> str:
    """Get Alias 2 field from case text."""
    if match := re.search(r"Alias 2: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_dob(text: str) -> datetime | None:
    """Get DOB field from case text."""
    if match := re.search(r"(\d{2}/\d{2}/\d{4})(?:.{0,5}DOB:)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_phone(text: str) -> str:
    """Get Phone field from case text."""
    if match := re.search(r"(Phone: )(.+)", text):
        out = re.sub(r"[^0-9]", "", match.group(2)).strip()
        if len(out) < 7 or out[:10] == "2050000000":
            return ""
        elif len(out) > 10:
            return out[:10]
        else:
            return out
    else:
        return ""


def get_race(text: str) -> str:
    """Get Race field from case text."""
    if match := re.search(r"(B|W|H|A)/(F|M)", text):
        return match.group(1)
    else:
        return ""


def get_sex(text: str) -> str:
    """Get Sex field from case text."""
    if match := re.search(r"(B|W|H|A)/(F|M)", text):
        return match.group(2)
    else:
        return ""


def get_address_1(text: str) -> str:
    """Get Address 1 field from case text."""
    if match := re.search(r"(?:Address 1:)(.+)(?:Phone)*?", text):
        return re.sub(r"Phone.+", "", match.group(1).strip()).strip()
    else:
        return ""


def get_address_2(text: str) -> str:
    """Get Address 2 field from case text."""
    if match := re.search(r"(?:Address 2:)(.+)", text):
        return re.sub(r"Defendant Information|JID:.+", "", match.group(1)).strip()
    else:
        return ""


def get_city(text: str) -> str:
    """Get City field from case text."""
    if match := re.search(r"(?:City: )(.*)(?:State: )(.*)", text):
        return match.group(1).strip()
    else:
        return ""


def get_state(text: str) -> str:
    """Get State field from case text."""
    if match := re.search(r"(?:City: )(.*)(?:State: )(.*)", text):
        return match.group(2).strip()
    else:
        return ""


def get_country(text: str) -> str:
    """Get Country field from case text."""
    if match := re.search(r"Country: (\w*)", text):
        return match.group(1)
    else:
        return ""


def get_zip_code(text: str) -> str:
    """Get Zip Code field from case text."""
    if match := re.search(r"(Zip: )(.+)", text):
        return re.sub(r"-0000$|[A-Z].+", "", match.group(2)).strip()
    else:
        return ""


def get_address(text: str) -> str:
    """Get full street address from case text."""
    street1 = get_address_1(text)
    street2 = get_address_2(text)
    zipcode = get_zip_code(text)
    city = get_city(text)
    state = get_state(text)
    out = (
        f"{street1} {street2} {city}, {state} {zipcode}".strip()
        if len(city) > 3
        else f"{street1} {street2} {city} {state} {zipcode}".strip()
    )
    return re.sub(r"\s+", " ", out)


def get_total_amount_due(text: str) -> float | None:
    """Get total amount due from case text."""
    if match := re.search(r"(Total:.+\-?\$[^\n]*)", text):
        split_row = match.group(1).split()
        if len(split_row) < 2:
            return None
        return float(re.sub(",", "", split_row[1].replace("$", "")))
    else:
        return None


def get_total_amount_paid(text: str) -> float | None:
    """Get total amount paid from case text."""
    if match := re.search(r"(Total:.+\-?\$[^\n]*)", text):
        split_row = match.group(1).split()
        if len(split_row) < 3:
            return None
        return float(re.sub(",", "", split_row[2].replace("$", "")))
    else:
        return None


def get_total_balance(text: str) -> float | None:
    """Get total balance from case text."""
    if match := re.search(r"(Total:.+\-?\$[^\n]*)", text):
        split_row = match.group(1).split()
        if len(split_row) < 4:
            return None
        return float(re.sub(",", "", split_row[3].replace("$", "")))
    else:
        return None


def get_total_amount_hold(text: str) -> float | None:
    """Get total amount hold from case text."""
    if match := re.search(r"(Total:.+\-?\$[^\n]*)", text):
        split_row = match.group(1).split()
        if len(split_row) < 5:
            return None
        return float(re.sub(",", "", split_row[4].replace("$", "")))
    else:
        return None


def get_short_case_number(text: str) -> str:
    """Get short case number from case text."""
    if match := re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", text):
        return match.group()
    else:
        return ""


def get_county(text: str) -> str:
    """Get County field from case text."""
    if match := re.search(r"County: (\d\d)", text):
        return match.group(1)
    else:
        return ""


def get_case_number(text: str) -> str:
    """Get full case number from case text."""
    county = re.search(r"County: (\d{2})", text)
    short = re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", text)
    if short and county:
        return f"{county.group(1)}-{short.group(1)}"
    if short and not county:
        return short.group(1)
    return ""


def get_case_year(text: str) -> int | None:
    """Get Case Year from case text."""
    if match := re.search(r"\w{2}\-(\d{4})-\d{6}\.\d{2}", text):
        return int(match.group(1))
    else:
        return None


def get_last_name(text: str) -> str:
    """Get Last Name from case text."""
    if (name := get_name(text)) not in (None, ""):
        assert isinstance(name, str)
        return name.split()[0].strip()
    else:
        return ""


def get_first_name(text: str) -> str:
    """Get First Name from case text."""
    if (name := get_name(text)) not in (None, ""):
        assert isinstance(name, str)
        split_name = name.split()
        if len(split_name) == 1:
            return ""
        return split_name[1].strip()
    else:
        return ""


def get_middle_name(text: str) -> str:
    """Get Middle Name from case text."""
    if (name := get_name(text)) not in (None, ""):
        assert isinstance(name, str)
        split_name = name.split()
        if len(split_name) < 3:
            return ""
        return split_name[2].strip()
    else:
        return ""


def get_related_cases(text: str) -> str:
    """Get Related Cases from case text."""
    if match := re.search(r"Related Cases: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_filing_date(text: str) -> datetime | None:
    """Get Filing Date from case text."""
    if match := re.search(r"Filing Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_case_initiation_date(text: str) -> datetime | None:
    """Get Case Initiation Date from case text."""
    if match := re.search(r"Case Initiation Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_arrest_date(text: str) -> datetime | None:
    """Get Arrest Date from case text."""
    if match := re.search(r"Arrest Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_offense_date(text: str) -> datetime | None:
    """Get Offense Date from case text."""
    if match := re.search(r"Offense Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_indictment_date(text: str) -> datetime | None:
    """Get Indictment Date from case text."""
    if match := re.search(r"Indictment Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_youthful_date(text: str) -> datetime | None:
    """Get Youthful Date from case text."""
    if match := re.search(r"Youthful Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_retrieved(text: str) -> datetime | None:
    """Get Retrieved date from case text."""
    if match := re.search(r"Alacourt\.com (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_court_action(text: str) -> str:
    """Get Court Action field from case text."""
    if match := re.search(
        (
            r"Court Action: (WAIVED TO GJ \d\d/\d\d/\d\d\d\d|WAIVED TO GJ|GUILTY PLEA"
            r"|NOT GUILTY/INSAN E|GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS"
            r" W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL"
            r" PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|TRANSFERED"
            r" ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER"
            r" \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND"
            r" FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50"
            r" CASE\)|DISMISSED|FORFEITURE|TRANSFER|REMANDED|WAIVED|ACQUITTED|WITHDRAWN"
            r"|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER"
            r"|PROBATION NT REVOKE|PROBATION/S|ANCTION|NO PROBABLE CAUSE|PETITION"
            r" GRANTED|PROBATION TERMINATED|FINAL FORF\. SET ASIDE|DOCKETED"
            r"|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)"
            r"|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)"
        ),
        text,
    ):
        return re.sub("DOCKETED", "DOCKETED BY MISTAKE", match.group(1))
    else:
        return ""


def get_court_action_date(text: str) -> datetime | None:
    """Get Court Action Date from case text."""
    if match := re.search(r"Court Action Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_description(text: str) -> str:
    """Get Charge Description from case text."""
    if match := re.search(r"Charge: ([A-Z\.0-9\-\s]+)", text):
        return match.group(1).rstrip("C").strip()
    else:
        return ""


def get_jury_demand(text: str) -> str:
    """Get Jury Demand field from case text."""
    if match := re.search(r"Jury Demand: ([A-Za-z]+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_al_institutional_service_num(text: str) -> str:
    """Get AL Institutional Service Num from case text."""
    if match := re.search(r"(\d+)\s*\n\s*Youthful Date:", text):
        return match.group(1).strip()
    else:
        return ""


def get_inpatient_treatment_ordered(text: str) -> str:
    """Get Inpatient Treatment Ordered from case text."""
    if match := re.search(r"Inpatient Treatment Ordered: (YES|NO)", text):
        return match.group(1).strip()
    else:
        return ""


def get_trial_type(text: str) -> str:
    """Get Trial Type field from case text."""
    if match := re.search(r"Trial Type: ([A-Z\s]+)", text):
        return re.sub(r"[\s\n]*[PS]$", "", match.group(1)).strip()
    else:
        return ""


def get_judge(text: str) -> str:
    """Get Judge field from case text."""
    if match := re.search(r"Judge: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_probation_office_number(text: str) -> str:
    """Get Probation Office Number field from case text."""
    if match := re.search(r"Probation Office \#: ([0-9\-]+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_defendant_status(text: str) -> str:
    """Get Defendant Status field from case text."""
    if match := re.search(r"Defendant Status: ([A-Z\s]+)", text):
        return re.sub(r"[\s\n]+", " ", match.group(1).rstrip("J").strip())
    else:
        return ""


def get_arresting_officer(text: str) -> str:
    """Get Arresting Officer field from case text."""
    if match := re.search(r"Arresting Officer: (.+)", text):
        return match.group(1).rstrip("S").rstrip("P").strip()
    else:
        return ""


def get_arresting_agency_type(text: str) -> str:
    """Get Arresting Agency Type field from case text."""
    if match := re.search(r"([^0-9]+) Arresting Agency Type:", text):
        out = match.group(1)
        out = re.sub(r"^\-.+", "", out)
        out = re.sub(r"County\:", "", out)
        out = re.sub(r"Defendant Status\:", "", out)
        out = re.sub(r"Judge\:", "", out)
        out = re.sub(r"Trial Type\:", "", out)
        out = re.sub(r"Probation Office \#\:", "", out)
        return out.strip()
    else:
        return ""


def get_probation_office_name(text: str) -> str:
    """Get Probation Office Name field from case text."""
    if match := re.search(r"Probation Office Name: ([A-Z0-9]+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_traffic_citation_number(text: str) -> str:
    """Get Traffic Citation Number field from case text."""
    if match := re.search(r"Traffic Citation \#: ([A-Z0-9]+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_previous_dui_convictions(text: str) -> int | None:
    """Get Previous DUI Convictions field from case text."""
    if match := re.search(r"Previous DUI Convictions: (\d{3})", text):
        return int(match.group(1))
    else:
        return None


def get_case_initiation_type(text: str) -> str:
    """Get Case Initiation Type field from case text."""
    if match := re.search(r"Case Initiation Type: ([A-Z\s]+)", text):
        return match.group(1).rstrip("J").strip()
    else:
        return ""


def get_domestic_violence(text: str) -> str:
    """Get Domestic Violence field from case text."""
    if match := re.search(r"Domestic Violence: (YES|NO)", text):
        return match.group(1).strip()
    else:
        return ""


def get_agency_ori(text: str) -> str:
    """Get Agency ORI field from case text."""
    if match := re.search(r"Agency ORI: ([A-Z\s-]+)", text):
        if out := re.search(r"^(.*)", match.group(1)):
            return out.group(1).strip()
        else:
            return ""
    else:
        return ""


def get_driver_license_no(text: str) -> str:
    """Get Driver License No field from case text."""
    if match := re.search(r"Driver License N°: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_ssn(text: str) -> str:
    """Get SSN field from case text."""
    if match := re.search(r"([X\d]{3}\-[X\d]{2}-[X\d]{4})", text):
        return match.group(1).strip()
    else:
        return ""


def get_state_id(text: str) -> str:
    """Get State ID field from case text."""
    if match := re.search(r"([A-Z0-9]{11}?) State ID:", text):
        return match.group(1).strip()
    else:
        return ""


def get_weight(text: str) -> int | None:
    """Get Weight field from case text."""
    if match := re.search(r"Weight: (\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_height(text: str) -> str:
    """Get Height field from case text."""
    if match := re.search(r"Height : (\d'\d{2})", text):
        return match.group(1).strip() + '"'
    else:
        return ""


def get_eyes(text: str) -> str:
    """Get Eyes field from case text."""
    if match := re.search(r"Eyes/Hair: (\w{3})/(\w{3})", text):
        return match.group(1).strip()
    else:
        return ""


def get_hair(text: str) -> str:
    """Get Hair field from case text."""
    if match := re.search(r"Eyes/Hair: (\w{3})/(\w{3})", text):
        return match.group(2).strip()
    else:
        return ""


def get_warrant_issuance_date(text: str) -> datetime | None:
    """Get Warrant Issuance Date from case text."""
    if match := re.search(r"(\d\d?/\d\d?/\d\d\d\d) Warrant Issuance Date:", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_warrant_action_date(text: str) -> datetime | None:
    """Get Warrant Action Date from case text."""
    if match := re.search(r"Warrant Action Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_warrant_issuance_status(text: str) -> str:
    """Get Warrant Issuance Status field from case text."""
    if match := re.search(r"Warrant Issuance Status: (\w)", text):
        return match.group(1).strip()
    else:
        return ""


def get_warrant_action_status(text: str) -> str:
    """Get Warrant Action Status field from case text."""
    if match := re.search(r"Warrant Action Status: (\w)", text):
        return match.group(1)
    else:
        return ""


def get_warrant_location_status(text: str) -> str:
    """Get Warrant Location Status field from case text."""
    if match := re.search(r"Warrant Location Status: (\w)", text):
        return match.group(1)
    else:
        return ""


def get_warrant_issuance_description(text: str) -> str:
    """Get Warrant Issuance Description field from case text."""
    if descs := re.search(r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)", text):
        if match := re.search(
            r"(ALIAS WARRANT|BENCH WARRANT|FAILURE TO PAY WARRANT|PROBATION WARRANT)",
            descs.group(1),
        ):
            return match.group(1)
        else:
            return ""
    else:
        return ""


def get_warrant_action_description(text: str) -> str:
    """Get Warrant Action Description field from case text."""
    if descs := re.search(r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)", text):
        if match := re.search(
            r"(WARRANT RECALLED|WARRANT DELAYED|WARRANT RETURNED|WARRANT SERVED)",
            descs.group(1),
        ):
            return match.group(1)
        else:
            return ""
    else:
        return ""


def get_warrant_location_description(text: str) -> str:
    """Get Warrant Location Description field from case text."""
    if descs := re.search(r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)", text):
        if match := re.search(r"(CLERK'S OFFICE|LAW ENFORCEMENT)", descs.group(1)):
            return match.group(1)
        else:
            return ""
    else:
        return ""


def get_number_of_warrants(text: str) -> str:
    """Get Number Of Warrants from case text."""
    if match := re.search(r"Number Of Warrants: (\d{3}\s\d{3})", text):
        return match.group(1)
    else:
        return ""


def get_bond_type(text: str) -> str:
    """Get Bond Type field from case text."""
    if match := re.search(r"Bond Type: (\w)", text):
        return match.group(1)
    else:
        return ""


def get_bond_type_desc(text: str) -> str:
    """Get Bond Type Desc field from case text."""
    if match := re.search(r"Bond Type Desc: ([A-Z\s]+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_bond_amount(text: str) -> float | None:
    """Get Bond Amount field from case text."""
    if match := re.search(r"([\d\.]+) Bond Amount:", text):
        return float(re.sub(r"[^0-9\.\s]", "", match.group(1)).strip())
    else:
        return None


def get_surety_code(text: str) -> str:
    """Get Surety Code field from case text."""
    if match := re.search(r"Surety Code: (.+)", text):
        return re.sub(r"Release.+", "", match.group(1)).strip()
    else:
        return ""


def get_bond_release_date(text: str) -> datetime | None:
    """Get Bond Release Date from case text."""
    if match := re.search(r"Release Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_failed_to_appear_date(text: str) -> datetime | None:
    """Get Failed to Appear Date from case text."""
    if match := re.search(r"Failed to Appear Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_bondsman_process_issuance(text: str) -> datetime | None:
    """Get Bondsman Process Issuance from case text."""
    if match := re.search(
        r"Bondsman Process Issuance: ([^\n]*?) Bondsman Process Return:", text
    ):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    return None


def get_bondsman_process_return(text: str) -> datetime | None:
    """Get Bondsman Process Return field from case text."""
    if match := re.search(r"Bondsman Process Return: (.+)", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    return None


def get_appeal_date(text: str) -> datetime | None:
    """Get Appeal Date from case text."""
    if match := re.search(r"([\n\s/\d]*?) Appeal Court:", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    return None


def get_appeal_court(text: str) -> str:
    """Get Appeal Court from case text."""
    if match := re.search(r"([A-Z\-\s]+) Appeal Case Number", text):
        return match.group(1).strip()
    else:
        return ""


def get_origin_of_appeal(text: str) -> str:
    """Get Origin Of Appeal field from case text."""
    if match := re.search(r"Orgin Of Appeal: ([A-Z\-\s]+)", text):
        return match.group(1).rstrip("L").strip()
    else:
        return ""


def get_appeal_to_desc(text: str) -> str:
    """Get Appeal To Desc field from case text."""
    if match := re.search(r"Appeal To Desc: ([A-Z\-\s]+)", text):
        if out := re.search(r"^(.*)", match.group(1)):
            return out.group(1).strip()
        else:
            return ""
    else:
        return ""


def get_appeal_status(text: str) -> str:
    """Get Appeal Status field from case text."""
    if match := re.search(r"Appeal Status: ([A-Z\-\s]+)", text):
        return match.group(1).rstrip("A").strip()
    else:
        return ""


def get_appeal_to(text: str) -> str:
    """Get Appeal To field from case text."""
    if match := re.search(r"Appeal To: (\w?) Appeal", text):
        return match.group(1).strip()
    else:
        return ""


def get_lower_court_appeal_date(text: str) -> datetime | None:
    """Get Lower Court Appeal Date from case text."""
    if match := re.search(r"(.+)LowerCourt Appeal Date:", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1).strip(), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def get_disposition_date_of_appeal(text: str) -> datetime | None:
    """Get Disposition Date Of Appeal field from case text."""
    if match := re.search(r"Disposition Type Of Appeal: ([^A-Za-z]+)", text):
        try:
            return datetime.strptime(
                re.sub(r"[\n\s:\-]", "", match.group(1)).strip(), "%m/%d/%Y"
            )
        except ValueError:
            return None
    else:
        return None


def get_disposition_type_of_appeal(text: str) -> str:
    """Get Disposition Type Of Appeal field from case text."""
    if match := re.search(
        r"Disposition Date Of Appeal: (.+?) Disposition Type Of Appeal", text
    ):
        return match.group(1)
    else:
        return ""


def get_appeal_case_number(text: str) -> str:
    """Get Appeal Case Number field from case text."""
    if match := re.search(r"Appeal Case Number: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_transfer_reason(text: str) -> str:
    """Get Transfer Reason field from case text."""
    if match := re.search(r"Transfer Reason (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_admin_last_update(text: str) -> datetime | None:
    """Get Admin Last Update field from case text."""
    if match := re.search(
        r"(?s)Administrative Information.+?Last Update: (\d\d?/\d\d?/\d\d\d\d)",
        text,
    ):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_number_of_subpoenas(text: str) -> int | None:
    """Get Number Of Subpoenas field from case text."""
    if match := re.search(r"Number of Subponeas: (\d{3})", text):
        return int(match.group(1))
    else:
        return None


def get_admin_updated_by(text: str) -> str:
    """Get Admin Updated By field from case text."""
    if match := re.search(r"Updated By: (\w{3})", text):
        return match.group(1).strip()
    else:
        return ""


def get_transfer_to_admin_doc_date(text: str) -> datetime | None:
    """Get Transfer to Admin Doc Date from case text."""
    if match := re.search(r"(.+)Transfer to Admin Doc Date:", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def get_transfer_desc(text: str) -> str:
    """Get Transfer Desc field from case text."""
    if match := re.search(r"Transfer Desc: ([A-Z\s]{0,15}) \d\d?/\d\d?/\d\d\d\d", text):
        return match.group(1).strip()
    else:
        return ""


def get_continuance_date(text: str) -> datetime | None:
    """Get Continuance Date from case text."""
    if match := re.search(r"(?s)Continuance Date\s*\n*\s*(\d\d/\d\d/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_continuance_reason(text: str) -> str:
    """Get Continuance Reason field from case text."""
    if match := re.search(
        r"Continuance Reason\s*\n*\s*([A-Z0-9]{2}/[A-Z0-9]{2}/[A-Z0-9]{4})",
        text,
    ):
        return match.group(1)
    else:
        return ""


def get_continuance_description(text: str) -> str:
    """Get Continuance Description field from case text."""
    if match := re.search(r"Description:(.+?)Number of Previous Continuances:", text):
        return match.group(1).strip()
    else:
        return ""


def get_number_of_previous_continuances(text: str) -> int | None:
    """Get Number Of Previous Continuances field from case text."""
    if match := re.search(r"Number of Previous Continuances:\s*\n*\s(\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_tbnv1(text: str) -> datetime | None:
    """Get TBNV1 date from case text."""
    if match := re.search(r"Date Trial Began but No Verdict \(TBNV1\): ([^\n]+)", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1).strip(), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def get_tbnv2(text: str) -> datetime | None:
    """Get TBNV2 date from case text."""
    if match := re.search(r"Date Trial Began but No Verdict \(TBNV2\): ([^\n]+)", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1).strip(), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def get_turnover_date(text: str) -> datetime | None:
    """Get TurnOver Date from case text."""
    if match := re.search(r"TurnOver Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_turnover_amt(text: str) -> float | None:
    """Get TurnOver Amt field from case text."""
    if match := re.search(r"TurnOver Amt\: (\-?\$\d+\.\d\d)", text):
        return float(match.group(1).replace("$", ""))
    else:
        return None


def get_frequency_amt(text: str) -> float | None:
    """Get Frequency Amt field from case text."""
    if match := re.search(r"Frequency Amt\: (\-?\$\d+\.\d\d)", text):
        return float(match.group(1).replace("$", ""))
    else:
        return None


def get_due_date(text: str) -> datetime | None:
    """Get Due Date field from case text."""
    if match := re.search(r"Due Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_over_under_paid(text: str) -> float | None:
    """Get Over/Under Paid field from case text."""
    if match := re.search(r"Over/Under Paid: (\-?\$\d+.\d\d)", text):
        return float(match.group(1).replace("$", ""))
    else:
        return None


def get_last_paid_date(text: str) -> datetime | None:
    """Get Last Paid Date from case text."""
    if match := re.search(r"Last Paid Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_payor(text: str) -> str:
    """Get Payor field from case text."""
    if match := re.search(r"Payor\: ([A-Z0-9]{4})", text):
        return match.group(1)
    else:
        return ""


def get_enforcement_status(text: str) -> str:
    """Get Enforcement Status field from case text."""
    if match := re.search(r"Enforcement Status\: (.+)", text):
        raw = match.group(1).rstrip("F")
        raw = re.sub(r"\s*\n\s*", " ", raw)
        raw = re.sub(r"\s+", " ", raw)
        raw = re.sub(
            r"PRETRIAL/JAIL DIVERSON: PERMITS MAILERS, RECEIPTING,",
            "PRETRIAL/JAIL DIVERSON: PERMITS MAILERS, RECEIPTING, DA TURNOVE",
            raw,
        )
        return raw.strip()
    else:
        return ""


def get_frequency(text: str) -> str:
    """Get Frequency field from case text."""
    if match := re.search(r"Frequency\: ([W|M])", text):
        return re.sub(r"Cost Paid By\:", "", match.group(1))
    else:
        return ""


def get_placement_status(text: str) -> str:
    """Get Placement Status field from case text."""
    if match := re.search(r"Placement Status\: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_pretrial(text: str) -> str:
    """Get PreTrial field from case text."""
    if match := re.search(r"PreTrial\: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


def get_pretrial_date(text: str) -> datetime | None:
    """Get PreTrial Date from case text."""
    if match := re.search(r"PreTrail Date\: (.+)PreTrial", text):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def get_pretrial_terms(text: str) -> str:
    """Get PreTrial Terms field from case text."""
    if match := re.search(r"PreTrial Terms\: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


def get_pre_terms_date(text: str) -> datetime | None:
    """Get Pre Terms Date from case text."""
    if match := re.search(r"Pre Terms Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_delinquent(text: str) -> str:
    """Get Delinquent field from case text."""
    if match := re.search(r"Delinquent\: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


def get_delinquent_date(text: str) -> datetime | None:
    """Get Delinquent Date from case text."""
    if match := re.search(r"Delinquent Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_da_mailer(text: str) -> str:
    """Get DA Mailer field from case text."""
    if match := re.search(r"DA Mailer\: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


def get_da_mailer_date(text: str) -> datetime | None:
    """Get DA Mailer Date from case text."""
    if match := re.search(r"DA Mailer Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_warrant_mailer(text: str) -> str:
    """Get Warrant Mailer field from case text."""
    if match := re.search(r"Warrant Mailer\: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


def get_warrant_mailer_date(text: str) -> datetime | None:
    """Get Warrant Mailer Date from case text."""
    if match := re.search(r"Warrant Mailer Date\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_last_update(text: str) -> datetime | None:
    """Get Last Update field from case text."""
    if match := re.search(r"Last Update\: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_updated_by(text: str) -> str:
    """Get Updated By field from case text."""
    if match := re.search(r"Updated By\: ([A-Z]{3})", text):
        return match.group(1)
    else:
        return ""


def get_sentence_requirements_completed(text: str) -> list[str]:
    """Get Sentence Requirements Completed field from case text."""
    return re.findall(r"(?:Requrements Completed: )(YES|NO|UNKNOWN)", text)


def get_sentence_date(text: str) -> list[datetime]:
    """Get Sentence Date from case text."""
    out = []
    for x in re.findall(r"(?:Sentence Date: )(\d\d?/\d\d?/\d\d\d\d)", text):
        with suppress(ValueError):
            out += [datetime.strptime(x, "%m/%d/%Y")]
    return out


def get_jail_credit_period(text: str) -> list[datetime]:
    """Get Jail Credit Period field from case text."""
    out_strs = re.findall(r"(?s)([^\n]+)(?:\n\s*Probation Begin Date:)", text)
    out_strs = [re.sub(r"License.+", "", x) for x in out_strs]
    out_strs = [
        match.group(1)
        for x in out_strs
        if (match := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", x))
    ]
    out = []
    for x in out_strs:
        with suppress(ValueError):
            out += [datetime.strptime(x, "%m/%d/%Y")]
    return out


def get_sentence_provisions(text: str) -> list[str]:
    """Get Sentence Provisions field from case text."""
    return re.findall(r"(?:Sentence Provisions: )([YN])", text)


def get_sentence_start_date(text: str) -> list[datetime]:
    """Get Sentence Start Date from case text."""
    out = []
    for x in re.findall(r"(?:Sentence Start Date: )(\d\d?/\d\d?/\d\d\d\d)", text):
        with suppress(ValueError):
            out += [datetime.strptime(x, "%m/%d/%Y")]
    return out


def get_sentence_end_date(text: str) -> list[datetime]:
    """Get Sentence End Date from case text."""
    out = []
    for x in re.findall(r"(?:Sentence End Date: )(\d\d?/\d\d?/\d\d\d\d)", text):
        with suppress(ValueError):
            out += [datetime.strptime(x, "%m/%d/%Y")]
    return out


def get_probation_begin_date(text: str) -> list[datetime]:
    """Get Probation Begin Date from case text."""
    out = []
    for x in re.findall(
        (
            r"(?:License Susp Period: )(?:\d+ Years, \d+ Months, \d+"
            r" Days\.)?(?:\s*\n\s*)(\d\d/\d\d/\d\d\d\d)(?:\s*\n?\s*)(?:\d+"
            r" Years, \d+ Months, \d+ Days\.)?"
        ),
        text,
    ):
        with suppress(ValueError):
            out += [datetime.strptime(x, "%m/%d/%Y")]
    return out


def get_probation_period(text: str) -> list[str]:
    """Get Probation Period field from case text."""
    return [x.strip() for x in re.findall(r"(?:Probation Period\: )(.+)", text)]


def get_license_susp_period(text: str) -> list[str]:
    """Get License Susp Period field from case text."""
    return [x.strip() for x in re.findall(r"(?:License Susp Period\: )(.+)", text)]


def get_probation_revoke(text: str) -> list[datetime]:
    """Get Probation Revoke field from case text."""
    out = []
    for x in re.findall(r"(?:Probation Revoke: )(\d\d?/\d\d?/\d\d\d\d)", text):
        with suppress(ValueError):
            out += [datetime.strptime(x, "%m/%d/%Y")]
    return out


def get_balance_by_fee_code(text: str, code: str) -> float | None:
    """Get Balance for Fee Code from case text."""
    row_matches = [
        match.strip()
        for match in re.findall(rf"(I?N?ACTIVE[^\n]+? {code} [^\n]+)", text)
    ]
    value_matches = [
        match.group(1)
        for row in row_matches
        if (match := re.search(r"(\-?\$[\d,]+\.\d\d)$", row))
    ]
    values = [float(re.sub(r"[\$,]", "", match)) for match in value_matches]
    return sum(values) if len(values) > 0 else None


def get_amount_due_by_fee_code(text: str, code: str) -> float | None:
    """Get Amount Due for Fee Code from case text."""
    row_matches = [
        match.strip()
        for match in re.findall(rf"(I?N?ACTIVE[^\n]+? {code} [^\n]+)", text)
    ]
    value_matches = [
        match.group(3)
        for row in row_matches
        if (match := re.search(r"^(I?N?ACTIVE)?\s*([YN]?) (\-?\$[\d,]+\.\d\d)", row))
    ]
    values = [float(re.sub(r"[\$,]", "", match)) for match in value_matches]
    return sum(values) if len(values) > 0 else None


def get_amount_paid_by_fee_code(text: str, code: str) -> float | None:
    """Get Amount Paid for Fee Code from case text."""
    row_matches = [
        match.strip()
        for match in re.findall(rf"(I?N?ACTIVE[^\n]+? {code} [^\n]+)", text)
    ]
    value_matches = [
        match.group(4)
        for row in row_matches
        if (
            match := re.search(
                r"^(I?N?ACTIVE)?\s*([YN]?) (\-?\$[\d,]+\.\d\d) (\-?\$[\d,]+\.\d\d)", row
            )
        )
    ]
    values = [float(re.sub(r"[\$,]", "", match)) for match in value_matches]
    return sum(values) if len(values) > 0 else None


def get_amount_hold_by_fee_code(text: str, code: str) -> float | None:
    """Get Amount Hold for Fee Code from case text."""
    row_matches = [
        match.strip()
        for match in re.findall(rf"(I?N?ACTIVE[^\n]+? {code} [^\n]+)", text)
    ]
    value_matches = [
        match.group(5)
        for row in row_matches
        if (
            match := re.search(
                r"^(I?N?ACTIVE)?\s*([YN]?) (\-?\$[\d,]+\.\d\d) (\-?\$[\d,]+\.\d\d)"
                r" (\-?\$[\d,]+\.\d\d)",
                row,
            )
        )
    ]
    values = [float(re.sub(r"[\$,]", "", match)) for match in value_matches]
    return sum(values) if len(values) > 0 else None


def get_suspension_date(text: str) -> datetime | None:
    """Get Suspension Date from case text."""
    if match := re.search(r"Suspension Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_speed(text: str) -> int | None:
    """Get Speed field from case text."""
    if match := re.search(r"Speed: (\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_completion_date(text: str) -> datetime | None:
    """Get Completion Date from case text."""
    if match := re.search(r"Completion Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_clear_date(text: str) -> datetime | None:
    """Get Clear Date from case text."""
    if match := re.search(r"Clear Date: (\d\d?/\d\d?/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_speed_limit(text: str) -> int | None:
    """Get Speed Limit field from case text."""
    if match := re.search(r"Speed Limit: (\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_blood_alcohol_content(text: str) -> float | None:
    """Get Blood Alcohol Content field from case text."""
    if match := re.search(
        (
            r"Blood Alcohol Content: Completion Date: ?(\d\d?/\d\d?/\d\d\d\d)?"
            r" (\d+\.\d\d\d)"
        ),
        text,
    ):
        return float(match.group(2))
    else:
        return None


def get_ticket_number(text: str) -> str:
    """Get Ticket Number field from case text."""
    if match := re.search(r"Ticket Number: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_rule_20(text: str) -> str:
    """Get Rule 20 field from case text."""
    if match := re.search(r"Rule 20: (.+?) Clear Date:", text):
        return match.group(1).strip()
    else:
        return ""


def get_collection_status(text: str) -> str:
    """Get Collection Status field from case text."""
    if match := re.search(
        r"(?s)Collection Status: (.+?) \d\d?/\d\d?/\d\d\d\d",
        text,
    ):
        out = match.group(1).strip()
        out = re.sub(r"\n", "", out)
        out = re.sub(r"\s+", " ", out)
        out = re.sub(r"DOB:.+", "", out)
        out = out.strip()
        return out
    else:
        return ""


def get_vehicle_desc(text: str) -> str:
    """Get Vehicle Desc field from case text."""
    if match := re.search(r"Tag Number: (.+?) Vehicle Desc:", text):
        return match.group(1).strip()
    else:
        return ""


def get_vehicle_state(text: str) -> int | None:
    """Get Vehicle State field from case text."""
    if match := re.search(r"Vehicle State: (\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_driver_license_class(text: str) -> str:
    """Get Driver License Class field from case text."""
    if match := re.search(r"Driver License Class: (.+)", text):
        return re.sub(r"/.+", "", match.group(1)).strip()
    else:
        return ""


def get_commercial_vehicle(text: str) -> str:
    """Get Commercial Vehicle field from case text."""
    if match := re.search(r"Commercial Vehicle: (YES|NO|UNKNOWN)", text):
        return match.group(1)
    else:
        return ""


def get_tag_number(text: str) -> str:
    """Get Tag Number field from case text."""
    if match := re.search(r"([A-Z0-9]+) Tag Number:", text):
        return match.group(1)
    else:
        return ""


def get_vehicle_year(text: str) -> str:
    """Get Vehicle Year field from case text."""
    if match := re.search(r"Vehicle Year: (.+?) ?Vehicle State:", text):
        return match.group(1).strip()
    else:
        return ""


def get_passengers_present(text: str) -> str:
    """Get Passengers Present field from case text."""
    if match := re.search(r"(YES|NO) Passengers Present:", text):
        return match.group(1)
    else:
        return ""


def get_commercial_driver_license_required(text: str) -> str:
    """Get Commercial Driver License Required field from case text."""
    if match := re.search(r"Commercial Driver License Required: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


def get_hazardous_materials(text: str) -> str:
    """Get Hazardous Materials field from case text."""
    if match := re.search(r"Hazardous Materials: (YES|NO)", text):
        return match.group(1)
    else:
        return ""


# TABLE ROW GET FUNCTIONS


def get_attorneys(text: str) -> list[str]:
    """Get Attorneys from case text."""
    if match := re.search(r"(?s)Attorney Code\s*\n\s*(.+?)Warrant", text):
        raw = re.sub(r"Alt Name:.+", "", match.group(1))
        raw = re.sub(r"[A-Z\s]+Name:.+", "", raw)
        raw = re.sub(r"(?s)(City|Race|Type|DOB|Index):.+", "", raw)
        split = re.split(r"(\s[A-Z0-9]{6}\s+\n)", raw)
        split = [re.sub("\n", "", x) for x in split]
        split = [re.sub(r"\s+", " ", x) for x in split]
        split = [x.strip() for x in split]
        col1 = split[::2][:-1]
        col2 = split[1::2]
        return [f"{col1[i]} {col2[i]}" for i in range(len(col1))]
    else:
        return []


def get_case_action_summary(text: str) -> list[str]:
    """Get case action summary from case text."""
    if match := re.search(r"(?s)Case Action Summary(.+) Date", text):
        table_text = re.sub(r"\s*\n\s*Operator\s*", "", match.group(1))
        table_text = re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", table_text)
        split_rows = re.split(r"(\d\d?/\d\d?/\d\d\d\d)\s*\n", table_text)
        col1 = split_rows[::2][:-1]
        col1 = [row.strip() for row in col1]
        col2 = split_rows[1::2]
        return [f"{col1[i]} {col2[i]}" for i in range(len(col1))]
    else:
        return []


def get_images(text: str) -> list[str]:
    """Get images from case text."""
    if match := re.search(r"(?s)Images(.+)END OF THE REPORT", text):
        table_text = re.sub(r"\n Pages\s*", "", match.group(1))
        table_text = re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", table_text)
        table_text = re.sub(r"Date: Description Doc# Title  \n Images", "", table_text)
        table_text = re.sub(r"^[\n\s]*", "", table_text)
        table_text = re.sub(r"[\n\s]*$", "", table_text)
        split_rows = re.split(r"(\d\d?:\d\d:\d\d [AP]M)", table_text)
        col1 = split_rows[::2][:-1]
        col1 = [x.replace("\n", "").strip() for x in col1]
        col2 = split_rows[1::2]
        return [f"{col1[i]} {col2[i]}" for i in range(len(col1))]
    else:
        return []


def get_central_disbursement_division(text: str) -> list[str]:
    """Get Alabama Central Disbursement Division table rows from case text."""
    if match := re.search(
        r"(?s)Alabama Central Disbursement Division(.+?)(Requesting Party|Date:)", text
    ):
        table_text = re.sub(
            r"  \n Description From Party To Party Emp Party Reason Disbursement"
            r" Accoun  \n Transaction Batch  \n Operator  \n ",
            "",
            match.group(1),
        )
        table_text = re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", table_text)
        table_text = re.sub(r"\s*\n\s*$", "", table_text)
        split_rows = re.split(r"(\d\d?/\d\d?/\d\d\d\d)", table_text)
        col1 = split_rows[::2][1:]
        col1 = [re.sub(r"\n", "", x) for x in col1]
        col1 = [re.sub(r"\s+", " ", x).strip() for x in col1]
        col2 = split_rows[1::2]
        return [f"{col2[i]} {col1[i]}" for i in range(len(col1))]
    else:
        return []


def get_witnesses(text: str) -> list[str]:
    """Get witnesses from case text."""
    if match := re.search(
        r"(?s)SJIS Witness List\s*\n\s*Date Issued\s*\n\s*Subpoena(.+?)Date",
        text,
    ):
        table_str = re.sub(
            r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", match.group(1)
        )
        table_str = re.sub(r"Requesting Party Witness # Name", "", table_str)
        split_rows = re.split(r"( [A-Z0-9]{4}\s*\n)", table_str)
        col1 = [x.replace("\n", "").strip() for x in split_rows[::2][:-1]]
        col1 = [re.sub(r"\s+", " ", x) for x in col1]
        col2 = [x.replace("\n", "").strip() for x in split_rows[1::2]]
        return [f"{col2[i]} {col1[i]}" for i in range(len(col1))]
    else:
        return []


def get_financial_history(text: str) -> list[str]:
    """Get financial history from case text."""
    if match := re.search(r"(?s)Financial History(.+?)Requesting Party", text):
        table_text = match.group(1)
        table_text = re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", table_text)
        table_text = re.sub(
            (
                r"(?s)\s*\n Description From Party To Party Admin Fee\s*\n\s*Money"
                r" Type\s*\n\s*Reason Disbursement Accoun\s*\n\s*Transaction"
                r" Batch\s*\n\s*Operator\s*\n\s*"
            ),
            "",
            table_text,
        )
        table_text = re.sub(
            (
                r"(?s)\s*Transaction Date\s*\n\s*Attorney Receipt Number Amount"
                r" Description"
                r" From Party To Party Admin Fee\s*\n\s*Money Type\s*\n\s*Reason"
                r" Disbursement Accoun\s*\n\s*Transaction Batch\s*\n\s*Operator\s*\n\s*"
            ),
            "",
            table_text,
        )
        table_text = re.sub(r"(?s)\s*\n\s*SJIS Witness List\s*\n\s*", "", table_text)
        rows = re.split(r"(\d\d/\d\d/\d\d\d\d)", table_text)
        col1 = [row.replace("\n", "") for row in rows[::2][1:]]
        col1 = [re.sub(r"\s+", " ", row).strip() for row in col1]
        col2 = rows[1::2]
        return [f"{col2[i]} {col1[i]}" for i in range(len(col1))]
    else:
        return []


def get_continuances(text: str) -> list[str]:
    """Get continuances from case text."""
    if match := re.search(
        r"(?s)Continuances.+?Comments\s*\n(.+?)\s*\n\s*Court Action", text
    ):
        clean_text = re.sub(r"(?s)Parties.+", "", match.group(1))
        split_text = re.split(
            r"(\d\d?/\d\d?/\d\d\d\d \d\d?:\d\d?:\d\d [AP]M)", clean_text
        )
        col1 = [x.replace("\n", "").strip() for x in split_text[::2][1:]]
        col2 = split_text[1::2]
        return [f"{col2[i]} {col1[i]}" for i in range(len(col1))]
    else:
        return []


def get_restitution(text: str) -> list[str]:
    """Get restitution from case text."""
    all_tables = re.findall(r"(?s)Restitution (.+?) (?:Programs|Split)", text)
    all_tables = [
        re.sub(r"Recipient Description Amount\s*\n\s*", "", x) for x in all_tables
    ]
    all_tables = [
        re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", x) for x in all_tables
    ]
    all_tables = [re.sub(r"Restitution\s*\n\s*", "", x) for x in all_tables]
    all_tables = [re.sub(r"(?s)Linked Cases.+", "", x) for x in all_tables]
    all_tables = [re.sub(r"\s*\n\s*$", "", x) for x in all_tables]
    all_tables = [re.sub(r"Chain Gang.+", "", x) for x in all_tables]
    all_tables = [re.sub(r"(?s)Enhanced.+", "", x) for x in all_tables]
    all_tables = [x for x in all_tables if re.search(r"^\w+ \d+ ", x)]
    all_tables = [x.split("\n") for x in all_tables]
    all_tables = [item for sublist in all_tables for item in sublist]
    all_tables = [x for x in all_tables if re.search(r"^\w+ \d+ ", x)]
    return [x.strip() for x in all_tables]


def get_linked_cases(text: str) -> list[str]:
    """Get linked cases from case text."""
    all_tables = re.findall(
        (
            r"(?s)Linked Cases\s*\n\s*Sentencing Number Case Type Case Type Description"
            r" CaseNumber(.+?)Enforcement|Sentence"
        ),
        text,
    )
    all_tables = [re.sub("(?s)Sentence.+", "", x) for x in all_tables]
    all_tables = [re.sub(r"^\s*\n\s*", "", x) for x in all_tables]
    all_tables = [re.sub(r"\s*\n\s*$", "", x) for x in all_tables]
    all_tables = [
        re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", x) for x in all_tables
    ]
    all_tables = [x for x in all_tables if re.search(r"[A-Z]", x)]
    all_tables = [x.split("\n") for x in all_tables]
    all_tables = [item for sublist in all_tables for item in sublist]
    all_tables = [x.strip() for x in all_tables]
    return [x for x in all_tables if re.search(r"[A-Z]", x)]


def get_settings(text: str) -> list[str]:
    """Get settings from case text."""
    if match := re.search(r"(?s)Description\:\s*\n\s*Settings(.+?)Court Action", text):
        clean_match = re.sub(r"^\s+\n\s*", "", match.group(1))
        clean_match = re.sub(r"\s*\n\s*$", "", clean_match)
        clean_match = re.sub(r"(?s)(Parties|Continuances).+", "", clean_match)
        clean_match = re.sub(
            r"\s*Date: Que: Time: Description:\s*\n\s*", "", clean_match
        )
        clean_match = re.sub(r"(?s)\s*\n\s*Date Time.+", "", clean_match)
        return [row.strip() for row in clean_match.split("\n")]
    else:
        return []


def get_filing_charges(text: str) -> list[str]:
    """Get filing charges from case text."""
    if match := re.search(r"(?s)Filing Charges(.+?)Disposition Charges", text):
        table_text = re.sub(
            r"\n\s*# Code Description Cite Type Description Category ID Class\s*\n\s*",
            "",
            match.group(1),
        )
        table_text = re.sub(r"^[\s\n]+", "", table_text)
        table_text = re.sub(r"[\s\n]+$", "", table_text)
        table_text = re.sub(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "", table_text)
        split_rows = re.split(
            (
                r"(?m)(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG"
                r"|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER"
                r"|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET"
                r"|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)\s*$"
            ),
            table_text,
        )
        col1 = split_rows[::2][:-1]
        col1 = [row.replace("\n", "").strip() for row in col1]
        col1 = [re.sub(r"\s+", " ", row) for row in col1]
        col2 = split_rows[1::2]
        return [f"{col1[i]} {col2[i]}".strip() for i in range(len(col1))]
    else:
        return []


def get_disposition_charges(text: str) -> list[str]:
    """Get disposition charges from case text."""
    if match := re.search(
        r"(?s)Disposition Charges (.+?) (Sentences|Enforcement)", text
    ):
        table_text = match.group(1)
        table_text = re.sub(
            r"# Code Court Action Category Cite Court Action Date\s*\n\s*",
            "",
            table_text,
        )
        table_text = re.sub(
            r"Type Description Description Class ID\s*\n\s*", "", table_text
        )
        table_text = re.sub(
            r"(..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+)", "", table_text
        )
        table_text = re.sub(r"^[\s\n]+", "", table_text)
        table_text = re.sub(r"[\s\n]+$", "", table_text)
        split_rows = re.split(r"(?m)^\s*(\d{3}) ", table_text)
        col1 = split_rows[::2][1:]
        col2 = split_rows[1::2]
        rows = [f"{col2[i]} {col1[i]}" for i in range(len(col1))]
        return [re.sub(r"[\s\n]+", " ", row).strip() for row in rows]
    else:
        return []


# NON-CRIMINAL CASE FIELDS


def get_style(text: str) -> str:
    """Get Style from case text."""
    if match := re.search(r"(?s)[A-Z]{2}-\d{4}-\d{6}\.\d\d\s*\n([^\n]+)", text):
        return re.sub(r"(\s+)", " ", match.group(1).strip())
    else:
        return ""


def get_filed_date(text: str) -> datetime | None:
    """Get Filed field from case text."""
    if match := re.search(r"Filed: (\d\d/\d\d/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_no_of_plaintiffs(text: str) -> int | None:
    """Get No of Plaintiffs field from case text."""
    if match := re.search(r"(\d+) No of Plaintiffs:", text):
        return int(match.group(1))
    else:
        return None


def get_no_of_defendants(text: str) -> int | None:
    """Get No of Plaintiffs field from case text."""
    if match := re.search(r"No of Defendants: (\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_case_status(text: str) -> str:
    """Get Case Status field from case text."""
    if match := re.search(r"Case Status: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_track(text: str) -> str:
    """Get Track field from case text."""
    if match := re.search(r"Track: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_case_type(text: str) -> str:
    """Get Case Type field from case text."""
    if match := re.search(r"(.+) Case Type: ", text):
        return re.sub(r"Filed: (\d\d/\d\d/\d\d\d\d)?", "", match.group(1)).strip()
    else:
        return ""


def get_appellate_case(text: str) -> int | None:
    """Get Appellate Case field from case text."""
    if match := re.search(r"Appellate Case: (\d+)", text):
        return int(match.group(1))
    else:
        return None


def get_damage_amt(text: str) -> float | None:
    """Get Damage Amt field from case text."""
    if match := re.search(r"Damage Amt: ([\d\.]+)", text):
        return float(match.group(1))
    else:
        return None


def get_punitive_damages(text: str) -> float | None:
    """Get Punitive Damages field from case text."""
    if match := re.search(r"([\d\.]+) Punitive Damages:", text):
        return float(match.group(1))
    else:
        return None


def get_compensatory_damages(text: str) -> float | None:
    """Get Compensatory Damages field from case text."""
    if match := re.search(r"([\d\.]+) Compensatory Damages:", text):
        return float(match.group(1))
    else:
        return None


def get_general_damages(text: str) -> float | None:
    """Get General Damages field from case text."""
    if match := re.search(r"General Damages: ([\d\.]+)", text):
        return float(match.group(1))
    else:
        return None


def get_no_damages(text: str) -> str:
    """Get No Damages field from case text."""
    if match := re.search(r"No Damages: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_payment_frequency(text: str) -> str:
    """Get Payment Frequency field from case text."""
    if match := re.search(r"Payment Frequency: (\w) ", text):
        return match.group(1).strip()
    else:
        return ""


def get_cost_paid_by(text: str) -> str:
    """Get Cost Paid By field from case text."""
    if match := re.search(r"Cost Paid By: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_court_action_code(text: str) -> str:
    """Get Court Action Code field from case text."""
    if match := re.search(r"(.+) Court Action Code:", text):
        return match.group(1).strip()
    else:
        return ""


def get_num_of_trial_days(text: str) -> int | None:
    """Get Num of Trial days field from case text."""
    if match := re.search(r"Num of Trial days: (.+)", text):
        return int(match.group(1).strip())
    else:
        return None


def get_court_action_desc(text: str) -> str:
    """Get Court Action Desc field from case text."""
    if match := re.search(r"Court Action Desc: (.+?) Court Action Date", text):
        return match.group(1).strip()
    else:
        return ""


def get_judgment_for(text: str) -> str:
    """Get Judgment For field from case text."""
    if match := re.search(r"Judgment For: (.+?)Num", text):
        return match.group(1).strip()
    else:
        return ""


def get_disposition_judge(text: str) -> str:
    """Get Disposition Judge field from case text."""
    if match := re.search(r"Disposition Judge:(.+)", text):
        return re.sub(r"Minstral.+", "", match.group(1)).strip()
    else:
        return ""


def get_minstral(text: str) -> datetime | None:
    """Get Minstral field from case text."""
    if match := re.search(r"Minstral: (\d\d/\d\d/\d\d\d\d)", text):
        try:
            return datetime.strptime(match.group(1), "%m/%d/%Y")
        except ValueError:
            return None
    else:
        return None


def get_comment_1(text: str) -> str:
    """Get Comment 1 field from case text."""
    if match := re.search(r"(.+) Comment 1:", text):
        return match.group(1).strip()
    else:
        return ""


def get_comment_2(text: str) -> str:
    """Get Comment 1 field from case text."""
    if match := re.search(r"(.+) Comment 2:", text):
        return match.group(1).strip()
    else:
        return ""


def get_origin_of_case(text: str) -> str:
    """Get Origin of Case field from case text."""
    if match := re.search(r"Orgin of Case: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_support(text: str) -> str:
    """Get Support field from case text."""
    if match := re.search(r"Support: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_uifsa(text: str) -> str:
    """Get UIFSA field from case text."""
    if match := re.search(r"(.+) UIFSA:", text):
        return match.group(1).strip()
    else:
        return ""


def get_adc(text: str) -> str:
    """Get ADC field from case text."""
    if match := re.search(r"ADC: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_contempt(text: str) -> str:
    """Get Contempt field from case text."""
    if match := re.search(r"Contempt: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_legal_separation(text: str) -> str:
    """Get Legal Separation field from case text."""
    if match := re.search(r"Legal Separation: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_annulment(text: str) -> str:
    """Get Annulment field from case text."""
    if match := re.search(r"Annulment: (.+)", text):
        return match.group(1).strip()
    else:
        return ""


def get_dna_test(text: str) -> str:
    """Get DNA Test field from case text."""
    if match := re.search(r"(.+)Modification:", text):
        return match.group(1).strip()
    else:
        return ""


def get_arrearage(text: str) -> str:
    """Get Arrearage field from case text."""
    if match := re.search(r"Arrearage: (.+?)Garnishment:", text):
        return match.group(1).strip()
    else:
        return ""


def get_paternity(text: str) -> str:
    """Get Paternity field from case text."""
    if match := re.search(r"Paternity: (.)", text):
        return match.group(1).strip()
    else:
        return ""


def get_income_withholding_order(text: str) -> str:
    """Get Income Withholding Order field from case text."""
    if match := re.search(r"Imcome Withholding Order: (.+?) Paternity:", text):
        return match.group(1)
    else:
        return ""


def get_first_date(text: str) -> datetime | None:
    """Get First Date field from case text."""
    if match := re.search(
        r"(?s)Department of Human Resources(.+?)(Parties|Settings)", text
    ):
        if date := re.search(r"(\d\d?/\d\d?/\d\d\d\d)", match.group(1)):
            try:
                return datetime.strptime(date.group(1), "%m/%d/%Y")
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def get_custody(text: str) -> str:
    """Get Custody field from case text."""
    if match_1 := re.search(r"(?s)Orgin of Case:[^\n]+\n([^\n]+)", text):
        if match_2 := re.search(r"([A-Z]-[A-Z]+)", match_1.group(1)):
            return match_2.group(1)
        else:
            return ""
    else:
        return ""


def get_no_of_children(text: str) -> int | None:
    """Get No of Children field from case text."""
    if match_1 := re.search(
        r"(?s)Department of Human Resources(.+?)(Parties|Settings)", text
    ):
        if match_2 := re.search(r"\d\d?/\d\d?/\d\d\d\d (\d+)", match_1.group(1)):
            return int(match_2.group(1))
        else:
            return None
    else:
        return None


def get_parties(text: str) -> list[str]:
    """Get Party Descriptions from case text."""
    matches = re.findall(r"(Party \d+ - .+)", text)
    return [
        match.replace("DOB:", "").replace("Alt Name:", "").strip() for match in matches
    ]

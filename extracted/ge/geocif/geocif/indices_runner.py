"""CID Indices Pipeline Runner.

Computes Climatic Impact Driver (CID) indices from EO/climate data
for each country, crop, and season using ICCLIM via multiprocessing.

Usage::

    from geocif import indices_runner
    indices_runner.run(cfg_geocif)
"""

import ast
import logging
import warnings
from multiprocessing import Pool, cpu_count
from pathlib import Path

import arrow as ar
import pandas as pd
from tqdm.rich import tqdm

warnings.filterwarnings("ignore")

from .cid import indices
from geocif import utils as ut
from geoprepare import base

logger = logging.getLogger(__name__)


def _require_country_option(parser, country, option) -> str:
    """
    Read ``option`` from the country-specific config section, falling back to
    the DEFAULT section. Raises if neither has the option.

    Args:
        parser: ConfigParser instance.
        country: Country name (any case/spacing).
        option: Config option name to read.

    Returns:
        The option value as a string.

    Raises:
        ValueError: If neither section has the option.
    """
    country_lower = country.lower().replace(" ", "_")
    if parser.has_section(country_lower) and parser.has_option(country_lower, option):
        return parser.get(country_lower, option)
    if parser.has_option("DEFAULT", option):
        return parser.get("DEFAULT", option)
    raise ValueError(
        f"{option} not specified for country {country} in config file."
    )


def _get_country_option(parser, country, option, default: str) -> str:
    """
    Like ``_require_country_option`` but returns ``default`` when the option is
    missing from both sections. Always returns a ``str``.
    """
    country_lower = country.lower().replace(" ", "_")
    if parser.has_section(country_lower) and parser.has_option(country_lower, option):
        return parser.get(country_lower, option)
    if parser.has_option("DEFAULT", option):
        return parser.get("DEFAULT", option)
    return default


def get_admin_zone(country, parser) -> str:
    """Return the admin level (e.g. "adm1") for ``country``."""
    return _require_country_option(parser, country, "admin_level")


def get_crops(country, parser):
    """Return the list of crops configured for ``country``."""
    return ast.literal_eval(_require_country_option(parser, country, "crops"))


def get_seasons(country, parser, crop=None):
    """Return the list of harvest seasons for ``country``.

    If ``seasons`` is configured, use it directly.  Otherwise auto-detect
    from the crop calendar Excel file by checking which season sheets have
    positive calendar values for this country/crop.  Falls back to ``[1]``
    when neither config nor calendar data is available.
    """
    raw = _get_country_option(parser, country, "seasons", default="")
    if raw:
        return ast.literal_eval(raw)

    # Auto-detect from crop calendar file
    if crop is not None:
        from pathlib import Path
        from geocif import utils as ut

        dir_calendars = Path(parser.get("PATHS", "dir_crop_calendars"))
        calendar_file = _get_country_option(parser, country, "calendar_file", default="")
        if calendar_file:
            calendar_path = dir_calendars / calendar_file
            country_display = country.replace("_", " ").title()
            detected = ut.detect_seasons_from_calendar(
                calendar_path, country_display, crop
            )
            logger.info(f"Auto-detected seasons {detected} for {country} {crop} from {calendar_file}")
            return detected

    return [1]


def get_max_forecast_season(parser, countries) -> int:
    """Max year listed in any country's ``forecast_seasons`` (0 if none).

    Used to extend the CID year range one year past today when a configured
    forecast season has not started yet (pre-season forecasting from
    forecast-only CIDs, e.g. south_africa maize 2027 launched in Sep 2026).
    """
    max_year = 0
    for country in countries:
        raw = _get_country_option(parser, country, "forecast_seasons", default="")
        if not raw:
            continue
        try:
            seasons = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            continue
        if seasons:
            try:
                max_year = max(max_year, max(int(s) for s in seasons))
            except (TypeError, ValueError):
                continue
    return max_year


def get_input_file_path(country, parser, data_source="harvest") -> Path:
    """
    Resolve the input directory for ``country`` based on ``data_source``:
      - ``harvest``: ``${PATHS:dir_output}/{project_name}[/crop_t{floor}|crop_p{ceil}]/{country}/``
      - ``agmet``:   ``${input_file_path}/{country}/`` (country-specific override wins)

    Geoprepare names its output subdir per the active crop-mask mode
    (geoprepare ``base.py``: ``crop_t{floor}`` when ``threshold = True``,
    ``crop_p{ceil}`` when ``threshold = False``), so we mirror the same
    branching here. Legacy configs without the ``threshold`` option fall
    through to the bare ``{project_name}/{country}/`` layout.
    """
    country_lower = country.lower().replace(" ", "_")

    if data_source == "harvest":
        dir_output = parser.get("PATHS", "dir_output")
        project_name = parser.get("DEFAULT", "project_name")
        if parser.has_option("DEFAULT", "threshold"):
            if parser.getboolean("DEFAULT", "threshold"):
                floor = parser.getint("DEFAULT", "floor")
                return Path(f"{dir_output}/{project_name}/crop_t{floor}/{country_lower}")
            ceil = parser.getint("DEFAULT", "ceil")
            return Path(f"{dir_output}/{project_name}/crop_p{ceil}/{country_lower}")
        return Path(f"{dir_output}/{project_name}/{country_lower}")

    base_path = _require_country_option(parser, country, "input_file_path")
    return Path(f"{base_path}/{country_lower}")


class cid_runner(base.BaseGeo):
    def __init__(self, path_config_file):
        super().__init__(path_config_file)

        # Parse configuration files
        self.parse_config()

        # Get data_source from config (default: 'harvest')
        if self.parser.has_option("DEFAULT", "data_source"):
            self.data_source = self.parser.get("DEFAULT", "data_source").lower()
        else:
            self.data_source = "harvest"
        
        # Validate data_source
        if self.data_source not in ["harvest", "agmet"]:
            raise ValueError(f"Invalid data_source: {self.data_source}. Must be 'harvest' or 'agmet'.")

        # Get base input path from DEFAULT section (for agmet mode)
        if self.parser.has_option("DEFAULT", "input_file_path"):
            self.base_dir = Path(self.parser.get("DEFAULT", "input_file_path"))
        elif self.data_source == "agmet":
            raise ValueError("input_file_path not specified in DEFAULT section of config file (required for agmet mode).")
        
        if self.parser.has_option("DEFAULT", "do_parallel_indices"):
            self.do_parallel = self.parser.getboolean("DEFAULT", "do_parallel_indices")
        else:
            self.do_parallel = False

        if self.parser.has_option("DEFAULT", "fraction_cpus"):
            self.fraction_cpus = self.parser.getfloat("DEFAULT", "fraction_cpus")
        else:
            self.fraction_cpus = 0.75
        
        # Read countries and methods from config file
        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.method = self.parser.get("DEFAULT", "method")
        self.stage_mode = self.parser.get("DEFAULT", "stage_mode", fallback="cumulative")

    _FILE_COLUMNS = ["directory", "path", "filename", "admin_zone"]

    def collect_files_harvest(self):
        """
        Collect files for 'harvest' data source.
        Reads specific files with pattern: ``{country}_{crop}_s{season}.csv``
        from ``${PATHS:dir_output}/{project_name}/crop_t{floor}/{country}/``.
        """
        rows = []

        for country in self.countries:
            country_lower = country.lower().replace(" ", "_")
            country_path = get_input_file_path(country, self.parser, data_source="harvest")

            crops = get_crops(country, self.parser)
            admin_zone = get_admin_zone(country, self.parser)

            for crop in crops:
                seasons = get_seasons(country, self.parser, crop=crop)
                for season in seasons:
                    filename = f"{country_lower}_{crop}_s{season}.csv"
                    filepath = country_path / filename

                    if filepath.exists():
                        rows.append({
                            "directory": "countries",
                            "path": filepath,
                            "filename": filename,
                            "admin_zone": admin_zone,
                        })
                    else:
                        logger.warning(f"Expected file not found: {filepath}")

        return pd.DataFrame(rows, columns=self._FILE_COLUMNS)

    def collect_files_agmet(self):
        """
        Collect files for 'agmet' data source.
        Recursively finds all CSV files in the input directory.
        """
        rows = []

        def _add_from(search_root):
            for filepath in search_root.rglob("*.csv"):
                country_name = filepath.parents[0].name
                # HACK: Skip korea for now, as it is giving errors
                if country_name == "republic_of_korea":
                    continue
                rows.append({
                    "directory": filepath.parents[1].name,
                    "path": filepath,
                    "filename": filepath.name,
                    "admin_zone": get_admin_zone(country_name, self.parser),
                })

        if self.countries and self.countries != ["all"]:
            for country in self.countries:
                _add_from(get_input_file_path(country, self.parser, data_source="agmet"))
        else:
            _add_from(self.base_dir)

        return pd.DataFrame(rows, columns=self._FILE_COLUMNS)

    def collect_files(self):
        """
        Collect files based on ``self.data_source``:

        1. ``harvest``: reads the fixed set of ``{country}_{crop}_s{season}.csv``
           files from the extraction output directory.
        2. ``agmet``: recursively globs all CSVs under the agmet input path.

        :return: DataFrame with columns ``[directory, path, filename, admin_zone]``.
        """
        if self.data_source == "harvest":
            return self.collect_files_harvest()
        return self.collect_files_agmet()

    def process_combinations(self, df, method):
        """
        Build a deduplicated list of ``(directory, path, filename, admin_zone, method)``
        tuples from ``df``. These are the file-level task descriptors for the
        main loop; one tuple per unique CSV file.

        :param df:
        :param method:
        :return:
        """
        return list({
            (row["directory"], row["path"], row["filename"], row["admin_zone"], method)
            for _, row in df.iterrows()
        })

    def main(self):
        """
        Three-phase pipeline:
        1. Discover regions per file (sequential preprocessing).
        2. Build flat (file, year, region) task list.
        3. Execute all tasks via multiprocessing.Pool (or sequentially).
        Main process handles CSV output writing (serial, no race conditions).
        """
        # Create a dataframe of the files to be analyzed
        df_files = self.collect_files()

        if df_files.empty:
            logger.warning(
                f"No files found for data_source='{self.data_source}' "
                f"and countries={self.countries}"
            )
            return

        # Extract unique crops from filenames by stripping the known country prefix
        crops_found = set()
        for _, row in df_files.iterrows():
            fname = row["filename"].rsplit("_s", 1)[0]  # e.g. "south_africa_maize"
            for country in self.countries:
                prefix = country.lower().replace(" ", "_") + "_"
                if fname.startswith(prefix):
                    crops_found.add(fname[len(prefix):])
                    break
        crops_found = sorted(crops_found)

        num_cpu = max(1, int(cpu_count() * self.fraction_cpus)) if self.do_parallel else 0
        combinations = self.process_combinations(df_files, self.method)
        # Earliest harvest year to include. Configurable via [DEFAULT]
        # start_year (fallback 2001 to preserve the historical floor for
        # configs that don't set it).
        start_year = self.parser.getint("DEFAULT", "start_year", fallback=2001)
        end_year = ar.utcnow().year
        # Extend one year forward when any country's forecast_seasons asks
        # for a season that has not started yet (pre-season forecasting from
        # S2S/FLDAS forecast leads). Capped at current_year + 1: forecast
        # leads reach ~6 months out, so no later season can have any data.
        max_fs = get_max_forecast_season(self.parser, self.countries)
        if max_fs > end_year:
            end_year = min(max_fs, ar.utcnow().year + 1)
            logger.info(
                f"forecast_seasons includes {max_fs} -> extending CID year "
                f"range through {end_year} (future-season pre-season mode)"
            )
        years = list(range(start_year, end_year + 1))

        # ── Phase 1: Discover regions per file ──
        file_regions = {}
        for combo in tqdm(combinations, desc="Discovering regions", unit="file"):
            status, path, filename, admin_zone, category = combo
            regions = indices.discover_regions(
                self.parser, status, path, filename, admin_zone, category, "ndvi"
            )
            file_regions[combo] = regions

        # ── Phase 2: Build flat (file, year, region) task list ──
        # Skip old years (< current_year - 1) that already have output files,
        # unless redo is True.  This mirrors manage_existing_files() logic that
        # used to live inside _run_one_year.
        current_year = pd.Timestamp.now().year
        flat_tasks = []
        skipped_years = 0
        for combo, regions in file_regions.items():
            if not regions:
                continue
            status, path, filename, admin_zone, category = combo
            # Build a CIDs instance once per file to get output paths
            crop, season = ut.get_crop_season(filename)
            country = regions[0][0].lower().replace(" ", "_")
            obj_probe = indices.CIDs(
                parser=self.parser, process_type=status, file_path=path,
                file_name=filename, admin_zone=admin_zone, method=category,
                harvest_year=years[0], redo=False,
            )
            obj_probe.crop = crop
            obj_probe.season = season
            obj_probe.country = country
            obj_probe.prepare_directories()

            # Future years apply only to countries whose own
            # forecast_seasons ask for them (pre-season mode) -- one
            # country's 2027 must not spawn no-op tasks for every other
            # country in the config.
            country_max_fs = get_max_forecast_season(self.parser, [country])

            for year in years:
                # Check skip logic: old years with existing output
                if year < (current_year - 1):
                    out_fname = f"{country}_{crop}_s{season}_{year}.csv"
                    out_path = obj_probe.dir_output / out_fname
                    if out_path.is_file():
                        skipped_years += 1
                        continue
                if year > current_year:
                    if year > country_max_fs:
                        continue
                    # Remove a stale future-season CSV from a previous run
                    # up front: the append protocol only deletes on first
                    # WRITE, so an all-empty rerun would otherwise leave
                    # last run's forecasts in place. (The legacy
                    # _run_one_year path already deletes up front.)
                    out_path = (obj_probe.dir_output
                                / f"{country}_{crop}_s{season}_{year}.csv")
                    if out_path.is_file():
                        out_path.unlink()
                for region in regions:
                    flat_tasks.append(indices.ProcessTaskArgs(
                        parser=self.parser,
                        process_type=status,
                        file_path=path,
                        file_name=filename,
                        admin_zone=admin_zone,
                        method=category,
                        year=year,
                        region=region,
                        vi_var="ndvi",
                        redo=False,
                        stage_mode=self.stage_mode,
                    ))
        if skipped_years:
            logger.info(f"Skipped {skipped_years} file-year combos (output already exists)")

        total_regions = sum(len(r) for r in file_regions.values())
        avg_per_worker = (
            f"~{len(flat_tasks) // max(num_cpu, 1)}"
            if self.do_parallel and num_cpu else "n/a (serial)"
        )
        ut.display_run_summary("Producing Climatic Impact-Drivers", [
            ("Countries", self.countries),
            ("Crops", crops_found if crops_found else ["(from filenames)"]),
            ("Files", str(len(combinations))),
            ("Year range",
                f"{years[0]}-{years[-1]} ({len(years)} years)" if years else "(empty)"),
            ("start_year (config)",
                str(self.parser.getint("DEFAULT", "start_year", fallback=2001))),
            ("Regions", str(total_regions)),
            ("Total tasks", str(len(flat_tasks))),
            ("Skipped (output exists)", str(skipped_years)),
            ("Tasks per worker (avg)", avg_per_worker),
            ("Data source", self.data_source),
            ("Method", self.method),
            ("Stage mode", self.stage_mode),
            ("Output dir", str(self.dir_output)),
            ("Parallel", str(self.do_parallel)),
            ("CPUs", str(num_cpu) if self.do_parallel else "0"),
        ], wait=20)

        # ── Phase 3: Execute tasks ──
        # Track which output files have been started so we delete stale data
        # on first write (previously done per-year in _run_one_year).
        started_outputs: set = set()

        def _write_result(output_path_str: str, df_result) -> None:
            if not output_path_str or df_result.empty:
                return
            out = Path(output_path_str)
            if output_path_str not in started_outputs:
                # First write for this output file — delete stale data
                if out.exists():
                    out.unlink()
                started_outputs.add(output_path_str)
            write_header = not out.exists()
            df_result.to_csv(out, index=False, mode="a", header=write_header)

        if self.do_parallel:
            with Pool(num_cpu) as p:
                pbar = tqdm(total=len(flat_tasks), desc="CID", unit="task", mininterval=2)
                for output_path_str, df_result, task_desc in p.imap_unordered(
                    indices.process_task, flat_tasks
                ):
                    pbar.set_description(task_desc)
                    pbar.update(1)
                    _write_result(output_path_str, df_result)
                pbar.close()
        else:
            pbar = tqdm(flat_tasks, desc="CID", unit="task", mininterval=5)
            for task in pbar:
                pbar.set_description(
                    f"{task.file_name} | {task.year} | {task.region[1]}"
                )
                output_path_str, df_result, _ = indices.process_task(task)
                _write_result(output_path_str, df_result)


def run(path_config_files=[]):
    """Entry point: validate index definitions and run the indices pipeline."""
    # Sanity-check index definitions have no spaces in keys
    indices.validate_index_definitions()

    obj = cid_runner(path_config_files)

    from geocif.data import ensure_metadata
    ensure_metadata(obj.parser)

    # Iterate over methods from config file
    obj.main()


if __name__ == "__main__":
    run()
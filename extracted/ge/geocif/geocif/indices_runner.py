import ast
import logging
import warnings
from multiprocessing import Pool, cpu_count
from pathlib import Path

import arrow as ar
import pandas as pd
from tqdm import tqdm

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


def get_seasons(country, parser):
    """Return the list of harvest seasons for ``country`` (defaults to ``[1]``)."""
    return ast.literal_eval(
        _get_country_option(parser, country, "seasons", default="[1]")
    )


def get_input_file_path(country, parser, data_source="harvest") -> Path:
    """
    Resolve the input directory for ``country`` based on ``data_source``:
      - ``harvest``: ``${PATHS:dir_output}/{project_name}[/crop_t{floor}]/{country}/``
      - ``agmet``:   ``${input_file_path}/{country}/`` (country-specific override wins)
    """
    country_lower = country.lower().replace(" ", "_")

    if data_source == "harvest":
        dir_output = parser.get("PATHS", "dir_output")
        project_name = parser.get("DEFAULT", "project_name")
        if parser.has_option("DEFAULT", "threshold") and parser.getboolean("DEFAULT", "threshold"):
            floor = parser.getint("DEFAULT", "floor")
            return Path(f"{dir_output}/{project_name}/crop_t{floor}/{country_lower}")
        return Path(f"{dir_output}/{project_name}/{country_lower}")

    base_path = _require_country_option(parser, country, "input_file_path")
    return Path(f"{base_path}/{country_lower}")


class cei_runner(base.BaseGeo):
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
        
        # Read countries and methods from config file
        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.method = self.parser.get("DEFAULT", "method")

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
            seasons = get_seasons(country, self.parser)
            admin_zone = get_admin_zone(country, self.parser)

            for crop in crops:
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
                        logger.warning("Expected file not found: %s", filepath)

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

        :param method:
        :return:
        """
        # Create a dataframe of the files to be analyzed
        df_files = self.collect_files()
        
        if df_files.empty:
            logger.warning(
                "No files found for data_source='%s' and countries=%s",
                self.data_source,
                self.countries,
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

        num_cpu = int(cpu_count() * 0.75) if self.do_parallel else 0
        params = [
            ("Countries", self.countries),
            ("Crops", crops_found if crops_found else ["(from filenames)"]),
            ("Data source", self.data_source),
            ("Method", self.method),
            ("Parallel", str(self.do_parallel)),
        ]
        if self.do_parallel:
            params.append(("CPUs", str(num_cpu)))
        ut.display_run_summary("Producing Climatic Impact-Drivers", params, wait=20)

        combinations = self.process_combinations(df_files, self.method)

        # One task per file, covering all harvest years in a single call so the
        # ICCLIM result cache inside process_file amortizes icclim.index calls
        # across years (~25x speedup on the cached path). The redo flag is
        # False here; process_file / CEIs still force recomputation for the
        # current and previous harvest years regardless.
        years = list(range(2001, ar.utcnow().year + 1))
        tasks = [
            (
                self.parser,
                status,
                path,
                filename,
                admin_zone,
                category,
                years,
                "ndvi",
                False,  # redo
            )
            for status, path, filename, admin_zone, category in combinations
        ]
        # Note: countries have already been filtered at collect_files_* time;
        # no redundant post-filter on `i[3].lower()` needed.

        if self.do_parallel:
            with Pool(num_cpu) as p:
                for _ in tqdm(
                    p.imap_unordered(indices.process_file, tasks),
                    total=len(tasks),
                    desc="CEI files",
                ):
                    pass
        else:
            pbar = tqdm(tasks, desc="CEI files")
            for val in pbar:
                pbar.set_description(f"Main loop {val[3]} {val[5]}")
                indices.process_file(val)


def run(path_config_files=[]):
    """Entry point: validate index definitions and run the indices pipeline."""
    # Sanity-check index definitions have no spaces in keys
    indices.validate_index_definitions()

    obj = cei_runner(path_config_files)

    from geocif.data import ensure_metadata
    ensure_metadata(obj.parser)

    # Iterate over methods from config file
    obj.main()


if __name__ == "__main__":
    run()
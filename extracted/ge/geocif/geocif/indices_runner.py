import itertools
import warnings
import ast
from multiprocessing import Pool, cpu_count
from pathlib import Path

import arrow as ar
import pandas as pd
from tqdm import tqdm

warnings.filterwarnings("ignore")

from .cid import indices
from geocif import utils as ut
from geoprepare import base

# Show usage info on import
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console()
_table = Table(show_header=False, box=None, padding=(0, 1))
_table.add_column(style="bold cyan", no_wrap=True)
_table.add_column()
_table.add_row("Usage", "from geocif import indices_runner; indices_runner.run(cfg)")
_table.add_row("cfg", "\\[geobase.txt, countries.txt, crops.txt, geocif.txt]")
_console.print(Panel(_table, title="[bold bright_white]GeoCIF Indices Runner[/]", border_style="bright_blue", padding=(1, 2)))


def remove_duplicates(lst):
    """

    :param lst:
    :return:
    """
    return list(set([i for i in lst]))


def get_admin_zone(country, parser):
    """
    Get admin zone and admin column name from config file for the given country.
    Falls back to DEFAULT section if not specified for country.
    
    :param country: Country name
    :param parser: ConfigParser object
    :return: tuple of (admin_zone, admin_col_name)
    """
    country = country.title().replace(" ", "_")
    country_lower = country.lower()
    
    # Try to get admin_level from country-specific section
    if parser.has_section(country_lower) and parser.has_option(country_lower, "admin_level"):
        admin_zone = parser.get(country_lower, "admin_level")
    # Fall back to DEFAULT section
    elif parser.has_option("DEFAULT", "admin_level"):
        admin_zone = parser.get("DEFAULT", "admin_level")
    else:
        raise ValueError(f"admin_level not specified for country {country} in config file.")
    
    # admin_col_name is legacy (replaced by config-driven shapefile column mapping);
    # kept for backwards compatibility but no longer required.
    if parser.has_section(country_lower) and parser.has_option(country_lower, "admin_col_name"):
        admin_col_name = parser.get(country_lower, "admin_col_name")
    elif parser.has_option("DEFAULT", "admin_col_name"):
        admin_col_name = parser.get("DEFAULT", "admin_col_name")
    else:
        admin_col_name = "ADM1_NAME"
    
    return admin_zone, admin_col_name


def get_crops(country, parser):
    """
    Get crops list from config file for the given country.
    Falls back to DEFAULT section if not specified for country.
    
    :param country: Country name
    :param parser: ConfigParser object
    :return: list of crops
    """
    country_lower = country.lower().replace(" ", "_")
    
    # Try to get crops from country-specific section
    if parser.has_section(country_lower) and parser.has_option(country_lower, "crops"):
        crops_str = parser.get(country_lower, "crops")
    # Fall back to DEFAULT section
    elif parser.has_option("DEFAULT", "crops"):
        crops_str = parser.get("DEFAULT", "crops")
    else:
        raise ValueError(f"crops not specified for country {country} in config file.")
    
    return ast.literal_eval(crops_str)


def get_seasons(country, parser):
    """
    Get seasons list from config file for the given country.
    Falls back to DEFAULT section if not specified for country.
    Default is [1] if not specified anywhere.
    
    :param country: Country name
    :param parser: ConfigParser object
    :return: list of seasons (integers)
    """
    country_lower = country.lower().replace(" ", "_")
    
    # Try to get seasons from country-specific section
    if parser.has_section(country_lower) and parser.has_option(country_lower, "seasons"):
        seasons_str = parser.get(country_lower, "seasons")
        return ast.literal_eval(seasons_str)
    # Fall back to DEFAULT section
    elif parser.has_option("DEFAULT", "seasons"):
        seasons_str = parser.get("DEFAULT", "seasons")
        return ast.literal_eval(seasons_str)
    # Final fallback - default to season 1
    else:
        return [1]


def get_input_file_path(country, parser, data_source="harvest"):
    """
    Get input file path from config file for the given country.
    Path depends on data_source flag:
        - 'harvest': ${PATHS:dir_output}/{project_name}/crop_t{floor}/{country}/
        - 'agmet': ${PATHS:dir_crop_inputs}/processed/{country}/
    
    :param country: Country name
    :param parser: ConfigParser object
    :param data_source: 'harvest' or 'agmet'
    :return: Path object for input files
    """
    country_lower = country.lower().replace(" ", "_")
    
    if data_source == "harvest":
        # Use dir_output/{project_name}/{dir_threshold}/{country}/ path
        # project_name and dir_threshold come from geoextract.txt config
        dir_output = parser.get("PATHS", "dir_output")
        project_name = parser.get("DEFAULT", "project_name")
        if parser.has_option("DEFAULT", "threshold") and parser.getboolean("DEFAULT", "threshold"):
            floor = parser.getint("DEFAULT", "floor")
            path_str = f"{dir_output}/{project_name}/crop_t{floor}/{country_lower}"
        else:
            path_str = f"{dir_output}/{project_name}/{country_lower}"
    else:
        # Use agmet path - check country-specific first, then DEFAULT
        if parser.has_section(country_lower) and parser.has_option(country_lower, "input_file_path"):
            path_str = parser.get(country_lower, "input_file_path")
        elif parser.has_option("DEFAULT", "input_file_path"):
            path_str = parser.get("DEFAULT", "input_file_path")
        else:
            raise ValueError(f"input_file_path not specified for country {country} in config file.")
        
        # Append country subdirectory for agmet
        path_str = f"{path_str}/{country_lower}"
    
    return Path(path_str)


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

    def collect_files_harvest(self):
        """
        Collect files for 'harvest' data source.
        Reads specific files with pattern: {country}_{crop}_s{season}.csv
        from ${PATHS:dir_output}/{project_name}/crop_t{floor}/{country}/
        
        :return: DataFrame with file information
        """
        df_files = pd.DataFrame(columns=["directory", "path", "filename", "admin_zone", "admin_col_name"])
        
        for country in self.countries:
            country_lower = country.lower().replace(" ", "_")
            country_path = get_input_file_path(country, self.parser, data_source="harvest")
            
            # Get crops and seasons for this country
            crops = get_crops(country, self.parser)
            seasons = get_seasons(country, self.parser)
            
            # Get admin_zone and admin_col_name from config file
            admin_zone, admin_col_name = get_admin_zone(country, self.parser)
            
            for crop in crops:
                for season in seasons:
                    # Construct expected filename
                    filename = f"{country_lower}_{crop}_s{season}.csv"
                    filepath = country_path / filename
                    
                    if filepath.exists():
                        # For harvest mode, directory is 'countries'
                        process_type = "countries"
                        
                        # Add to dataframe
                        df_files.loc[len(df_files)] = [
                            process_type, 
                            filepath, 
                            filename, 
                            admin_zone, 
                            admin_col_name
                        ]
                    else:
                        print(f"Warning: Expected file not found: {filepath}")
        
        return df_files

    def collect_files_agmet(self):
        """
        Collect files for 'agmet' data source.
        Recursively finds all CSV files in the processed directory.
        
        :return: DataFrame with file information
        """
        df_files = pd.DataFrame(columns=["directory", "path", "filename", "admin_zone", "admin_col_name"])
        
        # If specific countries are defined, check their paths individually
        if self.countries and self.countries != ['all']:
            for country in self.countries:
                country_path = get_input_file_path(country, self.parser, data_source="agmet")
                
                # Go up one level since get_input_file_path now includes country
                # and we want to search from the country directory
                for filepath in country_path.rglob("*.csv"):
                    country_name = filepath.parents[0].name

                    # Get admin_zone and admin_col_name from config file
                    admin_zone, admin_col_name = get_admin_zone(country_name, self.parser)

                    # HACK: Skip korea for now, as it is giving errors
                    if country_name == "republic_of_korea":
                        continue

                    # Get name of directory one level up
                    process_type = filepath.parents[1].name

                    # Get name of file
                    filename = filepath.name

                    # Add to dataframe
                    df_files.loc[len(df_files)] = [process_type, filepath, filename, admin_zone, admin_col_name]
        else:
            # Use base directory for all countries
            for filepath in self.base_dir.rglob("*.csv"):
                country = filepath.parents[0].name

                # Get admin_zone and admin_col_name from config file
                admin_zone, admin_col_name = get_admin_zone(country, self.parser)

                # HACK: Skip korea for now, as it is giving errors
                if country == "republic_of_korea":
                    continue

                # Get name of directory one level up
                process_type = filepath.parents[1].name

                # Get name of file
                filename = filepath.name

                # Add to dataframe
                df_files.loc[len(df_files)] = [process_type, filepath, filename, admin_zone, admin_col_name]

        # Exclude those rows where directory is processed and file is already in
        # processed_include_fall directory
        no_fall = df_files["directory"] == "processed"
        include_fall = df_files[df_files["directory"] == "processed_include_fall"][
            "filename"
        ]

        df_files = df_files[~(no_fall & (df_files["filename"].isin(include_fall)))]

        return df_files

    def collect_files(self):
        """
        Collect files based on data_source configuration.
        
        1. If data_source='harvest': Read specific files {country}_{crop}_s{season}.csv
           from ${PATHS:dir_output}/{project_name}/crop_t{floor}/{country}/
        2. If data_source='agmet': Recursively find all CSVs in processed directory
        
        :return: DataFrame with columns: directory, path, filename, admin_zone, admin_col_name
        """
        if self.data_source == "harvest":
            return self.collect_files_harvest()
        else:
            return self.collect_files_agmet()

    def process_combinations(self, df, method):
        """
        Create a list of tuples of the following:
            - directory: name of directory where file is located
            - path: full path to file
            - filename: name of file
            - method: whether to compute indices for phenological stages or not
        This tuple will be used as input to the `process` function
        :param df:
        :param method:
        :return:
        """
        combinations = []

        for index, row in tqdm(df.iterrows()):
            combinations.extend(
                list(
                    itertools.product([row["directory"]], [row["path"]], [row["filename"]], [row["admin_zone"]], [method])
                )
            )

        combinations = remove_duplicates(combinations)

        return combinations

    def main(self):
        """

        :param method:
        :return:
        """
        # Create a dataframe of the files to be analyzed
        df_files = self.collect_files()
        
        if df_files.empty:
            print(f"No files found for data_source='{self.data_source}' and countries={self.countries}")
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

        # Add an element to the tuple to indicate the season
        # Last element is redo flag which is True if the analysis is to be redone
        # and False otherwise. Analysis is always redone for the current year
        # and last year whether file exists or not
        combinations = [
            (
                self.parser,
                status,
                path,
                filename,
                admin_zone,
                category,
                year,
                "ndvi",
                False,  # redo
            )
            for year in range(2001, ar.utcnow().year + 1)
            for status, path, filename, admin_zone, category in combinations
        ]

        # Filter combinations based on countries from config file
        if self.countries and self.countries != ['all']:
            combinations = [
                i
                for i in combinations
                if any(country.lower().replace(" ", "_") in i[3].lower() 
                       for country in self.countries)
            ]

        if self.do_parallel:
            with Pool(num_cpu) as p:
                for i, _ in enumerate(p.imap_unordered(indices.process, combinations)):
                    pass
        else:
            # Use the code below if you want to test without parallelization or
            # if you want to debug by using pdb
            pbar = tqdm(combinations)
            for i, val in enumerate(pbar):
                pbar.set_description(
                    f"Main loop {combinations[i][2]} {combinations[i][5]}"
                )
                indices.process(val)


def run(path_config_files=[]):
    """

    Args:
        path_config_files:

    Returns:

    """
    """ Check dictionary keys to have no spaces"""
    indices.validate_index_definitions()

    obj = cei_runner(path_config_files)

    from geocif.data import ensure_metadata
    ensure_metadata(obj.parser)

    # Iterate over methods from config file
    obj.main()


if __name__ == "__main__":
    run()
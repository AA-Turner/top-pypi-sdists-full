"""Configuration loader for the production_analysis (BEAST) pipeline.

Reads the ``[BEAST]`` section of a geocif config file (typically
``geocif.txt``) and returns a :class:`SimpleNamespace` with typed values.

Pass either a single config path or a list of paths.  When multiple paths
are given, later files override earlier ones (matching ConfigParser's
``read`` semantics), and ``${PATHS:...}`` interpolation works across files
so ``geobase.txt + geocif.txt`` resolves correctly.
"""
import ast
import configparser
from pathlib import Path
from types import SimpleNamespace


def load_config(path_config_file):
    """Parse the ``[BEAST]`` section into a typed namespace."""
    if isinstance(path_config_file, (list, tuple)):
        paths = [str(p) for p in path_config_file]
    else:
        paths = [str(path_config_file)]

    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    parser.read(paths)

    s = "BEAST"
    # Optional input_csv — required when input_format=hvstat, ignored
    # (with a logged warning at the call site) when input_format=amis.
    input_csv = (
        Path(parser.get(s, "input_csv"))
        if parser.has_option(s, "input_csv") and parser.get(s, "input_csv").strip()
        else None
    )
    cfg = SimpleNamespace(
        input_csv=input_csv,
        # Loader switch: 'hvstat' (default, reads cfg.input_csv) or 'amis'
        # (reads per-crop XLSX workbooks under
        # ${PATHS:dir_production_statistics} matching the configured
        # countries × crops × seasons set).
        input_format=parser.get(s, "input_format", fallback="hvstat").strip().lower(),
        # AMIS path needs the production_statistics directory; hvstat
        # ignores this. Read from [PATHS] (resolved via ExtendedInterpolation).
        dir_production_statistics=(
            Path(parser.get("PATHS", "dir_production_statistics"))
            if parser.has_section("PATHS")
               and parser.has_option("PATHS", "dir_production_statistics")
            else None
        ),
        output_dir=Path(parser.get(s, "output_dir")),
        min_years=parser.getint(s, "min_years", fallback=15),
        tcp_minmax=ast.literal_eval(parser.get(s, "tcp_minmax", fallback="[0, 8]")),
        tseg_minlength=parser.getint(s, "tseg_minlength", fallback=5),
        mcmc_seed=parser.getint(s, "mcmc_seed", fallback=42),
        strong_cp_threshold=parser.getfloat(s, "strong_cp_threshold", fallback=0.5),
        top_n_crops_heatmap=parser.getint(s, "top_n_crops_heatmap", fallback=12),
        sens_n_high=parser.getint(s, "sens_n_high", fallback=150),
        sens_n_med=parser.getint(s, "sens_n_med", fallback=250),
        sens_n_low=parser.getint(s, "sens_n_low", fallback=100),
        sens_n_none=parser.getint(s, "sens_n_none", fallback=100),
        sens_configs=ast.literal_eval(parser.get(s, "sens_configs")),
        example_series=ast.literal_eval(parser.get(s, "example_series")),
        # Stage-toggle flags consumed by production_runner
        run_detection=parser.getboolean(s, "run_detection", fallback=True),
        run_plots=parser.getboolean(s, "run_plots", fallback=True),
        run_sensitivity=parser.getboolean(s, "run_sensitivity", fallback=True),
        run_spatial=parser.getboolean(s, "run_spatial", fallback=False),
        # Spatial co-occurrence analysis: path to a multi-country admin
        # boundary shapefile (e.g. GAUL or country-specific shp). When
        # unset and run_spatial=True, falls back to
        # ${PATHS:dir_boundary_files}/gaul2014_admin1.shp.
        boundary_shp=(
            Path(parser.get(s, "boundary_shp"))
            if parser.has_option(s, "boundary_shp")
               and parser.get(s, "boundary_shp").strip()
            else None
        ),
    )
    cfg.parser = parser  # carried through for beast_spatial's per-country boundary lookups
    cfg.output_dir.mkdir(exist_ok=True, parents=True)
    return cfg

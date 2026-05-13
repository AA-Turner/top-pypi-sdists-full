import logging
import os
import sys
from pathlib import Path

import arrow as ar
import logzero


class TqdmStreamHandler(logging.StreamHandler):
    """StreamHandler that writes via `tqdm.write` so log lines don't tear
    an active progress bar in the same process. Falls back to plain write
    if tqdm isn't around."""

    def emit(self, record):
        try:
            msg = self.format(record)
            try:
                from tqdm import tqdm as std_tqdm
                std_tqdm.write(msg, file=self.stream)
            except Exception:
                self.stream.write(msg + self.terminator)
                self.flush()
        except Exception:
            self.handleError(record)


def read_config(path_config_file):
    """

    Args:
        path_config_file ():

    Returns:

    """
    from configparser import ConfigParser, ExtendedInterpolation

    parser = ConfigParser(
        inline_comment_prefixes=(";",), interpolation=ExtendedInterpolation()
    )

    # Normalize to list so we can check each file
    paths = path_config_file if isinstance(path_config_file, (list, tuple)) else [path_config_file]
    missing = [str(p) for p in paths if not Path(p).is_file()]
    if missing:
        raise FileNotFoundError(
            f"Config file(s) not found: {missing}"
        )

    try:
        parser.read(paths)
    except Exception as e:
        raise IOError(f"Cannot read {path_config_file}: {e}")

    if not parser.sections():
        raise ValueError(
            f"No sections found after reading config files: {[str(p) for p in paths]}"
        )

    return parser


class Logger:
    # adapted from https://gist.github.com/empr/2036153
    # Level	    Numeric value
    # CRITICAL	      50
    # ERROR	          40
    # WARNING	      30
    # INFO	          20
    # DEBUG	          10
    # NOTSET	       0
    def __init__(
        self,
        dir_log,  # Path to the directory where the log file will be saved
        project="geoprepare",  # Name of the project, this will be created as a subdirectory in dir_log
        file="logger.txt",  # Name of the log file
        level=logging.INFO,  # Logging level (see above)
    ):
        log_format = "[%(asctime)s] %(message)s"
        dir_log = Path(dir_log) / project / ar.now().format("MMMM_DD_YYYY")
        os.makedirs(dir_log, exist_ok=True)

        self.logger = logzero.setup_logger(
            name=file,
            logfile=dir_log / file,
            formatter=logzero.LogFormatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M"),
            maxBytes=int(1e6),  # 1 MB size
            backupCount=3,
            level=level,
        )

        # Replace logzero's stderr StreamHandler with a tqdm-aware variant
        # so log warnings don't tear an active progress bar. Leave the
        # rotating file handler alone (FileHandler is a StreamHandler too,
        # hence the explicit FileHandler exclusion).
        for h in list(self.logger.handlers):
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler):
                new_h = TqdmStreamHandler(h.stream)
                new_h.setLevel(h.level)
                new_h.setFormatter(h.formatter)
                self.logger.removeHandler(h)
                self.logger.addHandler(new_h)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


def get_logging_level(level):
    """

    Args:
        level:

    Returns:

    """
    if level == "DEBUG":
        return logging.DEBUG
    elif level == "INFO":
        return logging.INFO
    elif level == "WARNING":
        return logging.WARNING
    elif level == "ERROR":
        return logging.ERROR
    else:
        return logging.INFO


def _check_project_name_consistency(path_config_file):
    """
    Verify project_name in [DEFAULT] matches across all config files.

    Mismatched project_name causes geocif to read merged CSVs from a
    different path than where geoprepare wrote them — silently producing
    empty/missing data. Raise loudly so the user fixes the config.
    """
    from configparser import ConfigParser

    paths = path_config_file if isinstance(path_config_file, (list, tuple)) else [path_config_file]
    seen: dict = {}  # {project_name: first_file_that_set_it}
    for p in paths:
        cp = ConfigParser(inline_comment_prefixes=(";",))
        try:
            cp.read(str(p))
        except Exception:
            continue
        # ConfigParser auto-promotes DEFAULT keys; check if explicitly defined
        if not cp.has_option("DEFAULT", "project_name"):
            continue
        name = cp.get("DEFAULT", "project_name")
        if name not in seen:
            seen[name] = str(p)

    if len(seen) > 1:
        details = "\n".join(f"  {p}: project_name = {n}" for n, p in seen.items())
        raise ValueError(
            f"project_name mismatch across config files:\n{details}\n"
            f"Geocif reads merged CSVs from outputs/{{project_name}}/... — "
            f"if files disagree, the path will be wrong and data will be missing.\n"
            f"Fix: set project_name to the same value in all configs above."
        )


def setup_logger_parser(path_config_file, name_project="geocif", name_file="ml"):
    """

    Args:
        path_config_file:
        name_project:
        name_file:
        level:

    Returns:

    """
    _check_project_name_consistency(path_config_file)
    parser = read_config(path_config_file)
    dir_logs = parser.get("PATHS", "dir_logs")
    level = parser.get("LOGGING", "log_level", fallback="INFO")
    level = get_logging_level(level)

    logger = Logger(
        dir_log=dir_logs,
        project=name_project,
        file=name_file,
        level=level,
    )

    return logger, parser

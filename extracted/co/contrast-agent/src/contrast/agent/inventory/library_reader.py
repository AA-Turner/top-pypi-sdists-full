# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections import defaultdict
from contextlib import suppress
import time
from types import ModuleType
from collections.abc import Iterable
from contrast_vendor import importlib_metadata
import threading

from contrast.agent.scope import contrast_scope
from contrast_fireball import Library, LibraryObservation
from contrast.reporting import Reporter
from contrast.utils.patch_utils import get_loaded_modules
from contrast.utils.libraries import (
    distributions,
    get_hash,
    get_module_distribution_metadata,
    normalize_file_name,
)
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

IMPORTABLE_FILE_SUFFIXES = (".py", ".so")
CONTRAST_DIST_NAMES = (
    "contrast-agent",
    "contrast-agent-lib",
    "contrast-fireball",
    "contrast-agent-bundle",
)


def try_distribution(name: str) -> importlib_metadata.Distribution | None:
    with suppress(importlib_metadata.PackageNotFoundError):
        return importlib_metadata.distribution(name)
    return None


CONTRAST_DIST_HASHES = tuple(
    get_hash(dist.name, dist.version)
    for name in CONTRAST_DIST_NAMES
    if (dist := try_distribution(name))
)


class LibraryReader:
    """
    LibraryReader is responsible for reading and reporting the installed libraries
    in the running environment.
    """

    def __init__(self, reporter: Reporter) -> None:
        self.reporter = reporter
        self.analysis_thread = threading.Thread(
            target=self._read_distribution_packages, daemon=True
        )

    def start(self) -> None:
        self.analysis_thread.start()

    @contrast_scope()
    def _read_distribution_packages(self) -> None:
        """
        Reads every installed distribution package and reports it as a Library.
        """
        logger.debug("Analyzing libraries...")

        libraries = self.discover_libraries()
        self._report_discovered_libraries(libraries)

        observations = self.observed_libraries()
        self._report_observed_libraries(observations)

    def discover_libraries(self) -> list[Library]:
        """
        Reads every installed distribution package and returns it as a Library.
        """
        return [
            library
            for dist in distributions()
            if (library := library_from_distribution(dist))
        ]

    def _report_discovered_libraries(self, libraries: list[Library]) -> None:
        reportable_libraries = [
            library for library in libraries if library.file not in CONTRAST_DIST_NAMES
        ]
        if not reportable_libraries:
            return

        logger.debug(
            "Reporting discovered libraries",
            count=len(reportable_libraries),
            discovered_libraries=[
                f"{lib.file} - {lib.version}" for lib in reportable_libraries
            ],
        )
        self.reporter.new_libraries(reportable_libraries)

    def observed_libraries(self) -> list[LibraryObservation]:
        """
        Reads every loaded module and returns it as a LibraryObservation.
        """
        return LibraryObservations(get_loaded_modules().values()).to_list()

    def _report_observed_libraries(
        self, observations: list[LibraryObservation]
    ) -> None:
        reportable_observations = [
            observation
            for observation in observations
            if observation.library_hash not in CONTRAST_DIST_HASHES
        ]
        if not reportable_observations:
            return

        logger.debug(
            "Reporting observed libraries",
            count=len(reportable_observations),
            used_libraries=[
                f"{obs.library_hash} - {obs.names}" for obs in reportable_observations
            ],
        )
        self.reporter.new_library_observations(reportable_observations)


def library_from_distribution(
    dist: importlib_metadata.Distribution,
) -> Library | None:
    """
    Returns a Library object from the given distribution if it is a valid library.
    Otherwise, returns None.

    A distribution is considered a valid library if it has at least one importable file
    and it is not an editable install.
    """
    metadata = dist.metadata
    name = metadata["Name"]
    version = metadata["Version"]
    dist_hash = get_hash(name, version)
    url = metadata.get("Home-page", "")

    module_files = dist.files
    if module_files is None:
        # case where the metadata files listing files (RECORD, SOURCES.txt etc..) are missing.
        return None

    if is_editable_install(name, version, module_files):
        # We decided to omit this case since whatever the package is, its probably under active development
        # and still not a library at that point in time
        return None

    importable_module_files = {
        str(f)
        for f in module_files
        if f.name.endswith(IMPORTABLE_FILE_SUFFIXES) and f.name != "setup.py"
    }
    file_count = len(importable_module_files)
    if file_count == 0:
        return None

    current_time = int(time.time() * 1000)

    return Library(
        class_count=file_count,
        internal_date=current_time,
        external_date=current_time,
        file=name,
        hash=dist_hash,
        url=url,
        version=version,
    )


def is_editable_install(
    dist_name: str, version: str, all_files: list[importlib_metadata.PackagePath]
):
    return (
        importlib_metadata.PackagePath(f"__editable__{dist_name.lower()}-{version}.pth")
        in all_files
    )


class LibraryObservations:
    """
    LibraryObservations is responsible for collecting and reporting the loaded libraries
    in the running environment.
    """

    def __init__(self, modules: Iterable[ModuleType]) -> None:
        # {hash: [file_name]}
        self._observations: dict[str, list[str]] = defaultdict(list)

        for module in modules:
            self.add_module(module)

    def add_module(self, module: ModuleType) -> None:
        if (
            (file_name := getattr(module, "__file__", None))
            and (norm_file_name := normalize_file_name(file_name))
            and (dist_meta := get_module_distribution_metadata(module))
        ):
            self._observations[
                get_hash(dist_meta["Name"], dist_meta["Version"])
            ].append(norm_file_name)

    def to_list(self) -> list[LibraryObservation]:
        return [
            LibraryObservation(library_hash=hash, names=files)
            for hash, files in self._observations.items()
        ]

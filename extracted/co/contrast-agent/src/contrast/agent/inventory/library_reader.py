# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import threading
import time
from collections import defaultdict
from contextlib import suppress
from typing import TYPE_CHECKING

from contrast_fireball import Library, LibraryObservation

from contrast.agent.scope import contrast_scope
from contrast.utils.decorators import fail_loudly
from contrast.utils.distributions import (
    LightDistribution,
    all_distributions,
    distribution_from_module,
    get_hash,
    normalize_file_name,
)
from contrast.utils.patch_utils import get_loaded_modules
from contrast_vendor import importlib_metadata
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from collections.abc import Iterable
    from types import ModuleType

    from contrast.import_hook import ContrastMetaPathFinder
    from contrast.reporting.fireball import Client

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

    def __init__(
        self,
        fireball_client: Client,
        *,
        analyze_libraries: bool = True,
        enable_shields: bool = False,
        path_finder: ContrastMetaPathFinder | None = None,
    ) -> None:
        self.fireball_client = fireball_client
        self.analyze_libraries = analyze_libraries
        self.enable_shields = enable_shields
        self.path_finder = path_finder
        self.analysis_thread = threading.Thread(
            target=self._read_distribution_packages, daemon=True
        )

    def start(self) -> None:
        if not self.analyze_libraries and not self.enable_shields:
            logger.debug(
                "Library analysis and shields are disabled; skipping library reading"
            )
            return
        self.analysis_thread.start()

    @contrast_scope()
    def _read_distribution_packages(self) -> None:
        """
        Discovers every installed distribution package once, then reports them as
        Libraries (if library analysis is enabled) and/or instruments CVE shields
        (if shields are enabled).
        """
        logger.debug("Analyzing libraries...")

        libraries = self.discover_libraries()

        if self.enable_shields:
            # Fireball only looks up shield definitions for reported libraries, so
            # shields must be enabled first to be ready for them.
            self._enable_shields(libraries)

        if self.analyze_libraries:
            self._report_discovered_libraries(libraries)
            # Fireball drops observations of libraries that haven't been discovered
            # yet, so the import hook only observes libraries from here on. This must
            # happen before snapshotting sys.modules, so every import is reported by
            # the import hook, the snapshot, or both. Fireball ignores duplicate
            # observations.
            if self.path_finder is not None:
                self.path_finder.enable_library_observations(self.fireball_client)
            report_library_observations(self.fireball_client, self.observed_libraries())

    @fail_loudly("Unable to initialize Contrast CVE Shields")
    def _enable_shields(self, libraries: list[Library]) -> None:
        if not self.analyze_libraries:
            # Fireball only looks up shield definitions for reported libraries.
            logger.warning(
                "CVE Shields won't receive shield definitions from Contrast while "
                "library analysis is disabled"
            )
        # shields raises ImportError on <3.12, so this import is deferred until needed.
        from contrast.agent import shields

        shields.enable(self.fireball_client, libraries)

    def discover_libraries(self) -> list[Library]:
        """
        Reads every installed distribution package and returns it as a Library.
        """
        return [
            library
            for dist in all_distributions()
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
        self.fireball_client.new_libraries(reportable_libraries)

    def observed_libraries(self) -> list[LibraryObservation]:
        """
        Reads every loaded module and returns it as a LibraryObservation.
        """
        return LibraryObservations(get_loaded_modules().values()).to_list()


def observe_library(fireball_client: Client, module: ModuleType) -> None:
    """
    Reports the library that an imported module belongs to.
    """
    if (hash_and_file := _library_hash_and_file(module)) is None:
        return
    library_hash, file_name = hash_and_file
    report_library_observations(
        fireball_client,
        [LibraryObservation(library_hash=library_hash, names=[file_name])],
    )


def report_library_observations(
    fireball_client: Client, observations: list[LibraryObservation]
) -> None:
    reportable_observations = [
        observation
        for observation in observations
        if observation.library_hash not in CONTRAST_DIST_HASHES
    ]
    if not reportable_observations:
        return

    fireball_client.new_library_observations(reportable_observations)


def library_from_distribution(dist: LightDistribution) -> Library | None:
    """
    Returns a Library object from the given distribution if it is a valid library.
    Otherwise, returns None.

    A distribution is considered a valid library if it has at least one importable file
    and it is not an editable install.
    """
    name = dist.name
    version = dist.version
    dist_hash = get_hash(name, version)

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
        url=None,
        version=version,
    )


def is_editable_install(
    dist_name: str, version: str, all_files: list[importlib_metadata.PackagePath]
):
    return (
        importlib_metadata.PackagePath(f"__editable__{dist_name.lower()}-{version}.pth")
        in all_files
    )


def _library_hash_and_file(module: ModuleType) -> tuple[str, str] | None:
    """
    Returns the (library hash, normalized file name) for the given module, or None if
    the module doesn't belong to an installed distribution.
    """
    if (
        (file_name := getattr(module, "__file__", None))
        and (norm_file_name := normalize_file_name(file_name))
        and (dist_meta := distribution_from_module(module))
    ):
        return get_hash(dist_meta.name, dist_meta.version), norm_file_name
    return None


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
        if hash_and_file := _library_hash_and_file(module):
            library_hash, file_name = hash_and_file
            self._observations[library_hash].append(file_name)

    def to_list(self) -> list[LibraryObservation]:
        return [
            LibraryObservation(library_hash=hash, names=files)
            for hash, files in self._observations.items()
        ]

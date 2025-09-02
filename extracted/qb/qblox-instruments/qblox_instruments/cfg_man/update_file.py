# ----------------------------------------------------------------------------
# Description    : Update file format utilities
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2021)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import copy
import json
import os
import re
import tarfile
import tempfile
import zipfile
from collections.abc import Iterable
from typing import BinaryIO, Callable, Optional

from qblox_instruments.build import DeviceInfo
from qblox_instruments.cfg_man import log
from qblox_instruments.cfg_man.const import VERSION
from qblox_instruments.cfg_man.probe import ConnectionInfo

# ----------------------------------------------------------------------------


class UpdateFile:
    """
    Representation of a device update file.
    """

    __slots__ = [
        "_fname",
        "_format",
        "_metadata",
        "_models",
        "_tempdir",
        "_update_fname",
    ]

    # ------------------------------------------------------------------------
    def __init__(self, fname: str, check_version: bool = True) -> None:
        """
        Loads an update file.

        Parameters
        ----------
        fname: str
            The file to load.
        check_version: bool
            Whether to throw a NotImplementedError if the minimum
            configuration management client version reported by the update
            file is newer than our client version.
        """
        super().__init__()

        # Save filename.
        self._fname = fname

        # Be lenient: if the user downloaded a release file and forgot to
        # extract it, extract it for them transparently.
        self._update_fname = None
        self._tempdir = None

        def extract(fin) -> None:
            log.debug(
                '"%s" looks like a release file, extracting update.tar.gz from it...',
                self._fname,
            )
            self._tempdir = tempfile.TemporaryDirectory()
            self._update_fname = os.path.join(self._tempdir.__enter__(), "update.tar.gz")
            with open(self._update_fname, "wb") as fout:
                while True:
                    buf = fin.read(4096)
                    if not buf:
                        break
                    while buf:
                        buf = buf[fout.write(buf) :]

        try:
            log.debug('Determining file type of "%s"...', self._fname)
            with tarfile.TarFile.open(self._fname, "r:*") as tar:
                for name in tar.getnames():
                    if name.endswith("update.tar.gz"):
                        with tar.extractfile(name) as fin:
                            extract(fin)
                        break
                else:
                    log.debug(
                        '"%s" looks like it might indeed be an update file.',
                        self._fname,
                    )
                    self._update_fname = self._fname
        except tarfile.TarError:
            try:
                with zipfile.ZipFile(self._fname, "r") as zip:
                    for name in zip.namelist():
                        if name.endswith("update.tar.gz"):
                            with zip.open(name, "r") as fin:
                                extract(fin)
                            break
            except zipfile.BadZipFile:
                pass
        if self._update_fname is None:
            raise ValueError("invalid update file")

        # Read the tar file.
        try:
            log.debug('Scanning update tar file "%s"...', self._update_fname)
            with tarfile.TarFile.open(self._update_fname, "r:gz") as tar:
                fmts = set()
                meta_json = None
                models = set()
                metadata = {}
                while True:
                    info = tar.next()
                    if info is None:
                        break
                    name = info.name
                    log.debug("  %s", name)
                    if name.startswith("."):
                        name = name[1:]
                    if name.startswith("/") or name.startswith("\\"):
                        name = name[1:]
                    name, *tail = re.split(r"/|\\", name, maxsplit=1)
                    if name == "meta.json" and not tail:
                        fmts.add("multi")
                        meta_json = info
                    elif name.startswith("only_"):
                        name = name[5:]
                        if name not in models:
                            fmts.add("multi")
                            metadata[name] = {"manufacturer": "qblox", "model": name}
                            models.add(name)
                    elif name == "common":
                        fmts.add("multi")
                    elif name not in models:
                        fmts.add("legacy")
                        metadata[name] = {"manufacturer": "qblox", "model": name}
                        models.add(name)
                log.debug("Scan complete")
                log.debug("")
                if meta_json is not None:
                    with tar.extractfile(meta_json) as f:
                        metadata.update(json.loads(f.read()))
                if len(fmts) != 1:
                    raise ValueError("invalid update file")
                self._format = next(iter(fmts))
                self._models = {
                    model: DeviceInfo.from_dict(metadata[model]) for model in sorted(models)
                }
                self._metadata = metadata.get("meta", {})
        except tarfile.TarError:
            raise ValueError("invalid update file")

        # Check client version.
        if check_version and (
            self._metadata.get("meta", {}).get("min_cfg_man_client", (0, 0, 0)) > VERSION
        ):
            raise NotImplementedError(
                "update file format is too new. Please update Qblox Instruments first"
            )

    # ------------------------------------------------------------------------
    def close(self) -> None:
        """
        Cleans up any operating resources that we may have claimed.
        """
        if hasattr(self, "_tempdir") and self._tempdir is not None:
            self._tempdir.cleanup()
            self._tempdir = None

    # ------------------------------------------------------------------------
    def __del__(self) -> None:
        self.close()

    # ------------------------------------------------------------------------
    def __enter__(self) -> "UpdateFile":
        return self

    # ------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback) -> Optional[bool]:
        self.close()

    # ------------------------------------------------------------------------
    def needs_confirmation(self) -> Optional[str]:
        """
        Returns whether the update file requests the user to confirm something
        before application, and if so, what message should be printed.

        Returns
        -------
        Optional[str]
            None if there is nothing exceptional about this file, otherwise
            this is the confirmation message.
        """
        return self._metadata.get("confirm", None)

    # ------------------------------------------------------------------------
    def __str__(self) -> str:
        return self._fname

    # ------------------------------------------------------------------------
    def __repr__(self) -> str:
        return repr(self._fname)

    # ------------------------------------------------------------------------
    def summarize(self) -> str:
        """
        Returns a summary of the update file format.

        Returns
        -------
        str
            Update file summary.
        """
        if self._format == "legacy":
            return f"legacy update file for {next(iter(self._models))}"
        return f"update file for {', '.join(self._models)}"

    # ------------------------------------------------------------------------
    def pprint(self, output: Callable[[str], None] = log.info) -> None:
        """
        Pretty-prints the update file metadata.

        Parameters
        ----------
        output: Callable[[str], None]
            The function used for printing. Each call represents a line.
        """
        min_client = self._metadata.get("min_cfg_man_client", None)
        if min_client is not None:
            if self._format != "legacy":
                min_client = (0, 2, 0)
            min_client = ".".join(map(str, min_client))

        query_message = self._metadata.get("confirm", "None")

        output(f"Update file              : {self._fname}")
        output(f"File format              : {self._format}")
        output(f"Minimum client version   : {min_client}")
        output(f"Query message            : {query_message}")
        output(f"Contains updates for     : {len(self._models)} product(s)")
        for model, di in self._models.items():
            output(f"  Model                  : {model}")
            for key, pretty in (
                ("sw", "Application"),
                ("fw", "FPGA firmware"),
                ("kmod", "Kernel module"),
                ("cfg_man", "Cfg. manager"),
            ):
                if key in di:
                    output(f"    {pretty + ' version':<21}: {di[key]}")

    # ------------------------------------------------------------------------
    def load(
        self,
        ci: ConnectionInfo,
        included_slots: Optional[Iterable[int]] = None,
        excluded_slots: Optional[Iterable[int]] = None,
    ) -> BinaryIO:
        """
        Loads an update file, checking whether the given update file is
        compatible within the given connection context. Returns a file-like
        object opened in binary read mode if compatible, or throws a
        ValueError if there is a problem.

        Parameters
        ----------
        ci: ConnectionInfo
            Connection information object retrieved from autoconf(), to verify
            that the update file is compatible, or to make it compatible, if
            possible.
        included_slots: Optional[Iterable[int]]
            list of included slot indices. Optional, by default None.
        excluded_slots: Optional[Iterable[int]]
            list of excluded slot indices. Optional, by default None.

        Returns
        -------
        BinaryIO
            Binary file-like object for the update file. Will at least be
            opened for reading, and rewound to the start of the file. This may
            effectively be ``open(fname, "rb")``, but could also be a
            ``tempfile.TemporaryFile`` to an update file specifically
            converted to be compatible with the given environment. It is the
            responsibility of the caller to close the file.

        Raises
        ------
        ValueError
            If there is a problem with the given update file.
        """

        # Check whether the update includes data for all the devices we need to
        # support.
        log.info(f"Models In Cluster        : {sorted(ci.all_updatable_models)}")
        log.info(f"Models In Update Package : {sorted(set(self._models.keys()))}")

        incompatible_modules = set()

        def check_update_compatibility(slot: int, model: str) -> None:
            """
            Check if the given update file is compatible within the cluster.
            Take into account included and excluded slots: a module is not considered
            incompatible if it is also excluded from the update.
            :param slot:    slot number to check for
            :param model:   model name of module in slot
            """
            if model.endswith("qdm"):
                return

            if (model not in self._models) and (
                (included_slots is None and excluded_slots is None)
                or (included_slots is not None and slot in included_slots)
                or (excluded_slots is not None and slot not in excluded_slots)
            ):
                incompatible_modules.add(model)

        if ci.slot_index is not None:
            # Single slot update
            model = next(iter(ci.all_updatable_models))
            slot_no = int(ci.slot_index)
            log.info(f"Single-Slot Update in slot {slot_no}")
            check_update_compatibility(slot_no, model)

        elif ci.device.modules is not None:
            # Multiple slots update
            log.info("Multi-Slot Update")
            for slot, module in ci.device.modules.items():
                model = module.model
                slot_no = int(slot)
                check_update_compatibility(slot_no, model)

        else:
            raise RuntimeError("failed to determine update compatibility for update file")

        incompatible_modules = list(sorted(incompatible_modules))
        if incompatible_modules:
            if len(incompatible_modules) == 1:
                to_print = incompatible_modules[0]
            else:
                to_print = ", ".join(incompatible_modules[:-1]) + " and " + incompatible_modules[-1]
            raise ValueError(f"update file is not compatible with {to_print} devices")

        # If we're connected to the server via the legacy update protocol, we
        # must also supply a legacy update file. So if this is not already in
        # the legacy format, we have to downconvert the file format.
        if ci.protocol == "legacy" and self._format != "legacy":
            if len(ci.all_updatable_models) != 1:
                raise ValueError(
                    "cannot update multiple devices at once with legacy configuration managers"
                )
            log.info(
                "Converting multi-device update to legacy update file for %s...",
                ci.device.model,
            )
            with tarfile.open(self._update_fname, "r:gz") as tar:
                common = {}
                specific = {}
                infos = []
                log.debug("Scanning input tar file...")
                while True:
                    info = tar.next()
                    if info is None:
                        break
                    log.debug("  %s", info.name)
                    infos.append(info)
                for info in infos:
                    # Split filename into the name of the root directory of the
                    # tar file and the corresponding root path on the device.
                    name = info.name
                    if name.startswith("."):
                        name = name[1:]
                    if name.startswith("/") or name.startswith("\\"):
                        name = name[1:]
                    tar_dir, *root_path = re.split(r"[\\/]", name, maxsplit=1)
                    root_path = "/" + root_path[0] if root_path else "/"

                    # Save the info blocks for the files relevant to us.
                    if tar_dir == "only_" + ci.device.model:
                        specific[root_path] = info
                    elif tar_dir == "common":
                        common[root_path] = info

                # Device-specific files override common files.
                files = common
                files.update(specific)

                # Create a new tar.gz file with the files for this device
                # specifically.
                log.debug("Recompressing in legacy format...")
                file_obj = tempfile.TemporaryFile("w+b")  # noqa: SIM115
                try:
                    with tarfile.open(None, "w:gz", file_obj) as tar_out:
                        for idx, (path, info) in enumerate(sorted(files.items())):
                            log.progress(
                                idx / len(files),
                                "Recompressing update archive in legacy format...",
                            )

                            # Determine the path in the new tarfile.
                            out_info = copy.copy(info)
                            if path == "/":
                                out_info.name = f"./{ci.device.model}"
                            else:
                                out_info.name = f"./{ci.device.model}{path}"

                            log.debug("  %s", out_info.name)
                            tar_out.addfile(out_info, tar.extractfile(info))
                finally:
                    log.clear_progress()

                log.debug("Legacy update file complete")
                log.debug("")

                # Rewind back to the start of the file to comply with
                # postconditions.
                file_obj.seek(0)

                return file_obj

        # No need to change the contents of the update file, so just open the
        # file as-is.
        return open(self._update_fname, "rb")

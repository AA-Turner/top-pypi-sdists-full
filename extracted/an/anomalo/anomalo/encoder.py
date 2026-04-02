from __future__ import annotations

import importlib
import os
from collections import defaultdict, namedtuple
from typing import Any


ANOMALO_DATA_KEY = "AnomaloData"
ANOMALO_VERSION_ID_KEY = "AnomaloVersionID"
ANOMALO_VERSION_ID = 1

Format = namedtuple(
    "Format",
    ["pkg", "pkg_postimport", "load", "load_args", "save", "save_args", "wrap_obj"],
)


# Include AnomaloVersionID in the output file first without affecting subkey sorting
class YAMLMetadataWrapper:
    def __init__(self, data: Any):
        self.data = data

    def __iter__(self):
        yield from (
            {"AnomaloVersionID": ANOMALO_VERSION_ID, "AnomaloData": self.data}
        ).items()


def _yaml_postimport(imported_pkg: Any) -> None:
    representer = importlib.import_module("yaml.representer")
    imported_pkg.add_representer(defaultdict, representer.Representer.represent_dict)
    imported_pkg.add_representer(
        YAMLMetadataWrapper, representer.Representer.represent_dict
    )


class Encoder:
    ENCODER_ALIASES = {"yml": "yaml"}
    ENCODERS = {
        "yaml": Format(
            pkg="yaml",
            pkg_postimport=_yaml_postimport,
            load="safe_load",
            load_args=None,
            save="dump",
            save_args=None,
            wrap_obj=lambda obj: YAMLMetadataWrapper(obj),
        ),
        "json": Format(
            pkg="json",
            pkg_postimport=None,
            load="load",
            load_args=None,
            save="dump",
            save_args={"indent": 4, "sort_keys": True},
            wrap_obj=lambda obj: {
                ANOMALO_VERSION_ID_KEY: ANOMALO_VERSION_ID,
                ANOMALO_DATA_KEY: obj,
            },
        ),
    }

    def __init__(self, filename: str):
        self.filename = filename
        self.file_ext = os.path.splitext(filename)[1][1:]
        supported_extensions = self.ENCODERS.keys() | self.ENCODER_ALIASES.keys()
        if self.file_ext not in supported_extensions:
            raise Exception(
                f"Unsupported file type extension {self.file_ext}. "
                f"Supported extensions are: {', '.join(sorted(supported_extensions))}"
            )
        self.file_encoder: Format = self.ENCODERS[
            self.ENCODER_ALIASES.get(self.file_ext, self.file_ext)
        ]
        try:
            self.pkg = importlib.import_module(self.file_encoder.pkg)
            if self.file_encoder.pkg_postimport:
                self.file_encoder.pkg_postimport(self.pkg)
        except ModuleNotFoundError as e:
            raise Exception(
                f'Package "{self.file_encoder.pkg}" for {self.file_ext} '
                "file type support was not found"
            ) from e

    def _unwrap_obj(self, obj: dict[str, Any]) -> Any:
        if obj.get(ANOMALO_VERSION_ID_KEY) != ANOMALO_VERSION_ID:
            return {}
        return obj.get(ANOMALO_DATA_KEY) or {}

    def load(self, *args, **kwargs) -> Any:
        with open(self.filename) as file_handle:
            passed_kwargs = {**kwargs, **(self.file_encoder.load_args or {})}
            return self._unwrap_obj(
                getattr(self.pkg, self.file_encoder.load)(
                    file_handle, *args, **passed_kwargs
                ),
            )

    def save(self, obj: Any, *args, **kwargs) -> None:
        if not obj:
            print(f"No data to save")
            return
        with open(self.filename, "w") as file_handle:
            passed_kwargs = {**kwargs, **(self.file_encoder.save_args or {})}
            getattr(self.pkg, self.file_encoder.save)(
                self.file_encoder.wrap_obj(obj),
                file_handle,
                *args,
                **passed_kwargs,
            )

"""Hatchling metadata hook: require at least the vention-grpc-py-sdk release scripts/ci_python_package.py resolved."""

from __future__ import annotations

import runpy
from pathlib import Path

from hatchling.metadata.plugin.interface import MetadataHookInterface

SOURCE_MODULE = Path(__file__).parent / "src" / "vention_sim" / "_source.py"


class SdkPinMetadataHook(MetadataHookInterface):
    def update(self, metadata: dict) -> None:
        if not SOURCE_MODULE.is_file():
            raise FileNotFoundError(f"{SOURCE_MODULE} is missing. Build with `pnpm nx run python-sdk:build`.")
        sdk_version = runpy.run_path(str(SOURCE_MODULE))["VENTION_GRPC_PY_SDK_VERSION"]
        # The sim protos embed vention-protos messages, so the stubs need every proto
        # the pinned vention-protos commit ships. Later releases keep those, and a
        # lower bound also admits the `<next release>.devN` builds that open
        # vention-protos-clients PRs publish, which an exact pin rejects.
        metadata["dependencies"] = [
            f"vention-grpc-py-sdk>={sdk_version}",
            "protobuf>=6.31.1,<7",
            "grpcio>=1.74.0,<2",
        ]

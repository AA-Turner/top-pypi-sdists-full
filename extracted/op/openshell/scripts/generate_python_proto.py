# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Generate Python protobuf stubs and make their imports package-relative."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# `mise run proto:fetch` exports exactly the SDK's protos (two roots and their
# imports) into proto/, so every file there is compiled.
PROTO_DIR = Path("proto")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-pyi",
        action="store_true",
        help=(
            "Skip .pyi type stubs. Needed with protoc older than 3.20 "
            "(e.g. Fedora's grpcio-tools 1.48), which has no --pyi_out."
        ),
    )
    args = parser.parse_args()
    output_dir = Path("src/openshell/_proto")
    proto_files = sorted(str(path) for path in PROTO_DIR.glob("*.proto"))
    if not proto_files:
        sys.exit(f"no .proto files in {PROTO_DIR}/; run `mise run proto:fetch`")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            "-Iproto",
            "--python_out=src/openshell/_proto",
            *(
                []
                if args.no_pyi
                else [
                    "--pyi_out=src/openshell/_proto",
                    "--mypy_grpc_out=generate_concrete_servicer_stubs:src/openshell/_proto",
                ]
            ),
            "--grpc_python_out=src/openshell/_proto",
            *proto_files,
        ],
        check=True,
    )

    # Rewrite only imports of our generated modules, leaving google.protobuf
    # imports intact. The same rule covers runtime modules and type stubs.
    modules = "|".join(re.escape(f"{Path(path).stem}_pb2") for path in proto_files)
    pattern = rf"^import ({modules})( as \w+)?$"
    suffixes = ["_pb2.py", "_pb2_grpc.py"]
    if not args.no_pyi:
        suffixes.extend(["_pb2.pyi", "_pb2_grpc.pyi"])
    for proto in proto_files:
        for suffix in suffixes:
            file_path = output_dir / f"{Path(proto).stem}{suffix}"
            text = file_path.read_text()
            text = re.sub(pattern, r"from . import \1\2", text, flags=re.MULTILINE)
            file_path.write_text(text)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download and vendor LLVM Demangle source files."""

import argparse
import os
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

LLVM_VERSIONS = {
    11: "11.1.0",
    12: "12.0.1",
    13: "13.0.1",
    14: "14.0.6",
    15: "15.0.7",
    16: "16.0.6",
    17: "17.0.6",
    18: "18.1.8",
    19: "19.1.7",
    20: "20.1.0",
    21: "21.1.0",
}

URL_TEMPLATE = (
    "https://github.com/llvm/llvm-project/releases/download/"
    "llvmorg-{version}/llvm-project-{version}.src.tar.xz"
)

HEADER_SUBDIR = "llvm/include/llvm/Demangle"
SOURCE_SUBDIR = "llvm/lib/Demangle"


def vendor(major_version: int, output_dir: Path):
    full_version = LLVM_VERSIONS[major_version]
    url = URL_TEMPLATE.format(version=full_version)

    vendor_dir = output_dir / f"llvm{major_version}"
    if vendor_dir.exists():
        shutil.rmtree(vendor_dir)

    include_dest = vendor_dir / "include" / "llvm" / "Demangle"
    lib_dest = vendor_dir / "lib" / "Demangle"
    include_dest.mkdir(parents=True)
    lib_dest.mkdir(parents=True)

    tar_prefix = f"llvm-project-{full_version}.src"
    header_prefix = f"{tar_prefix}/{HEADER_SUBDIR}/"
    source_prefix = f"{tar_prefix}/{SOURCE_SUBDIR}/"

    print(f"Downloading LLVM {full_version} from {url} ...")

    with tempfile.TemporaryDirectory() as tmpdir:
        archive_path = os.path.join(tmpdir, "llvm.tar.xz")
        urllib.request.urlretrieve(url, archive_path)

        print("Extracting Demangle files ...")
        with tarfile.open(archive_path, "r:xz") as tar:
            for member in tar.getmembers():
                if member.isdir():
                    continue
                if member.name.startswith(header_prefix):
                    data = tar.extractfile(member)
                    filename = os.path.basename(member.name)
                    (include_dest / filename).write_bytes(data.read())
                elif member.name.startswith(source_prefix):
                    data = tar.extractfile(member)
                    filename = os.path.basename(member.name)
                    if filename.endswith((".cpp", ".h", ".def")):
                        (lib_dest / filename).write_bytes(data.read())

    print(f"Vendored LLVM {full_version} Demangle into {vendor_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vendor LLVM Demangle sources")
    parser.add_argument(
        "--llvm-version",
        type=int,
        required=True,
        choices=sorted(LLVM_VERSIONS.keys()),
        help="LLVM major version to vendor",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("vendor"),
        help="Output directory (default: vendor/)",
    )
    args = parser.parse_args()
    vendor(args.llvm_version, args.output_dir)

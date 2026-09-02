import os
from itertools import zip_longest
from typing import NamedTuple

import pytest

from tpk_ar.blob import TpkEngineAssetsBlob, TpkTypeTreeBlob
from tpk_ar.enums import TpkCompressionType, TpkDataType
from tpk_ar.file import TpkFile

SAMPLES_PATH = os.path.join(os.path.dirname(__file__), "samples")


class SampleInformation(NamedTuple):
    type: TpkDataType
    version: int
    compression: TpkCompressionType
    path: str


def generate_sample_path(type: TpkDataType, version: int, compression: TpkCompressionType) -> str:
    if type == TpkDataType.TypeTreeInformation:
        type_str = "type_tree"
    elif type == TpkDataType.EngineAssets:
        type_str = "engine_assets"
    else:
        raise ValueError(f"Invalid type: {type}")
    version_str = f"v{version}"
    compression_str = compression.name.lower() if compression != TpkCompressionType.NONE else "uncompressed"
    return os.path.join(SAMPLES_PATH, type_str, version_str, f"{compression_str}.tpk")


SAMPLES = [
    SampleInformation(type=st, version=sv, compression=sc, path=generate_sample_path(st, sv, sc))
    for st in [TpkDataType.TypeTreeInformation, TpkDataType.EngineAssets]
    for sv in [1, 2]
    for sc in [
        TpkCompressionType.Brotli,
        TpkCompressionType.Lzma,
        TpkCompressionType.Lz4,
        TpkCompressionType.NONE,
    ]
    if os.path.exists(generate_sample_path(st, sv, sc))
]


@pytest.mark.parametrize("sample", SAMPLES)
def test_parsing(sample: SampleInformation) -> None:
    with open(sample.path, "rb") as f:
        tpk_file = TpkFile.parse(f)
        assert tpk_file.DataType == sample.type
        assert tpk_file.TpkVersionNumber == sample.version
        assert tpk_file.CompressionType == sample.compression

        data_blob = tpk_file.GetDataBlob()
        if sample.type == TpkDataType.TypeTreeInformation:
            assert isinstance(data_blob, TpkTypeTreeBlob)
        elif sample.type == TpkDataType.EngineAssets:
            assert isinstance(data_blob, TpkEngineAssetsBlob)


def test_version_compatibility() -> None:
    lzma_v1_fp = os.path.join(SAMPLES_PATH, "type_tree", "v1", "lzma.tpk")
    lzma_v2_fp = os.path.join(SAMPLES_PATH, "type_tree", "v2", "lzma.tpk")
    with open(lzma_v1_fp, "rb") as f1:
        tpk_file_v1 = TpkFile.parse(f1)
        tree1 = tpk_file_v1.GetDataBlob()
    with open(lzma_v2_fp, "rb") as f2:
        tpk_file_v2 = TpkFile.parse(f2)
        tree2 = tpk_file_v2.GetDataBlob()

    assert isinstance(tree1, TpkTypeTreeBlob)
    assert isinstance(tree2, TpkTypeTreeBlob)

    string_map1 = tree1.CommonString.BuildMap(tree1.StringBuffer)
    string_map2 = tree2.CommonString.BuildMap(tree2.StringBuffer)

    # stringmap1 is shorter than stringmap2
    # using zip_longest to handle the length difference while being version agnostic
    for e1, e2 in zip_longest(string_map1.items(), string_map2.items()):
        if e1 is None:
            break
        assert e1 == e2

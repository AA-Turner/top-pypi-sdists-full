import pytest

from eumdac.download_app import (
    _divide_into_chunks,
    _check_chunks,
    _reassemble_from_chunks,
)
from pathlib import Path


def test_divide_into_chunks():
    output = _divide_into_chunks("basedir", 2948, 1000)
    expected = {
        Path("basedir") / "chunk.0": (0, 1000),
        Path("basedir") / "chunk.1": (1000, 2000),
        Path("basedir") / "chunk.2": (2000, 2948),
    }
    assert output == expected


def test_divide_into_chunks_bigger_chunk():
    output = _divide_into_chunks("basedir", 2948, 3000)
    expected = {
        Path("basedir") / "chunk.0": (0, 2948),
    }
    assert output == expected


def test_divide_into_chunks_exact_division():
    output = _divide_into_chunks("basedir", 2000, 1000)
    expected = {
        Path("basedir") / "chunk.0": (0, 1000),
        Path("basedir") / "chunk.1": (1000, 2000),
    }
    assert output == expected


def _create_binary_file(file_name, num_bytes, bvalue=b"\0"):
    with open(file_name, "wb") as file:
        file.write(bvalue * num_bytes)


def test_check_chunks(tmp_path):
    (tmp_path / Path("testprodname")).mkdir()
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.0", 1000)
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.1", 1000)
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.2", 948)
    output = _check_chunks(
        {
            tmp_path / Path("testprodname") / "chunk.0": (0, 1000),
            tmp_path / Path("testprodname") / "chunk.1": (1000, 2000),
            tmp_path / Path("testprodname") / "chunk.2": (2000, 2948),
        }
    )
    assert output


def test_check_chunks_invalid_size(tmp_path):
    (tmp_path / Path("testprodname")).mkdir()
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.0", 999)
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.1", 1000)
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.2", 948)
    output = _check_chunks(
        {
            tmp_path / Path("testprodname") / "chunk.0": (0, 1000),
            tmp_path / Path("testprodname") / "chunk.1": (1000, 2000),
            tmp_path / Path("testprodname") / "chunk.2": (2000, 2948),
        }
    )
    assert output is False


def test_check_chunks_chunk_missing(tmp_path):
    (tmp_path / Path("testprodname")).mkdir()
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.0", 999)
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.2", 948)
    output = _check_chunks(
        {
            tmp_path / Path("testprodname") / "chunk.0": (0, 1000),
            tmp_path / Path("testprodname") / "chunk.1": (1000, 2000),
            tmp_path / Path("testprodname") / "chunk.2": (2000, 2948),
        }
    )
    assert output is False


def test_reassemble_from_chunks(tmp_path):
    (tmp_path / Path("testprodname")).mkdir()
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.0", 1000, b"\0")
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.1", 1000, b"\1")
    _create_binary_file(tmp_path / Path("testprodname") / "chunk.2", 948, b"\2")
    output = _reassemble_from_chunks(
        {
            tmp_path / Path("testprodname") / "chunk.0": (0, 1000),
            tmp_path / Path("testprodname") / "chunk.1": (1000, 2000),
            tmp_path / Path("testprodname") / "chunk.2": (2000, 2948),
        },
        tmp_path / "output",
    )
    assert output.stat().st_size == 2948
    with output.open("rb") as outf:
        bindata = outf.read()
        print(type(bindata))
        assert bindata[0] == 0
        assert bindata[1000] == 1
        assert bindata[2000] == 2

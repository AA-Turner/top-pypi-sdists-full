from __future__ import annotations
import os
import zipfile
import logging

import requests
from tqdm.autonotebook import tqdm


logger = logging.getLogger(__name__)


def download_url(url: str, save_path: str, chunk_size: int = 1024):
    """Download url with progress bar using tqdm

    Args:
        url (str): downloadable url
        save_path (str): local path to save the downloaded file
        chunk_size (int, optional): chunking of files. Defaults to 1024.
    """
    r = requests.get(url, stream=True)
    total = int(r.headers.get("Content-Length", 0))
    with (
        open(save_path, "wb") as fd,
        tqdm(
            desc=save_path,
            total=total,
            unit="iB",
            unit_scale=True,
            unit_divisor=chunk_size,
        ) as bar,
    ):
        for data in r.iter_content(chunk_size=chunk_size):
            size = fd.write(data)
            bar.update(size)


def unzip(zip_file: str, out_dir: str):
    zip_ = zipfile.ZipFile(zip_file, "r")
    zip_.extractall(path=out_dir)
    zip_.close()


def download_and_unzip(url: str, out_dir: str, chunk_size: int = 1024) -> str:
    dataset = url.split("/")[-1]
    zip_file = os.path.join(out_dir, dataset)
    data_dir = os.path.join(out_dir, dataset.replace(".zip", ""))

    if os.path.isfile(os.path.join(data_dir, "queries.jsonl")) and os.path.isfile(
        os.path.join(data_dir, "corpus.jsonl")
    ):
        return data_dir

    os.makedirs(out_dir, exist_ok=True)

    if not os.path.isfile(zip_file):
        logger.info(f"Downloading {dataset} ...")
        download_url(url, zip_file, chunk_size)

    if not os.path.isdir(zip_file.replace(".zip", "")):
        logger.info(f"Unzipping {dataset} ...")
        unzip(zip_file, out_dir)

    return data_dir

# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import argparse
import io
import os
import re
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.cloud import storage
from zipfile import ZipFile, BadZipFile

OPENVID_BASE = "https://huggingface.co/datasets/nkp37/OpenVid-1M/resolve/main"
CSV_PATHS = [
    "data/train/OpenVid-1M.csv",
    "data/train/OpenVidHD.csv",
]


def parse_gcs_uri(gcs_uri: str) -> Tuple[str, str]:
    """
    Parse 'gs://bucket/prefix/...' -> (bucket, prefix_without_leading_slash)
    """
    if not gcs_uri.startswith("gs://"):
        raise ValueError("gcs_uri must start with gs://")
    path = gcs_uri[5:]
    parts = path.split("/", 1)
    bucket = parts[0]
    prefix = parts[1] if len(parts) > 1 else ""
    prefix = prefix.strip("/")
    return bucket, prefix


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception_type((requests.RequestException,))
)
def _http_get(url: str, stream: bool = True) -> requests.Response:
    headers = {"User-Agent": "openvid-to-gcs/1.0"}
    r = requests.get(url, stream=stream, timeout=60, headers=headers)
    r.raise_for_status()
    return r


def _download_to_file(url: str, out_path: str) -> None:
    with _http_get(url, stream=True) as r, open(out_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)


def _stitch_parts_to_file(part_paths, out_path):
    with open(out_path, "wb") as out:
        for p in part_paths:
            with open(p, "rb") as src:
                shutil.copyfileobj(src, out, length=1024 * 1024)


def _blob_exists(bucket: storage.Bucket, key: str) -> bool:
    return bucket.blob(key).exists()


def _upload_stream(bucket: storage.Bucket, key: str, fh: io.BufferedReader, content_type: Optional[str] = None):
    blob = bucket.blob(key)
    # Reasonable chunk size (8MB) for large files; adjust if needed
    blob.chunk_size = 8 * 1024 * 1024
    blob.upload_from_file(fh, rewind=True, content_type=content_type)


def upload_zip_members_to_gcs(zip_path: str, bucket: storage.Bucket, dest_prefix: str,
                              workers: int = 4, subdir: str = "video/") -> None:
    """
    Streams each file inside a ZIP directly to GCS without extracting to disk.
    """
    dest_prefix = dest_prefix.rstrip("/") + "/"
    target_prefix = dest_prefix + subdir  # e.g., gs://bucket/prefix/video/
    with ZipFile(zip_path, "r") as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]

        def _task(name: str):
            # Flatten any nested dirs in the zip; keep only basename (mimics `unzip -j`)
            base = os.path.basename(name)
            gcs_key = f"{target_prefix}{base}"
            if _blob_exists(bucket, gcs_key):
                return f"skip exists: {gcs_key}"
            with zf.open(name, "r") as src:
                bio = io.BytesIO(src.read())
                bio.seek(0)
                # Try to guess content type by extension (optional)
                ct = None
                _ = base.lower()
                if _.endswith(".mp4"):
                    ct = "video/mp4"
                elif _.endswith(".webm"):
                    ct = "video/webm"
                _upload_stream(bucket, gcs_key, bio, content_type=ct)
            return f"uploaded: {gcs_key}"

        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(_task, n) for n in names]
            for fut in as_completed(futures):
                msg = fut.result()
                print(msg)


def download_and_upload_csvs(bucket: storage.Bucket, dest_prefix: str) -> None:
    dest_prefix = dest_prefix.rstrip("/") + "/"
    for rel in CSV_PATHS:
        url = f"{OPENVID_BASE}/{rel}"
        gcs_key = f"{dest_prefix}{rel}"
        if _blob_exists(bucket, gcs_key):
            print(f"skip exists: {gcs_key}")
            continue
        print(f"downloading {url}")
        buf = io.BytesIO(_http_get(url, stream=True).content)
        buf.seek(0)
        _upload_stream(bucket, gcs_key, buf, content_type="text/csv")
        print(f"uploaded: gs://{bucket.name}/{gcs_key}")


def process_part(i: int, tmp_dir: str, bucket: storage.Bucket, dest_prefix: str, workers: int) -> None:
    base_zip_url = f"{OPENVID_BASE}/OpenVid_part{i}.zip"
    main_zip_path = os.path.join(tmp_dir, f"OpenVid_part{i}.zip")
    if os.path.exists(main_zip_path):
        print(f"found cached: {main_zip_path}")
    else:
        try:
            print(f"downloading {base_zip_url}")
            _download_to_file(base_zip_url, main_zip_path)
        except Exception as e:
            print(f"direct zip download failed for part {i}: {e} — trying split parts")
            # try split parts aa/ab
            aa_url = f"{OPENVID_BASE}/OpenVid_part{i}_partaa"
            ab_url = f"{OPENVID_BASE}/OpenVid_part{i}_partab"
            aa_path = os.path.join(tmp_dir, f"OpenVid_part{i}_partaa")
            ab_path = os.path.join(tmp_dir, f"OpenVid_part{i}_partab")

            # download parts if not on disk
            if not os.path.exists(aa_path):
                print(f"downloading {aa_url}")
                _download_to_file(aa_url, aa_path)
            if not os.path.exists(ab_path):
                print(f"downloading {ab_url}")
                _download_to_file(ab_url, ab_path)

            print("stitching split parts...")
            _stitch_parts_to_file([aa_path, ab_path], main_zip_path)

    # Stream members to GCS
    try:
        upload_zip_members_to_gcs(main_zip_path, bucket, dest_prefix, workers=workers, subdir="video/")
    except BadZipFile as e:
        raise RuntimeError(f"Corrupt zip for part {i}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download OpenVid-1M and upload decompressed contents to GCS.")
    parser.add_argument("--gcs_uri", required=True, help="Destination like gs://bucket/prefix")
    parser.add_argument("--tmp_dir", default=None, help="Temp directory to use (default: system temp)")
    parser.add_argument("--start", type=int, default=0, help="Start part index (inclusive)")
    parser.add_argument("--end", type=int, default=186, help="End part index (inclusive)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel uploads per zip")
    args = parser.parse_args()

    bucket_name, dest_prefix = parse_gcs_uri(args.gcs_uri)

    tmp_dir = args.tmp_dir or tempfile.mkdtemp(prefix="openvid_zip_")
    os.makedirs(tmp_dir, exist_ok=True)

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Parts
    for i in range(args.start, args.end + 1):
        try:
            print(f"\n=== Processing part {i} ===")
            process_part(i, tmp_dir, bucket, dest_prefix, workers=args.workers)
        except Exception as e:
            print(f"ERROR part {i}: {e}")

    # CSV metadata
    try:
        print("\n=== Uploading CSV metadata ===")
        download_and_upload_csvs(bucket, dest_prefix)
    except Exception as e:
        print(f"ERROR uploading CSVs: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()

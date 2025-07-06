from pathlib import Path

from google.cloud import storage

from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)

# --- Generic GCS helpers -----------------------------------------------------

def _gcs_client(sa_path: str) -> storage.Client:
    return storage.Client.from_service_account_json(sa_path)

def download_from_gcs(
    service_account_json_path: str,
    bucket_name: str,
    prefix: str,
    local_dir: Path,
) -> int:
    """
    Download all blobs under `prefix` in `bucket_name` to `local_dir`.
    Returns number of files downloaded.
    """
    client = _gcs_client(service_account_json_path)
    bucket = client.bucket(bucket_name)
    prefix = prefix.rstrip("/") + "/"
    local_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for blob in bucket.list_blobs(prefix=prefix):
        rel = blob.name[len(prefix):]
        if not rel or rel == ".keep":
            continue
        dest = local_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(dest))
        count += 1

    logger.info("Downloaded %d files from GCS %s/%s", count, bucket_name, prefix)
    return count

def upload_to_gcs(
    service_account_json_path: str,
    bucket_name: str,
    prefix: str,
    local_dir: Path,
) -> int:
    """
    Upload all files under `local_dir` to `bucket_name` at `prefix`.
    Returns number of files uploaded.
    """
    client = _gcs_client(service_account_json_path)
    bucket = client.bucket(bucket_name)
    prefix = prefix.rstrip("/") + "/"

    files = [p for p in local_dir.rglob("*") if p.is_file()]
    for f in files:
        rel = str(f.relative_to(local_dir))
        blob = bucket.blob(f"{prefix}{rel}")
        blob.upload_from_filename(str(f))

    logger.info("Uploaded %d files to GCS %s/%s", len(files), bucket_name, prefix)
    return len(files)
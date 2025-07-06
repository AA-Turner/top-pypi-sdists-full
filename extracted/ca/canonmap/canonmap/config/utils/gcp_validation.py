import os
import json

from google.cloud import storage
from google.api_core.exceptions import Forbidden, NotFound, GoogleAPIError

from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)

class BucketError(Exception):
    """Base exception for bucket validation errors."""
    pass

class BucketNotFoundError(BucketError):
    """Raised when the bucket does not exist and cannot be created."""
    pass

class BucketPermissionError(BucketError):
    """Raised when access to the bucket or prefix is denied."""
    pass

def _emit_gcloud_script(
    project_id: str,
    sa_email: str,
    service_account_json_path: str,
    commands: list[str],
    script_filename: str
) -> str:
    """
    Write a bash script to `canonmap_troubleshooting/<script_filename>`,
    make it executable, and return its path.
    """
    dir_path = "canonmap_troubleshooting"
    os.makedirs(dir_path, exist_ok=True)
    script_path = os.path.join(dir_path, script_filename)
    header = "#!/usr/bin/env bash\n\n" \
             "set -euo pipefail\n\n" \
             f"SERVICE_ACCOUNT_JSON=\"{service_account_json_path}\"\n\n"
    with open(script_path, "w") as f:
        f.write(header)
        for cmd in commands:
            f.write(cmd + "\n")
    os.chmod(script_path, 0o755)
    logger.success("Troubleshooting script created at %s", script_path)
    return script_path

def _load_service_account_info(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        logger.warning("Could not load service account info: %s", e)
        return {}

def validate_service_account_path(gcp_service_account_json_path: str):
    logger.info("Validating service account JSON file path: %s", gcp_service_account_json_path)
    if not os.path.exists(gcp_service_account_json_path):
        logger.error("Service account JSON file not found at %s", gcp_service_account_json_path)
        raise FileNotFoundError(f"Service account JSON file not found at {gcp_service_account_json_path}")
    logger.success(f"Service account JSON file found at {gcp_service_account_json_path}")


def validate_bucket_config(self, troubleshooting: bool = False):
    # verify service-account JSON exists and is valid
    validate_service_account_path(self.gcp_service_account_json_path)
    service_account_path = self.gcp_service_account_json_path
    sa_info = _load_service_account_info(service_account_path)
    sa_email = sa_info.get("client_email", "<SERVICE_ACCOUNT_EMAIL>")
    project_id = sa_info.get("project_id", "<PROJECT_ID>")

    try:
        client = storage.Client.from_service_account_json(self.gcp_service_account_json_path)
    except GoogleAPIError as e:
        logger.error("GCS API error creating client: %s", e)
        raise BucketError(f"GCS API error creating client: {e}")

    # attempt to get or create bucket
    try:
        bucket = client.get_bucket(self.gcp_bucket_name)
        logger.success("Accessed GCP bucket: %s", self.gcp_bucket_name)
    except Forbidden as e:
        logger.error("Permission denied on bucket '%s': %s", self.gcp_bucket_name, e)
        if troubleshooting:
            # build grant-view commands
            cmds = [
                f"gcloud auth activate-service-account --key-file=\"$SERVICE_ACCOUNT_JSON\"",
                f"gcloud config set project {project_id}",
                f"gcloud projects add-iam-policy-binding {project_id} "
                f"--member=\"serviceAccount:{sa_email}\" "
                "--role=\"roles/storage.bucketViewer\"",
                f"gcloud projects add-iam-policy-binding {project_id} "
                f"--member=\"serviceAccount:{sa_email}\" "
                "--role=\"roles/storage.objectViewer\""
            ]
            script = _emit_gcloud_script(
                project_id,
                sa_email,
                self.gcp_service_account_json_path,
                cmds,
                f"fix_permissions_{self.gcp_bucket_name}.sh"
            )
            raise BucketPermissionError(
                f"Permission denied to bucket '{self.gcp_bucket_name}'. "
                f"Troubleshooting script: {script}"
            )
        raise BucketPermissionError(f"Permission denied to bucket '{self.gcp_bucket_name}'")
    except NotFound:
        logger.error("Bucket not found: %s", self.gcp_bucket_name)
        if self.sync_strategy == "none" or not self.auto_create_bucket:
            raise BucketNotFoundError(f"Bucket '{self.gcp_bucket_name}' does not exist")
        try:
            bucket = client.create_bucket(self.gcp_bucket_name)
            logger.success("Created bucket: %s", self.gcp_bucket_name)
        except Forbidden as e:
            logger.error("Permission denied creating bucket '%s': %s", self.gcp_bucket_name, e)
            if troubleshooting:
                cmds = [
                    f"gcloud auth activate-service-account --key-file=\"$SERVICE_ACCOUNT_JSON\"",
                    f"gcloud config set project {project_id}",
                    f"gcloud storage buckets create gs://{self.gcp_bucket_name} "
                    f"--project={project_id}"
                ]
                script = _emit_gcloud_script(
                    project_id,
                    sa_email,
                    self.gcp_service_account_json_path,
                    cmds,
                    f"create_bucket_{self.gcp_bucket_name}.sh"
                )
                raise BucketPermissionError(
                    f"Failed to create bucket '{self.gcp_bucket_name}'. "
                    f"Troubleshooting script: {script}"
                )
            raise BucketPermissionError(f"Failed to create bucket '{self.gcp_bucket_name}'")
    except GoogleAPIError as e:
        logger.error("GCS API error for bucket '%s': %s", self.gcp_bucket_name, e)
        raise BucketError(f"GCS API error for bucket '{self.gcp_bucket_name}': {e}")

    # at this point, `bucket` exists and is accessible
    # now validate or create prefix if specified
    if self.gcp_bucket_prefix:
        prefix = self.gcp_bucket_prefix.rstrip("/") + "/"
        logger.info("Validating bucket prefix: %s", prefix)
        try:
            first_blob = next(bucket.list_blobs(prefix=prefix, max_results=1), None)
        except GoogleAPIError as e:
            logger.error("GCS API error listing blobs for prefix '%s': %s", prefix, e)
            raise BucketError(f"GCS API error listing blobs for prefix '{prefix}': {e}")
        if not first_blob:
            if self.sync_strategy != "none" and self.auto_create_bucket_prefix:
                try:
                    blob = bucket.blob(prefix + ".keep")
                    blob.upload_from_string("", content_type="application/octet-stream")
                    logger.success("Created prefix marker at '%s'", prefix)
                except Forbidden as e:
                    logger.error("Permission denied creating prefix '%s': %s", prefix, e)
                    if troubleshooting:
                        cmds = [
                            f"gcloud auth activate-service-account --key-file=\"$SERVICE_ACCOUNT_JSON\"",
                            f"gcloud config set project {project_id}",
                            f"gcloud projects add-iam-policy-binding {project_id} "
                            f"--member=\"serviceAccount:{sa_email}\" "
                            "--role=\"roles/storage.objectCreator\"",
                            f"touch .keep && "
                            f"gcloud storage cp .keep gs://{self.gcp_bucket_name}/{prefix}.keep"
                        ]
                        script = _emit_gcloud_script(
                            project_id,
                            sa_email,
                            self.gcp_service_account_json_path,
                            cmds,
                            f"create_prefix_{self.gcp_bucket_name}_{self.gcp_bucket_prefix}.sh"
                        )
                        raise BucketPermissionError(
                            f"Failed to create prefix '{prefix}'. "
                            f"Troubleshooting script: {script}"
                        )
                    raise BucketPermissionError(f"Failed to create prefix '{prefix}'")
            else:
                raise BucketNotFoundError(f"No objects found with prefix '{prefix}'")
        logger.success("Bucket prefix validated: %s", prefix)
    else:
        logger.info("No bucket prefix specified, skipping")

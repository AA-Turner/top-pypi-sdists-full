"""GCP Cloud Function: serverless job monitor.

Triggered every 3 minutes by Cloud Scheduler.
Reads job manifests from GCS, checks status, recreates preempted instances.
"""
import json
import logging
import os
from datetime import datetime, timezone

from google.cloud import compute_v1, storage, pubsub_v1, secretmanager_v1

import sys

def _log(msg):
    """Write to stderr for Cloud Run log capture."""
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()

logger = type('L', (), {'info': staticmethod(_log), 'error': staticmethod(_log)})()

PROJECT = os.environ.get("GCP_PROJECT", "wisent-480400")
BUCKET = os.environ.get("JOBS_BUCKET", f"wisent-jobs-{PROJECT}")
ALERTS_TOPIC = os.environ.get("ALERTS_TOPIC", f"projects/{PROJECT}/topics/wisent-job-alerts")
MAX_RESTARTS = 20
ZONE_ROTATION = ["us-central1-b", "us-central1-a", "us-central1-c", "us-central1-f"]

storage_client = storage.Client()
compute_client = compute_v1.InstancesClient()
publisher = pubsub_v1.PublisherClient()


def _now():
    return datetime.now(timezone.utc).isoformat()


def _get_secret(name):
    client = secretmanager_v1.SecretManagerServiceClient()
    resource = f"projects/{PROJECT}/secrets/{name}/versions/latest"
    response = client.access_secret_version(request={"name": resource})
    return response.payload.data.decode("utf-8")


HEARTBEAT_STALE_MINUTES = 15


def _read_status(bucket, job_id):
    blob = storage_client.bucket(bucket).blob(f"status/{job_id}/status")
    if not blob.exists():
        return None
    return blob.download_as_text().strip().split()[0]


def _heartbeat_stale(bucket, job_id):
    """Check if the heartbeat file is older than HEARTBEAT_STALE_MINUTES."""
    blob = storage_client.bucket(bucket).blob(f"status/{job_id}/heartbeat")
    if not blob.exists():
        return False  # No heartbeat yet — instance still starting up
    blob.reload()
    updated = blob.updated
    if updated is None:
        return False
    age_minutes = (datetime.now(timezone.utc) - updated).total_seconds() / 60
    return age_minutes > HEARTBEAT_STALE_MINUTES


def _instance_exists(name, zone):
    try:
        inst = compute_client.get(project=PROJECT, zone=zone, instance=name)
        return inst.status in ("RUNNING", "STAGING", "PROVISIONING")
    except Exception:
        return False


def _terminate_instance(name, zone):
    try:
        compute_client.delete(project=PROJECT, zone=zone, instance=name)
    except Exception:
        pass


def _recreate_instance(job):
    """Recreate a preempted instance from job manifest data."""
    import logging
    logger = logging.getLogger(__name__)
    name = job["instance_ref"].split("@")[0]
    old_zone = job["instance_ref"].split("@")[1] if "@" in job["instance_ref"] else ZONE_ROTATION[0]
    # Delete the TERMINATED instance first (can't reuse the name)
    _terminate_instance(name, old_zone)
    machine_type = job["machine_type"]
    accel_type = job.get("accel_type", "")
    boot_disk_gb = job.get("boot_disk_gb", 200)
    image = job.get("image", "pytorch-2-9-cu129-ubuntu-2204-nvidia-580-v20260408")
    image_project = job.get("image_project", "deeplearning-platform-release")
    startup_script = job.get("startup_script", "")

    for zone in ZONE_ROTATION:
        try:
            disk = compute_v1.AttachedDisk(
                auto_delete=True,
                boot=True,
                initialize_params=compute_v1.AttachedDiskInitializeParams(
                    disk_size_gb=boot_disk_gb,
                    source_image=f"projects/{image_project}/global/images/{image}",
                ),
            )
            network = compute_v1.NetworkInterface(
                access_configs=[compute_v1.AccessConfig(name="External NAT")],
            )
            metadata = compute_v1.Metadata(items=[
                compute_v1.Items(key="startup-script", value=startup_script),
            ])
            scheduling = compute_v1.Scheduling(
                preemptible=False,
                on_host_maintenance="TERMINATE",
            )
            accelerators = []
            if accel_type:
                accelerators.append(compute_v1.AcceleratorConfig(
                    accelerator_type=f"zones/{zone}/acceleratorTypes/{accel_type}",
                    accelerator_count=1,
                ))
            instance = compute_v1.Instance(
                name=name,
                machine_type=f"zones/{zone}/machineTypes/{machine_type}",
                disks=[disk],
                network_interfaces=[network],
                metadata=metadata,
                scheduling=scheduling,
                guest_accelerators=accelerators,
            )
            op = compute_client.insert(project=PROJECT, zone=zone, instance_resource=instance)
            op.result()
            return f"{name}@{zone}"
        except Exception as e:
            if "already exists" in str(e):
                return f"{name}@{zone}"
            continue
    return None


def _alert(message):
    try:
        publisher.publish(ALERTS_TOPIC, message.encode("utf-8"))
    except Exception:
        logger.error(f"Alert dispatch error: {message}")


def monitor_jobs(request=None):
    """Main entry point for Cloud Function."""
    logger.info("Monitor triggered, scanning active batches...")
    bucket = storage_client.bucket(BUCKET)
    blobs = list(bucket.list_blobs(prefix="active/"))

    for blob in blobs:
        if not blob.name.endswith(".json"):
            continue

        manifest = json.loads(blob.download_as_text())
        batch_id = manifest["batch_id"]
        updated = False

        for job in manifest["jobs"]:
            if job["status"] in ("COMPLETED", "FAILED"):
                continue

            job_id = job["job_id"]
            status = _read_status(BUCKET, job_id)
            ref = job["instance_ref"]
            name = ref.split("@")[0]
            zone = ref.split("@")[1] if "@" in ref else ZONE_ROTATION[0]

            if status == "COMPLETED":
                job["status"] = "COMPLETED"
                job["completed_at"] = _now()
                _terminate_instance(name, zone)
                updated = True
                logger.info(f"{batch_id}/{job_id}: COMPLETED")

            elif status == "FAILED":
                job["status"] = "FAILED"
                job["failed_at"] = _now()
                _terminate_instance(name, zone)
                _alert(f"Job {batch_id}/{job_id} FAILED: {job['command']}")
                updated = True
                logger.info(f"{batch_id}/{job_id}: FAILED")

            else:
                exists = _instance_exists(name, zone)
                stale = _heartbeat_stale(BUCKET, job_id)

                if not exists or stale:
                    reason = "preempted" if not exists else "stale heartbeat"
                    restarts = job.get("restarts", 0)
                    if restarts >= MAX_RESTARTS:
                        job["status"] = "FAILED"
                        job["failed_at"] = _now()
                        _alert(f"Job {batch_id}/{job_id} hit restart cap ({MAX_RESTARTS})")
                        updated = True
                        continue

                    logger.info(f"{batch_id}/{job_id}: {reason}, recreating...")
                    if exists:
                        _terminate_instance(name, zone)
                    new_ref = _recreate_instance(job)
                    if new_ref:
                        job["instance_ref"] = new_ref
                        job["restarts"] = restarts + 1
                        job["last_restart"] = _now()
                        updated = True
                        logger.info(f"{batch_id}/{job_id}: recreated ({restarts+1})")
                    else:
                        _alert(f"Job {batch_id}/{job_id} recreation failed in all zones")

        all_done = all(j["status"] in ("COMPLETED", "FAILED") for j in manifest["jobs"])
        if all_done:
            dest = "completed/" if all(j["status"] == "COMPLETED" for j in manifest["jobs"]) else "failed/"
            bucket.blob(f"{dest}{batch_id}.json").upload_from_string(
                json.dumps(manifest, indent=2), content_type="application/json")
            blob.delete()
            n_ok = sum(1 for j in manifest["jobs"] if j["status"] == "COMPLETED")
            n_err = sum(1 for j in manifest["jobs"] if j["status"] == "FAILED")
            _alert(f"Batch {batch_id} done: {n_ok} completed, {n_err} failed")
            logger.info(f"Batch {batch_id}: moved to {dest}")
        elif updated:
            blob.upload_from_string(
                json.dumps(manifest, indent=2), content_type="application/json")

    return "OK"

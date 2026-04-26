"""AWS Lambda: serverless job monitor.

Triggered every 3 minutes by EventBridge.
Reads job manifests from S3, checks status, recreates terminated instances.
"""
import json
import os
import sys
from datetime import datetime, timezone

import boto3

BUCKET = os.environ.get("JOBS_BUCKET", "wisent-jobs")
ALERTS_TOPIC = os.environ.get("ALERTS_TOPIC_ARN", "")
REGION = os.environ.get("AWS_REGION", "us-east-1")
MAX_RESTARTS = 20
AZ_ROTATION = [f"{REGION}a", f"{REGION}c", f"{REGION}d", f"{REGION}b"]

s3 = boto3.client("s3")
ec2 = boto3.client("ec2", region_name=REGION)
ssm = boto3.client("ssm", region_name=REGION)
sns = boto3.client("sns", region_name=REGION) if ALERTS_TOPIC else None


def _log(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


def _now():
    return datetime.now(timezone.utc).isoformat()


def _read_status(bucket, job_id):
    try:
        obj = s3.get_object(Bucket=bucket, Key=f"status/{job_id}/status")
        return obj["Body"].read().decode().strip().split()[0]
    except s3.exceptions.NoSuchKey:
        return None
    except Exception:
        return None


def _heartbeat_stale(bucket, job_id):
    try:
        obj = s3.head_object(Bucket=bucket, Key=f"status/{job_id}/heartbeat")
        modified = obj["LastModified"]
        age_min = (datetime.now(timezone.utc) - modified).total_seconds() / 60
        return age_min > 15
    except Exception:
        return False


def _instance_exists(instance_id):
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        state = resp["Reservations"][0]["Instances"][0]["State"]["Name"]
        return state in ("running", "pending")
    except Exception:
        return False


def _terminate_instance(instance_id):
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
    except Exception:
        pass


def _recreate_instance(job):
    """Recreate a terminated instance from job manifest data."""
    instance_type = job.get("machine_type", "g6e.xlarge")
    ami = job.get("ami", "")
    sg = job.get("security_group", "")
    iam_profile = job.get("iam_profile", "wisent-instance-profile")
    boot_disk_gb = job.get("boot_disk_gb", 200)
    startup_script = job.get("startup_script", "")

    import base64
    user_data_b64 = base64.b64encode(startup_script.encode()).decode()

    for az in AZ_ROTATION:
        try:
            subnets = ec2.describe_subnets(
                Filters=[{"Name": "availability-zone", "Values": [az]}]
            )
            if not subnets["Subnets"]:
                continue
            subnet_id = subnets["Subnets"][0]["SubnetId"]

            resp = ec2.run_instances(
                ImageId=ami,
                InstanceType=instance_type,
                SecurityGroupIds=[sg],
                SubnetId=subnet_id,
                IamInstanceProfile={"Name": iam_profile},
                UserData=user_data_b64,
                BlockDeviceMappings=[{
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "VolumeSize": boot_disk_gb,
                        "VolumeType": "gp3",
                        "DeleteOnTermination": True,
                    },
                }],
                TagSpecifications=[{
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": f"wisent-{job['job_id']}"},
                        {"Key": "JobId", "Value": job["job_id"]},
                    ],
                }],
                MinCount=1, MaxCount=1,
            )
            new_id = resp["Instances"][0]["InstanceId"]
            _log(f"Created {new_id} in {az}")
            return new_id
        except Exception as e:
            if "InsufficientInstanceCapacity" in str(e):
                continue
            _log(f"Launch failed in {az}: {e}")
            continue
    return None


def _alert(message):
    _log(f"ALERT: {message}")
    if sns and ALERTS_TOPIC:
        try:
            sns.publish(TopicArn=ALERTS_TOPIC, Message=message)
        except Exception:
            pass


def handler(event, context):
    """Lambda entry point."""
    _log("Monitor triggered, scanning active batches...")

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix="active/"):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.endswith(".json"):
                continue

            manifest = json.loads(
                s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
            )
            batch_id = manifest["batch_id"]
            updated = False

            for job in manifest["jobs"]:
                if job["status"] in ("COMPLETED", "FAILED"):
                    continue

                job_id = job["job_id"]
                status = _read_status(BUCKET, job_id)
                instance_id = job["instance_ref"]

                if status == "COMPLETED":
                    job["status"] = "COMPLETED"
                    job["completed_at"] = _now()
                    _terminate_instance(instance_id)
                    updated = True
                    _log(f"{batch_id}/{job_id}: COMPLETED")

                elif status == "FAILED":
                    job["status"] = "FAILED"
                    job["failed_at"] = _now()
                    _terminate_instance(instance_id)
                    _alert(f"Job {batch_id}/{job_id} FAILED")
                    updated = True

                else:
                    exists = _instance_exists(instance_id)
                    stale = _heartbeat_stale(BUCKET, job_id)

                    if not exists or stale:
                        reason = "terminated" if not exists else "stale heartbeat"
                        restarts = job.get("restarts", 0)
                        if restarts >= MAX_RESTARTS:
                            job["status"] = "FAILED"
                            job["failed_at"] = _now()
                            _alert(f"{batch_id}/{job_id} hit restart cap")
                            updated = True
                            continue

                        _log(f"{batch_id}/{job_id}: {reason}, recreating...")
                        if exists:
                            _terminate_instance(instance_id)
                        new_id = _recreate_instance(job)
                        if new_id:
                            job["instance_ref"] = new_id
                            job["restarts"] = restarts + 1
                            job["last_restart"] = _now()
                            updated = True
                        else:
                            _alert(f"{batch_id}/{job_id} recreation failed")

            all_done = all(
                j["status"] in ("COMPLETED", "FAILED") for j in manifest["jobs"]
            )
            if all_done:
                dest = "completed/" if all(
                    j["status"] == "COMPLETED" for j in manifest["jobs"]
                ) else "failed/"
                s3.put_object(
                    Bucket=BUCKET,
                    Key=f"{dest}{batch_id}.json",
                    Body=json.dumps(manifest, indent=2),
                )
                s3.delete_object(Bucket=BUCKET, Key=key)
                n_ok = sum(1 for j in manifest["jobs"] if j["status"] == "COMPLETED")
                n_err = len(manifest["jobs"]) - n_ok
                _alert(f"Batch {batch_id} done: {n_ok} ok, {n_err} failed")
            elif updated:
                s3.put_object(
                    Bucket=BUCKET,
                    Key=key,
                    Body=json.dumps(manifest, indent=2),
                )

    return {"statusCode": 200, "body": "OK"}

import binascii
import hashlib
import os


def generate_trace_id(*args) -> int:
    # Create input string similar to Go implementation
    input_str = "".join([str(arg) for arg in args])

    # Generate SHA-256 hash
    hash_obj = hashlib.sha256(input_str.encode())
    hash_hex = hash_obj.hexdigest()

    # Take first 32 characters and convert to bytes
    trace_id_hex = hash_hex[:32]
    trace_id_bytes = binascii.unhexlify(trace_id_hex)

    # Create OpenTelemetry trace ID
    return int.from_bytes(trace_id_bytes, byteorder="big")


def generate_span_id(*args) -> int:
    # Create input string similar to Go implementation
    input_str = "".join([str(arg) for arg in args])

    # Generate SHA-256 hash
    hash_obj = hashlib.sha256(input_str.encode())
    hash_hex = hash_obj.hexdigest()

    # Take characters 16-32 of the hex hash (8 bytes)
    span_id_hex = hash_hex[16:32]
    span_id_bytes = binascii.unhexlify(span_id_hex)

    return int.from_bytes(span_id_bytes, byteorder="big")


def get_job_trace_id() -> int:
    """returns a unique trace id for the job"""
    return generate_trace_id(
        os.environ.get("GITHUB_REPOSITORY", ""),
        os.environ.get("GITHUB_WORKFLOW", ""),
        os.environ.get("GITHUB_JOB", ""),
        os.environ.get("GITHUB_RUN_ID", ""),
        os.environ.get("GITHUB_RUN_NUMBER", ""),
        os.environ.get("GITHUB_RUN_ATTEMPT", ""),
    )


def get_job_span_id() -> int:
    """returns a unique trace id for the job"""
    return generate_span_id(
        os.environ.get("GITHUB_REPOSITORY", ""),
        os.environ.get("GITHUB_WORKFLOW", ""),
        os.environ.get("GITHUB_JOB", ""),
        os.environ.get("GITHUB_RUN_ID", ""),
        os.environ.get("GITHUB_RUN_NUMBER", ""),
        os.environ.get("GITHUB_RUN_ATTEMPT", ""),
        os.environ.get("STEP_ID", ""),
    )


def get_resource_attributes() -> dict[str, str | int]:
    """Returns resource attributes appropriate for
    https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/githubreceiver

    // Not merged into main yet
    https://github.com/krzko/opentelemetry-collector-contrib/blob/feat-add-githubactionseventreceiver/receiver/githubactionsreceiver/trace_event_handling.go
    """
    # We are running within github action
    if os.environ.get("GITHUB_ACTION"):
        return {
            "ci.github.owner": os.environ.get("GITHUB_REPOSITORY_OWNER", ""),
            "ci.github.repository": os.environ.get("GITHUB_REPOSITORY", ""),
            "ci.github.workflow": os.environ.get("GITHUB_WORKFLOW", ""),
            "ci.github.actor": os.environ.get("GITHUB_ACTOR", ""),
            "ci.github.base_ref": os.environ.get("GITHUB_BASE_REF", ""),
            "ci.github.head_ref": os.environ.get("GITHUB_HEAD_REF", ""),
            "ci.github.ref": os.environ.get("GITHUB_REF", ""),
            "ci.github.sha": os.environ.get("GITHUB_SHA", ""),
            "ci.github.job_id": os.environ.get("GITHUB_JOB", ""),
            "ci.github.run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "ci.github.run_number": os.environ.get("GITHUB_RUN_NUMBER", ""),
            "ci.github.run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
            "ci.github.event_name": os.environ.get("GITHUB_EVENT_NAME", ""),
            "ci.github.url": f"{os.environ.get('GITHUB_SERVER_URL')}/{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{os.environ.get('GITHUB_RUN_ID')}",
            "ci.github.step_id": os.environ.get("STEP_ID", ""),
        }
    return {}

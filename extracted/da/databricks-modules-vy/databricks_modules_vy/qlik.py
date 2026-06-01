import time
import sys
import json
from enum import Enum

from qsaas.qsaas import Tenant


def execute_qlikcloud_task(appid, api_key, tenant, tenant_id, max_queue_time = 60*5):
    """
    Uses the qsaas library to reload a Qlik Sense Cloud app
    https://github.com/eapowertools/qsaas

    Parameters:
        appid (string): Appid for the task to run
        api_key (string): Api key for Qlik Sense Cloud
        tenant (string): Qlik tenant name
        tenant_id (string): Qlik tenant id
        max_queue_time (int): Max minutes a task can stay queued before failing. Default 5 minutes.

    """

    # Create connection
    q = Tenant(
        api_key=api_key,
        tenant=tenant,
        tenant_id=tenant_id,
    )

    # Trigger Qlik Cloud
    response = q.post("reloads", json.dumps({"appId": appid}))
    session_id = response["id"]

    # Check status every 10sec
    status = None
    start_time = time.time()
    while status not in ["SUCCEEDED", "FAILED"]:
        if status == "QUEUED" and time.time() - start_time > max_queue_time:
            queued_time = time.time() - start_time
            raise Exception(
                f"Error: Task was QUEUED for {queued_time} seconds. Marking task as failed"
            )

        time.sleep(10)
        # Retry if 500 error
        try:
            temp_response = q.get("reloads/" + session_id)
        except Exception as e:
            if e.args[0] == 500:
                # Wait 30 seconds until retry
                print(f"Warning: Qlik API 500 error while polling {session_id}, retrying in 30s...")
                time.sleep(30)
                continue
            else:
                raise

        status = temp_response["status"]

    if status == "FAILED":
        error_msg = temp_response["log"]
        raise Exception(
            f"""Error: Qlik task did not finish successfully. Status: {status}. Marking task as FAILED. Qlik Error message: \n{error_msg}"""
        )


if __name__ == "__main__":
    app_id = sys.argv[1]
    api_key = sys.argv[2]
    execute_qlikcloud_task(app_id, api_key)

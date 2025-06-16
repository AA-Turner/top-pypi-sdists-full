import time
import sys
import json
from enum import Enum

from qsaas.qsaas import Tenant


def execute_qlikcloud_task(appid, api_key, tenant, tenant_id):
    """
    Uses the qsaas library to reload a Qlik Sense Cloud app
    https://github.com/eapowertools/qsaas

    Parameters:
        appid (string): Appid for the task to run
        api_key (string): Api key for Qlik Sense Cloud
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
        # Allows the status to be QUEUED for > 5 minutes (60 * 5)
        if status == "QUEUED" and time.time() - start_time > 60 * 5:
            queued_time = time.time() - start_time
            raise Exception(
                f"Error: Task was QUEUED for {queued_time} seconds. Marking task as failed"
            )

        time.sleep(10)
        temp_response = q.get("reloads/" + session_id)
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

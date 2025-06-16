from __future__ import annotations
from .logging import lp
import time
import requests
import sys


def _start_snaplogic_task(url, bearer_token, params={}):
    """
    The function starts a SnapLogic task using the API described here:
    https://docs-snaplogic.atlassian.net/wiki/spaces/SD/pages/993296417/Running+a+Triggered+Task

    In order to start a snaplogic pipeline using a triggered task with a GET request without
    waiting for the pipeline to finish, you have to add an API response using two snaps that return:
        {
        "status":
        200
        "ruuid":
        "<the ruuid of the task run>"
        }
    The relevant snaps can be found in one of the SnapLogic pipelines that currently use airflow.

    Parameters:
        url (string):           The url of the task to be started
        bearer_token (string):  The bearer_token of the Snaplogic task
        params (dict):          The pipeline parameters to send to the SnapLogic task

    Returns:
        ruuid (string):         The id of the task run
    """
    lp("Starting SnapLogic task...")
    response = requests.get(
        url, headers={"Authorization": f"Bearer {bearer_token}"}, timeout=60, params=params
    )
    lp(response.json())  # Log the response object for debugging purposes

    try:
        # Attempt to extract 'ruuid' information from the response JSON
        try:
            ruuid = response.json()[0]["ruuid"]

        # Reminder to add JSON-generator and Mapper for the 200 API response
        except:
            lp(
                "Have you remembered to add API-resposne in Snaplogic? JSON-Generator-snap + Mapper-snap for an 200 API response"
            )
            raise Exception(response.json())

    except:
        # If the extraction fails, raise an exception with the entire response object
        raise Exception(response.json())

    lp("SnapLogic task started")
    return ruuid


def _get_snaplogic_task_state(org_name, snaplogic_basic_token, ruuid):
    """
    The function retrieves the state of a SnapLogic task.
    The states of a SnapLogic task can be one of the following:
    Queued:     Pipeline is queued for processing, all Pipelines start in this state.
    NoUpdate:   Intermediate state at startup.
    Prepared:   Pipeline has been prepared.
    Started:    Pipeline has started execution.
    Completed:  Pipeline has completed successfully.
    Failing:    Pipeline execution encountered an error and is waiting for Snaps to complete execution before moving to the Failed state.
    Failed:     Pipeline failed.
    Stopped:    Pipeline was stopped, by user or by the system, indicated by the "stopper" key.
    Stopping:   Pipeline is stopping.
    Suspending: Resumable Pipeline has encountered an error and is storing its state.
    Suspended:  Resumable Pipeline has encountered an error and is suspended.
    Resuming:   Resumable Pipeline is loading its state and will soon resume execution where it left off.

    The API is decribed here: https://docs-snaplogic.atlassian.net/wiki/spaces/SD/pages/2432598066/Retrieve+Info+About+a+Task

    Parameters:
        org_name (string):              The name of the SnapLogic environment
        ruuid (string):                 The id of the task run to get the state from
        snaplogic_basic_token (string): The token for Snaplogic

    Returns:
        state (string):                 The state of the snaplogic task run
    """
    n_retries = 0
    while n_retries < 3:
        try:
            response = requests.get(
                f"https://elastic.snaplogic.com/api/1/rest/public/runtime/{org_name}/{ruuid}",
                headers={"Authorization": f"Basic {snaplogic_basic_token}"},
                timeout=60,
            )
            state = response.json()["response_map"]["state"]
            reason = response.json()["response_map"]["reason"]
            return state, reason
        except requests.exceptions.ReadTimeout:
            n_retries += 1
            lp(f"Read timeout. Retry ({n_retries}/3)")

    raise Exception("Fetching snaplogic task state failed 3 times.")


def _wait_for_snaplogic_task_to_finish(org_name, snaplogic_basic_token, ruuid):
    """
    The function polls the SnapLogic task run every 10 seconds until the run has finished.

    Parameters:
        org_name (string):              The name of the SnapLogic environment
        ruuid (string):                 The id of the task run to get the state from
        snaplogic_basic_token (string): The token for Snaplogic
    """
    start_time = time.time()
    state, reason = _get_snaplogic_task_state(org_name, snaplogic_basic_token, ruuid)
    print_state = True
    while state in (
        "Queued",
        "NoUpdate",
        "Prepared",
        "Started",
        "Failing",
        "Stopping",
        "Suspending",
        "Resuming",
    ):
        if print_state:
            lp(f"Current state on SnapLogic task: {state}")
        time.sleep(10)
        new_state, reason = _get_snaplogic_task_state(org_name, snaplogic_basic_token, ruuid)
        if new_state == state:  # Print state only if there is a different new state
            print_state = False
        state = new_state
    minutes, seconds = divmod(time.time() - start_time, 60)
    lp(f"Pipeline completed in {minutes:.0f} minutes and {seconds:.0f} seconds")
    lp(f"Final state: {state}")
    if state == "Failed":
        lp("The snaplogic pipeline failed with the following reason:")
        lp(reason)
        raise Exception("The snaplogic pipeline failed")
    elif state == "Stopped":
        raise Exception("The snaplogic pipeline stopped")
    elif state == "Suspended":
        raise Exception("The snaplogic pipeline suspended")


def execute_snaplogic_task(url, bearer_token, org_name, snaplogic_basic_token, params={}):
    """
    The function starts a SnapLogic task, and then waits for the task to finish.
    In order to start a snaplogic pipeline using a triggered task with a GET request
    without waiting for the pipeline to finish, you have to add an API response using two snaps that return:
        {
        "status":
        200
        "ruuid":
        "<the ruuid of the task run>"
        }
    The relevant snaps can be found in one of the SnapLogic pipelines that currently use airflow.
    This function is the only function that should be called from outside this script.

    Parameters:
        url (string):                   The url of the task to be started
        bearer_token (string):          The bearer_token of the Snaplogic task
        org_name (string):              The name of the SnapLogic environment
        params (dict):                  The pipeline parameters to send to the SnapLogic task
    """
    ruuid = _start_snaplogic_task(url, bearer_token, params)
    _wait_for_snaplogic_task_to_finish(org_name, snaplogic_basic_token, ruuid)


if __name__ == "__main__":
    snap_org = "Vy_Utvikling" if env == "test" else "Vy_Produksjon"
    secret_scope = sys.argv[1]
    lp(f"Running pipeline with scope: {secret_scope}")
    params = {}
    if len(sys.argv) > 2:
        params = {key.strip(): value.strip() for key, value in [p.split("|") for p in sys.argv[2:]]}
        lp(f"Params: {params}")
    execute_snaplogic_task(url, token, snap_org, snaplogic_basic_token, params)

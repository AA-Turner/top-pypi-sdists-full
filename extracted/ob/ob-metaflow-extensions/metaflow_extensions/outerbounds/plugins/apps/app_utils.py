from metaflow.exception import MetaflowException
import os
from metaflow.metaflow_config_funcs import init_config
import requests
import time
import random

# IMPORTANT: Currently contents of this file are mostly duplicated from the outerbounds package.
# This is purely due to the time rush of having to deliver this feature. As a fast forward, we
# will reorganize things in a way that the amount of duplication in minimum.


APP_READY_POLL_TIMEOUT_SECONDS = 300
# Even after our backend validates that the app routes are ready, it takes a few seconds for
# the app to be accessible via the browser. Till we hunt down this delay, add an extra buffer.
APP_READY_EXTRA_BUFFER_SECONDS = 30


def start_app(port=-1, name=""):
    """
    Starts an app on the workstation.
    List workstations, looks for "NamedPorts", then makes an update call to the NamedPorts for the workstation.
    """
    if len(name) == 0 or len(name) >= 20:
        raise MetaflowException("App name should not be more than 20 characters long.")
    elif not name.isalnum() or not name.islower():
        raise MetaflowException(
            "App name can only contain lowercase alphanumeric characters."
        )

    if "WORKSTATION_ID" not in os.environ:
        raise MetaflowException(
            "All outerbounds app commands can only be run from a workstation."
        )

    # Every workstation has this environment variable set.
    workstation_id = os.environ["WORKSTATION_ID"]

    try:
        try:
            conf = init_config()
            metaflow_token = conf["METAFLOW_SERVICE_AUTH_KEY"]
            api_url = conf["OBP_API_SERVER"]

            workstations_response = requests.get(
                f"https://{api_url}/v1/workstations",
                headers={"x-api-key": metaflow_token},
            )
            workstations_response.raise_for_status()
        except:
            raise MetaflowException("Failed to list workstations!")

        workstations_json = workstations_response.json()["workstations"]
        for workstation in workstations_json:
            if workstation["instance_id"] == os.environ["WORKSTATION_ID"]:
                if "named_ports" in workstation["spec"]:
                    try:
                        ensure_app_start_request_is_valid(
                            workstation["spec"]["named_ports"], port, name
                        )
                    except ValueError as e:
                        raise MetaflowException(str(e))

                    for named_port in workstation["spec"]["named_ports"]:
                        if int(named_port["port"]) == port:
                            if named_port["enabled"] and named_port["name"] == name:
                                print(f"App {name} started on port {port}!")
                                print(
                                    f"Browser URL: https://{api_url.replace('api', 'ui')}/apps/{os.environ['WORKSTATION_ID']}/{name}/"
                                )
                                print(
                                    f"API URL: https://{api_url}/apps/{os.environ['WORKSTATION_ID']}/{name}/"
                                )
                                return
                            else:
                                try:
                                    response = requests.put(
                                        f"https://{api_url}/v1/workstations/update/{workstation_id}/namedports",
                                        headers={"x-api-key": metaflow_token},
                                        json={
                                            "port": port,
                                            "name": name,
                                            "enabled": True,
                                        },
                                    )

                                    response.raise_for_status()
                                    poll_success = wait_for_app_port_to_be_accessible(
                                        api_url,
                                        metaflow_token,
                                        workstation_id,
                                        name,
                                        APP_READY_POLL_TIMEOUT_SECONDS,
                                    )
                                    if poll_success:
                                        print(f"App {name} started on port {port}!")
                                        print(
                                            f"Browser URL: https://{api_url.replace('api', 'ui')}/apps/{os.environ['WORKSTATION_ID']}/{name}/"
                                        )
                                        print(
                                            f"API URL: https://{api_url}/apps/{os.environ['WORKSTATION_ID']}/{name}/"
                                        )
                                    else:
                                        raise MetaflowException(
                                            f"The app could not be deployed in {APP_READY_POLL_TIMEOUT_SECONDS / 60} minutes. Please try again later."
                                        )
                                except Exception:
                                    raise MetaflowException(
                                        f"Failed to start app {name} on port {port}!"
                                    )
    except Exception as e:
        raise MetaflowException(f"Failed to start app {name} on port {port}!")


def ensure_app_start_request_is_valid(existing_named_ports, port: int, name: str):
    """
    Ensures that the port number is available on the workstation and that an app of
    the same name is not already opened on a different port.

    Args:
        existing_named_ports: A list of named ports on the workstation.
        port: The port number to check.
        name: The name of the app to check.
    """
    existing_apps_by_port = {np["port"]: np for np in existing_named_ports}

    if port not in existing_apps_by_port:
        raise MetaflowException(f"Port {port} not found on workstation")

    for existing_named_port in existing_named_ports:
        if (
            name == existing_named_port["name"]
            and existing_named_port["port"] != port
            and existing_named_port["enabled"]
        ):
            raise MetaflowException(
                f"App with name '{name}' is already deployed on port {existing_named_port['port']}"
            )


def wait_for_app_port_to_be_accessible(
    api_url, metaflow_token, workstation_id, app_name, poll_timeout_seconds
) -> bool:
    """
    Waits for the app to be ready by polling the workstation status.
    """
    num_retries_per_request = 3
    start_time = time.time()
    retry_delay = 1.0
    poll_interval = 10
    wait_message = f"App {app_name} is currently being deployed..."
    while time.time() - start_time < poll_timeout_seconds:
        for _ in range(num_retries_per_request):
            try:
                workstations_response = requests.get(
                    f"https://{api_url}/v1/workstations",
                    headers={"x-api-key": metaflow_token},
                )
                workstations_response.raise_for_status()
                if is_app_ready(workstations_response.json(), workstation_id, app_name):
                    print(wait_message)
                    time.sleep(APP_READY_EXTRA_BUFFER_SECONDS)
                    return True
                else:
                    print(wait_message)
                    time.sleep(poll_interval)
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
            ):
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay for the next attempt
                retry_delay += random.uniform(0, 1)  # Add jitter
                retry_delay = min(retry_delay, 10)
    return False


def is_app_ready(response_json: dict, workstation_id: str, app_name: str) -> bool:
    """Checks if the app is ready in the given workstation's response."""
    workstations = response_json.get("workstations", [])
    for workstation in workstations:
        if workstation.get("instance_id") == workstation_id:
            hosted_apps = workstation.get("status", {}).get("hosted_apps", [])
            for hosted_app in hosted_apps:
                if hosted_app.get("name") == app_name:
                    return bool(hosted_app.get("ready"))
    return False

import os
from ..exceptions import MissingConfigurationException

# Can be called during an initalization event of a locust test to
# procedurally generate Appian credentials


def procedurally_generate_credentials(CONFIG: dict) -> None:
    """
    Helper method that can be used to procedurally generate a set of Appian user credentials

    Note: This class must be called in the UserActor class of your Locust test in order to create
    the credentials before any Locust users begin to pick them up.

    Args:
        CONFIG: full locust config dictionary, AKA the utls.c variable in locust tests Make sure the following keys are present.
        procedural_credentials_prefix: Base string for each generated username
        procedural_credentials_count: Appended to prefix, will create 1 -> Count+1 users
        procedural_credentials_password: String which will serve as the password for all users

    Returns:
        None

    """
    required_keys = [
        "procedural_credentials_prefix",
        "procedural_credentials_count",
        "procedural_credentials_password",
    ]
    missing_keys = [key for key in required_keys if key not in CONFIG]
    if missing_keys:
        raise MissingConfigurationException(missing_keys)

    if "credentials" not in CONFIG:
        CONFIG["credentials"] = []
    for i in range(CONFIG["procedural_credentials_count"]):
        creds = [
            CONFIG["procedural_credentials_prefix"] + str(int(i) + 1),
            CONFIG["procedural_credentials_password"],
        ]
        CONFIG["credentials"].append(creds)

    if not CONFIG["credentials"]:
        raise Exception("Something went wrong while attempting to procedurally generate Appian credentials. Please verify all relevant configuration.")


def setup_distributed_creds(CONFIG: dict) -> dict:
    """
    Helper method to distribute Appian credentials across separate load drivers when running Locust in distributed mode.
    Credential pairs will be passed out in Round Robin fashion to each load driver.

    Note: This class must be called in the UserActor class of your Locust test to ensure that the "credentials" key is
    prepared before tests begin.

    Note: If fewer credential pairs are provided than workers, credentials will be distributed to workers in a Modulo fashion.

    Args:
        CONFIG: full locust config dictionary, AKA the utls.c variable in locust tests Make sure the following keys are present.

    Returns:
        CONFIG: same as input but with credentials key updated to just the subset of credentials required for given load driver.

    """
    if 'credentials' not in CONFIG:
        raise MissingConfigurationException(['credentials'])

    # STY is the envrionment variable to identify which 'screen' subprocess we are running in. There will be one unique STY name
    # per load driver when running in distributed mode.
    session_name = os.getenv("STY")
    if session_name and "locustdriver" in session_name:
        # The variable will look like "12345.locustdriver-2-0"
        num_workers, worker_id = map(int, session_name.split("locustdriver-")[1].split("-"))
        credentials_subset = CONFIG['credentials'][worker_id % (len(CONFIG['credentials']))::num_workers]
        if len(credentials_subset) > 0:
            CONFIG['credentials'] = credentials_subset
    return CONFIG['credentials']

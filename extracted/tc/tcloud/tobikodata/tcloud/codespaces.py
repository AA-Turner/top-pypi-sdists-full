import os


def is_in_codespace() -> bool:
    """
    Check if the current environment is a GitHub codespace.
    """
    env_var = os.getenv("CODESPACES")
    if env_var:
        return env_var == "true"
    return False

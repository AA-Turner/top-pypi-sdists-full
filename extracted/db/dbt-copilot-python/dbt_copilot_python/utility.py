import os


def is_copilot():
    """Are we running in an AWS Copilot provisioned environment?"""
    return "COPILOT_ENVIRONMENT_NAME" in os.environ

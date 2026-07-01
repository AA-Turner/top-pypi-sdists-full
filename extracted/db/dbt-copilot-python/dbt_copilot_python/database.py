import json
import os


def setup_database(environment_key, **extra_keys):
    """Take a Copilot database environment variable and return the django
    configuration."""
    config = json.loads(os.environ[environment_key])

    return {
        "ENGINE": f"django.db.backends.{config['engine']}",
        "NAME": config["dbname"],
        "USER": config["username"],
        "PASSWORD": config["password"],
        "HOST": config["host"],
        "PORT": config["port"],
        **extra_keys,
    }


def database_from_env(environment_key, **extra_keys):
    """
    Set up the default django database from a Copilot database environment
    variable.

    Usage in settings.py:

    DATABASES = database_from_env("MY_DATABASE")
    """

    return {"default": setup_database(environment_key, **extra_keys)}


def database_url_from_env(environment_key):
    """
    Set up the default database URL from a Copilot database environment
    variable.

    Usage in settings.py:

    DATABASES = { 'default': dj_database_url.config(default=database_url_from_env("MY_DATABASE")) }
    """
    config = json.loads(os.environ[environment_key])

    return "{engine}://{username}:{password}@{host}:{port}/{dbname}".format(**config)

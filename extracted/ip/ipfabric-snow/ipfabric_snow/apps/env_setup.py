import getpass
from typing import Dict, Tuple, TypedDict

import typer
from rich.prompt import Prompt
from ipfabric_snow.utils.env_manager import EnvManager
from ipfabric_snow.utils.logger import ipf_logger as logger

ENV_VARS = ["IPF_URL", "IPF_TOKEN", "SNOW_URL", "SNOW_TOKEN"]
OPTIONAL_ENV_VARS = ["IPF_USER", "IPF_PASS", "SNOW_PASS", "SNOW_USER"]

env_setup_app = typer.Typer()


class SensitiveVars(TypedDict, total=False):
    SNOW_USER: str
    SNOW_PASS: str
    SNOW_TOKEN: str
    IPF_USER: str
    IPF_PASS: str
    IPF_TOKEN: str


def get_auth(env_vars):
    token = env_vars.get("SNOW_TOKEN")
    username = env_vars.get("SNOW_USER")
    password = env_vars.get("SNOW_PASS")

    if token:
        return token
    elif username and password:
        return username, password
    else:
        raise ValueError("Incomplete authentication credentials")


def handle_auth(service_name, env_vars, env_vars_to_write, store_sensitive=False):
    logger.debug(f"Entering handle_auth with service_name: {service_name}")
    user_var = f"{service_name}_USER"
    pass_var = f"{service_name}_PASS"
    token_var = f"{service_name}_TOKEN"

    service_user = env_vars.get(user_var)
    service_pass = env_vars.get(pass_var)
    service_token = env_vars.get(token_var)

    sensitive_vars = {}
    if not (service_token or (service_user and service_pass)):
        auth_option = Prompt.ask(
            f"Username and password or token for {service_name.replace('_', ' ')}?\nPlease enter 'user' or 'token'. Default is token.\n",
            choices=["user", "token"],
            default="token",
        )
        if auth_option == "user":
            service_user = typer.prompt(f"Please enter the {user_var} value")
            service_pass = getpass.getpass(f"Please enter the {pass_var} value:")
            sensitive_vars.update({user_var: service_user, pass_var: service_pass})
            if store_sensitive:
                env_vars_to_write.update(
                    {user_var: service_user, pass_var: service_pass}
                )
        else:
            service_token = getpass.getpass(f"Please enter the {token_var} value:")
            sensitive_vars.update({token_var: service_token})
            if store_sensitive:
                env_vars_to_write.update({token_var: service_token})

    logger.debug(
        f"Exiting handle_auth with env_vars_to_write: {env_vars_to_write.keys()}"
    )
    return env_vars_to_write, sensitive_vars


def setup_environment():
    logger.info("Setting up the environment")
    env_manager = EnvManager()
    env_vars = env_manager.read_env_file()

    env_vars_to_write = {}
    sensitive_vars = {}
    for service_name in ["SNOW", "IPF"]:
        updated_env_vars, updated_sensitive_vars = handle_auth(
            service_name, env_vars, env_vars_to_write, store_sensitive=False
        )
        sensitive_vars.update(updated_sensitive_vars)

    for var in ["IPF_URL", "SNOW_URL"]:
        logger.debug(f"Checking for {var}")
        value = env_vars.get(var) or typer.prompt(f"Please enter the {var} value")
        env_vars_to_write.update({var: value})

    store_sensitive = typer.confirm(
        "Do you want to store sensitive data (passwords, tokens) in the .env file?"
    )
    if store_sensitive:
        env_vars_to_write.update(sensitive_vars)

    env_manager.write_env_file(env_vars_to_write)
    logger.info("Environment setup complete")

    return sensitive_vars


@env_setup_app.command("setup", help="Prompt to help Setup the environment variables")
def initialize_env():
    setup_environment()


def validate_env(sensitive_vars: SensitiveVars = None) -> Tuple[bool, Dict[str, str]]:
    logger.info("Validating the environment")
    env_manager = EnvManager()
    env_vars = env_manager.read_env_file()

    if sensitive_vars:
        env_vars.update(sensitive_vars)

    missing_vars = []
    for service_name in ["SNOW", "IPF"]:
        user_var = f"{service_name}_USER"
        pass_var = f"{service_name}_PASS"
        token_var = f"{service_name}_TOKEN"

        if not (
            env_vars.get(token_var)
            or (env_vars.get(user_var) and env_vars.get(pass_var))
        ):
            missing_vars.extend([user_var, pass_var, token_var])

    for var in ["IPF_URL", "SNOW_URL"]:
        if not env_vars.get(var):
            missing_vars.append(var)

    logger.info("Environment validation complete")
    if missing_vars:
        logger.warning(f"Missing variables: {', '.join(missing_vars)}")
        return False, {var: env_vars.get(var) for var in missing_vars}
    else:
        logger.info("All necessary environment variables are set.")
    return True, {var: env_vars.get(var) for var in ENV_VARS + OPTIONAL_ENV_VARS}


def ensure_environment_is_setup():
    check, env_vars = validate_env()
    if not check:
        logger.error(f"Missing environment variables: {env_vars.keys()}")
        should_setup = typer.confirm(
            "The environment is not properly set up. Would you like to set it up now?"
        )
        if should_setup:
            sensitive_vars = setup_environment()
            check, env_vars = validate_env(sensitive_vars)
            if not check:
                logger.error(
                    f"Environment setup failed. Missing environment variables: {env_vars.keys()}"
                )
                raise typer.Exit(code=1)
        else:
            logger.info(
                f"Run ipf-serviceNow env setup to setup the environment manually."
            )
            raise typer.Exit(code=1)
    else:
        sensitive_vars = {}
    all_vars = {**env_vars, **sensitive_vars}
    return all_vars

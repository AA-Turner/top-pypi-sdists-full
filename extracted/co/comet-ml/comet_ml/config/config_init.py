# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import logging
import os
import os.path
from typing import Any, Dict, Optional, Tuple

from ..exceptions import AnonymousModeException, InvalidAPIKey, Unauthorized
from ..logging_messages import (
    COMET_INIT_DEPRECATED,
    CONFIG_ANONYMOUS_ARGUMENT_DEPRECATED,
    CONFIG_ANONYMOUS_MODE_DISCONTINUED,
    CONFIG_API_KEY_CHECK_FAILED,
    CONFIG_API_KEY_IS_INVALID,
    CONFIG_API_KEY_IS_NOT_SET,
    CONFIG_API_KEY_SAVE_FAILED_WARNING,
    CONFIG_INIT_ONPREM_FAILED_EXCEPTION,
    CONFIG_INIT_ONPREM_START_INFO,
    CONFIG_INIT_ONPREM_USER_INPUT_INFO,
)
from ..utils import get_api_key_from_user, get_root_url, is_interactive, sanitize_url
from .config_api import get_api_key, get_comet_url_override, get_config
from .config_class import Config, _input_user
from .config_constants import COMET_ROOT_URL
from .config_helper import config_path_from_directory, get_default_config_path
from .config_io import api_key_save

LOGGER = logging.getLogger(__name__)


def login(
    directory: Optional[str] = None,
    force: Optional[bool] = False,
    anonymous: Optional[bool] = None,
    **settings: Any
) -> None:
    """An easy, safe, interactive way to set and save your Comet settings.

    Will ask for your api_key if not already set. Your
    api_key will not be shown.

    Args:
        directory (str): The location to save the
            .comet.config file. Typical values are "~/" (home)
            and "./" (current directory). Default is "~/" or
            COMET_CONFIG, if set.
        force (bool): If True, forces the user to
            enter required information, such as the api key.
        anonymous (bool): Deprecated. Anonymous mode has been discontinued,
            passing True raises an error.
        settings (Any): Any valid setting and value.

    Notes:
        Valid settings include: `api_key`, `disable_auto_logging`, `experiment_key`,
        `offline_directory`, `workspace`, `project_name`, `logging_console`, `logging_file`,
        `logging_file_level`, `logging_file_overwrite`, `timeout_cleaning`, `timeout_upload`.

    Example:
        ```python
        import comet_ml
        comet_ml.login()
        ```
    """
    _init(directory=directory, force=force, anonymous=anonymous, settings=settings)


def init(
    directory: Optional[str] = None,
    force: Optional[bool] = False,
    anonymous: Optional[bool] = None,
    **settings: Any
) -> None:
    """
    Deprecated. Use comet_ml.login() instead.
    """
    LOGGER.warning(COMET_INIT_DEPRECATED)
    _init(directory=directory, force=force, anonymous=anonymous, settings=settings)


def _init_get_api_key(
    prompt_user: bool,
    settings: Dict[str, Any],
    config: Config,
    force: bool = False,
) -> Tuple[Optional[str], bool]:
    need_to_save = False
    if "api_key" in settings:
        api_key = settings.pop("api_key", None)
        if api_key is not None:
            need_to_save = True
    elif not force:
        api_key = config.get_string(None, "comet.api_key")
    else:
        api_key = None

    if api_key is None:
        if prompt_user:
            api_key = get_api_key_from_user()
            if api_key is not None:
                need_to_save = True

    return api_key, need_to_save


def _check_api_key_validity(api_key: str, config: Config) -> None:
    # check that provided api_key is in correct format
    parsed_api_key = get_api_key(api_key, config)
    if parsed_api_key is None:
        raise InvalidAPIKey(api_key, get_comet_url_override(config))

    from ..api import API

    try:
        API(api_key=api_key).get_account_details()
    except Unauthorized:
        raise InvalidAPIKey(api_key, get_comet_url_override(config))


def _init(
    directory: Optional[str] = None,
    should_prompt_user: Optional[bool] = None,
    anonymous: Optional[bool] = None,
    settings: Optional[Dict[str, Any]] = None,
    force: Optional[bool] = False,
) -> None:

    if anonymous:
        raise AnonymousModeException(CONFIG_ANONYMOUS_MODE_DISCONTINUED)
    if anonymous is not None:
        LOGGER.warning(CONFIG_ANONYMOUS_ARGUMENT_DEPRECATED)

    if settings is None:
        settings = {}

    if force is None:
        force = False

    # We only save the api_key if given by parameter, or
    # by getpass. We don't save it if in the environment

    config = get_config()
    config_path = (
        config_path_from_directory(directory)
        if directory is not None
        else get_default_config_path()
    )

    if should_prompt_user is None:
        should_prompt_user = is_interactive()

    _check_and_save_api_key(
        config=config,
        config_path=config_path,
        should_prompt_user=should_prompt_user,
        settings=settings,
        force=force,
    )

    if len(settings) > 0:
        # Set in environment to save:
        config._set_settings(settings, environ=True)


def _check_and_save_api_key(
    config: Config,
    config_path: str,
    settings: Dict[str, Any],
    should_prompt_user: bool = False,
    force: bool = False,
) -> bool:

    api_key, need_to_save = _init_get_api_key(
        prompt_user=should_prompt_user,
        settings=settings,
        config=config,
        force=force,
    )

    if api_key is None:
        LOGGER.info(CONFIG_API_KEY_IS_NOT_SET)
        return False

    try:
        _check_api_key_validity(api_key, config)
    except InvalidAPIKey:
        LOGGER.error(
            CONFIG_API_KEY_IS_INVALID,
            api_key,
            get_comet_url_override(config),
            exc_info=True,
        )
        return False
    except Exception:
        LOGGER.error(CONFIG_API_KEY_CHECK_FAILED, exc_info=True)
        return False

    # From here we know that the API Key is valid for the configured Comet installation

    if need_to_save:
        try:
            api_key_save(config_path, api_key)
        except Exception:
            LOGGER.warning(CONFIG_API_KEY_SAVE_FAILED_WARNING, exc_info=True)

    return True


def init_onprem(force: bool = False) -> None:

    if force:
        for var in ["COMET_OPTIMIZER_URL", "COMET_URL_OVERRIDE", "COMET_API_KEY"]:
            if var in os.environ:
                del os.environ[var]

    config = get_config()
    config_path = get_default_config_path()

    client_url = get_comet_url_override(config)

    root_url = sanitize_url(get_root_url(client_url))

    if root_url == COMET_ROOT_URL or force:
        LOGGER.info(CONFIG_INIT_ONPREM_START_INFO)

        client_url = _input_user(CONFIG_INIT_ONPREM_USER_INPUT_INFO)

        # Set the environment variables, config.save will save them in the local config file
        os.environ["COMET_URL_OVERRIDE"] = client_url

    # We currently force the user confirmation, but it might hang
    # if not in a TTY
    config.save(_prompt_user_confirmation=True, force=force)

    try:
        _check_and_save_api_key(
            config=config,
            config_path=config_path,
            should_prompt_user=True,
            settings={},
            force=force,
        )
    except Exception:
        raise Exception(CONFIG_INIT_ONPREM_FAILED_EXCEPTION)

import os
import json
from typing import Tuple, Union

import requests
from .utils import safe_requests_wrapper
from .exceptions import OuterboundsConfigurationException


class PerimeterExtractor:

    config = None

    @classmethod
    def for_ob_cli(
        cls, config_dir: str, profile: str
    ) -> Union[Tuple[str, str], Tuple[None, None]]:
        """
        This function will be called when we are trying to extract the perimeter
        via the ob cli's execution. We will rely on the following logic:
        1. check environment variables like OB_CURRENT_PERIMETER / OBP_PERIMETER
        2. run init config to extract the perimeter related configurations.

        Returns
        -------
            Tuple[str, str] : Tuple containing perimeter name , API server url.
        """
        from outerbounds.utils import metaflowconfig

        perimeter = None
        api_server = None
        if os.environ.get("OB_CURRENT_PERIMETER") or os.environ.get("OBP_PERIMETER"):
            perimeter = os.environ.get("OB_CURRENT_PERIMETER") or os.environ.get(
                "OBP_PERIMETER"
            )

        if os.environ.get("OBP_API_SERVER"):
            api_server = os.environ.get("OBP_API_SERVER")

        if perimeter is None or api_server is None:
            metaflow_config = metaflowconfig.init_config(config_dir, profile)
            perimeter = metaflow_config.get("OBP_PERIMETER")
            api_server = metaflowconfig.get_sanitized_url_from_config(
                config_dir, profile, "OBP_API_SERVER"
            )

        return perimeter, api_server  # type: ignore

    @classmethod
    def during_programmatic_access(cls) -> Union[Tuple[str, str], Tuple[None, None]]:
        from metaflow.metaflow_config_funcs import init_config

        clean_url = (
            lambda url: f"https://{url}".rstrip("/")
            if not url.startswith("https://")
            else url
        )

        config = init_config()
        api_server, perimeter, integrations_url = None, None, None
        perimeter = config.get(
            "OBP_PERIMETER", os.environ.get("OBP_PERIMETER", perimeter)
        )
        if perimeter is None:
            raise OuterboundsConfigurationException("OBP_PERIMETER")

        api_server = config.get(
            "OBP_API_SERVER", os.environ.get("OBP_API_SERVER", api_server)
        )

        if api_server is not None and not api_server.startswith("https://"):
            api_server = clean_url(api_server)

        if api_server is not None:
            return perimeter, api_server

        integrations_url = config.get(
            "OBP_INTEGRATIONS_URL", os.environ.get("OBP_INTEGRATIONS_URL", None)
        )

        if integrations_url is not None and not integrations_url.startswith("https://"):
            integrations_url = clean_url(integrations_url)

        if integrations_url is not None:
            api_server = integrations_url.rstrip("/integrations")

        if api_server is None:
            raise OuterboundsConfigurationException("OBP_API_SERVER")

        return perimeter, api_server

    @classmethod
    def config_during_programmatic_access(cls) -> dict:
        #!HACK: Resolving remote configs is a PITA (all the variable piping we need to do via metaflow)
        # So instead we will just derive the URL. We are in this situation because its a pain
        # to load configurations at arbitrary points in the runtime.
        if cls.config is not None:
            return json.loads(json.dumps(cls.config))  # Return fresh copy
        from metaflow.metaflow_config import SERVICE_HEADERS

        perimeter, api_server = cls.during_programmatic_access()
        response = safe_requests_wrapper(
            requests.get,
            f"{api_server}/v1/perimeters/{perimeter}/metaflowconfigs/default",
            headers=SERVICE_HEADERS,
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"Server error: {response.text}. Please reach out to your Outerbounds support team."
            )
        try:
            remote_config = response.json()

            if not remote_config.get("config"):
                raise json.JSONDecodeError
        except json.JSONDecodeError:
            raise RuntimeError(
                "Exception retrieving remote outerbounds configuration. "
                "Please reach out to Outerbounds suport team with this stack trace."
            )

        cls.config = remote_config.get("config")
        return json.loads(json.dumps(cls.config))  # Return fresh copy

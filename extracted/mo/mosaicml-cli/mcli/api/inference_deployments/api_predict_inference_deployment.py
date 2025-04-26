""" Predict on an Inference Deployment """
from __future__ import annotations

import json
from http import HTTPStatus
from typing import Any, Callable, Dict, Generator, Optional, Union, cast

import requests
import validators
from requests import Response

from mcli import config
from mcli.api.exceptions import InferenceServerException
from mcli.api.inference_deployments import get_inference_deployment
from mcli.api.model.inference_deployment import InferenceDeployment

__all__ = ['predict']


def predict(
    deployment: Union[InferenceDeployment, str],
    inputs: Dict[str, Any],
    *,
    timeout: Optional[int] = 60,
    stream: bool = False,
) -> Union[Dict[str, Any], Generator[str, None, None]]:
    """Sends input to \'/predict\' endpoint of an inference deployment on the MosaicML
    platform. Runs prediction on input and returns output produced by the model.

    Arguments:
        deployment: The deployment to make a prediction with. Can be a InferenceDeployment object,
            the name of an deployment, or a string which is of the form https://<deployment dns>.
        input: Input data to run prediction on in the form of dictionary
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised.
        stream: If True, the response will be streamed and a generator will be returned.
            Streaming supports only a single input at a time.
    Raises:
        HTTPError: If sending the request to the endpoint fails
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    validate_url = cast(Callable[[str], bool], validators.url)
    if isinstance(deployment, str) and not validate_url(deployment):
        # if a string is passed in that is not a url then lookup the deployment and get the name
        deployment = get_inference_deployment(deployment)
    conf = config.MCLIConfig.load_config()
    api_key = conf.api_key
    headers = {
        'authorization': api_key,
    }
    base_url = deployment
    if isinstance(deployment, InferenceDeployment):
        base_url = f'https://{deployment.public_dns}'
    try:
        if stream:
            # we use an internal function to satisfy pyright
            def gen():
                with requests.post(url=f'{base_url}/predict_stream',
                                   timeout=timeout,
                                   json=inputs,
                                   headers=headers,
                                   stream=True) as resp:
                    for line in resp.iter_lines():
                        if line:
                            loaded = json.loads(line)
                            if loaded:
                                yield loaded

            return gen()
        else:
            resp: Response = requests.post(url=f'{base_url}/predict', timeout=timeout, json=inputs, headers=headers)
            if resp.ok:
                try:
                    return resp.json()
                except requests.JSONDecodeError as e:
                    raise InferenceServerException.from_bad_response(resp) from e
            else:
                raise InferenceServerException.from_server_error_response(resp.content.decode().strip(),
                                                                          resp.status_code)
    except requests.exceptions.ReadTimeout as e:
        raise InferenceServerException.from_server_error_response(str(e), HTTPStatus.REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError as e:
        raise InferenceServerException.from_requests_error(e) from e

import json
import logging
from enum import Enum
from json import JSONDecodeError

from qwak_inference.constants import QwakConstants
from qwak_inference.realtime_client.rest_helpers import RestSession, SocketConfiguration

try:
    from qwak.exceptions import QwakHTTPException
except ImportError:
    from qwak_inference.exceptions import QwakHTTPException

_TRAFFIC_SPLIT_HEADER = "x-realtime-route-mode"


class InferenceOutputFormat(Enum):
    PANDAS = 1
    DICTIONARY = 2
    RAW = 3


DEFAULT_ENVIRONMENT_ERROR_MESSAGE = (
    "Failed to get default environment name. This might be due to connectivity "
    "issues or missing account configuration."
)


class RealTimeClient(object):
    def __init__(
        self,
        model_id: str,
        environment: str = None,
        variation: str = None,
        model_api: str = None,
        log_level: int = logging.INFO,
        socket_configuration: SocketConfiguration = SocketConfiguration(),
    ):
        """

        :param model_id: The model id to invoke against. If not provided, will attempt to extract the model ID from the
        `QWAK_MODEL_ID` environment variable
        :log_level: Logging level, Use logging level from std logging library.
        """
        logging.basicConfig(level=log_level)

        self.r_session = RestSession(socket_configuration=socket_configuration)

        self.model_id = model_id
        self.content_type = "application/json; format=pandas-split"

        if model_api:
            logging.debug(f"Using provided model API: {model_api}")
            self.model_api = model_api
        else:
            if environment:
                model_api_url = _get_model_api_url_for_environment_name(
                    self.r_session, environment
                )
                self.model_api = _get_model_url(model_api_url, model_id, variation)
                logging.debug(
                    f"Using model API: {self.model_api} from provided environment: {environment}"
                )
            else:
                model_api_url = _get_model_api_url_from_default_environment(
                    self.r_session
                )
                self.model_api = _get_model_url(model_api_url, model_id, variation)
                logging.debug(
                    f"Using model API: {self.model_api} from default environment"
                )

    def predict(
        self,
        feature_vectors,
        output_format=InferenceOutputFormat.DICTIONARY,
        metadata: dict = {},
        orient: str = "split",
    ):
        """
        Perform a prediction request against a Qwak based model

        :param feature_vectors: A list of feature vectors to predict against. Each feature vector is modeled as a python
         dictionary, or a pandas Dataframe
        :param output_format: A list of feature vectors to predict against. Each feature vector is modeled as a python
         dictionary, or a pandas Dataframe
        :param metadata: metadata to split traffic based on
        :return: Prediction response from the model
        :param orient: The format of the JSON string. Default is 'split'. See pandas.DataFrame.to_json for more details
        """

        if feature_vectors.__class__.__name__ == "DataFrame":
            feature_vectors = feature_vectors.to_json(orient=orient)

        if isinstance(feature_vectors, dict) or isinstance(feature_vectors, list):
            feature_vectors = json.dumps(feature_vectors)

        try:
            rule_based_traffic = {}
            if metadata:
                rule_based_traffic = metadata.copy()
                rule_based_traffic[_TRAFFIC_SPLIT_HEADER] = "true"

            response = self.r_session.post(
                self.model_api, data=feature_vectors, headers=rule_based_traffic
            )

            if response.status_code >= 400:
                exception_class_name = response.headers.get("X-Exception-Class")
                msg = f"{response.status_code}: {response.text}"

                logging.debug(f"Failed to predict. Response: {response}")

                raise QwakHTTPException(response.status_code, msg, exception_class_name)

            elif response.status_code != 200:
                raise QwakHTTPException(response.status_code, response.content)

            if output_format == InferenceOutputFormat.RAW:
                return response.content

            if output_format == InferenceOutputFormat.DICTIONARY:
                dict_response = json.loads(response.content)
                return dict_response
            elif output_format == InferenceOutputFormat.PANDAS:
                try:
                    import pandas as pd
                except ImportError:
                    raise ImportError(
                        "Pandas is not installed. Please install pandas to use the pandas output format"
                    )
                dict_response = json.loads(response.content)
                return pd.DataFrame(dict_response)
            else:
                raise ValueError(
                    f"Non supported inference output parameter {output_format}"
                )
        except QwakHTTPException as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Failed to make a prediction request. Error is: {e}")


def _get_model_api_url_from_default_environment(r_session) -> str:
    try:
        response = r_session.post(QwakConstants.QWAK_AUTHENTICATED_USER_ENDPOINT)
        account_details = response.json()["authenticatedUserContext"]["user"][
            "accountDetails"
        ]
        default_environment_id = account_details["defaultEnvironmentId"]
        model_api_url = account_details["environmentById"][default_environment_id][
            "configuration"
        ]["modelApiUrl"]
        return model_api_url
    except JSONDecodeError:
        raise RuntimeError(DEFAULT_ENVIRONMENT_ERROR_MESSAGE)
    except Exception as e:
        raise RuntimeError(f"{DEFAULT_ENVIRONMENT_ERROR_MESSAGE} Error is: {e}")


def _get_model_api_url_for_environment_name(r_session, environment_name):
    try:
        response = r_session.post(QwakConstants.QWAK_AUTHENTICATED_USER_ENDPOINT)
        account_details = response.json()["authenticatedUserContext"]["user"][
            "accountDetails"
        ]

        for environment_id, environment_config in account_details[
            "environmentById"
        ].items():
            if environment_config["name"] == environment_name:
                model_api_url = environment_config["configuration"]["modelApiUrl"]
                return model_api_url

        logging.warning(
            f"Failed to find environment configuration with name: {environment_name}. Using a fallback url instead."
        )
        return f"models.{environment_name}.qwak.ai"

    except JSONDecodeError:
        raise RuntimeError(DEFAULT_ENVIRONMENT_ERROR_MESSAGE)
    except Exception:
        raise RuntimeError(DEFAULT_ENVIRONMENT_ERROR_MESSAGE + " Error is: {e}")


def _get_model_url(model_api_url, model_id, variation=None) -> str:
    model_route = f"{model_id}/{variation}" if variation else model_id
    return f"https://{model_api_url}/v1/{model_route}/predict"

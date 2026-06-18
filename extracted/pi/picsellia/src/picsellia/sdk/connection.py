import abc
import logging
import os
from collections.abc import Iterable, Mapping
from io import IOBase
from pathlib import Path
from typing import IO, Any
from urllib.parse import urljoin
from uuid import UUID

import orjson
import requests
from beartype import beartype
from requests import Response, Session
from requests.exceptions import ConnectionError, InvalidJSONError

import picsellia.exceptions as exceptions
from picsellia import __version__
from picsellia.decorators import exception_handler, retry
from picsellia.services.upload.file import FileUploader
from picsellia.types.enums import ObjectDataType

logger = logging.getLogger("picsellia")

DEFAULT_DOWNLOAD_TIMEOUT = 30
DEFAULT_TIMEOUT = 300

DATA_TYPE = str | bytes | Mapping[str, Any] | Iterable[tuple[str, str, None]] | IO


def reset_body(body):
    if "files" in body and isinstance(body["files"], dict):
        logger.debug("Seeking buffered readers to zero")
        for value in body["files"].values():
            if isinstance(value, IOBase):
                try:
                    value.seek(0)
                except Exception:
                    pass


def wrapped_request(f):
    def decorated(self, *args, regenerate_jwt=True, **kwargs):
        resp = f(self, *args, **kwargs)

        if resp.status_code == 401:
            if regenerate_jwt:
                logger.info(f"Regenerating connection token to {self.host}...")
                self._jwt, self._expires_in = self.generate_jwt()
                reset_body(kwargs)
                return decorated(self, *args, regenerate_jwt=False, **kwargs)
            else:
                raise exceptions.UnauthorizedError(
                    "You are not authorized to do this: regeneration of connection token failed."
                )

        return resp

    return decorated


def handle_response(f):
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        check_status_code(response)
        return response

    return decorated


# No exception handling: exception needs to be raised
def check_status_code(response: Response):  # noqa: C901
    status = int(response.status_code)
    if status == 200:
        logger.debug("OK.")
    elif status == 201:
        logger.debug("Resource created.")
    elif status == 202:
        logger.debug("Accepted.")
    elif status == 203:
        logger.debug("OK.")
    elif status == 204:
        logger.debug("No content.")
    elif status != 208 and status <= 299:
        logger.debug(f"Request done : {status}")
    else:
        try:
            data = response.json()
            if "message" not in data:
                data["message"] = f"No message ({status})"

            message = data["message"]
            if "detail" in data and data["detail"] is not None and data["detail"] != []:
                if isinstance(data["detail"], list):
                    message += ". Detail: \n"
                    for item in data["detail"]:
                        message += " > " + str(item) + "\n"
                else:
                    message = message + ". Detail: " + str(data["detail"])
        except (KeyError, InvalidJSONError):
            message = response.text

        logger.debug(
            f"Platform returned an error (status code: {status}). Message : {message}"
        )

        if status == 208:
            raise exceptions.DistantStorageError(
                "An object has already this name in S3."
            )
        if status == 400:
            raise exceptions.BadRequestError(message)
        if status == 401:
            raise exceptions.UnauthorizedError(message)
        if status == 402:
            raise exceptions.InsufficientResourcesError(message)
        if status == 403:
            raise exceptions.ForbiddenError(message)
        if status == 404:
            raise exceptions.ResourceNotFoundError(message)
        if status == 405:
            raise exceptions.PicselliaError(f"Method not allowed: {message}")
        if status == 409:
            raise exceptions.ResourceConflictError(message)
        if status == 413:
            raise exceptions.RequestTooLargeError(
                "There is too much data in your request."
            )
        if status == 422:
            raise exceptions.BadRequestError(message)
        if status == 423:
            raise exceptions.ResourceLockedError(message)
        if status == 429:
            raise exceptions.TooManyRequestError(message)
        if status == 500:
            raise exceptions.InternalServerError(message)
        if status == 502:
            raise exceptions.BadGatewayError("Picsellia is unavailable at the moment.")
        raise exceptions.PicselliaError(f"[{status}] Something went wrong, {message}")


class AbstractConnection(abc.ABC):
    def __init__(self, host: str, session: Session | None = None) -> None:
        self.host = host
        if session is not None:
            self.session = session
        else:
            self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None:
            self.session.close()

    @property
    @abc.abstractmethod
    def headers(self):
        pass

    def get(self, path: str, params: dict | None = None, stream: bool = False):
        url = urljoin(self.host, path)
        return self.session.get(
            url=url,
            headers=self.headers,
            params=params,
            stream=stream,
            timeout=DEFAULT_TIMEOUT,
        )

    def xget(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
        stream: bool = False,
    ):
        url = urljoin(self.host, path)
        return self.session.request(
            method="XGET",
            url=url,
            data=data,
            headers=self.headers,
            params=params,
            stream=stream,
            timeout=DEFAULT_TIMEOUT,
        )

    def post(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
        files: Any | None = None,
    ):
        url = urljoin(self.host, path)
        return self.session.post(
            url=url,
            data=data,
            headers=self.headers,
            params=params,
            files=files,
            timeout=DEFAULT_TIMEOUT,
        )

    def put(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        url = urljoin(self.host, path)
        return self.session.put(
            url=url,
            data=data,
            headers=self.headers,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )

    def patch(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        url = urljoin(self.host, path)
        return self.session.patch(
            url=url,
            data=data,
            headers=self.headers,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )

    def delete(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        url = urljoin(self.host, path)
        return self.session.delete(
            url=url,
            data=data,
            headers=self.headers,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )


class Connection(AbstractConnection):
    def __init__(
        self,
        host: str,
        api_token: str,
        content_type: str = "application/json",
        session: Session | None = None,
    ) -> None:
        super().__init__(host, session)
        self.api_token = api_token
        self._headers = {
            "Authorization": "Bearer " + api_token,
            "User-Agent": f"Picsellia-SDK/{__version__}",
        }
        if content_type:
            self._headers["Content-type"] = content_type

        self._connector_id = None
        self._organization_id = None

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Connection):
            return self.host == __o.host and self.api_token == __o.api_token

        return False

    @property
    def headers(self):
        return self._headers

    @property
    def connector_id(self):
        if self._connector_id is None:
            raise exceptions.NoConnectorFound(
                "This organization has no default connector, and connect retrieve and upload files."
            )
        return self._connector_id

    @connector_id.setter
    def connector_id(self, value):
        self._connector_id = value

    @property
    def organization_id(self):
        return self._organization_id

    @organization_id.setter
    def organization_id(self, value):
        self._organization_id = value
        self.headers["X-Picsellia-Organization"] = str(self._organization_id)

    @handle_response
    @retry((requests.ConnectionError, requests.exceptions.ChunkedEncodingError))
    def get(self, path: str, params: dict | None = None, stream: bool = False):
        return super().get(path, params, stream)

    @handle_response
    @retry((requests.ConnectionError, requests.exceptions.ChunkedEncodingError))
    def xget(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
        stream: bool = False,
    ):
        return super().xget(path, data, params, stream)

    @handle_response
    @retry(requests.ConnectionError)
    def post(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
        files: Any | None = None,
    ):
        return super().post(path, data, params, files)

    @handle_response
    @retry(requests.ConnectionError)
    def put(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        return super().put(path, data, params)

    @handle_response
    @retry(requests.ConnectionError)
    def patch(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        return super().patch(path, data, params)

    @handle_response
    @retry(requests.ConnectionError)
    def delete(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        return super().delete(path, data, params)

    ##############################################################
    # ------------------------- UPLOAD ------------------------- #
    ##############################################################
    @exception_handler
    @beartype
    def _generate_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        connector_id: UUID | None = None,
        context: dict[str, UUID] | None = None,
        upload_dir: str | None = None,
    ) -> str:
        if connector_id is None:
            connector_id = self.connector_id

        payload: dict[str, Any] = {"filename": filename, "type": object_name_type}
        if context:
            payload["context"] = context

        if upload_dir:
            payload["upload_dir"] = upload_dir

        r = self.post(
            path=f"/api/organization/{self.organization_id}/connector/{connector_id}/generate_object_name",
            data=orjson.dumps(payload),
        ).json()
        return r["object_name"]

    @beartype
    def generate_data_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        connector_id: UUID | None = None,
        upload_dir: str | None = None,
    ):
        if object_name_type not in [
            ObjectDataType.DATA,
            ObjectDataType.DATA_PROJECTION,
        ]:
            raise RuntimeError(
                f"Cannot generate data object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename, object_name_type, connector_id, upload_dir=upload_dir
        )

    @beartype
    def generate_dataset_version_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        dataset_version_id: UUID,
        connector_id: UUID | None = None,
    ):
        if object_name_type not in [ObjectDataType.CAMPAIGN_FILE]:
            raise RuntimeError(
                f"Cannot generate dataset version object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename,
            object_name_type,
            connector_id,
            context={"dataset_version_id": dataset_version_id},
        )

    @beartype
    def generate_deployment_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        deployment_id: UUID,
        connector_id: UUID | None = None,
    ):
        if object_name_type not in [ObjectDataType.REVIEW_CAMPAIGN_FILE]:
            raise RuntimeError(
                f"Cannot generate deployment object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename,
            object_name_type,
            connector_id,
            context={"deployment_id": deployment_id},
        )

    @beartype
    def generate_job_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        job_id: UUID,
        connector_id: UUID | None = None,
    ):
        if object_name_type not in [ObjectDataType.LOGGING]:
            raise RuntimeError(
                f"Cannot generate job object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename,
            object_name_type,
            connector_id=connector_id,
            context={"job_id": job_id},
        )

    @beartype
    def generate_experiment_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        experiment_id: UUID,
        connector_id: UUID | None = None,
    ):
        if object_name_type not in (
            ObjectDataType.ARTIFACT,
            ObjectDataType.LOG_IMAGE,
            ObjectDataType.LOGGING,
        ):
            raise RuntimeError(
                f"Cannot generate experiment object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename,
            object_name_type,
            connector_id=connector_id,
            context={"experiment_id": experiment_id},
        )

    @beartype
    def generate_model_version_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        model_version_id: UUID,
        connector_id: UUID | None = None,
    ):
        if object_name_type not in (
            ObjectDataType.MODEL_THUMB,
            ObjectDataType.MODEL_FILE,
        ):
            raise RuntimeError(
                f"Cannot generate model version object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename,
            object_name_type,
            connector_id=connector_id,
            context={"model_version_id": model_version_id},
        )

    @beartype
    def generate_report_object_name(
        self,
        filename: str,
        object_name_type: ObjectDataType,
        dataset_version_id: UUID,
        report_id: UUID,
        connector_id: UUID | None = None,
    ):
        if object_name_type != ObjectDataType.AGENTS_REPORT:
            raise RuntimeError(
                f"Cannot generate report object name with type {object_name_type}"
            )
        return self._generate_object_name(
            filename,
            object_name_type,
            connector_id=connector_id,
            context={"report_id": report_id, "dataset_version_id": dataset_version_id},
        )

    def upload_file(
        self,
        object_name: str,
        path: str | Path,
        connector_id: UUID | None = None,
    ) -> tuple[requests.Response, bool, str]:
        """Upload a single file to the server.
        If file is bigger than 5Mb, it will send it by multipart.

        Arguments:
            path (str): Absolute path to the file
            object_name (str): Destination object name.
            connector_id (UUID): Connector on which you need to upload file, if it's not default connector.
        """
        if connector_id is None:
            connector_id = self.connector_id

        uploader = FileUploader(connector_id, self.session, self.host, self.headers)
        return uploader.upload(object_name, path)

    ##############################################################
    # ------------------------ DOWNLOAD ------------------------ #
    ##############################################################
    def init_download(self, object_name: str, connector_id: UUID | None = None) -> str:
        """Retrieve a presigned url of this object name in order to download it"""
        if connector_id is None:
            connector_id = self.connector_id

        payload = {"object_name": object_name}
        r = self.post(
            path=f"/api/object-storage/{connector_id}/retrieve_presigned_url",
            data=orjson.dumps(payload),
        )

        if r.status_code != 200:
            raise exceptions.DistantStorageError("Errors while getting a presigned url")

        r = r.json()
        if "presigned_url" not in r:
            raise exceptions.DistantStorageError(
                "Errors while getting a presigned url. Unparsable response"
            )

        return r["presigned_url"]

    def do_download_file(
        self,
        path: str | Path,
        url: str,
        is_large: bool,
        force_replace: bool,
        retry_count: int = 1,
    ) -> bool:
        try:
            return self._do_download_file(path, url, is_large, force_replace)
        except (exceptions.NetworkError, ConnectionError) as e:
            # Here for retro compatibility
            raise exceptions.DownloadError(
                f"Could not download {url} into {path}"
            ) from e

    @retry((exceptions.NetworkError, ConnectionError))
    def _do_download_file(
        self,
        path: str | Path,
        url: str,
        is_large: bool,
        force_replace: bool,
    ) -> bool:
        """Retrieve a presigned url of this object name in order to download it"""
        if os.path.exists(path) and not force_replace:
            return False

        parent_path = Path(path).parent.absolute()
        os.makedirs(parent_path, exist_ok=True)

        response = self.session.get(
            url, stream=is_large, timeout=DEFAULT_DOWNLOAD_TIMEOUT
        )

        if response.status_code == 429 or (500 <= response.status_code < 600):
            raise exceptions.NetworkError(
                f"Response status code is {response.status_code}. Could not get {url}"
            )

        response.raise_for_status()

        total_length = response.headers.get("content-length")
        if total_length is None:
            raise exceptions.NetworkError(
                "Downloaded content is empty but response is 200"
            )

        with open(path, "wb") as handler:
            if not is_large:
                handler.write(response.content)
            else:
                for data in response.iter_content(chunk_size=4096):
                    handler.write(data)

        return True


class JwtServiceConnection(AbstractConnection):
    def __init__(
        self,
        host: str,
        jwt_identifier_data: dict,
        login_path: str,
        session: Session | None = None,
    ) -> None:
        """JwtServiceConnection may be used to handle a JwtAuthentication connection with a service.
        You need to give a dict `jwt_identifier_data` that will be sent to the host to ensures validity of your request.
        This data will depend on service contacted. For example for a Deployment / Jwt request on Oracle, this will be :
        {
            "api_token" : <user_api_token>,
            "deployment_id" : <deployment_id>
        }
        """
        super().__init__(host, session)
        self.jwt_identifier_data = jwt_identifier_data
        self.login_path = login_path
        self._jwt, self._expires_in = None, None

    @property
    def jwt(self) -> str:
        if self._jwt is None:
            self._jwt, self._expires_in = self.generate_jwt()
        return self._jwt

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.jwt}"}

    def generate_jwt(self):
        response = self._call_auth_login()

        if response.status_code != 200:
            raise exceptions.UnauthorizedError("Unauthorized attempt to connect.")

        try:
            data = response.json()
            return data["jwt"], data["expires"]
        except Exception:
            raise exceptions.UnauthorizedError(
                "Cannot parse response from external service. Please contact support."
            )

    @retry((requests.ReadTimeout, requests.ConnectionError))
    def _call_auth_login(self) -> Response:
        url = urljoin(self.host, self.login_path)
        return self.session.post(url=url, data=orjson.dumps(self.jwt_identifier_data))

    @wrapped_request
    @retry((requests.ConnectionError, requests.exceptions.ChunkedEncodingError))
    def get(self, path: str, params: dict | None = None, stream: bool = False):
        return super().get(path, params, stream)

    @wrapped_request
    @retry((requests.ConnectionError, requests.exceptions.ChunkedEncodingError))
    def xget(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
        stream: bool = False,
    ):
        return super().xget(path, data, params, stream)

    @wrapped_request
    @retry(requests.ConnectionError)
    def post(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
        files: Any | None = None,
    ):
        return super().post(path, data, params, files)

    @wrapped_request
    @retry(requests.ConnectionError)
    def put(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        return super().put(path, data, params)

    @wrapped_request
    @retry(requests.ConnectionError)
    def patch(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        return super().patch(path, data, params)

    @wrapped_request
    @retry(requests.ConnectionError)
    def delete(
        self,
        path: str,
        data: DATA_TYPE | None = None,
        params: dict | None = None,
    ):
        return super().delete(path, data, params)


Connexion = Connection
JwtServiceConnexion = JwtServiceConnection

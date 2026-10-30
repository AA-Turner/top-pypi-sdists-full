"""
A loopback stand-in for the AWS Notebook app's kernel callback server, for local-kernel tests.

Mirrors ``src/engine/kernels/callback-server.ts`` and ``connections/operations.ts`` of the app:
operations are ``POST /api/<family>/<op>`` with a JSON body and ``Authorization: Bearer <token>``;
``connections.get`` answers the row, with ``connectionCredentials`` when ``withSecret`` is set
and the app is signed in, ``403 AccessDeniedException`` when it is signed out; ``connections.list``
answers a bare array of the rows in scope (filtered by ``type`` and ``store`` when given), without
credentials, and an empty array when signed out; every failure is ``{"error": {"code", "message"}}``.
"""

from __future__ import annotations

import json
import threading
import unittest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional, Tuple

from sagemaker_studio import local_kernel
from sagemaker_studio.local_kernel import configure_local_kernel, reset_local_kernel

SIGNED_OUT_MESSAGE = "Sign in to AWS to use this connection's data."


def credentials(key: str = "AKIA_TEST", minutes: Optional[float] = 60) -> Dict[str, Any]:
    """``connectionCredentials`` as the app answers them (ISO ``Z`` expiration)."""
    payload = {
        "accessKeyId": key,
        "secretAccessKey": f"{key}-secret",
        "sessionToken": f"{key}-token",
    }
    if minutes is not None:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        payload["expiration"] = expiration.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return payload


def _location(
    account: Optional[str], region: Optional[str], access_role: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not account and not region and not access_role:
        return []
    aws_location: Dict[str, str] = {}
    if account:
        aws_location["awsAccountId"] = account
    if region:
        aws_location["awsRegion"] = region
    if access_role:
        aws_location["accessRole"] = access_role
    return [{"awsLocation": aws_location}]


def s3_record(
    connection_id: str = "s3raw",
    name: str = "raw",
    uri: str = "s3://b/raw/",
    account: Optional[str] = "111122223333",
    region: Optional[str] = "us-west-2",
    store: str = "machine",
) -> Dict[str, Any]:
    """An S3 row as the app stores and answers it (no DataZone scope fields)."""
    return {
        "connectionId": connection_id,
        "name": name,
        "type": "S3",
        "createdAt": "2026-10-05T16:40:33.379Z",
        "updatedAt": "2026-10-05T16:40:33.379Z",
        "physicalEndpoints": _location(account, region),
        "props": {"s3Properties": {"s3Uri": uri}},
        "store": store,
    }


def athena_record(
    connection_id: str = "wh",
    name: str = "warehouse",
    workgroup: str = "primary",
    catalog: str = "AwsDataCatalog",
    account: str = "111122223333",
    region: str = "us-west-2",
    access_role: Optional[str] = None,
) -> Dict[str, Any]:
    """An ATHENA row (what the app vends today); with ``access_role``, one the app signs as that role."""
    return {
        "connectionId": connection_id,
        "name": name,
        "type": "ATHENA",
        "createdAt": "2026-10-05T16:40:33.387Z",
        "updatedAt": "2026-10-05T16:40:33.387Z",
        "physicalEndpoints": _location(account, region, access_role),
        "props": {"athenaProperties": {"workgroupName": workgroup}},
        "catalog": catalog,
    }


def lakehouse_record(
    connection_id: str = "lakehouse1",
    name: str = "catalog",
    workgroup: Optional[str] = "primary",
    account: str = "111122223333",
    region: str = "us-east-2",
    with_scope: bool = True,
    updated_at: str = "2026-10-12T18:09:38.848541480Z",
    access_role: Optional[str] = None,
) -> Dict[str, Any]:
    """
    A LAKEHOUSE catalog connection as the app will vend it: the Athena workgroup to query the
    catalog with is an ``athena`` entry of ``configurations``; with ``access_role``, one whose data
    is reached as that role. Every id is made up.
    """
    record: Dict[str, Any] = {
        "configurations": (
            [{"classification": "athena", "properties": {"workgroupName": workgroup}}]
            if workgroup
            else []
        ),
        "connectionId": connection_id,
        "createdAt": "2026-10-12T18:09:38.848541480Z",
        "name": name,
        "physicalEndpoints": _location(account, region, access_role),
        "props": {
            "lakehouseProperties": {"captureDataLineage": True, "glueLineageSyncEnabled": True}
        },
        "type": "LAKEHOUSE",
        "updatedAt": updated_at,
    }
    if with_scope:
        record.update(
            {
                "domainId": "dzd-exampledomain",
                "domainUnitId": "exampledomainunit",
                "environmentId": "exampleenvironment",
                "environmentUserRole": f"arn:aws:iam::{account}:role/datazone_usr_role_example",
                "projectId": "exampleproject",
                "scope": "PROJECT",
            }
        )
    return record


class FakeApp:
    """
    The app's callback server on a random loopback port.

    Attributes:
        url, token: What the app would put in ``AWS_NOTEBOOK_APP_URL`` / ``AWS_NOTEBOOK_APP_TOKEN``.
        records: Rows by connection id.
        credentials: The signed-in session's ``connectionCredentials``; ``None`` when signed out.
        per_connection_credentials: Credentials for one connection id (an ``accessRole``).
        raw_responses: ``connection id -> (status, body bytes, content type)`` to answer verbatim.
        raw_list_response: ``(status, body bytes, content type)`` for ``connections.list`` to answer verbatim.
        redirects: ``connection id -> (3xx status, Location)`` to answer with a redirect.
        calls: Every admitted request as ``(operation, body, authorization header)``.
        requests: Every request received, admitted or not, as ``(method, path, authorization)``.
    """

    def __init__(self, token: str = "s3cr3t-t0ken", signed_in: bool = True):
        self.token = token
        self.records: Dict[str, Dict[str, Any]] = {}
        self.credentials: Optional[Dict[str, Any]] = credentials() if signed_in else None
        self.per_connection_credentials: Dict[str, Dict[str, Any]] = {}
        self.raw_responses: Dict[str, Tuple[int, bytes, str]] = {}
        self.raw_list_response: Optional[Tuple[int, bytes, str]] = None
        self.redirects: Dict[str, Tuple[int, str]] = {}
        self.calls: List[Tuple[str, Dict[str, Any], Optional[str]]] = []
        self.requests: List[Tuple[str, str, Optional[str]]] = []
        self.refused: List[Tuple[int, str]] = []
        app = self

        class Handler(BaseHTTPRequestHandler):
            def _send(
                self,
                status: int,
                body: Any,
                content_type: str = "application/json",
                headers: Optional[Dict[str, str]] = None,
            ):
                data = body if isinstance(body, bytes) else json.dumps(body).encode()
                # Drain whatever of the request body is still unread, so an early refusal (401,
                # 415) does not reset the connection under the client while it reads our answer.
                remaining = int(self.headers.get("Content-Length") or 0) - getattr(
                    self, "_consumed", 0
                )
                if remaining > 0:
                    self.rfile.read(remaining)
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                for name, value in (headers or {}).items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(data)

            def _error(self, status: int, code: str, message: str):
                app.refused.append((status, code))
                self._send(status, {"error": {"code": code, "message": message}})

            def do_POST(self):  # noqa: N802
                authorization = self.headers.get("Authorization")
                app.requests.append((self.command, self.path, authorization))
                if "Origin" in self.headers:
                    return self._error(
                        403, "AccessDeniedException", "Browser requests are not accepted"
                    )
                if authorization != f"Bearer {app.token}":
                    return self._error(
                        401, "UnrecognizedClientException", "Missing or invalid bearer token"
                    )
                content_type = self.headers.get("Content-Type", "")
                if not content_type.lower().startswith("application/json"):
                    return self._error(
                        415, "UnsupportedMediaType", "Request body must be application/json"
                    )
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                self._consumed = length
                try:
                    body = json.loads(raw.decode("utf-8")) if raw else None
                except ValueError:
                    return self._error(400, "ValidationException", "Request body is not valid JSON")
                if not isinstance(body, dict):
                    return self._error(
                        400, "ValidationException", "Request body is empty; send the input as JSON"
                    )
                if not self.path.startswith("/api/"):
                    return self._error(501, "NotImplemented", f"No operation at {self.path}")
                operation = self.path[len("/api/") :]
                app.calls.append((operation, body, authorization))
                if operation == "connections/list":
                    return self._list(body)
                if operation != "connections/get":
                    return self._error(501, "NotImplemented", f'No such operation "{operation}"')
                return self._get(body)

            def _list(self, body: Dict[str, Any]):
                if app.raw_list_response is not None:
                    status, data, content_type = app.raw_list_response
                    return self._send(status, data, content_type)
                # Signed out, nothing is in scope: the app answers an empty array, not an error.
                if app.credentials is None:
                    return self._send(200, [])
                rows = [
                    dict(record)
                    for record in app.records.values()
                    if (body.get("type") is None or record.get("type") == body.get("type"))
                    and (body.get("store") is None or record.get("store") == body.get("store"))
                ]
                return self._send(200, rows)

            def _get(self, body: Dict[str, Any]):
                connection_id = body.get("identifier") or body.get("connectionIdentifier")
                if not connection_id:
                    return self._error(
                        400, "ValidationException", "identifier or connectionIdentifier is required"
                    )
                if connection_id in app.raw_responses:
                    status, data, content_type = app.raw_responses[connection_id]
                    return self._send(status, data, content_type)
                if connection_id in app.redirects:
                    status, location = app.redirects[connection_id]
                    return self._send(status, b"", "text/plain", headers={"Location": location})
                record = app.records.get(connection_id)
                if record is None:
                    return self._error(
                        404, "ResourceNotFoundException", f"No connection with id {connection_id}"
                    )
                row = dict(record)
                if body.get("withSecret"):
                    creds = app.per_connection_credentials.get(connection_id, app.credentials)
                    if creds is None:
                        return self._error(403, "AccessDeniedException", SIGNED_OUT_MESSAGE)
                    row["connectionCredentials"] = dict(creds)
                return self._send(200, row)

            def do_GET(self):  # noqa: N802
                app.requests.append((self.command, self.path, self.headers.get("Authorization")))
                self._error(405, "MethodNotAllowed", "Operations are called with POST")

            def log_message(self, *args):  # silence the test output
                pass

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.url = f"http://127.0.0.1:{self._server.server_port}"

    # -- scenario helpers ------------------------------------------------------------------

    def add(self, record: Dict[str, Any]) -> str:
        self.records[record["connectionId"]] = record
        return record["connectionId"]

    def sign_out(self) -> None:
        self.credentials = None

    def sign_in(self, key: str = "AKIA_TEST", minutes: Optional[float] = 60) -> Dict[str, Any]:
        self.credentials = credentials(key, minutes)
        return self.credentials

    def get_calls(self, connection_id: Optional[str] = None, with_secret: Optional[bool] = None):
        """The ``connections.get`` requests, optionally for one id / secret flag."""
        found = []
        for operation, body, _auth in self.calls:
            if operation != "connections/get":
                continue
            wanted = body.get("identifier") or body.get("connectionIdentifier")
            if connection_id is not None and wanted != connection_id:
                continue
            if with_secret is not None and bool(body.get("withSecret")) != with_secret:
                continue
            found.append(body)
        return found

    def list_calls(self):
        """The ``connections.list`` request bodies."""
        return [body for operation, body, _auth in self.calls if operation == "connections/list"]

    def env(self) -> Dict[str, str]:
        return {local_kernel.APP_URL_ENV_VAR: self.url, local_kernel.APP_TOKEN_ENV_VAR: self.token}

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()


class LocalKernelTestCase(unittest.TestCase):
    """A test case running as a local kernel against a :class:`FakeApp`."""

    signed_in = True

    def setUp(self):
        self.app = FakeApp(signed_in=self.signed_in)
        configure_local_kernel(self.app.url, self.app.token)
        self.kernel = local_kernel.local_kernel()

    def tearDown(self):
        reset_local_kernel()
        self.app.close()

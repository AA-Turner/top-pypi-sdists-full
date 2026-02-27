import json
from typing import Any
from typing import AnyStr
from typing import IO

from .build_constants import BUILD_GCLOUD_REST
from .session import SyncSession
from .token import Token
from .token import Type
from .utils import encode

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[assignment]

API_ROOT_IAM = 'https://iam.googleapis.com/v1'
API_ROOT_IAM_CREDENTIALS = 'https://iamcredentials.googleapis.com/v1'
SCOPES = ['https://www.googleapis.com/auth/iam']


class IamClient:
    def __init__(
        self, service_file: str | IO[AnyStr] | None = None,
        session: Session | None = None,
        token: Token | None = None,
    ) -> None:
        self.session = SyncSession(session)
        self.token = token or Token(
            service_file=service_file, scopes=SCOPES,
            session=self.session.session,  # type: ignore[arg-type]
        )

        if self.token.token_type not in {
            Type.GCE_METADATA,
            Type.SERVICE_ACCOUNT,
        }:
            raise TypeError(
                'IAM Credentials Client is only valid for use '
                'with Service Accounts or GCE Metadata',
            )

    def headers(self) -> dict[str, str]:
        token = self.token.get()
        return {
            'Authorization': f'Bearer {token}',
        }

    @property
    def service_account_email(self) -> str | None:
        return self.token.service_data.get('client_email')

    # https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.keys/get
    def get_public_key(
        self, key_id: str | None = None,
        key: str | None = None,
        service_account_email: str | None = None,
        project: str | None = None,
        session: Session | None = None,
        timeout: int = 10,
    ) -> dict[str, str]:
        service_account_email = (
            service_account_email
            or self.service_account_email
        )
        project = project or self.token.get_project()

        if not key_id and not key:
            raise ValueError('get_public_key must have either key_id or key')

        if not key:
            key = (
                f'projects/{project}/serviceAccounts/'
                f'{service_account_email}/keys/{key_id}'
            )

        url = f'{API_ROOT_IAM}/{key}?publicKeyType=TYPE_X509_PEM_FILE'
        headers = self.headers()

        s = SyncSession(session) if session else self.session

        resp = s.get(url=url, headers=headers, timeout=timeout)

        data: dict[str, str] = resp.json()
        return data

    # https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.keys/list
    def list_public_keys(
            self, service_account_email: str | None = None,
            project: str | None = None,
            session: Session | None = None,
            timeout: int = 10,
    ) -> list[dict[str, str]]:
        service_account_email = (
            service_account_email
            or self.service_account_email
        )
        project = project or self.token.get_project()

        url = (
            f'{API_ROOT_IAM}/projects/{project}/'
            f'serviceAccounts/{service_account_email}/keys'
        )

        headers = self.headers()

        s = SyncSession(session) if session else self.session

        resp = s.get(url=url, headers=headers, timeout=timeout)

        data: list[dict[str, Any]] = (resp.json()).get('keys', [])
        return data

    # https://cloud.google.com/iam/credentials/reference/rest/v1/projects.serviceAccounts/signBlob
    def sign_blob(
        self, payload: str | bytes | None,
        service_account_email: str | None = None,
        delegates: list[str] | None = None,
        session: Session | None = None,
        timeout: int = 10,
    ) -> dict[str, str]:
        service_account_email = (
            service_account_email
            or self.service_account_email
        )
        if not service_account_email:
            raise TypeError(
                'sign_blob must have a valid '
                'service_account_email',
            )

        resource_name = f'projects/-/serviceAccounts/{service_account_email}'
        url = f'{API_ROOT_IAM_CREDENTIALS}/{resource_name}:signBlob'

        json_str = json.dumps({
            'delegates': delegates or [resource_name],
            'payload': encode(payload or '').decode('utf-8'),
        })

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(json_str)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session

        resp = s.post(
            url=url, data=json_str, headers=headers,
            timeout=timeout,
        )
        data: dict[str, Any] = resp.json()
        return data

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> 'IamClient':
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

from dataclasses import dataclass
from typing import List, Literal, Optional, Union

import requests

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.credentials import resolve_headers

Kind = Literal["passwordless", "task-waiting", "message"]


@dataclass
class EmailAttachment:
    filename: str
    content: str
    type: str

    def to_dict(self):
        return {
            "filename": self.filename,
            "content": self.content,
            "type": self.type,
        }


@dataclass
class EmailParams:
    kind: Kind
    to: List[str]
    subject: str
    body: str
    attachments: List[EmailAttachment]
    is_html: bool
    is_resend: bool

    def to_dict(self):
        return {
            "kind": self.kind,
            "to": self.to,
            "subject": self.subject,
            "body": self.body,
            "attachments": [attachment.to_dict() for attachment in self.attachments],
            "isHtml": self.is_html,
            "isResend": self.is_resend,
        }

    def __init__(
        self,
        kind: Kind,
        to: List[str],
        subject: str,
        body: str,
        attachments: List[Union[EmailAttachment, dict]],
        is_html: bool,
        is_resend: bool = False,
    ):
        self.kind = kind
        self.to = to
        self.subject = subject
        self.body = body
        self.is_html = is_html
        self.is_resend = is_resend

        self.attachments = []
        for attachment in attachments:
            if isinstance(attachment, EmailAttachment):
                self.attachments.append(attachment)
            elif isinstance(attachment, dict):
                self.attachments.append(EmailAttachment(**attachment))
            else:
                raise ValueError("Invalid attachment type")


class EmailRepository:
    def __init__(self, client: "HTTPClient"):
        self.client = client

    def send(self, param: EmailParams, user_jwt: Optional[str] = None):
        headers = resolve_headers() or {}
        if user_jwt:
            headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
        response = self.client.post(
            endpoint="/email",
            json=param.to_dict(),
            headers=headers,
        )
        if not response.ok:
            # raise_for_status() drops the response body. cloud-api returns
            # {"error": "...", "code": "..."} on things like consumption blocks;
            # surface the actual message so users know what to do.
            try:
                payload = response.json()
                detail = payload.get("error") if isinstance(payload, dict) else None
            except ValueError:
                detail = None
            if not detail:
                detail = response.text or response.reason
            raise requests.HTTPError(
                f"{response.status_code} {response.reason}: {detail}",
                response=response,
            )

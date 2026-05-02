# components/notify/SendEmail.py
import os
from typing import Dict, List, Optional, Iterable, Union
import asyncio
from pathlib import Path
from email.header import Header
from navconfig.logging import logging
from notify.providers.email import Email
from notify.models import Actor
from .flow import FlowComponent
from ..exceptions import ComponentError, FileNotFound
from ..interfaces import TemplateSupport
from ..interfaces.credentials import CredentialsInterface

def _encode_header(value: str) -> str:
    try:
        value.encode("ascii")
        return value
    except UnicodeEncodeError:
        return str(Header(value, "utf-8"))

try:
    import pandas as pd  # optional at import time
except Exception:  # pragma: no cover
    pd = None


def expand_path(filename: str) -> Iterable[Path]:
    """Expand a (possibly masked) filename that may include globs (~, *, ?)."""
    p = Path(os.path.expandvars(os.path.expanduser(str(filename))))
    if any(ch in p.name for ch in ["*", "?", "["]):
        return Path(p.parent).glob(p.name)
    return [p]


class SendEmail(TemplateSupport, CredentialsInterface, FlowComponent):
    """
    SendEmail

    Renders a Jinja template per dataframe row and emails the output to the
    address in the configured `to` column.

    Properties
    ----------
    credentials / account : dict (required)
        SMTP credentials (hostname, port, username, password).
    template : str (required)
        Path to a Jinja template (HTML or text).
    subject : str (required)
        Jinja-templated subject, rendered per-row.
    to : str (required)
        Dataframe column containing the recipient email address.
    attachments : list[str] (optional)
        File paths or globs. Masks/globs supported via Flowtask masks.
    masks : dict (optional)
        Flowtask masks (applied to subject, template path and attachments).

    Input:  pandas.DataFrame (or list[dict]); Output: original input (pass-through).

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SendEmail:
          # attributes here
        ```
    """
    _version = "1.0.0"
    use_template: bool = True
    _credentials: dict = {
        "hostname": str,
        "port": int,
        "username": str,
        "password": str,
    }

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        job=None,
        stat=None,
        **kwargs,
    ):
        # alias 'account' → 'credentials' (compat with SendNotify)
        if "account" in kwargs and "credentials" not in kwargs:
            kwargs["credentials"] = kwargs.pop("account")

        self.subject: str = kwargs.get("subject", "")
        self.template: Optional[str] = kwargs.get("template")
        self.to: Optional[str] = kwargs.get("to")
        self.attachments: List[str] = kwargs.get("attachments", [])
        self._body_text: Optional[str] = kwargs.get("body", 'Hello, this is a test email.')
        self._list_attachment: List[Path] = []
        self._title_column: str = kwargs.get("title_column", "title")
        self.tpl_args: dict = kwargs.get("tpl_args", {})
        # enable TemplateSupport string rendering if available
        self.use_template = True

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

        await super().start(**kwargs)

        if not self.subject:
            raise ComponentError(
                "SendEmail: missing 'subject'."
            )
        if not self.template:
            raise ComponentError(
                "SendEmail: missing 'template' path."
            )
        if not self.to:
            raise ComponentError(
                "SendEmail: missing 'to' column name."
            )

        # expand env vars in credentials, coerce types
        self.processing_credentials()

        # masks on subject / template / attachments
        subj = self.subject
        tmpl = self.template
        if hasattr(self, "masks"):
            subj = self.mask_replacement(subj)
            tmpl = self.mask_replacement(tmpl)
            self.attachments = [self.mask_replacement(a) for a in self.attachments]

        # persist masked values
        self.subject = subj
        self.template = tmpl
        # read template file (absolute or relative)
        if not self.template_exists(self.template):
            raise FileNotFound(
                f"SendEmail: template file not found: {self.template}"
            )

        self.subject = subj  # store possibly masked subject

        # attachments (glob + existence check)
        self._list_attachment = []
        for item in self.attachments:
            for f in expand_path(item):
                self._list_attachment.append(Path(f))

        for f in self._list_attachment:
            if not f.exists():
                raise FileNotFound(f"SendEmail: attachment doesn't exist: {f}")

        # normalize input to DataFrame
        if self.data is None:
            raise ComponentError(
                "SendEmail: requires a dataframe input (got None)."
            )

        if pd is not None and isinstance(self.data, pd.DataFrame):
            self._df = self.data
        else:
            if pd is None:
                raise ComponentError(
                    "SendEmail: pandas is required to handle non-DataFrame inputs."
                )
            try:
                self._df = pd.DataFrame(self.data)
            except Exception as err:
                raise ComponentError(
                    f"SendEmail: invalid input; expected DataFrame or list of dicts: {err}"
                ) from err

        if self.to not in self._df.columns:
            raise ComponentError(
                f"SendEmail: 'to' column '{self.to}' not found in dataframe."
            )
        return True

    async def run(self):
        self._result = self.data  # pass-through

        account = {**self.credentials}
        if "port" in account:
            try:
                account["port"] = int(account["port"])
            except Exception:
                pass

        try:
            mail = Email(**account)
        except Exception as err:
            raise ComponentError(
                f"SendEmail: error creating Email provider: {err}"
            ) from err

        sent = 0
        errors = 0

        async with mail as m:
            for idx, row in self._df.iterrows():
                ctx: Dict[str, Union[str, int, float, None]] = row.to_dict()

                # subject / body render with TemplateSupport if available; fallback to str.format_map
                try:
                    subject = self.mask_replacement(self.subject)
                    subject = (
                        self._templateparser.from_string(subject, ctx)
                        if hasattr(self, "_templateparser")
                        else subject
                    )
                except Exception:
                    try:
                        subject = self.subject.format_map(ctx)  # best-effort
                    except Exception:
                        subject = self.subject

                try:
                    body_text = self.mask_replacement(self._body_text)
                    body = (
                        self._templateparser.from_string(body_text, ctx)
                        if hasattr(self, "_templateparser")
                        else body_text
                    )
                except Exception as err:
                    logging.exception(err)
                    raise ComponentError(
                        f"SendEmail: error rendering template for row {idx}: {err}"
                    ) from err

                intro_text = getattr(self, 'intro_text', "")
                try:
                    intro_text = self.mask_replacement(intro_text)
                    intro_text = (
                        self._templateparser.from_string(intro_text, ctx)
                        if hasattr(self, "_templateparser")
                        else intro_text
                    )
                except Exception:
                    pass

                _title = row.get(self._title_column, "No Title")
                _title = self.mask_replacement(_title)
                _title = self._templateparser.from_string(
                    _title, ctx
                ) if hasattr(self, "_templateparser") else _title

                _subtitle = row.get("subtitle", "")
                _subtitle = self.mask_replacement(_subtitle)
                _subtitle = self._templateparser.from_string(
                    _subtitle, ctx
                ) if hasattr(self, "_templateparser") else _subtitle

                to_value = row[self.to]
                if pd.isna(to_value):
                    to_value = None
                if not to_value or not isinstance(to_value, str):
                    errors += 1
                    self._logger.error(
                        f"SendEmail: invalid recipient in row {idx}: {to_value!r}"
                    )
                    continue

                # to_value = 'jlara@trocglobal.com'
                name = row.get("display_name") or row.get("name") or to_value
                actor = Actor(name=name, account={"address": to_value})

                atts = [str(p) for p in self._list_attachment] or []

                arguments = {}
                for key, val in self.tpl_args.items():
                    arguments[key] = row.get(val)
                message = await self._templateparser.async_render(
                    self.template, {
                        "title": _title,
                        "subtitle": _subtitle,
                        "intro_text": intro_text,
                        "body_text": body,
                        **arguments
                    }
                )
                subject = _encode_header(subject)
                try:
                    resp = await m.send(
                        recipient=actor,
                        subject=subject,
                        message=message,
                        attachments=atts,
                    )
                    if not resp:
                        raise RuntimeError(
                            "Email provider returned empty response"
                        )
                    sent += 1
                    self.add_metric(
                        "EmailSent",
                        {"to": to_value, "subject": subject, "result": str(resp)},
                    )
                    logging.info(
                        f"SendEmail: sent to {to_value} (row {idx})"
                    )
                except Exception as err:
                    errors += 1
                    self._logger.exception(
                        f"SendEmail: send failed for {to_value}: {err}"
                    )
                    # If your framework enforces SkipErrors, let it handle; otherwise raise
                    if getattr(self, "skipError", None) is None:
                        raise ComponentError(
                            f"SendEmail: send failed for {to_value}: {err}"
                        ) from err

        self.add_metric(
            "EmailSummary",
            {"sent": sent, "errors": errors, "total": int(self._df.shape[0])},
        )
        return self._result

    async def close(self):
        # Email provider is closed by the async context manager in run()
        return True

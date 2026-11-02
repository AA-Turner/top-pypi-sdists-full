"""Shared base for the models this SDK reads off another service's wire."""

from pydantic import BaseModel, ConfigDict


class ForwardCompatibleModel(BaseModel):
    """Base for every model a client reads: a field it does not know is ignored.

    A newer server may add fields, and a reader built on this base keeps reading the
    response or event. Subclasses must not set ``extra="forbid"``; a test checks every
    response and event model. Request models that a server validates, such as the
    ``session_workflow`` inputs, may stay strict: a client sends them and never reads
    them.

    The harness has the same base, under the same name, in
    ``mistralai.vibe.harness.app_server.session.models``.
    """

    model_config = ConfigDict(extra="ignore")

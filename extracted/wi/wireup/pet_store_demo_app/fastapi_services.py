from __future__ import annotations

from fastapi import Request
from typing_extensions import Annotated

from wireup import Inject, injectable

from pet_store_demo_app.services.session import SQLAlchemySession


@injectable(lifetime="scoped")
class AuthService:
    def __init__(
        self,
        request: Request,
        session: SQLAlchemySession,
        default_actor: Annotated[str, Inject(config="auth.demo_actor")],
    ) -> None:
        self.request = request
        self.session = session
        self.default_actor = default_actor

    def describe(self) -> dict[str, str]:
        actor = self.request.headers.get("x-demo-user", self.default_actor)
        return {
            "actor": actor,
            "path": self.request.url.path,
            "schema": self.session.schema,
        }

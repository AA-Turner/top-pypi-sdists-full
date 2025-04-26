import typing as t

from pydantic import UUID4, BaseModel


class SessionState(BaseModel):
    api_key: t.Optional[UUID4]
    jwt: t.Optional[str]

    def to_auth_headers(self) -> t.Dict[str, str]:
        headers: t.Dict[str, str] = {}
        if self.api_key:
            headers["X-Api-Key"] = str(self.api_key)
        if self.jwt:
            headers["Authorization"] = f"Bearer {self.jwt}"
        return headers

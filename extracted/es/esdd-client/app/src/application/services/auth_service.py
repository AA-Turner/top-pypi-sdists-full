from typing import Optional

from app.src.infrastructure.repositories.auth_repository_impl import AuthRepositoryImpl
from app.src.infrastructure.repositories.git_oauth_repository import GitOAuthRepository
from app.src.infrastructure.repositories.mpds_oauth_repository import (
    MPDSOAuthRepository,
)
from app.src.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl


class AuthService:
    def __init__(
        self,
        git_repo: Optional[GitOAuthRepository] = None,
        mpds_repo: Optional[MPDSOAuthRepository] = None,
        task_repo: Optional[TaskRepositoryImpl] = None,
        auth_repo: Optional[AuthRepositoryImpl] = None,
        api_url: Optional[str] = None,
    ) -> None:
        self.api_url = api_url or "http://localhost:8000"
        self.git = git_repo or GitOAuthRepository(api_url=self.api_url)
        self.mpds = mpds_repo or MPDSOAuthRepository(api_url=self.api_url)
        self.task_repo = task_repo
        self._current_token: Optional[str] = None
        self._current_user_id: Optional[int] = None
        self.auth_repo = auth_repo or AuthRepositoryImpl()

    async def is_authenticated(self, access_token) -> bool:
        return await self.auth_repo.is_authenticated(access_token)

    def set_token(self, token: str, user_id: Optional[int] = None) -> None:
        self._current_token = token
        self._current_user_id = user_id
        if self.task_repo:
            self.task_repo.set_token(token)

    def get_current_token(self) -> Optional[str]:
        return self._current_token

    def get_current_user_id(self) -> Optional[int]:
        return self._current_user_id

    def get_auth_url(
        self, provider: str = "github", redirect_url: Optional[str] = None
    ) -> str:
        if provider == "github":
            return self.git.generate_auth_url(redirect_url)
        elif provider == "mpds":
            return self.mpds.generate_auth_url(redirect_url)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def get_task_repository(self) -> TaskRepositoryImpl:
        if not self._current_token:
            raise ValueError("No token available. Please authenticate first.")

        if not self.task_repo:
            self.task_repo = TaskRepositoryImpl(
                api_url=self.api_url, token=self._current_token
            )

        return self.task_repo

    def clear_auth(self) -> None:
        self._current_token = None
        self._current_user_id = None
        if self.task_repo:
            self.task_repo.set_token(None)

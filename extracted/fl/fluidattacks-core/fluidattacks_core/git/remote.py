from .codecommit_utils import call_codecommit_ls_remote
from .https_utils import call_https_ls_remote
from .ssh_utils import call_ssh_ls_remote


async def ls_remote(
    repo_url: str,
    repo_branch: str,
    *,
    credential_key: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
    arn: str | None = None,
    org_external_id: str | None = None,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    if credential_key is not None:
        return await call_ssh_ls_remote(
            repo_url,
            credential_key,
            repo_branch,
        )

    if arn is not None and org_external_id is not None:
        return await call_codecommit_ls_remote(
            repo_url,
            arn,
            repo_branch,
            org_external_id=org_external_id,
            follow_redirects=follow_redirects,
        )

    return await call_https_ls_remote(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        branch=repo_branch,
        provider=provider,
        is_pat=is_pat,
        follow_redirects=follow_redirects,
    )

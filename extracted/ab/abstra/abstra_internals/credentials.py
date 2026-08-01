import os
from threading import Lock
from typing import Optional, Set

from abstra_internals.consts.filepaths import CREDENTIALS_FILEPATH
from abstra_internals.settings import Settings

credentials_lock = Lock()

# Tokens cloud-api has refused (see services/api_key_status). Only consulted to
# decide between the environment token and the one on disk: in a web editor pod
# the environment token comes from the deployment, so when it is revoked the only
# way to recover without replacing the pod is to let a token written at runtime
# take over. Process-wide and in-memory on purpose — a fresh process re-reads the
# deployment's token and starts from scratch.
_rejected_lock = Lock()
_rejected_tokens: Set[str] = set()


def mark_token_rejected(token: str) -> None:
    with _rejected_lock:
        _rejected_tokens.add(token)


def forget_token_rejection(token: str) -> None:
    """Un-reject a single token, for when it is handed back to us as current.

    Only that one: the whole point of the rejection is that the environment's
    token stays out of the way so a token stored at runtime can take over. A
    blanket clear here would hand the revoked environment token back on the very
    next call, which 401s, re-flags it and repairs again in a loop. Rejections
    never need to outlive the process — a redeploy is a new process with a fresh
    (and presumably working) environment token.
    """
    with _rejected_lock:
        _rejected_tokens.discard(token)


def _is_rejected(token: str) -> bool:
    with _rejected_lock:
        return token in _rejected_tokens


def _read_credentials_file() -> Optional[str]:
    with credentials_lock:
        try:
            credentials_path = Settings.root_path.joinpath(CREDENTIALS_FILEPATH)
        except Exception:
            # No project root configured yet. Resolving credentials must not
            # depend on that: the API key check runs on a background thread that
            # can fire before boot finishes, and raising here would leave a
            # revoked key undetected instead of merely unfixable.
            return None

        if not credentials_path.exists():
            return None

        with open(credentials_path, "r", encoding="utf-8") as f:
            return f.read().strip() or None


def get_credentials():
    """The token to authenticate against cloud-api with.

    The environment wins, as it always has: it is how deployed pods (web editor
    and workers) are given their credential. The file is the fallback for a local
    install — and the repair channel for a pod whose environment token has been
    revoked, which is the only case where the file overrides the environment.
    """
    env_token = os.getenv("ABSTRA_API_TOKEN")
    if env_token and not _is_rejected(env_token):
        return env_token

    file_token = _read_credentials_file()
    if file_token and not _is_rejected(file_token):
        return file_token

    # Everything known is rejected: keep answering with the deployment's token so
    # the failure stays the same one the caller already reports, instead of
    # silently swapping in another dead credential.
    return env_token or file_token


def delete_credentials():
    with credentials_lock:
        credentials_path = Settings.root_path.joinpath(CREDENTIALS_FILEPATH)

        if credentials_path.exists():
            credentials_path.unlink()


def set_credentials(token: str):
    with credentials_lock:
        credentials_path = Settings.root_path.joinpath(CREDENTIALS_FILEPATH)
        credentials_path.parent.mkdir(exist_ok=True)

        credentials_path.write_text(token, encoding="utf-8")

    forget_token_rejection(token)


def resolve_headers():
    credentials = get_credentials()

    if not credentials:
        return None

    return {"Api-Authorization": f"Bearer {credentials}"}


def resolve_headers_raise():
    headers = resolve_headers()
    if headers is None:
        raise Exception("You must be logged in to execute this operation")
    return headers

"""Auto-generated stub for module: loader."""
from typing import Any

from .models import AppManifest, CustomConfig

# Constants
DEFAULT_RETRIES: int
DEFAULT_TIMEOUT_SECONDS: float
MANIFEST_FILENAME: str
MAX_DOWNLOAD_BYTES: Any
MAX_UNPACKED_BYTES: Any
MAX_ZIP_ENTRIES: int
logger: Any

# Functions
def cache_root(cache_dir: str | Any.Any[str] | None = None) -> Any:
    """
    Where unpacked remote apps live. ``$MATRICE_APPS_CACHE`` overrides the default.
    """
    ...
def canonical_cache_url(url: str) -> str:
    """
    The cache identity of a URL: scheme + host + path. No query, no fragment.
    
        A presigned S3 URL carries ``X-Amz-Signature``/``-Date``/``-Credential``, all of which change
        every time the URL is minted. Keying the cache on the whole URL therefore produces a fresh
        entry directory and a full re-download on every single container start, forever. The signature
        identifies the *requester*; only the path identifies the *object*.
    
        The residual risk — a URL whose query selects the content — is covered by the
        ``content-<sha256-of-bytes>`` directory: a fresh fetch always lands in the right place. Only
        the immutable shortcut could serve the wrong bytes, and that needs an immutability marker in
        the path, which such a URL does not have.
    """
    ...
def load_app(ref: str | Any.Any[str]) -> Any:
    """
    Load and validate an app manifest. Raises :class:`AppLoadError` on any failure.
    
        This is the narrow entry point named in ``09`` §5. Use :func:`load_app_bundle` when you also
        need the folder, the resolved custom code, or the sample/golden files.
    """
    ...
def load_app_bundle(ref: str | Any.Any[str]) -> Any:
    """
    The full loader. See the module docstring for the stages.
    
        ``allow_remote_code`` vouches for the *provenance* of ``ref``: pass ``True`` when the reference
        came from somewhere authenticated (the platform's own usecase-download API) so that a remote
        app's ``logic.py`` may be executed. Left ``None``, a remote app carrying custom code is checked
        against the trusted-host set — see :func:`remote_code_allowed`.
    """
    ...
def load_manifest_file(path: str | Any.Any[str]) -> Any:
    """
    Parse and validate a single ``app.yaml``, with no folder, cache or custom-code handling.
    
        For tooling that only needs the schema verdict — ``matrice-analytics validate``, editors, the
        test generator. Use :func:`load_app` to actually run an app: only the full loader checks that
        ``logic.py`` imports and that declared fixtures exist.
    """
    ...
def redact_url(url: str) -> str:
    """
    A URL safe to log. A presigned query string is a bearer credential, not metadata.
    
        Public because anything that reports *which* reference failed has the same problem: a bundle
        candidate named in an error message travels straight into a log.
    """
    ...
def remote_code_allowed(url: str) -> bool:
    """
    May we ``exec_module()`` Python out of a zip fetched from this host?
    
        Deliberately a *host* check and not a content check: nothing about the bytes can tell us who
        produced them. ``$MATRICE_APPS_URL``'s own host is trusted implicitly — an operator who
        configured it has already chosen where apps come from.
    """
    ...
def resolve_ref(ref: str | Any.Any[str]) -> Any:
    """
    Turn a reference into a path or a URL.
    
        Accepted, in the order they are tried:
    
        1. ``http(s)://…`` — a zip of the app folder
        2. anything that looks like a path (absolute, contains a separator, or exists)
        3. a bare ``app_id`` or ``app_id@version``, resolved against ``MATRICE_APPS_ROOT`` (a folder)
           or ``MATRICE_APPS_URL`` (a zip base URL)
    
        Both the path and the URL form exist so that offline and local development never touch the
        network (``09`` §5).
    """
    ...

# Classes
class AppFetchError:
    # The app folder or zip could not be read/downloaded.

    ...
class AppLoadError(Exception):
    # Base class for every failure in resolve → fetch → unpack → validate → cache.

    ...
class AppRef:
    # A parsed app reference — the output of the *resolve* stage.

    ...
class AppResolveError:
    # The reference could not be turned into a folder or a URL.

    ...
class AppUnpackError:
    # The archive was rejected — traversal, symlink, or size/entry bounds.

    ...
class CustomCodeError:
    # ``logic.py`` is missing, does not contain the named symbol, or has no ``Config``.

    ...
class CustomImpl:
    # A resolved ``custom.impl`` reference, checked at load time.

    ...
class LoadedApp:
    # Everything the runtime needs about one app folder.

    def app_id(self: Any) -> str: ...

class ManifestValidationError:
    # ``app.yaml`` is not a valid manifest. Raised at load time, deliberately fatal.

    ...

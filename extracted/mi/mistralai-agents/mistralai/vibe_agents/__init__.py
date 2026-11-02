"""SDK for integrating with the vibe_agents platform.

This package has two submodules with different dependency profiles:

- `mistralai.vibe_agents.session_workflow`
    Pure session workflow contract types (pydantic only). Cheap to import,
    no `mistralai.workflows` dependency.

- `mistralai.vibe_agents.sessions_client`
    Typed sessions API HTTP client and response models. Import it only when
    the concrete httpx client is needed.

The root namespace intentionally does NOT eagerly re-export from
`sessions_client`. Import concrete submodules explicitly when you need them:

    from mistralai.vibe_agents.session_workflow import SessionWorkflowStartInput
    from mistralai.vibe_agents.sessions_client import SessionsClient

A future Speakeasy-generated client for the vibe_agents HTTP API will be
embedded as a sibling submodule (e.g. `mistralai.vibe_agents.worker_client`
or similar), following the same pattern as `mistralai.workflows` where the
Speakeasy-generated worker client lives alongside the handwritten SDK.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mistralai-agents")
except PackageNotFoundError:
    # A source tree put on sys.path without installing the distribution has no metadata.
    __version__ = "0.0.0+unknown"

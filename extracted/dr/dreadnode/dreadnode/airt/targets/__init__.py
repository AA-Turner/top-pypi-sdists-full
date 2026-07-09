"""Universal custom targets for AI red teaming.

A red-teaming *target* is any system you can send a message to and read a response
from. This package turns a declarative :class:`TargetSpec` into a dreadnode ``@task``
target that plugs straight into ``multimodal_attack`` / the attack studies —
regardless of where the model is deployed (AWS, Azure ML/AI Foundry, Google Vertex,
a self-hosted endpoint) or how it authenticates.

Two transports:

- ``http`` — request/response endpoints. Fully declarative: an endpoint, an auth scheme
  (:class:`TargetAuth`), a JSON request template placing ``{prompt}`` / ``{image_b64}`` /
  ``{audio_b64}`` / ``{video_b64}``, and a JSONPath to the response text. Covers Azure
  ML / AI Foundry, Vertex ``predict``, SageMaker sync-invoke, OpenAI-compatible, etc.

- ``streaming`` — realtime / speech-to-speech protocols with a bespoke handshake. The
  spec *selects* a protocol adapter; ``nova_sonic`` (Amazon Bedrock bidirectional S2S)
  ships in :mod:`dreadnode.airt.targets.streaming`.

Module layout: :mod:`spec` (models) · :mod:`message` (payload conversion) ·
:mod:`auth` (auth strategies) · :mod:`http` (HTTP transport) · :mod:`streaming`
(streaming adapters) · :mod:`factory` (:func:`build_target` dispatcher).

Credentials are always read from environment variables / platform secrets — never
inlined into the spec.
"""

from dreadnode.airt.targets.factory import build_target
from dreadnode.airt.targets.spec import AuthType, TargetAuth, TargetSpec, Transport
from dreadnode.airt.targets.streaming import nova_sonic_target

__all__ = [
    "AuthType",
    "TargetAuth",
    "TargetSpec",
    "Transport",
    "build_target",
    "nova_sonic_target",
]

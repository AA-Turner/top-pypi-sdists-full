"""Prediction targets: query a classifier's predict API and read back a numeric
prediction (probabilities / logits / label).

This is the numeric counterpart to the text :class:`~dreadnode.airt.targets.spec.TargetSpec`.
Model-extraction and membership-inference attacks need the model's *output vector*
(a softmax over classes or a hard label), not free text — so a target here returns a
structured :class:`Prediction` parsed from the JSON body via JSONPath.

The same declarative shape covers a shipped Dreadnode environment (`endpoint` =
injected challenge URL, `auth` = none) and a user's own model in Azure ML / Azure
Container Apps / SageMaker / any HTTP predict endpoint (`auth` = api_key / bearer /
aws_sigv4 / azure_ad). Only the spec changes; the attacks are identical.
"""

import asyncio
import json
import typing as t

import httpx
import numpy as np
from pydantic import BaseModel, Field

from dreadnode.airt.targets.auth import apply_auth
from dreadnode.airt.targets.spec import TargetSpec
from dreadnode.core.task import Task, task

#: How the query input is rendered into the request body's ``{input}`` placeholder.
PredictionInputFormat = t.Literal["json_array", "image_b64", "text"]
#: Which output the endpoint returns (and which the attack should treat as primary).
PredictionOutput = t.Literal["probabilities", "logits", "label"]

#: A single query input: a feature vector (tabular), a base64 string (image), or text.
QueryInput = t.Sequence[float] | np.ndarray | str | bytes


class Prediction(BaseModel):
    """A single model prediction. At least one field is populated; ``label`` is
    derived from ``probabilities``/``logits`` (argmax) when the endpoint returns only
    a soft output."""

    label: int | str | None = None
    probabilities: list[float] | None = None
    logits: list[float] | None = None

    @property
    def vector(self) -> list[float] | None:
        """The soft output vector (probabilities preferred, else logits)."""
        if self.probabilities is not None:
            return self.probabilities
        return self.logits

    @property
    def hard_label(self) -> int | str | None:
        """A concrete label: the explicit one, else argmax of the soft vector."""
        if self.label is not None:
            return self.label
        vec = self.vector
        return int(np.argmax(vec)) if vec else None


class PredictionTargetSpec(TargetSpec):
    """Declarative description of a numeric predict endpoint. Subclasses
    :class:`TargetSpec` so it reuses ``endpoint``/``auth``/``timeout_s`` and the auth
    machinery; the text-only fields (``response_text_path`` etc.) are unused here."""

    #: Request body with a single ``{input}`` placeholder (rendered per ``input_format``).
    request_template: str = '{"inputs": {input}}'
    #: What the endpoint returns / the attack's primary signal.
    output: PredictionOutput = "probabilities"
    #: JSONPath to the probability vector.
    probabilities_path: str = "$.probabilities"
    #: JSONPath to the logits vector.
    logits_path: str = "$.logits"
    #: JSONPath to the scalar predicted label.
    label_path: str = "$.label"
    #: Optional JSONPath to human-readable class names.
    class_names_path: str | None = None
    #: How ``{input}`` is encoded into the request body.
    input_format: PredictionInputFormat = "json_array"
    #: Number of classes; inferred from the soft vector when omitted.
    num_classes: int | None = None
    name: str = "prediction_target"
    #: Max concurrent in-flight queries for :func:`predict_many`.
    max_concurrency: int = Field(default=16, ge=1)


def _jsonpath_first(data: t.Any, path: str | None) -> t.Any:
    if not path:
        return None
    from jsonpath_ng.ext import parse as jp_parse

    matches = [m.value for m in jp_parse(path).find(data)]
    return matches[0] if matches else None


def _to_float_list(x: QueryInput) -> list[float]:
    arr = np.asarray(x, dtype=np.float64).ravel()
    return [float(v) for v in arr.tolist()]


def _to_b64(x: QueryInput) -> str:
    import base64

    if isinstance(x, str):
        return x  # already base64
    if isinstance(x, bytes):
        return base64.b64encode(x).decode("ascii")
    raise TypeError("image_b64 input must be a base64 str or raw bytes")


def render_prediction_body(
    template: str, x: QueryInput, input_format: PredictionInputFormat
) -> dict:
    """Render the request body for one query input.

    ``json_array`` inserts a JSON array (template supplies no quotes: ``{"features": {input}}``);
    ``text``/``image_b64`` insert a string value (template supplies the quotes: ``{"text": "{input}"}``).
    """
    if input_format == "json_array":
        token = json.dumps(_to_float_list(x))
    elif input_format == "text":
        # Escape for embedding inside the template's quotes; drop the outer quotes.
        token = json.dumps(str(x))[1:-1]
    else:  # image_b64
        token = _to_b64(x)
    return json.loads(template.replace("{input}", token))


def parse_prediction(data: t.Any, spec: PredictionTargetSpec) -> Prediction:
    """Parse a JSON response body into a :class:`Prediction` via the spec's JSONPaths."""
    probs = _jsonpath_first(data, spec.probabilities_path)
    logits = _jsonpath_first(data, spec.logits_path)
    label = _jsonpath_first(data, spec.label_path)
    return Prediction(
        label=label,
        probabilities=[float(v) for v in probs] if isinstance(probs, list) else None,
        logits=[float(v) for v in logits] if isinstance(logits, list) else None,
    )


async def predict_call(
    spec: PredictionTargetSpec, x: QueryInput, *, client: httpx.AsyncClient | None = None
) -> Prediction:
    """POST one query to the endpoint (with auth) and parse the prediction.

    Kept free of the ``@task`` wrapper so request/response logic is unit-testable
    without tracing/storage. Pass ``client`` to reuse a connection pool across queries.
    """
    body = render_prediction_body(spec.request_template, x, spec.input_format)
    content = json.dumps(body).encode("utf-8")
    headers = apply_auth(spec, {"Content-Type": "application/json"}, spec.endpoint, content)

    owns_client = client is None
    client = client or httpx.AsyncClient(timeout=spec.timeout_s)
    try:
        resp = await client.post(spec.endpoint, content=content, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    finally:
        if owns_client:
            await client.aclose()
    return parse_prediction(data, spec)


async def predict_many(
    spec: PredictionTargetSpec,
    xs: t.Sequence[QueryInput],
    *,
    client: httpx.AsyncClient | None = None,
) -> list[Prediction]:
    """Query a batch of inputs concurrently over one connection pool.

    This is the campaign primitive used by extraction / membership attacks —
    ``len(xs)`` counts toward the query budget. Concurrency is bounded by
    ``spec.max_concurrency``. Pass ``client`` to reuse an existing pool (or inject a
    test transport); otherwise one is created and closed here.
    """
    semaphore = asyncio.Semaphore(spec.max_concurrency)
    owns_client = client is None
    client = client or httpx.AsyncClient(timeout=spec.timeout_s)

    async def _one(x: QueryInput) -> Prediction:
        async with semaphore:
            return await predict_call(spec, x, client=client)

    try:
        return await asyncio.gather(*(_one(x) for x in xs))
    finally:
        if owns_client:
            await client.aclose()


def build_prediction_target(spec: PredictionTargetSpec) -> Task[..., Prediction]:
    """Build a dreadnode ``@task`` that predicts one input → :class:`Prediction`
    (one span per query, for when per-query tracing is wanted).

    Example (Azure Container Apps, API key)::

        from dreadnode.airt import PredictionTargetSpec, TargetAuth
        spec = PredictionTargetSpec(
            endpoint="https://fraud-api.<region>.azurecontainerapps.io/predict",
            auth=TargetAuth(type="api_key", header="X-API-Key", env_var="ACA_KEY"),
            request_template='{"features": {input}}',
            probabilities_path="$.probabilities",
        )
    """

    async def target(x: QueryInput) -> Prediction:
        return await predict_call(spec, x)

    return task(target, name=spec.name)

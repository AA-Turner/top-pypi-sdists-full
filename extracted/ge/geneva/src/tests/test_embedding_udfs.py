# ruff: noqa: ANN201, ANN202, PIE804
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import sys
import types

import numpy as np
import pyarrow as pa
import pytest

import geneva.udfs.embeddings as embedding_mod
import geneva.udfs.gemini as gemini_mod
import geneva.udfs.openai as openai_mod
from geneva import connect
from geneva.transformer import UDFArgType
from geneva.udfs.embeddings import gemini_embedding_udf, sentence_transformer_udf
from geneva.udfs.gemini import gemini_udf
from geneva.udfs.openai import openai_embedding_udf, openai_udf
from geneva.udfs.text.embeddings import _build_embedding_udf


class DummySentenceTransformer:
    def __init__(self, model_name, device=None) -> None:
        self.model_name = model_name
        self.device = device

    def get_sentence_embedding_dimension(self) -> int:
        return 2

    def encode(self, values, **kwargs):
        return np.asarray(
            [[float(len(value)), float(len(value) + 1)] for value in values],
            dtype=np.float32,
        )


@pytest.fixture
def mock_sentence_transformers(monkeypatch):
    instances = []

    def _loader(model_name, device=None):
        model = DummySentenceTransformer(model_name, device=device)
        instances.append(model)
        return model

    def _patched_loader(model_name, device=None, trust_remote_code=False):
        return _loader(model_name, device=device)

    monkeypatch.setattr(
        embedding_mod._SentenceTransformersModel,
        "_load_model",
        staticmethod(_patched_loader),
    )
    monkeypatch.setattr(embedding_mod, "_resolve_device", lambda num_gpus: None)
    return instances


def test_mock_embedding_udf_flow(tmp_path, mock_sentence_transformers) -> None:
    db = connect(tmp_path)
    table = db.create_table(
        "documents",
        pa.Table.from_pydict({"body": ["hello", "world"]}),
    )

    udf = sentence_transformer_udf(
        "fake-model/1",
        column="body",
        normalize=False,
    )

    assert udf.func.dimension == 2

    batch = pa.RecordBatch.from_arrays([pa.array(["test"])], ["body"])
    assert udf(batch).to_pylist() == [[4.0, 5.0]]

    # test empty column handling
    empty_batch = pa.RecordBatch.from_arrays([pa.array([], type=pa.string())], ["body"])
    assert udf(empty_batch).to_pylist() == []

    table.add_columns({"embedding": udf})

    # test null handling
    batch_with_nulls = pa.RecordBatch.from_arrays(
        [pa.array(["geneva", None, "udf"])], ["body"]
    )
    assert len(udf(batch_with_nulls).to_pylist()) == 3


def test_missing_column(mock_sentence_transformers) -> None:
    # The embedder is an Array UDF over its configured column; the framework
    # projects and dispatches that column, so a batch missing it errors on
    # dispatch rather than inside embed().
    udf = sentence_transformer_udf("fake-model/2", column="title")
    assert udf.arg_type is UDFArgType.ARRAY
    assert udf.input_columns == ["title"]
    batch = pa.RecordBatch.from_arrays([pa.array(["hello"])], ["body"])
    with pytest.raises(KeyError, match="title"):
        udf(batch)


# ---------------------------------------------------------------------------
# Gemini embedding UDF tests
# ---------------------------------------------------------------------------

_FAKE_DIM = 3


class _FakeContentEmbedding:
    """Mimics a ``google.genai`` ``ContentEmbedding`` object."""

    def __init__(self, values: list[float]) -> None:
        self.values = values


class _FakeEmbedResult:
    """Mimics the result of ``client.models.embed_content(...)``."""

    def __init__(self, embeddings: list[_FakeContentEmbedding]) -> None:
        self.embeddings = embeddings


class _FakeModels:
    """Mimics ``client.models`` on a ``genai.Client``."""

    def embed_content(self, *, model, contents, config=None):
        output_dim = _FAKE_DIM
        if config is not None and config.output_dimensionality is not None:
            output_dim = config.output_dimensionality
        if isinstance(contents, list):
            embs = [
                _FakeContentEmbedding([float(i + 1)] * output_dim)
                for i, _ in enumerate(contents)
            ]
        else:
            embs = [_FakeContentEmbedding([0.5] * output_dim)]
        return _FakeEmbedResult(embs)


class _FakeGeminiClient:
    """Minimal stand-in for ``genai.Client``."""

    def __init__(self) -> None:
        self.models = _FakeModels()


@pytest.fixture
def mock_gemini_embedding(monkeypatch):
    """Patch _GeminiEmbeddingModel._build_model to return a fake client."""
    # The embed() path lazy-imports google.genai.types for EmbedContentConfig,
    # so the fake client alone isn't enough — skip if google-genai is missing.
    pytest.importorskip("google.genai")
    fake = _FakeGeminiClient()

    def _build(self):  # noqa: ANN001, ANN202
        return fake

    monkeypatch.setattr(embedding_mod._GeminiEmbeddingModel, "_build_model", _build)
    monkeypatch.setattr("geneva.udfs.text.embeddings._gemini_retry", lambda: None)
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    return fake


def test_gemini_embedding_basic(mock_gemini_embedding) -> None:
    udf = gemini_embedding_udf(
        column="body", output_dimensionality=_FAKE_DIM, dimension=_FAKE_DIM
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", "world"])], ["body"])
    result = udf(batch).to_pylist()

    assert len(result) == 2
    assert result[0] == [1.0, 1.0, 1.0]
    assert result[1] == [2.0, 2.0, 2.0]


def test_gemini_embedding_null_handling(mock_gemini_embedding) -> None:
    udf = gemini_embedding_udf(
        column="body", output_dimensionality=_FAKE_DIM, dimension=_FAKE_DIM
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", None, "world"])], ["body"])
    result = udf(batch).to_pylist()

    assert len(result) == 3
    assert result[0] == [1.0, 1.0, 1.0]
    assert result[1] is None
    assert result[2] == [2.0, 2.0, 2.0]


def test_gemini_embedding_empty_batch(mock_gemini_embedding) -> None:
    udf = gemini_embedding_udf(column="body", dimension=_FAKE_DIM)

    batch = pa.RecordBatch.from_arrays([pa.array([], type=pa.string())], ["body"])
    assert udf(batch).to_pylist() == []


def test_gemini_embedding_dimension_from_known_model(mock_gemini_embedding) -> None:
    udf = gemini_embedding_udf(column="body", model="gemini-embedding-001")
    # Dimension should be resolved from the lookup table (3072)
    assert udf.func.dimension == 3072


def test_gemini_embedding_output_dimensionality(mock_gemini_embedding) -> None:
    udf = gemini_embedding_udf(column="body", output_dimensionality=2, dimension=2)

    batch = pa.RecordBatch.from_arrays([pa.array(["test"])], ["body"])
    result = udf(batch).to_pylist()
    assert result == [[1.0, 1.0]]


def test_gemini_embedding_unknown_model_warns(mock_gemini_embedding) -> None:
    with pytest.warns(UserWarning, match="Unknown Gemini embedding model"):
        gemini_embedding_udf(
            column="body", model="not-a-real-model", dimension=_FAKE_DIM
        )


# ---------------------------------------------------------------------------
# Gemini generative UDF tests
# ---------------------------------------------------------------------------


class _FakeGenerateResponse:
    """Mimics the result of ``client.models.generate_content(...)``."""

    def __init__(self, text: str) -> None:
        self.text = text


class _FakeGenerativeModels:
    """Mimics ``client.models`` for generative content."""

    def generate_content(self, *, model, contents):
        if isinstance(contents, list):
            # binary input: contents is [Part, prompt_str]
            return _FakeGenerateResponse("binary response")
        return _FakeGenerateResponse(f"response to: {contents}")


class _FakeGenerativeClient:
    """Minimal stand-in for ``genai.Client`` for generative UDF."""

    def __init__(self) -> None:
        self.models = _FakeGenerativeModels()


@pytest.fixture
def mock_gemini_generative(monkeypatch):
    """Patch _GeminiModel.client to return a fake client."""
    # gemini_udf's binary path lazy-imports google.genai.types for Part —
    # skip if the package is missing.
    pytest.importorskip("google.genai")
    fake = _FakeGenerativeClient()

    monkeypatch.setattr(
        gemini_mod._GeminiModel,
        "client",
        property(lambda self: fake),
    )
    monkeypatch.setattr("geneva.udfs.text.gemini._gemini_retry", lambda: None)
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    return fake


def test_gemini_udf_text_generation(mock_gemini_generative) -> None:
    udf_instance = gemini_udf(
        column="body",
        prompt="Summarise this",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello world"])], ["body"])
    result = udf_instance(batch).to_pylist()

    assert len(result) == 1
    assert result[0] == "response to: Summarise this\n\nhello world"


def test_gemini_udf_binary_input(mock_gemini_generative) -> None:
    udf_instance = gemini_udf(
        column="image",
        prompt="Describe this image",
        mime_type="image/jpeg",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays(
        [pa.array([b"\x89PNG fake"], type=pa.binary())], ["image"]
    )
    result = udf_instance(batch).to_pylist()

    assert len(result) == 1
    assert result[0] == "binary response"


def test_gemini_udf_missing_mime_type(mock_gemini_generative) -> None:
    udf_instance = gemini_udf(
        column="image",
        prompt="Describe",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays(
        [pa.array([b"\x89PNG fake"], type=pa.binary())], ["image"]
    )
    with pytest.raises(ValueError, match="mime_type is required"):
        udf_instance(batch)


def test_gemini_udf_null_handling(mock_gemini_generative) -> None:
    udf_instance = gemini_udf(
        column="body",
        prompt="Summarise",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", None, "world"])], ["body"])
    result = udf_instance(batch).to_pylist()

    assert len(result) == 3
    assert result[0] is not None
    assert result[1] is None
    assert result[2] is not None


def test_gemini_udf_unknown_model_warns(mock_gemini_generative) -> None:
    with pytest.warns(UserWarning, match="Unknown Gemini model"):
        gemini_udf(
            column="body",
            prompt="test",
            model="not-a-real-model",
            version="v1",
        )


# ---------------------------------------------------------------------------
# OpenAI embedding UDF tests
# ---------------------------------------------------------------------------

_FAKE_OPENAI_DIM = 3


class _FakeOpenAIEmbeddingData:
    """Mimics an OpenAI ``Embedding`` object."""

    def __init__(self, embedding: list[float]) -> None:
        self.embedding = embedding


class _FakeOpenAIUsage:
    """Mimics the ``usage`` block, which reports the real token count."""

    def __init__(self, prompt_tokens: int) -> None:
        self.prompt_tokens = prompt_tokens
        self.total_tokens = prompt_tokens


class _FakeOpenAIEmbedResponse:
    """Mimics the result of ``client.embeddings.create(...)``."""

    def __init__(
        self, data: list[_FakeOpenAIEmbeddingData], prompt_tokens: int = 0
    ) -> None:
        self.data = data
        self.usage = _FakeOpenAIUsage(prompt_tokens)


class _FakeOpenAIEmbeddings:
    """Mimics ``client.embeddings`` on an ``openai.OpenAI``.

    Records the inputs of every request in ``calls`` so tests can assert how
    a batch was split.  When *echo* is set, each embedding encodes its own
    input text (which must parse as a float), which lets tests verify that
    embeddings land on the right rows across request boundaries.
    """

    def __init__(
        self,
        echo: bool = False,
        reject_over: int | None = None,
        bytes_per_token: int = 4,
        report_usage: bool = True,
        fail_with: Exception | None = None,
    ) -> None:
        self.echo = echo
        self.calls: list[list[str]] = []
        # Reject any request with more than this many inputs, the way the API
        # rejects one over its token cap.
        self.reject_over = reject_over
        # Bytes per token this fake "tokenizer" reports back through usage.
        self.bytes_per_token = bytes_per_token
        # When false the response carries no usable token count, which pins
        # chunking to the opening estimate instead of a calibrated one.
        self.report_usage = report_usage
        self.fail_with = fail_with

    def create(self, *, input, model, **kwargs):  # noqa: A002
        self.calls.append(list(input))
        if self.reject_over is not None and len(input) > self.reject_over:
            raise _bad_request(
                f"Requested {len(input)} inputs, max {self.reject_over} "
                "tokens per request"
            )
        if self.fail_with is not None:
            raise self.fail_with
        dim = kwargs.get("dimensions") or _FAKE_OPENAI_DIM
        if self.echo:
            data = [_FakeOpenAIEmbeddingData([float(text)] * dim) for text in input]
        else:
            data = [
                _FakeOpenAIEmbeddingData([float(i + 1)] * dim)
                for i, _ in enumerate(input)
            ]
        if not self.report_usage:
            return _FakeOpenAIEmbedResponse(data, prompt_tokens=0)
        total = sum(len(text.encode("utf-8")) for text in input)
        tokens = total // self.bytes_per_token
        return _FakeOpenAIEmbedResponse(data, prompt_tokens=max(1, tokens))


class _FakeOpenAIEmbeddingClient:
    """Minimal stand-in for ``openai.OpenAI`` for embedding UDF."""

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        self.embeddings = _FakeOpenAIEmbeddings(**kwargs)


def _bad_request(message: str) -> Exception:
    """Build a real ``openai.BadRequestError`` carrying ``message``."""
    import httpx
    import openai

    response = httpx.Response(
        400, request=httpx.Request("POST", "https://api.openai.com/v1/embeddings")
    )
    return openai.BadRequestError(message, response=response, body=None)


def _install_fake_openai_embedding(monkeypatch, **kwargs):  # noqa: ANN003
    """Patch _OpenAIEmbeddingModel._build_model to return a fake client."""
    fake = _FakeOpenAIEmbeddingClient(**kwargs)

    def _build(self):  # noqa: ANN001, ANN202
        return fake

    monkeypatch.setattr(openai_mod._OpenAIEmbeddingModel, "_build_model", _build)
    monkeypatch.setattr(openai_mod, "_openai_retry", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    return fake


@pytest.fixture
def mock_openai_embedding(monkeypatch):
    return _install_fake_openai_embedding(monkeypatch)


@pytest.fixture
def mock_openai_embedding_echo(monkeypatch):
    """Fake client whose embeddings echo their input text."""
    return _install_fake_openai_embedding(monkeypatch, echo=True)


def test_openai_embedding_basic(mock_openai_embedding) -> None:
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", "world"])], ["body"])
    result = udf_inst(batch).to_pylist()

    assert len(result) == 2
    assert result[0] == [1.0, 1.0, 1.0]
    assert result[1] == [2.0, 2.0, 2.0]


def test_openai_embedding_null_handling(mock_openai_embedding) -> None:
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", None, "world"])], ["body"])
    result = udf_inst(batch).to_pylist()

    assert len(result) == 3
    assert result[0] == [1.0, 1.0, 1.0]
    assert result[1] is None
    assert result[2] == [2.0, 2.0, 2.0]


def test_openai_embedding_empty_batch(mock_openai_embedding) -> None:
    udf_inst = openai_embedding_udf(column="body", dimension=_FAKE_OPENAI_DIM)

    batch = pa.RecordBatch.from_arrays([pa.array([], type=pa.string())], ["body"])
    assert udf_inst(batch).to_pylist() == []


def test_openai_embedding_dimension_from_known_model(
    mock_openai_embedding,
) -> None:
    udf_inst = openai_embedding_udf(column="body", model="text-embedding-3-small")
    # Dimension should be resolved from the lookup table (1536)
    assert udf_inst.func.dimension == 1536


def test_openai_embedding_output_dimensionality(mock_openai_embedding) -> None:
    udf_inst = openai_embedding_udf(column="body", output_dimensionality=2, dimension=2)

    batch = pa.RecordBatch.from_arrays([pa.array(["test"])], ["body"])
    result = udf_inst(batch).to_pylist()
    assert result == [[1.0, 1.0]]


def test_openai_embedding_single_request_under_limits(mock_openai_embedding) -> None:
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", "world"])], ["body"])
    udf_inst(batch)

    assert mock_openai_embedding.embeddings.calls == [["hello", "world"]]


def test_openai_embedding_all_null_batch_makes_no_request(
    mock_openai_embedding,
) -> None:
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    batch = pa.RecordBatch.from_arrays(
        [pa.array([None, None], type=pa.string())], ["body"]
    )
    assert udf_inst(batch).to_pylist() == [None, None]
    assert mock_openai_embedding.embeddings.calls == []


def test_openai_embedding_chunks_by_max_inputs(mock_openai_embedding_echo) -> None:
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_inputs_per_request=2,
    )

    texts = [str(i) for i in range(5)]
    batch = pa.RecordBatch.from_arrays([pa.array(texts)], ["body"])
    result = udf_inst(batch).to_pylist()

    assert mock_openai_embedding_echo.embeddings.calls == [
        ["0", "1"],
        ["2", "3"],
        ["4"],
    ]
    # Each row keeps the embedding of its own text across chunk boundaries.
    assert result == [[float(i)] * _FAKE_OPENAI_DIM for i in range(5)]


def test_openai_embedding_chunks_by_token_budget(monkeypatch) -> None:
    # 400 bytes at the opening 4.0 bytes/token estimate is ~101 tokens, so
    # two fit a 250 token budget and the third opens a new request. Usage is
    # withheld so this pins chunking alone, not the calibration on top of it.
    client = _install_fake_openai_embedding(monkeypatch, report_usage=False)
    text = "x" * 400
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_tokens_per_request=250,
    )

    batch = pa.RecordBatch.from_arrays([pa.array([text] * 5)], ["body"])
    udf_inst(batch)

    sizes = [len(call) for call in client.embeddings.calls]
    assert sizes == [2, 2, 1]


def test_openai_embedding_token_budget_counts_utf8_bytes(monkeypatch) -> None:
    """The estimate is bytes, not characters.

    This is the CJK case the character heuristic got wrong: the same character
    count costs three times the bytes, and close to one token per character, so
    it has to chunk more aggressively -- not identically.
    """
    ascii_client = _install_fake_openai_embedding(monkeypatch, report_usage=False)
    chars = 200
    udf_ascii = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_tokens_per_request=400,
    )
    batch = pa.RecordBatch.from_arrays([pa.array(["x" * chars] * 4)], ["body"])
    udf_ascii(batch)
    ascii_sizes = [len(c) for c in ascii_client.embeddings.calls]

    cjk_client = _install_fake_openai_embedding(monkeypatch, report_usage=False)
    udf_cjk = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_tokens_per_request=400,
    )
    # Same number of characters, three bytes each.
    batch = pa.RecordBatch.from_arrays([pa.array(["\u6df1" * chars] * 4)], ["body"])
    udf_cjk(batch)
    cjk_sizes = [len(c) for c in cjk_client.embeddings.calls]

    assert ascii_sizes == [4]
    assert cjk_sizes == [2, 2]


def test_openai_embedding_calibrates_from_reported_usage(monkeypatch) -> None:
    """A response reports the real token count, so the next request grows.

    The opening estimate is 4.0 bytes/token. This fake bills 8, so after one
    response the model knows it can send twice as much per request -- learned
    from a success, with no rejection needed to teach it.
    """
    client = _install_fake_openai_embedding(monkeypatch, bytes_per_token=8)
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_tokens_per_request=100,
    )

    texts = ["y" * 200] * 12
    batch = pa.RecordBatch.from_arrays([pa.array(texts)], ["body"])
    udf_inst(batch)

    sizes = [len(c) for c in client.embeddings.calls]
    # 200 bytes is ~51 estimated tokens at first, so only one fits the 100
    # token budget; usage reports 25, and every later request carries more.
    assert sizes[0] == 1
    assert max(sizes) > sizes[0]
    assert sum(sizes) == len(texts)


def test_openai_embedding_bisects_a_rejected_request(monkeypatch) -> None:
    """An over-cap 400 is recovered by halving, not by failing the batch."""
    client = _install_fake_openai_embedding(monkeypatch, echo=True, reject_over=2)
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    texts = [str(i) for i in range(8)]
    batch = pa.RecordBatch.from_arrays([pa.array(texts)], ["body"])
    result = udf_inst(batch).to_pylist()

    # The whole chunk goes out first, then halves until the pieces fit.
    assert client.embeddings.calls[0] == texts
    accepted = [c for c in client.embeddings.calls if len(c) <= 2]
    assert accepted == [["0", "1"], ["2", "3"], ["4", "5"], ["6", "7"]]
    # Every row still gets its own embedding, in its own position.
    assert result == [[float(i)] * _FAKE_OPENAI_DIM for i in range(8)]


def test_openai_embedding_reraises_unrelated_bad_request(monkeypatch) -> None:
    """A 400 that is not about size is not worth splitting -- fail fast."""
    import openai

    client = _install_fake_openai_embedding(
        monkeypatch, fail_with=_bad_request("Unsupported dimensions for this model")
    )
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["a", "b", "c", "d"])], ["body"])
    with pytest.raises(openai.BadRequestError):
        udf_inst(batch)

    # One attempt, not a bisection cascade.
    assert len(client.embeddings.calls) == 1


def test_openai_embedding_reraises_a_single_oversized_input(monkeypatch) -> None:
    """One input over the per-input limit cannot be split; surface the error."""
    import openai

    client = _install_fake_openai_embedding(monkeypatch, reject_over=0)
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["only"])], ["body"])
    with pytest.raises(openai.BadRequestError):
        udf_inst(batch)

    assert client.embeddings.calls == [["only"]]


def test_openai_embedding_oversized_input_sent_alone(mock_openai_embedding) -> None:
    # The middle text alone exceeds the budget; it gets its own request
    # rather than failing locally.
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_tokens_per_request=100,
    )

    huge = "x" * 4000
    batch = pa.RecordBatch.from_arrays([pa.array(["a", huge, "b"])], ["body"])
    udf_inst(batch)

    assert mock_openai_embedding.embeddings.calls == [["a"], [huge], ["b"]]


def test_openai_embedding_chunking_preserves_null_positions(
    mock_openai_embedding_echo,
) -> None:
    udf_inst = openai_embedding_udf(
        column="body",
        output_dimensionality=_FAKE_OPENAI_DIM,
        dimension=_FAKE_OPENAI_DIM,
        max_inputs_per_request=2,
    )

    batch = pa.RecordBatch.from_arrays(
        [pa.array(["0", None, "1", "2", None, "3"])], ["body"]
    )
    result = udf_inst(batch).to_pylist()

    assert mock_openai_embedding_echo.embeddings.calls == [["0", "1"], ["2", "3"]]
    assert result == [
        [0.0] * _FAKE_OPENAI_DIM,
        None,
        [1.0] * _FAKE_OPENAI_DIM,
        [2.0] * _FAKE_OPENAI_DIM,
        None,
        [3.0] * _FAKE_OPENAI_DIM,
    ]


def test_openai_embedding_unknown_model_warns(mock_openai_embedding) -> None:
    with pytest.warns(UserWarning, match="Unknown OpenAI embedding model"):
        openai_embedding_udf(
            column="body", model="not-a-real-model", dimension=_FAKE_OPENAI_DIM
        )


def test_embedding_udfs_are_array_udfs_scoped_to_their_column(
    mock_openai_embedding, mock_sentence_transformers, mock_gemini_embedding
) -> None:
    """Embedding UDFs are Array UDFs projected to just their text column.

    Declaring input_columns=[column] lets the scanner read only that column
    (GEN-921) instead of the whole row, and dispatches it as a pa.Array.
    """
    for inst, column in [
        (openai_embedding_udf(column="body", dimension=_FAKE_OPENAI_DIM), "body"),
        (sentence_transformer_udf("fake-model/9", column="title"), "title"),
        (gemini_embedding_udf(column="caption", dimension=_FAKE_DIM), "caption"),
    ]:
        assert inst.arg_type is UDFArgType.ARRAY
        assert inst.input_columns == [column]


# ---------------------------------------------------------------------------
# OpenAI generative (Chat Completions) UDF tests
# ---------------------------------------------------------------------------


class _FakeOpenAIMessage:
    """Mimics ``response.choices[0].message``."""

    def __init__(self, content: str) -> None:
        self.content = content


class _FakeOpenAIChoice:
    """Mimics ``response.choices[0]``."""

    def __init__(self, message: _FakeOpenAIMessage) -> None:
        self.message = message


class _FakeOpenAIChatResponse:
    """Mimics the result of ``client.chat.completions.create(...)``."""

    def __init__(self, choices: list[_FakeOpenAIChoice]) -> None:
        self.choices = choices


class _FakeOpenAIChatCompletions:
    """Mimics ``client.chat.completions``."""

    def create(self, *, model, messages):
        content = messages[0].get("content", "")
        if isinstance(content, list):
            # binary/image input
            return _FakeOpenAIChatResponse(
                [_FakeOpenAIChoice(_FakeOpenAIMessage("binary response"))]
            )
        return _FakeOpenAIChatResponse(
            [_FakeOpenAIChoice(_FakeOpenAIMessage(f"response to: {content}"))]
        )


class _FakeOpenAIChatClient:
    """Minimal stand-in for ``openai.OpenAI`` for chat completions."""

    def __init__(self) -> None:
        self.chat = type("Chat", (), {"completions": _FakeOpenAIChatCompletions()})()


@pytest.fixture
def mock_openai_generative(monkeypatch):
    """Patch _OpenAIModel.client to return a fake client."""
    fake = _FakeOpenAIChatClient()

    monkeypatch.setattr(
        openai_mod._OpenAIModel,
        "client",
        property(lambda self: fake),
    )
    monkeypatch.setattr(openai_mod, "_openai_retry", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    return fake


def test_openai_udf_text_generation(mock_openai_generative) -> None:
    udf_instance = openai_udf(
        column="body",
        prompt="Summarise this",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello world"])], ["body"])
    result = udf_instance(batch).to_pylist()

    assert len(result) == 1
    assert result[0] == "response to: Summarise this\n\nhello world"


def test_openai_udf_binary_input(mock_openai_generative) -> None:
    udf_instance = openai_udf(
        column="image",
        prompt="Describe this image",
        mime_type="image/jpeg",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays(
        [pa.array([b"\x89PNG fake"], type=pa.binary())], ["image"]
    )
    result = udf_instance(batch).to_pylist()

    assert len(result) == 1
    assert result[0] == "binary response"


def test_openai_udf_missing_mime_type(mock_openai_generative) -> None:
    udf_instance = openai_udf(
        column="image",
        prompt="Describe",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays(
        [pa.array([b"\x89PNG fake"], type=pa.binary())], ["image"]
    )
    with pytest.raises(ValueError, match="mime_type is required"):
        udf_instance(batch)


def test_openai_udf_null_handling(mock_openai_generative) -> None:
    udf_instance = openai_udf(
        column="body",
        prompt="Summarise",
        version="v1",
    )

    batch = pa.RecordBatch.from_arrays([pa.array(["hello", None, "world"])], ["body"])
    result = udf_instance(batch).to_pylist()

    assert len(result) == 3
    assert result[0] is not None
    assert result[1] is None
    assert result[2] is not None


def test_openai_udf_unknown_model_warns(mock_openai_generative) -> None:
    with pytest.warns(UserWarning, match="Unknown OpenAI model"):
        openai_udf(
            column="body",
            prompt="test",
            model="not-a-real-model",
            version="v1",
        )


# ---------------------------------------------------------------------------
# OpenAI client construction (GEN-914)
# ---------------------------------------------------------------------------


def _capture_openai_client_kwargs(monkeypatch) -> dict:
    """Swap in a fake ``openai`` module recording ``OpenAI(...)`` kwargs."""
    captured: dict = {}

    class _RecordingClient:
        def __init__(self, **kwargs) -> None:
            captured.update(kwargs)

    fake = types.ModuleType("openai")
    fake.OpenAI = _RecordingClient
    monkeypatch.setitem(sys.modules, "openai", fake)
    return captured


def test_openai_embedding_client_disables_brotli(monkeypatch) -> None:
    captured = _capture_openai_client_kwargs(monkeypatch)

    model = openai_mod._OpenAIEmbeddingModel(
        model_name="text-embedding-3-small",
        column="body",
        normalize=False,
        api_key="fake-key",
    )
    model._build_model()

    assert "br" not in captured["default_headers"]["Accept-Encoding"]


def test_openai_generative_client_disables_brotli(monkeypatch) -> None:
    captured = _capture_openai_client_kwargs(monkeypatch)

    model = openai_mod._OpenAIModel(api_key="fake-key", prompt="summarize")
    assert model.client is not None

    assert "br" not in captured["default_headers"]["Accept-Encoding"]


class TestEmbeddingModelCallCompatibility:
    """The model call contract is a persistence boundary.

    ``EmbeddingUDF.__call__`` is cloudpickled by value; the model class is
    resolved by reference from the installed module. So a payload and the
    module it runs against can disagree about the contract in either
    direction, and both have to keep working.
    """

    @staticmethod
    def _model(monkeypatch):  # noqa: ANN001, ANN205
        _install_fake_openai_embedding(monkeypatch, echo=True)
        from geneva.udfs.openai import _OpenAIEmbeddingModel

        return _OpenAIEmbeddingModel(
            model_name="text-embedding-3-small",
            column="body",
            normalize=False,
            api_key="k",
            output_dimensionality=_FAKE_OPENAI_DIM,
        )

    def test_old_payload_calling_embed_still_works(self, monkeypatch) -> None:
        """Upgrade: a payload pickled before the Array UDFs calls
        ``embed(batch)`` against today's module."""
        model = self._model(monkeypatch)
        batch = pa.RecordBatch.from_arrays([pa.array(["1", "2"])], ["body"])

        via_batch = model.embed(batch).to_pylist()
        via_array = model.embed_array(pa.array(["1", "2"])).to_pylist()

        assert via_batch == via_array
        assert via_batch == [[1.0] * _FAKE_OPENAI_DIM, [2.0] * _FAKE_OPENAI_DIM]

    def test_embed_rejects_a_batch_without_the_column(self, monkeypatch) -> None:
        model = self._model(monkeypatch)
        batch = pa.RecordBatch.from_arrays([pa.array(["1"])], ["other"])

        with pytest.raises(ValueError, match="not found in RecordBatch"):
            model.embed(batch)

    def test_new_payload_falls_back_on_an_older_module(
        self, mock_openai_embedding_echo
    ) -> None:
        """Rollback: today's wrapper against a module that predates
        ``embed_array`` and only offers ``embed(batch)``."""
        seen: list[pa.RecordBatch] = []

        class _OldModel:
            """A model as the previous release defined it: RecordBatch only."""

            column = "body"

            def embed(self, batch: pa.RecordBatch) -> pa.Array:
                seen.append(batch)
                values = batch.column(batch.schema.get_field_index("body"))
                return pa.array(
                    [[float(v)] * _FAKE_OPENAI_DIM for v in values.to_pylist()],
                    type=pa.list_(pa.float32(), _FAKE_OPENAI_DIM),
                )

        udf_inst = _build_embedding_udf(
            _OldModel(),  # type: ignore[arg-type]
            udf_name="old-embedding",
            num_gpus=0.0,
            dimension=_FAKE_OPENAI_DIM,
        )

        result = udf_inst(pa.array(["3", "4"])).to_pylist()

        # The array was rebuilt into the one-column batch the old contract
        # expects -- one column, not the whole row.
        assert len(seen) == 1
        assert seen[0].schema.names == ["body"]
        assert result == [[3.0] * _FAKE_OPENAI_DIM, [4.0] * _FAKE_OPENAI_DIM]

# ruff: noqa: ANN201, ANN202, PIE804
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import numpy as np
import pyarrow as pa
import pytest

import geneva.udfs.embeddings as embedding_mod
import geneva.udfs.gemini as gemini_mod
import geneva.udfs.openai as openai_mod
from geneva import connect
from geneva.udfs.embeddings import gemini_embedding_udf, sentence_transformer_udf
from geneva.udfs.gemini import gemini_udf
from geneva.udfs.openai import openai_embedding_udf, openai_udf


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
    udf = sentence_transformer_udf("fake-model/2", column="title")
    batch = pa.RecordBatch.from_arrays([pa.array(["hello"])], ["body"])
    with pytest.raises(ValueError, match="Column 'title' not found"):
        udf.func(batch)


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


class _FakeOpenAIEmbedResponse:
    """Mimics the result of ``client.embeddings.create(...)``."""

    def __init__(self, data: list[_FakeOpenAIEmbeddingData]) -> None:
        self.data = data


class _FakeOpenAIEmbeddings:
    """Mimics ``client.embeddings`` on an ``openai.OpenAI``."""

    def create(self, *, input, model, **kwargs):  # noqa: A002
        dim = kwargs.get("dimensions") or _FAKE_OPENAI_DIM
        data = [
            _FakeOpenAIEmbeddingData([float(i + 1)] * dim) for i, _ in enumerate(input)
        ]
        return _FakeOpenAIEmbedResponse(data)


class _FakeOpenAIEmbeddingClient:
    """Minimal stand-in for ``openai.OpenAI`` for embedding UDF."""

    def __init__(self) -> None:
        self.embeddings = _FakeOpenAIEmbeddings()


@pytest.fixture
def mock_openai_embedding(monkeypatch):
    """Patch _OpenAIEmbeddingModel._build_model to return a fake client."""
    fake = _FakeOpenAIEmbeddingClient()

    def _build(self):  # noqa: ANN001, ANN202
        return fake

    monkeypatch.setattr(openai_mod._OpenAIEmbeddingModel, "_build_model", _build)
    monkeypatch.setattr(openai_mod, "_openai_retry", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    return fake


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


def test_openai_embedding_unknown_model_warns(mock_openai_embedding) -> None:
    with pytest.warns(UserWarning, match="Unknown OpenAI embedding model"):
        openai_embedding_udf(
            column="body", model="not-a-real-model", dimension=_FAKE_OPENAI_DIM
        )


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

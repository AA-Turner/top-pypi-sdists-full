"""Test VoyageAI embeddings."""

from langchain_voyageai import VoyageAIEmbeddings

# Please set VOYAGE_API_KEY in the environment variables
MODEL = "voyage-2"


def test_langchain_voyageai_embedding_documents() -> None:
    """Test voyage embeddings."""
    documents = ["foo bar"]
    embedding = VoyageAIEmbeddings(model=MODEL)  # type: ignore[call-arg]
    output = embedding.embed_documents(documents)
    assert len(output) == 1
    assert len(output[0]) == 1024


def test_langchain_voyageai_embedding_documents_multiple() -> None:
    """Test voyage embeddings."""
    documents = ["foo bar", "bar foo", "foo"]
    embedding = VoyageAIEmbeddings(model=MODEL, batch_size=2)
    output = embedding.embed_documents(documents)
    assert len(output) == 3
    assert len(output[0]) == 1024
    assert len(output[1]) == 1024
    assert len(output[2]) == 1024


def test_langchain_voyageai_embedding_query() -> None:
    """Test voyage embeddings."""
    document = "foo bar"
    embedding = VoyageAIEmbeddings(model=MODEL)  # type: ignore[call-arg]
    output = embedding.embed_query(document)
    assert len(output) == 1024


async def test_langchain_voyageai_async_embedding_documents_multiple() -> None:
    """Test voyage embeddings."""
    documents = ["foo bar", "bar foo", "foo"]
    embedding = VoyageAIEmbeddings(model=MODEL, batch_size=2)
    output = await embedding.aembed_documents(documents)
    assert len(output) == 3
    assert len(output[0]) == 1024
    assert len(output[1]) == 1024
    assert len(output[2]) == 1024


async def test_langchain_voyageai_async_embedding_query() -> None:
    """Test voyage embeddings."""
    document = "foo bar"
    embedding = VoyageAIEmbeddings(model=MODEL)  # type: ignore[call-arg]
    output = await embedding.aembed_query(document)
    assert len(output) == 1024


def test_langchain_voyageai_embedding_documents_with_output_dimension() -> None:
    """Test voyage embeddings."""
    documents = ["foo bar"]
    embedding = VoyageAIEmbeddings(model="voyage-3-large", output_dimension=256)  # type: ignore[call-arg]
    output = embedding.embed_documents(documents)
    assert len(output) == 1
    assert len(output[0]) == 256


def test_langchain_voyageai_contextual_embedding_documents() -> None:
    """Test contextual voyage embeddings for documents."""
    documents = ["foo bar", "baz qux"]
    embedding = VoyageAIEmbeddings(model="voyage-context-3")  # type: ignore[call-arg]
    output = embedding.embed_documents(documents)
    assert len(output) == 2
    assert len(output[0]) == 1024  # Default embedding dimension
    assert len(output[1]) == 1024


def test_langchain_voyageai_contextual_embedding_query() -> None:
    """Test contextual voyage embeddings for query."""
    query = "foo bar"
    embedding = VoyageAIEmbeddings(model="voyage-context-3")  # type: ignore[call-arg]
    output = embedding.embed_query(query)
    assert len(output) == 1024


def test_langchain_voyageai_contextual_embedding_with_output_dimension() -> None:
    """Test contextual voyage embeddings with custom output dimension."""
    documents = ["foo bar"]
    embedding = VoyageAIEmbeddings(model="voyage-context-3", output_dimension=512)  # type: ignore[call-arg]
    output = embedding.embed_documents(documents)
    assert len(output) == 1
    assert len(output[0]) == 512


async def test_langchain_voyageai_async_contextual_embedding_documents() -> None:
    """Test async contextual voyage embeddings for documents."""
    documents = ["foo bar", "baz qux", "hello world"]
    embedding = VoyageAIEmbeddings(model="voyage-context-3")  # type: ignore[call-arg]
    output = await embedding.aembed_documents(documents)
    assert len(output) == 3
    assert len(output[0]) == 1024
    assert len(output[1]) == 1024
    assert len(output[2]) == 1024


async def test_langchain_voyageai_async_contextual_embedding_query() -> None:
    """Test async contextual voyage embeddings for query."""
    query = "foo bar"
    embedding = VoyageAIEmbeddings(model="voyage-context-3")  # type: ignore[call-arg]
    output = await embedding.aembed_query(query)
    assert len(output) == 1024


def test_langchain_voyageai_contextual_embedding_realistic_documents() -> None:
    """Test contextual voyage embeddings with realistic document context."""
    documents = [
        "The Mediterranean diet emphasizes fish, olive oil, "
        "and vegetables, believed to reduce chronic diseases.",
        "Photosynthesis in plants converts light energy into "
        "glucose and produces essential oxygen.",
        "Apple's conference call to discuss fourth fiscal quarter "
        "results is scheduled for Thursday, November 2, 2023.",
    ]
    embedding = VoyageAIEmbeddings(model="voyage-context-3")  # type: ignore[call-arg]
    output = embedding.embed_documents(documents)
    assert len(output) == 3
    assert all(len(emb) == 1024 for emb in output)
    # Verify embeddings are different (not all zeros or identical)
    assert output[0] != output[1]
    assert output[1] != output[2]


def test_langchain_voyageai_contextual_embedding_query_with_context() -> None:
    """Test contextual voyage embeddings for query with realistic context."""
    query = "When is Apple's conference call scheduled?"
    embedding = VoyageAIEmbeddings(model="voyage-context-3")  # type: ignore[call-arg]
    output = embedding.embed_query(query)
    assert len(output) == 1024
    # Verify embedding is not all zeros
    assert any(val != 0.0 for val in output)

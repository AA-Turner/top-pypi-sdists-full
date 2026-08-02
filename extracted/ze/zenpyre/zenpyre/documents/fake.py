r"""Contain functions to generate fake documents.

It is designed to be used for testing and debugging purposes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.documents import Document

from zenpyre.utils.imports import check_faker, is_faker_available

if TYPE_CHECKING or is_faker_available():  # pragma: no cover
    import faker

__all__ = ["generate_fake_documents"]


def generate_fake_documents(
    n: int = 5,
    seed: int | None = None,
    nb_sentences: int = 5,
) -> list[Document]:
    """Generate synthetic LangChain Documents with Faker-generated
    content.

    Each document gets a unique ``id`` (``"doc-{i}"``), a Faker-generated
    paragraph as its content, and metadata containing a fake author name
    and a single-word topic.

    Note:
        Content is **not guaranteed to be unique**: ``Faker.paragraph()``
        has no built-in uniqueness constraint, so with a large enough
        ``n`` (or a small enough ``nb_sentences``), two documents could
        coincidentally receive identical text. If strict uniqueness
        matters for your use case, deduplicate the result or use
        Faker's ``unique`` proxy (e.g. ``fake.unique.paragraph(...)``,
        which raises once its internal pool is exhausted).

    Warning:
        ``Faker.seed()`` seeds Faker's shared, process-wide random
        generator, not just the local ``fake`` instance created here.
        Passing ``seed`` therefore affects the reproducibility of *any*
        other ``Faker()`` instance used elsewhere in the same process
        after this function runs, not only calls made through this
        function.

    Args:
        n: Number of documents to generate. Must be non-negative;
            ``n=0`` returns an empty list.
        seed: Optional seed for reproducible output. If ``None``,
            content differs on every call (see the Warning above about
            seeding's process-wide scope).
        nb_sentences: Number of sentences per document's generated
            paragraph, passed through to ``Faker.paragraph()``. Higher
            values reduce (but do not eliminate) the chance of two
            documents coincidentally sharing identical content.

    Returns:
        A list of ``n`` Document objects, each with a distinct ``id``
            and independently generated content and metadata.

    Raises:
        ValueError: If ``n`` is negative.
        RuntimeError: If the optional ``faker`` dependency is not
            installed.

    Example:
        ```pycon
        >>> from zenpyre.documents.fake import generate_fake_documents
        >>> docs = generate_fake_documents(n=3, seed=42)
        >>> len(docs)
        3
        >>> [doc.id for doc in docs]
        ['doc-0', 'doc-1', 'doc-2']
        >>> docs2 = generate_fake_documents(n=3, seed=42)
        >>> [doc.page_content for doc in docs] == [doc.page_content for doc in docs2]
        True

        ```
    """
    check_faker()

    if n < 0:
        msg = f"'n' must be non-negative, got {n}."
        raise ValueError(msg)

    if seed is not None:
        faker.Faker.seed(seed)
    fake = faker.Faker()

    return [
        Document(
            id=f"doc-{i}",
            page_content=fake.paragraph(nb_sentences=nb_sentences),
            metadata={"author": fake.name(), "topic": fake.word()},
        )
        for i in range(n)
    ]

"""The data catalog's closed vocabularies, client copy (plan data-catalog, finding 8).

Mirrors the server's catalog enums (``app/core``): the roles a run's use of a
dataset, source or checkpoint carries (C2), the kinds and providers of an
external source (C1), and how strong a dataset version's identity is (C3).
Closed lists, the artifact-kinds lesson: free text grew to 104 words.

Dependency-free (``probe._compat`` only, for Python 3.10's StrEnum) so the SDK,
the CLI and a server-side test can all import it. THE SERVER VALIDATES: a word
this copy does not know is refused there (422), never folded here.
"""

from __future__ import annotations

from probe._compat import StrEnum


class Role(StrEnum):
    """What a run used a dataset, source or checkpoint FOR (`meta.roles` on a
    `consumes` edge). `init` is the weights a run started from: a Hub base model
    or another run's checkpoint (R15; never `base_model`, Q11)."""

    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"
    EVAL = "eval"
    INIT = "init"
    TOKENIZER = "tokenizer"
    OTHER = "other"


class SourceKind(StrEnum):
    """`external_sources.kind`."""

    DATASET = "dataset"
    MODEL = "model"
    OTHER = "other"


class Provider(StrEnum):
    """`external_sources.provider`, worked out by the server from the uri."""

    HUGGINGFACE = "huggingface"
    S3 = "s3"
    GCS = "gcs"
    AZURE = "azure"
    HTTP = "http"
    GIT = "git"
    DATABASE = "database"
    LOCAL = "local"
    OTHER = "other"


class Identity(StrEnum):
    """How strong a dataset version's `content_hash` is (`meta.identity`).

    `bytes`: every file fully hashed. `partial`: some file was fingerprinted
    (over 1 GiB, past the I/O budget) or left out. `pointer`: a remote uri Probe
    never reads, identified by ``sha256("uri\\nrevision")``."""

    BYTES = "bytes"
    PARTIAL = "partial"
    POINTER = "pointer"


class HashMode(StrEnum):
    """`log_dataset(hash=...)`: hash within the run's I/O budget (R8), or every byte."""

    BUDGET = "budget"
    FULL = "full"


class Registered(StrEnum):
    """`GET /v1/catalog/datasets?registered=`."""

    ALL = "all"
    YES = "yes"
    NO = "no"


class Stored(StrEnum):
    """A checkpoint's `stored` (`GET /v1/catalog/checkpoints?stored=`): Probe
    holds the bytes, or the row points at where the run left them."""

    STORED = "stored"
    REFERENCE = "reference"


class Direction(StrEnum):
    """`GET /v1/provenance?direction=`."""

    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"

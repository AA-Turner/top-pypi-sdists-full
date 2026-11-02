"""pyiceberg's ``FsspecFileIO`` with an S3 filesystem of its own.

pyiceberg's ``_s3`` builds an ``S3FileSystem`` through fsspec's instance cache,
which hands every table and every thread the same instance, since the signer
is not part of the cache key. It then unregisters and re-registers its signer
on that shared client. Two effects follow:

* Loading a second table re-points the shared client at that table's signer
  endpoint, so the first table's requests fail with ``403``.
* pyiceberg caches the filesystem per thread, so a worker thread re-runs the
  unregister/register while another thread's request is in flight. That
  request goes out without an ``Authorization`` header and fails with ``403``.

``SigningFileIO`` builds a private ``S3FileSystem`` with the signer registered
before anything can use it, and never touches the shared one.

Lakekeeper's ``loadTable`` response sets ``py-io-impl`` to pyiceberg's
``FsspecFileIO`` for every table, and pyiceberg lets that override the catalog
properties, so ``LakekeeperCatalog`` swaps it for ``SigningFileIO``.
"""

from __future__ import annotations

from typing import Any

from pyiceberg.catalog.rest import RestCatalog
from pyiceberg.io import PY_IO_IMPL, S3_SIGNER, FileIO
from pyiceberg.io.fsspec import SIGNERS, FsspecFileIO, _s3
from pyiceberg.typedef import EMPTY_DICT, Properties

STOCK_FILE_IO = "pyiceberg.io.fsspec.FsspecFileIO"
SIGNING_FILE_IO = "databaas_utils.catalog_io.SigningFileIO"

_S3_SCHEMES = ("s3", "s3a", "s3n")
# pyiceberg's id for its handler; reused so the two never both register.
_SIGNER_ID = 1925


def private_s3(properties: Properties) -> Any:
    """An uncached ``S3FileSystem`` configured like pyiceberg's, signer attached.

    Raises:
        ValueError: If ``s3.signer`` names a signer pyiceberg does not know.
    """
    from botocore import UNSIGNED
    from s3fs import S3FileSystem

    # pyiceberg maps the remaining properties to s3fs options; without the
    # signer it registers nothing and does not connect.
    unsigned = {k: v for k, v in properties.items() if k != S3_SIGNER}
    options = dict(_s3(unsigned).storage_options)
    signer_name = properties.get(S3_SIGNER)
    if not signer_name:
        return S3FileSystem(**options, skip_instance_cache=True)
    signer_cls = SIGNERS.get(signer_name)
    if signer_cls is None:
        raise ValueError(f"Signer not available: {signer_name}")
    options["config_kwargs"] = {
        **options.get("config_kwargs", {}),
        "signature_version": UNSIGNED,
    }
    fs = S3FileSystem(**options, skip_instance_cache=True)
    fs.s3.meta.events.register_last(
        "before-sign.s3", signer_cls(properties), unique_id=_SIGNER_ID
    )
    return fs


class SigningFileIO(FsspecFileIO):
    """``FsspecFileIO`` whose S3 filesystems are never shared.

    pyiceberg still caches one filesystem per thread; each is private to this
    FileIO and has its signer from the start.
    """

    def __init__(self, properties: Properties) -> None:
        """Route the S3 schemes to :func:`private_s3`."""
        super().__init__(properties)
        for scheme in _S3_SCHEMES:
            self._scheme_to_fs[scheme] = private_s3


class LakekeeperCatalog(RestCatalog):
    """``RestCatalog`` that gives every table a :class:`SigningFileIO`."""

    def _load_file_io(
        self, properties: Properties = EMPTY_DICT, location: str | None = None
    ) -> FileIO:
        if properties.get(PY_IO_IMPL) == STOCK_FILE_IO:
            properties = {**properties, PY_IO_IMPL: SIGNING_FILE_IO}
        return super()._load_file_io(properties, location)

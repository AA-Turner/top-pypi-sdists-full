"""tentaclio is a library that tries to unify how to load, store data.

The main use cases in mind are ETL processes and notebooks, but can be used in many other contexts.
The main benefits are:
    * url based resource management.
    * same function to open readers and writers for resources of different natures.
    Just change the url, the code remains the same.
    * The same for dbs, create clients with ease and use them regardless
    the underlying implementation (thanks to sqlalchemy).
    * Credentials management that allows a distributed credentials storage.
"""

from tentaclio import *  # noqa
from tentaclio.fs.remover import ClientRemover
from tentaclio.fs.scanners import ClientDirScanner
from tentaclio.streams.stream_client_handler import StreamURLHandler

from .clients.s3_client import *  # noqa


# s3 buckets
STREAM_HANDLER_REGISTRY.register("s3", StreamURLHandler(S3Client))  # type: ignore
SCANNER_REGISTRY.register("s3", ClientDirScanner(S3Client))  # type: ignore
COPIER_REGISTRY.register("s3+s3", S3Client("s3://"))  # type: ignore
REMOVER_REGISTRY.register("s3", ClientRemover(S3Client))  # type: ignore

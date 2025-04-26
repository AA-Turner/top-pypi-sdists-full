import urllib
from abc import ABC
from abc import abstractmethod
from typing import Optional
from urllib.parse import ParseResult

import attrs


class PrefixedUriResolver(ABC):
    @abstractmethod
    def uri(self, key: str) -> ParseResult:
        pass


@attrs.frozen
class PrefixedS3ResolverImpl(PrefixedUriResolver):
    bucket: Optional[str]

    def uri(self, key: str) -> ParseResult:
        if not self.bucket:
            msg = "Need to specify an S3 bucket to write "
            raise Exception(msg)
        return urllib.parse.urlparse(f"s3://{self.bucket}/{key}")


@attrs.frozen
class PrefixedLocalFileResolverImpl(PrefixedUriResolver):
    base_dir: str

    def uri(self, key: str) -> ParseResult:
        return urllib.parse.urlparse(f"file://{self.base_dir}/{key}")

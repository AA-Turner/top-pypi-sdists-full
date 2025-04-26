from collections import namedtuple
from urllib.parse import urlparse

from tinybird_cdk import errors

from . import gcs, s3

# Public interface for cloud service names. Please, do not hardcode or rely on
# the values stored in these constants outside of this file.
S3 = 'S3'
GCS = 'GCS'

ParsedURL = namedtuple("ParsedURL", "service bucket key")

# Parses URLs of cloud file storage services and returns a named tuple with
# three attributes:
#
#   * `service` an opaque value that represents the cloud service. Their public
#     interface outside of this file are the constants defined above.
#   * `bucket` is a string with the bucket name.
#   * `key` is either a non-empty string or `None`. Non-empty strings have no
#     leading or trailing slashes even if they had them in the original URL.
#
# If the service is unknown, `errors.UnsupportedCloudServiceSchemeError` is raised.
def parse_url(url):
    parsed = urlparse(url)
    service = _service_for(parsed.scheme)
    bucket = parsed.netloc
    key = parsed.path.strip('/') or None
    return ParsedURL(service, bucket, key)

def client_for(service):
    if service == 'S3':
        return s3.Client()
    if service == 'GCS':
        return gcs.Client()
    raise errors.UnsupportedCloudServiceError(service)

def _service_for(scheme):
    if scheme == 's3':
        return S3
    if scheme in ('gs', 'gcs'):
        return GCS
    raise errors.UnsupportedCloudServiceSchemeError(scheme)

import datetime

import google.api_core.exceptions as storage_exceptions
import humanize
from google.cloud import storage

from tinybird_cdk import logger, utils

from . import abstract_client, gcp


class Client(abstract_client.Client):
    '''Concrete class for the GCS cloud storage service.'''

    # We don't generally support passing clients from calling code. However, in
    # this case the trade-off seems worthwhile because the one used in the core
    # test suite needs anonymous credentials and a custom endpoint. There is no
    # point in supporting that down here if real usage does not need it.
    def __init__(self, client=None):
        self.gcs = client or storage.Client(credentials=gcp.credentials(), project=gcp.project_id())

    # https://cloud.google.com/storage/docs/gsutil#syntax.
    def uri(self, bucket, key=None):
        uri = f'gs://{bucket}'
        if key:
            uri += f'/{key}'
        return uri

    # https://googleapis.dev/python/storage/latest/client.html#google.cloud.storage.client.Client.list_blobs
    def ls(self, bucket, directory=None):
        kwargs = {}
        if directory:
            kwargs['prefix'] = f'{directory}/'
        blobs = self.gcs.list_blobs(bucket, **kwargs)
        keys = [blob.name for blob in blobs]
        keys.sort()
        return keys

    # https://googleapis.dev/python/storage/latest/blobs.html#google.cloud.storage.blob.Blob.generate_signed_url
    def public_url(self, bucket, key, expires_in_s=abstract_client.DEFAULT_TTL_FOR_PUBLIC_URLS_S):
        bucket = self.gcs.bucket(bucket)
        blob = bucket.get_blob(key)
        expiration = datetime.datetime.now() + datetime.timedelta(seconds=expires_in_s)
        return blob.generate_signed_url(expiration=expiration)

    # https://googleapis.dev/python/storage/latest/buckets.html#google.cloud.storage.bucket.Bucket.delete_blob
    def rm(self, bucket, key):
        logger.info(f'Deleting {self.uri(bucket, key)}')
        bucket = self.gcs.bucket(bucket)
        try:
            return bucket.delete_blob(key)
        except storage_exceptions.NotFound:
            return None

    # https://googleapis.dev/python/storage/latest/buckets.html#google.cloud.storage.bucket.Bucket.delete_blobs
    def rmtree(self, bucket, directory=None):
        if blobs := self.ls(bucket, directory):
            logger.info(f'Deleting all blobs under {self.uri(bucket, directory)}/')
            bucket = self.gcs.bucket(bucket)
            bucket.delete_blobs(blobs)

    # https://cloud.google.com/storage/docs/composite-objects
    # https://googleapis.dev/python/storage/latest/blobs.html#google.cloud.storage.blob.Blob.compose
    def cat(self, bucket, directory):
        bucket = self.gcs.bucket(bucket)
        keys = self.ls(bucket, directory)

        if not keys:
            return None

        if len(keys) == 1:
            blob = bucket.get_blob(keys[0])
            self._log_blob(blob)
            return keys[0]

        # A composite object can concatenate at most 32 source objects. These
        # can in turn be composites, including itself, so we only need one key
        # for the final blob.
        #
        # We iterate in chunks of at most 32 - 1, to leave one spot for the
        # current composite from the 2nd iteration on. We do not need this spot
        # in the first iteration, but KISS.
        composite_key = self.cat_key(directory)
        logger.info(f'Concatenating {len(keys)} GCS blobs into {composite_key}')

        composite = bucket.blob(composite_key)
        composite.content_type = bucket.get_blob(keys[0]).content_type

        for i, keys in enumerate(utils.chunks(keys, 32 - 1)):
            blobs = []
            for key in keys:
                blob = bucket.get_blob(key)
                self._log_blob(blob)
                blobs.append(blob)

            if i:
                blobs = [composite] + blobs
            composite.compose(blobs)

        self._log_blob(composite)

        return composite_key

    def _log_blob(self, blob):
        uri = self.uri(blob.bucket.name, blob.name)
        logger.debug(f'{uri} ({humanize.naturalsize(blob.size)})')

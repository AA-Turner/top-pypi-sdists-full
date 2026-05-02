import re
from spotml.deployment.abstract_cloud_instance.abstract_bucket_manager import AbstractBucketManager
from spotml.deployment.abstract_cloud_instance.errors.bucket_not_found import BucketNotFoundError
from spotml.providers.gcp.helpers.gs_client import GSClient
from spotml.providers.gcp.resources.bucket import Bucket
from spotml.utils import random_string


class BucketManager(AbstractBucketManager):

    def __init__(self, project_name: str, region: str):
        super().__init__(project_name)

        self._gs = GSClient()
        self._region = region
        self._bucket_prefix = 'spotml-%s' % project_name.lower()

    def get_bucket(self) -> Bucket:
        buckets = self._gs.list_buckets()

        regex = re.compile('-'.join([self._bucket_prefix, '[a-z0-9]{12}', self._region]))
        buckets = [bucket for bucket in buckets if regex.match(bucket.name) is not None]

        if len(buckets) > 1:
            raise ValueError('Found several project buckets in the same region: %s.'
                             % ', '.join(bucket.name for bucket in buckets))

        if not len(buckets):
            raise BucketNotFoundError

        bucket = Bucket(buckets[0])

        return bucket

    def create_bucket(self) -> Bucket:
        bucket_name = '-'.join([self._bucket_prefix, random_string(12), self._region])
        bucket = self._gs.create_bucket(bucket_name, self._region)

        return Bucket(bucket)

from nexuscli.api import util, validations
from nexuscli.api.base_model import BaseModel


class Blobstore(BaseModel):
    """
    Blob store object.

    Configuration example for type: File

    .. code:: python

       {
         "softQuota": {
           "type": "spaceUsedQuota",
           "limit": 100
         },
         "name": "test",
         "type": "File",
         "path": "/tmp/test"
       }

    Configuration example for type: S3

    .. code:: python

       {
         "name": "something-s3",
         "type": "S3",
         "bucketConfiguration": {
           "bucket": {
             "region": "us-east-1",
             "name": "mynexusbucket",
             "prefix": "path-prefix",
             "expiration": 3
           },
           "encryption": {
             "encryptionType": "s3ManagedEncryption",
             "encryptionKey": ""
           },
           "bucketSecurity": {
             "accessKeyId": "AKIASLMFS2HSCEW2MZCC",
             "role": "",
             "sessionToken": ""
           }
         }
       }
    """
    TYPES = ['S3', 'File']
    QUOTA_TYPES = ['spaceRemainingQuota', 'spaceUsedQuota']
    ENCRYPTION_TYPES = ['s3ManagedEncryption', 'kmsManagedEncryption']

    def _validate_type(self) -> None:
        if not isinstance(self._raw.get('type'), str):
            raise ValueError('type must be a str')
        self._raw['type'] = self._raw['type'].title()
        validations.ensure_known('type', self._raw['type'], self.TYPES)

    def _validate_type_file(self) -> None:
        if self.type == 'File':
            if not isinstance(self._raw.get('path'), str) or not self._raw.get('path'):
                raise ValueError('path must be a non-empty str for blobstores of type `file`')

    def _validate_quota(self) -> None:
        if self._raw.get('softQuota') is None:
            self._raw['softQuota'] = None
        else:
            if not isinstance(self.soft_quota, dict):
                raise ValueError('softQuota must be a dict')
            if not isinstance(self.soft_quota['limit'], int):
                raise ValueError('softQuota.limit must be an integer')
            validations.ensure_known('softQuota.type', self.soft_quota['type'], self.QUOTA_TYPES)

    def _validate_params(self) -> None:
        super()._validate_params()
        self._validate_type()
        self._validate_type_file()
        self._validate_quota()

    @property
    def type(self) -> str:
        return self._raw['type']

    @property
    def soft_quota(self):
        return self._raw['softQuota']

    @util.with_min_version('3.19.0')
    def update(self, params: dict) -> None:
        self.configuration.update(params)
        resp = self._client.put(
            f'blobstores/{self.type.lower()}/{self.name}', json=self.configuration)
        util.validate_response(resp, 204)

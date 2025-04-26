import boto3
import humanize

from tinybird_cdk import config, logger

from . import abstract_client


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
class Client(abstract_client.Client):
    '''Concrete class for the S3 cloud storage service.'''

    # Assumes standard AWS_* variables are set.
    #
    # AWS_ENDPOINT_URL is used for testing against LocalStack, but it is not
    # understood by boto3, so we need to pass it by hand. This PR
    #
    #     https://github.com/boto/boto3/pull/2746
    #
    # adding support for it is open at the time of this writing.
    def __init__(self):
        kwargs = {'service_name': 's3'}
        if endpoint_url := config.get('AWS_ENDPOINT_URL', optional=True):
            kwargs['endpoint_url'] = endpoint_url
        self.s3 = boto3.session.Session().resource(**kwargs)
        self.client = self.s3.meta.client

    # In theory, the URI starts with "S3" according to the documentation:
    #
    #     https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html
    #
    # but the AWS CLI rejects it, and official examples use "s3".
    def uri(self, bucket, key=None):
        uri = f's3://{bucket}'
        if key:
            uri += f'/{key}'
        return uri

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.objects
    def ls(self, bucket, directory=None):
        bucket = self.s3.Bucket(bucket)
        if directory:
            objects = bucket.objects.filter(Prefix=f'{directory}/')
        else:
            objects = bucket.objects.all()
        keys = [object.key for object in objects]
        keys.sort()
        return keys

    # The resource-oriented API does not have a way to do this, see
    #
    #     https://github.com/boto/boto3/issues/2998
    #
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url
    def public_url(self, bucket, key, expires_in_s=abstract_client.DEFAULT_TTL_FOR_PUBLIC_URLS_S):
        params = {'Bucket': bucket, 'Key': key}
        return self.client.generate_presigned_url('get_object', Params=params, ExpiresIn=expires_in_s)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.delete
    def rm(self, bucket, key):
        logger.info(f'Deleting {self.uri(bucket, key)}')
        self.s3.Object(bucket, key).delete()

    def rmtree(self, bucket, directory=None):
        if keys := self.ls(bucket, directory):
            logger.info(f'Deleting all objects under {self.uri(bucket, directory)}/')
            for key in keys:
                self.rm(bucket, key)

    # S3 does not have the equivalent of GCS composite objects, you emulate that
    # functionality with mutipart uploads. Please note they require all parts to
    # be at least 5MB, except perhaps for the last one. Therefore, this is not a
    # generic object concatenation.
    #
    # The resource-oriented API does not work for multipart uploads due to
    #
    #     https://github.com/boto/boto3/issues/1660
    #
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_multipart_upload
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_part_copy
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.complete_multipart_upload
    def cat(self, bucket, directory):
        keys = self.ls(bucket, directory)

        if not keys:
            return None

        if len(keys) == 1:
            self._log_object(bucket, keys[0])
            return keys[0]

        upload_key = self.cat_key(directory)
        logger.info(f'Concatenating {len(keys)} S3 objects into {upload_key}')

        upload_content_type = self.s3.Object(bucket, keys[0]).content_type
        upload_id = self.client.create_multipart_upload(Bucket=bucket, Key=upload_key, ContentType=upload_content_type)['UploadId']

        parts = []
        for part_number, key in enumerate(keys, start=1):
            self._log_object(bucket, key)
            response = self.client.upload_part_copy(
                UploadId=upload_id,
                Bucket=bucket,
                Key=upload_key,
                CopySource=f'{bucket}/{key}',
                PartNumber=part_number)
            parts.append({'ETag': response['CopyPartResult']['ETag'], 'PartNumber': part_number})

        self.client.complete_multipart_upload(
            UploadId=upload_id,
            Bucket=bucket,
            Key=upload_key,
            MultipartUpload={'Parts': parts})

        self._log_object(bucket, upload_key)

        return upload_key

    def _log_object(self, bucket, key):
        uri = self.uri(bucket, key)
        size = self.s3.ObjectSummary(bucket, key).size
        logger.debug(f'{uri} ({humanize.naturalsize(size)})')

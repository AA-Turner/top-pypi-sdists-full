from configurations import values


class Media:
    MEDIA_URL = "/media/"


class LocalMedia(Media):
    @property
    def MEDIA_ROOT(self):  # noqa
        return self.BASE_DIR.joinpath("mediafiles")


class S3Media(Media):
    AWS_ACCESS_KEY_ID = values.Value("minio_access_key", environ_prefix=None)
    AWS_SECRET_ACCESS_KEY = values.Value("minio_secret_access_key", environ_prefix=None)

    AWS_S3_REGION_NAME = values.Value("", environ_prefix=None)
    AWS_S3_ENDPOINT_URL = values.Value("http://localhost:9000", environ_prefix=None)
    AWS_S3_SIGNATURE_VERSION = values.Value("s3v4", environ_prefix=None)
    AWS_DEFAULT_ACL = values.Value(None, environ_prefix=None)
    AWS_S3_FILE_OVERWRITE = values.BooleanValue(False, environ_prefix=None)

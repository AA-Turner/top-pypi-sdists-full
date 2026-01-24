class Staticfiles:
    STATIC_URL = "static/"


class LocalStaticfiles(Staticfiles):
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    @property
    def STATIC_ROOT(self):  # noqa
        return self.BASE_DIR.joinpath("staticfiles")


class S3Staticfiles(Staticfiles):
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
    }

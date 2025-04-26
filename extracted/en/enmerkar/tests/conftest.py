from django.conf import settings

from testproject import settings as testproject_settings


def pytest_configure():
    filtered_settings = {k: v for (k, v) in vars(testproject_settings).items()
                         if k.isupper()}
    settings.configure(**filtered_settings)

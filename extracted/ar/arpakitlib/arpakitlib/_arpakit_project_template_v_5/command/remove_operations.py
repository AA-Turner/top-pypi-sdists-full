from project.business_service.remove_operations import remove_operations
from project.core.settings import get_cached_settings
from project.core.util import setup_logging


def __command():
    setup_logging()
    get_cached_settings().raise_if_mode_prod()
    remove_operations()


if __name__ == '__main__':
    __command()

from click.exceptions import ClickException


class UnionRequireConfigException(ClickException):
    """Union remote is not properly configuration"""

"""The public interface or entry point for the Format 2 workflow code."""

__version__ = '0.0.2'

PROJECT_NAME = "markdown-it-reporter"
PROJECT_OWNER = PROJECT_USERAME = "galaxyproject"
PROJECT_AUTHOR = 'Galaxy Project and Community'
PROJECT_EMAIL = 'jmchilton@gmail.com'
PROJECT_URL = "https://github.com/galaxyproject/markdown-it-reporter"


from ._impl import html_report


__all__ = (
    'html_report',
)

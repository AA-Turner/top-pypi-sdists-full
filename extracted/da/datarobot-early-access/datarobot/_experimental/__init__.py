# flake8: noqa
# because the unused imports are on purpose

import logging

from .models.idiomatic_project import IdiomaticProject

logger = logging.getLogger(__package__)

experimental_warning = (
    "You have imported from the _experimental directory.\n"
    "This directory is used for unreleased datarobot features.\n"
    "Unless you specifically know better,"
    " you don't have the access to use this functionality in the app, so this code will not work."
)

logger.warning(experimental_warning)

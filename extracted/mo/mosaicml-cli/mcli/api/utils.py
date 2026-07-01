"""
Utils for all api folders
"""

import logging
import os
import ssl
import sys

from mcli.utils.utils_logging import WARN, FormatString, format_string

logger = logging.getLogger(__name__)


def check_python_certificates():
    # Only support macOS checks for now
    if sys.platform != 'darwin':
        return

    certificates_exist = os.path.exists(ssl.get_default_verify_paths().openssl_cafile)
    if not certificates_exist:
        command = 'bash /Applications/Python*/Install\\ Certificates.command'
        command = format_string(command, FormatString.BLUE)
        message = ('Python SSL Certificates are not installed. '
                   'These are required to make HTTPs requests against MosaicML services.')
        message = format_string(message, FormatString.RED)
        logger.error(f'{message}\n\n{WARN}Please run the '
                     f'following command to install them: \n{command}\n')

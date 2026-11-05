# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import io
import json
import textwrap
import time
import uuid
import zipfile
from typing import Optional

# The alphabet the UI uses for template ids: no 0/1/O/I/l lookalikes.
_UUID_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def _int_to_string(number: int, alphabet: str, padding: Optional[int] = None) -> str:
    """Write ``number`` in base ``len(alphabet)``, most significant digit first.

    Zero is the empty string. With ``padding``, the result is left-padded with
    ``alphabet[0]`` to at least that many characters.
    """
    digits = []
    while number:
        number, digit = divmod(number, len(alphabet))
        digits.append(alphabet[digit])
    if padding:
        digits.extend(alphabet[0] * max(padding - len(digits), 0))
    return "".join(reversed(digits))


def _short_uuid(length: int) -> str:
    """Return a random id of at least ``length`` characters from _UUID_ALPHABET."""
    return _int_to_string(uuid.uuid4().int, _UUID_ALPHABET, length)


def create_panel_zip(name: str, code: str, description: str = "") -> bytes:
    """Package Python code as a panel zip, in the format the UI exports.

    The code is dedented first, so a triple-quoted block indented to match the
    surrounding source is stored as valid top-level Python.

    Args:
        name: The panel's display name.
        code: The panel's Python source.
        description: The description shown in the Panel library.

    Returns:
        The zip file's contents, ready for ``write/template/upload``.
    """
    template = {
        "templateName": name,
        "code": {
            "code": "",
            "css": "",
            "description": description,
            "html": "",
            "defaultConfig": "",
            "internalResources": [],
            "userResources": [],
            "pyCode": textwrap.dedent(code).strip("\n"),
            "type": "py",
            "pyConfig": "{}",
        },
        "createdAt": int(time.time() * 1000),
        "thumbnailName": "template-thumbnail-%s" % _short_uuid(25),
        "editable": True,
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip_fp:
        zip_fp.writestr("tempVisualizationTemplate.json", json.dumps(template))
    return buffer.getvalue()

#
# Copyright 2019 Stephan Müller
#
# Licensed under the GPLv3 license

"""Gitlab codequality reporter"""
from __future__ import absolute_import, print_function

import hashlib
import html
import json
import os
import pathlib
from collections import OrderedDict
from itertools import groupby

from jinja2 import FileSystemLoader, Environment
from pylint.reporters import BaseReporter


class GitlabPagesHtmlReporter(BaseReporter):
    """Report messages in HTML document with links to GitLab source code."""

    name = "gitlab-pages-html"
    extension = "html"

    CI_PROJECT_URL = os.getenv("CI_PROJECT_URL", "")
    CI_COMMIT_REF_NAME = os.getenv("CI_COMMIT_REF_NAME", "")

    _MSG_TYPES = {
        "info": "table-primary",
        "convention": "table-primary",
        "refactor": "table-primary",
        "warning": "table-warning",
        "error": "table-error",
        "fatal": "table-error",
    }

    _COLUMN_NAMES = OrderedDict(
        {
            "line": "Line",
            "column": "Column",
            "type": "Type",
            "obj": "Object",
            "message": "Message",
            "symbol": "Symbol",
            "message_id": "Message Id",
        }
    )

    def __init__(self, output=None):
        BaseReporter.__init__(self, output)
        self.messages = []

    def handle_message(self, msg):
        """Manage message of different type and in the context of path."""
        self.messages.append(msg)

    def display_messages(self, layout):
        """Launch layouts display."""

        ordered_messages = OrderedDict()

        sorted_messages = sorted(self.messages, key=lambda msg: msg.module)
        for module, messages in groupby(sorted_messages, lambda msg: msg.module):
            ordered_messages.update({module: []})
            for message in list(messages):
                ordered_messages[module].append(
                    {
                        "class": self._MSG_TYPES[message.category],
                        "url": (
                            f"{self.CI_PROJECT_URL}/blob/{self.CI_COMMIT_REF_NAME}/{message.path}#L{str(message.line)}"
                        ),
                        "path": pathlib.Path(message.path).as_posix(),
                        "row": OrderedDict(
                            {
                                "line": message.line,
                                "column": message.column,
                                "type": message.category,
                                "obj": message.obj,
                                "message": message.msg.replace("\n", "<br />"),
                                "symbol": message.symbol,
                                "message_id": message.msg_id,
                            }
                        ),
                    }
                )

        template = Environment(
            loader=FileSystemLoader(searchpath=os.path.dirname(os.path.abspath(__file__)))
        ).get_template("templates/report.html.j2")

        print(template.render(data=ordered_messages, column_names=self._COLUMN_NAMES), file=self.out)

    def display_reports(self, layout):
        """Do nothing."""

    def _display(self, layout):
        """Do nothing."""


class GitlabCodeClimateReporter(BaseReporter):
    """Report messages and layouts in Gitlab Code Climate format. Read more on
    https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html."""

    name = "gitlab-codeclimate"
    extension = "json"

    _MSG_SEVERITIES = {
        "info": "info",
        "convention": "minor",
        "refactor": "major",
        "warning": "major",
        "error": "critical",
        "fatal": "blocker",
    }

    _MSG_CATEGORIES = {
        "info": "Compatibility",
        "convention": "Style",
        "refactor": "Clarity",
        "warning": "Bug Risk",
        "error": "Bug Risk",
        "fatal": "Bug Risk",
    }

    def __init__(self, output=None, hash_fingerprint=True):
        BaseReporter.__init__(self, output)
        self.hash_fingerprint = hash_fingerprint
        self.messages = []
        self.hashes = set()

    def handle_message(self, msg):
        """Manage message of different type and in the context of path."""

        if self.hash_fingerprint:
            message_hash = ":".join([msg.path, msg.msg_id])
            sha256_hash = hashlib.sha256(message_hash.encode())
            while sha256_hash.hexdigest() in self.hashes:
                # In cases of hash collisions, new hashes will be generated.
                sha256_hash.update(sha256_hash.hexdigest().encode())

            fingerprint = sha256_hash.hexdigest()
            self.hashes.add(fingerprint)

        else:
            fingerprint = ":".join([msg.path, str(msg.line), msg.msg_id])

        self.messages.append(
            {
                "type": "issue",
                "check_name": msg.msg_id,
                "description": html.escape(msg.msg_id + ": " + msg.msg or "", quote=False),
                "categories": [self._MSG_CATEGORIES[msg.category]],
                "severity": self._MSG_SEVERITIES[msg.category],
                "location": {
                    "path": pathlib.Path(msg.path).as_posix(),
                    "lines": {
                        "begin": msg.line,
                    },
                },
                "fingerprint": fingerprint,
            }
        )

    def display_messages(self, layout):
        """Launch layouts display."""
        print(json.dumps(self.messages, indent=4), file=self.out)

    def display_reports(self, layout):
        """Do nothing."""

    def _display(self, layout):
        """Do nothing."""


class GitlabCodeClimateReporterNoHash(GitlabCodeClimateReporter):
    """Same as GitlabCodeClimateReporter but does not hash fingerprint. Supports nbqa."""

    name = "gitlab-codeclimate-nohash"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, hash_fingerprint=False, **kwargs)

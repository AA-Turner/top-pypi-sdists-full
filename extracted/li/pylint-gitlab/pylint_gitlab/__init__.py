#
# Copyright 2019 Stephan Müller
#
# Licensed under the GPLv3 license

"""Module ``pylint_gitlab``."""

from pylint_gitlab.reporter import GitlabCodeClimateReporter, GitlabCodeClimateReporterNoHash, GitlabPagesHtmlReporter


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(GitlabCodeClimateReporter)
    linter.register_reporter(GitlabCodeClimateReporterNoHash)
    linter.register_reporter(GitlabPagesHtmlReporter)

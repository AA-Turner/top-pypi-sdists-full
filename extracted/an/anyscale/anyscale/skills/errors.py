from typing import List

from anyscale.skills.models import Platform, TermsStatus


SKILLS_TERMS_DOC_URL = "https://docs.anyscale.com/agent-skills-terms"


class SkillsError(Exception):
    """Base class for all skills SDK errors."""


class TermsNotAcceptedError(SkillsError):
    """Raised when skills terms have not been accepted for the target version."""

    def __init__(self, terms: TermsStatus):
        self.terms = terms
        super().__init__(f"Skills terms have not been accepted for v{terms.version}.")


class PlatformVersionMismatchError(SkillsError):
    """Raised when an install would leave platforms on different versions."""

    def __init__(
        self,
        existing_version: str,
        resolved_version: str,
        already_installed: List[Platform],
        new_platforms: List[Platform],
        all_platforms: List[Platform],
    ):
        self.existing_version = existing_version
        self.resolved_version = resolved_version
        self.already_installed = already_installed
        self.new_platforms = new_platforms
        self.all_platforms = all_platforms
        super().__init__(
            f"Installing would leave platforms on mixed versions "
            f"(existing v{existing_version}, requested v{resolved_version})."
        )


class AlreadyInstalledError(SkillsError):
    """Raised when skills are already installed at a different version.

    Re-run with force=True to reinstall at the resolved version.
    """

    def __init__(
        self,
        existing_version: str,
        resolved_version: str,
        already_installed: List[Platform],
    ):
        self.existing_version = existing_version
        self.resolved_version = resolved_version
        self.already_installed = already_installed
        super().__init__(
            f"Skills v{existing_version} already installed; "
            f"use force=True to reinstall at v{resolved_version}."
        )

from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.skills._private.skills_sdk import PrivateSkillsSDK
from anyscale.skills.models import Platform, SkillsListResult, TermsStatus


_SKILLS_SDK_SINGLETON_KEY = "skills_sdk"

_LIST_EXAMPLE = """
import anyscale

info = anyscale.skills.list()
print(f"Available: v{info.available_version}")
"""

_LIST_ARG_DOCSTRINGS = {
    "version": "List skills for a specific version instead of latest.",
}


@sdk_command(
    _SKILLS_SDK_SINGLETON_KEY,
    PrivateSkillsSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001
    version: Optional[str] = None, *, _private_sdk: Optional[PrivateSkillsSDK] = None,
) -> SkillsListResult:
    """List installed skills and available updates."""
    return _private_sdk.list(version=version)  # type: ignore


_INSTALL_EXAMPLE = """
import anyscale
from anyscale.skills.models import Platform

anyscale.skills.install(platforms=[Platform.CLAUDE_CODE], accept_terms=True)
"""

_INSTALL_ARG_DOCSTRINGS = {
    "platforms": "Target platforms (e.g. [Platform.CLAUDE_CODE, Platform.CURSOR]).",
    "version": "Specific version to install.",
    "accept_terms": "Accept terms non-interactively.",
    "force": "Force reinstall even if already installed.",
    "from_file": "Install from a local bundle tarball instead of downloading.",
}


@sdk_command(
    _SKILLS_SDK_SINGLETON_KEY,
    PrivateSkillsSDK,
    doc_py_example=_INSTALL_EXAMPLE,
    arg_docstrings=_INSTALL_ARG_DOCSTRINGS,
)
def install(
    platforms: List[Platform],
    version: Optional[str] = None,
    accept_terms: bool = False,
    force: bool = False,
    from_file: Optional[str] = None,
    *,
    _private_sdk: Optional[PrivateSkillsSDK] = None,
) -> str:
    """Install skills for the specified platform(s).

    Returns the installed version string.
    """
    return _private_sdk.install(  # type: ignore
        platforms=platforms,
        version=version,
        accept_terms=accept_terms,
        force=force,
        from_file=from_file,
    )


_UPDATE_EXAMPLE = """
import anyscale

anyscale.skills.update()
"""

_UPDATE_ARG_DOCSTRINGS = {
    "force": "Re-download and reinstall even if already on the latest version.",
    "accept_terms": "Accept updated terms non-interactively.",
}


@sdk_command(
    _SKILLS_SDK_SINGLETON_KEY,
    PrivateSkillsSDK,
    doc_py_example=_UPDATE_EXAMPLE,
    arg_docstrings=_UPDATE_ARG_DOCSTRINGS,
)
def update(
    force: bool = False,
    accept_terms: bool = False,
    *,
    _private_sdk: Optional[PrivateSkillsSDK] = None,
) -> str:
    """Update skills to the latest version.

    Returns the updated version string.
    """
    return _private_sdk.update(force=force, accept_terms=accept_terms)  # type: ignore


_GET_TERMS_EXAMPLE = """
import anyscale

terms = anyscale.skills.get_terms()
print(terms.version, terms.accepted)
"""

_GET_TERMS_ARG_DOCSTRINGS = {
    "version": "Fetch terms for a specific version instead of latest.",
}


@sdk_command(
    _SKILLS_SDK_SINGLETON_KEY,
    PrivateSkillsSDK,
    doc_py_example=_GET_TERMS_EXAMPLE,
    arg_docstrings=_GET_TERMS_ARG_DOCSTRINGS,
)
def get_terms(
    version: Optional[str] = None, *, _private_sdk: Optional[PrivateSkillsSDK] = None,
) -> TermsStatus:
    """Fetch the current user's terms acceptance status."""
    return _private_sdk.get_terms(version=version)  # type: ignore


_ACCEPT_TERMS_EXAMPLE = """
import anyscale

terms = anyscale.skills.get_terms()
if not terms.accepted:
    anyscale.skills.accept_terms(terms)
"""

_ACCEPT_TERMS_ARG_DOCSTRINGS = {
    "terms": "Terms status to accept (as returned by get_terms or TermsNotAcceptedError.terms).",
}


@sdk_command(
    _SKILLS_SDK_SINGLETON_KEY,
    PrivateSkillsSDK,
    doc_py_example=_ACCEPT_TERMS_EXAMPLE,
    arg_docstrings=_ACCEPT_TERMS_ARG_DOCSTRINGS,
)
def accept_terms(
    terms: TermsStatus, *, _private_sdk: Optional[PrivateSkillsSDK] = None,
) -> None:
    """Record acceptance of the given terms version. No-op if already accepted."""
    _private_sdk.accept_terms(terms)  # type: ignore

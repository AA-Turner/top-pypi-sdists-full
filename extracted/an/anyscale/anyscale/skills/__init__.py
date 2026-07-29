from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.skills._private.skills_sdk import PrivateSkillsSDK
from anyscale.skills.commands import (
    _ACCEPT_TERMS_ARG_DOCSTRINGS,
    _ACCEPT_TERMS_EXAMPLE,
    _GET_TERMS_ARG_DOCSTRINGS,
    _GET_TERMS_EXAMPLE,
    _INSTALL_ARG_DOCSTRINGS,
    _INSTALL_EXAMPLE,
    _LIST_ARG_DOCSTRINGS,
    _LIST_EXAMPLE,
    _UPDATE_ARG_DOCSTRINGS,
    _UPDATE_EXAMPLE,
    accept_terms as accept_terms,
    get_terms as get_terms,
    install as install,
    list as list,  # noqa: A004
    update as update,
)
from anyscale.skills.errors import (  # noqa: F401
    AlreadyInstalledError,
    PlatformVersionMismatchError,
    SKILLS_TERMS_DOC_URL,
    SkillsError,
    TermsNotAcceptedError,
)
from anyscale.skills.models import (  # noqa: F401
    CatalogEntry,
    ConfigDir,
    InstalledMetadata,
    Platform,
    PlatformInstallInfo,
    PlatformMetadata,
    PLATFORMS,
    SkillsListResult,
    SkillsManifest,
    TermsStatus,
)


class SkillsSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateSkillsSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_LIST_EXAMPLE, arg_docstrings=_LIST_ARG_DOCSTRINGS,
    )
    def list(self, version: Optional[str] = None) -> "SkillsListResult":  # noqa: F811
        """List installed skills and available updates."""
        return self._private_sdk.list(version=version)

    @sdk_docs(
        doc_py_example=_INSTALL_EXAMPLE, arg_docstrings=_INSTALL_ARG_DOCSTRINGS,
    )
    def install(  # noqa: F811
        self,
        platforms: List[Platform],
        version: Optional[str] = None,
        accept_terms: bool = False,  # noqa: F811
        force: bool = False,
        from_file: Optional[str] = None,
    ) -> str:
        """Install skills for the specified platform(s)."""
        return self._private_sdk.install(
            platforms=platforms,
            version=version,
            accept_terms=accept_terms,
            force=force,
            from_file=from_file,
        )

    @sdk_docs(
        doc_py_example=_UPDATE_EXAMPLE, arg_docstrings=_UPDATE_ARG_DOCSTRINGS,
    )
    def update(  # noqa: F811
        self, force: bool = False, accept_terms: bool = False,  # noqa: F811
    ) -> str:
        """Update skills to the latest version."""
        return self._private_sdk.update(force=force, accept_terms=accept_terms)

    @sdk_docs(
        doc_py_example=_GET_TERMS_EXAMPLE, arg_docstrings=_GET_TERMS_ARG_DOCSTRINGS,
    )
    def get_terms(self, version: Optional[str] = None,) -> "TermsStatus":  # noqa: F811
        """Fetch the current user's terms acceptance status."""
        return self._private_sdk.get_terms(version=version)

    @sdk_docs(
        doc_py_example=_ACCEPT_TERMS_EXAMPLE,
        arg_docstrings=_ACCEPT_TERMS_ARG_DOCSTRINGS,
    )
    def accept_terms(self, terms: "TermsStatus") -> None:  # noqa: F811
        """Record acceptance of the given terms version."""
        self._private_sdk.accept_terms(terms)

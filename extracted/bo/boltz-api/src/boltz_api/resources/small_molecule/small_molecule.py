# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .design import (
    DesignResource,
    AsyncDesignResource,
    DesignResourceWithRawResponse,
    AsyncDesignResourceWithRawResponse,
    DesignResourceWithStreamingResponse,
    AsyncDesignResourceWithStreamingResponse,
)
from .explore import (
    ExploreResource,
    AsyncExploreResource,
    ExploreResourceWithRawResponse,
    AsyncExploreResourceWithRawResponse,
    ExploreResourceWithStreamingResponse,
    AsyncExploreResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .library_screen import (
    LibraryScreenResource,
    AsyncLibraryScreenResource,
    LibraryScreenResourceWithRawResponse,
    AsyncLibraryScreenResourceWithRawResponse,
    LibraryScreenResourceWithStreamingResponse,
    AsyncLibraryScreenResourceWithStreamingResponse,
)

__all__ = ["SmallMoleculeResource", "AsyncSmallMoleculeResource"]


class SmallMoleculeResource(SyncAPIResource):
    """
    Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
    """

    @cached_property
    def design(self) -> DesignResource:
        """Generate novel small molecules optimized for binding to a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return DesignResource(self._client)

    @cached_property
    def library_screen(self) -> LibraryScreenResource:
        """Screen an existing library of small molecules against a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return LibraryScreenResource(self._client)

    @cached_property
    def explore(self) -> ExploreResource:
        """
        Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
        """
        return ExploreResource(self._client)

    @cached_property
    def with_raw_response(self) -> SmallMoleculeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return SmallMoleculeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SmallMoleculeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return SmallMoleculeResourceWithStreamingResponse(self)


class AsyncSmallMoleculeResource(AsyncAPIResource):
    """
    Small Molecule Pipeline: design novel small molecules and screen compound libraries against protein targets. Includes de novo generation and virtual screening.
    """

    @cached_property
    def design(self) -> AsyncDesignResource:
        """Generate novel small molecules optimized for binding to a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return AsyncDesignResource(self._client)

    @cached_property
    def library_screen(self) -> AsyncLibraryScreenResource:
        """Screen an existing library of small molecules against a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return AsyncLibraryScreenResource(self._client)

    @cached_property
    def explore(self) -> AsyncExploreResource:
        """
        Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
        """
        return AsyncExploreResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSmallMoleculeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSmallMoleculeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSmallMoleculeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncSmallMoleculeResourceWithStreamingResponse(self)


class SmallMoleculeResourceWithRawResponse:
    def __init__(self, small_molecule: SmallMoleculeResource) -> None:
        self._small_molecule = small_molecule

    @cached_property
    def design(self) -> DesignResourceWithRawResponse:
        """Generate novel small molecules optimized for binding to a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return DesignResourceWithRawResponse(self._small_molecule.design)

    @cached_property
    def library_screen(self) -> LibraryScreenResourceWithRawResponse:
        """Screen an existing library of small molecules against a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return LibraryScreenResourceWithRawResponse(self._small_molecule.library_screen)

    @cached_property
    def explore(self) -> ExploreResourceWithRawResponse:
        """
        Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
        """
        return ExploreResourceWithRawResponse(self._small_molecule.explore)


class AsyncSmallMoleculeResourceWithRawResponse:
    def __init__(self, small_molecule: AsyncSmallMoleculeResource) -> None:
        self._small_molecule = small_molecule

    @cached_property
    def design(self) -> AsyncDesignResourceWithRawResponse:
        """Generate novel small molecules optimized for binding to a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return AsyncDesignResourceWithRawResponse(self._small_molecule.design)

    @cached_property
    def library_screen(self) -> AsyncLibraryScreenResourceWithRawResponse:
        """Screen an existing library of small molecules against a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return AsyncLibraryScreenResourceWithRawResponse(self._small_molecule.library_screen)

    @cached_property
    def explore(self) -> AsyncExploreResourceWithRawResponse:
        """
        Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
        """
        return AsyncExploreResourceWithRawResponse(self._small_molecule.explore)


class SmallMoleculeResourceWithStreamingResponse:
    def __init__(self, small_molecule: SmallMoleculeResource) -> None:
        self._small_molecule = small_molecule

    @cached_property
    def design(self) -> DesignResourceWithStreamingResponse:
        """Generate novel small molecules optimized for binding to a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return DesignResourceWithStreamingResponse(self._small_molecule.design)

    @cached_property
    def library_screen(self) -> LibraryScreenResourceWithStreamingResponse:
        """Screen an existing library of small molecules against a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return LibraryScreenResourceWithStreamingResponse(self._small_molecule.library_screen)

    @cached_property
    def explore(self) -> ExploreResourceWithStreamingResponse:
        """
        Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
        """
        return ExploreResourceWithStreamingResponse(self._small_molecule.explore)


class AsyncSmallMoleculeResourceWithStreamingResponse:
    def __init__(self, small_molecule: AsyncSmallMoleculeResource) -> None:
        self._small_molecule = small_molecule

    @cached_property
    def design(self) -> AsyncDesignResourceWithStreamingResponse:
        """Generate novel small molecules optimized for binding to a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return AsyncDesignResourceWithStreamingResponse(self._small_molecule.design)

    @cached_property
    def library_screen(self) -> AsyncLibraryScreenResourceWithStreamingResponse:
        """Screen an existing library of small molecules against a protein target.

        Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
        """
        return AsyncLibraryScreenResourceWithStreamingResponse(self._small_molecule.library_screen)

    @cached_property
    def explore(self) -> AsyncExploreResourceWithStreamingResponse:
        """
        Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
        """
        return AsyncExploreResourceWithStreamingResponse(self._small_molecule.explore)

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
from .sequence_redesign import (
    SequenceRedesignResource,
    AsyncSequenceRedesignResource,
    SequenceRedesignResourceWithRawResponse,
    AsyncSequenceRedesignResourceWithRawResponse,
    SequenceRedesignResourceWithStreamingResponse,
    AsyncSequenceRedesignResourceWithStreamingResponse,
)

__all__ = ["ProteinResource", "AsyncProteinResource"]


class ProteinResource(SyncAPIResource):
    """
    Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
    """

    @cached_property
    def design(self) -> DesignResource:
        """Generate binder or generic protein designs.

        New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
        """
        return DesignResource(self._client)

    @cached_property
    def sequence_redesign(self) -> SequenceRedesignResource:
        """Redesign selected protein residues in one fixed CIF structure.

        Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
        """
        return SequenceRedesignResource(self._client)

    @cached_property
    def library_screen(self) -> LibraryScreenResource:
        """Screen an existing library of proteins against a target structure.

        Results are scored by binding confidence (likelihood of protein-protein interaction) and structure confidence.
        """
        return LibraryScreenResource(self._client)

    @cached_property
    def with_raw_response(self) -> ProteinResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return ProteinResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProteinResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return ProteinResourceWithStreamingResponse(self)


class AsyncProteinResource(AsyncAPIResource):
    """
    Design novel protein binders, redesign selected residues in fixed structures, and screen protein libraries against targets.
    """

    @cached_property
    def design(self) -> AsyncDesignResource:
        """Generate binder or generic protein designs.

        New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
        """
        return AsyncDesignResource(self._client)

    @cached_property
    def sequence_redesign(self) -> AsyncSequenceRedesignResource:
        """Redesign selected protein residues in one fixed CIF structure.

        Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
        """
        return AsyncSequenceRedesignResource(self._client)

    @cached_property
    def library_screen(self) -> AsyncLibraryScreenResource:
        """Screen an existing library of proteins against a target structure.

        Results are scored by binding confidence (likelihood of protein-protein interaction) and structure confidence.
        """
        return AsyncLibraryScreenResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProteinResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProteinResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProteinResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncProteinResourceWithStreamingResponse(self)


class ProteinResourceWithRawResponse:
    def __init__(self, protein: ProteinResource) -> None:
        self._protein = protein

    @cached_property
    def design(self) -> DesignResourceWithRawResponse:
        """Generate binder or generic protein designs.

        New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
        """
        return DesignResourceWithRawResponse(self._protein.design)

    @cached_property
    def sequence_redesign(self) -> SequenceRedesignResourceWithRawResponse:
        """Redesign selected protein residues in one fixed CIF structure.

        Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
        """
        return SequenceRedesignResourceWithRawResponse(self._protein.sequence_redesign)

    @cached_property
    def library_screen(self) -> LibraryScreenResourceWithRawResponse:
        """Screen an existing library of proteins against a target structure.

        Results are scored by binding confidence (likelihood of protein-protein interaction) and structure confidence.
        """
        return LibraryScreenResourceWithRawResponse(self._protein.library_screen)


class AsyncProteinResourceWithRawResponse:
    def __init__(self, protein: AsyncProteinResource) -> None:
        self._protein = protein

    @cached_property
    def design(self) -> AsyncDesignResourceWithRawResponse:
        """Generate binder or generic protein designs.

        New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
        """
        return AsyncDesignResourceWithRawResponse(self._protein.design)

    @cached_property
    def sequence_redesign(self) -> AsyncSequenceRedesignResourceWithRawResponse:
        """Redesign selected protein residues in one fixed CIF structure.

        Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
        """
        return AsyncSequenceRedesignResourceWithRawResponse(self._protein.sequence_redesign)

    @cached_property
    def library_screen(self) -> AsyncLibraryScreenResourceWithRawResponse:
        """Screen an existing library of proteins against a target structure.

        Results are scored by binding confidence (likelihood of protein-protein interaction) and structure confidence.
        """
        return AsyncLibraryScreenResourceWithRawResponse(self._protein.library_screen)


class ProteinResourceWithStreamingResponse:
    def __init__(self, protein: ProteinResource) -> None:
        self._protein = protein

    @cached_property
    def design(self) -> DesignResourceWithStreamingResponse:
        """Generate binder or generic protein designs.

        New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
        """
        return DesignResourceWithStreamingResponse(self._protein.design)

    @cached_property
    def sequence_redesign(self) -> SequenceRedesignResourceWithStreamingResponse:
        """Redesign selected protein residues in one fixed CIF structure.

        Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
        """
        return SequenceRedesignResourceWithStreamingResponse(self._protein.sequence_redesign)

    @cached_property
    def library_screen(self) -> LibraryScreenResourceWithStreamingResponse:
        """Screen an existing library of proteins against a target structure.

        Results are scored by binding confidence (likelihood of protein-protein interaction) and structure confidence.
        """
        return LibraryScreenResourceWithStreamingResponse(self._protein.library_screen)


class AsyncProteinResourceWithStreamingResponse:
    def __init__(self, protein: AsyncProteinResource) -> None:
        self._protein = protein

    @cached_property
    def design(self) -> AsyncDesignResourceWithStreamingResponse:
        """Generate binder or generic protein designs.

        New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
        """
        return AsyncDesignResourceWithStreamingResponse(self._protein.design)

    @cached_property
    def sequence_redesign(self) -> AsyncSequenceRedesignResourceWithStreamingResponse:
        """Redesign selected protein residues in one fixed CIF structure.

        Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
        """
        return AsyncSequenceRedesignResourceWithStreamingResponse(self._protein.sequence_redesign)

    @cached_property
    def library_screen(self) -> AsyncLibraryScreenResourceWithStreamingResponse:
        """Screen an existing library of proteins against a target structure.

        Results are scored by binding confidence (likelihood of protein-protein interaction) and structure confidence.
        """
        return AsyncLibraryScreenResourceWithStreamingResponse(self._protein.library_screen)

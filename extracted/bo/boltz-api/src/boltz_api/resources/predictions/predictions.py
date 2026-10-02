# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .adme import (
    AdmeResource,
    AsyncAdmeResource,
    AdmeResourceWithRawResponse,
    AsyncAdmeResourceWithRawResponse,
    AdmeResourceWithStreamingResponse,
    AsyncAdmeResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .structure_and_binding import (
    StructureAndBindingResource,
    AsyncStructureAndBindingResource,
    StructureAndBindingResourceWithRawResponse,
    AsyncStructureAndBindingResourceWithRawResponse,
    StructureAndBindingResourceWithStreamingResponse,
    AsyncStructureAndBindingResourceWithStreamingResponse,
)

__all__ = ["PredictionsResource", "AsyncPredictionsResource"]


class PredictionsResource(SyncAPIResource):
    """Run prediction models on molecular inputs.

    Each application is available as its own endpoint with application-specific inputs and outputs.
    """

    @cached_property
    def structure_and_binding(self) -> StructureAndBindingResource:
        """
        Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
        """
        return StructureAndBindingResource(self._client)

    @cached_property
    def adme(self) -> AdmeResource:
        """
        Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
        """
        return AdmeResource(self._client)

    @cached_property
    def with_raw_response(self) -> PredictionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return PredictionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PredictionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return PredictionsResourceWithStreamingResponse(self)


class AsyncPredictionsResource(AsyncAPIResource):
    """Run prediction models on molecular inputs.

    Each application is available as its own endpoint with application-specific inputs and outputs.
    """

    @cached_property
    def structure_and_binding(self) -> AsyncStructureAndBindingResource:
        """
        Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
        """
        return AsyncStructureAndBindingResource(self._client)

    @cached_property
    def adme(self) -> AsyncAdmeResource:
        """
        Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
        """
        return AsyncAdmeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPredictionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPredictionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPredictionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncPredictionsResourceWithStreamingResponse(self)


class PredictionsResourceWithRawResponse:
    def __init__(self, predictions: PredictionsResource) -> None:
        self._predictions = predictions

    @cached_property
    def structure_and_binding(self) -> StructureAndBindingResourceWithRawResponse:
        """
        Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
        """
        return StructureAndBindingResourceWithRawResponse(self._predictions.structure_and_binding)

    @cached_property
    def adme(self) -> AdmeResourceWithRawResponse:
        """
        Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
        """
        return AdmeResourceWithRawResponse(self._predictions.adme)


class AsyncPredictionsResourceWithRawResponse:
    def __init__(self, predictions: AsyncPredictionsResource) -> None:
        self._predictions = predictions

    @cached_property
    def structure_and_binding(self) -> AsyncStructureAndBindingResourceWithRawResponse:
        """
        Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
        """
        return AsyncStructureAndBindingResourceWithRawResponse(self._predictions.structure_and_binding)

    @cached_property
    def adme(self) -> AsyncAdmeResourceWithRawResponse:
        """
        Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
        """
        return AsyncAdmeResourceWithRawResponse(self._predictions.adme)


class PredictionsResourceWithStreamingResponse:
    def __init__(self, predictions: PredictionsResource) -> None:
        self._predictions = predictions

    @cached_property
    def structure_and_binding(self) -> StructureAndBindingResourceWithStreamingResponse:
        """
        Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
        """
        return StructureAndBindingResourceWithStreamingResponse(self._predictions.structure_and_binding)

    @cached_property
    def adme(self) -> AdmeResourceWithStreamingResponse:
        """
        Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
        """
        return AdmeResourceWithStreamingResponse(self._predictions.adme)


class AsyncPredictionsResourceWithStreamingResponse:
    def __init__(self, predictions: AsyncPredictionsResource) -> None:
        self._predictions = predictions

    @cached_property
    def structure_and_binding(self) -> AsyncStructureAndBindingResourceWithStreamingResponse:
        """
        Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
        """
        return AsyncStructureAndBindingResourceWithStreamingResponse(self._predictions.structure_and_binding)

    @cached_property
    def adme(self) -> AsyncAdmeResourceWithStreamingResponse:
        """
        Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
        """
        return AsyncAdmeResourceWithStreamingResponse(self._predictions.adme)

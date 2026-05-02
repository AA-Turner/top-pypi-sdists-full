import inspect
import logging
from typing import Any, Dict, List, Type, Union, Callable, Iterable, Optional
from typing_extensions import Self, Required, TypedDict, cast

from scale_gp.types import ResultSchemaFlexibleParam
from scale_gp.types.shared_params.chunk_extra_info_schema import Chunk, ChunkExtraInfoSchema
from scale_gp.types.shared_params.result_schema_generation import ResultSchemaGeneration
from scale_gp.types.shared_params.string_extra_info_schema import StringExtraInfoSchema

from .._client import SGPClient
from ..types.evaluation_datasets import FlexibleChunk, FlexibleMessage
from ..types.evaluation_datasets.test_case import TestCase
from ..types.application_test_case_output_batch_params import (
    Item as _ApplicationTestCaseOutputItem,
    ItemTraceSpan,
)

log: logging.Logger = logging.getLogger("scale_gp")


class ExternalApplicationOutputCompletion(TypedDict, total=False):
    generation_output: Required[str]
    metrics: Optional[Dict[str, float]]
    trace_spans: Optional[Iterable[ItemTraceSpan]]


class ExternalApplicationOutputFlexible(TypedDict):
    generation_output: Union[
        str,
        float,
        List[FlexibleChunk],
        List[FlexibleMessage],
        List[object],
        Dict[str, Union[str, float, List[FlexibleChunk], List[FlexibleMessage], List[object], object]],
        object,
    ]
    metrics: Optional[Dict[str, float]]
    trace_spans: Optional[Iterable[ItemTraceSpan]]


class ExternalApplicationOutputContextChunks(ExternalApplicationOutputCompletion):
    chunks: List[Chunk]


class ExternalApplicationOutputContextString(ExternalApplicationOutputCompletion):
    info: str


ExternalApplicationOutput = Union[
    ExternalApplicationOutputFlexible,
    ExternalApplicationOutputCompletion,
    ExternalApplicationOutputContextChunks,
    ExternalApplicationOutputContextString,
]

ExternalApplicationCallable = Union[
    Callable[[Any], ExternalApplicationOutput],
    Callable[[Any, TestCase], ExternalApplicationOutput],
]


class ExternalApplication:
    def __init__(self, client: SGPClient):
        self.client = client
        self._initialized = False
        self._output_model: Optional[Type[ExternalApplicationOutput]] = None

    def initialize(self, *, application_variant_id: str, application: ExternalApplicationCallable) -> Self:
        application_variant = self.client.application_variants.retrieve(application_variant_id)

        if application_variant.version != "OFFLINE":
            raise ValueError(f"Application variant {application_variant_id} is not an external application.")

        self.application_variant = application_variant

        def application_wrapper(input_data: Union[str, object], test_case: TestCase) -> ExternalApplicationOutput:
            args: List[Any] = [input_data]
            if len(inspect.signature(application).parameters) == 2:
                args.append(test_case)
            return application(*args)

        self.application = application_wrapper
        self._initialized = True
        return self

    def generate_outputs(self, *, evaluation_dataset_id: str, evaluation_dataset_version: int) -> None:
        self._check_initialized()

        test_cases = self._retrieve_test_cases_to_run(evaluation_dataset_id, evaluation_dataset_version)
        test_case_id_to_output: Dict[str, ExternalApplicationOutput] = {}

        for test_case in test_cases:
            input_ = test_case.test_case_data.input
            log.info(f'\nRunning test case {test_case.id}\nInput: "{input_}"')

            output = self.application(input_, test_case)
            log.info(f'\nApplication responded with:\n"{output["generation_output"]}"')

            test_case_id_to_output[test_case.id] = output

        if test_case_id_to_output:
            self._create_outputs(evaluation_dataset_version, test_case_id_to_output)

        log.info(
            f"Created {len(test_case_id_to_output)} outputs on evaluation dataset {evaluation_dataset_id} version {evaluation_dataset_version} for application variant {self.application_variant.id}"
        )

    def _retrieve_test_cases_to_run(self, evaluation_dataset_id: str, version: int) -> List[TestCase]:
        test_case_history_response = self.client.evaluation_datasets.test_cases.history.list(
            str(version),
            evaluation_dataset_id=evaluation_dataset_id,
            limit=10_000,
        )

        return [test_case for test_case in test_case_history_response.items]

    def _create_outputs(
        self,
        evaluation_dataset_version: int,
        test_case_id_to_output: Dict[str, ExternalApplicationOutput],
    ) -> None:
        items: List[_ApplicationTestCaseOutputItem] = []

        def get_output_dict(
            output: ExternalApplicationOutput,
        ) -> Union[ResultSchemaGeneration, ResultSchemaFlexibleParam]:
            if "chunks" in output:
                return ResultSchemaGeneration(
                    generation_output=output["generation_output"],
                    generation_extra_info=ChunkExtraInfoSchema(
                        schema_type="CHUNKS",
                        chunks=output["chunks"],
                    ),
                )

            elif "info" in output:
                return ResultSchemaGeneration(
                    generation_output=output["generation_output"],
                    generation_extra_info=StringExtraInfoSchema(
                        schema_type="STRING",
                        info=output["info"],
                    ),
                )

            generation_output = output["generation_output"]
            if isinstance(generation_output, str):
                return ResultSchemaGeneration(generation_output=generation_output)

            return ResultSchemaFlexibleParam(generation_output=cast(Any, generation_output))

        for test_case_id, output in test_case_id_to_output.items():
            item: _ApplicationTestCaseOutputItem = {
                "account_id": self.application_variant.account_id,
                "application_variant_id": self.application_variant.id,
                "evaluation_dataset_version_num": evaluation_dataset_version,
                "output": get_output_dict(output),
                "test_case_id": test_case_id,
            }
            if "metrics" in output and output["metrics"]:
                item["metrics"] = output["metrics"]
            if "trace_spans" in output and output["trace_spans"]:
                item["trace_spans"] = output["trace_spans"]
            items.append(item)

        self.client.application_test_case_outputs.batch(
            items=items,
        )

    def _check_initialized(self) -> None:
        if not self._initialized:
            raise ValueError(f"{self} is not initialized.")

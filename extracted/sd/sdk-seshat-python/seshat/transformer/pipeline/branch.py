from concurrent.futures.process import ProcessPoolExecutor
from typing import List, Dict

from seshat.data_class import SFrame, GroupSFrame
from seshat.general.config import DEFAULT_SF_KEY
from seshat.general.exceptions import InvalidArgumentsError
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer import Transformer
from seshat.transformer.merger.base import SFrameMerger
from seshat.transformer.pipeline import Pipeline


def process_pipeline(sf, sf_key, pipe, index, *args, **kwargs):
    if index is not None:
        return sf_key + f"__{index}", pipe(sf.get(sf_key), *args, **kwargs)
    return sf_key, pipe(sf.get(sf_key), *args, **kwargs)


class Branch(Transformer):
    """
    Branch is a Transformer that runs multiple pipelines simultaneously and merges their outputs.
    It can execute pipelines in parallel using multiple processes.

    Parameters
    ----------
    pipe_map : Dict[str, Pipeline | List[Pipeline]], optional
        A dictionary mapping SFrames to pipelines or lists of pipelines.
    merger : Merger, optional
        An object to merge the pipeline outputs.
    default_pipeline : Pipeline, optional
        A pipeline to apply to all SFrames not included in pipe_map. If None, unhandled SFrames are preserved as-is.
    parallel : bool, optional
        Whether to run pipelines in parallel. Default is False.
    max_workers : int, optional
        Maximum number of workers for parallel execution. Default is 16.
    group_keys
        Group keys for the parent Transformer class.
    *args
        Additional positional arguments.
    **kwargs
        Additional keyword arguments.

    Example usage
    ----------
    1. Creating a Branch instance with a list of pipelines:

        >>> sf_input = GroupSFrame(children={"default": DFrame(transaction_df), "address": DFrame(address_df)})
        ... pipe_map = {
        ... "default": [Pipeline(pipes=[ZeroAddressTrimmer(), LowTransactionTrimmer()]),
        ...             Pipeline(pipes=[OperationOnColsDeriver(
        ...                 cols=("sent_count", "received_count"),
        ...                 result_col="tx_count",
        ...                 agg_func="sum",
        ...                 is_numeric=True,
        ...             )])],
        ... }
        ... branch = Branch(pipe_map=pipe_map, merger=Merger())
        ... result = branch(sf_input)

    2. Creating a Branch instance with a single pipeline for each SFrame:

        >>> sf_input = GroupSFrame(children={"default": DFrame(transaction_df), "address": DFrame(address_df)})
        ... pipe_map = {
        ...     "default": Pipeline(pipes=[ZeroAddressTrimmer(), LowTransactionTrimmer()]),
        ...     "address": Pipeline(pipes=[FeatureForAddressDeriver(
        ...         value_col="ez_token_transfers_id",
        ...         result_col="received_count",
        ...         default_index_col="to_address",
        ...         agg_func="nunique",
        ...         is_numeric=False,
        ...     )])
        ... }
        ... branch = Branch(pipe_map=pipe_map, merger=Merger())
        ... result = branch(sf_input)
    """

    merger: SFrameMerger
    parallel: bool
    max_workers: int
    HANDLER_NAME = "run"

    def __init__(
        self,
        pipe_map: Dict[str, Pipeline | List[Pipeline]] = None,
        merger: SFrameMerger = None,
        default_pipeline: Pipeline = None,
        parallel: bool = False,
        max_workers: int = 16,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)

        self.pipe_map = pipe_map or {}
        self.merger = merger
        self.default_pipeline = default_pipeline
        self.parallel = parallel
        self.max_workers = max_workers

    def calculate_complexity(self):
        def max_complexity(pipe_val):
            if type(pipe_val) is Pipeline:
                return pipe_val.calculate_complexity()
            return max([pipe.calculate_complexity() for pipe in pipe_val])

        pipe_complexity = max_complexity(self.pipe_map) if self.pipe_map else 0
        default_complexity = (
            self.default_pipeline.calculate_complexity() if self.default_pipeline else 0
        )
        merger_complexity = self.merger.calculate_complexity() if self.merger else 0
        return max(pipe_complexity, default_complexity) * 0.2 + merger_complexity

    def __call__(self, sf_input: SFrame, *args, **kwargs) -> SFrame:
        result = super().__call__(sf_input, *args, **kwargs)
        if self.merger:
            result = self.merger(result)
        if isinstance(sf_input, GroupSFrame) and not self.default_pipeline:
            not_applied_sfs = set(sf_input.children.keys()) - (
                self.pipe_map.keys() if self.pipe_map else set()
            )
            for key in not_applied_sfs:
                result[key] = sf_input[key]
        return result

    def call_handler(self, sf: SFrame, *args, **kwargs) -> Dict[str, object]:
        return self.run(sf, *args, **kwargs)

    def run(self, sf: SFrame, *args, **kwargs):
        if isinstance(sf, GroupSFrame):
            if self.pipe_map and set(self.pipe_map.keys()).difference(
                set(sf.children.keys())
            ):
                raise InvalidArgumentsError(
                    "Pipeline map keys must exist in passed SFrame"
                )
        else:
            sf = sf.make_group(DEFAULT_SF_KEY)
        result = (
            self.run_parallel_pipes(sf, *args, **kwargs)
            if self.parallel
            else self.run_pipes(sf, *args, **kwargs)
        )
        return result

    def run_pipes(self, sf: GroupSFrame, *args, **kwargs):
        results = {}
        handled_keys = set()

        if self.pipe_map:
            for sf_key, pipes in self.pipe_map.items():
                handled_keys.add(sf_key)
                if isinstance(pipes, list):
                    for i in range(len(pipes)):
                        results[sf_key + f"__{i}"] = pipes[i](
                            sf.get(sf_key), *args, **kwargs
                        )
                else:
                    results[sf_key] = pipes(sf.get(sf_key), *args, **kwargs)

        if self.default_pipeline:
            unhandled_keys = set(sf.children.keys()) - handled_keys
            for sf_key in unhandled_keys:
                pipeline_result = self.default_pipeline(sf.get(sf_key), *args, **kwargs)
                results[sf_key] = pipeline_result

        return results

    def run_parallel_pipes(self, sf: SFrame, *args, **kwargs):
        results = {}
        handled_keys = set()

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            if self.pipe_map:
                for sf_key, pipes in self.pipe_map.items():
                    handled_keys.add(sf_key)
                    if isinstance(pipes, list):
                        for i in range(len(pipes)):
                            futures.append(
                                executor.submit(
                                    process_pipeline,
                                    sf,
                                    sf_key,
                                    pipes[i],
                                    i,
                                    *args,
                                    **kwargs,
                                )
                            )
                    else:
                        futures.append(
                            executor.submit(
                                process_pipeline,
                                sf,
                                sf_key,
                                pipes,
                                None,
                                *args,
                                **kwargs,
                            )
                        )

            if isinstance(sf, GroupSFrame):
                unhandled_keys = set(sf.children.keys()) - handled_keys
                if self.default_pipeline:
                    for sf_key in unhandled_keys:
                        futures.append(
                            executor.submit(
                                process_pipeline,
                                sf,
                                sf_key,
                                self.default_pipeline,
                                None,
                                *args,
                                **kwargs,
                            )
                        )

            for future in futures:
                key, result = future.result()
                results[key] = result

        return results

    def should_convert(self, sf: SFrame):
        return False


class BranchStory(BaseTransformerStory):
    transformer = Branch
    use_cases = [
        "Run multiple independent pipelines on the same input data and collect results",
        "Apply different transformations to different SFrames in a GroupSFrame simultaneously",
        "Execute pipelines in parallel to improve processing performance",
    ]
    logic_overview = (
        "Branch applies multiple pipelines to SFrames and optionally merges results. "
        "It maps pipelines to specific SFrame keys, processes them sequentially or in parallel, "
        "and can merge outputs using a Merger. When a list of pipelines is provided for a single "
        "SFrame key, the outputs are stored with indexed keys. Often used after BranchClassifier "
        "to apply different pipelines to each classified group."
    )
    steps = [
        "Initialize with a pipe_map defining which pipelines apply to which SFrames",
        "Validate that all pipe_map keys exist in the input GroupSFrame",
        "For each SFrame key in pipe_map, apply the associated pipeline(s)",
        "If parallel=True, execute pipelines concurrently using ProcessPoolExecutor",
        "Store results with original keys or indexed keys for multiple pipelines",
        "If a merger is configured, merge the pipeline results",
        "Preserve any SFrames not in pipe_map in the output",
    ]
    tags = ["pipeline", "parallel-processing"]

    def get_scenarios(self):
        from test.transformer.pipeline.test_branch_pipeline import (
            BranchPipelineTestCase,
        )

        return TransformerScenario.from_testcase(
            BranchPipelineTestCase, transformer=self.transformer
        )

    interactions = [
        (
            "BranchClassifier",
            "BranchClassifier creates groups, Branch processes each group separately. "
            "The pipe_map keys in Branch must exactly match the group keys generated by BranchClassifier. "
            "Use NestedKeyMerger after Branch to combine results back into a single SFrame. "
            "This pattern is essential when you need to run different pipelines based on grouping criteria "
            "such as timestamp ranges, categories, or other attributes. The workflow is: "
            "BranchClassifier (split by criteria) → Branch (apply different pipelines) → NestedKeyMerger "
            "(combine results). This allows parallel processing of different data segments with "
            "specialized transformations.",
        )
    ]

from typing import Literal, Optional, Sequence, Union

from dlt.common.typing import TypedDict

from dlt.pipeline.typing import TPipelineStep


class RetryPolicyConfig(TypedDict, total=False):
    """Configuration for retry policy in dlt.yml"""

    type: Literal["none", "backoff", "fixed"]
    max_attempts: Optional[int]
    multiplier: Optional[int]
    min: Optional[int]
    max: Optional[int]


class PipelineRunConfig(TypedDict, total=False):
    """Configuration for pipeline run as defined in dlt.yml"""

    run_from_clean_folder: Optional[bool]
    store_trace_info: Optional[Union[bool, str]]
    retry_policy: Optional[RetryPolicyConfig]
    retry_pipeline_steps: Optional[Sequence[TPipelineStep]]

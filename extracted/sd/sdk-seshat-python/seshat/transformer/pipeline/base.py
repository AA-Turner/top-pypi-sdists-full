from typing import List

from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer import Transformer


class Pipeline(Transformer):
    """
    A data processing pipeline that sequentially applies a list of transformers to input data.
    Each transformer in the `pipes` list processes the data and passes the output to the next transformer
    in the sequence. The result from the last transformer in the list is the final output of the pipeline.

    The transformers in the `pipes` list must be capable of applying a transformation and
    producing an output that can be handled by the next transformer in the list, if there is one.
    This allows for a flexible and modular design where different transformations can be chained
    together to achieve complex data processing workflows.

    Parameters
    ----------
    pipes : list of Transformer instances
        A list of transformer objects through which the data will be passed in sequence.
        The output of one transformer becomes the input to the next.

    Examples
    --------
    >>> pipeline = Pipeline(pipes=[transformer1, transformer2]
    >>> pipeline(input_data)

    Notes
    -----
    This pipeline design is particularly useful for data transformations where multiple
    discrete processing steps are required. Each transformer should be designed to handle
    the output from the previous transformer in the sequence, ensuring compatibility between transformations.
    """

    pipes: List[Transformer]

    def __init__(self, pipes: List[Transformer]):
        self.pipes = pipes

    def __call__(self, sf_input, *args, **kwargs):
        result = sf_input
        for pipe in self.pipes:
            result = pipe(result, *args, **kwargs)
        return result

    def replace(self, transformer: Transformer, index: int):
        self.pipes[index] = transformer
        return self

    def append(self, transformer: Transformer):
        self.pipes.append(transformer)
        return self

    def insert(self, transformer: Transformer, index: int):
        self.pipes.insert(index, transformer)
        return self

    def remove(self, index: int):
        self.pipes.pop(index)
        return self


class PipelineStory(BaseTransformerStory):
    transformer = Pipeline
    use_cases = [
        (
            "Chain multiple transformers to process data sequentially, where the output of one transformer "
            "becomes the input for the next."
        ),
        (
            "Build modular and reusable data processing workflows by combining simple transformers "
            "into a complex pipeline."
        ),
    ]
    logic_overview = (
        "The Pipeline transformer takes a list of transformer instances and applies them in sequence "
        "to the input data. Each transformer's output is passed as input to the next transformer in the list. "
        "The final output is the result of the last transformer. "
        "This enables flexible, modular, and reusable data processing workflows."
    )
    steps = [
        "Initialize the Pipeline with a list of transformer instances (pipes).",
        "Pass the input data to the first transformer in the list.",
        "Take the output of each transformer and pass it as input to the next transformer in the sequence.",
        "Continue this process until all transformers have been applied.",
        "Return the output from the last transformer as the final result.",
    ]
    tags = ["pipeline" "sequential-processing"]

    def get_scenarios(self):
        from test.transformer.pipeline.test_pipeline import PipelineDFTestCase

        return TransformerScenario.from_testcase(
            PipelineDFTestCase, transformer=self.transformer
        )

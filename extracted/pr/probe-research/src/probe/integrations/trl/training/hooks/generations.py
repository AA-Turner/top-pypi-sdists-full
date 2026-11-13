"""Which sample each loss row is, for trainers that generate a batch, then shuffle and split it into micro-batches
(GRPO, RLOO, Distillation): two 1-D tensors added to each generation's output ride TRL's shuffle and split
(`shuffle_sequence_dict`, `split_tensor_dict`), so a micro-batch row still names its generation row and the key the
sample recorder gave it (`{split}:{step}:{call}:{process}:{row}`)."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any

from probe.generated.samples import SampleSplit

ROW, GENERATION = "_probe_points_row", "_probe_points_generation"
#: Train generations whose rows can still be trained (`steps_per_generation x num_iterations` micro-steps each).
MAX_GENERATIONS = 256
#: Eval generations are trained by the one loss call right after them (each is dropped then); a pass that records
#: nothing leaves these few.
MAX_EVAL_GENERATIONS = 16


class GenerationStamps:
    """Generation ordinal -> its rows' key prefix, by split: a long `evaluate()` never evicts the train generations
    still being trained."""

    def __init__(self, recorder: Any) -> None:
        self.recorder = recorder
        self._prefixes: dict[str, OrderedDict[int, str]] = {
            SampleSplit.TRAIN: OrderedDict(), SampleSplit.EVAL: OrderedDict()}
        self._count = 0

    def stamp(self, output: Any, split: str) -> None:
        """Name each row of a generation's output by the key the sample recorder gave it (the call it just took)."""
        ids = output.get("completion_ids") if isinstance(output, dict) else None
        if type(ids).__module__.split(".")[0] != "torch":
            return  # not TRL's tensors: nothing to carry through its shuffle
        import torch

        step, call = self.recorder.get_last_call(split)
        rows = int(ids.shape[0])
        ordinal = self._count
        self._count += 1
        prefixes = self._prefixes[split]
        prefixes[ordinal] = f"{split}:{step}:{call}:{self.recorder.rank}"
        while len(prefixes) > (MAX_GENERATIONS if split == SampleSplit.TRAIN else MAX_EVAL_GENERATIONS):
            prefixes.popitem(last=False)
        output[ROW] = torch.arange(rows, device=ids.device)
        output[GENERATION] = torch.full((rows,), ordinal, dtype=torch.long, device=ids.device)

    def get_columns(self, inputs: Any) -> list[Any] | None:
        """The two stamp columns of a micro-batch (copied with its rows), or None when it carries none."""
        return [inputs[ROW], inputs[GENERATION]] if ROW in inputs else None

    def take_keys(self, places: list[tuple[float, float]], split: str) -> list[str]:
        """Each row's sample key from its (row, generation) stamp; an eval generation is trained by this one call, so
        it is dropped here."""
        prefixes = self._prefixes[split]
        keys = [f"{prefixes[int(generation)]}:{int(row)}" for row, generation in places]
        if split == SampleSplit.EVAL:
            for _row, generation in places:
                prefixes.pop(int(generation), None)
        return keys

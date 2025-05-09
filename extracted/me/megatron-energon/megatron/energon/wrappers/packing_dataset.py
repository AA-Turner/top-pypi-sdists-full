# Copyright (c) 2025, NVIDIA CORPORATION.
# SPDX-License-Identifier: BSD-3-Clause

import inspect
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from megatron.energon.errors import SYSTEM_EXCEPTIONS, FatalSampleError
from megatron.energon.flavors.base_dataset import SavableDataset, set_sample_restore_key
from megatron.energon.worker import WorkerConfig
from megatron.energon.wrappers._log_exception import log_exception
from megatron.energon.wrappers.base import BaseWrapperDataset, SampleIndex, get_sample_restore_key
from megatron.energon.wrappers.buffer import SavableSampleBuffer
from megatron.energon.wrappers.skip import SkipSample

T_sample = TypeVar("T_sample")
T_batch_sample = TypeVar("T_batch_sample")


class PackingDataset(
    BaseWrapperDataset[T_sample, T_batch_sample], Generic[T_sample, T_batch_sample]
):
    """This dataset wrapper transforms samples of a dataset into chunks/packs of samples, which are
    then combined into a batch."""

    buffer_size: int
    pre_packer: Callable[[List[T_sample]], List[List[T_sample]]]
    final_packer: Callable[[List[T_sample]], T_batch_sample]
    final_packer_stateless: bool
    packer_config: Optional[Union[Dict[str, Any], Callable[[], Dict[str, Any]]]]
    error_handler: Callable[[Exception, List[T_sample]], None]

    #: The buffer for collecting the samples that shall be packed.
    _reading_buffer: SavableSampleBuffer

    #: Contains the pre-selected samples to be packed.
    #: The full buffer will be passed to the pre_packer.
    _pre_packing_buffer: SavableSampleBuffer

    #: Lengths of the selected groups of samples to be packed together.
    #: The samples are stored sequentially in the pre_packing_buffer because
    #: SavableSampleBuffer doesn't support nesting. But to keep the groups
    #: separate, we need to store the lengths of the groups here.
    _pre_packing_lengths: List[List[int]]

    #: Sample index for the pre_packer
    _pre_packing_sample_index: SampleIndex

    #: Sample index for the final_packer
    _final_packing_sample_index: SampleIndex

    _savable_fields = (
        "_reading_buffer",
        "_pre_packing_buffer",
        "_pre_packing_lengths",
        "_pre_packing_sample_index",
        "_final_packing_sample_index",
    )

    def __init__(
        self,
        dataset: SavableDataset[T_sample],
        buffer_size: int,
        pre_packer: Callable[[List[T_sample]], List[List[T_sample]]],
        final_packer: Callable[[List[T_sample]], T_batch_sample],
        *,
        final_packer_stateless: bool = False,
        packer_config: Optional[Union[Dict[str, Any], Callable[[], Dict[str, Any]]]] = None,
        error_handler: Callable[[Exception, List[T_sample]], None] = log_exception,
        worker_config: WorkerConfig,
    ):
        """Construct a PackingDataset which is used for sequence packing.
        Using a pre_packer and final_packer, it buffers the incoming samples, groups
        them together based on the logic provided by the pre_packer, and then (using
        the final_packer) combines each group into a packed single sample also called
        a "pack" or a "packed sequence".

        Args:
            dataset: The input dataset to wrap
            buffer_size: The desired size of the input buffer for pre packing. Last buffer of a dataset may be smaller.
            pre_packer: Function which selects samples from the buffer to be packed together.
                May raise :exc:`megatron.energon.SkipSample` to skip a buffer.
            final_packer: Function which combines the selected samples into a single sample.
            final_packer_stateless: If True, the final_packer is stateless, thus samples can be
                stored/restored.
            packer_config: Configuration for the (pre|final)_packer functions. If callable, it should return the
                configuration. Defaults to None.
            error_handler: Function which handles exceptions raised by the batcher. The default
                implementation logs the exception.
            worker_config: Configuration for the workers.
        """
        super().__init__(dataset, worker_config=worker_config)

        assert buffer_size > 0, "Packing buffer size must be greater than 0."

        self.buffer_size = buffer_size
        self.pre_packer = pre_packer
        self.final_packer = final_packer
        self.final_packer_stateless = final_packer_stateless
        self.packer_config = packer_config
        self.error_handler = error_handler

        self.reset_state_own()

    def reset_state_own(self) -> None:
        self._reading_buffer = SavableSampleBuffer(self.dataset, worker_config=self.worker_config)
        self._pre_packing_buffer = SavableSampleBuffer(
            self.dataset, worker_config=self.worker_config
        )
        self._pre_packing_lengths = []
        self._pre_packing_sample_index = SampleIndex(self.worker_config, src=self)
        self._final_packing_sample_index = SampleIndex(self.worker_config, src=self)

    def __len__(self):
        """The real length is unknown, since it depends on the packing function.
        We approximate it by the length of the source dataset."""

        return len(self.dataset)

    def _fill_reading_buffer(self, source_iter: Iterator) -> bool:
        """
        Fill the reading buffer with samples from the dataset source iterator.

        Args:
            source_iter: Iterator of samples from the dataset.

        Returns:
            True if samples are successfully read into the buffer, False if no more data.
        """

        while len(self._reading_buffer) + len(self._pre_packing_buffer) < self.buffer_size:
            try:
                sample = next(source_iter)
                self._reading_buffer.append(sample)
            except StopIteration:
                return False
        return True

    def __iter__(self) -> Iterator[T_batch_sample]:
        pre_packing_lengths = self._pre_packing_lengths
        # The source dataset
        src_iter = iter(self.dataset)

        self._pre_packing_buffer.worker_start()
        self._reading_buffer.worker_start()

        def next_pre_pack():
            """Take the samples from the reading buffer and select groups of samples to be packed
            together."""

            assert len(self._pre_packing_buffer) == 0
            if len(self._reading_buffer) > 0:
                # Take all samples from the reading buffer and pre_pack them
                samples = list(self._reading_buffer)
                # Clear buffer and pre_packing_lengths
                self._reading_buffer.clear()
                pre_packing_lengths.clear()
                # Now pre pack the samples
                try:
                    with self._pre_packing_sample_index.ctx():
                        pre_packs = self.pre_packer(samples)
                except SkipSample:
                    pre_packs = []
                except SYSTEM_EXCEPTIONS:
                    raise FatalSampleError.from_sample(samples)
                except Exception as e:
                    self.error_handler(e, samples)
                    pre_packs = []

                # Put the pre-packed samples into the pre_packing_buffer
                # They will be flattened here to avoid nested buffers
                # But the lengths of the groups are stored in pre_packing_lengths
                # so that the groups can be separated later
                for pre_pack in pre_packs:
                    self._pre_packing_buffer.extend(pre_pack)
                    pre_packing_lengths.append(len(pre_pack))

        def next_final_pack() -> Generator[T_batch_sample, None, None]:
            """Yield the next packs from the buffer. The final packer is called on the fly."""

            pack = list(self._pre_packing_buffer[: pre_packing_lengths[0]])
            del self._pre_packing_buffer[: pre_packing_lengths[0]]
            del pre_packing_lengths[0]
            try:
                pack_restore_keys = tuple(get_sample_restore_key(sample) for sample in pack)
                with self._final_packing_sample_index.ctx() as pack_idx:
                    final_packed_sample = self.final_packer(pack)
                if isinstance(final_packed_sample, Generator):
                    assert inspect.isgeneratorfunction(self.final_packer), (
                        f"Generator in {self.final_packer} but not marked as such."
                    )
                    for pack_sub_idx, (pack_idx, inner_batch_sample) in enumerate(
                        self._final_packing_sample_index.iter_ctx(final_packed_sample, pack_idx)
                    ):
                        yield set_sample_restore_key(
                            inner_batch_sample,
                            pack_idx,
                            pack_sub_idx,
                            *pack_restore_keys,
                            src=self,
                        )
                else:
                    yield set_sample_restore_key(
                        final_packed_sample,
                        pack_idx,
                        *pack_restore_keys,
                        src=self,
                    )
            except SkipSample:
                pass
            except SYSTEM_EXCEPTIONS:
                raise FatalSampleError.from_sample(pack)
            except Exception as e:
                self.error_handler(e, pack)

        # Main loop:
        pre_pack_round = 0
        while True:
            if pre_pack_round > 10:
                raise RuntimeError("Pre packer did not yield any packs after 10 rounds.")
            # Fill a portion of the buffer
            if not self._fill_reading_buffer(src_iter):
                # Break out of the main loop when the source is exhausted.
                # But yield the remaining packs first.
                if len(self._reading_buffer) > 0:
                    next_pre_pack()
                break

            # Create new pre packs if necessary
            if len(pre_packing_lengths) == 0:
                assert len(self._pre_packing_buffer) == 0
                assert len(self._reading_buffer) == self.buffer_size
                next_pre_pack()
                if len(pre_packing_lengths) == 0:
                    # Retry packing, nothing was returned.
                    pre_pack_round += 1
                    continue

            if len(pre_packing_lengths) > 0:
                pre_pack_round = 0

            yield from next_final_pack()

        # Yield the remaining packs, flushing the collecting buffer
        while len(pre_packing_lengths) > 0:
            yield from next_final_pack()

    def can_restore_sample(self) -> bool:
        # Cannot really verify if the returned elements contain a __restore_key__.
        # If the user wants to use this, well...
        return super().can_restore_sample() and self.final_packer_stateless

    def assert_can_restore(self):
        assert self.final_packer_stateless, (
            f"Final packer {self.final_packer} must be stateless to restore samples."
        )
        super().assert_can_restore()

    def restore_sample(self, index: Tuple[Union[str, int, tuple], ...]) -> T_sample:
        # We need to store multiple indices to restore a batch.
        self.assert_can_restore()
        if inspect.isgeneratorfunction(self.final_packer):
            id, pack_idx, pack_sub_idx, *pack_restore_keys = index
            assert id == type(self).__name__
        else:
            id, pack_idx, *pack_restore_keys = index
            assert id == type(self).__name__
        batch = [self.dataset.restore_sample(inner_idx) for inner_idx in pack_restore_keys]
        with self._final_packing_sample_index.ctx(pack_idx):
            final_pack = self.final_packer(batch)
        if isinstance(final_pack, Generator):
            assert inspect.isgeneratorfunction(self.final_packer), (
                f"Generator in {self.final_packer} but not marked as such."
            )
            for cur_batch_sub_idx, (pack_idx, inner_batch_sample) in enumerate(
                self._final_packing_sample_index.iter_ctx(final_pack, pack_idx)
            ):
                if cur_batch_sub_idx == pack_sub_idx:
                    return set_sample_restore_key(
                        inner_batch_sample,
                        pack_idx,
                        pack_sub_idx,
                        *pack_restore_keys,
                        src=self,
                    )
            assert False, f"Pack sub-index {pack_sub_idx} not found in pack"
        else:
            return set_sample_restore_key(final_pack, pack_idx, *pack_restore_keys, src=self)

    def config(self) -> Dict[str, Any]:
        return {
            "type": type(self).__qualname__,
            "buffer_size": self.buffer_size,
            "pre_packer": self._function_config(self.pre_packer),
            "final_packer": self._function_config(self.final_packer),
            "final_packer_stateless": self.final_packer_stateless,
            **(
                {
                    "packer_config": (
                        self.packer_config() if callable(self.packer_config) else self.packer_config
                    )
                }
                if self.packer_config
                else {}
            ),
            "error_handler": self._function_config(self.error_handler),
            "worker_config": self.worker_config.config(),
            "dataset": self.dataset.config(),
        }

    def __str__(self):
        return f"PackingDataset(buffer_size={self.buffer_size}, pre_packer={self.pre_packer}, final_packer={self.final_packer}, dataset={self.dataset})"

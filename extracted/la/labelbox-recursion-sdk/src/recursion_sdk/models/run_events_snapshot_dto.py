from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_blocks_item import RunEventsSnapshotDtoBlocksItem
  from ..models.run_events_snapshot_dto_pooled_boxplots_item import RunEventsSnapshotDtoPooledBoxplotsItem
  from ..models.run_events_snapshot_dto_status_type_0 import RunEventsSnapshotDtoStatusType0
  from ..models.run_events_snapshot_dto_terminal_type_0_type_0 import RunEventsSnapshotDtoTerminalType0Type0
  from ..models.run_events_snapshot_dto_terminal_type_0_type_1 import RunEventsSnapshotDtoTerminalType0Type1





T = TypeVar("T", bound="RunEventsSnapshotDto")



@_attrs_define
class RunEventsSnapshotDto:
    """ A read snapshot of a job's live training telemetry, projected from run_events. Render precomputed blocks only — no
    stats math in the consumer.

        Example:
            {'status': None, 'blocks': [], 'terminal': None, 'pooledBoxplots': []}

        Attributes:
            status (None | RunEventsSnapshotDtoStatusType0): Most recently ingested status envelope for this job, or null if
                none has arrived yet.
            blocks (list[RunEventsSnapshotDtoBlocksItem]): Blocks documents ingested for this job, ordered oldest to newest
                by step, capped to a bounded recent window.
            terminal (None | RunEventsSnapshotDtoTerminalType0Type0 | RunEventsSnapshotDtoTerminalType0Type1): Terminal
                record for this job, once it has finished.
            pooled_boxplots (list[RunEventsSnapshotDtoPooledBoxplotsItem]): Pooled five-number summaries for every boxplot-
                block title present in blocks, computed once server-side across the full fetched window — see
                PooledBoxplotSchema.
     """

    status: None | RunEventsSnapshotDtoStatusType0
    blocks: list[RunEventsSnapshotDtoBlocksItem]
    terminal: None | RunEventsSnapshotDtoTerminalType0Type0 | RunEventsSnapshotDtoTerminalType0Type1
    pooled_boxplots: list[RunEventsSnapshotDtoPooledBoxplotsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_blocks_item import RunEventsSnapshotDtoBlocksItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_pooled_boxplots_item import RunEventsSnapshotDtoPooledBoxplotsItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0 import RunEventsSnapshotDtoStatusType0 # noqa: PLC0415
        from ..models.run_events_snapshot_dto_terminal_type_0_type_0 import RunEventsSnapshotDtoTerminalType0Type0 # noqa: PLC0415
        from ..models.run_events_snapshot_dto_terminal_type_0_type_1 import RunEventsSnapshotDtoTerminalType0Type1 # noqa: PLC0415
        status: dict[str, Any] | None
        if isinstance(self.status, RunEventsSnapshotDtoStatusType0):
            status = self.status.to_dict()
        else:
            status = self.status

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item = blocks_item_data.to_dict()
            blocks.append(blocks_item)



        terminal: dict[str, Any] | None
        if isinstance(self.terminal, RunEventsSnapshotDtoTerminalType0Type0):
            terminal = self.terminal.to_dict()
        elif isinstance(self.terminal, RunEventsSnapshotDtoTerminalType0Type1):
            terminal = self.terminal.to_dict()
        else:
            terminal = self.terminal

        pooled_boxplots = []
        for pooled_boxplots_item_data in self.pooled_boxplots:
            pooled_boxplots_item = pooled_boxplots_item_data.to_dict()
            pooled_boxplots.append(pooled_boxplots_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "blocks": blocks,
            "terminal": terminal,
            "pooledBoxplots": pooled_boxplots,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_blocks_item import RunEventsSnapshotDtoBlocksItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_pooled_boxplots_item import RunEventsSnapshotDtoPooledBoxplotsItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0 import RunEventsSnapshotDtoStatusType0 # noqa: PLC0415
        from ..models.run_events_snapshot_dto_terminal_type_0_type_0 import RunEventsSnapshotDtoTerminalType0Type0 # noqa: PLC0415
        from ..models.run_events_snapshot_dto_terminal_type_0_type_1 import RunEventsSnapshotDtoTerminalType0Type1 # noqa: PLC0415
        d = dict(src_dict)
        def _parse_status(data: object) -> None | RunEventsSnapshotDtoStatusType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                status_type_0 = RunEventsSnapshotDtoStatusType0.from_dict(data)



                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoStatusType0, data)

        status = _parse_status(d.pop("status"))


        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in (_blocks):
            blocks_item = RunEventsSnapshotDtoBlocksItem.from_dict(blocks_item_data)



            blocks.append(blocks_item)


        def _parse_terminal(data: object) -> None | RunEventsSnapshotDtoTerminalType0Type0 | RunEventsSnapshotDtoTerminalType0Type1:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                terminal_type_0_type_0 = RunEventsSnapshotDtoTerminalType0Type0.from_dict(data)



                return terminal_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                terminal_type_0_type_1 = RunEventsSnapshotDtoTerminalType0Type1.from_dict(data)



                return terminal_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoTerminalType0Type0 | RunEventsSnapshotDtoTerminalType0Type1, data)

        terminal = _parse_terminal(d.pop("terminal"))


        pooled_boxplots = []
        _pooled_boxplots = d.pop("pooledBoxplots")
        for pooled_boxplots_item_data in (_pooled_boxplots):
            pooled_boxplots_item = RunEventsSnapshotDtoPooledBoxplotsItem.from_dict(pooled_boxplots_item_data)



            pooled_boxplots.append(pooled_boxplots_item)


        run_events_snapshot_dto = cls(
            status=status,
            blocks=blocks,
            terminal=terminal,
            pooled_boxplots=pooled_boxplots,
        )

        return run_events_snapshot_dto


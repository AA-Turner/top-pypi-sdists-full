from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.snapshot_tag import SnapshotTag
    from istari_digital_client.legacy.v2.models.system import System


@dataclass
class SubsystemLink:
    system: System
    tag: Optional[SnapshotTag] = field(default=None)

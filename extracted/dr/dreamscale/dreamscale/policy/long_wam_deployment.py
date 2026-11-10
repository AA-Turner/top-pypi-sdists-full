"""Server-described Long-WAM deployment wire: its robot preset (the Bimanual YAM, checked
against dreamscale_transport.long_wam_deploy by the shared preset session), its actions (joint
targets held between chunks, RTC off), and what it adds to them: each request carries per
camera one strip of 224x224 frames, those 48, 44, ..., 4 executed ticks back that the episode
has reached, then the current one (``context.TickHistory``). Before the oldest offset, the
episode's first frame travels once ahead of them, and the server repeats it for the offsets
not yet reached, as upstream's window does (``history_start``)."""

from __future__ import annotations

import dataclasses
from typing import Any

from dreamscale_transport.images import WireImage
from dreamscale_transport.long_wam_deploy import HISTORY_OFFSETS, IMAGE_SIZE

from dreamscale.deploy_bases.long_wam import UNITS
from dreamscale.policy.preset_deployment import PresetSessionDeployment, preset_runtime_contract

# Each camera stretched to 224x224 (upstream's processor resizes without cropping).
WIRE_IMAGE = WireImage(IMAGE_SIZE, IMAGE_SIZE, mode="stretch", resample="bilinear", quality=90)


class LongWamSessionDeployment(PresetSessionDeployment):
    units = UNITS


def runtime_contract(resolved: Any, deployment: Any) -> Any:
    contract = preset_runtime_contract(LongWamSessionDeployment, resolved, deployment)
    return dataclasses.replace(contract, wire_image=WIRE_IMAGE, history_ticks=HISTORY_OFFSETS,
                               history_start=True)

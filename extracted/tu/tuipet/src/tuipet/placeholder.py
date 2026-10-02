"""Stand-in sprite for any creature whose art is unfinished -- DVPet's own
`copymon`. In the current data set this never triggers (all 1525 creatures have
real, extracted art), but if a future build has an unfinished cell we show a real
DVPet sprite, never a drawn one."""
from __future__ import annotations
from . import data


def _frames():
    cm = data.load_effects().get("copymon")
    return cm if cm else [["0000000000000000"]]


# the stand-in sheet must answer EVERY raw role index (visual audit
# 2026-07-25): data.ROLES tops out at index 10 (exhausted) and the geriatric
# shuffle (+9 over idle's [0,1]) tops at 10 too, but copymon is a single
# frame -- so the crash-loop defense record_for exists for ("a cross-version
# save wears the placeholder") crashed on the first non-guarded pose fetch
# (IndexError in _pose_rows: every care fx, the sleep pose, the sick
# collapse).  Pad the sheet to 11: same rip, every slot answers.
FRAMES = (_frames() * 11)[:11]
W = max(len(r) for r in FRAMES[0])
H = len(FRAMES[0])


def record(num, name, stage, attribute):
    return {"num": num, "name": name, "stage": stage, "attribute": attribute,
            "field": "None", "element": "None", "spriteSet": 0, "spriteNum": 0,
            "w": W, "h": H, "frames": FRAMES, "_placeholder": True}

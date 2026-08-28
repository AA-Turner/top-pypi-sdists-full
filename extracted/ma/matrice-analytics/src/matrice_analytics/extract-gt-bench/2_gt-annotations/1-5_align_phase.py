r"""
align_phase.py — find the Case B rotation S by eye, then lock it across the subsample.

Runs BETWEEN 1_consolidate.py and 2_verify.py.

The collection's `src_idx` is rotated from the true source-video frame by an unknown
CONSTANT S (Case B: the RTP clock never resets per loop, so the collector anchored
src_idx=0 to wherever the stream happened to be).  This tool lets you slide the
detection overlay and the video frame INDEPENDENTLY until the boxes sit on people,
then "SET" to lock the offset and step forward in subsample order — the video frame
follows in lockstep so you can confirm the alignment holds frame after frame.  Once
convinced, save: frames/alerts/counts are re-keyed by S to ABSOLUTE source-video
indices.

Overlays use exactly what `1_consolidate.py` put in `frames` — the
`agg_summary.tracking_stats.detections` boxes (its default), not the raw model
detections.

Model of operation
------------------
  FREE  : detection cursor and video frame move separately.
  SET   : S = (video_frame - src_idx) mod N is locked.  Stepping the detection
          cursor recomputes video_frame = (src_idx + S) mod N (wraps at the loop
          end → back to the top of the video).  Nudging the video re-defines S.

Controls
--------
  VIDEO frame :  <- / ->  -1 / +1     Up / Down  -10 / +10     [ / ]  -100 / +100
                 (in SET mode these nudge S instead, re-aligning globally)
  DETECTION   :  a / d  prev / next sample        z / c  -10 / +10 samples
  f           :  toggle SET (lock offset & follow  /  free scrub)
  s           :  save re-keyed (absolutely-mapped) JSON to --out
  r           :  reset to FREE
  q / Esc     :  quit

Usage
-----
    python align_phase.py --video path\to\loitering-check.mp4 --json vms-pred.json
    python align_phase.py --video gt.mp4 --json vms-pred.json --out vms-pred-aligned.json
"""

import argparse
import json
import sys
from pathlib import Path

import cv2

from loitering_common import color_for_class, ensure_loitering_class_names

VERIFY_COLORS = {0: (180, 50, 200), 1: (0, 140, 255)}  # BGR: person / loitering_person


state = {
    "cap": None,
    "data": {},
    "samples": [],       # sorted src_idx ints present in the JSON
    "di": 0,             # detection cursor (index into samples)
    "vf": 0,             # current video frame
    "N": 0,              # loop length in frames (modulus)
    "S": None,           # locked rotation when set; last value kept for save
    "set_mode": False,
    "class_names": {},
    "alerts": {},
    "n_video_frames": 0,
}


def src_idx_now():
    return state["samples"][state["di"]]


def get_dets(src_idx):
    return state["data"]["frames"].get(str(src_idx), [])


def clamp_di(i):
    return max(0, min(len(state["samples"]) - 1, i))


def wrap_vf(v):
    n = state["N"]
    return v % n if n else max(0, v)


def move_detection(delta):
    state["di"] = clamp_di(state["di"] + delta)
    if state["set_mode"] and state["S"] is not None:
        state["vf"] = wrap_vf(src_idx_now() + state["S"])


def move_video(delta):
    if state["set_mode"]:
        # Re-define the global offset by nudging the video while staying on this sample.
        state["S"] = wrap_vf((state["S"] or 0) + delta)
        state["vf"] = wrap_vf(src_idx_now() + state["S"])
    else:
        state["vf"] = wrap_vf(state["vf"] + delta)


def toggle_set():
    if state["set_mode"]:
        state["set_mode"] = False
    else:
        state["S"] = wrap_vf(state["vf"] - src_idx_now())
        state["set_mode"] = True


def color_for(cid):
    return VERIFY_COLORS.get(int(cid), VERIFY_COLORS[0])


def class_label(cid):
    return state["class_names"].get(str(int(cid)), str(int(cid)))


def read_video_frame(idx):
    cap = state["cap"]
    n = state["n_video_frames"]
    i = idx % n if n else idx
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
    ok, frame = cap.read()
    if not ok:
        import numpy as np
        return np.zeros((480, 640, 3), dtype="uint8")
    return frame


def draw_box(img, det, w, h):
    cid = int(det.get("class_id", 0))
    x1 = int(det["bbox"][0] * w); y1 = int(det["bbox"][1] * h)
    x2 = int(det["bbox"][2] * w); y2 = int(det["bbox"][3] * h)
    c = color_for(cid)
    cv2.rectangle(img, (x1, y1), (x2, y2), c, 2)
    label = det.get("category") or class_label(cid)
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(label, font, 0.45, 1)
    cv2.rectangle(img, (x1, max(0, y1 - th - 6)), (x1 + tw + 6, y1), c, -1)
    cv2.putText(img, label, (x1 + 3, max(th + 1, y1 - 4)), font, 0.45,
                (255, 255, 255), 1, cv2.LINE_AA)


def draw_overlay(img):
    sidx = src_idx_now()
    mode = "SET" if state["set_mode"] else "FREE"
    s_txt = "--" if state["S"] is None else str(state["S"])
    boxes = len(get_dets(sidx))
    line1 = (f"[{mode}]  sample {state['di'] + 1}/{len(state['samples'])}  src_idx={sidx}"
             f"   video_frame={state['vf']}   S={s_txt}   boxes={boxes}")
    line2 = ("VIDEO <-/-> 1  Up/Dn 10  [ ] 100   |   DET a/d 1  z/c 10   |   "
             "f SET/follow   s save   r reset   q quit")
    if state["set_mode"]:
        line2 = ("SET: a/d step detection (video follows)   <-/-> nudge S   "
                 "f unset   s save   q quit")
    font = cv2.FONT_HERSHEY_SIMPLEX
    sizes = [cv2.getTextSize(t, font, 0.45, 1)[0] for t in (line1, line2)]
    panel_w = max(s[0] for s in sizes) + 16
    cv2.rectangle(img, (6, 6), (6 + panel_w, 6 + 18 * 2 + 8), (0, 0, 0), -1)
    y = 6 + 8 + sizes[0][1]
    for t in (line1, line2):
        cv2.putText(img, t, (14, y), font, 0.45, (220, 220, 220), 1, cv2.LINE_AA)
        y += 18


def render():
    img = read_video_frame(state["vf"])
    h, w = img.shape[:2]
    for det in get_dets(src_idx_now()):
        draw_box(img, det, w, h)
    draw_overlay(img)
    return img


def save_aligned(out_path):
    if state["S"] is None:
        print("Nothing to save yet — align the boxes and press 'f' to SET first.")
        return
    data = state["data"]
    n = state["N"]
    S = state["S"]
    base = int(data.get("phase_offset", 0))

    def rekey(m):
        return {str((int(k) + S) % n): v for k, v in m.items()} if n else dict(m)

    out = dict(data)
    out["frames"] = rekey(data.get("frames", {}))
    if data.get("alerts"):
        out["alerts"] = rekey(data["alerts"])
    if data.get("counts"):
        out["counts"] = rekey(data["counts"])
    out["phase_offset"] = (base + S) % n if n else base + S
    out["aligned_by"] = "align_phase"
    Path(out_path).write_text(json.dumps(out, indent=2))
    print(f"saved aligned JSON (S={S}, total phase_offset={out['phase_offset']}) -> {out_path}")
    print(f"  equivalent: 1_consolidate.py ... --phase_offset {out['phase_offset']}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--video", required=True, help="The ORIGINAL source video streamed in stage 1.")
    p.add_argument("--json", required=True, help="Consolidated tracking_stats predictions (from 1_consolidate.py).")
    p.add_argument("--meta", default=None, help="meta.json (optional; for n_source_frames).")
    p.add_argument("--out", default=None, help="Where to write the re-keyed JSON (default: <json>-aligned.json).")
    args = p.parse_args()

    data = json.loads(Path(args.json).read_text())
    data.setdefault("frames", {})
    data["class_names"] = ensure_loitering_class_names(data.get("class_names"))
    if data.get("detections_source") == "model":
        print("[WARN] this JSON was consolidated with --detections_source model; "
              "re-run 1_consolidate.py with the default (tracking_stats) for req-7 overlays.")

    state["data"] = data
    state["class_names"] = data["class_names"]
    state["alerts"] = data.get("alerts", {})
    state["samples"] = sorted(int(k) for k in data["frames"].keys())
    if not state["samples"]:
        sys.exit("ERROR: no frames in the JSON.")

    n_frames = int(data.get("n_frames") or 0)
    if args.meta and Path(args.meta).is_file():
        n_frames = int(json.loads(Path(args.meta).read_text()).get("n_source_frames") or n_frames)

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        sys.exit(f"ERROR: cannot open {args.video}")
    state["cap"] = cap
    state["n_video_frames"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    state["N"] = n_frames or state["n_video_frames"]
    if not state["N"]:
        sys.exit("ERROR: could not determine loop length N (no n_frames/meta/video count).")
    if state["n_video_frames"] and n_frames and state["n_video_frames"] != n_frames:
        print(f"[WARN] video has {state['n_video_frames']} frames but n_frames={n_frames}; "
              "is this the exact file that was streamed?")

    out_path = args.out or str(Path(args.json).with_name(Path(args.json).stem + "-aligned.json"))

    win = "align_phase"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cv2.resizeWindow(win, min(1280, w or 1280), min(720, h or 720))

    KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN = 2424832, 2555904, 2490368, 2621440
    try:
        while True:
            cv2.imshow(win, render())
            k = cv2.waitKeyEx(20)
            if k == -1:
                try:
                    if cv2.getWindowProperty(win, cv2.WND_PROP_VISIBLE) < 1:
                        break
                except cv2.error:
                    break
                continue
            ak = k & 0xFF
            if k == KEY_RIGHT or ak == ord('.'):
                move_video(1)
            elif k == KEY_LEFT or ak == ord(','):
                move_video(-1)
            elif k == KEY_UP:
                move_video(10)
            elif k == KEY_DOWN:
                move_video(-10)
            elif ak == ord(']'):
                move_video(100)
            elif ak == ord('['):
                move_video(-100)
            elif ak == ord('d'):
                move_detection(1)
            elif ak == ord('a'):
                move_detection(-1)
            elif ak == ord('c'):
                move_detection(10)
            elif ak == ord('z'):
                move_detection(-10)
            elif ak == ord('f'):
                toggle_set()
            elif ak == ord('r'):
                state["set_mode"] = False
            elif ak == ord('s'):
                save_aligned(out_path)
            elif ak == ord('q') or k == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    if state["S"] is not None:
        print(f"final S = {state['S']}  (total phase_offset would be "
              f"{(int(state['data'].get('phase_offset', 0)) + state['S']) % state['N']})")
    print("bye.")


if __name__ == "__main__":
    main()

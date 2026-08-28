"""
2_verify.py — verify / correct VMS predictions against the ORIGINAL video.

Unlike a normal frame-by-frame verifier, the VMS only processes a SUBSAMPLE of
the source video (every 3rd-4th frame), so this tool walks ONLY the frames that
were actually collected (the keys present in the consolidated JSON) and, for each
one, seeks the original source video to that TRUE source-frame index — read from
the key itself (= `src_idx` from section 1) — so the boxes land on the right
pixels.  `meta.json` (optional) supplies `n_source_frames` for the heads-up
display and a sanity check on coverage.

This is step 2 of section 2:  consolidate -> [verify] -> track.
You correct boxes and toggle `person` <-> `loitering_person` here; the saved JSON
is the ground truth fed to `3_track.py`.

Phase alignment (Case B)
------------------------
If stage-1 RTP ran continuously (no per-loop reset), `src_idx` is rotated from the
true video frame by an unknown CONSTANT S, so the boxes will not sit on people until
you set that offset.  Nudge it live (`,`/`.` `<`/`>` `[`/`]`) until the boxes line up
on any one frame — because S is constant, every frame lines up at once.  The chosen
offset is saved into the JSON (`view_phase_offset`) and reused next launch; pass the
SAME value to `3_track.py --phase-offset` for its overlay render.  Benchmarking is
unaffected (GT and predictions share the same src_idx keys either way).

Controls
--------
  <- / -> (or a / d) : prev / next SAMPLED frame
  + / -              : change the draw class (person <-> loitering_person)
  l                  : toggle class of the box under the mouse
  left-drag          : draw a new box (in the current draw class)
  right-click        : delete the box under the cursor
  , .  < >  [ ]      : phase align by -/+ 1, 25, 100 frames (find S once; it's constant)
  s                  : save     e : save + export annotated video     q / Esc : quit

Usage
-----
    python 2_verify.py --video path/to/test-vms-gt.mp4 --json vms-pred.json
    python 2_verify.py --video path/to/test-vms-gt.mp4 --json vms-pred.json --meta loitering-test/meta.json
    # phase shift (Case B) if you did NOT resolve it in 1_consolidate.py:
    python 2_verify.py --video gt.mp4 --json vms-pred.json --phase-offset 359
    # headless render of the saved boxes onto the sampled frames:
    python 2_verify.py --video gt.mp4 --json vms-pred.json --export out_annotated.mp4
"""

import argparse
import json
import sys
from pathlib import Path

import cv2

from loitering_common import (
    LOITERING_CLASS_ID,
    PERSON_CLASS_ID,
    clamp_class_id,
    ensure_loitering_class_names,
)

# BGR — interactive verify only
VERIFY_COLORS = {
    PERSON_CLASS_ID: (180, 50, 200),       # purple
    LOITERING_CLASS_ID: (0, 140, 255),     # orange
}


state = {
    "cap": None,
    "data": {},
    "samples": [],          # ordered list of source-frame indices that were collected
    "cur": 0,               # index INTO samples
    "phase_offset": 0,      # added to src_idx before seeking the video
    "n_source_frames": 0,
    "current_class": 0,
    "dirty": False,
    "drag_anchor": None,
    "drag_now": None,
    "json_path": "",
    "width": 0,
    "height": 0,
    "class_names": {},
    "alerts": {},
    "last_mouse": (0, 0),
}


def src_idx_now():
    return state["samples"][state["cur"]]


def _frame_span():
    """Number of frames in one loop of the source video (for phase wrap)."""
    return state["n_source_frames"] or state.get("n_video_frames") or 0


def video_frame_now():
    n = _frame_span()
    v = src_idx_now() + state["phase_offset"]
    return v % n if n else v


def adjust_phase(delta):
    """Nudge the constant Case-B rotation S used to seek the video (wraps mod N)."""
    n = _frame_span()
    state["phase_offset"] = (state["phase_offset"] + delta) % n if n else state["phase_offset"] + delta


def get_dets(src_idx):
    return state["data"]["frames"].setdefault(str(src_idx), [])


def color_for(cid):
    return VERIFY_COLORS.get(int(cid), VERIFY_COLORS[PERSON_CLASS_ID])


def class_label(cid):
    return state["class_names"].get(str(int(cid)), str(int(cid)))


def read_video_frame(video_frame_idx):
    cap = state["cap"]
    n = state["n_video_frames"]
    idx = max(0, min(n - 1, int(video_frame_idx))) if n else int(video_frame_idx)
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, frame = cap.read()
    if not ok:
        # fall back to a black canvas so the tool keeps working past the tail
        import numpy as np
        return np.zeros((state["height"], state["width"], 3), dtype="uint8")
    return frame


def draw_box(img, det, w, h):
    cid = int(det["class_id"])
    x1 = int(det["bbox"][0] * w)
    y1 = int(det["bbox"][1] * h)
    x2 = int(det["bbox"][2] * w)
    y2 = int(det["bbox"][3] * h)
    c = color_for(cid)
    cv2.rectangle(img, (x1, y1), (x2, y2), c, 2)
    label = class_label(cid)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale, thickness = 0.45, 1
    (tw, th), _ = cv2.getTextSize(label, font, scale, thickness)
    cv2.rectangle(img, (x1, max(0, y1 - th - 6)), (x1 + tw + 6, y1), c, -1)
    cv2.putText(img, label, (x1 + 3, max(th + 1, y1 - 4)), font, scale,
                (255, 255, 255), thickness, cv2.LINE_AA)


def draw_overlay(img):
    cur = state["cur"]
    total = len(state["samples"])
    cc = state["current_class"]
    sidx = src_idx_now()
    boxes = len(get_dets(sidx))
    dirty = " *" if state["dirty"] else ""
    has_alert = " [ALERT]" if state["alerts"].get(str(sidx)) else ""
    line1 = (f"sample {cur + 1}/{total}  src_idx={sidx}  video_frame={video_frame_now()}"
             f"  phase={state['phase_offset']}  |  draw: {class_label(cc)}  |  boxes: {boxes}{dirty}{has_alert}")
    line2 = ("<-/-> nav   +/- class   l toggle   drag draw   R del   s save   q quit"
             "   |   PHASE align: , . (1)  < > (25)  [ ] (100)")
    lines = (line1, line2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale, thickness, line_gap, pad = 0.45, 1, 18, 8
    sizes = [cv2.getTextSize(line, font, scale, thickness)[0] for line in lines]
    panel_w = max(s[0] for s in sizes) + pad * 2
    panel_h = line_gap * len(lines) + pad
    cv2.rectangle(img, (6, 6), (6 + panel_w, 6 + panel_h), (0, 0, 0), -1)
    y = 6 + pad + sizes[0][1]
    for line in lines:
        cv2.putText(img, line, (6 + pad, y), font, scale, (220, 220, 220),
                    thickness, cv2.LINE_AA)
        y += line_gap


def render_frame():
    img = read_video_frame(video_frame_now())
    h, w = img.shape[:2]
    for det in get_dets(src_idx_now()):
        draw_box(img, det, w, h)
    if state["drag_anchor"] is not None and state["drag_now"] is not None:
        ax, ay = state["drag_anchor"]
        bx, by = state["drag_now"]
        cv2.rectangle(img, (ax, ay), (bx, by), color_for(state["current_class"]), 2)
    draw_overlay(img)
    return img


def find_box_at(src_idx, x, y):
    boxes = get_dets(src_idx)
    w, h = state["width"], state["height"]
    cands = []
    for i, d in enumerate(boxes):
        x1, y1 = d["bbox"][0] * w, d["bbox"][1] * h
        x2, y2 = d["bbox"][2] * w, d["bbox"][3] * h
        if x1 <= x <= x2 and y1 <= y <= y2:
            cands.append(((x2 - x1) * (y2 - y1), i))
    if not cands:
        return -1
    cands.sort()
    return cands[0][1]


def on_mouse(event, x, y, flags, _userdata):
    state["last_mouse"] = (x, y)
    w, h = state["width"], state["height"]
    if event == cv2.EVENT_LBUTTONDOWN:
        state["drag_anchor"] = (x, y)
        state["drag_now"] = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and state["drag_anchor"] is not None:
        state["drag_now"] = (x, y)
    elif event == cv2.EVENT_LBUTTONUP and state["drag_anchor"] is not None:
        ax, ay = state["drag_anchor"]
        state["drag_anchor"] = None
        state["drag_now"] = None
        x1, x2 = sorted((ax, x))
        y1, y2 = sorted((ay, y))
        if x2 - x1 < 5 or y2 - y1 < 5:
            return
        x1, x2 = max(0, min(w, x1)), max(0, min(w, x2))
        y1, y2 = max(0, min(h, y1)), max(0, min(h, y2))
        get_dets(src_idx_now()).append({
            "class_id": int(state["current_class"]),
            "confidence": 1.0,
            "bbox": [x1 / w, y1 / h, x2 / w, y2 / h],
            "track_id": "-1",
        })
        state["dirty"] = True
    elif event == cv2.EVENT_RBUTTONDOWN:
        i = find_box_at(src_idx_now(), x, y)
        if i >= 0:
            del get_dets(src_idx_now())[i]
            state["dirty"] = True


def save_json():
    # Record the calibrated Case-B rotation so verify/track can reuse it and you
    # only have to find it once. Frame keys stay as src_idx (kept consistent with
    # the predictions file); this is a viewing offset, not a re-key.
    state["data"]["view_phase_offset"] = state["phase_offset"]
    Path(state["json_path"]).write_text(json.dumps(state["data"], indent=2))
    state["dirty"] = False


def ensure_opencv_gui():
    try:
        probe = "__opencv_gui_probe__"
        cv2.namedWindow(probe, cv2.WINDOW_NORMAL)
        cv2.destroyWindow(probe)
    except cv2.error:
        print(
            "ERROR: OpenCV in this environment has no GUI support.\n"
            "Interactive verify needs the opencv-python wheel, not opencv-python-headless.\n"
            "  python -m pip uninstall -y opencv-python-headless\n"
            "  python -m pip install --force-reinstall opencv-python",
            file=sys.stderr,
        )
        sys.exit(1)


def export_annotated(video_path, out_path):
    """Render saved boxes onto ONLY the sampled frames, written in sample order."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sys.exit(f"ERROR: cannot open {video_path}")
    fps = float(state["data"].get("fps") or cap.get(cv2.CAP_PROP_FPS) or 30.0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(str(out_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    if not writer.isOpened():
        cap.release()
        sys.exit(f"ERROR: cannot open writer for {out_path}")
    for sidx in state["samples"]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, sidx + state["phase_offset"])
        ok, frame = cap.read()
        if not ok:
            continue
        for det in get_dets(sidx):
            draw_box(frame, det, w, h)
        writer.write(frame)
    cap.release()
    writer.release()
    print(f"exported -> {out_path}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--video", required=True, help="ORIGINAL source video that was streamed in section 1.")
    p.add_argument("--json", required=True, help="Consolidated predictions JSON (from 1_consolidate.py).")
    p.add_argument("--meta", default=None, help="meta.json (optional; for n_source_frames + coverage check).")
    p.add_argument("--phase-offset", type=int, default=0,
                   help="Add this to each src_idx before seeking the video (Case B, if unresolved).")
    p.add_argument("--export", default=None,
                   help="If set, render saved boxes onto the sampled frames and exit (headless).")
    args = p.parse_args()

    data = json.loads(Path(args.json).read_text())
    data.setdefault("frames", {})
    data["class_names"] = ensure_loitering_class_names(data.get("class_names"))

    state["data"] = data
    state["json_path"] = args.json
    # CLI flag wins; else reuse a previously calibrated offset stored in the JSON.
    state["phase_offset"] = args.phase_offset or int(data.get("view_phase_offset", 0))
    state["class_names"] = data["class_names"]
    state["alerts"] = data.get("alerts", {})
    state["samples"] = sorted((int(k) for k in data["frames"].keys()))
    if not state["samples"]:
        sys.exit("ERROR: no frames in the predictions JSON — nothing to verify.")

    if args.meta and Path(args.meta).is_file():
        meta = json.loads(Path(args.meta).read_text())
        state["n_source_frames"] = int(meta.get("n_source_frames") or 0)
        covered = meta.get("source_frames_covered")
        if covered is not None and covered != len(state["samples"]):
            print(f"[WARN] meta says {covered} covered frames, JSON has "
                  f"{len(state['samples'])} — proceeding with the JSON.")

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        sys.exit(f"ERROR: cannot open {args.video}")
    state["cap"] = cap
    state["n_video_frames"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    state["width"], state["height"] = w, h
    data["width"], data["height"] = w, h

    if args.export:
        print(f"exporting sampled frames {args.video} -> {args.export} ...")
        export_annotated(args.video, args.export)
        cap.release()
        return

    print(f"opening {args.video}  ({len(state['samples'])} sampled frames, "
          f"video has {state['n_video_frames']} frames) ...", flush=True)
    ensure_opencv_gui()
    win = "verify"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win, min(1280, w), min(720, h))
    cv2.setMouseCallback(win, on_mouse)

    KEY_LEFT, KEY_RIGHT = 2424832, 2555904
    try:
        while True:
            cv2.imshow(win, render_frame())
            k = cv2.waitKeyEx(20)
            if k == -1:
                try:
                    if cv2.getWindowProperty(win, cv2.WND_PROP_VISIBLE) < 1:
                        break
                except cv2.error:
                    break
                continue
            ascii_k = k & 0xFF
            if k == KEY_LEFT or ascii_k == ord('a'):
                state["cur"] = max(0, state["cur"] - 1)
                state["drag_anchor"] = state["drag_now"] = None
            elif k == KEY_RIGHT or ascii_k == ord('d'):
                state["cur"] = min(len(state["samples"]) - 1, state["cur"] + 1)
                state["drag_anchor"] = state["drag_now"] = None
            elif ascii_k in (ord('+'), ord('=')):
                state["current_class"] = clamp_class_id(state["current_class"] + 1)
            elif ascii_k in (ord('-'), ord('_')):
                state["current_class"] = clamp_class_id(state["current_class"] - 1)
            elif ascii_k == ord(','):
                adjust_phase(-1)
            elif ascii_k == ord('.'):
                adjust_phase(1)
            elif ascii_k == ord('<'):
                adjust_phase(-25)
            elif ascii_k == ord('>'):
                adjust_phase(25)
            elif ascii_k == ord('['):
                adjust_phase(-100)
            elif ascii_k == ord(']'):
                adjust_phase(100)
            elif ascii_k == ord('l'):
                mx, my = state["last_mouse"]
                i = find_box_at(src_idx_now(), mx, my)
                if i >= 0:
                    d = get_dets(src_idx_now())[i]
                    d["class_id"] = (LOITERING_CLASS_ID
                                     if int(d["class_id"]) == PERSON_CLASS_ID
                                     else PERSON_CLASS_ID)
                    state["dirty"] = True
            elif ascii_k == ord('s'):
                save_json()
                print("saved")
            elif ascii_k == ord('e'):
                save_json()
                out = Path(args.video).with_name(Path(args.video).stem + "_annotated.mp4")
                export_annotated(args.video, out)
            elif ascii_k == ord('q') or k == 27:
                break
    finally:
        save_json()
        cap.release()
        cv2.destroyAllWindows()
    print("bye.")


if __name__ == "__main__":
    main()

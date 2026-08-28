"""
prepare_gt_video.py — probe the ORIGINAL GT video for rtp-based collection.

The old silence/marker/buffer/end-gate wrapping is GONE.  The media server streams
the raw file as a looping RTSP camera (`ffmpeg -re -stream_loop -1 ... -c:v copy`)
and `redis_gt_collect.py` aligns each output to its source frame via rtp_timestamp
and the video's PTS table — no in-band markers are needed.

This tool just inspects the raw video and prints the values the collector needs:
frame count (N), fps, per-frame tick interval, and the loop span in ticks/seconds.
Point the media-server FILE camera at this same raw file.

Usage
-----
    python prepare_gt_video.py --input path/to/gt_content.mp4
"""

import argparse
import sys

from rtp_map import RTP_CLOCK_HZ, build_pts_reference


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", required=True, help="The raw GT video to stream and collect against.")
    args = p.parse_args()

    try:
        ref = build_pts_reference(args.input)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    diffs = [b - a for a, b in zip(ref.pts_ticks, ref.pts_ticks[1:])]
    cfr = len(set(diffs)) <= 1
    span_s = ref.loop_span_ticks / RTP_CLOCK_HZ

    print("=" * 60)
    print(f"  Video            : {args.input}")
    print(f"  Source frames N  : {ref.n_frames}")
    print(f"  FPS              : {ref.fps:.3f}")
    print(f"  Frame interval   : {ref.frame_interval_ticks} ticks @ {RTP_CLOCK_HZ} Hz")
    print(f"  Timing           : {'constant (CFR)' if cfr else 'variable (VFR) — PTS table used'}")
    print(f"  Loop span        : {ref.loop_span_ticks} ticks  ({span_s:.3f} s)")
    print("=" * 60)
    print("  Stream this raw file via the media-server FILE camera, then:")
    print("    export GT_SOURCE_VIDEO=" + args.input)
    print("    python3 redis_gt_collect.py")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
import logging
import sys

from rtp_map import RTP_CLOCK_HZ, build_pts_reference

_logger = logging.getLogger(__name__)


def _configure_cli_logging() -> None:
    """Send the report to stdout and errors to stderr, with no log decoration.

    This tool's stdout IS its product, so the handler uses a bare "%(message)s"
    formatter: the bytes on stdout are identical to the print() calls this
    replaced. Configured here rather than at import so importing the module
    stays side-effect free.
    """
    if _logger.handlers:
        return
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.INFO)
    out.addFilter(lambda record: record.levelno < logging.ERROR)
    out.setFormatter(logging.Formatter("%(message)s"))
    err = logging.StreamHandler(sys.stderr)
    err.setLevel(logging.ERROR)
    err.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(out)
    _logger.addHandler(err)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--input", required=True, help="The raw GT video to stream and collect against.")
    args = p.parse_args()
    _configure_cli_logging()

    try:
        ref = build_pts_reference(args.input)
    except RuntimeError as exc:
        _logger.error("ERROR: %s", exc)
        return 1

    # strict=False on purpose: the second sequence is the first offset by one,
    # so it is always one shorter and that defines the pair count.
    diffs = [b - a for a, b in zip(ref.pts_ticks, ref.pts_ticks[1:], strict=False)]
    cfr = len(set(diffs)) <= 1
    span_s = ref.loop_span_ticks / RTP_CLOCK_HZ

    _logger.info("%s", "=" * 60)
    _logger.info("  Video            : %s", args.input)
    _logger.info("  Source frames N  : %s", ref.n_frames)
    _logger.info("  FPS              : %.3f", ref.fps)
    _logger.info("  Frame interval   : %s ticks @ %s Hz", ref.frame_interval_ticks, RTP_CLOCK_HZ)
    _logger.info(
        "  Timing           : %s",
        "constant (CFR)" if cfr else "variable (VFR) — PTS table used",
    )
    _logger.info("  Loop span        : %s ticks  (%.3f s)", ref.loop_span_ticks, span_s)
    _logger.info("%s", "=" * 60)
    _logger.info("  Stream this raw file via the media-server FILE camera, then:")
    _logger.info("%s", "    export GT_SOURCE_VIDEO=" + args.input)
    _logger.info("    python3 redis_gt_collect.py")
    _logger.info("%s", "=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

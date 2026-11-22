/* teleop-track.js — a robot's cameras on this page as native WebRTC video tracks (the only path now): each camera a
   <video> the browser plays, and the frame on the screen found exactly by the RTP timestamp its vm message carries.

   In one sentence: the console offers a fixed 8 recvonly video transceivers → the robot fills one per camera in the order
   they first appear and names each on seq-ctl (`vm`, with its RTP timestamp) → each track becomes a <video>, and
   requestVideoFrameCallback on it reads the frame now on the screen, looks its `n` and capture time up by that frame's
   RTP timestamp, and tells the connection — for frame_us (glass to glass) and for the frame a command is made from.

   WHY the RTP timestamp, not the newest vm: a vm on seq-ctl can reach the page before its frame is shown, so the newest
   one is a frame the person has not seen yet. The frame the browser shows carries its own RTP timestamp
   (requestVideoFrameCallback's metadata), and the vm says which `n` and capture time that timestamp is: an exact pair, so
   `ref_us` / `ref_n` and `frame_us` are the frame on the screen, never a later one.

   WHY a fixed 8: the console cannot know how many cameras before it offers, so it offers 8 and the robot fills what it
   has; an unfilled transceiver never carries a track and costs nothing (no inbound-rtp stat until media arrives, measured
   Chrome 157).

   CSP / injection: a track plays on a <video>; a camera's name (the robot's) reaches the page only as text. */

import { nowUs } from '/assets/teleop-wire.js';

export const MAX_CAMERAS = 8;         // the console offers this many recvonly video transceivers
const H264 = /^video\/H264$/i;

/* This browser's receive codecs with only H.264 kept, for setCodecPreferences: 8 recvonly transceivers are ~47 KB of SDP
   with every codec and ~26 KB H.264-only, and the robot encodes H.264 regardless. null where the browser does not say. */
export function h264Only() {
  if (typeof RTCRtpReceiver !== 'function' || typeof RTCRtpReceiver.getCapabilities !== 'function') return null;
  const caps = RTCRtpReceiver.getCapabilities('video');
  const only = ((caps && caps.codecs) || []).filter((c) => H264.test(c.mimeType));
  return only.length ? only : null;
}

/* The video frames the browser shows for the robot's cameras, paired to their `n` and capture time. `onCamera(key, video)`
   a camera seen first; `onShown(n, tUs)` the newest frame on the screen; `offset()` the robot's clock less this one's, or
   null; `stats` the connection's measures; `trace()` its trace callback or null; `video()` a <video> maker (a test's fake). */
export class Tracks {
  constructor({ onCamera, onShown, offset, stats, trace, video }) {
    this.onCamera = onCamera;
    this.onShown = onShown;
    this.offset = offset;
    this.stats = stats;
    this.trace = trace;
    this.makeVideo = video || (() => document.createElement('video'));
    this.cams = new Map();            // i -> { key, video, byRtp: Map(rtp -> {n, tUs}), started }
    this.stashed = new Map();         // i -> MediaStream, a track that arrived before its first vm
    this.closed = false;
  }

  /* One camera's working state, made on its first vm or first track. */
  cam(i) {
    let c = this.cams.get(i);
    if (!c) { c = { key: null, video: null, byRtp: new Map(), started: false }; this.cams.set(i, c); }
    return c;
  }

  /* A received track (pc.ontrack): held by its transceiver's m-line index until a vm names its camera. */
  onTrack(stream, i) {
    if (this.closed || !Number.isInteger(i)) return;
    this.stashed.set(i, stream);
    if (this.cams.has(i) && this.cams.get(i).key !== null) this.attach(i);
  }

  /* A vm message on seq-ctl: which camera track i is, and what `n` / capture time a given RTP timestamp is. */
  vm(m) {
    if (this.closed || !Number.isInteger(m.i)) return;
    const c = this.cam(m.i);
    if (c.key === null && m.key != null) c.key = String(m.key);
    if (Number.isInteger(m.rtp)) {
      c.byRtp.set(m.rtp >>> 0, { n: Number.isInteger(m.n) ? m.n : null, tUs: Number.isInteger(m.capture_us) ? m.capture_us : null });
      if (c.byRtp.size > 600) c.byRtp.delete(c.byRtp.keys().next().value);
    }
    if (!c.video && c.key !== null && this.stashed.has(m.i)) this.attach(m.i);
  }

  /* Its track and a vm both here: its <video> made, handed to the page, and its frames read. */
  attach(i) {
    const c = this.cams.get(i);
    const stream = this.stashed.get(i);
    if (!c || c.video || !stream) return;
    const video = this.makeVideo();
    video.autoplay = true;
    video.muted = true;
    video.playsInline = true;
    try { video.srcObject = stream; } catch (_) { /* a test's fake takes the stream its own way */ }
    c.video = video;
    this.onCamera(c.key || `camera ${i}`, video);
    this.read(i, c, video);
  }

  /* Each frame the browser shows for camera i (requestVideoFrameCallback): no buffer of ours, a person drives from it. */
  read(i, c, video) {
    if (c.started || typeof video.requestVideoFrameCallback !== 'function') return;
    c.started = true;
    const onFrame = (now, md) => {
      if (this.closed || !this.cams.has(i)) return;
      this.shown(c, now, md);
      video.requestVideoFrameCallback(onFrame);
    };
    video.requestVideoFrameCallback(onFrame);
  }

  /* One frame on the screen: its `n` and capture time found by its RTP timestamp, its glass-to-glass timed, the newest
     told to the connection. A frame whose vm never came (seq-ctl dropped it) is shown but cannot be placed. */
  shown(c, now, md) {
    const rtp = md && Number.isInteger(md.rtpTimestamp) ? (md.rtpTimestamp >>> 0) : null;
    const hit = rtp !== null ? c.byRtp.get(rtp) : undefined;
    if (!hit) return;
    const shownUs = Math.floor((performance.timeOrigin + (md && Number.isFinite(md.presentationTime) ? md.presentationTime : now)) * 1000);
    const off = this.offset();
    if (Number.isInteger(hit.tUs) && off !== null) this.stats.sample('frame_us', shownUs - (hit.tUs - off));
    if (Number.isInteger(hit.n)) this.onShown(hit.n, hit.tUs);
    const trace = this.trace && this.trace();
    if (trace) trace({ kind: 'frame', n: hit.n, t_us: hit.tUs, off_us: off, decoded_us: null, shown_us: shownUs });
  }

  close() {
    this.closed = true;
    for (const c of this.cams.values()) {
      if (c.video) { try { c.video.srcObject = null; } catch (_) { /* a fake with none */ } }
    }
    this.cams.clear();
    this.stashed.clear();
  }
}

/* How many video frames a getStats report holds received and dropped, summed over its inbound-rtp video entries: the
   browser's own count, which the connection reads into frames_received / frames_dropped (a native track's jitter buffer
   and decoder are the browser's, so only it knows what it dropped). A pure function, so node checks it. */
export function framesOf(report) {
  let received = 0;
  let dropped = 0;
  report.forEach((r) => {
    if (r.type === 'inbound-rtp' && (r.kind === 'video' || r.mediaType === 'video')) {
      received += r.framesDecoded || 0;
      dropped += r.framesDropped || 0;
    }
  });
  return { received, dropped };
}

export { nowUs };

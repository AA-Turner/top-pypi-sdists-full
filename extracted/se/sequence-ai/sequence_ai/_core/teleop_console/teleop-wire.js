/* teleop-wire.js — the parts of a direct connection to a robot that are arithmetic, with nothing of the browser's in them, so
   node checks each against the SDK (tools/check/test_teleop_wire.mjs): the channels' settings, a message in pieces and back, the
   paced sending side, the two clocks and the latency figures.

   In one sentence: a message goes out as pieces of at most 16 KB each behind an 8-byte head, handed on only while the channel
   holds little unsent → the other side puts them back in any order → ticks and tocks tell how far the robot's clock is from this
   one → every latency goes into a window of its newest 256 samples, read as nearest-rank percentiles.

   WHY all of it as the SDK does it: the robot is the SDK, and its code is the rule.

   WHY the numbers come out the same as Python's: a bench reads these beside the Python console's, and a percentile of
   one reads against the other only if it is the same one. */

/* Each channel by label: a command and a clock's tick are worth nothing late and are never sent again; a camera frame may be
   sent again while it can still arrive in time; who drives is reliable and in order, a stop being not to be lost. */
export const CHANNELS = {
  'seq-cmd': { ordered: false, maxRetransmits: 0 },
  'seq-ctl': { ordered: false, maxRetransmits: 0 },
  'seq-state': { ordered: false, maxRetransmits: 0 },
  'seq-video': { ordered: false, maxPacketLifeTime: 150 },
  'seq-who': {},
};

const HEAD = 8;                       // a piece's head: its message's number (u32), its index (u16), how many pieces (u16)
export const PIECE_BYTES = 16 * 1024;
export const HIGH_BYTES = 64 * 1024;  // pieces are handed to the channel while it holds less than this unsent
export const LOW_BYTES = 32 * 1024;   // and again as it drains below this
// Messages waiting on a channel, not yet begun, past which the oldest is dropped: a newer command makes an older one no use.

const QUEUED = { 'seq-state': 1, 'seq-video': 3, 'seq-cmd': 1, 'seq-ctl': 64, 'seq-who': 1 << 16 };
const PARTIALS = 32;                  // messages whose pieces are still coming, past which the oldest is dropped
const PARTIAL_MS = 2000;              // or once older than this

/* This machine's clock as every time on the wire is written: whole microseconds since the epoch. */
export const nowUs = () => Math.floor((performance.timeOrigin + performance.now()) * 1000);

/* `data` as the pieces message `number` goes in: each its head and at most PIECE_BYTES of it. */
export function pieces(number, data) {
  const count = Math.max(1, Math.ceil(data.length / PIECE_BYTES));
  if (count > 0xffff) throw new Error(`a message of ${data.length} bytes is past what one goes in`);
  const out = [];
  for (let i = 0; i < count; i += 1) {
    const body = data.subarray(i * PIECE_BYTES, (i + 1) * PIECE_BYTES);
    const piece = new Uint8Array(HEAD + body.length);
    const view = new DataView(piece.buffer);
    view.setUint32(0, number >>> 0);
    view.setUint16(4, i);
    view.setUint16(6, count);
    piece.set(body, HEAD);
    out.push(piece);
  }
  return out;
}

/* One channel's pieces put back together as they come, in any order: a message whole once its every piece is here; one whose
   pieces stopped coming is dropped. */
export class Assembly {
  constructor() {
    this.partial = new Map();         // number -> { count, got: Map(index -> bytes), at }
    this.dropped = 0;                 // messages given up on: a piece never came
  }

  /* One piece: the message it completes, else null. A piece that does not read is dropped. */
  add(piece, now = performance.now()) {
    if (piece.length < HEAD) return null;
    const view = new DataView(piece.buffer, piece.byteOffset, piece.byteLength);
    const number = view.getUint32(0);
    const index = view.getUint16(4);
    const count = view.getUint16(6);
    if (!count || index >= count) return null;
    const body = piece.subarray(HEAD);
    if (count === 1) return body;     // one piece: whole as it is
    let got = this.partial.get(number);
    if (!got || got.count !== count) {
      got = { count, got: new Map(), at: now };
      this.partial.set(number, got);
    }
    got.got.set(index, body);
    if (got.got.size === count) {
      this.partial.delete(number);
      let size = 0;
      for (const b of got.got.values()) size += b.length;
      const whole = new Uint8Array(size);
      let at = 0;
      for (let i = 0; i < count; i += 1) {
        const b = got.got.get(i);
        whole.set(b, at);
        at += b.length;
      }
      return whole;
    }
    this.prune(now);
    return null;
  }

  /* Messages whose pieces stopped coming: any past PARTIAL_MS, the oldest past PARTIALS. */
  prune(now) {
    for (const [number, p] of this.partial) {
      if (now - p.at > PARTIAL_MS) {
        this.partial.delete(number);
        this.dropped += 1;
      }
    }
    while (this.partial.size > PARTIALS) {
      let oldest = null;
      for (const [number, p] of this.partial) if (oldest === null || p.at < this.partial.get(oldest).at) oldest = number;
      this.partial.delete(oldest);
      this.dropped += 1;
    }
  }
}

/* One channel's sending side, paced: messages queued whole and handed on a piece at a time while the channel holds little
   unsent, so a command waits behind one piece at most; the oldest not yet begun dropped past QUEUED. */
export class Sender {
  constructor(channel) {
    this.channel = channel;
    this.most = QUEUED[channel.label] ?? 8;
    this.queue = [];                  // [pieces, next index]
    this.number = 0;
    this.dropped = 0;
    channel.bufferedAmountLowThreshold = LOW_BYTES;
    channel.onbufferedamountlow = () => this.pump();
  }

  put(data) {
    this.queue.push([pieces(this.number, data), 0]);
    this.number = (this.number + 1) >>> 0;
    // one half sent is finished: its receiver holds its first pieces
    const begun = this.queue[0][1] > 0 ? 1 : 0;
    while (this.queue.length - begun > this.most) {
      this.queue.splice(begun, 1);    // the oldest not begun, never the one just queued
      this.dropped += 1;
    }
    this.pump();
  }

  pump() {
    if (this.channel.readyState !== 'open') return;
    while (this.queue.length && this.channel.bufferedAmount < HIGH_BYTES) {
      const head = this.queue[0];
      this.channel.send(head[0][head[1]]);
      head[1] += 1;
      if (head[1] === head[0].length) this.queue.shift();
    }
  }
}

const ROUNDS = 16;                    // the rounds the offset is chosen from, about eight seconds of ticks
const FIRST_TICKS = 5;                // so a command's age is known within a second of connecting
const FIRST_TICK_MS = 50;
const TICK_MS = 500;

/* Whole microseconds a message carried, or null for anything else. */
const micros = (v) => (Number.isInteger(v) ? v : null);

/* The robot's clock as this console reads it: of the last ROUNDS ticks the one with the shortest trip, whose offset is off by
   at most half that trip. */
export class Clock {
  constructor() {
    this.rounds = [];                 // [trip, offset] of the newest rounds, in microseconds
    this.ticks = 0;
  }

  tick(now = nowUs()) {
    this.ticks += 1;
    return { t: 'tick', a_us: now };
  }

  // milliseconds until the next tick
  due() { return this.ticks < FIRST_TICKS ? FIRST_TICK_MS : TICK_MS; }

  /* The robot's tock, come at `at`: one round kept, its trip in microseconds; times that do not read or cannot be: null. */
  tock(message, at = nowUs()) {
    const a = micros(message.a_us);
    const b = micros(message.b_us);
    const c = micros(message.c_us);
    if (a === null || b === null || c === null) return null;
    const trip = (at - a) - (c - b);
    if (trip < 0) return null;        // a clock stepped mid-round
    this.rounds.push([trip, Math.floor(((b - a) + (c - at)) / 2)]);
    if (this.rounds.length > ROUNDS) this.rounds.shift();
    return trip;
  }

  // the round with the shortest trip, and of those the smallest offset, as Python's min() of a tuple
  best() {
    let out = null;
    for (const r of this.rounds) if (!out || r[0] < out[0] || (r[0] === out[0] && r[1] < out[1])) out = r;
    return out;
  }

  get offsetUs() { const r = this.best(); return r ? r[1] : null; }

  get errorUs() { const r = this.best(); return r ? Math.floor(r[0] / 2) : null; }
}

const WINDOW = 256;
// Each percentile, and the samples its window must hold first: below that it would be the window's max, not a percentile.
const PERCENTILES = [[50, 2], [95, 20], [99, 100]];

/* Python's round(): half to even, so a mean reads the same on both sides. */
function roundHalfEven(x) {
  const r = Math.round(x);
  return Math.abs(x % 1) === 0.5 && r % 2 !== 0 ? r - 1 : r;
}

/* The q-th percentile of `ordered`, sorted: the ceil(q/100 * n)-th smallest. */
export function nearestRank(ordered, q) {
  if (!ordered.length) return null;
  return ordered[Math.max(0, Math.ceil((q * ordered.length) / 100) - 1)];
}

/* One latency's newest WINDOW samples, written over the oldest. */
class Window {
  constructor() {
    this.values = new Float64Array(WINDOW);
    this.n = 0;
    this.at = 0;
    this.sum = 0;
    this.last = null;
    this.total = 0;
  }

  add(us) {
    if (this.n === WINDOW) this.sum -= this.values[this.at];
    else this.n += 1;
    this.values[this.at] = us;
    this.sum += us;
    this.at = (this.at + 1) % WINDOW;
    this.last = us;
    this.total += 1;
  }

  read() {
    const ordered = Array.from(this.values.subarray(0, this.n)).sort((a, b) => a - b);
    const out = { n: this.n, total: this.total, last: this.last, mean: this.n ? roundHalfEven(this.sum / this.n) : null,
      max: ordered.length ? ordered[ordered.length - 1] : null };
    for (const [q, floor] of PERCENTILES) out[`p${q}`] = this.n >= floor ? nearestRank(ordered, q) : null;
    return out;
  }
}

/* A console's measures, declared so a snapshot holds every one from the start. */
const CONSOLE = {
  counters: ['commands_sent', 'commands_unanswered', 'frames_received', 'frames_dropped', 'frames_expired', 'states_received'],
  gauges: ['clock_offset_us', 'clock_uncertainty_us'],
  latencies: ['command_us', 'rtt_us', 'frame_us', 'state_us', 'input_us'],
};

/* A connection's counters, gauges and latencies, read at once: the shape of the Python console's metrics(). */
export class Stats {
  constructor() {
    this.counters = Object.fromEntries(CONSOLE.counters.map((n) => [n, 0]));
    this.gauges = Object.fromEntries(CONSOLE.gauges.map((n) => [n, null]));
    this.windows = Object.fromEntries(CONSOLE.latencies.map((n) => [n, new Window()]));
  }

  count(name, n = 1) { this.counters[name] = (this.counters[name] || 0) + n; }

  gauge(name, value) { this.gauges[name] = value; }

  sample(name, us) {
    if (!Number.isFinite(us)) throw new Error(`a latency is a finite number of microseconds, not ${us}`);
    (this.windows[name] ||= new Window()).add(roundHalfEven(us));
  }

  snapshot() {
    return { counters: { ...this.counters }, gauges: { ...this.gauges },
      latency_us: Object.fromEntries(Object.entries(this.windows).map(([k, w]) => [k, w.read()])) };
  }
}

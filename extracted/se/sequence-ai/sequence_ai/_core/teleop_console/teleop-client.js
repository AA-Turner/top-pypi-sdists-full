/* teleop-client.js — this browser connected straight to a robot (WebRTC): the console side of a direct teleoperation connection,
   what sequence_ai.teleop() is in Python.

   In one sentence: connect() makes the five channels, offers (POST /v1/teleop/offer, naming the robot) and waits for the
   robot's answer (GET /v1/teleop/pairing/{id}, long-polled) → the two meet, or it fails saying why, and nothing goes any other way →
   on the reliable channel the robot says who drives; take(), release() and stop() are each said and answered with who drives then,
   a heartbeat every 0.5 s (a driving console silent for 3 s stops its robot) → send(chunk) goes at once, numbered and timed, the
   chunk as it was given → the robot's cameras are native video tracks drawn by teleop-track.js, and metrics() says how late everything was.

   WHY the platform sees only the first words: a person's pictures and commands go straight to the robot and reach no server of
   ours; the platform hands over each side's connection details once and deletes them.

   WHY no way around a pair that cannot meet: a console that silently went another way would drive at a latency its person never
   chose.
   WHY the chunk is not looked at: what a person sends is theirs, in the form their policy's answers have.

   Everything the robot says is data: it is read by msgpack (no extension types) and reaches the page only as text. */

import { pack, unpack } from '/assets/msgpack.js';
import { Assembly, CHANNELS, Clock, Sender, Stats, nowUs } from '/assets/teleop-wire.js';
import { MAX_CAMERAS, Tracks, framesOf, h264Only } from '/assets/teleop-track.js';

const OFFER = '/v1/teleop/offer';
const PAIRING = '/v1/teleop/pairing/';
// A round of asking for the robot's answer, in seconds: under the 20 s gatewayGet gives any request, so a round that waits its full
// time still comes back as an answer rather than an aborted request.
const PAIRING_WAIT_S = 15;
const CONNECT_MS = 30000;             // the whole of it: the offer, the robot's answer, the two meeting and its first word
// How long the checks may go with no pair answering before the two are taken to have no way to each other: a firewall or a NAT that
// keeps them apart drops every check, and a browser may wait out CONNECT_MS before it says so (the Python console's DIRECT_S).
const DIRECT_MS = 5000;
const CHECKING = ['new', 'checking'];
const GATHER_MS = 5000;               // how long this side's addresses are gathered for before the offer goes with what it has
const HEARTBEAT_MS = 500;
const SAY_MS = 5000;                  // how long a take, release or stop waits for the robot's answer
const LOST_AFTER_MS = 2000;           // a command with no receipt past this is counted lost
const PENDING_KEPT = 4096;
// The two STUN servers under our own domain: the first is the address the connection is found by, the two together tell a NAT that
// gives each peer a port of its own (natOf), as the robot's STUN and STUN_SECOND do.
const STUN = ['stun:stun.generalsequences.com:3478', 'stun:stun2.generalsequences.com:3478'];

/* A failure with the reason a program switches on, the gateway's answer where it was the gateway's, and - where the two
   networks kept the console and its robot apart - each side's NAT and how far the connection got (`details`, as the Python
   console's Unavailable.details). */
export class TeleopError extends Error {
  constructor(message, reason, response = null, details = null) {
    super(message);
    this.name = 'TeleopError';
    this.reason = reason;
    this.response = response;
    this.details = details;
  }
}

/* An SDP's candidate lines as { kind, address, port }. */
function candidates(sdp) {
  const out = [];
  for (const line of (sdp || '').split(/\r?\n/)) {
    if (!line.startsWith('a=candidate:')) continue;
    const parts = line.split(' ');
    const at = parts.indexOf('typ');
    out.push({ line, kind: at >= 0 ? parts[at + 1] : null, address: parts[4], port: parts[5] });
  }
  return out;
}

/* `sdp` with every candidate but host and server-reflexive ones taken out, a relay's above all. */
export function onlyHostSrflx(sdp) {
  return keptCandidates(sdp, false);
}

/* `sdp` with the candidates a side may use: host and server-reflexive, and a TURN server's relayed ones where its server
   named one and this console takes a relay (`relay`). */
export function keptCandidates(sdp, relay) {
  const kinds = relay ? ['host', 'srflx', 'relay'] : ['host', 'srflx'];
  const kept = [];
  for (const line of (sdp || '').split(/\r?\n/)) {
    if (line === '') continue;
    if (line.startsWith('a=candidate:')) {
      const c = candidates(line)[0];
      if (!kinds.includes(c.kind)) continue;
    }
    kept.push(line);
  }
  return `${kept.join('\r\n')}\r\n`;
}

/* Which way a connection went, from its getStats report: "relay" where the pair its ICE chose goes through a TURN server,
   else "direct". The transport's selected pair, else a nominated pair that succeeded. */
export function pathOf(report) {
  const byId = new Map();
  let chosen = null;
  report.forEach((s) => {
    byId.set(s.id, s);
    if (s.type === 'transport' && s.selectedCandidatePairId) chosen = s.selectedCandidatePairId;
  });
  let pair = chosen ? byId.get(chosen) : null;
  if (!pair) report.forEach((s) => { if (!pair && s.type === 'candidate-pair' && s.nominated && s.state === 'succeeded') pair = s; });
  if (!pair) return 'direct';
  const kinds = [byId.get(pair.localCandidateId), byId.get(pair.remoteCandidateId)].map((c) => c && c.candidateType);
  return kinds.includes('relay') ? 'relay' : 'direct';
}

/* The kinds of candidate `sdp` offers, each once, sorted. */
export const candidateTypes = (sdp) => [...new Set(candidates(sdp).map((c) => c.kind).filter(Boolean))].sort();

/* What NAT this browser is behind, from the server-reflexive candidates its offer holds: asked of two STUN servers from one socket,
   one public port is a NAT a pair can meet through, two are a port of its own for each peer. A page cannot open a socket and ask as
   teleop_direct.nat_probe does, and these candidates say the same. `unnamed`: no STUN server's name resolved, which says nothing of
   its NAT. */
export function natOf(sdp, unnamed = false) {
  const seen = candidates(sdp).filter((c) => c.kind === 'srflx');
  if (!seen.length) return { kind: unnamed ? 'unknown' : 'no_udp', public: null };
  const ports = new Set(seen.map((c) => `${c.address}:${c.port}`));
  return { kind: ports.size > 1 ? 'dependent' : 'independent', public: seen[0].address };
}

/* What stopped a direct connection, from each side's NAT and how far it got, in words that name no address and no provider and say
   what happened, not how it was told: each follows "no direct connection to the robot: ", word for word teleop_direct.why_not's. */
export function whyNot(mine, theirs, facts) {
  const m = mine || {};
  const t = theirs || {};
  const ice = facts.ice === 'completed' || facts.ice === 'connected';
  if (ice && facts.dtls !== 'connected' && facts.dtls !== null && facts.dtls !== undefined) {
    return 'the robot\'s certificate did not match, so the connection was refused';
  }
  if (ice) return 'the two connected, but the data channels did not open in time';
  return apart(m, t, facts, false);
}

/* Why a connection went through a relay and not straight to the robot, from each side's NAT and the candidates each offered:
   what whyNot says of a pair that had no relay (teleop_direct.why_relayed). */
export function whyRelayed(mine, theirs, facts) {
  return apart(mine || {}, theirs || {}, facts || {}, true);
}

/* What kept the two apart, by their NATs: the same words whether that failed the connection or sent it through a relay, but for
   what then became of it. */
function apart(m, t, facts, relayed) {
  const kinds = [m.kind, t.kind];
  if (kinds.includes('no_udp')) {
    const side = kinds[0] === 'no_udp' ? 'this machine\'s' : 'the robot\'s';
    return `${side} network blocks outgoing UDP${relayed ? ', so the relay carried it over TCP' : ''}`;
  }
  if (m.public && m.public === t.public && (facts.mine || []).includes('host') && (facts.theirs || []).includes('host')) {
    return 'both are on the same network, but it keeps devices apart (client isolation) or a firewall drops UDP';
  }
  if (kinds[0] === 'dependent' && kinds[1] === 'dependent') {
    return `both are behind symmetric NATs, so neither can reach the other${relayed ? ' directly' : ''}`;
  }
  if (kinds.includes('dependent')) {
    const side = kinds[0] === 'dependent' ? 'this machine\'s' : 'the robot\'s';
    // through a relay no more is known: the other side most likely let in no packet it did not ask for, but a direct way slower than
    // the Python console's RELAY_GRACE_S, or a browser's own choice, goes through the relay as well
    if (relayed) return `${side} NAT is symmetric`;
    return `${side} NAT is symmetric, and the other side blocks unsolicited packets`;
  }
  return `a firewall between the two networks blocks ${relayed ? 'direct UDP' : 'UDP'}`;
}

const isMap = (v) => v !== null && typeof v === 'object' && !Array.isArray(v) && !(v instanceof Uint8Array);

/* One console's connection to one robot. `robot` its name; `operator` the name this console goes by. `gateway` { send, get }: as
   gateway.js's gatewaySend and gatewayGet answer ({status, body}). `on`: { driver(state), receipt(id, did, oneWayUs), ended(why),
   camera(path, canvas) }, each optional. `rtc`, `cameras`: a test's fakes. */
export class TeleopClient {
  constructor({ robot, operator, gateway, on = {}, rtc = globalThis.RTCPeerConnection, cameras = {}, iceServers = [],
    directOnly = false }) {
    this.iceServers = Array.isArray(iceServers) ? iceServers.filter((s) => s && s.urls) : [];   // its server's relays
    this.directOnly = !!directOnly;   // a relay refused: straight, or not at all
    this.robot = robot;
    this.operator = operator || null;
    this.gateway = gateway;
    this.on = on;
    this.rtc = rtc;
    this.pc = null;
    this.path = 'direct';
    this.whyRelay = null;           // through a relay: why not straight (whyRelayed)
    this.state = { driver: 'model', by: null, since: null };
    this.yours = false;
    this.opened = false;              // the robot said who drives
    this.closed = null;               // why this connection ended, once it has
    this.sent = 0;
    this.pending = new Map();         // commands sent with no receipt yet: number -> when, this console's clock
    this.answers = false;             // the robot answered a command: one unanswered is then counted
    this.clock = new Clock();
    this.stats = new Stats();
    this.out = {};                    // each channel's sending side, by label
    this.ref = { n: null, tUs: null };   // the newest frame on the screen: what the next command was made from
    this.waiting = [];                // the takes, releases and stops the robot has not answered yet
    this.waiters = [];                // what connect() is waiting for: every channel open, or the robot's first word
    this.trace = null;                // set by a bench: called with each frame shown {kind, n, t_us, off_us, decoded_us, shown_us}
    this.beat = null;
    this.framesTimer = null;          // reads the browser's frame counts from getStats while connected
    this.framesPrev = { received: 0, dropped: 0 };
    this.localSdp = null;
    this.remoteSdp = null;
    this.tracks = new Tracks({
      onCamera: (key, video) => { if (this.on.camera) this.on.camera(key, video); },
      onShown: (n, tUs) => this.saw(n, tUs),
      offset: () => this.clock.offsetUs,
      stats: this.stats,
      trace: () => this.trace,
      ...cameras,
    });
  }

  /* Who drives the robot now, as it last said: {driver: "model" | "human" | "stopped", by, since}. "model" is no one, on a robot with
     no policy. */
  get driver() { return { ...this.state }; }

  /* Whether this console drives the robot now. */
  get driving() { return this.yours; }

  // ── connecting ──────────────────────────────────────────────────────

  /* Connect straight to the robot: resolved once the robot has said who drives, or throws TeleopError saying why. */
  async connect() {
    const end = performance.now() + CONNECT_MS;
    let unnamed = false;
    const relay = this.iceServers.length > 0 && !this.directOnly;
    const pc = new this.rtc({ iceServers: [{ urls: STUN }, ...(relay ? this.iceServers : [])] });
    this.pc = pc;
    pc.onconnectionstatechange = () => {
      if (pc.connectionState === 'failed' || pc.connectionState === 'closed') this.ended(`the direct connection to the robot ${pc.connectionState}`);
    };
    // a name that did not resolve says nothing of this network's NAT; a server that did not answer does
    pc.onicecandidateerror = (e) => { if (/lookup/i.test(e.errorText || '')) unnamed = true; };
    // every channel before the offer, as the robot only hears of what the offer holds
    for (const [label, options] of Object.entries(CHANNELS)) this.wire(pc.createDataChannel(label, options));
    // a fixed MAX_CAMERAS recvonly video transceivers before the offer: the robot fills one per camera, the rest stay
    // empty (no track, no cost); H.264 only, which the robot encodes and which keeps the offer's SDP small
    const pref = h264Only();
    for (let i = 0; i < MAX_CAMERAS; i += 1) {
      const t = pc.addTransceiver('video', { direction: 'recvonly' });
      if (pref && t.setCodecPreferences) { try { t.setCodecPreferences(pref); } catch (_) { /* a browser that will not */ } }
    }
    // a track the robot sends: its m-line index is which camera (the robot fills them in order), its frames read by teleop-track;
    // a stream of its own, never e.streams[0]: the robot's tracks share one stream (aiortc gives a connection one), and a video
    // given a stream plays its first video track alone - every camera would show the first
    pc.ontrack = (e) => {
      if (!e.track || e.track.kind !== 'video') return;
      this.tracks.onTrack(new MediaStream([e.track]), parseInt((e.transceiver && e.transceiver.mid) || '', 10));
    };
    await pc.setLocalDescription(await pc.createOffer());
    await this.gathered(pc);
    this.localSdp = keptCandidates(pc.localDescription.sdp, relay);
    const nat = natOf(this.localSdp, unnamed);
    const placed = await this.gateway.send('POST', OFFER, { robot: this.robot,
      ...(this.operator ? { operator: this.operator } : {}), sdp: this.localSdp, nat,
      ...(this.directOnly ? { direct_only: true } : {}) });
    if (placed.status !== 200 || !placed.body || !placed.body.pairing) throw this.refused(placed);
    const answer = await this.answerOf(String(placed.body.pairing), end);
    this.remoteSdp = keptCandidates(answer.sdp, relay);
    await pc.setRemoteDescription({ type: 'answer', sdp: this.remoteSdp });
    // no pair answering within DIRECT_MS is no way between the two; once one has, DTLS and the channels have until `end`
    await this.until(() => this.allOpen() || !CHECKING.includes(pc.iceConnectionState), Math.min(end, performance.now() + DIRECT_MS));
    const noWay = !this.allOpen() && CHECKING.includes(pc.iceConnectionState);
    if (noWay || !await this.until(() => this.allOpen(), end)) {
      const facts = this.facts();
      const why = whyNot(nat, answer.nat, facts);
      this.close();
      throw new TeleopError(`no direct connection to the robot: ${why}`, 'direct_failed', null,
        { console: nat, robot: answer.nat, ...facts });
    }
    try { this.path = pathOf(await pc.getStats()); } catch (_) { /* a browser that will not say: direct, as it was */ }
    // through a relay: why not straight, for its person to read (the teleop plan, 2a)
    this.whyRelay = this.path === 'relay' ? whyRelayed(nat, answer.nat, this.facts()) : null;
    // the robot's first word on its reliable channel: who drives
    if (!await this.until(() => this.opened, end)) {
      const why = this.closed || 'no answer in time';
      this.close();
      throw new TeleopError(`the robot said nothing on its direct connection: ${why}`, 'direct_failed');
    }
    this.beating();
    this.pollFrames();
  }

  /* The browser's own count of the video frames it received and dropped, read from getStats into frames_received /
     frames_dropped: a native track's jitter buffer and decoder are the browser's, so only it knows what it dropped. */
  pollFrames() {
    if (this.closed !== null || !this.pc) return;
    this.pc.getStats().then((report) => {
      if (this.closed !== null) return;
      const { received, dropped } = framesOf(report);
      this.stats.count('frames_received', Math.max(0, received - this.framesPrev.received));
      this.stats.count('frames_dropped', Math.max(0, dropped - this.framesPrev.dropped));
      this.framesPrev = { received, dropped };
    }).catch(() => {});
    if (this.closed === null) this.framesTimer = setTimeout(() => this.pollFrames(), 1000);
  }

  /* This side's addresses gathered, or GATHER_MS gone: the offer goes with what it has, no trickle.
     A STUN server that does not answer would otherwise hold it for as long as the browser tries. */
  gathered(pc) {
    if (pc.iceGatheringState === 'complete') return Promise.resolve();
    return new Promise((resolve) => {
      const done = () => { clearTimeout(timer); pc.onicegatheringstatechange = null; resolve(); };
      const timer = setTimeout(done, GATHER_MS);
      pc.onicegatheringstatechange = () => { if (pc.iceGatheringState === 'complete') done(); };
    });
  }

  /* The gateway's refusal as an error, its words kept for the page to say (errorLine). */
  refused(r) {
    const reason = (r.body && r.body.details && r.body.details.reason) || `status_${r.status}`;
    this.close();
    return new TeleopError('the platform refused this connection', reason, r);
  }

  /* The robot's answer to this console's offer, asked for until `end`. A round that reached nothing (status 0) is asked again. */
  async answerOf(pairing, end) {
    for (;;) {
      const left = Math.floor((end - performance.now()) / 1000);
      if (left < 1) {
        this.close();
        throw new TeleopError('no direct connection to the robot: it did not answer in time', 'direct_failed');
      }
      const r = await this.gateway.get(`${PAIRING}${encodeURIComponent(pairing)}?wait_s=${Math.min(left, PAIRING_WAIT_S)}`);
      if (r.status === 0) continue;
      if (r.status !== 200 || !r.body) throw this.refused(r);
      if (r.body.state === 'answered' && r.body.sdp) return r.body;
      if (r.body.state === 'failed') {
        this.close();
        throw new TeleopError(`no direct connection to the robot: it could not answer (${r.body.why})`, 'direct_failed');
      }
    }
  }

  /* What a failure is explained by: each side's candidate kinds and how far the connection got. */
  facts() {
    const pc = this.pc;
    const dtls = pc && pc.sctp && pc.sctp.transport ? pc.sctp.transport.state : null;
    return { connection: pc ? pc.connectionState : null, ice: pc ? pc.iceConnectionState : null, dtls,
      mine: candidateTypes(this.localSdp), theirs: candidateTypes(this.remoteSdp) };
  }

  /* One of CHANNELS: its sending side and its pieces in. */
  wire(channel) {
    channel.binaryType = 'arraybuffer';
    this.out[channel.label] = new Sender(channel);
    const assembly = new Assembly();
    channel.onmessage = (e) => {
      if (typeof e.data === 'string') return;
      const whole = assembly.add(new Uint8Array(e.data));
      if (whole) this.said(channel.label, whole, nowUs());
    };
    channel.onopen = () => {
      if (this.allOpen()) for (const s of Object.values(this.out)) s.pump();
      this.woke();
    };
  }

  allOpen() {
    return Object.keys(CHANNELS).every((l) => this.out[l] && this.out[l].channel.readyState === 'open');
  }

  /* Whether `ready()` came true before `end`, or this connection ended first. */
  until(ready, end) {
    return new Promise((resolve) => {
      const check = () => {
        if (ready()) return finish(true);
        if (this.closed !== null) return finish(false);
        return undefined;
      };
      const timer = setTimeout(() => finish(false), Math.max(1000, end - performance.now()));
      const finish = (v) => {
        clearTimeout(timer);
        this.waiters = this.waiters.filter((w) => w !== check);
        resolve(v);
      };
      this.waiters.push(check);
      check();
    });
  }

  woke() { for (const w of [...this.waiters]) w(); }

  // ── what the robot says ─────────────────────────────────────────────

  /* A whole message the robot sent: who drives, a control one, a step. One that does not read is no one's. */
  said(label, data, atUs) {
    let message;
    try {
      message = unpack(data);
    } catch (_) {
      return;
    }
    if (!isMap(message)) return;
    if (label === 'seq-who') {
      this.who(message);
    } else if (label === 'seq-ctl') {
      this.control(message, atUs);
    } else if (label === 'seq-state' && Number.isInteger(message.n)) {
      // the non-video arrays and how late they came; video frames are the RTP track now, Depth / Tactile the seq-video
      // channel (not drawn), so a step no longer carries a camera
      this.arrays(Number.isInteger(message.t_us) ? message.t_us : null, message.v, atUs);
    }
  }

  /* One step's arrays as they came: how late they came. They are not drawn. */
  arrays(made, value, atUs) {
    const off = this.clock.offsetUs;
    if (made !== null && off !== null) this.stats.sample('state_us', atUs - (made - off));
    if (value !== null && value !== undefined) this.stats.count('states_received');
  }

  /* What the robot says on its reliable channel. A plan's ask for a person is not shown here. */
  who(message) {
    if (message.t === 'driver') {
      const since = Number.isInteger(message.since_us) ? message.since_us / 1e6 : null;
      this.state = { driver: message.driver, by: message.by ?? null, since };
      this.yours = message.yours === true;
      this.opened = true;
      if (this.on.driver) this.on.driver(this.driver, this.yours);
      this.settle();
      this.woke();
    } else if (message.t === 'refused') {
      const first = this.waiting.shift();
      if (first) {
        clearTimeout(first.timer);
        first.reject(new TeleopError(String(message.why || 'the robot refused it'), String(message.reason || 'refused')));
      }
    }
    // a pong says nothing the clock's ticks do not
  }

  /* The robot's tock, a receipt for a command, or nothing this page knows. */
  control(message, atUs) {
    if (message.t === 'tock') {
      const trip = this.clock.tock(message, atUs);
      if (trip !== null) this.stats.sample('rtt_us', trip);
    } else if (message.t === 'vm') {
      this.tracks.vm(message);        // which camera a video track is, and what n / capture time its frames are
    } else if (message.t === 'got') {
      const sent = this.pending.get(message.id);
      this.pending.delete(message.id);
      this.answers = true;
      const off = this.clock.offsetUs;
      const got = Number.isInteger(message.got_us) ? message.got_us : null;
      const oneWay = sent !== undefined && off !== null && got !== null ? (got - off) - sent : null;
      if (oneWay !== null) this.stats.sample('command_us', oneWay);
      if (this.on.receipt) this.on.receipt(message.id, message.did, oneWay);
    }
  }

  /* The newest frame on the screen, by its capture time: what the next command is made from. */
  saw(n, tUs) {
    if (this.ref.tUs === null || tUs > this.ref.tUs) this.ref = { n, tUs };
  }

  // ── what it says ────────────────────────────────────────────────────

  /* That it is there, every HEARTBEAT_MS, and its clock's ticks: a timer of its own, a hidden page's being slowed to once a second,
     which still beats the robot's 3 s. */
  beating() {
    let pingAt = 0;
    let tickAt = 0;
    const beat = () => {
      if (this.closed !== null) return;
      const now = performance.now();
      if (now >= pingAt) {
        this.send_('seq-who', pack({ t: 'ping', at_us: nowUs() }));
        pingAt = now + HEARTBEAT_MS;
      }
      if (now >= tickAt) {
        this.send_('seq-ctl', pack(this.clock.tick()));
        tickAt = now + this.clock.due();
      }
      this.beat = setTimeout(beat, Math.max(5, Math.min(pingAt, tickAt) - performance.now()));
    };
    beat();
  }

  send_(label, data) {
    if (this.out[label]) this.out[label].put(data);
  }

  /* Say `kind` and wait for the robot's answer: resolved with who drives once `done()`, rejected with the refusal that came after it. */
  say(kind, done, timeoutMs = SAY_MS) {
    if (this.closed !== null || !this.pc) {
      return Promise.reject(new TeleopError(`this console's connection to the robot ended: ${this.closed || 'it was closed'}`, 'direct_lost'));
    }
    return new Promise((resolve, reject) => {
      const entry = { done, resolve, reject, timer: null };
      entry.timer = setTimeout(() => {
        this.waiting = this.waiting.filter((w) => w !== entry);
        reject(new TeleopError(`the robot did not answer ${kind} within ${timeoutMs / 1000} s`, 'no_answer'));
      }, timeoutMs);
      this.waiting.push(entry);
      this.send_('seq-who', pack({ t: kind, ...(this.operator ? { by: this.operator } : {}) }));
      this.settle();
    });
  }

  settle() {
    this.waiting = this.waiting.filter((w) => {
      if (!w.done()) return true;
      clearTimeout(w.timer);
      w.resolve(this.driver);
      return false;
    });
  }

  /* Drive the robot from this console: from now its act() hands back the chunks sent here. Rejected while another person drives. */
  take() { return this.say('take', () => this.yours && this.state.driver === 'human'); }

  /* Hand the robot back: to its model, or to no one where it has none. */
  release() { return this.say('release', () => this.state.driver === 'model'); }

  /* Stop the robot where it is, whoever drives it: any console may. */
  stop(timeoutMs) { return this.say('stop', () => this.state.driver === 'stopped', timeoutMs); }

  /* One action chunk to the robot, at once and as it is: what its next act() hands back, once. Numbered and timed, and saying the
     newest frame on this screen. `sampled_us`: when the input it was made from was read, for metrics' input_us. Returns its number. */
  send(chunk, { sampled_us: sampled } = {}) {
    if (this.closed !== null || !this.pc) {
      throw new TeleopError(`${this.closed || 'it was closed'}: connect again`, 'direct_lost');
    }
    if (!this.yours) throw new TeleopError('this console does not drive the robot: take it first', 'not_driving');
    this.sent += 1;
    const id = this.sent;
    const sentUs = nowUs();
    this.pending.set(id, sentUs);
    while (this.pending.size > PENDING_KEPT) this.pending.delete(this.pending.keys().next().value);
    this.stats.count('commands_sent');
    if (Number.isInteger(sampled)) this.stats.sample('input_us', sentUs - sampled);
    this.send_('seq-cmd', pack({ chunk, id, sent_us: sentUs, off_us: this.clock.offsetUs, ref_us: this.ref.tUs, ref_n: this.ref.n }));
    return id;
  }

  /* How this connection does: {path, latency_us, counters, gauges}, the shape of the Python console's metrics(). Commands past
     LOST_AFTER_MS with no receipt are counted here, and only once the robot has answered one: a channel that never carried a
     receipt says nothing of what was lost. */
  metrics() {
    const now = nowUs();
    let unanswered = 0;
    for (const [id, sent] of this.pending) {
      if (now - sent < LOST_AFTER_MS * 1000) break;
      this.pending.delete(id);
      unanswered += this.answers ? 1 : 0;
    }
    if (unanswered) this.stats.count('commands_unanswered', unanswered);
    this.stats.gauge('clock_offset_us', this.clock.offsetUs);
    this.stats.gauge('clock_uncertainty_us', this.clock.errorUs);
    return { path: this.path, ...(this.whyRelay ? { why_relay: this.whyRelay } : {}), ...this.stats.snapshot() };
  }

  // ── ending ──────────────────────────────────────────────────────────

  /* This connection is over, for the reason given: said once, and whatever was waiting is told. */
  ended(why) {
    if (this.closed !== null) return;
    this.closed = why;
    this.yours = false;
    clearTimeout(this.beat);
    clearTimeout(this.framesTimer);
    for (const w of this.waiting) {
      clearTimeout(w.timer);
      w.reject(new TeleopError(`this console's connection to the robot ended: ${why}`, 'direct_lost'));
    }
    this.waiting = [];
    this.tracks.close();
    this.woke();
    if (this.on.ended) this.on.ended(why);
  }

  /* End this console's connection: a robot it drove stops, told first where the page has the time to wait for that, and otherwise
     by its own watchdog. */
  close() {
    this.ended('the console closed its connection');
    const pc = this.pc;
    this.pc = null;
    if (pc) {
      try { pc.close(); } catch (_) { /* closing what already went */ }
    }
  }

  /* close(), a stop said first for up to `waitMs` when this console drives: leaving the tab, where nobody is looking at Stop any more. */
  async stopAndClose(waitMs = 500) {
    if (this.yours && this.closed === null) {
      try { await this.stop(waitMs); } catch (_) { /* the robot's own watchdog stops it */ }
    }
    this.close();
  }
}

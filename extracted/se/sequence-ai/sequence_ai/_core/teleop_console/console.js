/* console.js — the page `seq teleop serve` serves: one robot's cameras, Take, Release and Stop, and how late the picture is,
   connected straight to the robot (teleop-client.js) and paired by the server this page came from.

   In one sentence: the page opens → its token from the address's #token= (kept for this tab, and taken out of the address bar)
   or the field it asks in once the server refuses → it asks the server whose robot this is (/ping) → it offers to connect, and
   while the robot is not connected asks again every 2 s → Take, Release and Stop (Esc) drive it → the page closed ends the
   connection, a console that drives stopping the robot first. While it drives, Enter VR (where the browser offers WebXR)
   or Gamepad and keys send the person's own motion as its commands, each frame - a headset's head and hands or
   controllers, a gamepad's sticks, the keys held (teleop-xr.js) - which the robot turns into its joints
   (sequence_ai.retarget); the headset shows its cameras.
   Watch only, where the server names a MoQ relay (seq teleop serve --moq-port): the page loads MoQ's player
   (vendor/moq-watch.js), lists the cameras the robot's broadcast has beneath it as the relay announces them, and plays each
   in a <moq-watch>; it connects nothing straight to the robot, so it takes, releases and stops nothing.

   CSP: an external module under script-src 'self'; everything the robot or the server says goes in through textContent, its
   frames on a <video> playing a track. */

import { TeleopClient } from '/assets/teleop-client.js';
import { controls, latencyCells, whoLine } from '/assets/teleop-view.js';
import { PadKeys, XrInputs, xrSupported } from '/assets/teleop-xr.js';

const AGAIN_MS = 2000;                 // a robot not connected yet: asked for again this often
const READ_EVERY_MS = 1000;            // the figures, read this often while connected
const TOKEN_KEY = 'seq-teleop-token';
const OPERATOR_KEY = 'seq-teleop-operator';
const DIRECT_KEY = 'seq-teleop-direct-only';
const WATCH_KEY = 'seq-teleop-watch-only';
const PADS_KEY = 'seq-teleop-pad-keys';
const PLAYER = '/assets/vendor/moq-watch.js';
const PATH_TITLE = 'How pictures and commands go: straight between this browser and the robot, or through the relay its server names';
const $ = (id) => document.getElementById(id);
const put = (node, text) => { if (node.textContent !== text) node.textContent = text; };

/* A stored value, or '' where this browser keeps none (a private window, storage turned off). */
function stored(store, key) {
  try { return store.getItem(key) || ''; } catch (_) { return ''; }
}
function keep(store, key, value) {
  try { if (value) store.setItem(key, value); else store.removeItem(key); } catch (_) { /* kept for this page alone */ }
}

let token = stored(sessionStorage, TOKEN_KEY);
const given = /(?:^#|&)token=([^&]*)/.exec(location.hash);
if (given) {
  token = decodeURIComponent(given[1]);
  keep(sessionStorage, TOKEN_KEY, token);
  history.replaceState(null, '', location.pathname + location.search);
}

/* The server this page came from, as TeleopClient asks it: { status, body }. */
async function call(method, path, body) {
  const headers = { Accept: 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  const r = await fetch(path, { method, headers, cache: 'no-store',
    body: body === undefined ? undefined : JSON.stringify(body) });
  let parsed = null;
  try { parsed = await r.json(); } catch (_) { parsed = null; }
  return { status: r.status, body: parsed };
}
const server = { send: (method, path, body) => call(method, path, body), get: (path) => call('GET', path) };

let robot = null;          // the robot's name, as the server says it
let client = null;         // this page's connection, from its offer to its end
let relay = null;          // the MoQ relay its server names, as GET /v1/teleop/moq says it, or null
let watching = null;       // a watch through it: { conn, tiles }, from its start to its end
let connected = false;     // the robot has said who drives
let waiting = false;       // the robot is not connected yet: asked for again
let why = '';              // why it could not connect, or ended
let busy = false;          // a Take, Release or Stop on its way
let timer = 0;
let again = 0;
let xr = null;             // this console in a headset (Enter VR), from its start to its end
let pads = null;           // the gamepad and the keys, while Gamepad and keys is ticked

function said(line) { put($('said'), line); }

/* A person's motion - a headset's, a gamepad's, the keys' - to the robot as its command, while this console drives it: the
   robot's newest, which its retargeting turns into its joints. Not driving, nothing goes. */
function sendInputs(inputs) {
  if (client && connected && !watching && client.driving) client.send({ inputs });
}

function figures() {
  const cells = latencyCells(client && connected && !watching ? client.metrics() : null);
  put($('frame'), cells.frame);
  put($('rtt'), cells.rtt);
}

/* The page as things are now: what it waits on, who drives, and what can be pressed. */
function draw() {
  put($('robot'), robot || 'robot');
  put($('path'), watching ? 'watching through the MoQ relay' : connected && client ? (client.path === 'relay' ? 'through a relay' : 'direct') : '');
  $('path').title = connected && client && client.whyRelay ? `Not straight: ${client.whyRelay}.` : PATH_TITLE;
  const cams = $('view').querySelectorAll('.cam').length;
  const line = why || (waiting ? 'Waiting for the robot to connect' : !connected ? 'Connecting' : cams ? '' : 'No picture yet');
  put($('state'), line);
  $('state').hidden = !line;
  const state = client ? client.driver : {};
  const yours = !!(client && client.driving);
  put($('who'), connected && !watching ? whoLine(state, yours, null) : '');
  $('dot').dataset.state = !connected || watching ? '' : yours ? 'yours' : state.driver === 'human' ? 'human'
    : state.driver === 'stopped' ? 'stopped' : 'idle';
  const can = controls({ connected: connected && !watching, driver: state.driver, yours, busy });
  $('take').disabled = !can.take;
  $('release').disabled = !can.release;
  $('stop').disabled = !can.stop;
  $('vr').disabled = !xr && !(connected && !watching && yours);       // entered while driving, left any time
  put($('vr'), xr ? 'Exit VR' : 'Enter VR');
  $('again').hidden = connected || waiting || (!!(client || watching) && !why);
}

/* Everything a connection put on the page, gone with it. */
function clear() {
  clearInterval(timer);
  clearTimeout(again);
  timer = 0;
  client = null;
  if (xr) xr.exit().catch(() => {});
  if (watching) watching.conn.close();
  watching = null;
  connected = false;
  busy = false;
  for (const node of $('view').querySelectorAll('.cam')) node.remove();
  figures();
}

/* The relay's address as MoQ's player connects to it: where the server hands out a fingerprint - a relay that made its own
   certificate - its http:// twin, at which the player reads that fingerprint (/certificate.sha256) and pins it; else as it
   is. Its token goes in its query. */
function relayUrl(where) {
  const url = new URL(where.url);
  if ((where.fingerprints || []).length) url.protocol = 'http:';
  return url;
}

/* One camera's broadcast, playing. */
function tile(key, url, path) {
  const fig = document.createElement('figure');
  fig.className = 'cam';
  const player = document.createElement('moq-watch');
  for (const [name, value] of [['delay', 'instant'], ['visible', 'always'], ['catalog-format', 'hang']]) player.setAttribute(name, value);
  player.append(document.createElement('canvas'));
  player.setAttribute('name', path);
  player.setAttribute('url', url.toString());
  const cap = document.createElement('figcaption');
  cap.textContent = key || 'camera';
  fig.append(player, cap);
  $('view').append(fig);
  return fig;
}

/* Watch the robot through its server's MoQ relay: each camera the robot's broadcast has beneath it, as the relay announces
   it - a <moq-watch> for each, gone with its broadcast - until the page closes it. */
async function watch(where) {
  if (typeof WebTransport === 'undefined') {
    // MoQ's player would fall back to a WebSocket, which seq teleop serve's relay does not take (Playwright's WebKit 11-21)
    why = 'This browser has no WebTransport, which watching through the relay needs: Chrome, Edge or Firefox has it. '
      + 'Untick Watch only to connect straight.';
    draw();
    return;
  }
  let Net;
  try {
    ({ Net } = await import(PLAYER));
  } catch (err) {
    why = `MoQ's player did not load: ${err.message || err}`;
    draw();
    return;
  }
  const url = relayUrl(where);
  const w = { conn: new Net.Connection({ url, enabled: true }), tiles: new Map() };
  watching = w;
  connected = true;
  waiting = false;
  draw();
  const beneath = `${where.broadcast}/`;
  try {
    for await (const update of w.conn.announced(Net.Path.Pattern.subtree(where.broadcast))) {
      if (w !== watching) return;
      const path = String(update.prefix);
      if (!path.startsWith(beneath)) continue;            // the robot's own broadcast: its steps, no picture
      const key = path.slice(beneath.length);
      const shown = w.tiles.get(key);
      if (Net.Announce.isActive(update.kind)) {
        if (!shown) w.tiles.set(key, tile(key, url, path));
      } else if (shown) {
        shown.remove();
        w.tiles.delete(key);
      }
      draw();
    }
  } catch (err) {
    if (w !== watching) return;
    clear();
    why = `The watch through the MoQ relay ended: ${err.message || err}.`;
    draw();
  }
}

/* What a refusal or failure says, in the server's or the robot's own words. */
function wordsOf(err) {
  const body = err && err.response && err.response.body;
  return (body && body.detail) || (err && err.message) || String(err);
}

async function start() {
  if (client) return;
  why = '';
  said('');
  if (!robot) {
    const ping = await call('GET', '/ping').catch(() => null);
    robot = ping && ping.body && ping.body.robot ? String(ping.body.robot) : null;
  }
  // its server's MoQ relay, where it names one: Watch only offered, and taken where it is ticked
  const moq = await call('GET', '/v1/teleop/moq').catch(() => null);
  if (moq && moq.status === 401) {
    why = 'This server asks for its token: the TOKEN `seq teleop serve` printed, or the one it was given.';
    $('token-field').hidden = false;
    $('token').focus();
    draw();
    return;
  }
  relay = moq && moq.status === 200 && moq.body && moq.body.url && moq.body.broadcast ? moq.body : null;
  $('watch-field').hidden = !relay;
  if (relay && $('watch-only').checked) {
    await watch(relay);
    return;
  }
  const operator = $('operator').value.trim().slice(0, 80) || null;
  const directOnly = $('direct-only').checked;
  // its server's relays (seq teleop serve --turn), asked for before it gathers: none from a server that names none
  const ice = directOnly ? null : await call('GET', '/v1/teleop/ice').catch(() => null);
  const iceServers = ice && ice.status === 200 && ice.body && Array.isArray(ice.body.ice_servers) ? ice.body.ice_servers : [];
  let c = null;
  c = new TeleopClient({ robot, operator, gateway: server, iceServers, directOnly, on: {
    driver: () => { if (c === client) draw(); },
    ended: (ended) => {
      if (c !== client || !connected) return;   // while it connects, connect() says why
      clear();
      why = `The connection to the robot ended: ${ended}.`;
      draw();
    },
    camera: (key, video) => {
      const fig = document.createElement('figure');
      fig.className = 'cam';
      fig.dataset.key = key || '';           // the headset pairs a stereo camera's two by their names
      const cap = document.createElement('figcaption');
      cap.textContent = key || 'camera';
      fig.append(video, cap);
      $('view').append(fig);
      draw();
    },
  } });
  client = c;
  draw();
  try {
    await c.connect();
    if (c !== client) return;
    connected = true;
    waiting = false;
    if (c.whyRelay) said(`Through a relay, not straight: ${c.whyRelay}.`);
    window.__seqTeleop = c;              // for a bench measuring this page: as Python's op.metrics()
    timer = setInterval(figures, READ_EVERY_MS);
  } catch (err) {
    if (c !== client) return;
    clear();
    if (err.reason === 'robot_not_connected') {
      waiting = true;
      again = setTimeout(start, AGAIN_MS);
    } else if (err.response && err.response.status === 401) {
      waiting = false;
      why = 'This server asks for its token: the TOKEN `seq teleop serve` printed, or the one it was given.';
      $('token-field').hidden = false;
      $('token').focus();
    } else {
      waiting = false;
      why = `${wordsOf(err)}`;
    }
  }
  draw();
}

/* A Take, Release or Stop, one at a time: a refusal says the robot's own words. */
async function press(what) {
  if (!client || !connected || busy) return;
  busy = true;
  said('');
  draw();
  try {
    await what(client);
  } catch (err) {
    said(wordsOf(err));
  } finally {
    busy = false;
    draw();
  }
}

$('operator').value = stored(localStorage, OPERATOR_KEY);
$('direct-only').checked = stored(localStorage, DIRECT_KEY) === '1';
$('watch-only').checked = stored(localStorage, WATCH_KEY) === '1';
$('pad-keys').checked = stored(localStorage, PADS_KEY) === '1';
$('take').addEventListener('click', () => press((c) => c.take()));
$('release').addEventListener('click', () => press((c) => c.release()));
$('stop').addEventListener('click', () => press((c) => c.stop()));
xrSupported().then((ok) => { $('vr').hidden = !ok; });
$('vr').addEventListener('click', async () => {
  if (xr) {
    await xr.exit().catch(() => {});
    return;
  }
  const session = new XrInputs({ onInputs: sendInputs, cameras: () => [...$('view').querySelectorAll('.cam')]
      .map((fig) => ({ key: fig.dataset.key || '', video: fig.querySelector('video') })),
    onEnd: () => { if (xr === session) xr = null; draw(); } });
  xr = session;
  draw();
  try {
    await session.enter();
  } catch (err) {
    if (xr === session) xr = null;
    said(`The headset did not start: ${err.message || err}`);
  }
  draw();
});
function padKeys() {
  keep(localStorage, PADS_KEY, $('pad-keys').checked ? '1' : '');
  if ($('pad-keys').checked && !pads) {
    // in a headset its own hands and controllers drive, the gamepad and keys again once it is left: one command at a time
    pads = new PadKeys({ onInputs: (inputs) => { if (!xr) sendInputs(inputs); } });
    pads.start();
  } else if (!$('pad-keys').checked && pads) {
    pads.stop();
    pads = null;
  }
}
$('pad-keys').addEventListener('change', padKeys);
padKeys();
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && connected) press((c) => c.stop());
});
$('fields').addEventListener('submit', (e) => {
  e.preventDefault();
  keep(localStorage, OPERATOR_KEY, $('operator').value.trim());
  keep(localStorage, DIRECT_KEY, $('direct-only').checked ? '1' : '');
  keep(localStorage, WATCH_KEY, $('watch-only').checked ? '1' : '');
  const typed = $('token').value.trim();
  if (typed) {
    token = typed;
    keep(sessionStorage, TOKEN_KEY, token);
    $('token').value = '';
    $('token-field').hidden = true;
  }
  if (connected && !watching && !$('watch-only').checked) return;
  if (client && !why && !watching) return;
  clear();
  start();
});
$('watch-only').addEventListener('change', () => {
  keep(localStorage, WATCH_KEY, $('watch-only').checked ? '1' : '');
  if (!client && !watching) return;
  if (client && client.driving) {                    // one that drives lets go first: Release, then Watch only
    said('Release the robot first: a console that watches through the relay does not drive it.');
    return;
  }
  if (client) client.close();
  clear();
  start();
});
// the page going: nothing can be waited for, so the stop goes and the robot's own watchdog is behind it
window.addEventListener('pagehide', () => {
  if (xr) xr.exit().catch(() => {});
  const c = client;
  if (c) {
    if (c.driving) c.stop(0).catch(() => {});
    c.close();
  }
  if (watching) watching.conn.close();
});
start();

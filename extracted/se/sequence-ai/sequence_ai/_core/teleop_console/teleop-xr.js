/* teleop-xr.js — a teleop console's headset, gamepad and keys: what a person's hands, head, sticks and keys do, sent to the
   robot as they are, every frame the headset draws, for the robot's retargeting (sequence_ai.retarget) to turn into its joints;
   and, in the headset, the robot's cameras on screens in front of the person, a stereo camera's two one to each eye.

   In one sentence: Enter VR (where navigator.xr offers immersive-vr) → an XR session on the local floor, hand tracking where the
   headset has it → each XR frame: the head's pose, each hand's or controller's grip pose, a controller's trigger, squeeze, sticks
   and buttons, a hand's 25 joints → inputsOf() packs them as sequence_ai.retarget reads them → onInputs(inputs), which the
   console sends as its command (TeleopClient.send({inputs})); the cameras drawn on screens in a row, fixed where the person
   looked as the session began - a stereo pair (two cameras named alike but for left and right) one screen, its two to the two
   eyes, every other camera a screen of its own. Out of the headset, PadKeys does the same for a gamepad (the Gamepad API's
   standard mapping) and the keys held.

   WHY the raw inputs and not the robot's joints: the robot knows its arm, its limits and where it is; the console knows none of
   it. Sent raw, they are also what its recording keeps, so another retargeting can make the actions again from the same motion.
   CSP: an external module; no inline script, no eval. */

// a WebXR hand's joints, in XRHand's order: the wrist, then the thumb's four and each finger's five, base to tip
export const HAND_JOINTS = [
  'wrist',
  'thumb-metacarpal', 'thumb-phalanx-proximal', 'thumb-phalanx-distal', 'thumb-tip',
  'index-finger-metacarpal', 'index-finger-phalanx-proximal', 'index-finger-phalanx-intermediate',
  'index-finger-phalanx-distal', 'index-finger-tip',
  'middle-finger-metacarpal', 'middle-finger-phalanx-proximal', 'middle-finger-phalanx-intermediate',
  'middle-finger-phalanx-distal', 'middle-finger-tip',
  'ring-finger-metacarpal', 'ring-finger-phalanx-proximal', 'ring-finger-phalanx-intermediate',
  'ring-finger-phalanx-distal', 'ring-finger-tip',
  'pinky-finger-metacarpal', 'pinky-finger-phalanx-proximal', 'pinky-finger-phalanx-intermediate',
  'pinky-finger-phalanx-distal', 'pinky-finger-tip',
];

const round = (v) => Math.round(v * 1e5) / 1e5;      // 10 µm and 1e-5 of a quaternion: what a hand's tremor is above

/* A pose as sequence_ai.retarget reads it: {p: [x, y, z], q: [x, y, z, w]}, from an XRPose's transform (or null). */
export function poseOf(xrPose) {
  if (!xrPose || !xrPose.transform) return null;
  const { position: p, orientation: q } = xrPose.transform;
  return { p: [round(p.x), round(p.y), round(p.z)], q: [round(q.x), round(q.y), round(q.z), round(q.w)] };
}

/* A gamepad's buttons as their values (0 .. 1) and its axes, as the standard mapping has them. */
export function padOf(gamepad) {
  if (!gamepad) return null;
  return { axes: [...(gamepad.axes || [])].map(round),
           buttons: [...(gamepad.buttons || [])].map((b) => round(typeof b === 'number' ? b : (b.value || (b.pressed ? 1 : 0)))) };
}

/* One hand or controller of an XR frame: its kind, its grip pose, and a controller's trigger and squeeze (xr-standard: buttons 0
   and 1), sticks and buttons, or a hand's 25 joint positions - {tracked: false} where the headset has lost it this frame. */
export function sideOf(source, frame, space) {
  if (source.hand) {
    const joints = [];
    for (const name of HAND_JOINTS) {
      const joint = source.hand.get(name);
      const pose = joint && frame.getJointPose(joint, space);
      if (!pose) return { kind: 'hand', tracked: false };
      const { x, y, z } = pose.transform.position;
      joints.push([round(x), round(y), round(z)]);
    }
    const wrist = poseOf(frame.getJointPose(source.hand.get('wrist'), space));
    return { kind: 'hand', tracked: true, ...wrist, joints };
  }
  const grip = poseOf(frame.getPose(source.gripSpace || source.targetRaySpace, space));
  if (!grip) return { kind: 'controller', tracked: false };
  const pad = padOf(source.gamepad);
  const out = { kind: 'controller', tracked: true, ...grip };
  if (pad) {
    out.trigger = pad.buttons[0] || 0;
    out.squeeze = pad.buttons[1] || 0;
    out.axes = pad.axes;
    out.buttons = pad.buttons;
  }
  return out;
}

/* The inputs of one XR frame: {t, head, left, right}, t this console's clock in seconds (as the robot's stale_s reads it). */
export function inputsOf(frame, space, sources, nowMs = performance.timeOrigin + performance.now()) {
  const out = { t: Math.round(nowMs) / 1000, head: poseOf(frame.getViewerPose(space)) };
  for (const source of sources) {
    // a gaze-and-pinch pointer (WebXR's transient-pointer, as visionOS's natural input makes one) comes and goes with a pinch,
    // beside the very hand that pinches: that hand's own source drives, never the pointer
    if (source.targetRayMode === 'transient-pointer') continue;
    if (source.handedness === 'left' || source.handedness === 'right') out[source.handedness] = sideOf(source, frame, space);
  }
  return out;
}

/* Out of a headset: the first gamepad connected and the keys held, as the robot's Twist reads them. */
export class PadKeys {
  constructor({ onInputs, target = globalThis, pads = () => (navigator.getGamepads ? navigator.getGamepads() : []) }) {
    this.onInputs = onInputs;
    this.pads = pads;
    this.held = new Set();
    this.raf = null;
    // a key typed into a field (the operator's name, the token) drives nothing; a box ticked or a button pressed, which
    // keeps the focus after, is no field
    const typing = (e) => {
      const t = e.target;
      if (!t) return false;
      if (t.isContentEditable || /^(TEXTAREA|SELECT)$/.test(t.tagName || '')) return true;
      return t.tagName === 'INPUT' && !/^(checkbox|radio|button|submit|reset|range|color|file)$/i.test(t.type || 'text');
    };
    this.down = (e) => { if (!e.repeat && !typing(e)) this.held.add(e.key === 'Shift' ? 'shift' : e.key.toLowerCase()); };
    this.up = (e) => this.held.delete(e.key === 'Shift' ? 'shift' : e.key.toLowerCase());
    this.blur = () => this.held.clear();        // a key let go while the page had no focus is never heard: none is held
    this.target = target;
  }

  /* The inputs now: {t, pad, keys}, pad null where no gamepad is connected. */
  read(nowMs = performance.timeOrigin + performance.now()) {
    const pad = [...(this.pads() || [])].find(Boolean);
    return { t: Math.round(nowMs) / 1000, pad: padOf(pad), keys: [...this.held].sort() };
  }

  start() {
    this.target.addEventListener('keydown', this.down);
    this.target.addEventListener('keyup', this.up);
    this.target.addEventListener('blur', this.blur);
    const tick = () => { this.onInputs(this.read()); this.raf = requestAnimationFrame(tick); };
    this.raf = requestAnimationFrame(tick);
  }

  stop() {
    this.target.removeEventListener('keydown', this.down);
    this.target.removeEventListener('keyup', this.up);
    this.target.removeEventListener('blur', this.blur);
    if (this.raf != null) cancelAnimationFrame(this.raf);
    this.raf = null;
    this.held.clear();
  }
}

/* Whether this browser can take the console into a headset. */
export async function xrSupported(xr = globalThis.navigator && navigator.xr) {
  try { return Boolean(xr && await xr.isSessionSupported('immersive-vr')); } catch { return false; }
}

// ── in the headset: the cameras on a screen ───────────────────────────────────────────────────────────────────────────────

const VS = `attribute vec2 a; uniform mat4 m; varying vec2 uv;
void main() { uv = vec2(a.x * 0.5 + 0.5, 0.5 - a.y * 0.5); gl_Position = m * vec4(a, 0.0, 1.0); }`;
const FS = `precision mediump float; uniform sampler2D t; varying vec2 uv;
void main() { gl_FragColor = texture2D(t, uv); }`;

/* a × b, 4x4 column-major as WebXR and WebGL write them */
export function mul(a, b) {
  const out = new Float32Array(16);
  for (let c = 0; c < 4; c += 1) {
    for (let r = 0; r < 4; r += 1) {
      let s = 0;
      for (let k = 0; k < 4; k += 1) s += a[k * 4 + r] * b[c * 4 + k];
      out[c * 4 + r] = s;
    }
  }
  return out;
}

/* Where the screen stands: `distance` metres ahead of the head as the session began, level, at its height, facing it, its
   half-width and half-height scaling a quad of -1 .. 1 - a column-major model matrix. */
export function screenAt(head, { distance = 1.2, width = 1.6, aspect = 16 / 9 } = {}) {
  const [qx, qy, qz, qw] = head.q;
  // the head's forward (-z) turned by its orientation, flattened to the floor
  let fx = -(2 * (qx * qz + qw * qy));
  let fz = -(1 - 2 * (qx * qx + qy * qy));
  const n = Math.hypot(fx, fz) || 1;
  fx /= n; fz /= n;
  const [hx, hy, hz] = head.p;
  const w = width / 2;
  const h = w / aspect;
  // right = forward × up (on the floor: (-fz, 0, fx)); the screen faces back toward the head
  return new Float32Array([-fz * w, 0, fx * w, 0, 0, h, 0, 0, -fx, 0, -fz, 0, hx + fx * distance, hy, hz + fz * distance, 1]);
}

/* The robot's cameras as screens in a row, by their names: a stereo pair - two names alike but for "left" and "right", as
   head_left and head_right - one screen, its left camera to the left eye and its right to the right; every other camera a
   screen of its own, the same to both eyes. Each {left, right}: the cameras' indices; in the order the cameras came. */
export function panesOf(keys) {
  const words = (k) => String(k || '').toLowerCase();
  const swapped = (k) => words(k).replace(/(^|[^a-z])(left|right)(?=$|[^a-z])/g,
    (all, before, side) => before + (side === 'left' ? 'right' : 'left'));
  const sideOf = (k) => (/(^|[^a-z])left($|[^a-z])/.test(words(k)) ? 'left' : 'right');
  const panes = [];
  const used = new Set();
  keys.forEach((key, i) => {
    if (used.has(i)) return;
    const twin = swapped(key) === words(key) ? -1
      : keys.findIndex((other, j) => j !== i && !used.has(j) && words(other) === swapped(key));
    used.add(i);
    if (twin < 0) { panes.push({ left: i, right: i }); return; }
    used.add(twin);
    panes.push(sideOf(key) === 'left' ? { left: i, right: twin } : { left: twin, right: i });
  });
  return panes;
}

/* Where each of `aspects.length` screens stands: in a row, `distance` metres ahead of the head as the session began, 3.2 m
   wide in all at most (1.6 m one), a tenth of a screen apart - a model matrix each (screenAt's, moved along the row). */
export function rowAt(head, aspects, { distance = 1.2 } = {}) {
  const n = aspects.length;
  const width = Math.min(1.6, 3.2 / Math.max(n, 1));
  const step = width * 1.1;
  return aspects.map((aspect, i) => {
    const m = screenAt(head, { distance, width, aspect });
    const along = (i - (n - 1) / 2) * step;                 // from the row's middle, to the right
    m[12] += (m[0] / (width / 2)) * along;
    m[14] += (m[2] / (width / 2)) * along;
    return m;
  });
}

/* The cameras drawn into an XR session's layer, as screens in a row (panesOf). */
class Screens {
  constructor(gl) {
    this.gl = gl;
    const shader = (kind, src) => {
      const s = gl.createShader(kind);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    };
    this.prog = gl.createProgram();
    gl.attachShader(this.prog, shader(gl.VERTEX_SHADER, VS));
    gl.attachShader(this.prog, shader(gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(this.prog);
    this.buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    this.textures = [];                                     // a camera's, by its index
  }

  texture(i) {
    const { gl } = this;
    while (this.textures.length <= i) {
      const t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      this.textures.push(t);
    }
    return this.textures[i];
  }

  /* Each camera's newest frame into its texture: what its video element shows now. */
  upload(videos) {
    const { gl } = this;
    videos.forEach((video, i) => {
      if (!video || video.readyState < 2) return;
      gl.bindTexture(gl.TEXTURE_2D, this.texture(i));
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, video);
    });
  }

  /* `panes` (panesOf) at `models` (rowAt), each eye its side's camera of each. */
  draw(layer, pose, panes, models) {
    const { gl } = this;
    gl.bindFramebuffer(gl.FRAMEBUFFER, layer.framebuffer);
    gl.clearColor(0.05, 0.06, 0.08, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(this.prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buf);
    const a = gl.getAttribLocation(this.prog, 'a');
    gl.enableVertexAttribArray(a);
    gl.vertexAttribPointer(a, 2, gl.FLOAT, false, 0, 0);
    const m = gl.getUniformLocation(this.prog, 'm');
    pose.views.forEach((view) => {
      const vp = layer.getViewport(view);
      gl.viewport(vp.x, vp.y, vp.width, vp.height);
      const seen = mul(view.projectionMatrix, view.transform.inverse.matrix);
      panes.forEach((pane, i) => {
        gl.bindTexture(gl.TEXTURE_2D, this.texture(view.eye === 'right' ? pane.right : pane.left));
        gl.uniformMatrix4fv(m, false, mul(seen, models[i]));
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      });
    });
  }
}

/* The console in a headset: enter() starts an immersive-vr session and calls onInputs(inputs) every frame it draws until the
   person leaves it or exit() ends it; cameras() gives the robot's cameras to show, [{key, video}], as screens (panesOf). */
export class XrInputs {
  constructor({ onInputs, cameras = () => [], onEnd = () => {}, xr = globalThis.navigator && navigator.xr,
                Layer = globalThis.XRWebGLLayer }) {
    this.onInputs = onInputs;
    this.cameras = cameras;
    this.onEnd = onEnd;
    this.xr = xr;
    this.Layer = Layer;
    this.session = null;
    this.frames = 0;
  }

  async enter() {
    const session = await this.xr.requestSession('immersive-vr', { optionalFeatures: ['local-floor', 'hand-tracking'] });
    this.session = session;
    const canvas = document.createElement('canvas');
    // compatible from its creation: makeXRCompatible() waits for a headset that may never be there, and a context that is not
    // compatible makes XRWebGLLayer throw, saying so
    const gl = canvas.getContext('webgl', { xrCompatible: true, alpha: false });
    const layer = new this.Layer(session, gl);
    session.updateRenderState({ baseLayer: layer });
    let space;
    try { space = await session.requestReferenceSpace('local-floor'); } catch { space = await session.requestReferenceSpace('local'); }
    const screens = new Screens(gl);
    let head = null;          // where the head was as the session began: the screens stay there
    let layout = null;        // {seen: what it was laid out for, panes, models}, again when a camera comes or its size is known
    session.addEventListener('end', () => { this.session = null; this.onEnd(); });
    const onFrame = (time, frame) => {
      if (!this.session) return;
      session.requestAnimationFrame(onFrame);
      const inputs = inputsOf(frame, space, session.inputSources || []);
      this.frames += 1;
      this.onInputs(inputs);
      const pose = frame.getViewerPose(space);
      if (!pose) return;
      head = head || inputs.head;
      const cams = (this.cameras() || []).filter((c) => c && c.video);
      const aspectOf = (v) => (v.videoWidth && v.videoHeight ? v.videoWidth / v.videoHeight : 16 / 9);
      const seen = cams.map((c) => `${c.key}:${aspectOf(c.video)}`).join('|');
      if (head && (!layout || layout.seen !== seen)) {
        const panes = panesOf(cams.map((c) => c.key));
        layout = { seen, panes, models: rowAt(head, panes.map((p) => aspectOf(cams[p.left].video))) };
      }
      this.panes = layout ? layout.panes : [];
      screens.upload(cams.map((c) => c.video));
      if (layout) screens.draw(session.renderState.baseLayer || layer, pose, layout.panes, layout.models);
    };
    session.requestAnimationFrame(onFrame);
    return session;
  }

  async exit() {
    if (this.session) await this.session.end();
  }
}

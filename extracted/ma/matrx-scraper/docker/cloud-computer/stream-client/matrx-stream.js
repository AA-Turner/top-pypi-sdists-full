/* Cloud Computer screen page contract (loaded after Selkies' app.js).
 *
 * To the embedding app (window.parent, only to the allowed embedding origin):
 *   {type:"matrx-stream", state:"connecting"|"connected"|"reconnecting"|"disconnected", ts}
 *   "connected" means a picture is on screen: the video peer is connected AND
 *   a frame arrived after that connection (a connected peer whose first frame
 *   is still on its way left the app showing this page's black loader).
 *   {type:"matrx-stream", state:"keyboard", ok:true, ts}   after a keyboard reset
 *   {type:"matrx-stream", state:"quality", quality:{rttMs,fps,lossPct,delayMs,kbps,freezes,active,relay}, ts}
 *   every two seconds while connected and visible: raw numbers, the app judges them
 *   {type:"matrx-stream", state:"clipboard", ok, way:"in"|"out", ts}   the browser refused (or
 *   allowed again) reading the person's clipboard ("in") or writing to it ("out")
 * From the embedding app (event.origin must be that origin):
 *   {type:"matrx-stream-cmd", cmd:"keyboard-reset"}  release every held key, re-attach, focus, ack
 *   {type:"matrx-stream-cmd", cmd:"focus"}           focus the input element
 * The embedding origin is ?parent=<origin> or document.referrer's origin, and
 * must be https://aimatrx.com, a subdomain, or a *.localhost dev origin.
 */
(function () {
  "use strict";
  var NUM_LOCK = 0xff7f;
  var posts = (window.__matrxStreamPosts = []);

  function allowedOrigin(value) {
    try {
      var u = new URL(value);
      var h = u.hostname;
      if (u.protocol === "https:" && (h === "aimatrx.com" || h.slice(-12) === ".aimatrx.com")) return u.origin;
      if (h === "localhost" || h.slice(-10) === ".localhost" || h === "127.0.0.1") return u.origin;
    } catch (e) {}
    return "";
  }
  var params = new URLSearchParams(window.location.search);
  var parentOrigin = allowedOrigin(params.get("parent") || "") || allowedOrigin(document.referrer || "");
  var framed = window.parent !== window;

  function post(message) {
    message.type = "matrx-stream";
    message.ts = Date.now();
    posts.push(message);
    if (posts.length > 50) posts.shift();
    if (framed && parentOrigin) window.parent.postMessage(message, parentOrigin);
  }

  var state = null;
  var everConnected = false;
  function setState(next) {
    if (next === state) return;
    state = next;
    document.documentElement.setAttribute("data-matrx-stream", next);
    post({ state: next });
  }

  // Our loader: black, a calm pulse, no words (the app draws them).
  var loader = document.createElement("div");
  loader.id = "matrx-loader";
  loader.innerHTML = '<div class="matrx-pulse"></div>';
  document.body.appendChild(loader);
  // A browser that blocks autoplay shows the loader until a press starts play.
  loader.addEventListener("click", function () {
    try { app.playStream(); } catch (e) {}
  });
  var video = document.getElementById("stream");
  video.setAttribute("tabindex", "0");

  // Connection state: the picture is the stream. The video peer connecting is
  // not enough; "connected" waits for a frame decoded after that connection.
  // Two signals, either suffices: the next presented frame (requestVideoFrameCallback,
  // which a hidden page never fires) and the decoded-frame counter moving.
  var peerUp = false;
  var awaitingFrame = false;
  var framesAtConnect = 0;
  function decodedFrames() {
    try {
      if (video.getVideoPlaybackQuality) return video.getVideoPlaybackQuality().totalVideoFrames || 0;
    } catch (e) {}
    return video.webkitDecodedFrameCount || 0;
  }
  // A decoded frame is a picture only where nothing can be presented (a hidden
  // page) or presentation cannot be observed (no requestVideoFrameCallback).
  function decodedCounts() { return !!document.hidden || !video.requestVideoFrameCallback; }
  function frameShown(presented) {
    if (!video.videoWidth) return;
    if (!presented && !decodedCounts()) return;
    loader.classList.add("matrx-hidden");
    if (awaitingFrame && peerUp) {
      awaitingFrame = false;
      setState("connected");
    }
  }
  function watchForFrame() {
    if (!awaitingFrame) return;
    if (video.requestVideoFrameCallback) {
      video.requestVideoFrameCallback(function () {
        if (video.videoWidth) frameShown(true); else watchForFrame();
      });
    }
    // The decoded-frame counter counts only while the page is hidden (a hidden
    // page presents nothing) or the browser has no requestVideoFrameCallback.
    // On a visible page a decoded frame is not yet a picture: the app's pane
    // dropped its cover onto an unpainted frame on decode alone (2026-10-18).
    var poll = function () {
      if (!awaitingFrame) return;
      if (decodedCounts() && video.videoWidth && decodedFrames() !== framesAtConnect) frameShown(false);
      else setTimeout(poll, 100);
    };
    setTimeout(poll, 100);
  }
  video.addEventListener("playing", function () { frameShown(false); });
  video.addEventListener("loadeddata", function () { frameShown(false); });

  var onVideoState = webrtc.onconnectionstatechange;
  webrtc.onconnectionstatechange = function (s) {
    if (onVideoState) onVideoState(s);
    if (s === "connected") {
      everConnected = true;
      if (!peerUp) {
        peerUp = true;
        awaitingFrame = true;
        framesAtConnect = decodedFrames();
        watchForFrame();
      }
    } else if (s === "failed" || s === "disconnected" || s === "closed") {
      peerUp = false;
      awaitingFrame = false;
      setState(everConnected ? "reconnecting" : "connecting");
    }
  };
  // The signalling socket is not the session. It rides a server task that
  // every release drains, while the picture is peer to peer. Upstream reset
  // the whole session when the socket closed; while the peer is still
  // connected this page now only re-opens signalling as a RESUME (the hub puts
  // it back in its session) and the picture never stops. Upstream's reset
  // still runs when the peer is down, the hub refuses the resume (nothing to
  // resume), or the page closed signalling on purpose (Selkies' "reload").
  var resumes = (window.__matrxSignallingResumes = []);
  function peerConnected(rtc) {
    try { return !!(rtc && rtc.peerConnection && rtc.peerConnection.connectionState === "connected"); }
    catch (e) { return false; }
  }
  function keepSessionAcrossSignalling(sig, rtc, reset) {
    if (!sig || typeof sig.connect !== "function") return;
    var refused = false;
    var deliberate = false;
    var connect = sig.connect;
    sig.connect = function () {
      refused = false;
      deliberate = false;
      connect.call(sig);
      try {
        sig._ws_conn.addEventListener("message", function (event) {
          if (event.data === "ERROR matrx-no-session") refused = true;
        });
      } catch (e) {}
    };
    var disconnect = sig.disconnect;
    sig.disconnect = function () {
      deliberate = true;
      return disconnect.call(sig);
    };
    sig.ondisconnect = function () {
      if (!deliberate && !refused && peerConnected(rtc)) {
        sig.matrx_resume = true;
        resumes.push(Date.now());
        if (resumes.length > 50) resumes.shift();
        sig.connect();
        return;
      }
      sig.matrx_resume = false;
      reset();
    };
  }
  var onSignallingDown = signalling.ondisconnect;
  keepSessionAcrossSignalling(signalling, webrtc, function () {
    peerUp = false;
    awaitingFrame = false;
    setState(everConnected ? "reconnecting" : "connecting");
    if (onSignallingDown) onSignallingDown();
  });
  if (!signalling.connect) {
    signalling.ondisconnect = function () {
      peerUp = false;
      awaitingFrame = false;
      setState(everConnected ? "reconnecting" : "connecting");
      if (onSignallingDown) onSignallingDown();
    };
  }
  // Audio's own reset only: upstream's audio handler also closed the video
  // signalling, so a lost audio link used to restart the picture too.
  if (typeof audio_signalling !== "undefined" && typeof audio_webrtc !== "undefined") {
    keepSessionAcrossSignalling(audio_signalling, audio_webrtc, function () {
      try { audio_webrtc.reset(); } catch (e) {}
    });
  }

  // Picture quality. While connected the page measures its own video
  // connection and posts the raw numbers; the app decides what to tell the
  // person (2026-11-19: a laggy screen said nothing, and nobody could tell
  // whether the network or the machine was slow). Numbers only, no judgement:
  //   rttMs    round trip of the selected connection pair
  //   fps      frames decoded per second over the sample
  //   lossPct  video packets lost over the sample, percent
  //   delayMs  time a frame waited in the jitter buffer, averaged over the sample
  //   kbps     video received
  //   freezes  picture freezes during the sample
  //   relay    the picture travels through a relay
  //   active   the person pressed, moved or typed in this page during the sample
  //            (a still screen may lawfully send few frames; a driven one may not)
  var QUALITY_EVERY_MS = 2000;
  var lastSample = null;
  var lastInputAt = 0;
  function noteInput() { lastInputAt = Date.now(); }
  ["pointerdown", "pointermove", "wheel", "keydown"].forEach(function (type) {
    window.addEventListener(type, noteInput, true);
  });
  function num(value) { return typeof value === "number" && isFinite(value) ? value : null; }
  function readQuality(report, now) {
    var video_in = null;
    var pair = null;
    var byId = {};
    report.forEach(function (s) {
      byId[s.id] = s;
      if (s.type === "inbound-rtp" && (s.kind === "video" || s.mediaType === "video")) video_in = s;
      if (s.type === "transport" && s.selectedCandidatePairId) pair = s.selectedCandidatePairId;
    });
    var chosen = pair ? byId[pair] : null;
    if (!chosen) {
      report.forEach(function (s) {
        if (s.type === "candidate-pair" && s.nominated && s.state === "succeeded") chosen = s;
      });
    }
    if (!video_in) return null;
    var sample = {
      at: now,
      frames: num(video_in.framesDecoded) || 0,
      lost: num(video_in.packetsLost) || 0,
      received: num(video_in.packetsReceived) || 0,
      bytes: num(video_in.bytesReceived) || 0,
      buffered: num(video_in.jitterBufferDelay) || 0,
      emitted: num(video_in.jitterBufferEmittedCount) || 0,
      freezes: num(video_in.freezeCount) || 0
    };
    var previous = lastSample;
    lastSample = sample;
    if (!previous || sample.at <= previous.at || sample.frames < previous.frames) return null;
    var seconds = (sample.at - previous.at) / 1000;
    var packets = (sample.received - previous.received) + (sample.lost - previous.lost);
    var emitted = sample.emitted - previous.emitted;
    var local = chosen && chosen.localCandidateId ? byId[chosen.localCandidateId] : null;
    var remote = chosen && chosen.remoteCandidateId ? byId[chosen.remoteCandidateId] : null;
    var rtt = chosen ? num(chosen.currentRoundTripTime) : null;
    return {
      rttMs: rtt === null ? null : Math.round(rtt * 1000),
      fps: Math.round(((sample.frames - previous.frames) / seconds) * 10) / 10,
      lossPct: packets > 0 ? Math.round((Math.max(0, sample.lost - previous.lost) / packets) * 1000) / 10 : 0,
      delayMs: emitted > 0 ? Math.round(((sample.buffered - previous.buffered) / emitted) * 1000) : null,
      kbps: Math.round(((sample.bytes - previous.bytes) * 8) / seconds / 1000),
      freezes: Math.max(0, sample.freezes - previous.freezes),
      active: lastInputAt >= previous.at,
      relay: !!((local && local.candidateType === "relay") || (remote && remote.candidateType === "relay"))
    };
  }
  function sampleQuality() {
    setTimeout(sampleQuality, QUALITY_EVERY_MS);
    // A hidden page decodes nothing: its numbers would call every picture slow.
    if (state !== "connected" || document.hidden) { lastSample = null; return; }
    var pc = webrtc.peerConnection;
    if (!pc || typeof pc.getStats !== "function") return;
    try {
      pc.getStats().then(function (report) {
        var quality = readQuality(report, Date.now());
        if (quality) post({ state: "quality", quality: quality });
      }).catch(function () {});
    } catch (e) {}
  }
  setTimeout(sampleQuality, QUALITY_EVERY_MS);

  // This frame's own stream cookie lives two minutes; re-opened signalling
  // needs it, so the page keeps it fresh at the cadence the server names.
  var cookieEvery = 0;
  function refreshCookie() {
    if (typeof fetch !== "function") return;
    var again = function () { if (cookieEvery > 0) setTimeout(refreshCookie, cookieEvery * 1000); };
    fetch("matrx-cookie", { method: "POST", credentials: "same-origin", cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (body) {
        var every = body && Number(body.refresh_in_seconds);
        if (every > 0) cookieEvery = every;
        again();
      })
      .catch(again);
  }
  refreshCookie();
  window.addEventListener("pagehide", function () { setState("disconnected"); });

  // Keyboard. Guacamole keeps its own record of held keys; a key released while
  // this page had no focus (Cmd+Tab, switching tabs, a click in the parent page)
  // never sends its keyup, so the machine saw a modifier held forever and every
  // later key became a shortcut: typing "stopped" while the mouse worked.
  function keyboard() { return webrtc.input ? webrtc.input.keyboard : null; }
  // Keypad keys always type their digit or operator. Guacamole sends keypad
  // keysyms (KP_1, or KP_End when the client's NumLock is off; a Mac keyboard
  // has no NumLock at all), and the machine's Chrome typed nothing for them
  // even with X's NumLock on (2026-10-17). The physical key (event.code)
  // decides; the keypad keysym is the fallback when no code was seen.
  var KEYPAD_CODE = {
    Numpad0: 0x30, Numpad1: 0x31, Numpad2: 0x32, Numpad3: 0x33, Numpad4: 0x34,
    Numpad5: 0x35, Numpad6: 0x36, Numpad7: 0x37, Numpad8: 0x38, Numpad9: 0x39,
    NumpadDecimal: 0x2e, NumpadAdd: 0x2b, NumpadSubtract: 0x2d, NumpadMultiply: 0x2a,
    NumpadDivide: 0x2f, NumpadEnter: 0xff0d, NumpadEqual: 0x3d, NumpadComma: 0x2c
  };
  var KEYPAD_KEYSYM = {
    0xffb0: 0x30, 0xffb1: 0x31, 0xffb2: 0x32, 0xffb3: 0x33, 0xffb4: 0x34,
    0xffb5: 0x35, 0xffb6: 0x36, 0xffb7: 0x37, 0xffb8: 0x38, 0xffb9: 0x39,
    0xff9e: 0x30, 0xff9c: 0x31, 0xff99: 0x32, 0xff9b: 0x33, 0xff96: 0x34,
    0xff9d: 0x35, 0xff98: 0x36, 0xff95: 0x37, 0xff97: 0x38, 0xff9a: 0x39,
    0xffae: 0x2e, 0xff9f: 0x2e, 0xffab: 0x2b, 0xffad: 0x2d, 0xffaa: 0x2a,
    0xffaf: 0x2f, 0xff8d: 0xff0d, 0xffbd: 0x3d, 0xffac: 0x2c
  };
  var lastCode = "";
  function rememberCode(event) { lastCode = (event && event.code) || ""; }
  // Capture phase on window, registered before Guacamole attaches, so the
  // code is known when Guacamole hands over the keysym for the same event.
  window.addEventListener("keydown", rememberCode, true);
  window.addEventListener("keypress", rememberCode, true);
  window.addEventListener("keyup", rememberCode, true);
  var sentFor = {};
  function keypadKeysym(keysym) {
    if (Object.prototype.hasOwnProperty.call(KEYPAD_CODE, lastCode)) return KEYPAD_CODE[lastCode];
    if (Object.prototype.hasOwnProperty.call(KEYPAD_KEYSYM, keysym)) return KEYPAD_KEYSYM[keysym];
    return keysym;
  }
  window.__matrxKeypadKeysym = keypadKeysym;

  // Copy, cut and paste between the person's computer and the machine
  // (2026-11-19: the owner's shortcuts did nothing). Selkies' own page sends
  // the person's clipboard only when this window gains focus, and takes the
  // machine's clipboard only if clipboard permission was ALREADY granted when
  // it loaded; nothing ever asked, so neither direction worked. Here the
  // shortcut itself does the hand-off:
  //   paste (Ctrl+V, Ctrl+Shift+V): read the person's clipboard, send it to
  //     the machine ("cw,<base64>"), THEN send the keys;
  //   copy / cut (Ctrl+C, Ctrl+X): send the keys, then ask the machine for its
  //     clipboard ("cr"); what comes back is written to the person's clipboard.
  // A Mac's Command key is the machine's Control: the machine is Linux, where
  // Command (Super) does nothing. Command+W/T/N/Q still belong to the person's
  // own browser, which never lets a page see them.
  // A browser that refuses the clipboard is told to the app:
  //   {type:"matrx-stream", state:"clipboard", ok:false, way:"in"|"out"}
  // ("in" = the person's clipboard could not be read, "out" = not written),
  // and ok:true once it works again.
  var CONTROL_L = 0xffe3, CONTROL_R = 0xffe4, SHIFT_L = 0xffe1, SHIFT_R = 0xffe2;
  var MAC_COMMAND = { 0xffe7: true, 0xffe8: true, 0xffeb: true, 0xffec: true };
  var isMac = typeof navigator !== "undefined" && /Mac|iPhone|iPad/.test(navigator.platform || "");
  var KEY_V = { 0x76: true, 0x56: true };
  var KEY_COPY = { 0x63: true, 0x43: true, 0x78: true, 0x58: true };
  var PASTE_SETTLE_MS = 60;
  var COPY_SETTLE_MS = 300;
  var held = {};
  var swallowed = {};
  var pasting = false;
  var sendDown = null;
  var sendUp = null;
  var clipboardOk = { "in": true, out: true };
  function clipboardResult(way, ok) {
    if (clipboardOk[way] === ok) return;
    clipboardOk[way] = ok;
    post({ state: "clipboard", ok: ok, way: way });
  }
  function remoteKeysym(keysym) {
    if (isMac && MAC_COMMAND[keysym]) return CONTROL_L;
    return keypadKeysym(keysym);
  }
  function controlHeld() { return !!(held[CONTROL_L] || held[CONTROL_R]); }
  function localClipboard() {
    try {
      if (typeof navigator !== "undefined" && navigator.clipboard && navigator.clipboard.readText) {
        return navigator.clipboard.readText();
      }
    } catch (e) {}
    return Promise.reject(new Error("no clipboard"));
  }
  function sendClipboardToMachine() {
    return localClipboard().then(function (text) {
      clipboardResult("in", true);
      if (text) webrtc.sendDataChannelMessage("cw," + stringToBase64(text));
    }, function () {
      clipboardResult("in", false);
    });
  }
  function pasteChord(vKeysym) {
    if (pasting) return;
    pasting = true;
    var shift = !!(held[SHIFT_L] || held[SHIFT_R]);
    sendClipboardToMachine().then(function () {
      // The machine sets its clipboard before the keys arrive.
      setTimeout(function () {
        pasting = false;
        if (!sendDown || !sendUp) return;
        // A permission prompt blurs this page, which releases every held key.
        var stillHeld = controlHeld();
        if (!stillHeld) {
          sendDown(CONTROL_L);
          if (shift) sendDown(SHIFT_L);
        }
        sendDown(vKeysym);
        sendUp(vKeysym);
        if (!stillHeld) {
          if (shift) sendUp(SHIFT_L);
          sendUp(CONTROL_L);
        }
      }, PASTE_SETTLE_MS);
    });
  }
  function askMachineClipboard() {
    setTimeout(function () {
      try { webrtc.sendDataChannelMessage("cr"); } catch (e) {}
    }, COPY_SETTLE_MS);
  }
  // Whatever the machine copies lands on the person's clipboard (Selkies' own
  // handler wrote it only when permission had been granted before page load).
  webrtc.onclipboardcontent = function (content) {
    try {
      if (typeof navigator === "undefined" || !navigator.clipboard || !navigator.clipboard.writeText) {
        clipboardResult("out", false);
        return;
      }
      navigator.clipboard.writeText(content).then(
        function () { clipboardResult("out", true); },
        function () { clipboardResult("out", false); }
      );
    } catch (e) { clipboardResult("out", false); }
  };
  // A right-click menu's Paste reads the machine's clipboard: bring it up to date first.
  window.addEventListener("pointerdown", function (event) {
    if (event && event.button === 2) sendClipboardToMachine();
  }, true);

  function guardKeyboard() {
    var k = keyboard();
    if (!k || k.__matrxGuarded) return;
    k.__matrxGuarded = true;
    var down = k.onkeydown;
    var up = k.onkeyup;
    sendDown = down;
    sendUp = up;
    // The machine's NumLock is on from the start; the client never toggles it.
    k.onkeydown = function (keysym) {
      if (keysym === NUM_LOCK || !down) return;
      var sent = remoteKeysym(keysym);
      if (controlHeld() && KEY_V[sent]) {
        // Paste: the keys go out after the clipboard does (pasteChord).
        swallowed[keysym] = true;
        pasteChord(sent);
        return;
      }
      sentFor[keysym] = sent;
      held[sent] = true;
      var result = down(sent);
      if (controlHeld() && KEY_COPY[sent]) askMachineClipboard();
      return result;
    };
    k.onkeyup = function (keysym) {
      if (keysym === NUM_LOCK || !up) return;
      if (swallowed[keysym]) {
        delete swallowed[keysym];
        return;
      }
      var sent = Object.prototype.hasOwnProperty.call(sentFor, keysym) ? sentFor[keysym] : remoteKeysym(keysym);
      delete sentFor[keysym];
      delete held[sent];
      return up(sent);
    };
  }
  function releaseAll() {
    // Guacamole's reset fires a key-up for every key it holds: each must go out
    // as the keysym it was pressed as (sentFor), never re-read from the last
    // key event's code (a held Shift used to be released as keypad "1").
    lastCode = "";
    var k = keyboard();
    if (k) { try { k.reset(); } catch (e) {} }
    sentFor = {};
    held = {};
    swallowed = {};
    try { webrtc.sendDataChannelMessage("kr"); } catch (e) {}
  }
  function focusInput() {
    try { window.focus(); } catch (e) {}
    try { video.focus({ preventScroll: true }); } catch (e) {}
  }
  function reattach() {
    var input = webrtc.input;
    if (!input || !input.keyboard) return;
    try { input.detach_context(); input.attach_context(); } catch (e) {}
    guardKeyboard();
  }
  var onChannelOpen = webrtc.ondatachannelopen;
  webrtc.ondatachannelopen = function () {
    if (onChannelOpen) onChannelOpen();
    guardKeyboard();
    focusInput();
  };
  window.addEventListener("blur", releaseAll);
  window.addEventListener("focus", releaseAll);
  document.addEventListener("visibilitychange", releaseAll);
  video.addEventListener("pointerdown", focusInput);

  window.addEventListener("message", function (event) {
    if (!parentOrigin || event.origin !== parentOrigin) return;
    var data = event.data;
    if (!data || data.type !== "matrx-stream-cmd") return;
    if (data.cmd === "keyboard-reset") {
      releaseAll();
      reattach();
      focusInput();
      post({ state: "keyboard", ok: true });
    } else if (data.cmd === "focus") {
      focusInput();
    }
  });

  setState("connecting");
})();

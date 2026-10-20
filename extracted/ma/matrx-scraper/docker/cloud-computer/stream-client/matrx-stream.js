/* Cloud Computer screen page contract (loaded after Selkies' app.js).
 *
 * To the embedding app (window.parent, only to the allowed embedding origin):
 *   {type:"matrx-stream", state:"connecting"|"connected"|"reconnecting"|"disconnected", ts}
 *   "connected" means a picture is on screen: the video peer is connected AND
 *   a frame arrived after that connection (a connected peer whose first frame
 *   is still on its way left the app showing this page's black loader).
 *   {type:"matrx-stream", state:"keyboard", ok:true, ts}   after a keyboard reset
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
  function guardKeyboard() {
    var k = keyboard();
    if (!k || k.__matrxGuarded) return;
    k.__matrxGuarded = true;
    var down = k.onkeydown;
    var up = k.onkeyup;
    // The machine's NumLock is on from the start; the client never toggles it.
    k.onkeydown = function (keysym) {
      if (keysym === NUM_LOCK || !down) return;
      var sent = keypadKeysym(keysym);
      sentFor[keysym] = sent;
      return down(sent);
    };
    k.onkeyup = function (keysym) {
      if (keysym === NUM_LOCK || !up) return;
      var sent = Object.prototype.hasOwnProperty.call(sentFor, keysym) ? sentFor[keysym] : keypadKeysym(keysym);
      delete sentFor[keysym];
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

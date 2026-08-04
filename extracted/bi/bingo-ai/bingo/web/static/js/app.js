// Bingo web IDE — SPA controller.
(function () {
  "use strict";
  var BOOT = window.__BINGO__ || { token: "", port: 0, lang: "en" };
  var $ = function (id) { return document.getElementById(id); };

  var state = {
    mode: "dev",          // "dev" | "pentest"
    lang: BOOT.lang,
    tabs: [],             // [{path,model,dirty,view}]
    active: null,         // active tab path
    editor: null,         // monaco editor instance
    curAssistant: null,   // streaming assistant bubble
  };

  // ── token-aware fetch ────────────────────────────────────────
  function api(path, opts) {
    opts = opts || {};
    opts.headers = Object.assign({ "x-bingo-token": BOOT.token,
      "content-type": "application/json" }, opts.headers || {});
    return fetch(path, opts).then(function (r) {
      if (!r.ok) return r.json().then(function (e) { throw new Error(e.error || r.status); });
      return r.json();
    });
  }
  function post(path, body) {
    return api(path, { method: "POST", body: JSON.stringify(body || {}) });
  }

  function setStatus(busy) {
    var el = $("status");
    el.className = busy ? "busy" : "ready";
    el.title = window.t(busy ? "busy" : "ready", state.lang);
    $("btn-stop").hidden = !busy;
  }

  window.BINGO = { api: api, post: post, state: state, $: $, setStatus: setStatus, BOOT: BOOT };

  // ── Monaco editor + tabs ─────────────────────────────────────
  var LANG_MAP = {
    js: "javascript", ts: "typescript", py: "python", html: "html", htm: "html",
    css: "css", json: "json", md: "markdown", sh: "shell", yml: "yaml",
    yaml: "yaml", xml: "xml", sql: "sql", php: "php", go: "go", rs: "rust",
    java: "java", c: "c", cpp: "cpp", rb: "ruby", txt: "plaintext",
  };
  function langOf(path) {
    var ext = (path.split(".").pop() || "").toLowerCase();
    return LANG_MAP[ext] || "plaintext";
  }

  function initEditor() {
    require.config({ paths: { vs: "/static/vs" } });
    return new Promise(function (resolve) {
      require(["vs/editor/editor.main"], function () {
        monaco.editor.defineTheme("bingo", {
          base: "vs-dark", inherit: true, rules: [],
          colors: {
            "editor.background": "#17181c",
            "editor.lineHighlightBackground": "#1f2027",
            "editorLineNumber.foreground": "#565863",
            "editorLineNumber.activeForeground": "#adaeb8",
            "editorGutter.background": "#17181c",
            "editorCursor.foreground": "#9d86f0",
            "editor.selectionBackground": "#6e56cf3d",
            "editorIndentGuide.background1": "#2b2c34",
            "editorWidget.background": "#1a1b1f",
            "editorWidget.border": "#2b2c34",
            "scrollbarSlider.background": "#383a4466",
          },
        });
        state.editor = monaco.editor.create($("editor"), {
          value: "", language: "plaintext", theme: "bingo",
          automaticLayout: true, fontSize: 13, minimap: { enabled: false },
          scrollBeyondLastLine: false, padding: { top: 14 },
          fontFamily: "'Geist Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace",
          fontLigatures: true, smoothScrolling: true, cursorBlinking: "smooth",
          renderLineHighlight: "gutter", roundedSelection: true,
        });
        state.editor.onDidChangeModelContent(function () {
          var t = tabByPath(state.active);
          if (t && !t._quiet) { t.dirty = true; renderTabs(); }
        });
        state.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, saveActive);
        resolve();
      });
    });
  }

  function tabByPath(p) {
    for (var i = 0; i < state.tabs.length; i++)
      if (state.tabs[i].path === p) return state.tabs[i];
    return null;
  }

  function openFile(path) {
    var t = tabByPath(path);
    if (t) { activateTab(path); return; }
    api("/api/file?path=" + encodeURIComponent(path)).then(function (d) {
      var model = monaco.editor.createModel(d.text, langOf(path));
      state.tabs.push({ path: path, model: model, dirty: false });
      activateTab(path);
      renderTabs();
    }).catch(function (e) { pushMsg("err", String(e)); });
  }

  function activateTab(path) {
    state.active = path;
    var t = tabByPath(path);
    if (t && state.editor) {
      t._quiet = true;
      state.editor.setModel(t.model);
      t._quiet = false;
    }
    $("welcome").style.display = "none";
    renderTabs();
    renderTree();
  }

  function closeTab(path, ev) {
    if (ev) ev.stopPropagation();
    var i = state.tabs.findIndex(function (t) { return t.path === path; });
    if (i < 0) return;
    state.tabs[i].model.dispose();
    state.tabs.splice(i, 1);
    if (state.active === path) {
      var next = state.tabs[Math.max(0, i - 1)];
      if (next) activateTab(next.path);
      else { state.active = null; state.editor.setModel(null);
        $("welcome").style.display = "flex"; renderTabs(); }
    } else { renderTabs(); }
  }

  function renderTabs() {
    var box = $("tabs"); box.innerHTML = "";
    state.tabs.forEach(function (t) {
      var el = document.createElement("div");
      el.className = "tab" + (t.path === state.active ? " active" : "") +
        (t.dirty ? " dirty" : "");
      el.onclick = function () { activateTab(t.path); };
      var name = document.createElement("span");
      name.textContent = t.path.split("/").pop();
      var x = document.createElement("span");
      x.className = "x"; x.textContent = "✕";
      x.onclick = function (e) { closeTab(t.path, e); };
      el.appendChild(name); el.appendChild(x); box.appendChild(el);
    });
  }

  function saveActive() {
    var t = tabByPath(state.active);
    if (!t) return;
    post("/api/file", { path: t.path, text: t.model.getValue() }).then(function () {
      t.dirty = false; renderTabs();
    }).catch(function (e) { pushMsg("err", String(e)); });
  }

  window.BINGO.editor = { init: initEditor, open: openFile, save: saveActive,
    tabByPath: tabByPath, activateTab: activateTab };

  // ── file tree (lazy dir expansion) ───────────────────────────
  var treeState = { open: {}, entries: {} };  // path -> expanded, path -> children

  function loadDir(path) {
    return api("/api/files?path=" + encodeURIComponent(path)).then(function (d) {
      treeState.entries[path] = d.entries; return d.entries;
    });
  }

  function renderTree() {
    var ul = $("tree"); ul.innerHTML = "";
    renderLevel(ul, "", 0);
  }

  function renderLevel(ul, path, depth) {
    var entries = treeState.entries[path] || [];
    entries.forEach(function (e) {
      var li = document.createElement("li");
      li.className = (e.dir ? "dir" : "file") + (e.path === state.active ? " active" : "");
      var pad = "";
      for (var i = 0; i < depth; i++) pad += "  ";
      var icon = e.dir ? (treeState.open[e.path] ? "▾ " : "▸ ") : "  ";
      li.textContent = pad + icon + e.name;
      li.onclick = function (ev) { ev.stopPropagation(); onTreeClick(e); };
      ul.appendChild(li);
      if (e.dir && treeState.open[e.path]) renderLevel(ul, e.path, depth + 1);
    });
  }

  function onTreeClick(e) {
    if (e.dir) {
      if (treeState.open[e.path]) { treeState.open[e.path] = false; renderTree(); }
      else {
        treeState.open[e.path] = true;
        (treeState.entries[e.path] ? Promise.resolve() : loadDir(e.path))
          .then(renderTree);
      }
    } else { openFile(e.path); }
  }

  window.BINGO.tree = { load: loadDir, render: renderTree };
  window.renderTree = renderTree;

  // ── chat ─────────────────────────────────────────────────────
  function pushMsg(role, text) {
    var el = document.createElement("div");
    el.className = "msg " + role;
    el.textContent = text;
    $("messages").appendChild(el);
    $("messages").scrollTop = $("messages").scrollHeight;
    return el;
  }
  window.pushMsg = pushMsg;

  function appendAssistant(text) {
    if (!state.curAssistant) state.curAssistant = pushMsg("assistant", "");
    state.curAssistant.textContent += text;
    $("messages").scrollTop = $("messages").scrollHeight;
  }

  function addFinding(f) {
    var box = $("findings");
    var el = document.createElement("div");
    var sev = (f.severity || "info").toLowerCase();
    el.className = "finding " + sev;
    el.innerHTML = '<span class="sev">' + sev.toUpperCase() + "</span> " +
      escapeHtml(f.title || f.name || f.type || "finding");
    box.appendChild(el);
    box.scrollTop = box.scrollHeight;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; });
  }

  // ── WebSocket event stream ───────────────────────────────────
  function connectWS() {
    var url = "ws://" + location.host + "/ws?token=" + encodeURIComponent(BOOT.token);
    var ws = new WebSocket(url);
    ws.onmessage = function (ev) {
      var m; try { m = JSON.parse(ev.data); } catch (e) { return; }
      handleEvent(m.type, m.data || {});
    };
    ws.onclose = function () { setTimeout(connectWS, 1500); };
  }

  function handleEvent(type, data) {
    switch (type) {
      case "ping": break;
      case "dev_chunk": appendAssistant(data.text || ""); break;
      case "dev_done": onDevDone(data); break;
      case "dev_error": case "engine_error": case "auto_error":
        state.curAssistant = null; pushMsg("err", data.error || "error"); setStatus(false); break;
      case "stream_chunk": appendAssistant(data.text || data.chunk || ""); break;
      case "finding": addFinding(data); break;
      case "tool_result": pushMsg("tool", (data.summary || data.text || "").slice(0, 800)); break;
      case "auto_log": pushMsg("tool", data.msg || ""); break;
      case "auto_start": pushMsg("tool", "▶ " + data.mode + " " + (data.target || "")); break;
      case "auto_done": pushMsg("tool", "✓ " + data.mode + " done"); setStatus(false); break;
      case "session_done": case "_loop_exit": state.curAssistant = null; setStatus(false); break;
    }
  }

  function onDevDone(data) {
    state.curAssistant = null;
    setStatus(false);
    if (data.file && data.file.text) {
      // model returned a full file → drop into a tab, autosave.
      var path = data.file.name || (state.active || "untitled.txt");
      window.BINGO.editor.open(path);
      setTimeout(function () {
        var t = window.BINGO.editor.tabByPath(path);
        if (t) { t.model.setValue(data.file.text); }
      }, 120);
    }
  }

  window.BINGO.chat = { push: pushMsg, connect: connectWS, handle: handleEvent, addFinding: addFinding };

  // ── send / mode / controls ───────────────────────────────────
  function send() {
    var text = $("input").value.trim();
    if (!text) return;
    if (text.charAt(0) === "/") {
      var sp = text.indexOf(" ");
      var name = sp < 0 ? text : text.slice(0, sp);
      var arg = sp < 0 ? "" : text.slice(sp + 1).trim();
      $("input").value = ""; hideSlash();
      runSlash(name, arg);
      return;
    }
    $("input").value = "";
    pushMsg("user", text);
    setStatus(true);
    var openTab = tabByPath(state.active);
    if (state.mode === "dev") {
      post("/api/dev/ask", {
        message: text,
        file_name: state.active || "",
        file_text: openTab ? openTab.model.getValue() : "",
      }).catch(function (e) { pushMsg("err", String(e)); setStatus(false); });
    } else {
      post("/api/pentest/start", { message: text }).then(function (r) {
        if (!r.ok) { pushMsg("err", "No target URL detected."); setStatus(false); }
      }).catch(function (e) { pushMsg("err", String(e)); setStatus(false); });
    }
  }

  // ── slash command palette ───────────────────────────────────
  var CMDS = [];
  var slash = { open: false, items: [], sel: 0 };
  var ARG_CMDS = { "/login": 1, "/cred": 1, "/hint": 1, "/crack": 1,
    "/report": 1, "/load": 1, "/session": 1 };

  function loadCommands() {
    api("/api/commands").then(function (d) { CMDS = d.commands || []; });
  }

  function updateSlash() {
    var v = $("input").value;
    if (v.charAt(0) !== "/" || /\s/.test(v)) { hideSlash(); return; }
    var q = v.slice(1).toLowerCase();
    var items = CMDS.filter(function (c) {
      return c.cmd.slice(1).toLowerCase().indexOf(q) === 0;
    });
    if (!items.length) { hideSlash(); return; }
    slash.items = items; slash.sel = 0; slash.open = true; renderSlash();
  }

  function renderSlash() {
    var box = $("slash-menu"); box.innerHTML = "";
    slash.items.forEach(function (c, i) {
      var el = document.createElement("div");
      el.className = "slash-item" + (i === slash.sel ? " sel" : "");
      var a = document.createElement("span"); a.className = "sc-cmd"; a.textContent = c.cmd;
      var b = document.createElement("span"); b.className = "sc-desc"; b.textContent = c.desc;
      el.appendChild(a); el.appendChild(b);
      el.onmousedown = function (e) { e.preventDefault(); pickSlash(i); };
      box.appendChild(el);
    });
    box.hidden = false;
  }

  function hideSlash() { slash.open = false; $("slash-menu").hidden = true; }

  function pickSlash(i) {
    var c = slash.items[i]; if (!c) return;
    hideSlash();
    if (ARG_CMDS[c.cmd]) { $("input").value = c.cmd + " "; $("input").focus(); }
    else { $("input").value = ""; runSlash(c.cmd, ""); }
  }

  function slashKey(e) {
    if (!slash.open) return false;
    if (e.key === "ArrowDown") { slash.sel = (slash.sel + 1) % slash.items.length; renderSlash(); e.preventDefault(); return true; }
    if (e.key === "ArrowUp") { slash.sel = (slash.sel - 1 + slash.items.length) % slash.items.length; renderSlash(); e.preventDefault(); return true; }
    if (e.key === "Enter" || e.key === "Tab") { pickSlash(slash.sel); e.preventDefault(); return true; }
    if (e.key === "Escape") { hideSlash(); e.preventDefault(); return true; }
    return false;
  }

  function runSlash(name, arg) {
    post("/api/command", { name: name, arg: arg }).then(function (r) {
      if (r.action) clientAction(r.action);
      if (r.text) pushMsg(r.ok === false ? "err" : "tool", r.text);
    }).catch(function (e) { pushMsg("err", String(e)); });
  }

  function clientAction(a) {
    if (a === "clear") $("messages").innerHTML = "";
    else if (a === "help") showHelp();
    else if (a === "history") { $("messages").innerHTML = ""; restoreHistory(); }
    else if (a === "export") copyTranscript();
    else if (a === "retry") retryLast();
    else if (a === "settings") openSettings();
    else if (a === "quit") pushMsg("tool", window.t("quit_hint", state.lang));
  }

  function showHelp() {
    var lines = CMDS.map(function (c) { return c.cmd + "  —  " + c.desc; });
    pushMsg("tool", lines.join("\n"));
  }

  function retryLast() {
    var us = $("messages").querySelectorAll(".msg.user");
    if (!us.length) return;
    $("input").value = us[us.length - 1].textContent; send();
  }

  // ── settings modal ───────────────────────────────────────────
  function openSettings() {
    $("mode-select").value = state.mode;
    $("settings-modal").hidden = false;
  }
  function closeSettings() { $("settings-modal").hidden = true; }

  function setMode(mode) {
    state.mode = mode;
    document.body.setAttribute("data-mode", mode);
    var ml = $("mode-label"); if (ml) ml.textContent = mode.toUpperCase();
    document.querySelectorAll(".chat-tab").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-mode") === mode);
    });
    $("findings").style.display = mode === "pentest" ? "block" : "none";
  }

  function copyTranscript() {
    var lines = [];
    $("messages").querySelectorAll(".msg").forEach(function (m) {
      lines.push(m.textContent);
    });
    var text = lines.join("\n\n");
    if (!text) { pushMsg("tool", window.t("empty_copy", state.lang)); return; }
    navigator.clipboard.writeText(text).then(function () {
      pushMsg("tool", window.t("copied", state.lang));
    });
  }

  function restoreHistory() {
    api("/api/history").then(function (d) {
      (d.turns || []).forEach(function (turn) {
        pushMsg(turn.role === "user" ? "user" : "assistant", turn.content || "");
      });
    });
  }

  function loadConfig() {
    return api("/api/config").then(function (c) {
      state.lang = c.lang; window.__BINGO__.lang = c.lang;
      state.cfg = c;
      $("lang-select").value = c.lang;
      $("root-path").textContent = c.root;
      renderModels(c);
      renderProviders(c);
      window.applyI18n(c.lang);
    });
  }

  function renderModels(c) {
    var sel = $("model-select"); sel.innerHTML = "";
    (c.models || []).forEach(function (m) {
      var o = document.createElement("option");
      o.value = m.name; o.textContent = m.name;
      if (m.name === c.active_model) o.selected = true;
      sel.appendChild(o);
    });
    var list = $("model-list"); if (!list) return;
    list.innerHTML = "";
    (c.models || []).forEach(function (m) {
      var row = document.createElement("div"); row.className = "model-item";
      var active = m.name === c.active_model;
      var nm = document.createElement("div"); nm.className = "mi-name";
      nm.innerHTML = (active ? '<span class="mi-active">✓</span>' : "") +
        esc(m.name) + ' <span class="mi-prov">' + esc(m.provider) + "</span>";
      var del = document.createElement("button");
      del.className = "mi-del"; del.textContent = window.t("delete", state.lang) || "Delete";
      del.onclick = function () { deleteModel(m.name); };
      row.appendChild(nm); row.appendChild(del);
      list.appendChild(row);
    });
  }

  function renderProviders(c) {
    var ps = $("add-provider"); if (!ps) return;
    ps.innerHTML = "";
    (c.providers || []).forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.id; o.textContent = p.label;
      o.setAttribute("data-url", p.base_url);
      o.setAttribute("data-model", p.default_model);
      ps.appendChild(o);
    });
    fillProviderDefaults();
  }

  function fillProviderDefaults() {
    var ps = $("add-provider"); if (!ps || !ps.selectedOptions.length) return;
    var o = ps.selectedOptions[0];
    $("add-url").placeholder = o.getAttribute("data-url") || "Base URL";
    $("add-model").placeholder = o.getAttribute("data-model") || "Model name";
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch];
    });
  }

  function addModel() {
    var msg = $("add-msg"); msg.className = "add-msg";
    var body = {
      provider: $("add-provider").value,
      api_key: $("add-key").value,
      base_url: $("add-url").value,
      model: $("add-model").value,
      alias: $("add-alias").value,
    };
    post("/api/model/add", body).then(function () {
      $("add-key").value = ""; $("add-url").value = "";
      $("add-model").value = ""; $("add-alias").value = "";
      msg.className = "add-msg ok";
      msg.textContent = window.t("model_added", state.lang) || "Model added";
      loadConfig();
    }).catch(function (e) {
      msg.className = "add-msg err"; msg.textContent = e.message || "error";
    });
  }

  function deleteModel(name) {
    post("/api/model/delete", { name: name }).then(loadConfig).catch(function () {});
  }

  function wire() {
    $("btn-send").onclick = send;
    $("btn-stop").onclick = function () { post("/api/pentest/stop", {}); setStatus(false); };
    $("btn-copy").onclick = copyTranscript;
    $("input").addEventListener("keydown", function (e) {
      if (slashKey(e)) return;
      if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); send(); }
    });
    $("input").addEventListener("input", updateSlash);
    $("btn-settings").onclick = openSettings;
    $("settings-close").onclick = closeSettings;
    $("settings-modal").onclick = function (e) {
      if (e.target === $("settings-modal")) closeSettings();
    };
    $("mode-select").onchange = function () { setMode(this.value); };
    $("btn-cmds").onclick = function () {
      var inp = $("input"); inp.value = "/"; inp.focus(); updateSlash();
    };
    document.querySelectorAll(".chat-tab").forEach(function (b) {
      b.onclick = function () { setMode(b.getAttribute("data-mode")); };
    });
    document.querySelectorAll(".chip").forEach(function (c) {
      c.onclick = function () {
        setMode(c.getAttribute("data-mode") || "dev");
        var inp = $("input");
        inp.value = c.textContent.trim() + " ";
        inp.focus();
      };
    });
    $("lang-select").onchange = function () {
      post("/api/lang", { lang: this.value }).then(function (d) {
        state.lang = d.lang; window.__BINGO__.lang = d.lang; window.applyI18n(d.lang);
      });
    };
    $("model-select").onchange = function () {
      post("/api/model", { name: this.value }).then(loadConfig);
    };
    $("add-provider").onchange = fillProviderDefaults;
    $("add-submit").onclick = addModel;
  }

  // ── boot ─────────────────────────────────────────────────────
  window.addEventListener("DOMContentLoaded", function () {
    window.applyI18n(state.lang);
    wire();
    setMode("dev");
    loadConfig();
    loadCommands();
    loadDir("").then(renderTree);
    restoreHistory();
    connectWS();
    initEditor();
  });
})();

/* ═══════════════════════════════════════════════
   app.js — State machine, mode switching, API, polling
   ═══════════════════════════════════════════════ */

const Yantrik = (() => {
  "use strict";

  // ── State ──
  const State = {
    AI_IDLE: "ai-idle",
    AI_CHATTING: "ai-chat",
    GENERIC: "generic-home",
  };

  let currentState = State.AI_IDLE;
  let waiting = false; // LLM is generating
  let pollTimer = null;
  let lastStatus = null;

  // ── DOM refs ──
  const screens = {
    [State.AI_IDLE]: null,
    [State.AI_CHATTING]: null,
    [State.GENERIC]: null,
  };

  // ── API ──
  const api = {
    async post(path, body) {
      const resp = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
      return resp.json();
    },

    async get(path) {
      const resp = await fetch(path);
      if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
      return resp.json();
    },

    chat(message) { return this.post("/chat", { message }); },
    status() { return this.get("/status"); },
    urges() { return this.get("/urges"); },
    history(limit = 20) { return this.get(`/history?limit=${limit}`); },
    suppress(urgeId) { return this.post(`/urges/${urgeId}/suppress`, {}); },
  };

  // ── Screen transitions ──
  function switchTo(state) {
    if (state === currentState) return;

    const prev = screens[currentState];
    const next = screens[state];

    if (prev) prev.classList.remove("screen--active");
    if (next) next.classList.add("screen--active");

    currentState = state;
    localStorage.setItem("yantrik-mode", state);
    updatePolling();
  }

  // ── Polling ──
  function updatePolling() {
    if (pollTimer) clearInterval(pollTimer);

    const intervals = {
      [State.AI_IDLE]: 30000,
      [State.AI_CHATTING]: 5000,
      [State.GENERIC]: 15000,
    };

    const interval = intervals[currentState] || 15000;
    pollTimer = setInterval(poll, interval);
    poll(); // immediate first poll
  }

  async function poll() {
    try {
      const status = await api.status();
      lastStatus = status;

      // Update memory count
      const memEl = document.getElementById("memory-count");
      if (memEl) memEl.textContent = status.memory_count;

      // Update status dot
      const dot = document.querySelector(".status-dot");
      if (dot) dot.classList.remove("status-dot--offline");

      // Proactive orb state
      const orb = document.getElementById("orb");
      if (orb) {
        if (status.pending_urges > 0) {
          orb.classList.add("orb--proactive");
        } else {
          orb.classList.remove("orb--proactive");
        }
      }

      // If on generic mode, also fetch urges for cards
      if (currentState === State.GENERIC && typeof Glance !== "undefined") {
        const urgeData = await api.urges();
        Glance.render(urgeData.urges || []);
      }
    } catch (e) {
      // Offline
      const dot = document.querySelector(".status-dot");
      if (dot) dot.classList.add("status-dot--offline");
    }
  }

  // ── Orb interaction ──
  function onOrbTap() {
    switchTo(State.AI_CHATTING);
    if (typeof Chat !== "undefined") Chat.focus();
  }

  // ── Boot sequence ──
  async function bootSequence() {
    const bootEl = document.getElementById("boot");
    const statusEl = document.getElementById("boot-status");
    if (!bootEl) return endBoot();

    let healthOk = false;
    let fast = false;
    const bootStart = Date.now();

    // Poll /health — up to 10 attempts
    for (let i = 0; i < 10; i++) {
      try {
        const t0 = Date.now();
        const resp = await fetch("/health");
        if (resp.ok) {
          healthOk = true;
          if (Date.now() - t0 < 1000 && i === 0) fast = true;
          break;
        }
      } catch (_) { /* not ready yet */ }
      await new Promise(r => setTimeout(r, 1000));
    }

    if (fast) bootEl.querySelector(".boot")?.classList.add("boot--fast");

    // Fetch status for real data + personality
    if (healthOk) {
      try {
        const status = await api.status();
        const memCount = status.memory_count || 0;
        const lastAgo = status.last_interaction_ago_seconds;
        let agoText = "";
        if (lastAgo < 3600) agoText = `last seen ${Math.round(lastAgo / 60)}m ago`;
        else if (lastAgo < 86400) agoText = `last seen ${Math.round(lastAgo / 3600)}h ago`;
        else agoText = `last seen ${Math.round(lastAgo / 86400)}d ago`;

        if (statusEl) statusEl.textContent = `${memCount} memories \u00b7 ${agoText}`;

        // Apply personality-driven boot variants
        const p = status.personality;
        if (p && p.traits) {
          const traits = {};
          for (const t of p.traits) traits[t.trait_name] = t.score;
          const boot = bootEl.querySelector(".boot");
          if (boot) {
            if ((traits.warmth || 0) > 0.6) boot.classList.add("boot--warm");
            if ((traits.energy || 0) > 0.6) boot.classList.add("boot--eager");
            if ((traits.depth || 0) > 0.6) boot.classList.add("boot--deep");
          }
        }
      } catch (_) {
        if (statusEl) statusEl.textContent = "waking up...";
      }
    } else {
      if (statusEl) statusEl.textContent = "waking up...";
    }

    // Wait for minimum animation time
    const elapsed = Date.now() - bootStart;
    const minTime = fast ? 5000 : 9000;
    if (elapsed < minTime) {
      await new Promise(r => setTimeout(r, minTime - elapsed));
    }

    return endBoot();
  }

  function endBoot() {
    const bootEl = document.getElementById("boot");
    if (!bootEl) return initMain();

    const boot = bootEl.querySelector(".boot");
    if (boot) boot.classList.add("boot--hiding");

    setTimeout(() => {
      bootEl.classList.remove("screen--active");
      initMain();
    }, 800);
  }

  function initMain() {
    // Restore mode from localStorage
    const saved = localStorage.getItem("yantrik-mode");
    if (saved && screens[saved]) {
      currentState = saved;
    }

    screens[currentState].classList.add("screen--active");

    // Orb tap → chat
    const orbContainer = document.querySelector(".orb-container");
    if (orbContainer) orbContainer.addEventListener("click", onOrbTap);

    // Mode switch buttons
    document.getElementById("btn-to-generic")?.addEventListener("click", (e) => {
      e.stopPropagation();
      switchTo(State.GENERIC);
    });
    document.getElementById("btn-to-generic-chat")?.addEventListener("click", () => {
      switchTo(State.GENERIC);
    });
    document.getElementById("btn-to-ai")?.addEventListener("click", () => {
      switchTo(State.AI_IDLE);
    });
    document.getElementById("btn-back")?.addEventListener("click", () => {
      switchTo(State.AI_IDLE);
    });

    // Start polling
    updatePolling();

    // Restore chat history
    if (typeof Chat !== "undefined") Chat.init();
    if (typeof Glance !== "undefined") Glance.init();
  }

  // ── Init ──
  function init() {
    // Cache screen refs
    screens[State.AI_IDLE] = document.getElementById("ai-idle");
    screens[State.AI_CHATTING] = document.getElementById("ai-chat");
    screens[State.GENERIC] = document.getElementById("generic-home");

    // Run boot sequence
    bootSequence();
  }

  document.addEventListener("DOMContentLoaded", init);

  return {
    State,
    api,
    switchTo,
    get currentState() { return currentState; },
    get waiting() { return waiting; },
    set waiting(v) { waiting = v; },
    get lastStatus() { return lastStatus; },
  };
})();

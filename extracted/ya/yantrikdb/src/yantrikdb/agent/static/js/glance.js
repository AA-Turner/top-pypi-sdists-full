/* ═══════════════════════════════════════════════
   glance.js — Glance card rendering for Generic Mode
   ═══════════════════════════════════════════════ */

const Glance = (() => {
  "use strict";

  let container;
  let currentUrges = []; // track for diffing

  // ── Instinct display names ──
  const INSTINCT_LABELS = {
    PatternSurfacing: "pattern",
    Reminder: "reminder",
    EmotionalAwareness: "emotional",
    CheckIn: "check-in",
    FollowUp: "follow-up",
    ConflictAlerting: "conflict",
  };

  // ── Relative time ──
  function timeAgo(timestamp) {
    const seconds = Math.floor(Date.now() / 1000 - timestamp);
    if (seconds < 60) return "just now";
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  }

  // ── Build a single card ──
  function createCard(urge) {
    const card = document.createElement("div");
    card.className = "glance-card";
    card.dataset.urgeId = urge.urge_id;
    card.dataset.instinct = urge.instinct_name || "";

    // Urgency dot (opacity reflects urgency score)
    const dot = document.createElement("div");
    dot.className = "glance-card__urgency";
    dot.style.opacity = Math.max(0.3, urge.urgency || 0.5);
    card.appendChild(dot);

    // Body
    const body = document.createElement("div");
    body.className = "glance-card__body";

    const reason = document.createElement("div");
    reason.className = "glance-card__reason";
    reason.textContent = urge.suggested_message || urge.reason || "Something on my mind...";
    body.appendChild(reason);

    const meta = document.createElement("div");
    meta.className = "glance-card__meta";

    const tag = document.createElement("span");
    tag.className = "glance-card__instinct-tag";
    tag.textContent = INSTINCT_LABELS[urge.instinct_name] || urge.instinct_name || "thought";
    meta.appendChild(tag);

    if (urge.created_at) {
      const time = document.createElement("span");
      time.textContent = timeAgo(urge.created_at);
      meta.appendChild(time);
    }

    if (urge.boost_count > 0) {
      const boost = document.createElement("span");
      boost.textContent = `+${urge.boost_count}`;
      meta.appendChild(boost);
    }

    body.appendChild(meta);
    card.appendChild(body);

    // Tap → open chat with context
    card.addEventListener("click", () => {
      const msg = urge.suggested_message || urge.reason;
      if (msg && typeof Chat !== "undefined") {
        Chat.sendWithContext(`You mentioned: "${msg}" — tell me more about that.`);
      } else {
        Yantrik.switchTo(Yantrik.State.AI_CHATTING);
      }
    });

    return card;
  }

  // ── Render cards (diffing by urge_id) ──
  function render(urges) {
    if (!container) return;

    // Check if urges actually changed
    const newIds = urges.map(u => u.urge_id).join(",");
    const oldIds = currentUrges.map(u => u.urge_id).join(",");
    if (newIds === oldIds) return;

    currentUrges = urges;

    // Clear and rebuild
    container.innerHTML = "";

    if (urges.length === 0) {
      const empty = document.createElement("div");
      empty.className = "glance-empty";
      empty.innerHTML = `
        <div class="glance-empty__orb"></div>
        <div class="glance-empty__text">
          All quiet. Yantrik is thinking in the background.
        </div>
      `;
      container.appendChild(empty);
      return;
    }

    // Sort by urgency (highest first)
    const sorted = [...urges].sort((a, b) => (b.urgency || 0) - (a.urgency || 0));
    for (const urge of sorted) {
      container.appendChild(createCard(urge));
    }
  }

  // ── Init ──
  function init() {
    container = document.getElementById("glance-cards");

    // Initial fetch
    Yantrik.api.urges().then(data => {
      render(data.urges || []);
    }).catch(() => {
      render([]);
    });
  }

  return { init, render };
})();

/* ═══════════════════════════════════════════════
   chat.js — Streaming chat with token-by-token rendering
   ═══════════════════════════════════════════════ */

const Chat = (() => {
  "use strict";

  let messagesEl, inputEl, sendBtn, homeInputEl, homeSendBtn, typingEl;

  // ── Render a message ──
  function addMessage(role, text) {
    if (!messagesEl) return;
    const div = document.createElement("div");
    if (role === "user") {
      div.className = "msg msg--user";
      div.textContent = text;
    } else {
      div.className = "msg msg--yantrik";
      const span = document.createElement("span");
      span.className = "msg__text";
      span.textContent = text;
      div.appendChild(span);
    }
    messagesEl.appendChild(div);
    scrollToBottom();
    return div;
  }

  // Create an empty Yantrik message for streaming into
  function addStreamMessage() {
    if (!messagesEl) return null;
    const div = document.createElement("div");
    div.className = "msg msg--yantrik";
    const span = document.createElement("span");
    span.className = "msg__text";
    div.appendChild(span);
    messagesEl.appendChild(div);
    scrollToBottom();
    return span;
  }

  function scrollToBottom() {
    requestAnimationFrame(() => {
      if (messagesEl) messagesEl.scrollTop = messagesEl.scrollHeight;
    });
  }

  // ── Typing indicator ──
  function showTyping() {
    if (typingEl) typingEl.classList.add("visible");
    scrollToBottom();
  }

  function hideTyping() {
    if (typingEl) typingEl.classList.remove("visible");
  }

  // ── Send message (streaming) ──
  async function send(text) {
    text = text.trim();
    if (!text || Yantrik.waiting) return;

    addMessage("user", text);
    Yantrik.waiting = true;

    // Show thinking state
    showTyping();
    const orb = document.getElementById("orb");
    if (orb) orb.classList.add("orb--thinking");

    try {
      const resp = await fetch("/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

      // Switch from typing indicator to streaming message
      hideTyping();
      if (orb) orb.classList.remove("orb--thinking");
      const textEl = addStreamMessage();

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Parse SSE lines from buffer
        const lines = buffer.split("\n");
        buffer = lines.pop(); // keep incomplete line in buffer

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = line.slice(6).trim();

          if (data === "[DONE]") continue;

          try {
            const parsed = JSON.parse(data);
            if (parsed.error) {
              textEl.textContent += "\n[Error: " + parsed.error + "]";
            } else if (parsed.token) {
              textEl.textContent += parsed.token;
              scrollToBottom();
            }
          } catch (e) {
            // skip unparseable chunks
          }
        }
      }
    } catch (e) {
      hideTyping();
      if (orb) orb.classList.remove("orb--thinking");
      addMessage("yantrik", "I'm having trouble responding right now. Give me a moment.");
      console.error("Chat error:", e);
    }

    Yantrik.waiting = false;
  }

  // ── Input handling ──
  function setupInput(textarea, button) {
    // Auto-grow
    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";

      if (textarea.value.trim()) {
        button.classList.add("active");
      } else {
        button.classList.remove("active");
      }
    });

    // Enter to send (shift+enter for newline)
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const text = textarea.value;
        textarea.value = "";
        textarea.style.height = "auto";
        button.classList.remove("active");

        if (Yantrik.currentState === Yantrik.State.GENERIC) {
          Yantrik.switchTo(Yantrik.State.AI_CHATTING);
        }

        send(text);
      }
    });

    // Send button click
    button.addEventListener("click", () => {
      const text = textarea.value;
      textarea.value = "";
      textarea.style.height = "auto";
      button.classList.remove("active");

      if (Yantrik.currentState === Yantrik.State.GENERIC) {
        Yantrik.switchTo(Yantrik.State.AI_CHATTING);
      }

      send(text);
    });
  }

  // ── Load history on boot ──
  async function loadHistory() {
    try {
      const data = await Yantrik.api.history(20);
      if (data.turns && data.turns.length > 0) {
        for (const turn of data.turns) {
          if (turn.role === "user") addMessage("user", turn.content);
          else if (turn.role === "assistant") addMessage("yantrik", turn.content);
        }
      }
    } catch (e) {
      // History not available yet
    }
  }

  // ── Focus chat input ──
  function focus() {
    if (inputEl) {
      setTimeout(() => inputEl.focus(), 300);
    }
  }

  // ── Send with context (from glance card tap) ──
  function sendWithContext(text) {
    Yantrik.switchTo(Yantrik.State.AI_CHATTING);
    send(text);
  }

  // ── Init ──
  function init() {
    messagesEl = document.getElementById("messages");
    inputEl = document.getElementById("chat-input");
    sendBtn = document.getElementById("btn-send");
    homeInputEl = document.getElementById("home-input");
    homeSendBtn = document.getElementById("btn-home-send");
    typingEl = document.getElementById("typing-indicator");

    if (inputEl && sendBtn) setupInput(inputEl, sendBtn);
    if (homeInputEl && homeSendBtn) setupInput(homeInputEl, homeSendBtn);

    loadHistory();
  }

  return { init, addMessage, focus, sendWithContext };
})();

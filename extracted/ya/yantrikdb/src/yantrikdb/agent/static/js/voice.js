/* ═══════════════════════════════════════════════
   voice.js — Mic recording, STT, and TTS playback
   ═══════════════════════════════════════════════ */

const Voice = (() => {
  "use strict";

  let mediaRecorder = null;
  let audioChunks = [];
  let recording = false;
  let ttsAudio = null;

  // ── Start/stop recording ──
  async function toggleRecording(micBtn) {
    if (recording) {
      stopRecording(micBtn);
    } else {
      await startRecording(micBtn);
    }
  }

  async function startRecording(micBtn) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];

      mediaRecorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
          ? "audio/webm;codecs=opus"
          : "audio/webm",
      });

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        // Stop all tracks
        stream.getTracks().forEach((t) => t.stop());

        micBtn.classList.remove("recording");
        micBtn.classList.add("transcribing");

        const blob = new Blob(audioChunks, { type: "audio/webm" });
        await transcribeAndSend(blob, micBtn);
      };

      mediaRecorder.start();
      recording = true;
      micBtn.classList.add("recording");
    } catch (e) {
      console.error("Mic access denied:", e);
    }
  }

  function stopRecording(micBtn) {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
    }
    recording = false;
  }

  // ── Transcribe audio and send as chat ──
  async function transcribeAndSend(blob, micBtn) {
    try {
      const form = new FormData();
      form.append("audio", blob, "recording.webm");

      const resp = await fetch("/voice/stt", { method: "POST", body: form });
      if (!resp.ok) throw new Error(`STT failed: ${resp.status}`);

      const data = await resp.json();
      const text = data.text?.trim();

      micBtn.classList.remove("transcribing");

      if (text) {
        // Switch to chat mode if needed
        if (Yantrik.currentState !== Yantrik.State.AI_CHATTING) {
          Yantrik.switchTo(Yantrik.State.AI_CHATTING);
        }

        // Send transcribed text as a chat message, then speak the response
        await sendAndSpeak(text);
      }
    } catch (e) {
      micBtn.classList.remove("transcribing");
      console.error("Transcription error:", e);
    }
  }

  // ── Send text to chat/stream, collect response, speak it ──
  async function sendAndSpeak(text) {
    if (Yantrik.waiting) return;

    Chat.addMessage("user", text);
    Yantrik.waiting = true;

    const typingEl = document.getElementById("typing-indicator");
    if (typingEl) typingEl.classList.add("visible");
    const orb = document.getElementById("orb");
    if (orb) orb.classList.add("orb--thinking");

    try {
      const resp = await fetch("/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

      if (typingEl) typingEl.classList.remove("visible");
      if (orb) orb.classList.remove("orb--thinking");

      // Create streaming message element
      const messagesEl = document.getElementById("messages");
      const div = document.createElement("div");
      div.className = "msg msg--yantrik";
      const span = document.createElement("span");
      span.className = "msg__text";
      div.appendChild(span);
      messagesEl.appendChild(div);

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let fullText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = line.slice(6).trim();
          if (data === "[DONE]") continue;
          try {
            const parsed = JSON.parse(data);
            if (parsed.token) {
              span.textContent += parsed.token;
              fullText += parsed.token;
              messagesEl.scrollTop = messagesEl.scrollHeight;
            }
          } catch (e) {}
        }
      }

      // Speak the response
      if (fullText.trim()) {
        speakText(fullText.trim());
      }
    } catch (e) {
      if (typingEl) typingEl.classList.remove("visible");
      if (orb) orb.classList.remove("orb--thinking");
      Chat.addMessage("yantrik", "I'm having trouble right now.");
      console.error("Voice chat error:", e);
    }

    Yantrik.waiting = false;
  }

  // ── TTS playback ──
  async function speakText(text) {
    try {
      // Stop any current playback
      if (ttsAudio) {
        ttsAudio.pause();
        ttsAudio = null;
      }

      const resp = await fetch("/voice/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!resp.ok) return;

      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      ttsAudio = new Audio(url);
      ttsAudio.play();
      ttsAudio.onended = () => URL.revokeObjectURL(url);
    } catch (e) {
      console.error("TTS playback error:", e);
    }
  }

  // ── Init ──
  function init() {
    const micBtn = document.getElementById("btn-mic");
    const homeMicBtn = document.getElementById("btn-home-mic");

    if (micBtn) {
      micBtn.addEventListener("click", () => toggleRecording(micBtn));
    }
    if (homeMicBtn) {
      homeMicBtn.addEventListener("click", () => toggleRecording(homeMicBtn));
    }
  }

  document.addEventListener("DOMContentLoaded", init);

  return { speakText };
})();

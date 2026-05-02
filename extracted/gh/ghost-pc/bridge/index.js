/**
 * GhostPC WhatsApp Bridge
 *
 * Thin Node.js process that handles ONLY WhatsApp via Baileys.
 * Communicates with the Python agent via NDJSON (newline-delimited JSON) on stdin/stdout.
 *
 * Protocol:
 *   Python → Node (stdin):  JSON-RPC requests  (send_text, send_image, etc.)
 *   Node → Python (stdout): JSON-RPC events    (message, qr, connection.update)
 *   Node → stderr:          Debug logs          (pino logger)
 *
 * IMPORTANT: Nothing except JSON lines goes to stdout. All logging goes to stderr.
 */

import { createInterface } from "readline";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join, resolve } from "path";
import makeWASocket, {
  useMultiFileAuthState,
  makeCacheableSignalKeyStore,
  fetchLatestBaileysVersion,
  Browsers,
  DisconnectReason,
  getContentType,
  downloadMediaMessage,
} from "@whiskeysockets/baileys";
import pino from "pino";
import { Boom } from "@hapi/boom";

// --- Config ---
const CREDENTIALS_DIR = resolve(
  process.env.GHOST_CREDENTIALS_DIR || join(process.cwd(), "..", "credentials")
);
const AUTH_DIR = join(CREDENTIALS_DIR, "whatsapp");

// Ensure auth directory exists
if (!existsSync(AUTH_DIR)) {
  mkdirSync(AUTH_DIR, { recursive: true });
}

// --- Logger: MUST go to stderr, NOT stdout ---
const logger = pino(
  { level: process.env.LOG_LEVEL || "warn" },
  pino.destination(2) // fd 2 = stderr
);

// --- JSON-RPC helpers ---
function emit(obj) {
  process.stdout.write(JSON.stringify(obj) + "\n");
}

function emitEvent(type, data) {
  emit({ jsonrpc: "2.0", method: "event", params: { type, data } });
}

function emitResult(id, result) {
  emit({ jsonrpc: "2.0", id, result });
}

function emitError(id, message) {
  emit({ jsonrpc: "2.0", id, error: { code: -1, message } });
}

// --- In-memory message store (for getMessage requirement) ---
const messageStore = new Map();
const MAX_STORE_SIZE = 1000;

function storeMessage(key, message) {
  const storeKey = `${key.remoteJid}:${key.id}`;
  messageStore.set(storeKey, message);
  // Evict oldest if too large
  if (messageStore.size > MAX_STORE_SIZE) {
    const firstKey = messageStore.keys().next().value;
    messageStore.delete(firstKey);
  }
}

// --- WhatsApp connection ---
let sock = null;

async function connectWhatsApp() {
  emitEvent("bridge.status", { stage: "loading_auth" });

  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  emitEvent("bridge.status", { stage: "auth_loaded" });

  // Fetch the latest WhatsApp Web version so Baileys uses an up-to-date
  // protocol version.  Fall back gracefully if the CDN is unreachable.
  let waVersion;
  try {
    const { version } = await fetchLatestBaileysVersion();
    waVersion = version;
    emitEvent("bridge.status", { stage: "version_fetched", version });
  } catch (e) {
    logger.warn("Could not fetch latest WA version, using bundled default:", e.message);
    emitEvent("bridge.status", { stage: "version_fetch_failed", error: e.message });
  }

  emitEvent("bridge.status", { stage: "creating_socket" });

  sock = makeWASocket({
    auth: {
      creds: state.creds,
      keys: makeCacheableSignalKeyStore(state.keys, logger),
    },
    logger,
    printQRInTerminal: false,
    // Use a recognised browser preset — custom tuples like ["GhostPC","Desktop","1.0"]
    // can cause WhatsApp to reject the pairing silently.
    browser: Browsers.windows("Chrome"),
    ...(waVersion ? { version: waVersion } : {}),
    syncFullHistory: false,
    markOnlineOnConnect: true,
    getMessage: async (key) => {
      const storeKey = `${key.remoteJid}:${key.id}`;
      return messageStore.get(storeKey)?.message || undefined;
    },
  });

  emitEvent("bridge.status", { stage: "socket_created" });

  // --- Events ---

  // Credential updates (persist session)
  sock.ev.on("creds.update", saveCreds);

  // Connection state
  sock.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      emitEvent("qr", { qr });
    }

    if (connection === "open") {
      emitEvent("connection.update", { connection: "open" });
      logger.info("WhatsApp connected");
    }

    if (connection === "close") {
      const statusCode = /** @type {Boom} */ (lastDisconnect?.error)?.output
        ?.statusCode;
      const shouldReconnect = statusCode !== DisconnectReason.loggedOut;

      emitEvent("connection.update", {
        connection: "close",
        statusCode,
        shouldReconnect,
      });

      if (shouldReconnect) {
        logger.info("Reconnecting to WhatsApp...");
        setTimeout(connectWhatsApp, 3000);
      } else {
        logger.warn("Logged out of WhatsApp. Need to re-scan QR.");
        emitEvent("logged_out", {});
      }
    }
  });

  // Incoming messages
  sock.ev.on("messages.upsert", async ({ messages, type }) => {
    if (type !== "notify") return;

    for (const msg of messages) {
      const key = msg.key;
      if (!key?.remoteJid) continue;

      // Skip own messages, status broadcasts, groups (for now)
      if (key.fromMe) continue;
      if (key.remoteJid.endsWith("@broadcast")) continue;
      if (key.remoteJid.endsWith("@g.us")) continue; // Skip groups for MVP

      // Store message
      storeMessage(key, msg);

      // Extract text
      const messageContent = msg.message;
      if (!messageContent) continue;

      const contentType = getContentType(messageContent);
      let body = "";
      let mediaPath = null;

      // Extract text from various message types
      if (contentType === "conversation") {
        body = messageContent.conversation || "";
      } else if (contentType === "extendedTextMessage") {
        body = messageContent.extendedTextMessage?.text || "";
      } else if (contentType === "imageMessage") {
        body = messageContent.imageMessage?.caption || "[image]";
        // Download media
        try {
          const buffer = await downloadMediaMessage(msg, "buffer", {}, {
            logger,
            reuploadRequest: sock.updateMediaMessage,
          });
          const tmpPath = join(
            process.env.TEMP || "/tmp",
            `ghost_media_${Date.now()}.jpg`
          );
          writeFileSync(tmpPath, buffer);
          mediaPath = tmpPath;
        } catch (e) {
          logger.error("Media download failed:", e.message);
        }
      } else if (contentType === "videoMessage") {
        body = messageContent.videoMessage?.caption || "[video]";
      } else if (contentType === "audioMessage") {
        body = "[voice message]";
        // TODO: Download and transcribe
      } else if (contentType === "documentMessage") {
        body =
          messageContent.documentMessage?.caption ||
          `[document: ${messageContent.documentMessage?.fileName || "file"}]`;
      } else {
        // Unknown type — skip
        continue;
      }

      // Send read receipt
      try {
        await sock.readMessages([key]);
      } catch (e) {
        // Non-critical
      }

      // Resolve sender number
      const from = key.remoteJid.replace("@s.whatsapp.net", "");

      // Send typing indicator
      try {
        await sock.sendPresenceUpdate("composing", key.remoteJid);
      } catch (e) {
        // Non-critical
      }

      logger.info("Incoming message from +%s: %s", from, body.substring(0, 50));

      // Emit to Python
      emitEvent("message", {
        id: key.id,
        from: `+${from}`,
        body,
        mediaPath,
        pushName: msg.pushName || "",
        timestamp: msg.messageTimestamp
          ? Number(msg.messageTimestamp) * 1000
          : Date.now(),
      });
    }
  });
}

// --- Handle commands from Python (stdin) ---
const rl = createInterface({ input: process.stdin });

rl.on("line", async (line) => {
  let request;
  try {
    request = JSON.parse(line);
  } catch {
    return; // Ignore non-JSON
  }

  const { id, method, params } = request;
  if (!sock) {
    emitError(id, "WhatsApp not connected");
    return;
  }

  try {
    switch (method) {
      case "send_text": {
        const jid = toJid(params.to);
        const result = await sock.sendMessage(jid, { text: params.text });
        emitResult(id, { messageId: result?.key?.id });
        break;
      }

      case "send_image": {
        const jid = toJid(params.to);
        const buffer = readFileSync(params.path);
        const result = await sock.sendMessage(jid, {
          image: buffer,
          caption: params.caption || "",
          mimetype: "image/jpeg",
        });
        emitResult(id, { messageId: result?.key?.id });
        break;
      }

      case "send_video": {
        const jid = toJid(params.to);
        const buffer = readFileSync(params.path);
        const result = await sock.sendMessage(jid, {
          video: buffer,
          caption: params.caption || "",
          mimetype: "video/mp4",
        });
        emitResult(id, { messageId: result?.key?.id });
        break;
      }

      case "send_document": {
        const jid = toJid(params.to);
        const buffer = readFileSync(params.path);
        const result = await sock.sendMessage(jid, {
          document: buffer,
          fileName: params.filename || "file",
          mimetype: "application/octet-stream",
        });
        emitResult(id, { messageId: result?.key?.id });
        break;
      }

      case "send_composing": {
        const jid = toJid(params.to);
        await sock.sendPresenceUpdate("composing", jid);
        emitResult(id, { ok: true });
        break;
      }

      default:
        emitError(id, `Unknown method: ${method}`);
    }
  } catch (err) {
    emitError(id, err.message || String(err));
  }
});

// --- Helpers ---
function toJid(number) {
  // Convert +1234567890 to 1234567890@s.whatsapp.net
  const cleaned = number.replace(/[^0-9]/g, "");
  return `${cleaned}@s.whatsapp.net`;
}

// --- Start ---
logger.info("GhostPC WhatsApp bridge starting...");
emitEvent("bridge.status", { stage: "starting" });
connectWhatsApp().catch((err) => {
  emitEvent("bridge.error", { message: err.message || String(err) });
  logger.error("Fatal:", err);
  process.exit(1);
});

// Graceful shutdown
process.on("SIGTERM", () => {
  logger.info("Bridge shutting down...");
  if (sock) sock.end(undefined);
  process.exit(0);
});

process.on("SIGINT", () => {
  if (sock) sock.end(undefined);
  process.exit(0);
});

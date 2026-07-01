import { useEffect, useState } from "react";

export interface ActiveWorkspace {
  name?: string;
  path?: string;
  branch?: string;
  head?: string;
  // allow extra fields from the server without strict typing
  [k: string]: unknown;
}

const STORAGE_KEY = "cvc.chat.activeWorkspace";
const EVENT_NAME = "cvc:active-workspace-changed";

function readFromStorage(): ActiveWorkspace | null {
  try {
    if (typeof window === "undefined") return null;
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as ActiveWorkspace) : null;
  } catch {
    return null;
  }
}

/**
 * useActiveWorkspace — reads the workspace chosen in the chat page.
 *
 * The ChatPage is the canonical source of "what workspace is the user
 * in right now" — it persists the choice to localStorage. Overview,
 * Operations, and Timeline subscribe to this hook so they always show
 * data for the same workspace the user is chatting in.
 *
 * Two shapes for compatibility:
 *   - default: returns the workspace directly (preferred for new code)
 *   - legacy:  useActiveWorkspace().activeWorkspace (used by SoulPage
 *     before C2; the property accessor also works on the default shape
 *     because we expose both)
 *
 * Cross-tab sync: listens to the "storage" event so switching the
 * workspace in another tab is reflected live.
 */
export function useActiveWorkspace(): ActiveWorkspace | null {
  return _useActiveWorkspace();
}

/** Legacy shape — kept so older pages don't break. */
export function useActiveWorkspaceObject(): { activeWorkspace: ActiveWorkspace | null } {
  return { activeWorkspace: _useActiveWorkspace() };
}

function _useActiveWorkspace(): ActiveWorkspace | null {
  const [ws, setWs] = useState<ActiveWorkspace | null>(readFromStorage);

  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY) {
        setWs(readFromStorage());
      }
    };
    const onLocal = () => setWs(readFromStorage());

    window.addEventListener("storage", onStorage);
    window.addEventListener(EVENT_NAME, onLocal as EventListener);
    return () => {
      window.removeEventListener("storage", onStorage);
      window.removeEventListener(EVENT_NAME, onLocal as EventListener);
    };
  }, []);

  return ws;
}

/** Broadcast that the active workspace changed (call from ChatPage). */
export function notifyActiveWorkspaceChanged(): void {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new Event(EVENT_NAME));
}
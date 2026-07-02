/**
 * usePortalSession — Time Portal session state.
 *
 * v3.5.0 — When the user "enters the portal" from /time-portal, a UUID
 * (portal_id) is generated client-side and stored in localStorage so the
 * chat section can show a banner on every page reload until the user exits.
 *
 * The portal_id is also sent with every chat turn so the gateway can
 * inject historical-soul context. Multiple browser tabs/windows can hold
 * different portal_ids — the server tracks them all by id.
 */

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { PortalSession, PortalActiveResponse } from "@/lib/types";

const STORAGE_KEY = "cvc.portal_session.v1";

/**
 * Load the portal_id from localStorage. Returns null if absent or the
 * stored value isn't a non-empty string.
 */
function readStoredPortalId(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const v = window.localStorage.getItem(STORAGE_KEY);
    if (typeof v === "string" && v.length > 0 && v.length <= 256) return v;
  } catch {
    /* localStorage unavailable (private mode etc.) — fall through */
  }
  return null;
}

function writeStoredPortalId(id: string | null): void {
  if (typeof window === "undefined") return;
  try {
    if (id) window.localStorage.setItem(STORAGE_KEY, id);
    else window.localStorage.removeItem(STORAGE_KEY);
    // v3.5.2 — Notify SAME-tab listeners. The browser's storage event
    // only fires in OTHER tabs, so a same-tab consumer (e.g. the chat
    // page already mounted while we enter/exit the portal) wouldn't
    // otherwise pick up the change. Custom event bridges the gap.
    window.dispatchEvent(
      new CustomEvent("cvc:portal-changed", { detail: { id: id ?? null } }),
    );
  } catch {
    /* ignore */
  }
}

function makePortalId(): string {
  // UUID v4 — works in any modern browser, no crypto.randomUUID dependency.
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export interface PortalState {
  /** Active portal_id, or null when not in the portal. */
  portalId: string | null;
  /** Server-side session metadata (snapshot, iso_date, label). */
  session: PortalSession | null;
  /** True until we've finished the first /active lookup. */
  loading: boolean;
  /** Last error from the API (e.g. snapshot not found). */
  error: string | null;
}

export interface PortalActions {
  enter: (target: string, label?: string) => Promise<boolean>;
  exit: () => Promise<void>;
  refresh: () => Promise<void>;
}

export function usePortalSession(workspacePath?: string): [PortalState, PortalActions] {
  // v3.5.2 — SYNCHRONOUS localStorage read. Previously portalId started
  // as null and only flipped to the stored value AFTER the /active
  // round-trip resolved, which produced a visible flash on /chat
  // navigation (banner only appeared once the server responded). Now we
  // hydrate from localStorage in the useState initializer so the banner
  // is visible on the first render. The /active verification still runs
  // on mount to populate full session metadata + clear stale ids.
  const [portalId, setPortalId] = useState<string | null>(() => readStoredPortalId());
  const [session, setSession] = useState<PortalSession | null>(null);
  const [loading, setLoading] = useState<boolean>(() => readStoredPortalId() !== null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const stored = readStoredPortalId();
    if (!stored) {
      setPortalId(null);
      setSession(null);
      setLoading(false);
      return;
    }
    // CRITICAL: synchronously adopt the stored id so the banner is
    // already visible by the time the round-trip starts. This is a
    // belt-and-braces backup to the useState initializer above — if the
    // hook is called from a server-side context where useState's lazy
    // initializer saw a different window state, this still keeps things
    // in sync.
    setPortalId((prev) => (prev === stored ? prev : stored));
    try {
      const r: PortalActiveResponse = await api.portalActive(stored, workspacePath);
      if (r.active && r.session) {
        setPortalId(stored);
        setSession(r.session);
        setError(null);
      } else {
        // Stored portal is gone (server restart, session expired). Clear it.
        writeStoredPortalId(null);
        setPortalId(null);
        setSession(null);
        setError(null);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }, [workspacePath]);

  // On mount: read stored id and verify against server.
  useEffect(() => {
    refresh();
  }, [refresh]);

  // v3.5.2 — Cross-tab + same-tab sync. Listen for both the browser's
  // native `storage` event (fires in OTHER tabs) and our custom
  // `cvc:portal-changed` event (fires in the SAME tab — localStorage
  // writes don't trigger `storage` in the writing tab). This way
  // whether the user enters/exits the portal from this tab or another,
  // the chat page picks up the change immediately rather than waiting
  // for the next /active round-trip.
  useEffect(() => {
    function onStorage(e: StorageEvent) {
      if (e.key !== STORAGE_KEY) return;
      const next = e.newValue;
      if (next && next.length > 0 && next.length <= 256) {
        setPortalId(next);
        setSession(null);  // metadata will re-hydrate via refresh
        setLoading(true);
        void refresh();
      } else {
        setPortalId(null);
        setSession(null);
        setError(null);
      }
    }
    function onPortalChanged(e: Event) {
      const detail = (e as CustomEvent<{ id: string | null }>).detail;
      if (detail?.id && detail.id.length > 0 && detail.id.length <= 256) {
        setPortalId(detail.id);
        setSession(null);
        setLoading(true);
        void refresh();
      } else {
        setPortalId(null);
        setSession(null);
        setError(null);
      }
    }
    window.addEventListener("storage", onStorage);
    window.addEventListener("cvc:portal-changed", onPortalChanged as EventListener);
    return () => {
      window.removeEventListener("storage", onStorage);
      window.removeEventListener("cvc:portal-changed", onPortalChanged as EventListener);
    };
  }, [refresh]);

  const enter = useCallback(
    async (target: string, label?: string): Promise<boolean> => {
      const newId = makePortalId();
      try {
        const r = await api.portalEnter(newId, target, workspacePath, label);
        if (!r.ok) {
          setError(r.error || "failed to enter portal");
          return false;
        }
        // v3.5.2 — use the shared writer so the cvc:portal-changed
        // event fires and any other tab (or this tab's already-mounted
        // chat page) picks up the new session immediately.
        writeStoredPortalId(newId);
        setPortalId(newId);
        // The enter response carries enough fields to render the banner
        // without an extra round-trip.
        setSession({
          snapshot_id: r.snapshot_id || "",
          snapshot_timestamp: r.timestamp || 0,
          iso_date: r.iso_date || "",
          target_resolved: r.target_resolved || target,
          label: r.label || label || `portal: ${target}`,
          trigger: r.trigger || "?",
          created_at: Date.now() / 1000,
        });
        setError(null);
        return true;
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
        return false;
      }
    },
    [workspacePath],
  );

  const exit = useCallback(async () => {
    const id = portalId ?? readStoredPortalId();
    if (!id) return;
    try {
      await api.portalExit(id, workspacePath);
    } catch {
      /* best-effort — clear locally even if server call fails */
    }
    writeStoredPortalId(null);
    setPortalId(null);
    setSession(null);
    setError(null);
  }, [portalId, workspacePath]);

  return [
    { portalId, session, loading, error },
    { enter, exit, refresh },
  ];
}
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
  const [portalId, setPortalId] = useState<string | null>(null);
  const [session, setSession] = useState<PortalSession | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const stored = readStoredPortalId();
    if (!stored) {
      setPortalId(null);
      setSession(null);
      setLoading(false);
      return;
    }
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

  const enter = useCallback(
    async (target: string, label?: string): Promise<boolean> => {
      const newId = makePortalId();
      try {
        const r = await api.portalEnter(newId, target, workspacePath, label);
        if (!r.ok) {
          setError(r.error || "failed to enter portal");
          return false;
        }
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
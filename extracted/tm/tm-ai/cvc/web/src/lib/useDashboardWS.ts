/**
 * useDashboardWS — subscribe to /ws/dashboard for live commit/agent events.
 *
 * Reconnects with exponential backoff. Hands events to the consumer via the
 * `onEvent` callback. Returns connection status for badge display.
 */
import { useEffect, useRef, useState } from "react";
import { dashboardWsUrl } from "@/lib/api";

export interface DashboardEvent {
  type: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  payload?: any;
  timestamp?: number;
}

export type WSStatus = "connecting" | "open" | "closed" | "error";

export function useDashboardWS(onEvent?: (evt: DashboardEvent) => void) {
  const [status, setStatus] = useState<WSStatus>("connecting");
  const [lastEvent, setLastEvent] = useState<DashboardEvent | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);
  const onEventRef = useRef(onEvent);
  onEventRef.current = onEvent;

  useEffect(() => {
    let cancelled = false;
    let retryTimer: number | undefined;

    const connect = () => {
      if (cancelled) return;
      let url: string;
      try {
        url = dashboardWsUrl();
      } catch {
        setStatus("error");
        return;
      }
      setStatus("connecting");
      let ws: WebSocket;
      try {
        ws = new WebSocket(url);
      } catch {
        setStatus("error");
        scheduleRetry();
        return;
      }
      wsRef.current = ws;

      ws.onopen = () => {
        if (cancelled) return;
        retryRef.current = 0;
        setStatus("open");
      };
      ws.onmessage = (msg) => {
        if (cancelled) return;
        try {
          const evt: DashboardEvent = JSON.parse(msg.data);
          setLastEvent(evt);
          onEventRef.current?.(evt);
        } catch {
          /* ignore non-json */
        }
      };
      ws.onerror = () => {
        if (cancelled) return;
        setStatus("error");
      };
      ws.onclose = () => {
        if (cancelled) return;
        setStatus("closed");
        scheduleRetry();
      };
    };

    const scheduleRetry = () => {
      if (cancelled) return;
      const delay = Math.min(30000, 1000 * 2 ** retryRef.current);
      retryRef.current += 1;
      retryTimer = window.setTimeout(connect, delay);
    };

    connect();

    return () => {
      cancelled = true;
      if (retryTimer) window.clearTimeout(retryTimer);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, []);

  return { status, lastEvent };
}

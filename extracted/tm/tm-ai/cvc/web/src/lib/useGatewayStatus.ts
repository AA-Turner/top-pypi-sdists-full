import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export interface GatewayStatusSnapshot {
  proxy: "ok" | "down" | "unknown";
  agent: "ok" | "down" | "unknown";
  mcp: "ok" | "down" | "unknown";
  sdk: "ok" | "down" | "unknown";
  workspace?: string;
  branch?: string;
  totalCommits?: number;
  agentCount?: number;
  mcpToolCount?: number;
  /** Live version reported by the gateway's /health endpoint. */
  version?: string;
  lastUpdated: number;
}

const INITIAL: GatewayStatusSnapshot = {
  proxy: "unknown",
  agent: "unknown",
  mcp: "unknown",
  sdk: "unknown",
  lastUpdated: 0,
};

export function useGatewayStatus(intervalMs = 6000): GatewayStatusSnapshot {
  const [snap, setSnap] = useState<GatewayStatusSnapshot>(INITIAL);

  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | null = null;

    async function tick() {
      const next: GatewayStatusSnapshot = { ...INITIAL, lastUpdated: Date.now() };
      // health → proxy (+ live version)
      try {
        const h = await api.health();
        next.proxy = "ok";
        if (h?.version) next.version = h.version;
      } catch {
        next.proxy = "down";
      }
      // stats → branch / commits / agent
      try {
        const s = await api.stats();
        next.totalCommits = s.total_commits;
        next.agentCount = s.total_agents;
        next.agent = "ok";
      } catch {
        next.agent = "down";
      }
      // mcp
      try {
        const m = await api.mcpStatus();
        next.mcpToolCount = m.tools_count;
        next.mcp = m.available === false || m.status === "error" ? "down" : "ok";
      } catch {
        next.mcp = "down";
      }
      // sdk = hive mind agents endpoint
      try {
        const ag = await api.hivemindAgents();
        const list = Array.isArray(ag) ? ag : (ag.agents ?? []);
        next.agentCount = list.length;
        next.sdk = "ok";
      } catch {
        next.sdk = "down";
      }
      // ops status
      try {
        const o = await api.opsStatus();
        next.branch = o.branch;
        next.totalCommits = o.total_commits ?? next.totalCommits;
        next.workspace = o.workspace;
      } catch {
        /* keep what we have */
      }
      if (!cancelled) setSnap(next);
      timer = setTimeout(tick, intervalMs);
    }

    tick();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [intervalMs]);

  return snap;
}

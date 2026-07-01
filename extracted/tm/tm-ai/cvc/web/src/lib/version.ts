/**
 * Canonical CVC version for the web dashboard.
 *
 * Build-time value injected by `vite.config.ts` (define `__CVC_VERSION__`)
 * sourced from `pyproject.toml`. The runtime live value (whatever the gateway
 * reports via `/health`) overrides this in the sidebar when available — see
 * `useGatewayStatus`. Keeping the build-time fallback means the version still
 * renders correctly when the gateway is offline or hasn't responded yet.
 */
declare const __CVC_VERSION__: string;

export const CVC_VERSION: string =
  typeof __CVC_VERSION__ !== "undefined" ? __CVC_VERSION__ : "0.0.0-dev";

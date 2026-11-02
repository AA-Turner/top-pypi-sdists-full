/**
 * What the cube page's Apps table says about an app, and in what order
 * (docs/console-spec.md §4.26).
 *
 * Apollo's status values are enums. The table shows them in plain English and keeps the
 * raw value for a tooltip; a value with no entry here is shown RAW, never guessed at, so
 * a member Apollo adds later reads as itself rather than as something it is not. The
 * health, rollout and config members are the introspected ones `AppHealth.tsx` and
 * `apollo_models.STATUS_ICONS` already place. `lifecycle` has no table: its enum is
 * unverified (AGENTS.md, Teleport chip item 5), so it is always shown raw.
 */
import type { App, AppChange } from './api'
import { healthTone } from './AppHealth'

const HEALTH: Record<string, string> = {
  HEALTHY: 'Healthy',
  DEFERRING: 'Deferring',
  WARNING: 'Warning',
  REPAIRING: 'Repairing',
  ERROR: 'Error',
  TERMINAL: 'Terminal',
  SUSPENDED: 'Suspended',
  ACTIVE_PLAN: 'Deploying',
  OUT_OF_DATE: 'Out of date',
  NO_DATA: 'No data',
  UNKNOWN_HEALTH: 'Unknown',
  INDETERMINATE: 'Indeterminate',
}

const ROLLOUT: Record<string, string> = {
  UP_TO_DATE: 'Up to date',
  IN_GRACE_PERIOD: 'In grace period',
  ONGOING_BLUE_GREEN: 'Blue-green in progress',
  STALE_BLOCKED: 'Stale (blocked)',
  STALE_BLOCKED_TRANSIENT: 'Stale (briefly blocked)',
  STALE_BLUE_GREEN: 'Stale (blue-green)',
  STALE_OTHER: 'Stale',
  RECALLED: 'Recalled',
  NOT_AVAILABLE: 'Not available',
}

const CONFIG: Record<string, string> = {
  UP_TO_DATE: 'Up to date',
  PENDING: 'Pending',
  BLOCKED: 'Blocked',
  NOT_AVAILABLE: 'Not available',
}

/** `plan_state` is the server's own reading of the plan, in Apollo's casing. `Active` is
 *  seen live (`entity_health` prints it for an entity mid-plan). */
const PLAN: Record<string, string> = {
  NoWork: 'No work',
  Active: 'In progress',
  Blocked: 'Blocked',
}

function label(table: Record<string, string>, raw: string, empty = '—'): string {
  if (!raw) return empty
  return table[raw.toUpperCase()] ?? table[raw] ?? raw
}

export const healthLabel = (raw: string) => label(HEALTH, raw, 'unknown')
export const rolloutLabel = (raw: string) => label(ROLLOUT, raw)
export const configLabel = (raw: string) => label(CONFIG, raw)
export const planLabel = (raw: string) => (raw ? PLAN[raw] ?? raw : '—')

/** Why an app needs attention, most severe first, or null when it does not.
 *
 *  A fault TONE (warn or bad, the same line `AppHealth.isFault` draws), a block, or a
 *  last deploy that failed with no success on record. A neutral status — No data,
 *  Suspended, Apollo's undocumented roll-ups — is not a fault and is not counted. */
export type Attention = 'bad' | 'warn' | 'blocked' | 'failed'

export function attentionOf(app: App, change: AppChange | undefined): Attention | null {
  const tone = healthTone(app.health)
  if (tone === 'bad') return 'bad'
  if (tone === 'warn') return 'warn'
  if (app.plan_state === 'Blocked' || app.blockers.length > 0) return 'blocked'
  if (change?.state === 'unsuccessful') return 'failed'
  return null
}

const RANK: Record<Attention, number> = { bad: 0, warn: 1, blocked: 2, failed: 3 }

/** Apps needing attention first (most severe first), then the rest; by name within
 *  each. Returns a new array. */
export function sortByAttention(
  apps: App[],
  changes: Record<string, AppChange> | undefined,
): App[] {
  const rank = (a: App) => {
    const why = attentionOf(a, changes?.[a.entity_name])
    return why === null ? 4 : RANK[why]
  }
  return [...apps].sort((a, b) => rank(a) - rank(b) || a.name.localeCompare(b.name))
}

export type SummaryItem = { label: string; tone: string; count: number }

const TONE_ORDER: Record<string, number> = { bad: 0, warn: 1, ok: 2, unknown: 3 }

/** Apps counted by their health label, faults first. Counted by label rather than by
 *  tone so "No data" and "Suspended" are not merged under one invented word. */
export function healthSummary(apps: App[]): SummaryItem[] {
  const byLabel = new Map<string, SummaryItem>()
  for (const a of apps) {
    const l = healthLabel(a.health)
    const item = byLabel.get(l) ?? { label: l, tone: healthTone(a.health), count: 0 }
    item.count += 1
    byLabel.set(l, item)
  }
  return [...byLabel.values()].sort(
    (a, b) => TONE_ORDER[a.tone]! - TONE_ORDER[b.tone]! || a.label.localeCompare(b.label),
  )
}

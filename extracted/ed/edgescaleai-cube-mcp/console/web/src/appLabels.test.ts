/** appLabels: what the Apps table says about an app, and in what order. */
import { describe, it, expect } from 'vitest'

import type { App, AppChange } from './api'
import {
  attentionOf,
  healthLabel,
  healthSummary,
  planLabel,
  rolloutLabel,
  configLabel,
  sortByAttention,
} from './appLabels'

function app(name: string, over: Partial<App> = {}): App {
  return {
    id: `aeid:${name}`, name, entity_name: name, product_id: `p:${name}`, kind: 'app',
    lifecycle: 'INSTALLED', version: '1.0.0', health: 'HEALTHY', rollout: 'UP_TO_DATE',
    config_status: 'UP_TO_DATE', blockers: [], plan_state: 'NoWork', exposed: [], ...over,
  }
}

const failed: AppChange = {
  last_changed: '2026-10-13T10:00:00Z', age_seconds: 7200, state: 'unsuccessful',
}

describe('labels', () => {
  it.each([
    ['HEALTHY', 'Healthy'], ['DEFERRING', 'Deferring'], ['WARNING', 'Warning'],
    ['REPAIRING', 'Repairing'], ['ERROR', 'Error'], ['TERMINAL', 'Terminal'],
    ['SUSPENDED', 'Suspended'], ['ACTIVE_PLAN', 'Deploying'], ['OUT_OF_DATE', 'Out of date'],
    ['NO_DATA', 'No data'], ['UNKNOWN_HEALTH', 'Unknown'], ['INDETERMINATE', 'Indeterminate'],
  ])('names every ApolloEntityHealthStatus member: %s', (raw, label) => {
    expect(healthLabel(raw)).toBe(label)
  })

  it('shows an unrecognized health value RAW rather than guessing a name for it', () => {
    expect(healthLabel('SOME_NEW_APOLLO_VALUE')).toBe('SOME_NEW_APOLLO_VALUE')
  })

  it('says "unknown" for an empty health rather than rendering nothing', () => {
    expect(healthLabel('')).toBe('unknown')
  })

  it.each([
    ['UP_TO_DATE', 'Up to date'], ['IN_GRACE_PERIOD', 'In grace period'],
    ['ONGOING_BLUE_GREEN', 'Blue-green in progress'], ['STALE_BLOCKED', 'Stale (blocked)'],
    ['STALE_BLOCKED_TRANSIENT', 'Stale (briefly blocked)'],
    ['STALE_BLUE_GREEN', 'Stale (blue-green)'], ['STALE_OTHER', 'Stale'],
    ['RECALLED', 'Recalled'], ['NOT_AVAILABLE', 'Not available'],
  ])('names every ApolloEntityRolloutStatus member: %s', (raw, label) => {
    expect(rolloutLabel(raw)).toBe(label)
  })

  it.each([
    ['UP_TO_DATE', 'Up to date'], ['PENDING', 'Pending'], ['BLOCKED', 'Blocked'],
    ['NOT_AVAILABLE', 'Not available'],
  ])('names every ApolloEntityConfigStatus member: %s', (raw, label) => {
    expect(configLabel(raw)).toBe(label)
  })

  it('names the plan states it knows and shows any other raw', () => {
    expect(planLabel('NoWork')).toBe('No work')
    expect(planLabel('Blocked')).toBe('Blocked')
    expect(planLabel('Active')).toBe('In progress')
    expect(planLabel('SomethingElse')).toBe('SomethingElse')
    expect(rolloutLabel('')).toBe('—')
  })
})

describe('needs attention', () => {
  it('is a fault tone, a block, or a failed last deploy — in that order of severity', () => {
    expect(attentionOf(app('a', { health: 'TERMINAL' }), undefined)).toBe('bad')
    expect(attentionOf(app('a', { health: 'ERROR' }), undefined)).toBe('bad')
    expect(attentionOf(app('a', { health: 'WARNING' }), undefined)).toBe('warn')
    expect(attentionOf(app('a', { health: 'REPAIRING' }), undefined)).toBe('warn')
    expect(attentionOf(app('a', { plan_state: 'Blocked' }), undefined)).toBe('blocked')
    expect(attentionOf(app('a', { blockers: ['CONFIG_PROBLEM'] }), undefined)).toBe('blocked')
    expect(attentionOf(app('a'), failed)).toBe('failed')
  })

  it('does NOT count a neutral status: No data is not a fault', () => {
    expect(attentionOf(app('a', { health: 'NO_DATA' }), undefined)).toBeNull()
    expect(attentionOf(app('a', { health: 'SUSPENDED' }), undefined)).toBeNull()
    expect(attentionOf(app('a'), undefined)).toBeNull()
    expect(attentionOf(app('a'), { ...failed, state: 'changed' })).toBeNull()
  })
})

describe('order', () => {
  it('puts apps that need attention first, most severe first, then the rest by name', () => {
    const changes = { keyence: failed }
    const sorted = sortByAttention([
      app('zeta'), app('keyence'), app('alpha'),
      app('minio', { health: 'WARNING' }), app('rabbit', { health: 'ERROR' }),
      app('gate', { plan_state: 'Blocked' }),
    ], changes)
    expect(sorted.map(a => a.name)).toEqual(['rabbit', 'minio', 'gate', 'keyence', 'alpha', 'zeta'])
  })

  it('does not reorder the list it was given', () => {
    const list = [app('b'), app('a')]
    sortByAttention(list, undefined)
    expect(list.map(a => a.name)).toEqual(['b', 'a'])
  })
})

describe('summary', () => {
  it('counts apps by health label, faults first, and keeps each tone', () => {
    expect(healthSummary([
      app('a'), app('b'), app('c', { health: 'ERROR' }), app('d', { health: 'NO_DATA' }),
      app('e', { health: 'WARNING' }),
    ])).toEqual([
      { label: 'Error', tone: 'bad', count: 1 },
      { label: 'Warning', tone: 'warn', count: 1 },
      { label: 'Healthy', tone: 'ok', count: 2 },
      { label: 'No data', tone: 'unknown', count: 1 },
    ])
  })
})

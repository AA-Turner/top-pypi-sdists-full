/** Tests for the service-line join (docs/console-spec.md §4.4f). */
import { describe, it, expect } from 'vitest'

import type { App, Exposed, ServiceCandidate, ServiceCandidates } from './api'
import { buildServiceLines, servicesAnswered } from './serviceLines'

function app(name: string, exposed: Exposed[] = []): App {
  return {
    id: `aeid:${name}`, name, entity_name: name, product_id: `p:${name}`, kind: 'app',
    lifecycle: 'INSTALLED', version: '1', health: 'HEALTHY', rollout: '', config_status: '',
    blockers: [], plan_state: 'NoWork', exposed,
  }
}

function ex(name: string, ns: string | null, service = '', port = 80): Exposed {
  return {
    name, url: `https://${name}.apex`, uri: `http://${service}.${ns}:${port}`,
    companies: ['lear'], reachable: true,
    target: ns === null ? null : { namespace: ns, service, port },
  }
}

function svc(service: string, namespace: string, ports: number[]): ServiceCandidate {
  return {
    service, namespace, type: 'ClusterIP',
    ports: ports.map(p => ({
      port: p, protocol: 'TCP',
      app_uri: `http://${service}.${namespace}.svc.cluster.local:${p}`,
      app_uri_tcp: `tcp://${service}.${namespace}.svc.cluster.local:${p}`,
    })),
  }
}

function answer(over: Partial<ServiceCandidates> = {}): ServiceCandidates {
  return { cube: 'c', by_entity: {}, unattributed: [], error: '', infra_hidden: 0, ...over }
}

describe('buildServiceLines', () => {
  it('draws one line per port and puts each exposed app on the port it targets', () => {
    const console5001 = ex('minio-console-c', 'default', 'minio', 5001)
    const out = buildServiceLines(
      [app('minio', [console5001])], [],
      answer({ by_entity: { minio: [svc('minio', 'default', [5000, 5001])] } }),
    )
    const lines = out.byEntity.get('minio')!
    expect(lines.map(l => [l.port, l.exposed.map(e => e.name)])).toEqual([
      [5000, []],
      [5001, ['minio-console-c']],
    ])
    expect(lines.every(l => l.candidate)).toBe(true)
  })

  it('keeps every exposed line when services have not answered, and adds no others', () => {
    // In flight, a failed request, and a kubectl failure all mean "could not look".
    const a = app('sqlpad', [ex('sqlpad-c', 'mov-core', 'sqlpad')])
    for (const services of [undefined, null, answer({ error: 'x', unattributed: [svc('z', 'n', [1])] })]) {
      const out = buildServiceLines([a], [], services)
      expect(out.byEntity.get('sqlpad')!.map(l => l.key)).toEqual(['mov-core/sqlpad:80'])
      expect(out.byEntity.get('sqlpad')![0]!.candidate).toBeUndefined()
      expect(out.other).toEqual([])
    }
  })

  it('shares one line between two apps exposed on the same port', () => {
    const out = buildServiceLines(
      [app('sqlpad', [ex('b-c', 'mov-core', 'sqlpad'), ex('a-c', 'mov-core', 'sqlpad')])], [],
      answer(),
    )
    const [line] = out.byEntity.get('sqlpad')!
    expect(line!.exposed.map(e => e.name)).toEqual(['a-c', 'b-c'])
  })

  it('never parses a URI: an app with no target goes to "untargeted", whatever its uri says', () => {
    const noTarget = { ...ex('odd-c', null), uri: 'http://sqlpad.mov-core:80' }
    const legacy: Exposed = { ...ex('old-c', 'x', 'y'), target: undefined }
    const out = buildServiceLines([app('sqlpad', [noTarget])], [legacy],
      answer({ by_entity: { sqlpad: [svc('sqlpad', 'mov-core', [80])] } }))
    expect(out.untargeted.map(e => e.name)).toEqual(['odd-c', 'old-c'])
    expect(out.byEntity.get('sqlpad')![0]!.exposed).toEqual([])
  })

  it('puts an unmatched exposed app on its Service line wherever that line is owned', () => {
    // The entity join missed the app, but the services read attributed its Service: the
    // enumerated attribution wins, so the app shows under the entity that owns the port.
    const out = buildServiceLines([app('sqlpad')], [ex('x-c', 'mov-core', 'sqlpad')],
      answer({ by_entity: { sqlpad: [svc('sqlpad', 'mov-core', [80])] } }))
    expect(out.byEntity.get('sqlpad')![0]!.exposed.map(e => e.name)).toEqual(['x-c'])
    expect(out.other).toEqual([])
  })

  it('sends unattributed services, unmatched apps, and owners not on the page to "other"', () => {
    const out = buildServiceLines([app('sqlpad')], [ex('orphan-c', 'ns', 'orphan')],
      answer({
        unattributed: [svc('mystery', 'elsewhere', [8080])],
        by_entity: { 'not-on-page': [svc('ghost', 'g', [1])] },
      }))
    expect(out.other.map(l => l.key)).toEqual(['g/ghost:1', 'elsewhere/mystery:8080', 'ns/orphan:80'])
    expect(out.byEntity.has('sqlpad')).toBe(false)
  })

  it('orders lines by service then port, independent of state', () => {
    const before = buildServiceLines([app('a')], [],
      answer({ by_entity: { a: [svc('zeta', 'n', [9, 1]), svc('alpha', 'n', [5])] } }))
    const after = buildServiceLines([app('a', [ex('z-c', 'n', 'zeta', 9)])], [],
      answer({ by_entity: { a: [svc('zeta', 'n', [9, 1]), svc('alpha', 'n', [5])] } }))
    const keys = ['n/alpha:5', 'n/zeta:1', 'n/zeta:9']
    expect(before.byEntity.get('a')!.map(l => l.key)).toEqual(keys)
    expect(after.byEntity.get('a')!.map(l => l.key)).toEqual(keys)
  })
})

describe('servicesAnswered', () => {
  it('is true only for a clean answer', () => {
    expect(servicesAnswered(undefined)).toBe(false)
    expect(servicesAnswered(null)).toBe(false)
    expect(servicesAnswered(answer({ error: 'Could not read.' }))).toBe(false)
    expect(servicesAnswered(answer())).toBe(true)
  })
})

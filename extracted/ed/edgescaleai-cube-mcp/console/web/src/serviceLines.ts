/**
 * The cube page's service lines: one per Service PORT, beneath the app that owns it
 * (docs/console-spec.md §4.4f).
 *
 * A line is drawn from the UNION of two reads that arrive on different schedules:
 *
 *   * the services payload (kubectl, slow, can fail) — every publishable port; and
 *   * the detail payload (Apollo, fast) — every exposed app, each with the `target`
 *     port the server parsed out of its URI.
 *
 * So an exposed app's line, and its link, never wait on kubectl or depend on it
 * succeeding; only the "Not exposed" lines do. That is also why an unexposed line can
 * only come from the services payload: without it the page cannot say a port is not
 * exposed, only that it could not look.
 *
 * The join is EQUALITY on `{namespace, service, port}`, keys the server built — no URI
 * is parsed here. Which app a line sits under is the server's `_match_by_resource`
 * answer, applied to the Service (`by_entity`) and to the exposed app
 * (`_attach_exposed`) by the same rules, so the two agree by construction; where a
 * Service was enumerated, its attribution wins.
 */

import type { App, Exposed, ServiceCandidate, ServiceCandidates, ServicePort } from './api'

export type ServiceLine = {
  /** `<namespace>/<service>:<port>` — also the key an expose result is reported on. */
  key: string
  namespace: string
  service: string
  port: number
  /** The enumerated port, when the services read listed it. Absent for a line drawn
   *  from an exposed app alone: the read is in flight, failed, or no longer lists the
   *  Service (a stale target). Exposing needs it — the write path only accepts a URI
   *  the server enumerated. */
  candidate?: { svc: ServiceCandidate; port: ServicePort }
  /** Every exposed app on this port, sorted by name. Usually zero or one; two names, or
   *  an HTTP and a TCP app, can share a port. */
  exposed: Exposed[]
}

export type ServiceLines = {
  /** Lines owned by an entity on the page, keyed by entity name. */
  byEntity: Map<string, ServiceLine[]>
  /** Lines no entity on the page owns: services the join could not attribute, and
   *  exposed apps on them. */
  other: ServiceLine[]
  /** Exposed apps whose URI names no Service port (a raw IP, a bare host, a port-less
   *  `tcp://`), or from a server that sends no `target`. Never dropped. */
  untargeted: Exposed[]
}

export function lineKey(namespace: string, service: string, port: number): string {
  return `${namespace}/${service}:${port}`
}

/** Did the services read answer? `undefined` is in flight, `null` a failed request, a
 *  populated `error` a kubectl/tbot failure. Only a clean answer can say "not exposed". */
export function servicesAnswered(
  services: ServiceCandidates | null | undefined,
): services is ServiceCandidates {
  return Boolean(services && !services.error)
}

export function buildServiceLines(
  entities: App[],
  unmatched: Exposed[],
  services: ServiceCandidates | null | undefined,
): ServiceLines {
  const lines = new Map<string, { line: ServiceLine; owner: string | null }>()
  const untargeted: Exposed[] = []

  const addCandidate = (owner: string | null, svc: ServiceCandidate) => {
    for (const port of svc.ports) {
      const key = lineKey(svc.namespace, svc.service, port.port)
      if (lines.has(key)) continue
      lines.set(key, {
        owner,
        line: {
          key, namespace: svc.namespace, service: svc.service, port: port.port,
          candidate: { svc, port }, exposed: [],
        },
      })
    }
  }
  if (servicesAnswered(services)) {
    for (const [owner, svcs] of Object.entries(services.by_entity)) {
      for (const svc of svcs) addCandidate(owner, svc)
    }
    for (const svc of services.unattributed) addCandidate(null, svc)
  }

  const addExposed = (owner: string | null, e: Exposed) => {
    const t = e.target
    if (!t) {
      untargeted.push(e)
      return
    }
    const key = lineKey(t.namespace, t.service, t.port)
    const hit = lines.get(key)
    if (hit) {
      hit.line.exposed.push(e)
      return
    }
    lines.set(key, {
      owner,
      line: { key, namespace: t.namespace, service: t.service, port: t.port, exposed: [e] },
    })
  }
  for (const app of entities) {
    for (const e of app.exposed) addExposed(app.entity_name, e)
  }
  for (const e of unmatched) addExposed(null, e)

  // An owner that is not on the page (the services read saw an entity the detail read
  // did not) must not make its lines vanish; they go to "other" instead.
  const onPage = new Set(entities.map(a => a.entity_name))
  const byEntity = new Map<string, ServiceLine[]>()
  const other: ServiceLine[] = []
  for (const { line, owner } of lines.values()) {
    line.exposed.sort((a, b) => a.name.localeCompare(b.name))
    if (owner && onPage.has(owner)) {
      const list = byEntity.get(owner) ?? []
      list.push(line)
      byEntity.set(owner, list)
    } else {
      other.push(line)
    }
  }
  for (const list of byEntity.values()) list.sort(byServiceThenPort)
  other.sort(byServiceThenPort)
  untargeted.sort((a, b) => a.name.localeCompare(b.name))
  return { byEntity, other, untargeted }
}

/** Stable order: a line never moves when its state changes, because a line that jumps
 *  after Expose is disorienting. */
function byServiceThenPort(a: ServiceLine, b: ServiceLine): number {
  return a.service.localeCompare(b.service) || a.namespace.localeCompare(b.namespace) ||
    a.port - b.port
}

/**
 * Tests for the API client.
 *
 * L11 from the Phase 3 review: this module was entirely untested because every other
 * test mocks `fetchCube`/`fetchCubes` wholesale — so dropping the `encodeURIComponent`
 * its own comment calls load-bearing failed nothing, and neither did losing the 401
 * or 404 mapping the UI branches on.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

import {
  exposeApp,
  fetchAppLogs,
  fetchCube,
  fetchServices,
  fetchCubes,
  fetchExposed,
  fetchSession,
  submitFeedback,
  unexposeApp,
  NotFound,
  SessionExpired,
  CONSOLE_BASE,
} from './api'

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status, headers: { 'content-type': 'application/json' },
  })
}

let fetchMock: ReturnType<typeof vi.fn>

beforeEach(() => {
  // A FRESH Response per call: a Response body can only be read once, so returning
  // one shared object makes the second request fail with "Body is unusable".
  fetchMock = vi.fn().mockImplementation(async () => jsonResponse({}))
  vi.stubGlobal('fetch', fetchMock)
})
afterEach(() => vi.unstubAllGlobals())

describe('request shape', () => {
  it('sends same-origin credentials and asks for JSON', async () => {
    // Accept: application/json matters — the middleware bounces an unauthenticated
    // HTML request to the login page but 401s everything else, so asking for JSON
    // keeps an expired session a clean 401 rather than a login page parsed as JSON.
    await fetchSession()
    const init = fetchMock.mock.calls[0]?.[1]
    expect(init?.credentials).toBe('same-origin')
    expect(init?.headers.Accept).toBe('application/json')
    expect(init?.method).toBe('GET')
  })

  it('never sends an Authorization header — the cookie is the credential', async () => {
    await fetchSession()
    const init = fetchMock.mock.calls[0]?.[1]
    expect(Object.keys(init?.headers ?? {})).not.toContain('Authorization')
  })

  it('prefixes every path with the console base', async () => {
    await fetchSession()
    await fetchCubes()
    expect(fetchMock.mock.calls.length).toBe(2)
    for (const call of fetchMock.mock.calls) {
      expect(String(call[0]).startsWith(`${CONSOLE_BASE}/api/`)).toBe(true)
    }
  })
})

describe('cube name encoding', () => {
  it('percent-encodes the cube name into the path', async () => {
    await fetchCube('weird name')
    expect(fetchMock.mock.calls[0]?.[0]).toBe(`${CONSOLE_BASE}/api/cubes/weird%20name`)
  })

  it('encodes characters that would otherwise change the path structure', async () => {
    // The server resolves the name by EXACT match against the caller's visible set,
    // so it must arrive byte-identical rather than reinterpreted as extra segments
    // or a query string.
    await fetchCube('a?b#c')
    expect(fetchMock.mock.calls[0]?.[0]).toBe(`${CONSOLE_BASE}/api/cubes/a%3Fb%23c`)
  })

  it('leaves an ordinary Apollo environment name untouched', async () => {
    await fetchCube('cube-66odzn95')
    expect(fetchMock.mock.calls[0]?.[0]).toBe(`${CONSOLE_BASE}/api/cubes/cube-66odzn95`)
  })
})

describe('status mapping', () => {
  it('maps 401 to SessionExpired', async () => {
    fetchMock.mockResolvedValue(jsonResponse({ error: 'nope' }, 401))
    await expect(fetchCubes()).rejects.toBeInstanceOf(SessionExpired)
  })

  it('maps 404 to NotFound', async () => {
    fetchMock.mockResolvedValue(jsonResponse({ error: 'No such cube.' }, 404))
    await expect(fetchCube('x')).rejects.toBeInstanceOf(NotFound)
  })

  it('carries environments_truncated off a 404 so the page can stop blaming RBAC', async () => {
    fetchMock.mockResolvedValue(
      jsonResponse({ error: 'No such cube.', environments_truncated: true }, 404),
    )
    await expect(fetchCube('x')).rejects.toMatchObject({ environmentsTruncated: true })
  })

  it('defaults environmentsTruncated to false on a plain 404', async () => {
    fetchMock.mockResolvedValue(jsonResponse({ error: 'No such cube.' }, 404))
    await expect(fetchCube('x')).rejects.toMatchObject({ environmentsTruncated: false })
  })

  it("surfaces the server's error message on other failures", async () => {
    fetchMock.mockResolvedValue(jsonResponse({ error: 'Could not read the cube list.' }, 502))
    await expect(fetchCubes()).rejects.toThrow('Could not read the cube list.')
  })

  it('falls back to the status when the body is not the expected shape', async () => {
    // A proxy error page, say — must not throw while trying to read `.error`.
    fetchMock.mockResolvedValue(new Response('<html>502</html>', { status: 502 }))
    await expect(fetchCubes()).rejects.toThrow(/502/)
  })
})

describe('the request builders themselves', () => {
  // Every CubePage/LogsPage test spies on these functions, so it asserts the wrapper
  // was called with arguments the test itself chose — the mock encodes the contract.
  // That is exactly the shape of the double-qualification bug, and it left the CSRF
  // header, the HTTP method, the credentials mode and the URL all unverified: each
  // could be broken with 122/122 still green.

  it('unexposeApp POSTs with the CSRF header, cookies, and a JSON body', async () => {
    // Without the header the server refuses every write; without same-origin
    // credentials the cookie never goes and it 401s.
    await unexposeApp('cube-66odzn95', 'mov-sqlpad-cube-66odzn95', 'tok-abc')

    const [url, init] = fetchMock.mock.calls[0]!
    expect(url).toBe(`${CONSOLE_BASE}/api/cubes/cube-66odzn95/unexpose`)
    expect(init.method).toBe('POST')
    expect(init.credentials).toBe('same-origin')
    expect(init.headers['X-Console-CSRF']).toBe('tok-abc')
    expect(init.headers['Content-Type']).toBe('application/json')
    expect(JSON.parse(init.body)).toEqual({ app: 'mov-sqlpad-cube-66odzn95' })
  })

  it('unexposeApp percent-encodes the cube name into the path', async () => {
    await unexposeApp('cube/../evil', 'a', 't')
    expect(fetchMock.mock.calls[0]![0]).toBe(
      `${CONSOLE_BASE}/api/cubes/cube%2F..%2Fevil/unexpose`,
    )
  })

  it('unexposeApp raises SessionExpired on a 401', async () => {
    fetchMock.mockImplementation(async () => jsonResponse({}, 401))
    await expect(unexposeApp('cube-x', 'a', 't')).rejects.toBeInstanceOf(SessionExpired)
  })

  it('unexposeApp surfaces the server error message', async () => {
    fetchMock.mockImplementation(async () => jsonResponse({ error: 'Invalid or missing CSRF token.' }, 403))
    await expect(unexposeApp('cube-x', 'a', 't')).rejects.toThrow('Invalid or missing CSRF token.')
  })

  it('fetchExposed hits the light poll endpoint', async () => {
    // A wrong path here 404s every poll, so a pending unexpose never resolves.
    await fetchExposed('cube-66odzn95')
    expect(fetchMock.mock.calls[0]![0]).toBe(
      `${CONSOLE_BASE}/api/cubes/cube-66odzn95/exposed`,
    )
    expect(fetchMock.mock.calls[0]![1].method).toBe('GET')
  })

  it('fetchAppLogs sends the app, and omits since on a full load', async () => {
    await fetchAppLogs('cube-66odzn95', 'esai-sovereign-ai-litellm')
    const url = fetchMock.mock.calls[0]![0] as string
    expect(url).toBe(
      `${CONSOLE_BASE}/api/cubes/cube-66odzn95/logs?app=esai-sovereign-ai-litellm`,
    )
    expect(url).not.toContain('since=')
  })

  it('fetchAppLogs sends since on an incremental poll', async () => {
    // Dropping this silently turns a 10s incremental tick into a full-window rescan
    // — invisible to every LogsPage test, which spies on this function.
    await fetchAppLogs('cube-x', 'a', '2026-07-31T18:00:00Z')
    const url = fetchMock.mock.calls[0]![0] as string
    expect(url).toContain('&since=2026-07-31T18%3A00%3A00Z')
  })

  it('fetchAppLogs percent-encodes both segments', async () => {
    await fetchAppLogs('cube/x', 'app&name')
    const url = fetchMock.mock.calls[0]![0] as string
    expect(url).toBe(`${CONSOLE_BASE}/api/cubes/cube%2Fx/logs?app=app%26name`)
  })
})

describe('the expose request builders', () => {
  it('exposeApp POSTs app + uri with the CSRF header and cookies', async () => {
    await exposeApp('cube-66odzn95', 'sqlpad', 'http://sqlpad.mov-core.svc.cluster.local:80', 'tok-abc')

    const [url, init] = fetchMock.mock.calls[0]!
    expect(url).toBe(`${CONSOLE_BASE}/api/cubes/cube-66odzn95/expose`)
    expect(init.method).toBe('POST')
    expect(init.credentials).toBe('same-origin')
    expect(init.headers['X-Console-CSRF']).toBe('tok-abc')
    expect(JSON.parse(init.body)).toEqual({
      app: 'sqlpad', uri: 'http://sqlpad.mov-core.svc.cluster.local:80',
    })
  })

  it('exposeApp raises SessionExpired on a 401', async () => {
    fetchMock.mockImplementation(async () => jsonResponse({}, 401))
    await expect(exposeApp('c', 'a', 'u', 't')).rejects.toBeInstanceOf(SessionExpired)
  })

  it('exposeApp surfaces the server error', async () => {
    fetchMock.mockImplementation(async () =>
      jsonResponse({ error: 'Invalid or missing CSRF token.' }, 403))
    await expect(exposeApp('c', 'a', 'u', 't')).rejects.toThrow('Invalid or missing CSRF token.')
  })

  it('submitFeedback POSTs the form fields with the CSRF header and cookies', async () => {
    await submitFeedback(
      { feedback_type: 'support', summary: 's', details: 'd', business_impact: 'i', cube: 'cube-x' },
      'tok-abc',
    )

    const [url, init] = fetchMock.mock.calls[0]!
    expect(url).toBe(`${CONSOLE_BASE}/api/feedback`)
    expect(init.method).toBe('POST')
    expect(init.credentials).toBe('same-origin')
    expect(init.headers['X-Console-CSRF']).toBe('tok-abc')
    expect(JSON.parse(init.body)).toEqual({
      feedback_type: 'support', summary: 's', details: 'd', business_impact: 'i', cube: 'cube-x',
    })
    // No email field exists on the payload shape at all — the reporter is
    // resolved server-side, never supplied by this client.
    expect(init.body).not.toContain('email')
  })

  it('submitFeedback raises SessionExpired on a 401', async () => {
    fetchMock.mockImplementation(async () => jsonResponse({}, 401))
    await expect(
      submitFeedback({ feedback_type: 'support', summary: 's', details: 'd', business_impact: 'i' }, 't'),
    ).rejects.toBeInstanceOf(SessionExpired)
  })

  it('submitFeedback surfaces the server error', async () => {
    fetchMock.mockImplementation(async () =>
      jsonResponse({ error: 'Jira rejected the submission (400): ...' }, 502))
    await expect(
      submitFeedback({ feedback_type: 'support', summary: 's', details: 'd', business_impact: 'i' }, 't'),
    ).rejects.toThrow('Jira rejected the submission')
  })

  it('fetchServices hits the lazy candidates endpoint', async () => {
    await fetchServices('cube-66odzn95')
    expect(fetchMock.mock.calls[0]![0]).toBe(
      `${CONSOLE_BASE}/api/cubes/cube-66odzn95/services`,
    )
    expect(fetchMock.mock.calls[0]![1].method).toBe('GET')
  })
})

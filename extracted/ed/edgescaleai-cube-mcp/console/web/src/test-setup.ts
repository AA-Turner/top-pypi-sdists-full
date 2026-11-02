/** Vitest setup: DOM cleanup between tests and a clipboard stub.
 *
 * `@testing-library/react` auto-cleans when a global `afterEach` exists, which it
 * does under vitest — this file exists for the clipboard, which jsdom does not
 * implement at all. Without a stub, `navigator.clipboard.writeText` throws a
 * TypeError and the copy button's failure path would be the only one testable.
 */
import { afterEach, beforeEach, vi } from 'vitest'
import { cleanup } from '@testing-library/react'

import * as api from './api'

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})

beforeEach(() => {
  // Writable so an individual test can replace it to exercise the failure path.
  Object.defineProperty(navigator, 'clipboard', {
    value: { writeText: vi.fn().mockResolvedValue(undefined) },
    configurable: true,
    writable: true,
  })

  // `CubePage` fetches Teleport connectivity on every mount, and jsdom has no base
  // URL, so an un-stubbed call rejects — which `CubePage` turns into `null`, which
  // renders a "Teleport Unknown" chip into the DOM of every test that mounts the
  // page. Five existing files (CubePage, Hardware, Inventory, LastChanged,
  // AgentStatus) were passing only because their assertions happen to use loose
  // matching; the collision is not hypothetical — it is what broke
  // CubeStatus.test.tsx when the chip was added, and the next `getByText('Unknown')`
  // anywhere would have hit it for an unrelated reason.
  //
  // Defaulted to a PENDING promise so the chip renders nothing at all. A test that
  // cares spies over this (TeleportStatus.test.tsx does), and the `afterEach`
  // `restoreAllMocks` puts it back. Stubbed here rather than in each mount helper
  // because there are ~80 mount sites and a per-site stub is a thing to forget.
  vi.spyOn(api, 'fetchCubeTeleport').mockReturnValue(new Promise(() => {}))

  // The GPS row, likewise fetched on every cube-page mount. Defaulted to a stack with
  // the feature OFF, so every other test sees the page exactly as before the row
  // existed. `GpsLocation.test.tsx` spies over it.
  vi.spyOn(api, 'fetchCubeGps').mockResolvedValue({
    cube: '', gps: null, gps_source: { enabled: false, available: true },
  })

  // The landing page's map, fetched only when a viewer chooses Map, which needs a
  // session with `gps_enabled` (no shared fixture sets it). Defaulted anyway so a test
  // that turns it on without caring about the map never reaches the network: the data
  // PENDING (the map shows its skeleton) and the outline absent. `FleetMap.test.tsx`
  // spies over both.
  vi.spyOn(api, 'fetchFleetGps').mockReturnValue(new Promise(() => {}))
  vi.spyOn(api, 'fetchMapOutline').mockResolvedValue(null)

  // jsdom lays nothing out and reports every scroll as a "not implemented" error. The
  // app scrolls to the top on each link navigation (App.tsx), so it is silenced here;
  // a test that cares asserts on this spy.
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {})
})

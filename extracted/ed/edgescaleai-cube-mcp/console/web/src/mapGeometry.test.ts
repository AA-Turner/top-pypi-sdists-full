/** The fleet map's geometry, as plain functions of fixed inputs.
 *
 *  Every expected number here is worked out by hand from known facts, never by calling
 *  another function of the module:
 *
 *  - Web Mercator in unit square coordinates: x = (lon + 180) / 360 and
 *    y = (1 - ln(tan(pi/4 + lat/2)) / pi) / 2, so (0, 0) is the centre, and at 45 degrees
 *    ln(tan(67.5 deg)) = asinh(1) = 0.88137, giving y = 0.35972.
 *  - A degree of longitude is 111.32 km at the equator and 111.32 * cos(lat) elsewhere.
 *  - The drawing surface is VIEW_W x VIEW_H with FIT_PADDING kept clear on every side.
 *  - At zoom z one world unit is 960 * 2^z surface units, and the surface centre is
 *    (480, 260), so a view's numbers can be checked with pencil arithmetic.
 */
import { describe, expect, it } from 'vitest'

import {
  FIT_PADDING,
  VIEW_H,
  VIEW_W,
  WORLD_VIEW,
  clampView,
  clientToSurface,
  fitView,
  groupDots,
  onSurface,
  outlinePaths,
  panBy,
  project,
  toScreen,
  wheelZoomSteps,
  zoomBy,
} from './mapGeometry'

type P = { name: string; lat: number; lng: number }
const at = (name: string, lat: number, lng: number): P => ({ name, lat, lng })

const DENVER = at('denver', 39.74, -104.99)
const AURORA = at('aurora', 39.73, -104.83)
const LAKEWOOD = at('lakewood', 39.70, -105.08)
const BOULDER = at('boulder', 40.01, -105.27)
const SEATTLE = at('seattle', 47.61, -122.33)
const MIAMI = at('miami', 25.76, -80.19)
const BOSTON = at('boston', 42.36, -71.06)
const SAN_DIEGO = at('san-diego', 32.72, -117.16)
const LONDON = at('london', 51.51, -0.13)

const US_SPREAD = [SEATTLE, MIAMI, BOSTON, SAN_DIEGO]
const DENVER_AREA = [DENVER, AURORA, LAKEWOOD, BOULDER]

/** Degrees of longitude spanned by the view's full width, read off two projected points
 *  rather than the view's own fields. */
function visibleLonSpan(view: ReturnType<typeof fitView>, lat: number): number {
  const a = toScreen(project(lat, 0), view).x
  const b = toScreen(project(lat, 10), view).x
  return (VIEW_W / (b - a)) * 10
}

describe('project (Web Mercator, unit square)', () => {
  it('puts the equator at the prime meridian in the middle', () => {
    const p = project(0, 0)
    expect(p.x).toBeCloseTo(0.5, 9)
    expect(p.y).toBeCloseTo(0.5, 9)
  })

  it('maps longitude linearly onto x', () => {
    expect(project(0, -180).x).toBeCloseTo(0, 9)
    expect(project(0, 180).x).toBeCloseTo(1, 9)
    expect(project(0, 90).x).toBeCloseTo(0.75, 9)
  })

  it('stretches latitude the Mercator way (45 degrees -> 0.35972)', () => {
    expect(project(45, 0).y).toBeCloseTo(0.35972, 4)
    expect(project(-45, 0).y).toBeCloseTo(1 - 0.35972, 4)
  })

  it('clips near the poles at 85 degrees, so nothing goes to infinity', () => {
    // ln(tan(87.5 deg)) = ln(22.904) = 3.1313; (1 - 3.1313 / pi) / 2 = 0.00163.
    expect(project(85, 0).y).toBeCloseTo(0.00163, 4)
    expect(project(90, 0).y).toBeCloseTo(project(85, 0).y, 9)
    expect(project(-90, 0).y).toBeCloseTo(1 - 0.00163, 4)
    expect(Number.isFinite(project(90, 0).y)).toBe(true)
  })
})

describe('fitView', () => {
  it('shows the world when there is nothing to frame', () => {
    expect(fitView([])).toEqual(WORLD_VIEW)
    // The world view fits the full width: lon -180 and 180 land on the two edges.
    expect(toScreen(project(0, -180), WORLD_VIEW).x).toBeCloseTo(0, 6)
    expect(toScreen(project(0, 180), WORLD_VIEW).x).toBeCloseTo(VIEW_W, 6)
  })

  it('frames one cube at the centre, about 1000 km wide, never tighter', () => {
    const view = fitView([DENVER])
    const p = toScreen(project(DENVER.lat, DENVER.lng), view)
    expect(p.x).toBeCloseTo(VIEW_W / 2, 6)
    expect(p.y).toBeCloseTo(VIEW_H / 2, 6)
    // 500 km either side at 39.74 degrees: 500 / (111.32 * cos 39.74) = 500 / 85.60
    // = 5.841 degrees, so those two meridians sit on the left and right edges (within 1%).
    const left = toScreen(project(DENVER.lat, DENVER.lng - 5.841), view).x
    const right = toScreen(project(DENVER.lat, DENVER.lng + 5.841), view).x
    expect(Math.abs(left - 0)).toBeLessThan(VIEW_W * 0.01)
    expect(Math.abs(right - VIEW_W)).toBeLessThan(VIEW_W * 0.01)
  })

  it('shows a lone cube\'s state borders: Colorado around Denver', () => {
    // Colorado runs from 109.05 W to 102.05 W (about 600 km at this latitude). Framed
    // 5.841 degrees either side of 104.99 W, the west border is 4.06 degrees left of
    // centre: 480 - 4.06 / 5.841 * 480 = 146; the east border 2.94 right: 722.
    const view = fitView([DENVER])
    const west = toScreen(project(DENVER.lat, -109.05), view).x
    const east = toScreen(project(DENVER.lat, -102.05), view).x
    expect(west).toBeCloseTo(146, -1)
    expect(east).toBeCloseTo(722, -1)
  })

  it('keeps the 1000 km floor for two cubes a kilometre apart', () => {
    const view = fitView([DENVER, at('next-door', 39.74, -104.98)])
    // 1000 km at 39.74 degrees is 1000 / 85.60 = 11.68 degrees of longitude.
    expect(visibleLonSpan(view, 39.74)).toBeGreaterThan(11.68 * 0.99)
    expect(visibleLonSpan(view, 39.74)).toBeLessThan(11.68 * 1.01)
  })

  it('frames a US spread to the US, every cube inside the padding', () => {
    const view = fitView(US_SPREAD)
    for (const c of US_SPREAD) {
      const p = toScreen(project(c.lat, c.lng), view)
      expect(p.x).toBeGreaterThanOrEqual(FIT_PADDING - 0.5)
      expect(p.x).toBeLessThanOrEqual(VIEW_W - FIT_PADDING + 0.5)
      expect(p.y).toBeGreaterThanOrEqual(FIT_PADDING - 0.5)
      expect(p.y).toBeLessThanOrEqual(VIEW_H - FIT_PADDING + 0.5)
    }
    // Height binds here. Mercator m = ln(tan(45 + lat/2)): Seattle 0.9475, Miami 0.4654,
    // so the cubes span 0.4821 / (2 pi) = 0.07673 of the world's height. That fills
    // VIEW_H - 2 * FIT_PADDING = 424 units: scale 5526, and the full 960-unit width
    // then spans 960 / 5526 * 360 = 62.5 degrees of longitude.
    expect(visibleLonSpan(view, 35)).toBeCloseTo(62.5, 0)
  })

  it('pulls the frame out for a cube abroad', () => {
    const us = fitView(US_SPREAD)
    const withLondon = fitView([...US_SPREAD, LONDON])
    // Seattle to London is 122.2 degrees of longitude, all of it on screen.
    expect(visibleLonSpan(withLondon, 40)).toBeGreaterThan(122.2)
    expect(visibleLonSpan(withLondon, 40)).toBeGreaterThan(visibleLonSpan(us, 40))
    const london = toScreen(project(LONDON.lat, LONDON.lng), withLondon)
    expect(london.x).toBeLessThanOrEqual(VIEW_W - FIT_PADDING + 0.5)
  })

  it('does not depend on the order of the cubes', () => {
    expect(fitView([...US_SPREAD].reverse())).toEqual(fitView(US_SPREAD))
  })
})

describe('groupDots', () => {
  const names = (groups: { members: P[] }[]) =>
    groups.map(g => g.members.map(m => m.name).sort()).sort((a, b) => a[0]!.localeCompare(b[0]!))

  it('groups the Denver-area cubes into one dot at the fitted US zoom', () => {
    const fleet = [...US_SPREAD, ...DENVER_AREA]
    const groups = groupDots(fleet, fitView(fleet), 8)
    // At ~5,500 units per world width, Denver to Boulder (0.28 degrees of longitude)
    // is about 4 units apart: well inside two 8-unit radii.
    expect(names(groups)).toEqual([
      ['aurora', 'boulder', 'denver', 'lakewood'],
      ['boston'], ['miami'], ['san-diego'], ['seattle'],
    ])
  })

  it('at a ~1000 km Colorado frame, keeps the near neighbours together but not Boulder', () => {
    // At 1000 km across 960 units, 1 km is ~0.96 units. Denver to Aurora (0.16 degrees
    // of longitude = 13.7 km) is ~13 units and Denver to Lakewood (~8.9 km) ~8.5, both
    // inside 2 x 8; Boulder is ~38 km from Denver, ~37 units, so it stands alone.
    const groups = groupDots(DENVER_AREA, fitView(DENVER_AREA), 8)
    expect(names(groups)).toEqual([['aurora', 'denver', 'lakewood'], ['boulder']])
  })

  it('places a group at the centre of its members', () => {
    const a = at('a', 0, 0)
    const b = at('b', 0, 0.01)
    const [group] = groupDots([a, b], WORLD_VIEW, 8)
    const pa = toScreen(project(0, 0), WORLD_VIEW)
    const pb = toScreen(project(0, 0.01), WORLD_VIEW)
    expect(group!.x).toBeCloseTo((pa.x + pb.x) / 2, 9)
    expect(group!.y).toBeCloseTo((pa.y + pb.y) / 2, 9)
  })

  it('gives the same groups, in the same order, whatever order the cubes came in', () => {
    const fleet = [...US_SPREAD, ...DENVER_AREA]
    const view = fitView(fleet)
    const a = groupDots(fleet, view, 8)
    const b = groupDots([...fleet].reverse(), view, 8)
    expect(b).toEqual(a)
  })

  it('chains dots that each overlap the next into one group', () => {
    // Three dots 12 units apart on a line: each overlaps its neighbour (12 < 16), so
    // they are one group even though the ends are 24 units apart. Order-independent
    // only because overlap is transitive here; the alternative depends on input order.
    const view = WORLD_VIEW
    const step = 12 / (VIEW_W * 1) * 360 // degrees of longitude per 12 units at zoom 0
    const cubes = [at('c1', 0, 0), at('c2', 0, step), at('c3', 0, 2 * step)]
    expect(groupDots(cubes, view, 8)).toHaveLength(1)
  })

  it('returns nothing for no cubes', () => {
    expect(groupDots([], WORLD_VIEW, 8)).toEqual([])
  })
})

describe('outlinePaths', () => {
  it('draws a polyline as an SVG path in view coordinates', () => {
    // At the world view, lon -180 and 180 on the equator are the two edges of the
    // surface; the equator sits at (0.5 - 0.42) * 960 + 260 = 336.8.
    const [d] = outlinePaths([[-180, 0, 180, 0]], WORLD_VIEW)
    expect(d).toBe('M0.0,336.8L960.0,336.8')
  })

  it('skips a line that lies wholly off the surface', () => {
    const denver = fitView([DENVER])
    // A short line in Australia is nowhere near a 1000 km frame on Denver.
    expect(outlinePaths([[150, -30, 151, -31]], denver)).toEqual([])
  })

  it('ignores a malformed line rather than drawing NaN', () => {
    expect(outlinePaths([[1, 2, 3], [], [Number.NaN, 0, 1, 1]], WORLD_VIEW)).toEqual([])
  })
})

describe('zoomBy', () => {
  const near = (a: { x: number; y: number; zoom: number }, b: typeof a) => {
    expect(a.x).toBeCloseTo(b.x, 9)
    expect(a.y).toBeCloseTo(b.y, 9)
    expect(a.zoom).toBeCloseTo(b.zoom, 9)
  }

  it('zooms by whole steps around the centre, each step doubling the scale', () => {
    const view = { x: 0.5, y: 0.5, zoom: 2 }
    near(zoomBy(view, 1), { x: 0.5, y: 0.5, zoom: 3 })
    near(zoomBy(view, -1), { x: 0.5, y: 0.5, zoom: 1 })
    // World x 0.75 is 0.25 right of the centre: 0.25 * 3840 = 960 units at zoom 2,
    // 0.25 * 7680 = 1920 at zoom 3.
    expect(toScreen({ x: 0.75, y: 0.5 }, view).x).toBeCloseTo(480 + 960, 6)
    expect(toScreen({ x: 0.75, y: 0.5 }, zoomBy(view, 1)).x).toBeCloseTo(480 + 1920, 6)
  })

  it('keeps the point under the cursor where it is', () => {
    // At zoom 0 (960 units per world unit), surface (720, 380) is world
    // (0.5 + 240/960, 0.5 + 120/960) = (0.75, 0.625). At zoom 1 (1920 units) that point
    // stays at (720, 380) only if the centre is (0.75 - 240/1920, 0.625 - 120/1920).
    const view = { x: 0.5, y: 0.5, zoom: 0 }
    const zoomed = zoomBy(view, 1, { x: 720, y: 380 })
    near(zoomed, { x: 0.625, y: 0.5625, zoom: 1 })
    // And back out around the same point lands where it started.
    near(zoomBy(zoomed, -1, { x: 720, y: 380 }), view)
  })

  it('takes fractional steps, as a trackpad pinch sends them', () => {
    near(zoomBy({ x: 0.5, y: 0.5, zoom: 2 }, 0.25), { x: 0.5, y: 0.5, zoom: 2.25 })
  })

  it('stops zooming in at about 50 km across, at the view\'s latitude', () => {
    let view = fitView([DENVER])
    for (let i = 0; i < 20; i++) view = zoomBy(view, 1)
    // 50 km at 39.74 degrees: 50 / (111.32 * cos 39.74) = 50 / 85.60 = 0.5841 degrees.
    expect(visibleLonSpan(view, DENVER.lat)).toBeCloseTo(0.5841, 3)
    // Denver is still in the middle, and one more step changes nothing.
    const p = toScreen(project(DENVER.lat, DENVER.lng), view)
    expect(p.x).toBeCloseTo(VIEW_W / 2, 6)
    expect(p.y).toBeCloseTo(VIEW_H / 2, 6)
    expect(zoomBy(view, 1)).toEqual(view)

    // On the equator the same 50 km is 50 / 111.32 = 0.4492 degrees.
    let equator = { x: 0.5, y: 0.5, zoom: 5 }
    for (let i = 0; i < 20; i++) equator = zoomBy(equator, 1)
    expect(visibleLonSpan(equator, 0)).toBeCloseTo(0.4492, 3)
  })

  it('stops zooming out once the whole world fits', () => {
    let view = WORLD_VIEW
    for (let i = 0; i < 10; i++) view = zoomBy(view, -1)
    // The world's full height (one world unit) fits the 520-unit surface height:
    // scale 520, zoom log2(520 / 960) = ln(13/24) / ln 2 = -0.613105 / 0.693147.
    expect(view.zoom).toBeCloseTo(-0.884523, 5)
    // So 360 degrees of longitude span 520 units, and 85 N to 85 S span
    // (1 - 2 * 0.00163) * 520 = 518.3.
    const west = toScreen(project(0, -180), view).x
    const east = toScreen(project(0, 180), view).x
    expect(east - west).toBeCloseTo(520, 6)
    const north = toScreen(project(85, 0), view).y
    const south = toScreen(project(-85, 0), view).y
    expect(south - north).toBeCloseTo(518.3, 0)
  })

  it('treats a fitted view as inside the limits, so Fit is never clamped', () => {
    const fleets = [
      [DENVER],
      US_SPREAD,
      [...US_SPREAD, LONDON],
      // Alaska to New Zealand: as tall as fitView ever frames.
      [at('nome', 64.5, -165.4), at('dunedin', -45.87, 170.5)],
    ]
    for (const fleet of fleets) {
      const fit = fitView(fleet)
      expect(clampView(fit)).toEqual(fit)
    }
    expect(clampView(WORLD_VIEW)).toEqual(WORLD_VIEW)
  })
})

describe('panBy', () => {
  it('moves everything on the surface by the given units', () => {
    // At zoom 0, 96 units right and 48 up moves the centre 96/960 = 0.1 left and
    // 48/960 = 0.05 down in world units.
    const view = { x: 0.5, y: 0.5, zoom: 0 }
    const panned = panBy(view, 96, -48)
    expect(panned.x).toBeCloseTo(0.4, 9)
    expect(panned.y).toBeCloseTo(0.55, 9)
    expect(panned.zoom).toBe(0)
    const before = toScreen(project(DENVER.lat, DENVER.lng), view)
    const after = toScreen(project(DENVER.lat, DENVER.lng), panned)
    expect(after.x - before.x).toBeCloseTo(96, 6)
    expect(after.y - before.y).toBeCloseTo(-48, 6)
    // At zoom 1 the same 96 units is half as far in world units: 96/1920 = 0.05.
    expect(panBy({ x: 0.5, y: 0.5, zoom: 1 }, 96, 0).x).toBeCloseTo(0.45, 9)
  })

  it('keeps the frame\'s centre on the world, so it can never be dragged away', () => {
    // Dragged far right and up: the centre stops at 180 W and the 85 S clip line
    // (world y 1 - 0.00163), so the world's south-west corner sits mid-surface.
    const southWest = panBy(WORLD_VIEW, 1e5, -1e5)
    expect(southWest.x).toBeCloseTo(0, 9)
    expect(southWest.y).toBeCloseTo(0.99837, 4)
    const corner = toScreen(project(-85, -180), southWest)
    expect(corner.x).toBeCloseTo(VIEW_W / 2, 6)
    expect(corner.y).toBeCloseTo(VIEW_H / 2, 6)
    // And the other way: 180 E and the 85 N clip line (world y 0.00163).
    const northEast = panBy(WORLD_VIEW, -1e5, 1e5)
    expect(northEast.x).toBeCloseTo(1, 9)
    expect(northEast.y).toBeCloseTo(0.00163, 4)
  })

  it('does not change the zoom when the world is not at an edge', () => {
    const view = fitView(US_SPREAD)
    expect(panBy(view, 30, 30).zoom).toBe(view.zoom)
  })
})

describe('clampView', () => {
  it('pulls the zoom and the centre back inside the limits', () => {
    // 50 km on the equator is 50 / 40075 of the world: zoom log2(801.5) = 9.6466.
    expect(clampView({ x: 0.5, y: 0.5, zoom: 20 }).zoom).toBeCloseTo(9.6466, 3)
    const out = clampView({ x: -1, y: 2, zoom: -5 })
    expect(out.x).toBe(0)
    expect(out.y).toBeCloseTo(0.99837, 4)
    expect(out.zoom).toBeCloseTo(-0.884523, 5)
  })
})

describe('clientToSurface', () => {
  it('converts a pointer position into surface units', () => {
    // Drawn at half size (480 x 260) at (100, 50): two units per pixel.
    const rect = { left: 100, top: 50, width: 480, height: 260 }
    const p = clientToSurface(340, 180, rect)
    expect(p!.x).toBeCloseTo(480, 9)
    expect(p!.y).toBeCloseTo(260, 9)
    const corner = clientToSurface(100, 50, rect)
    expect(corner!.x).toBeCloseTo(0, 9)
    expect(corner!.y).toBeCloseTo(0, 9)
  })

  it('allows for the letterbox when the box is taller than the surface', () => {
    // 960 x 1040 box: the 960 x 520 surface is drawn 1:1, centred, starting 260 down.
    const rect = { left: 0, top: 0, width: 960, height: 1040 }
    const p = clientToSurface(480, 260 + 130, rect)
    expect(p!.x).toBeCloseTo(480, 9)
    expect(p!.y).toBeCloseTo(130, 9)
  })

  it('answers null for an element with no size, rather than dividing by zero', () => {
    expect(clientToSurface(10, 10, { left: 0, top: 0, width: 0, height: 0 })).toBeNull()
  })
})

describe('wheelZoomSteps', () => {
  it('turns a wheel notch into one step, in, and caps a big flick at one', () => {
    expect(wheelZoomSteps(-100, 0)).toBeCloseTo(1, 9)
    expect(wheelZoomSteps(50, 0)).toBeCloseTo(-0.5, 9)
    expect(wheelZoomSteps(-1000, 0)).toBe(1)
    expect(wheelZoomSteps(1000, 0)).toBe(-1)
    expect(wheelZoomSteps(0, 0)).toBe(0)
  })

  it('counts a three-line notch (line mode) as one step', () => {
    expect(wheelZoomSteps(-3, 1)).toBeCloseTo(1, 9)
  })
})

describe('the Denver group as the zoom increases', () => {
  it('splits into separate dots', () => {
    const fleet = [...US_SPREAD, ...DENVER_AREA]
    const fit = fitView(fleet)
    const denver = toScreen(project(DENVER.lat, DENVER.lng), fit)
    const denverGroup = (k: number) => {
      const view = zoomBy(fit, k, denver)
      return groupDots(fleet, view, 8)
        .filter(g => g.members.some(m => DENVER_AREA.includes(m)))
        .map(g => g.members.length)
        .sort()
    }
    // At the fit (~5,500 units per world unit) all four are within a few units; one
    // step in, Boulder is still ~14 units from Denver (< 16) so they stay one group.
    expect(denverGroup(0)).toEqual([4])
    expect(denverGroup(1)).toEqual([4])
    // Four steps in (~88,000 units per world unit) the closest pair, Denver and
    // Lakewood (0.09 degrees of longitude, 0.04 of latitude, ~0.00029 world units
    // apart), is ~25 units apart: every dot stands alone.
    expect(denverGroup(4)).toEqual([1, 1, 1, 1])
  })
})

describe('onSurface', () => {
  it('counts a mark as shown while any of it overlaps the 960 x 520 surface', () => {
    expect(onSurface({ x: 480, y: 260 }, 6)).toBe(true)
    expect(onSurface({ x: -5, y: 10 }, 6)).toBe(true) // 1 unit of it still shows
    expect(onSurface({ x: -7, y: 10 }, 6)).toBe(false)
    expect(onSurface({ x: 966, y: 526 }, 6)).toBe(true)
    expect(onSurface({ x: 480, y: 527 }, 6)).toBe(false)
  })
})

/** Geometry for the landing page's fleet map: projection, framing and dot grouping.
 *
 *  Plain functions of (data, view), following the rules `LineChart.tsx` sets for the
 *  console's SVG: a fixed drawing surface (`VIEW_W` x `VIEW_H`, scaled by `viewBox`),
 *  nothing measured from the DOM, so every number here is testable in jsdom with no
 *  layout and the map renders the same in the Docker build's test run as in a browser.
 *
 *  A view is a centre (in projected world units) and a zoom level, nothing else, so
 *  zooming and panning are changes to that state and drawing stays a function of it.
 *
 *  Coordinates: Web Mercator in a unit square. x = 0 at 180 W and 1 at 180 E; y = 0 at
 *  the top. Latitude is clipped at +/- 85 degrees, where Mercator heads to infinity. At
 *  zoom 0 the world's full width fills the surface; each zoom step doubles the scale.
 *  Longitude wraps nowhere: a fleet straddling the antimeridian is framed the long way
 *  round, which no current fleet does.
 */

export const VIEW_W = 960
export const VIEW_H = 520
/** Surface units kept clear around the framed cubes, so an edge dot is not cut off. */
export const FIT_PADDING = 48
/** The narrowest frame `fitView` picks: one cube shows its region, not a street. Wide
 *  enough that a lone cube's state borders and neighbours are in view (Colorado, for
 *  one, is about 600 km across). */
export const MIN_FRAME_KM = 1000
/** Earth's equatorial circumference: one world-width at the equator. */
const EARTH_KM = 40075
const MAX_LAT = 85

export type WorldPoint = { x: number; y: number }
export type ScreenPoint = { x: number; y: number }
export type View = {
  /** Centre of the surface, in world units. */
  x: number
  y: number
  /** log2 of (surface units per world unit / VIEW_W). */
  zoom: number
}
export type Located = { name: string; lat: number; lng: number }
export type DotGroup<T extends Located> = { x: number; y: number; members: T[] }

/** The whole world, nudged north of the equator so the inhabited latitudes fill the
 *  surface (about 77 N to 56 S at this aspect ratio) rather than Antarctica. */
export const WORLD_VIEW: View = { x: 0.5, y: 0.42, zoom: 0 }

const clampLat = (lat: number) => Math.max(-MAX_LAT, Math.min(MAX_LAT, lat))

export function project(lat: number, lng: number): WorldPoint {
  const phi = (clampLat(lat) * Math.PI) / 180
  return {
    x: (lng + 180) / 360,
    y: (1 - Math.log(Math.tan(Math.PI / 4 + phi / 2)) / Math.PI) / 2,
  }
}

/** The latitude at world y; the inverse of `project`'s y. */
function latitudeAt(y: number): number {
  return (Math.atan(Math.sinh(Math.PI * (1 - 2 * y))) * 180) / Math.PI
}

const scaleOf = (view: View) => VIEW_W * 2 ** view.zoom

export function toScreen(p: WorldPoint, view: View): ScreenPoint {
  const s = scaleOf(view)
  return { x: (p.x - view.x) * s + VIEW_W / 2, y: (p.y - view.y) * s + VIEW_H / 2 }
}

/** Frame the points: their bounding box fills the surface inside `FIT_PADDING`, but
 *  never narrower than `MIN_FRAME_KM` across at the frame's centre latitude, and never
 *  wider than the world's full height. No points: the world. */
export function fitView(points: readonly { lat: number; lng: number }[]): View {
  if (points.length === 0) return WORLD_VIEW
  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity
  for (const { lat, lng } of points) {
    const p = project(lat, lng)
    minX = Math.min(minX, p.x)
    maxX = Math.max(maxX, p.x)
    minY = Math.min(minY, p.y)
    maxY = Math.max(maxY, p.y)
  }
  const x = (minX + maxX) / 2
  const y = (minY + maxY) / 2
  const fitW = maxX > minX ? (VIEW_W - 2 * FIT_PADDING) / (maxX - minX) : Infinity
  const fitH = maxY > minY ? (VIEW_H - 2 * FIT_PADDING) / (maxY - minY) : Infinity
  // One world-width is EARTH_KM * cos(lat) across at latitude lat, so a frame
  // MIN_FRAME_KM wide there needs at most this many surface units per world unit.
  const cos = Math.cos((latitudeAt(y) * Math.PI) / 180)
  const floor = (VIEW_W * EARTH_KM * cos) / MIN_FRAME_KM
  const scale = Math.max(VIEW_H, Math.min(fitW, fitH, floor))
  return { x, y, zoom: Math.log2(scale / VIEW_W) }
}

/** Whether a mark of radius `margin` at `p` shows any part of itself on the surface. */
export function onSurface(p: ScreenPoint, margin: number): boolean {
  return p.x >= -margin && p.x <= VIEW_W + margin && p.y >= -margin && p.y <= VIEW_H + margin
}

/** Group points whose dots (radius `radiusPx` surface units) would overlap at `view`.
 *
 *  Overlap is joined transitively (single linkage): a dot touching either of two
 *  grouped dots joins their group. That is what makes the answer independent of input
 *  order; a greedy "join the first group in range" would not be. Members are sorted by
 *  name and groups by their first member, so the output is deterministic too. A group
 *  sits at the mean of its members' positions. */
export function groupDots<T extends Located>(
  points: readonly T[],
  view: View,
  radiusPx: number,
): DotGroup<T>[] {
  const sorted = [...points].sort(
    (a, b) => a.name.localeCompare(b.name) || a.lat - b.lat || a.lng - b.lng,
  )
  const at = sorted.map(p => toScreen(project(p.lat, p.lng), view))
  const parent = sorted.map((_, i) => i)
  const root = (i: number): number => {
    while (parent[i] !== i) i = parent[i] = parent[parent[i]!]!
    return i
  }
  const reach = 2 * radiusPx
  for (let i = 0; i < sorted.length; i++) {
    for (let j = i + 1; j < sorted.length; j++) {
      if (Math.hypot(at[i]!.x - at[j]!.x, at[i]!.y - at[j]!.y) < reach) {
        const a = root(i)
        const b = root(j)
        if (a !== b) parent[Math.max(a, b)] = Math.min(a, b)
      }
    }
  }
  const byRoot = new Map<number, number[]>()
  sorted.forEach((_, i) => {
    const r = root(i)
    byRoot.set(r, [...(byRoot.get(r) ?? []), i])
  })
  // Map insertion follows the sorted index of each group's first member.
  return [...byRoot.values()].map(indexes => ({
    x: indexes.reduce((sum, i) => sum + at[i]!.x, 0) / indexes.length,
    y: indexes.reduce((sum, i) => sum + at[i]!.y, 0) / indexes.length,
    members: indexes.map(i => sorted[i]!),
  }))
}

/** SVG path data for each outline polyline (flat [lon, lat, lon, lat, ...]) at `view`.
 *  A line wholly off the surface is skipped, and a malformed one (odd length, fewer
 *  than two points, a non-finite number) is ignored rather than drawn as NaN, which
 *  renders nothing and reports nothing. */
export function outlinePaths(lines: readonly (readonly number[])[], view: View): string[] {
  const out: string[] = []
  for (const line of lines) {
    if (line.length < 4 || line.length % 2 !== 0 || !line.every(Number.isFinite)) continue
    let d = ''
    let minX = Infinity
    let maxX = -Infinity
    let minY = Infinity
    let maxY = -Infinity
    for (let i = 0; i < line.length; i += 2) {
      const p = toScreen(project(line[i + 1]!, line[i]!), view)
      d += `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`
      minX = Math.min(minX, p.x)
      maxX = Math.max(maxX, p.x)
      minY = Math.min(minY, p.y)
      maxY = Math.max(maxY, p.y)
    }
    if (maxX < 0 || minX > VIEW_W || maxY < 0 || minY > VIEW_H) continue
    out.push(d)
  }
  return out
}

// ---------------------------------------------------------------------------
// Zooming and panning
// ---------------------------------------------------------------------------

/** The narrowest view zooming in reaches, across at the view's centre latitude. An
 *  outline map has nothing more to show closer than this. */
export const MIN_VIEW_KM = 50
/** The widest view: the world's full height (one world unit) fills the surface height.
 *  `fitView` never frames wider than this either, so a fitted view is always inside
 *  the limits and Fit returns to it exactly. */
export const MIN_ZOOM = Math.log2(VIEW_H / VIEW_W)
/** World y of the 85 degree clip lines, the top and bottom of the drawable world. */
const WORLD_TOP = project(MAX_LAT, 0).y
const WORLD_BOTTOM = project(-MAX_LAT, 0).y
/** Wheel distance, in pixels, that zooms one whole step; a bigger flick still zooms
 *  only one step, so one event can never jump from the world to a street. */
const WHEEL_PX_PER_STEP = 100
/** A line-mode wheel (Firefox's default) reports about three lines per notch. */
const WHEEL_PX_PER_LINE = WHEEL_PX_PER_STEP / 3

const clamp = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v))

/** The deepest zoom at world y: MIN_VIEW_KM across at that latitude, where one world
 *  width is EARTH_KM * cos(lat). */
function maxZoomAt(y: number): number {
  const cos = Math.cos((latitudeAt(y) * Math.PI) / 180)
  return Math.log2((EARTH_KM * cos) / MIN_VIEW_KM)
}

const clampZoom = (zoom: number, y: number) => clamp(zoom, MIN_ZOOM, maxZoomAt(y))

/** The view pulled back inside the limits. The pan rule: the surface's centre always
 *  lies on the drawn world (180 W to 180 E, 85 N to 85 S), so however far it is
 *  dragged at least a quarter of the frame still shows map, and a view can never be
 *  lost off the edge. The zoom is clamped at the (clamped) centre's latitude. */
export function clampView(view: View): View {
  const x = clamp(view.x, 0, 1)
  const y = clamp(view.y, WORLD_TOP, WORLD_BOTTOM)
  return { x, y, zoom: clampZoom(view.zoom, y) }
}

/** Zoom by `steps` (1 doubles the scale, -1 halves it; fractions allowed) keeping the
 *  world point under `around` (surface units, default the centre) where it is. The
 *  zoom limit is taken at that point's latitude, so zooming into a spot stops at
 *  MIN_VIEW_KM across there. */
export function zoomBy(
  view: View,
  steps: number,
  around: ScreenPoint = { x: VIEW_W / 2, y: VIEW_H / 2 },
): View {
  const dx = around.x - VIEW_W / 2
  const dy = around.y - VIEW_H / 2
  const s = scaleOf(view)
  const wx = view.x + dx / s
  const wy = view.y + dy / s
  const zoom = clampZoom(view.zoom + steps, wy)
  const s2 = VIEW_W * 2 ** zoom
  return clampView({ x: wx - dx / s2, y: wy - dy / s2, zoom })
}

/** Move everything on the surface by (dx, dy) surface units, as a drag does: dragging
 *  right moves the map right, so the centre moves left. */
export function panBy(view: View, dx: number, dy: number): View {
  const s = scaleOf(view)
  return clampView({ x: view.x - dx / s, y: view.y - dy / s, zoom: view.zoom })
}

/** A pointer's client position as surface units, given the element's on-screen box
 *  (read by the caller at event time; nothing here measures anything). Allows for the
 *  letterbox `preserveAspectRatio="xMidYMid meet"` leaves when the box's shape differs
 *  from the surface's. Null for a box with no size, which jsdom reports. */
export function clientToSurface(
  clientX: number,
  clientY: number,
  rect: { left: number; top: number; width: number; height: number },
): ScreenPoint | null {
  if (!(rect.width > 0) || !(rect.height > 0)) return null
  const unitsPerPx = Math.max(VIEW_W / rect.width, VIEW_H / rect.height)
  const padX = (rect.width * unitsPerPx - VIEW_W) / 2
  const padY = (rect.height * unitsPerPx - VIEW_H) / 2
  return {
    x: (clientX - rect.left) * unitsPerPx - padX,
    y: (clientY - rect.top) * unitsPerPx - padY,
  }
}

/** Zoom steps for one wheel event: scrolling up (negative deltaY) zooms in. */
export function wheelZoomSteps(deltaY: number, deltaMode: number): number {
  // deltaMode 0 is pixels, 1 lines, 2 pages (a page is far past the one-step cap).
  const px = deltaMode === 1 ? deltaY * WHEEL_PX_PER_LINE
    : deltaMode === 2 ? deltaY * VIEW_H
      : deltaY
  return clamp(-px / WHEEL_PX_PER_STEP, -1, 1) || 0
}

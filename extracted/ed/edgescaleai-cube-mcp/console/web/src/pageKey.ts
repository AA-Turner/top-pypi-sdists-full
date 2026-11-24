/**
 * Which navigations start a page afresh.
 *
 * Some routes are keyed on the navigation (`App.tsx`), so following a link to the page
 * already open re-reads it instead of doing nothing. But a page that keeps its own
 * state in the URL (the Products tab's open product, `?product=`) changes the location
 * too, and each change is a new `location.key`: keyed on that alone, opening a
 * product unmounted the whole page and read the product list again.
 *
 * So an in-page URL change carries the page's key forward in the router state
 * (`samePage`), and the route keys on `pageKey`. A link from anywhere else carries no
 * such state and still gets a fresh page.
 */
import type { Location } from 'react-router-dom'

/** The key a route should use: the one carried forward by an in-page change, else this
 *  navigation's own. */
export function pageKey(location: Location): string {
  const kept = (location.state as { pageKey?: unknown } | null)?.pageKey
  return typeof kept === 'string' ? kept : location.key
}

/** Router state for a URL change that stays on the same page. */
export function samePage(location: Location): { pageKey: string } {
  return { pageKey: pageKey(location) }
}

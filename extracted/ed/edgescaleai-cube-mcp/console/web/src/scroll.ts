/** Scroll the window to the top, for a page reached by a link.
 *
 *  jsdom implements no scrolling and reports every call as an error, so a missing or
 *  throwing `scrollTo` is ignored rather than allowed to break a navigation. */
export function scrollToTop() {
  try {
    window.scrollTo({ top: 0, left: 0 })
  } catch {
    // Nothing to scroll.
  }
}

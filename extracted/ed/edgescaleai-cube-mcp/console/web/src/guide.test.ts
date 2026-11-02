/**
 * Invariants for the Cube Field Guide (docs/console-spec.md §4.11).
 *
 * The guide is NOT part of this React app — it is a separate document under
 * `public/guide/`, which Vite copies verbatim into the Python package. It is
 * tested from here anyway, and deliberately so: `npm run build` is `tsc --noEmit
 * && vitest run && vite build`, and the Dockerfile's node stage runs that build,
 * so a red test here cannot produce a container image. There is no equivalent
 * gate on the Python side — pytest cannot execute the guide's JavaScript.
 *
 * **This suite is the guide's only real guarantee.** Those three files are the
 * source of truth and are edited by hand, in the repo; nothing about a text
 * editor stops someone reintroducing a `localStorage` call, pasting a customer
 * name back in, or breaking a lesson's rendering. `vendor-field-guide.py` made
 * these properties true once, at import; this is what keeps them true.
 *
 * Four things are pinned:
 *
 * 1. **Every lesson still renders.** A whole component is stubbed and nine
 *    templates were cut at import, so the JS is full of code paths nothing
 *    reaches — an edit that reconnects one, or breaks a template literal, shows
 *    up as a blank lesson. Walking all of them is the only detector for that.
 * 2. **No state.** Zero `localStorage` and zero network APIs, which is both the
 *    "static pages" requirement and what lets the served document declare
 *    `connect-src 'none'`.
 * 3. **No customer identity.** `/console` is multi-tenant. Note this is a list of
 *    KNOWN names, not a detector — it catches the residual strings the authored
 *    export left behind, and a regression that pastes them back, but new content
 *    about a real deployment still needs a human to anonymise it.
 * 4. **No inline `<script>` or `<style>`.** The served document's CSP has no
 *    `'unsafe-inline'` for scripts, so an inline block would not execute at all.
 */
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

import { beforeEach, describe, expect, it } from 'vitest'

const GUIDE_DIR = resolve(__dirname, '../public/guide')
const read = (name: string) => readFileSync(resolve(GUIDE_DIR, name), 'utf8')

const indexHtml = read('index.html')
const guideCss = read('guide.css')
const guideJs = read('guide.js')

/** Must match `console/routes.py::GUIDE_PREFIX`. */
const GUIDE_PREFIX = '/console/guide'

/**
 * Boot the guide the way a browser does and hand back the live document.
 *
 * `new Function` rather than an `import`: the guide's templates use `with(vm)`,
 * which is illegal in strict mode, and this package is `"type": "module"` so
 * anything imported here would be strict. A `<script src>` in a real browser is a
 * classic script — sloppy mode — and `new Function` reproduces that, since the
 * Function constructor does not inherit the caller's strictness.
 */
function boot() {
  const body = indexHtml.slice(indexHtml.indexOf('<body>') + '<body>'.length, indexHtml.indexOf('</body>'))

  // Parsed into a <template> and stripped through the DOM rather than by regex.
  // A `<script[\s\S]*?<\/script>` replace is what CodeQL calls an incomplete
  // multi-character sanitization: one pass cannot reason about nesting or about
  // the same characters appearing inside a comment. Using the parser makes the
  // question ("which script elements are in this document") exact. Assigning to
  // innerHTML never executes scripts, so this is safe before the removal too.
  const parsed = document.createElement('template')
  parsed.innerHTML = body
  parsed.content.querySelectorAll('script').forEach(el => el.remove())
  document.body.replaceChildren(parsed.content)

  const errors: unknown[] = []
  window.addEventListener('error', (e: ErrorEvent) => errors.push(e.error ?? e.message))
  // jsdom has no scrollTo and logs "Not implemented" noise on every lesson change.
  window.scrollTo = () => {}

  new Function(guideJs)()

  return {
    errors,
    main: document.getElementById('main') as HTMLElement,
    side: document.getElementById('side') as HTMLElement,
  }
}

/** Lesson ids in COURSE order, read out of the committed bundle. */
function courseLessonIds(): string[] {
  const course = /const COURSE=\[[\s\S]*?\n\];/.exec(guideJs)
  if (!course) throw new Error('could not find COURSE in guide.js')
  return [...course[0].matchAll(/\[\s*"[^"]*"\s*,\s*"[^"]*"\s*,\s*"([^"]+)"\s*\]/g)].map(m => m[1]!)
}

describe('the field guide renders', () => {
  beforeEach(() => {
    document.body.innerHTML = ''
  })

  it('boots and walks every lesson COURSE lists without an error', () => {
    const { errors, main, side } = boot()
    const total = courseLessonIds().length
    expect(total).toBeGreaterThan(20)

    // The first lesson is rendered by the bundle's own trailing render() call.
    const rendered: number[] = [main.innerHTML.length]
    expect(side.innerHTML.length).toBeGreaterThan(0)

    // "Next lesson" walks the whole course regardless of which sidebar accordions
    // are open, and disappears on the final lesson — which is the loop's bound.
    for (let step = 0; step < total; step++) {
      const next = document.querySelector<HTMLElement>('[data-nav="1"]')
      if (!next) break
      next.click()
      rendered.push(main.innerHTML.length)
    }

    expect(errors).toEqual([])
    expect(rendered).toHaveLength(total)
    // Every lesson produced real content. A stubbed-out component or a cut
    // template would show up here as an empty or near-empty body.
    for (const [i, length] of rendered.entries()) {
      expect(length, `lesson ${i} rendered ${length} chars`).toBeGreaterThan(200)
    }
  })

  it('offers the way back to the console on the last lesson', () => {
    boot()
    const total = courseLessonIds().length
    for (let step = 0; step < total; step++) {
      const next = document.querySelector<HTMLElement>('[data-nav="1"]')
      if (!next) break
      next.click()
    }
    expect(document.querySelector('[data-nav="1"]')).toBeNull()
    // A real navigation out of the guide, not a lesson.
    const back = document.querySelector<HTMLAnchorElement>('.nav a.btn')
    expect(back?.getAttribute('href')).toBe('/console')
  })

  it('renders no progress chrome', () => {
    const { side } = boot()
    // There is no progress backend, and a percentage that resets on reload would
    // promise one. The chip, the sidebar bar, and the checkmarks are all gone.
    expect(document.getElementById('progChip')).toBeNull()
    expect(side.querySelector('.prog-t')).toBeNull()
    expect(side.querySelector('.prog-f')).toBeNull()
    expect(document.body.innerHTML).not.toContain('% complete')
    expect(side.querySelector('.ck')).toBeNull()
  })

  it('renders no doubled words, which find-and-replace leaves behind', () => {
    // The authored guide is maintained by substitution ("Peplink" -> "the site
    // router", "Teleport" -> "Secure Access"), and a substitution that collides
    // with the following word leaves "The the site router" or "Secure Access
    // access" in the reader's face. Three shipped that way; this is the detector.
    //
    // Case-INSENSITIVE, or "The the" slips past — differing case is the usual
    // shape when the replacement lands mid-sentence. Alphabetic words of 2+ chars
    // only, so SVG path coordinates ("0 0", "24 24") are not false positives.
    //
    // Scanned per TEXT NODE, not over `main.textContent`. Concatenating the whole
    // subtree invents doubles that no reader sees: a heading "Identifying a Cube"
    // followed by a paragraph starting "Cube MCP filters…", or the two nav buttons
    // "← Back" and "Back to the console". A real doubled word is inside one node.
    const doubled = /\b([A-Za-z]{2,}) \1\b/i
    const found: string[] = []

    boot()
    const total = courseLessonIds().length
    for (let step = 0; step <= total; step++) {
      const main = document.getElementById('main')!
      const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT)
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        const text = (n.textContent || '').replace(/\s+/g, ' ')
        const m = doubled.exec(text)
        if (m) found.push(`lesson ${step}: "${text.slice(Math.max(0, m.index - 40), m.index + 60)}"`)
      }
      const next = document.querySelector<HTMLElement>('[data-nav="1"]')
      if (!next) break
      next.click()
    }

    expect(found).toEqual([])
  })

  it('has no dead cross-links', () => {
    // Lessons link to each other with `data-golesson="<lesson id>"`, which the
    // shell resolves against COURSE. A target that is NOT in COURSE silently does
    // nothing — no error, no navigation, just a link that does not work.
    //
    // This matters specifically because the import CUTS nine templates the
    // authored guide still contains. A new cross-link upstream pointing at one of
    // them (v2:handson, v2:ho_deploy, …) would ship as a dead link here and
    // nowhere else, so this cannot be checked in the authored file.
    boot()
    const listed = new Set(courseLessonIds())
    const total = listed.size
    const targets = new Set<string>()
    for (let step = 0; step <= total; step++) {
      document.querySelectorAll<HTMLElement>('#main [data-golesson]')
        .forEach(a => targets.add(a.dataset.golesson!))
      const next = document.querySelector<HTMLElement>('[data-nav="1"]')
      if (!next) break
      next.click()
    }

    expect(targets.size).toBeGreaterThan(0)
    expect([...targets].filter(t => !listed.has(t))).toEqual([])
  })

  it('carries the support address on every lesson', () => {
    // Added upstream, and it matches the console's own convention (spec 4.10):
    // help@edgescaleai.com on every state, not just the ones that go well.
    boot()
    const total = courseLessonIds().length
    let withFooter = 0
    for (let step = 0; step <= total; step++) {
      if (document.getElementById('main')!.querySelector('.gfoot')) withFooter++
      const next = document.querySelector<HTMLElement>('[data-nav="1"]')
      if (!next) break
      next.click()
    }
    expect(withFooter).toBe(total)
  })

  // D-1 "The Cube Stack" toggles its layers in the DOM rather than through a
  // re-render. A collapsed panel is clipped to zero height for the animation,
  // which on its own leaves the text readable by a screen reader while the
  // button announces "collapsed" — so the panel must also be inert, and the CSS
  // must hide it, for aria-expanded="false" to be true.
  it('hides a collapsed Cube Stack layer from assistive tech and toggles it in place', () => {
    const { main } = boot()
    for (let step = 0; step < courseLessonIds().length && !main.querySelector('[data-ilt]'); step++) {
      document.querySelector<HTMLElement>('[data-nav="1"]')!.click()
    }
    const buttons = [...main.querySelectorAll<HTMLButtonElement>('[data-ilt]')]
    expect(buttons).toHaveLength(6)

    const panelOf = (b: HTMLElement) => document.getElementById(b.getAttribute('aria-controls') ?? '')
    for (const b of buttons) {
      expect(b.getAttribute('aria-expanded')).toBe('false')
      expect(panelOf(b), 'button is associated with its panel').not.toBeNull()
      expect(panelOf(b)!.hasAttribute('inert')).toBe(true)
    }

    const [first, second] = buttons as [HTMLButtonElement, HTMLButtonElement]
    first.click()
    second.click()
    // Toggled in place: the same nodes, and both open at once.
    expect(main.contains(first)).toBe(true)
    expect(first.getAttribute('aria-expanded')).toBe('true')
    expect(panelOf(first)!.hasAttribute('inert')).toBe(false)
    expect(panelOf(second)!.hasAttribute('inert')).toBe(false)

    first.click()
    expect(first.getAttribute('aria-expanded')).toBe('false')
    expect(panelOf(first)!.hasAttribute('inert')).toBe(true)

    expect(guideCss).toMatch(/\.fgl \.ilexp\{[^}]*visibility:hidden/)
    expect(guideCss).toMatch(/\.fgl \.ilgroup\.open \.ilexp\{[^}]*visibility:visible/)
  })

  // The guide stores nothing, so its theme lives in the URL: `?theme=light` from
  // the console selects it, the toggle keeps the URL in step, and both links back
  // to the console carry it. Dark is the default and adds nothing to any URL.
  it('switches theme without storing it, and carries the choice back to the console', () => {
    window.history.replaceState(null, '', '/console/guide')
    delete document.documentElement.dataset.theme
    boot()
    expect(document.documentElement.dataset.theme).toBeUndefined()
    expect(document.getElementById('toConsole')?.getAttribute('href')).toBe('/console')

    document.querySelector<HTMLElement>('[data-theme-set="light"]')!.click()
    expect(document.documentElement.dataset.theme).toBe('light')
    expect(window.location.search).toBe('?theme=light')
    expect(document.getElementById('toConsole')?.getAttribute('href')).toBe('/console?theme=light')

    for (let step = 0; step < courseLessonIds().length; step++) {
      const next = document.querySelector<HTMLElement>('[data-nav="1"]')
      if (!next) break
      next.click()
    }
    expect(document.querySelector('.nav a.btn')?.getAttribute('href')).toBe('/console?theme=light')

    document.querySelector<HTMLElement>('[data-theme-set="dark"]')!.click()
    expect(document.documentElement.dataset.theme).toBeUndefined()
    expect(window.location.search).toBe('')
  })

  it('opens in light when the console hands it ?theme=light', () => {
    window.history.replaceState(null, '', '/console/guide?theme=light')
    delete document.documentElement.dataset.theme
    boot()
    expect(document.documentElement.dataset.theme).toBe('light')
    expect(document.querySelector('[data-theme-set="light"]')?.getAttribute('aria-pressed')).toBe('true')
    window.history.replaceState(null, '', '/')
    delete document.documentElement.dataset.theme
  })

  it('keeps the OS switcher working without persisting the choice', () => {
    const { main } = boot()
    expect(main.innerHTML).toContain('cos-mac')

    const windows = document.querySelector<HTMLElement>('[data-cos="win"]')
    windows!.click()
    expect(main.innerHTML).toContain('cos-win')
    expect(main.innerHTML).not.toContain('cos-mac')
  })
})

describe('the field guide keeps no state', () => {
  // Both halves of the guarantee: nothing is remembered between loads, and there
  // is nothing for the served document's `connect-src 'none'` to block.
  const bannedApis = [
    'localStorage',
    'sessionStorage',
    'indexedDB',
    'WebSocket',
    'XMLHttpRequest',
    'navigator.sendBeacon',
    'BROKER_URL',
    'BEACON_URL',
  ]

  it.each(bannedApis)('never mentions %s', api => {
    expect(guideJs).not.toContain(api)
    expect(indexHtml).not.toContain(api)
  })

  it.each(['fetch\\s*\\(', 'eval\\s*\\(', 'new Function'])('never calls %s', pattern => {
    // `script-src 'self'` carries no 'unsafe-eval', so a dynamic-code path would
    // fail at runtime rather than merely being untidy.
    expect(guideJs).not.toMatch(new RegExp(pattern))
  })
})

describe('the field guide is publishable to every tenant', () => {
  // `export-external.py`, the authored guide's own exporter, removes the internal
  // chapter's templates but leaves the component DATA behind — its
  // RESIDUAL_MARKERS list names "Lear Hammond" as something it reports rather
  // than removes. The console is multi-tenant, so one customer's name in a JS
  // blob is readable by every other customer via View Source.
  //
  // CUSTOMER identity only. Vendor and product names that are part of the Cube or
  // the platform — Peplink (the Cube's router), Palantir, Apollo, Foundry,
  // Teleport, Groundcover, Trino — are legitimate content and MUST NOT be listed
  // here: a name in this list cannot be written into a lesson at all, so a wrong
  // entry silently blocks correct documentation. `Peplink` was in this list by
  // mistake for exactly that reason.
  //
  // Matched CASE-INSENSITIVELY, and that is load-bearing. The first version of
  // this list had `seatforge`/`Seatforge`, neither of which matches the spelling
  // actually in the file — `SeatForge` — so a customer product name shipped
  // through a test that looked like it covered it.
  const denied = [
    'Lear Hammond',   // the customer
    'lear.com',       // their domain
    'grandprairie',   // their plant's town, which the export renames the company but not the site
    'SeatForge',      // their product
    'cube-9px8lv5i',  // a real Apollo environment id
    'onboarding.edgescaleai.com',  // a host that does not exist
  ]

  it.each(denied)('does not ship the string %s (any case)', needle => {
    const re = new RegExp(needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i')
    expect(guideJs).not.toMatch(re)
    expect(guideCss).not.toMatch(re)
    expect(indexHtml).not.toMatch(re)
  })

  it('does not ship the customer name on its own, ignoring innocent substrings', () => {
    // `Lear` needs word boundaries or it fires on "clear", "learn", "learner" —
    // 120 harmless lowercase hits. Bare `toContain` was unusable here, which is
    // why the entry above is the two-word form; this covers the one-word form.
    expect(guideJs).not.toMatch(/\bLear\b/)
    expect(guideJs).not.toMatch(/\bHammond\b/i)
  })
})

describe('the field guide is themeable', () => {
  // Light mode works by giving every color a --k<role>-<color> variable with a
  // dark value (:root) and a light one (:root[data-theme="light"]). A literal
  // color added anywhere else renders the same in both themes — usually dark
  // text on a now-light panel — so it is refused here rather than found by eye.
  const colorRe = /#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\((?!var)/
  const tokenBlock = (sel: string) => {
    const at = guideCss.indexOf(sel)
    return guideCss.slice(guideCss.indexOf('{', at) + 1, guideCss.indexOf('}', at))
  }
  const kVars = (body: string) => new Set([...body.matchAll(/(--k[fsl]-[\w]+):/g)].map(m => m[1]))

  it('defines a light value for every color variable', () => {
    const dark = kVars(tokenBlock('\n:root{--k'))
    const light = kVars(tokenBlock(':root[data-theme="light"]'))
    expect(dark.size).toBeGreaterThan(100)
    expect([...dark].filter(v => !light.has(v))).toEqual([])
  })

  it('uses no literal color outside the token blocks', () => {
    const lightEnd = guideCss.indexOf('}', guideCss.indexOf(':root[data-theme="light"]')) + 1
    const rules = guideCss
      .slice(lightEnd)
      .replace(/url\("data:[^"]*"\)/g, '')
    expect(rules.match(colorRe)?.[0]).toBeUndefined()

    const js = guideJs.replace(/data:[a-z/+]+;base64,[A-Za-z0-9+/=]+/g, '')
    const literalStyles = [...js.matchAll(/style="([^"]*)"/g)].map(m => m[1]!).filter(s => colorRe.test(s))
    expect(literalStyles).toEqual([])
    expect(js.match(/\s(?:fill|stroke)="#[0-9a-fA-F]{3,6}"/)?.[0]).toBeUndefined()
  })
})

describe('the field guide shell fits its CSP', () => {
  // Parsed once, with a real HTML parser. A `<script([^>]*)>` regex cannot tell a
  // tag from the same characters inside a comment or an attribute value, and this
  // is the assertion that certifies the split letting the document drop
  // 'unsafe-inline' from script-src — a check that can be fooled is worse than
  // none. (CodeQL: js/bad-tag-filter.)
  const shellDoc = new DOMParser().parseFromString(indexHtml, 'text/html')

  it('carries exactly one script, external, with no body', () => {
    const scripts = [...shellDoc.querySelectorAll('script')]
    expect(scripts).toHaveLength(1)
    expect(scripts[0]!.getAttribute('src')).toBe(`${GUIDE_PREFIX}/guide.js`)
    // An external script with inline content would run the inline part too.
    expect(scripts[0]!.textContent?.trim()).toBe('')
  })

  it('carries no inline style element', () => {
    // The 500+ inline style ATTRIBUTES are why `style-src` needs 'unsafe-inline';
    // a `<style>` element would mean the split missed a block.
    expect(shellDoc.querySelectorAll('style')).toHaveLength(0)
  })

  it('loads its assets from the path the server serves them on', () => {
    expect(indexHtml).toContain(`<script src="${GUIDE_PREFIX}/guide.js">`)
    expect(indexHtml).toContain(`<link rel="stylesheet" href="${GUIDE_PREFIX}/guide.css">`)
  })

  it('asks not to be indexed', () => {
    expect(indexHtml).toContain('name="robots" content="noindex, nofollow"')
  })

  it('carries the Edgescale favicon from the shared /static mount', () => {
    // NOT a data: URI (which the authored file used) and NOT under
    // /console/guide/: one file in cube-cloud's auth-exempt /static mount backs
    // this page, the console shell, and the four /auth/* pages. Root-absolute, or
    // it would resolve under /console/guide/ and 404.
    expect(indexHtml).toContain('href="/static/favicon.svg"')
    expect(indexHtml).toContain('href="/static/favicon.png"')
  })
})

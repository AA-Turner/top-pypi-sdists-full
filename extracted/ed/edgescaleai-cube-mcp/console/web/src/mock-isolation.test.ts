/**
 * The layout-preview mock must never reach the shipped bundle.
 *
 * `mock/fixtures.ts` contains invented customer names, site labels and serials. If
 * anything under `src/` ever imported it, `vite build` would inline that data into
 * the production bundle and the console would ship placeholder customers — the same
 * class of failure as the field guide carrying another customer's name into the repo
 * (`guide.test.ts`, and docs/console-spec.md §4.11).
 *
 * **Why a source-level check rather than scanning the built bundle.** The bundle is
 * gitignored and is written by `vite build`, which runs AFTER this suite inside
 * `npm run build` — so a test that read `console/static/` would find nothing and
 * pass vacuously on a clean checkout. A test that silently does not run is worse
 * than no test, and this repo has already been bitten by exactly that (the duckdb
 * dev-dependency note in AGENTS.md). "Nothing in `src/` references the mock" is the
 * property that actually guarantees the bundle is clean, and it is checkable here,
 * on every build, with no build ordering to get wrong.
 */
import { describe, it, expect } from 'vitest'
import { readFileSync, readdirSync, statSync } from 'node:fs'
import { resolve, join } from 'node:path'

const SRC = __dirname
const WEB = resolve(__dirname, '..')

function sourceFiles(dir: string): string[] {
  return readdirSync(dir).flatMap(entry => {
    const path = join(dir, entry)
    if (statSync(path).isDirectory()) return sourceFiles(path)
    return /\.(ts|tsx)$/.test(entry) ? [path] : []
  })
}

/** Anything that would pull the mock into a module graph rooted at `src/`. */
const FORBIDDEN = [
  'mock/fixtures',
  '../mock',
  './mock',
  'vite.mock.config',
]

describe('the layout-preview mock is isolated from the shipped bundle', () => {
  it('is referenced by no source file under src/', () => {
    const offenders: string[] = []
    for (const file of sourceFiles(SRC)) {
      // This very test names the forbidden strings, so it must exempt itself.
      if (file === resolve(SRC, 'mock-isolation.test.ts')) continue
      const text = readFileSync(file, 'utf8')
      for (const needle of FORBIDDEN) {
        if (text.includes(needle)) offenders.push(`${file} -> ${needle}`)
      }
    }
    expect(offenders).toEqual([])
  })

  it('is not the entry point of the shipped shell', () => {
    // index.html is what `vite build` roots the bundle at. If a preview entry were
    // ever left in here, the mock would ship even with src/ clean.
    const html = readFileSync(resolve(WEB, 'index.html'), 'utf8')
    expect(html).toContain('/src/main.tsx')
    expect(html).not.toContain('preview')
    expect(html).not.toContain('mock')
  })

  it('keeps the production build config free of the mock', () => {
    // `npm run build` must use vite.config.ts. A mock plugin added there would put
    // fixtures behind a dev-only-looking flag that still ships.
    const config = readFileSync(resolve(WEB, 'vite.config.ts'), 'utf8')
    expect(config).not.toContain('mock')
  })

  it('still declares the fixtures the mock config depends on', () => {
    // The converse guard: if `mock/` is deleted but `preview:mock` survives in
    // package.json, the harness breaks with a confusing resolver error instead of
    // saying so. Cheap to pin, and it keeps the README honest.
    const pkg = JSON.parse(readFileSync(resolve(WEB, 'package.json'), 'utf8'))
    if (pkg.scripts['preview:mock']) {
      const fixtures = readFileSync(resolve(WEB, 'mock/fixtures.ts'), 'utf8')
      expect(fixtures).toContain('export function cubeList')
    }
  })
})

describe('the mock harness is internally consistent', () => {
  // `tsconfig.json` includes only `src`, so `vite.mock.config.ts` and `mock/` are
  // NOT typechecked — neither `tsc --noEmit` nor `npm run build` sees them. A
  // dangling `fx.something()` therefore survives every gate and only surfaces as a
  // 500 when someone opens that page in the preview. It happened while adding the
  // "last changed" endpoint: the config was wired to `fx.cubeChanges` a step before
  // the fixture existed, and nothing complained.
  it('calls only fixtures that actually exist', () => {
    const config = readFileSync(resolve(WEB, 'vite.mock.config.ts'), 'utf8')
    const fixtures = readFileSync(resolve(WEB, 'mock/fixtures.ts'), 'utf8')

    const called = [...config.matchAll(/\bfx\.([A-Za-z0-9_]+)/g)].map(m => m[1])
    expect(called.length).toBeGreaterThan(0)

    const exported = new Set(
      [...fixtures.matchAll(/export\s+(?:function|const)\s+([A-Za-z0-9_]+)/g)]
        .map(m => m[1]),
    )
    const missing = [...new Set(called)].filter(n => n && !exported.has(n))
    expect(missing).toEqual([])
  })
})

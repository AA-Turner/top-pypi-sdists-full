import { describe, it, expect } from 'vitest'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

/** The stylesheet's structure, checked because a malformed one FAILS SILENTLY.
 *
 *  A union-merge resolution once dropped the closing brace of `.util-skeleton-chart`.
 *  Everything appended after it was swallowed into that rule, and because CSS nesting
 *  is valid syntax the build succeeded, every unit test passed, and the deploy went
 *  green — while `.field-wide` compiled to `.util-skeleton-chart .field-wide` and could
 *  never match anything. The only symptom was a layout that silently did not change.
 *
 *  Nothing else catches this: vitest does not apply CSS, jsdom does not do layout, and
 *  `vite build` is happy to compile nested rules. */
describe('styles.css structure', () => {
  const css = readFileSync(join(__dirname, 'styles.css'), 'utf8')
  // Comments can contain braces in prose; strip them before counting.
  const bare = css.replace(/\/\*[\s\S]*?\*\//g, '')

  it('has balanced braces', () => {
    const open = (bare.match(/\{/g) ?? []).length
    const close = (bare.match(/\}/g) ?? []).length
    expect(close).toBe(open)
  })

  it('never leaves a rule open, so no selector is accidentally nested', () => {
    // A `{` is legal inside another block ONLY when the outer one is an at-rule
    // (@media / @supports), which this file does use. Anything else means a rule
    // was left open and the following selectors became descendants of it.
    const stack: ('at' | 'rule')[] = []
    const offenders: string[] = []
    let line = 1
    let selector = ''
    for (const ch of bare) {
      if (ch === '\n') { line++; selector += ' '; continue }
      if (ch === '{') {
        const isAt = selector.trim().startsWith('@')
        if (stack.some(k => k === 'rule')) {
          offenders.push(`line ${line}: ${selector.trim().slice(0, 60)}`)
        }
        stack.push(isAt ? 'at' : 'rule')
        selector = ''
      } else if (ch === '}') {
        stack.pop()
        selector = ''
      } else {
        selector += ch
      }
    }
    expect(offenders, `rule(s) opened inside a non-at-rule block:\n${offenders.join('\n')}`)
      .toEqual([])
    expect(stack.length, 'a block was never closed').toBe(0)
  })

  it('keeps the expose-modal field rules at the top level', () => {
    // Named explicitly because these are the ones the bug actually disabled, and
    // they are invisible to every other test in this suite.
    for (const sel of ['label.overline', '.field-wide', '.rewrite-toggle']) {
      const re = new RegExp(`(^|\\})\\s*${sel.replace('.', '\\.')}\\s*\\{`, 'm')
      expect(bare, `${sel} is not a top-level rule`).toMatch(re)
    }
  })
})

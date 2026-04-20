/**
 * JS unit tests for the chat.js auto-propose banner (#1454).
 *
 * Follows the inline-copy pattern of chat_attribution.test.js: loading
 * the full chat.js IIFE into jsdom is heavy because of the globals it
 * expects, so the renderer under test is re-declared here and must stay
 * behaviourally in sync with ``_addAutoProposeBanner`` in
 * src/anteroom/static/js/chat.js.
 *
 * The core guarantees pinned by these tests:
 *   1. The banner renders nothing on empty / missing input.
 *   2. Every LLM-extracted string flows through textContent — never
 *      innerHTML — so a hostile preview can never execute as script.
 *   3. The Review button is wired and triggers MemoryPanel.openPanel()
 *      + _switchTab('review') when the panel is loaded.
 *   4. When MemoryPanel is absent (embedded views) the click is a no-op
 *      and does not throw.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';

function _addAutoProposeBanner(msgEl, items) {
    if (!msgEl || !Array.isArray(items) || items.length === 0) return;

    const banner = document.createElement('div');
    banner.className = 'memory-auto-propose-banner';

    const icon = document.createElement('span');
    icon.className = 'memory-auto-propose-icon';
    icon.textContent = '\uD83D\uDCA1';
    banner.appendChild(icon);

    const text = document.createElement('span');
    text.className = 'memory-auto-propose-text';
    const count = items.length;
    const noun = count === 1 ? 'memory' : 'memories';
    text.textContent = ` ${count} ${noun} queued for review`;
    banner.appendChild(text);

    const reviewBtn = document.createElement('button');
    reviewBtn.type = 'button';
    reviewBtn.className = 'memory-auto-propose-review';
    reviewBtn.textContent = 'Review';
    reviewBtn.addEventListener('click', () => {
        if (typeof MemoryPanel === 'undefined' || !MemoryPanel) return;
        try {
            MemoryPanel.openPanel();
            if (typeof MemoryPanel._switchTab === 'function') {
                MemoryPanel._switchTab('review');
            }
        } catch (_e) {
            // No-op
        }
    });
    banner.appendChild(reviewBtn);

    msgEl.appendChild(banner);
}

describe('_addAutoProposeBanner', () => {
    let msgEl;

    beforeEach(() => {
        document.body.innerHTML = '';
        msgEl = document.createElement('div');
        document.body.appendChild(msgEl);
        delete globalThis.MemoryPanel;
    });

    it('does nothing when items is empty', () => {
        _addAutoProposeBanner(msgEl, []);
        expect(msgEl.children.length).toBe(0);
    });

    it('does nothing when items is null', () => {
        _addAutoProposeBanner(msgEl, null);
        expect(msgEl.children.length).toBe(0);
    });

    it('does nothing when msgEl is null', () => {
        // Should not throw — the function bails out early.
        expect(() => _addAutoProposeBanner(null, [{ fqn: '@user/memory/x' }])).not.toThrow();
    });

    it('renders a single-item banner with singular noun', () => {
        _addAutoProposeBanner(msgEl, [
            { fqn: '@user/memory/pref-x', category: 'preference', content_preview: 'X.' },
        ]);
        const banner = msgEl.querySelector('.memory-auto-propose-banner');
        expect(banner).not.toBeNull();
        expect(banner.textContent).toContain('1 memory queued for review');
        expect(banner.textContent).not.toContain('memories');
    });

    it('renders a multi-item banner with plural noun', () => {
        _addAutoProposeBanner(msgEl, [
            { fqn: '@user/memory/x', category: 'preference', content_preview: 'X.' },
            { fqn: '@user/memory/y', category: 'decision', content_preview: 'Y.' },
            { fqn: '@user/memory/z', category: 'workflow_hint', content_preview: 'Z.' },
        ]);
        const banner = msgEl.querySelector('.memory-auto-propose-banner');
        expect(banner.textContent).toContain('3 memories queued for review');
    });

    it('exposes a Review button', () => {
        _addAutoProposeBanner(msgEl, [
            { fqn: '@user/memory/pref-x', category: 'preference', content_preview: 'X.' },
        ]);
        const btn = msgEl.querySelector('.memory-auto-propose-review');
        expect(btn).not.toBeNull();
        expect(btn.tagName).toBe('BUTTON');
        expect(btn.textContent).toBe('Review');
    });

    it('Review button opens MemoryPanel and switches to the review tab', () => {
        const openPanel = vi.fn();
        const switchTab = vi.fn();
        globalThis.MemoryPanel = { openPanel, _switchTab: switchTab };

        _addAutoProposeBanner(msgEl, [
            { fqn: '@user/memory/x', category: 'preference', content_preview: 'X.' },
        ]);
        msgEl.querySelector('.memory-auto-propose-review').click();
        expect(openPanel).toHaveBeenCalledTimes(1);
        expect(switchTab).toHaveBeenCalledWith('review');
    });

    it('Review button is a no-op when MemoryPanel is absent', () => {
        _addAutoProposeBanner(msgEl, [
            { fqn: '@user/memory/x', category: 'preference', content_preview: 'X.' },
        ]);
        expect(() => msgEl.querySelector('.memory-auto-propose-review').click()).not.toThrow();
    });

    it('hostile content_preview does not execute as script (XSS negative)', () => {
        const sentinel = vi.fn();
        globalThis._xssSentinel = sentinel;
        _addAutoProposeBanner(msgEl, [
            {
                fqn: '@user/memory/x',
                category: 'preference',
                content_preview: '<img src=x onerror="window._xssSentinel()">',
            },
        ]);
        // The preview text isn't even shown on the banner today, but the
        // banner should never grow an <img> tag from any future field
        // either — verify by walking the banner DOM.
        const banner = msgEl.querySelector('.memory-auto-propose-banner');
        expect(banner.querySelector('img')).toBeNull();
        // Sanity: sentinel never called.
        expect(sentinel).not.toHaveBeenCalled();
        delete globalThis._xssSentinel;
    });
});

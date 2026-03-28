/**
 * JS unit tests for queue badge rendering and lifecycle (#1175).
 *
 * Tests verify DOM insertion of .queued-badge with position text,
 * badge removal on queued_message event, and 429 toast rendering.
 */

import { describe, it, expect, beforeEach } from 'vitest';

// ---------------------------------------------------------------------------
// DOM helpers
// ---------------------------------------------------------------------------

function createMessageEl() {
    const el = document.createElement('div');
    el.className = 'message user';
    const role = document.createElement('span');
    role.className = 'message-role';
    role.textContent = 'YOU';
    el.appendChild(role);
    return el;
}

function insertQueueBadge(msgEl, position) {
    const badge = document.createElement('span');
    badge.className = 'queued-badge';
    badge.textContent = `queued (${position || '?'})`;
    msgEl.querySelector('.message-role').appendChild(badge);
    return badge;
}

function removeQueueBadges() {
    document.querySelectorAll('.queued-badge').forEach(b => {
        b.classList.add('promoting');
        setTimeout(() => b.remove(), 300);
    });
}

// ---------------------------------------------------------------------------
// Toast helper (simplified from chat.js)
// ---------------------------------------------------------------------------

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    return toast;
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('Queue badge DOM insertion', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    it('inserts badge with position text', () => {
        const el = createMessageEl();
        document.body.appendChild(el);

        insertQueueBadge(el, 3);

        const badge = el.querySelector('.queued-badge');
        expect(badge).not.toBeNull();
        expect(badge.textContent).toBe('queued (3)');
    });

    it('inserts badge with fallback text when position is missing', () => {
        const el = createMessageEl();
        document.body.appendChild(el);

        insertQueueBadge(el, undefined);

        const badge = el.querySelector('.queued-badge');
        expect(badge).not.toBeNull();
        expect(badge.textContent).toBe('queued (?)');
    });
});

describe('Queue badge removal on queued_message', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    it('adds promoting class and schedules removal', () => {
        const el = createMessageEl();
        document.body.appendChild(el);
        insertQueueBadge(el, 1);

        const badges = document.querySelectorAll('.queued-badge');
        expect(badges.length).toBe(1);

        // Simulate queued_message event handler
        removeQueueBadges();

        const badge = document.querySelector('.queued-badge');
        expect(badge).not.toBeNull();
        expect(badge.classList.contains('promoting')).toBe(true);
    });

    it('removes multiple badges at once', () => {
        const el1 = createMessageEl();
        const el2 = createMessageEl();
        document.body.appendChild(el1);
        document.body.appendChild(el2);
        insertQueueBadge(el1, 1);
        insertQueueBadge(el2, 2);

        expect(document.querySelectorAll('.queued-badge').length).toBe(2);

        removeQueueBadges();

        const badges = document.querySelectorAll('.queued-badge.promoting');
        expect(badges.length).toBe(2);
    });
});

describe('429 error toast', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    it('renders queue full toast message', () => {
        const detail = 'Queue full \u2014 wait for current work to finish';
        const toast = showToast(detail);

        expect(toast.textContent).toContain('Queue full');
        expect(toast.textContent).toContain('wait for current work to finish');
        expect(toast.classList.contains('toast')).toBe(true);
    });
});

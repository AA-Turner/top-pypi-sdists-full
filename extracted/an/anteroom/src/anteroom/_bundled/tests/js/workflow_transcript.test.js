/**
 * JS unit tests for workflow transcript panel logic (#1101).
 *
 * Since workflows.js is an IIFE, we reproduce key transcript logic
 * functions inline for testing (same pattern as workflows.test.js).
 */

import { describe, it, expect, beforeEach } from 'vitest';

// ---------------------------------------------------------------------------
// Reproduce _escapeHtml from workflows.js
// ---------------------------------------------------------------------------
function _escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ---------------------------------------------------------------------------
// Reproduce transcript rendering logic from workflows.js
// ---------------------------------------------------------------------------
const _MAX_TRANSCRIPT_LINES = 200;

function _appendTranscriptLine(container, stream, line, ts) {
    const div = document.createElement('div');
    div.className = `wf-line wf-${_escapeHtml(stream)}`;
    const tsShort = (ts || '').substring(11, 19);
    div.innerHTML = `<span class="wf-ts">${_escapeHtml(tsShort)}</span> <span class="wf-content">${_escapeHtml(line)}</span>`;
    container.appendChild(div);

    while (container.children.length > _MAX_TRANSCRIPT_LINES) {
        container.removeChild(container.firstChild);
    }
}

function _appendTranscriptSeparator(container, text) {
    const div = document.createElement('div');
    div.className = 'wf-separator';
    div.textContent = text;
    container.appendChild(div);
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('Transcript _escapeHtml', () => {
    it('escapes HTML entities in transcript content', () => {
        expect(_escapeHtml('<script>alert("xss")</script>')).not.toContain('<script>');
        expect(_escapeHtml('&')).toBe('&amp;');
    });

    it('preserves plain text', () => {
        expect(_escapeHtml('Hello from workflow')).toBe('Hello from workflow');
    });
});

describe('Transcript _appendTranscriptLine', () => {
    let container;

    beforeEach(() => {
        container = document.createElement('div');
    });

    it('appends a stdout line with correct class', () => {
        _appendTranscriptLine(container, 'stdout', 'hello', '2026-03-22T10:44:26');
        expect(container.children.length).toBe(1);
        expect(container.firstChild.classList.contains('wf-stdout')).toBe(true);
        expect(container.firstChild.textContent).toContain('hello');
    });

    it('appends a stderr line with correct class', () => {
        _appendTranscriptLine(container, 'stderr', 'error msg', '2026-03-22T10:44:26');
        expect(container.firstChild.classList.contains('wf-stderr')).toBe(true);
    });

    it('extracts HH:MM:SS from ISO timestamp', () => {
        _appendTranscriptLine(container, 'stdout', 'test', '2026-03-22T10:44:26');
        const ts = container.querySelector('.wf-ts');
        expect(ts.textContent).toBe('10:44:26');
    });

    it('handles empty timestamp gracefully', () => {
        _appendTranscriptLine(container, 'stdout', 'test', '');
        const ts = container.querySelector('.wf-ts');
        expect(ts.textContent).toBe('');
    });

    it('escapes HTML in line content', () => {
        _appendTranscriptLine(container, 'stdout', '<img onerror=alert(1)>', '2026-03-22T10:44:26');
        const content = container.querySelector('.wf-content');
        expect(content.innerHTML).not.toContain('<img');
        expect(content.textContent).toContain('<img');
    });

    it('escapes HTML in stream name', () => {
        _appendTranscriptLine(container, 'stdout"><script>', 'test', '2026-03-22T10:44:26');
        expect(container.innerHTML).not.toContain('<script>');
    });

    it('caps at MAX_TRANSCRIPT_LINES', () => {
        for (let i = 0; i < 210; i++) {
            _appendTranscriptLine(container, 'stdout', `line ${i}`, '2026-03-22T10:00:00');
        }
        expect(container.children.length).toBe(_MAX_TRANSCRIPT_LINES);
        // First line should be line 10 (0-9 were removed)
        expect(container.firstChild.textContent).toContain('line 10');
    });
});

describe('Transcript _appendTranscriptSeparator', () => {
    it('adds a separator div', () => {
        const container = document.createElement('div');
        _appendTranscriptSeparator(container, 'step_1 started');
        expect(container.children.length).toBe(1);
        expect(container.firstChild.classList.contains('wf-separator')).toBe(true);
        expect(container.firstChild.textContent).toBe('step_1 started');
    });
});

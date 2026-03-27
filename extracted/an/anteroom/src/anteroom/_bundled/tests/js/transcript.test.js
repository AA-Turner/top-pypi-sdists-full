/**
 * JS unit tests for workflow transcript rendering (#1112).
 *
 * Reproduces _renderTranscriptEntry from workflows.js inline for testing,
 * matching the exact implementation (same pattern as workflows.test.js).
 *
 * The function below is a verbatim copy of the IIFE-private function
 * in src/anteroom/static/js/workflows.js lines 243-273. If the
 * implementation changes, update this copy to match.
 */

import { describe, it, expect } from 'vitest';

// ---------------------------------------------------------------------------
// Reproduce _escapeHtml from workflows.js (verbatim)
// ---------------------------------------------------------------------------
function _escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ---------------------------------------------------------------------------
// Reproduce _renderTranscriptEntry from workflows.js (verbatim)
// DOMPurify is not available in vitest/jsdom, so the fallback path is tested.
// ---------------------------------------------------------------------------
function _renderTranscriptEntry(event) {
    const payload = event.payload || {};
    const etype = event.event_type || '';

    if (etype === 'transcript_assistant') {
        const content = typeof DOMPurify !== 'undefined' ? DOMPurify.sanitize(payload.content || '') : _escapeHtml(payload.content || '');
        return '<div class="message assistant wf-transcript-entry"><div class="message-content">' + content + '</div></div>';
    }
    if (etype === 'transcript_tool_call') {
        const name = _escapeHtml(payload.tool_name || '');
        const args = _escapeHtml(typeof payload.arguments === 'string' ? payload.arguments : JSON.stringify(payload.arguments || {}));
        return '<div class="message tool-call wf-transcript-entry"><div class="tool-name">' + name + '</div><pre class="tool-args">' + args + '</pre></div>';
    }
    if (etype === 'transcript_tool_result') {
        const name = _escapeHtml(payload.tool_name || '');
        const output = _escapeHtml(payload.output || '');
        const status = _escapeHtml(payload.status || '');
        return '<div class="message tool-result wf-transcript-entry"><div class="tool-name">' + name + ' &mdash; ' + status + '</div><pre class="tool-output">' + output + '</pre></div>';
    }
    if (etype === 'transcript_stdout') {
        return '<div class="wf-transcript-stdout"><pre>' + _escapeHtml(payload.content || '') + '</pre></div>';
    }
    if (etype === 'transcript_stderr') {
        return '<div class="wf-transcript-stderr"><pre>' + _escapeHtml(payload.content || '') + '</pre></div>';
    }
    if (etype === 'transcript_usage') {
        const tokens = (payload.total_tokens || 0).toLocaleString();
        return '<div class="wf-transcript-usage">' + tokens + ' tokens</div>';
    }
    return '';
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('_renderTranscriptEntry (verbatim copy from workflows.js)', () => {
    it('renders assistant with wf-transcript-entry class and content', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_assistant',
            payload: { content: 'Hello world' },
        });
        expect(html).toContain('wf-transcript-entry');
        expect(html).toContain('class="message assistant');
        expect(html).toContain('Hello world');
    });

    it('escapes XSS in assistant content via _escapeHtml fallback', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_assistant',
            payload: { content: '<script>alert("xss")</script>' },
        });
        expect(html).toContain('&lt;script&gt;');
        expect(html).not.toContain('<script>alert');
    });

    it('renders tool call with tool-name and tool-args', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_tool_call',
            payload: { tool_name: 'bash', arguments: '{"command": "ls"}' },
        });
        expect(html).toContain('wf-transcript-entry');
        expect(html).toContain('class="message tool-call');
        expect(html).toContain('bash');
        expect(html).toContain('class="tool-args"');
    });

    it('renders tool result with status and output', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_tool_result',
            payload: { tool_name: 'bash', status: 'success', output: 'file.py' },
        });
        expect(html).toContain('wf-transcript-entry');
        expect(html).toContain('class="message tool-result');
        expect(html).toContain('bash');
        expect(html).toContain('success');
        expect(html).toContain('file.py');
    });

    it('renders stdout with wf-transcript-stdout class', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_stdout',
            payload: { content: '5 passed in 0.8s' },
        });
        expect(html).toContain('wf-transcript-stdout');
        expect(html).toContain('5 passed in 0.8s');
    });

    it('renders stderr with wf-transcript-stderr class', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_stderr',
            payload: { content: 'error: module not found' },
        });
        expect(html).toContain('wf-transcript-stderr');
        expect(html).toContain('error: module not found');
    });

    it('renders usage with formatted token count', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_usage',
            payload: { total_tokens: 12450 },
        });
        expect(html).toContain('wf-transcript-usage');
        expect(html).toContain('12,450');
        expect(html).toContain('tokens');
    });

    it('returns empty string for unknown event type', () => {
        expect(_renderTranscriptEntry({ event_type: 'unknown', payload: {} })).toBe('');
    });

    it('handles missing payload gracefully', () => {
        const html = _renderTranscriptEntry({ event_type: 'transcript_assistant' });
        expect(html).toContain('wf-transcript-entry');
    });

    it('escapes XSS in tool call arguments', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_tool_call',
            payload: { tool_name: 'bash', arguments: '<img onerror=alert(1)>' },
        });
        expect(html).toContain('&lt;img');
        expect(html).not.toContain('<img onerror');
    });

    it('escapes XSS in tool result output', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_tool_result',
            payload: { tool_name: 'bash', status: 'ok', output: '<script>bad</script>' },
        });
        expect(html).toContain('&lt;script&gt;');
        expect(html).not.toContain('<script>bad');
    });

    it('handles object arguments by JSON.stringifying', () => {
        const html = _renderTranscriptEntry({
            event_type: 'transcript_tool_call',
            payload: { tool_name: 'write_file', arguments: { path: 'test.py', content: 'print("hi")' } },
        });
        expect(html).toContain('test.py');
    });
});

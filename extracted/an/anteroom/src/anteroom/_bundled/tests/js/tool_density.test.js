/**
 * JS unit tests for #1467 tool-result density rendering in chat.js.
 *
 * Direct load of chat.js is impractical (2600+ lines, heavy DOM globals), so
 * these tests inline-copy the density helper logic and assert on its DOM
 * behaviour. Mirrors the chat_save_memory.test.js / chat_attribution.test.js
 * convention: the inline copy must stay in sync with the source.
 *
 * Zero-config contract (HARD GATE): when summary fields are absent/null,
 * the helper is a no-op and the legacy raw-JSON DOM is unchanged.
 */

import { describe, it, expect, beforeEach } from 'vitest';

// ----- inline copy of density helpers from chat.js -----

let _toolRepeatRun = null;

function _toolRepeatReset() {
    _toolRepeatRun = null;
}

function _applyErrorClass(details, errorClass) {
    if (!errorClass) return;
    const allowed = new Set(['exit_nonzero', 'exception', 'timeout', 'denied']);
    if (!allowed.has(errorClass)) return;
    details.classList.add(`tool-error-${errorClass}`);
    details.setAttribute('aria-label', `Tool call failed: ${errorClass}`);
}

function _renderDiffHunks(container, previewText) {
    const lines = previewText.split('\n');
    const hunk = document.createElement('div');
    hunk.className = 'tool-diff-hunk';
    lines.forEach(line => {
        const lineDiv = document.createElement('div');
        if (line.startsWith('@@ ')) {
            lineDiv.className = 'tool-diff-hunk-header';
        } else if (line.startsWith('+') && !line.startsWith('+++')) {
            lineDiv.className = 'tool-diff-add';
        } else if (line.startsWith('-') && !line.startsWith('---')) {
            lineDiv.className = 'tool-diff-del';
        } else {
            lineDiv.className = 'tool-diff-context';
        }
        lineDiv.textContent = line;
        hunk.appendChild(lineDiv);
    });
    container.appendChild(hunk);
}

function _applyToolDensityEnhancements(details, data) {
    if (!details) return;
    const hasSummary = data && (data.summary || data.output_preview);
    const hasErrorClass = data && data.error_class;
    const hasShapeHash = data && data.output_shape_hash;

    _applyErrorClass(details, data && data.error_class);

    if (!hasSummary && !hasErrorClass && !hasShapeHash) {
        return;
    }

    const toolContent = details.querySelector('.tool-content');
    if (!toolContent) return;

    if (hasSummary) {
        const previewText = String(data.summary || data.output_preview || '');
        const summaryBody = document.createElement('div');
        summaryBody.className = 'tool-summary-body';

        if (previewText.startsWith('@@ ')) {
            _renderDiffHunks(summaryBody, previewText);
        } else {
            const pre = document.createElement('pre');
            pre.className = 'tool-summary-text';
            pre.textContent = previewText;
            summaryBody.appendChild(pre);
        }

        const rawDetails = document.createElement('details');
        rawDetails.className = 'tool-raw-output';
        const rawSummary = document.createElement('summary');
        rawSummary.textContent = 'Show raw output';
        rawDetails.appendChild(rawSummary);

        const children = Array.from(toolContent.childNodes);
        let outputLabelIdx = -1;
        for (let i = 0; i < children.length; i++) {
            const n = children[i];
            if (n.tagName === 'STRONG' && n.textContent && n.textContent.startsWith('Output')) {
                outputLabelIdx = i;
                break;
            }
        }
        if (outputLabelIdx >= 0) {
            for (let i = outputLabelIdx; i < children.length; i++) {
                rawDetails.appendChild(children[i]);
            }
        }

        toolContent.appendChild(summaryBody);
        toolContent.appendChild(rawDetails);
    }

    if (!hasShapeHash) {
        _toolRepeatReset();
        return;
    }

    const hash = String(data.output_shape_hash);
    const toolName = data.tool_name || 'tool';
    if (!_toolRepeatRun || _toolRepeatRun.hash !== hash) {
        _toolRepeatRun = {
            hash,
            count: 1,
            elements: [details],
            collapsedRow: null,
            toolName,
        };
        return;
    }

    _toolRepeatRun.count += 1;
    _toolRepeatRun.elements.push(details);
    _toolRepeatRun.toolName = toolName;

    if (_toolRepeatRun.collapsedRow) {
        const label = _toolRepeatRun.collapsedRow.querySelector('.tool-repeat-label');
        if (label) label.textContent = `${toolName} \u00d7 ${_toolRepeatRun.count}`;
        if (details.parentNode) details.parentNode.removeChild(details);
        return;
    }

    if (_toolRepeatRun.count >= 3) {
        _collapseRepeats(_toolRepeatRun);
    }
}

function _collapseRepeats(entry) {
    if (!entry || !entry.elements || entry.elements.length < 3) return;
    const firstEl = entry.elements[0];
    if (!firstEl || !firstEl.parentNode) return;

    const parent = firstEl.parentNode;
    const row = document.createElement('div');
    row.className = 'tool-call tool-repeat-collapsed';
    const label = document.createElement('span');
    label.className = 'tool-repeat-label';
    label.textContent = `${entry.toolName || 'tool'} \u00d7 ${entry.count}`;
    row.appendChild(label);
    parent.insertBefore(row, firstEl);
    entry.collapsedRow = row;

    entry.elements.forEach(el => {
        if (el && el.parentNode) el.parentNode.removeChild(el);
    });
}

// ----- helpers -----

function buildLegacyToolCall(status = 'success', output = { exit_code: 0 }) {
    // Mirror the legacy renderToolCallEnd DOM shape — outer details + summary
    // + .tool-content with <strong>Input</strong><pre> and <strong>Output</strong><pre>.
    const details = document.createElement('details');
    details.className = `tool-call tool-status-${status === 'success' ? 'success' : 'error'}`;
    const summary = document.createElement('summary');
    summary.textContent = `Tool: bash (${status})`;
    details.appendChild(summary);
    const toolContent = document.createElement('div');
    toolContent.className = 'tool-content';

    const inputLabel = document.createElement('strong');
    inputLabel.textContent = 'Input:';
    toolContent.appendChild(inputLabel);
    const inputPre = document.createElement('pre');
    inputPre.textContent = '{"cmd":"ls"}';
    toolContent.appendChild(inputPre);

    const outputLabel = document.createElement('strong');
    outputLabel.textContent = `Output (${status}):`;
    toolContent.appendChild(outputLabel);
    const outputPre = document.createElement('pre');
    outputPre.textContent = JSON.stringify(output, null, 2);
    toolContent.appendChild(outputPre);

    details.appendChild(toolContent);
    return details;
}

// ----- tests -----

describe('#1467 density fallback (normal mode)', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('no summary fields → DOM unchanged (zero-config contract)', () => {
        const details = buildLegacyToolCall('success');
        const before = details.outerHTML;
        _applyToolDensityEnhancements(details, {
            summary: null,
            output_preview: null,
            error_class: null,
            output_shape_hash: null,
            tool_name: 'bash',
        });
        const after = details.outerHTML;
        expect(after).toBe(before);
    });

    it('no tool-error-* class applied when error_class is null', () => {
        const details = buildLegacyToolCall('error', { exit_code: 1 });
        _applyToolDensityEnhancements(details, { error_class: null });
        const classes = Array.from(details.classList);
        expect(classes.some(c => c.startsWith('tool-error-'))).toBe(false);
    });

    it('missing data object → no-op', () => {
        const details = buildLegacyToolCall('success');
        const before = details.outerHTML;
        _applyToolDensityEnhancements(details, null);
        expect(details.outerHTML).toBe(before);
    });
});

describe('#1467 compact mode rendering', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('renders summary body and wraps raw output in nested details', () => {
        const details = buildLegacyToolCall('success');
        _applyToolDensityEnhancements(details, {
            summary: 'ran 2 lines',
            output_preview: 'ran 2 lines',
            error_class: null,
            output_shape_hash: 'abc123',
            tool_name: 'bash',
        });

        const summaryBody = details.querySelector('.tool-summary-body');
        expect(summaryBody).not.toBeNull();
        expect(summaryBody.textContent).toContain('ran 2 lines');

        const rawDetails = details.querySelector('details.tool-raw-output');
        expect(rawDetails).not.toBeNull();
        expect(rawDetails.querySelector('summary').textContent).toBe('Show raw output');
        // Raw output pre must be reachable inside the nested details.
        expect(rawDetails.textContent).toContain('Output (success)');
    });

    it('uses textContent (XSS-safe) for summary', () => {
        const details = buildLegacyToolCall('success');
        _applyToolDensityEnhancements(details, {
            summary: '<script>alert(1)</script>',
            output_preview: '<script>alert(1)</script>',
            output_shape_hash: 'h',
            tool_name: 'bash',
        });
        const summaryText = details.querySelector('.tool-summary-body .tool-summary-text');
        expect(summaryText).not.toBeNull();
        // If innerHTML were used, a <script> tag would exist in the DOM.
        expect(details.querySelectorAll('script').length).toBe(0);
        // The literal text IS in the summary body — just as text.
        expect(summaryText.textContent).toBe('<script>alert(1)</script>');
    });
});

describe('#1467 minimal mode rendering (output_preview fallback)', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('renders output_preview when summary is null', () => {
        const details = buildLegacyToolCall('success');
        _applyToolDensityEnhancements(details, {
            summary: null,
            output_preview: 'abbreviated output',
            output_shape_hash: 'abc',
            tool_name: 'bash',
        });
        const summaryBody = details.querySelector('.tool-summary-body');
        expect(summaryBody).not.toBeNull();
        expect(summaryBody.textContent).toContain('abbreviated output');
    });
});

describe('#1467 error-class CSS application', () => {
    beforeEach(() => { _toolRepeatReset(); });

    for (const cls of ['exit_nonzero', 'exception', 'timeout', 'denied']) {
        it(`applies tool-error-${cls} and aria-label`, () => {
            const details = buildLegacyToolCall('error');
            _applyToolDensityEnhancements(details, {
                summary: 'boom',
                output_preview: 'boom',
                error_class: cls,
                output_shape_hash: 'h',
                tool_name: 'bash',
            });
            expect(details.classList.contains(`tool-error-${cls}`)).toBe(true);
            expect(details.getAttribute('aria-label')).toBe(`Tool call failed: ${cls}`);
        });
    }

    it('rejects unknown error_class values', () => {
        const details = buildLegacyToolCall('error');
        _applyToolDensityEnhancements(details, {
            error_class: '<img onerror=1>',
            tool_name: 'bash',
        });
        // Unknown value → no CSS class applied (allowlist gate).
        expect(
            Array.from(details.classList).some(c => c.startsWith('tool-error-'))
        ).toBe(false);
    });
});

describe('#1467 preview truncation boundary', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('DOM text length matches server-provided preview length (no JS double-truncation)', () => {
        const preview = 'x'.repeat(10000);  // tool_output_max_chars default
        const details = buildLegacyToolCall('success');
        _applyToolDensityEnhancements(details, {
            summary: preview,
            output_preview: preview,
            output_shape_hash: 'h',
            tool_name: 'bash',
        });
        const body = details.querySelector('.tool-summary-body .tool-summary-text');
        expect(body.textContent.length).toBe(10000);
    });
});

describe('#1467 diff-hunk rendering', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('parses unified diff into line-typed divs', () => {
        const diff = '@@ -1,3 +1,3 @@\n context\n-old line\n+new line\n more context';
        const details = buildLegacyToolCall('success');
        _applyToolDensityEnhancements(details, {
            summary: diff,
            output_preview: diff,
            output_shape_hash: 'h',
            tool_name: 'edit_file',
        });
        const hunk = details.querySelector('.tool-diff-hunk');
        expect(hunk).not.toBeNull();
        expect(hunk.querySelector('.tool-diff-hunk-header').textContent).toBe('@@ -1,3 +1,3 @@');
        expect(hunk.querySelector('.tool-diff-del').textContent).toBe('-old line');
        expect(hunk.querySelector('.tool-diff-add').textContent).toBe('+new line');
        const contexts = hunk.querySelectorAll('.tool-diff-context');
        expect(contexts.length).toBeGreaterThanOrEqual(2);
    });

    it('does not classify +++ / --- markers as add/del lines', () => {
        const diff = '@@ -0,0 +0,0 @@\n+++ b/new\n--- a/old';
        const details = buildLegacyToolCall('success');
        _applyToolDensityEnhancements(details, {
            summary: diff,
            output_preview: diff,
            output_shape_hash: 'h',
            tool_name: 'edit_file',
        });
        const hunk = details.querySelector('.tool-diff-hunk');
        // +++ and --- are classified as context, not add/del
        expect(hunk.querySelectorAll('.tool-diff-add').length).toBe(0);
        expect(hunk.querySelectorAll('.tool-diff-del').length).toBe(0);
    });
});

describe('#1467 repeat-collapse', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('collapses 3 identical shape hashes into one row', () => {
        const parent = document.createElement('div');
        document.body.appendChild(parent);

        for (let i = 0; i < 3; i++) {
            const d = buildLegacyToolCall('success');
            parent.appendChild(d);
            _applyToolDensityEnhancements(d, {
                summary: 'ok',
                output_preview: 'ok',
                error_class: null,
                output_shape_hash: 'samehash',
                tool_name: 'bash',
            });
        }

        const collapsed = parent.querySelectorAll('.tool-repeat-collapsed');
        expect(collapsed.length).toBe(1);
        expect(collapsed[0].querySelector('.tool-repeat-label').textContent).toBe('bash \u00d7 3');
        // The original .tool-call elements have been removed.
        const remainingOriginals = parent.querySelectorAll('.tool-call:not(.tool-repeat-collapsed)');
        expect(remainingOriginals.length).toBe(0);

        document.body.removeChild(parent);
    });

    it('counter resets on turn boundary', () => {
        const parent = document.createElement('div');
        document.body.appendChild(parent);

        // First turn: 2 calls (not yet collapsed)
        for (let i = 0; i < 2; i++) {
            const d = buildLegacyToolCall('success');
            parent.appendChild(d);
            _applyToolDensityEnhancements(d, {
                output_preview: 'ok',
                output_shape_hash: 'h1',
                tool_name: 'bash',
            });
        }
        expect(parent.querySelectorAll('.tool-repeat-collapsed').length).toBe(0);

        // Reset (simulates turn_start / conversation load)
        _toolRepeatReset();

        // Second turn: 2 more calls same hash — should still not collapse
        // because the tracker was reset.
        for (let i = 0; i < 2; i++) {
            const d = buildLegacyToolCall('success');
            parent.appendChild(d);
            _applyToolDensityEnhancements(d, {
                output_preview: 'ok',
                output_shape_hash: 'h1',
                tool_name: 'bash',
            });
        }
        expect(parent.querySelectorAll('.tool-repeat-collapsed').length).toBe(0);

        document.body.removeChild(parent);
    });

    it('different shape hashes do not collapse together', () => {
        const parent = document.createElement('div');
        document.body.appendChild(parent);

        for (let i = 0; i < 3; i++) {
            const d = buildLegacyToolCall('success');
            parent.appendChild(d);
            _applyToolDensityEnhancements(d, {
                output_preview: 'ok',
                output_shape_hash: `hash${i}`,
                tool_name: 'bash',
            });
        }
        expect(parent.querySelectorAll('.tool-repeat-collapsed').length).toBe(0);

        document.body.removeChild(parent);
    });

    it('interleaved shapes break the run', () => {
        const parent = document.createElement('div');
        document.body.appendChild(parent);

        const hashes = ['samehash', 'otherhash', 'samehash', 'samehash'];
        for (const hash of hashes) {
            const d = buildLegacyToolCall('success');
            parent.appendChild(d);
            _applyToolDensityEnhancements(d, {
                output_preview: 'ok',
                output_shape_hash: hash,
                tool_name: 'bash',
            });
        }

        expect(parent.querySelectorAll('.tool-repeat-collapsed').length).toBe(0);
        expect(parent.querySelectorAll('.tool-call:not(.tool-repeat-collapsed)').length).toBe(4);

        document.body.removeChild(parent);
    });
});

describe('#1467 XSS negative tests', () => {
    beforeEach(() => { _toolRepeatReset(); });

    it('hostile summary/output_preview/tool_name/error_class never execute script', () => {
        const details = buildLegacyToolCall('error');
        _applyToolDensityEnhancements(details, {
            summary: '<script>alert(1)</script>',
            output_preview: '<img src=x onerror=alert(2)>',
            error_class: 'exception',
            output_shape_hash: '<script>bad</script>',
            tool_name: '<iframe src=evil></iframe>',
        });
        // No elements from injected markup ever appear.
        expect(details.querySelectorAll('script').length).toBe(0);
        expect(details.querySelectorAll('iframe').length).toBe(0);
        expect(details.querySelectorAll('img').length).toBe(0);
    });
});

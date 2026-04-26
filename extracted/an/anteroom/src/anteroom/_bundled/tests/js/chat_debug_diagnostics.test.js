import { beforeEach, describe, expect, it } from 'vitest';

let currentAssistantEl = null;

function scrollToBottom() {}

function renderDebugSummary(summary) {
    if (!currentAssistantEl || !summary || typeof summary !== 'object') return;
    const contentEl = currentAssistantEl.querySelector('.message-content');
    if (!contentEl) return;

    const details = document.createElement('details');
    details.className = 'debug-summary';

    const title = document.createElement('summary');
    const duration = Number.isFinite(summary.total_duration_seconds)
        ? `${summary.total_duration_seconds.toFixed(1)}s`
        : '';
    const stopReason = summary.stop_reason || 'unknown';
    title.textContent = duration ? `Debug diagnostics · ${duration} · ${stopReason}` : `Debug diagnostics · ${stopReason}`;
    details.appendChild(title);

    const body = document.createElement('div');
    body.className = 'debug-summary-body';

    const addRow = (label, value) => {
        if (value === undefined || value === null || value === '') return;
        const row = document.createElement('div');
        row.className = 'debug-summary-row';
        const key = document.createElement('span');
        key.className = 'debug-summary-key';
        key.textContent = label;
        const val = document.createElement('span');
        val.className = 'debug-summary-value';
        val.textContent = String(value);
        row.appendChild(key);
        row.appendChild(val);
        body.appendChild(row);
    };

    addRow('phase', summary.final_phase);
    if (summary.model) {
        addRow('model', [summary.model.provider, summary.model.name].filter(Boolean).join(' / '));
    }
    if (summary.usage && summary.usage.total_tokens !== undefined) {
        addRow('tokens', summary.usage.total_tokens);
    }
    if (summary.counters) {
        addRow('stream', `${summary.counters.tokens || 0} chunks, ${summary.counters.token_chars || 0} chars`);
    }

    const tools = Array.isArray(summary.tools) ? summary.tools.slice(0, 8) : [];
    if (tools.length > 0) {
        const list = document.createElement('ul');
        list.className = 'debug-summary-list';
        tools.forEach(tool => {
            const item = document.createElement('li');
            const durationText = Number.isFinite(tool.duration_seconds) ? ` · ${tool.duration_seconds.toFixed(2)}s` : '';
            item.textContent = `${tool.name || 'tool'} · ${tool.status || 'unknown'}${durationText}`;
            list.appendChild(item);
        });
        body.appendChild(list);
    }

    const events = Array.isArray(summary.runtime_events) ? summary.runtime_events.slice(0, 6) : [];
    if (events.length > 0) {
        addRow('events', events.map(e => e.kind).filter(Boolean).join(', '));
    }

    if (summary.redaction) {
        addRow('redaction', 'raw prompts, tokens, tool args, and tool output omitted');
    }

    details.appendChild(body);
    contentEl.appendChild(details);
    scrollToBottom();
}

beforeEach(() => {
    document.body.innerHTML = '<div class="message assistant"><div class="message-content"></div></div>';
    currentAssistantEl = document.querySelector('.message.assistant');
});

describe('chat debug diagnostics', () => {
    it('renders a compact debug summary block', () => {
        renderDebugSummary({
            total_duration_seconds: 3.25,
            stop_reason: 'completed',
            final_phase: 'streaming',
            model: {provider: 'openai', name: 'gpt-test'},
            usage: {total_tokens: 42},
            counters: {tokens: 4, token_chars: 120},
            tools: [{name: 'bash', status: 'success', duration_seconds: 0.42}],
            runtime_events: [{kind: 'queued_message'}],
            redaction: {raw_tool_output: 'omitted'},
        });

        const block = document.querySelector('.debug-summary');
        expect(block).not.toBeNull();
        expect(block.textContent).toContain('Debug diagnostics · 3.3s · completed');
        expect(block.textContent).toContain('openai / gpt-test');
        expect(block.textContent).toContain('bash · success · 0.42s');
        expect(block.textContent).toContain('raw prompts, tokens, tool args, and tool output omitted');
    });

    it('renders hostile values as text, not HTML', () => {
        const hostile = '<img src=x onerror="window.__DEBUG_XSS__=true">';
        renderDebugSummary({
            total_duration_seconds: 1,
            stop_reason: hostile,
            final_phase: hostile,
            model: {provider: hostile, name: 'gpt-test'},
            tools: [{name: hostile, status: 'error'}],
            redaction: {},
        });

        expect(document.body.textContent).toContain(hostile);
        expect(document.querySelectorAll('img').length).toBe(0);
        expect(globalThis.__DEBUG_XSS__).toBeUndefined();
    });
});

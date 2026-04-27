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

    addRow('request', summary.turn_id || summary.request_id);
    addRow('interface', summary.interface);
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
        list.className = 'debug-summary-list debug-summary-tools';
        tools.forEach(tool => {
            const item = document.createElement('li');
            const durationText = Number.isFinite(tool.duration_seconds) ? ` · ${tool.duration_seconds.toFixed(2)}s` : '';
            const timeoutText = Number.isFinite(tool.timeout_seconds) ? ` / ${tool.timeout_seconds.toFixed(0)}s timeout` : '';
            const argShape = tool.argument_shape && tool.argument_shape.type ? ` · args ${tool.argument_shape.type}` : '';
            const outShape = tool.output_shape && tool.output_shape.type ? ` · output ${tool.output_shape.type}` : '';
            const approval = tool.approval_decision ? ` · approval ${tool.approval_decision}` : '';
            const blocked = tool.hook_blocked ? ' · hook blocked' : '';
            item.textContent = `${tool.name || 'tool'} · ${tool.status || 'unknown'}${durationText}${timeoutText}${argShape}${outShape}${approval}${blocked}`;
            list.appendChild(item);
        });
        body.appendChild(list);
    }

    const activeTools = Array.isArray(summary.active_tools) ? summary.active_tools.slice(0, 4) : [];
    if (activeTools.length > 0) {
        const list = document.createElement('ul');
        list.className = 'debug-summary-list debug-summary-active-tools';
        activeTools.forEach(tool => {
            const item = document.createElement('li');
            const durationText = Number.isFinite(tool.duration_seconds) ? ` · ${tool.duration_seconds.toFixed(1)}s` : '';
            const timeoutText = Number.isFinite(tool.timeout_seconds) ? ` / ${tool.timeout_seconds.toFixed(0)}s timeout` : '';
            item.textContent = `${tool.name || 'tool'} · running${durationText}${timeoutText}`;
            list.appendChild(item);
        });
        body.appendChild(list);
    }

    const events = Array.isArray(summary.runtime_events) ? summary.runtime_events.slice(0, 6) : [];
    if (events.length > 0) {
        addRow('events', events.map(e => e.kind).filter(Boolean).join(', '));
    }

    const compactions = []
        .concat(Array.isArray(summary.phases) ? summary.phases : [])
        .concat(Array.isArray(summary.runtime_events) ? summary.runtime_events.filter(e => e && e.kind === 'compaction') : [])
        .filter(e => e && (e.phase === 'compacting' || e.kind === 'compaction'));
    if (compactions.length > 0) {
        const compaction = compactions[compactions.length - 1];
        const parts = [
            compaction.reason || compaction.strategy,
            compaction.estimated_tokens !== undefined ? `~${compaction.estimated_tokens} tokens` : '',
            compaction.message_count !== undefined ? `${compaction.message_count} msgs` : '',
            compaction.message_threshold !== undefined ? `threshold ${compaction.message_threshold}` : '',
            compaction.messages_compacted !== undefined ? `compacted ${compaction.messages_compacted}` : '',
            compaction.tail_preserved !== undefined ? `tail ${compaction.tail_preserved}` : '',
            compaction.bytes_saved !== undefined ? `saved ${compaction.bytes_saved} bytes` : '',
        ].filter(Boolean);
        addRow('compaction', parts.join(', '));
    }

    const errors = Array.isArray(summary.errors) ? summary.errors : [];
    if (errors.length > 0) {
        const error = errors[errors.length - 1];
        const parts = [
            error.code || 'error',
            error.timeout_type,
            Number.isFinite(error.elapsed_seconds) ? `${error.elapsed_seconds.toFixed(1)}s` : '',
        ].filter(Boolean);
        addRow('error', parts.join(', '));
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
            turn_id: 'web_abc123',
            interface: 'web',
            stop_reason: 'completed',
            final_phase: 'streaming',
            model: {provider: 'openai', name: 'gpt-test'},
            usage: {total_tokens: 42},
            counters: {tokens: 4, token_chars: 120},
            tools: [
                {
                    name: 'bash',
                    status: 'success',
                    duration_seconds: 0.42,
                    timeout_seconds: 30,
                    argument_shape: {type: 'object'},
                    output_shape: {type: 'object'},
                },
            ],
            active_tools: [{name: 'read_file', status: 'running', duration_seconds: 12.3, timeout_seconds: 30}],
            runtime_events: [
                {kind: 'queued_message'},
                {
                    kind: 'compaction',
                    reason: 'context_error_recovery',
                    strategy: 'drop_old_turn_groups',
                    estimated_tokens: 100000,
                    message_count: 90,
                    messages_compacted: 78,
                    tail_preserved: 10,
                },
            ],
            errors: [{code: 'timeout', timeout_type: 'stream_stall', elapsed_seconds: 30.4}],
            redaction: {raw_tool_output: 'omitted'},
        });

        const block = document.querySelector('.debug-summary');
        expect(block).not.toBeNull();
        expect(block.textContent).toContain('Debug diagnostics · 3.3s · completed');
        expect(block.textContent).toContain('web_abc123');
        expect(block.textContent).toContain('openai / gpt-test');
        expect(block.textContent).toContain('bash · success · 0.42s / 30s timeout · args object · output object');
        expect(block.textContent).toContain('read_file · running · 12.3s / 30s timeout');
        expect(block.textContent).toContain('context_error_recovery, ~100000 tokens, 90 msgs, compacted 78, tail 10');
        expect(block.textContent).toContain('timeout, stream_stall, 30.4s');
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

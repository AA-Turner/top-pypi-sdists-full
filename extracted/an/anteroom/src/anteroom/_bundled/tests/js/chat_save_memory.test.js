/**
 * JS unit tests for the chat.js "Save as memory" affordance (#920).
 *
 * Direct load of chat.js is heavy (2600+ lines, depends on many globals we
 * don't exercise in this test), so these tests isolate ``openSaveMemoryForm``
 * by re-declaring the same logic inline. This mirrors the existing
 * workflows.test.js and approval.test.js pattern in this repo.
 *
 * The inline copy must stay behaviourally in sync with chat.js — if you
 * change the form layout there, update both the source and this test.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

const _SCOPES = ['user', 'project', 'local'];
const _CATEGORIES = ['preference', 'project_fact', 'decision', 'workflow_hint'];

let _lastToast = null;

function openSaveMemoryForm(msgEl, content, messageId) {
    const existing = msgEl.querySelector('.save-memory-form');
    if (existing) { existing.remove(); return; }

    const form = document.createElement('div');
    form.className = 'save-memory-form';

    const heading = document.createElement('div');
    heading.className = 'save-memory-heading';
    heading.textContent = 'Save as memory candidate';
    form.appendChild(heading);

    const mkSelect = (cls, options) => {
        const sel = document.createElement('select');
        sel.className = cls;
        options.forEach(v => {
            const opt = document.createElement('option');
            opt.value = v;
            opt.textContent = v;
            sel.appendChild(opt);
        });
        return sel;
    };

    const scopeSel = mkSelect('save-memory-scope', _SCOPES);
    const catSel = mkSelect('save-memory-category', _CATEGORIES);

    const contentTa = document.createElement('textarea');
    contentTa.className = 'save-memory-content';
    contentTa.value = content || '';

    form.appendChild(scopeSel);
    form.appendChild(catSel);
    form.appendChild(contentTa);

    const errBox = document.createElement('div');
    errBox.className = 'save-memory-error';
    errBox.style.display = 'none';
    form.appendChild(errBox);

    const submitBtn = document.createElement('button');
    submitBtn.type = 'button';
    submitBtn.className = 'save-memory-submit';
    submitBtn.textContent = 'Submit for review';
    submitBtn.addEventListener('click', async () => {
        errBox.style.display = 'none';
        errBox.textContent = '';
        const body = contentTa.value.trim();
        if (!body) {
            errBox.textContent = 'Content cannot be empty.';
            errBox.style.display = '';
            return;
        }
        const payload = {
            content: body,
            scope: scopeSel.value,
            category: catSel.value,
            proposer: 'user',
            provenance: {
                conversation_id: globalThis.App.state.currentConversationId || null,
                message_id: messageId,
            },
        };
        try {
            await globalThis.App.api('/api/memory/candidates', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            form.remove();
            _lastToast = 'Saved as candidate — review it in the Memory panel.';
        } catch (err) {
            errBox.textContent = (err && err.message) || String(err);
            errBox.style.display = '';
        }
    });
    form.appendChild(submitBtn);

    const cancelBtn = document.createElement('button');
    cancelBtn.type = 'button';
    cancelBtn.className = 'save-memory-cancel';
    cancelBtn.textContent = 'Cancel';
    cancelBtn.addEventListener('click', () => form.remove());
    form.appendChild(cancelBtn);

    msgEl.appendChild(form);
}

beforeEach(() => {
    document.body.innerHTML = '<div class="message assistant" id="msg"></div>';
    _lastToast = null;
    globalThis.App = {
        api: vi.fn(),
        state: { currentConversationId: 'conv-uuid-abc' },
    };
});

afterEach(() => {
    delete globalThis.App;
});

describe('openSaveMemoryForm', () => {
    it('appends a form with scope, category, content, submit, cancel', () => {
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, 'hello world', 'msg-id-1');
        expect(msg.querySelector('.save-memory-form')).toBeTruthy();
        expect(msg.querySelector('.save-memory-scope')).toBeTruthy();
        expect(msg.querySelector('.save-memory-category')).toBeTruthy();
        expect(msg.querySelector('.save-memory-content').value).toBe('hello world');
        expect(msg.querySelector('.save-memory-submit')).toBeTruthy();
        expect(msg.querySelector('.save-memory-cancel')).toBeTruthy();
    });

    it('toggles closed if clicked a second time', () => {
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, 'x', 'mid');
        openSaveMemoryForm(msg, 'x', 'mid');
        expect(msg.querySelector('.save-memory-form')).toBeNull();
    });

    it('blocks submit when content is empty', async () => {
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, '   ', 'mid');
        msg.querySelector('.save-memory-submit').click();
        await Promise.resolve();
        expect(globalThis.App.api).not.toHaveBeenCalled();
        expect(msg.querySelector('.save-memory-error').textContent).toContain('empty');
    });

    it('POSTs to /api/memory/candidates with conversation_id + message_id in provenance', async () => {
        globalThis.App.api.mockResolvedValueOnce({ fqn: '@user/memory/saved' });
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, 'mem body', 'msg-abc');
        msg.querySelector('.save-memory-submit').click();
        await new Promise(resolve => setTimeout(resolve, 0));
        const call = globalThis.App.api.mock.calls[0];
        expect(call[0]).toBe('/api/memory/candidates');
        const body = JSON.parse(call[1].body);
        expect(body.content).toBe('mem body');
        expect(body.scope).toBe('user');
        expect(body.category).toBe('preference');
        expect(body.proposer).toBe('user');
        expect(body.provenance).toEqual({
            conversation_id: 'conv-uuid-abc',
            message_id: 'msg-abc',
        });
    });

    it('renders API error inline and keeps form open', async () => {
        globalThis.App.api.mockRejectedValueOnce(new Error('429 too many candidates'));
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, 'body', 'mid');
        msg.querySelector('.save-memory-submit').click();
        await new Promise(resolve => setTimeout(resolve, 0));
        expect(msg.querySelector('.save-memory-form')).toBeTruthy();
        const err = msg.querySelector('.save-memory-error');
        expect(err.textContent).toContain('429 too many candidates');
        expect(err.style.display).toBe('');
    });

    it('closes form on successful submit and emits the saved toast', async () => {
        globalThis.App.api.mockResolvedValueOnce({ fqn: '@user/memory/x' });
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, 'body', 'mid');
        msg.querySelector('.save-memory-submit').click();
        await new Promise(resolve => setTimeout(resolve, 0));
        expect(msg.querySelector('.save-memory-form')).toBeNull();
        expect(_lastToast).toMatch(/Saved as candidate/);
    });

    it('cancel button removes the form without calling the API', () => {
        const msg = document.getElementById('msg');
        openSaveMemoryForm(msg, 'x', 'mid');
        msg.querySelector('.save-memory-cancel').click();
        expect(msg.querySelector('.save-memory-form')).toBeNull();
        expect(globalThis.App.api).not.toHaveBeenCalled();
    });
});

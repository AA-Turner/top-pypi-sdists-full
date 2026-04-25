import { describe, it, expect, beforeEach, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const attachmentsSrc = readFileSync(
    resolve(__dirname, '../../src/anteroom/static/js/attachments.js'),
    'utf-8',
);

function buildDom() {
    document.body.innerHTML = `
        <button id="btn-attach"></button>
        <input id="file-input" type="file">
        <main class="chat-main"></main>
        <div id="attachment-previews"></div>
    `;
}

function loadAttachments() {
    const factory = new Function(`${attachmentsSrc}\nreturn Attachments;`);
    return factory();
}

describe('attachment upload size validation', () => {
    beforeEach(() => {
        buildDom();
        globalThis.alert = vi.fn();
        globalThis.URL.createObjectURL = vi.fn(() => 'blob:test');
    });

    it('accepts a text attachment exactly at the 50 MB default limit', () => {
        const Attachments = loadAttachments();
        Attachments.addFiles([
            {
                name: 'limit.txt',
                type: 'text/plain',
                size: 50 * 1024 * 1024,
            },
        ]);

        expect(globalThis.alert).not.toHaveBeenCalled();
        expect(Attachments.getFiles()).toHaveLength(1);
        expect(document.getElementById('attachment-previews').textContent).toContain('limit.txt (50.0 MB)');
    });

    it('rejects attachments over the 50 MB default limit with matching message', () => {
        const Attachments = loadAttachments();
        Attachments.addFiles([
            {
                name: 'too-big.txt',
                type: 'text/plain',
                size: (50 * 1024 * 1024) + 1,
            },
        ]);

        expect(Attachments.getFiles()).toHaveLength(0);
        expect(globalThis.alert).toHaveBeenCalledWith(expect.stringContaining('Maximum size: 50 MB'));
        expect(globalThis.alert).toHaveBeenCalledWith(expect.stringContaining('File too large: too-big.txt'));
    });
});

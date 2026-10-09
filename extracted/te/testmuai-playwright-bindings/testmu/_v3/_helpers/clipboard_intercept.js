(() => {
  if (window.__v16ClipInstalled) return;
  window.__v16ClipInstalled = true;
  const bridge = window.__v16ClipboardBridge;
  const send = (reps) => bridge(JSON.stringify({op: 'capture', reps})).catch(() => {});
  const readEntry = () => bridge(JSON.stringify({op: 'read'})).then((s) => JSON.parse(s));

  const b64ToFile = (b64, mime) => {
    const bin = atob(b64);
    const u = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    const ext = (mime.split('/')[1] || 'bin').split('+')[0];
    return new File([u], 'clipboard.' + ext, {type: mime});
  };
  const b64ToBlob = (b64, mime) =>
    new Blob([Uint8Array.from(atob(b64), (c) => c.charCodeAt(0))], {type: mime});

  // -- paste synthesis (used by the tool op AND the Ctrl/Cmd+V path) --
  window.__v16ClipboardPaste = (entry, plainOnly) => {
    let reps = (entry && entry.reps) || [];
    if (plainOnly) reps = reps.filter((r) => r.mime === 'text/plain');
    const dt = new DataTransfer();
    for (const r of reps) {
      if (r.text !== undefined) {
        try { dt.setData(r.mime, r.text); } catch (e) {}
      } else if (r.data_b64) {
        try { dt.items.add(b64ToFile(r.data_b64, r.mime)); } catch (e) {}
      }
    }
    const target = document.activeElement || document.body;
    const evt = new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true});
    const notPrevented = target.dispatchEvent(evt);
    if (notPrevented) {
      // Synthetic events skip the native insertion default action — emulate
      // for text (preserves caret + undo). isTrusted-checking editors are a
      // documented limitation.
      const text = dt.getData('text/plain');
      if (text) { try { document.execCommand('insertText', false, text); } catch (e) {} }
    }
    return true;
  };

  // -- patched async clipboard API (real API never invoked) --
  const api = {
    writeText: async (t) => { await send([{mime: 'text/plain', text: String(t)}]); },
    readText: async () => {
      const e = await readEntry();
      const r = (e.reps || []).find((x) => x.mime === 'text/plain');
      return r ? r.text : '';
    },
    write: async (items) => {
      const reps = [];
      for (const item of items || []) {
        for (const mime of item.types) {
          const blob = await item.getType(mime);
          if (mime.startsWith('text/')) {
            reps.push({mime, text: await blob.text()});
          } else {
            const buf = new Uint8Array(await blob.arrayBuffer());
            let bin = '';
            for (let i = 0; i < buf.length; i++) bin += String.fromCharCode(buf[i]);
            reps.push({mime, data_b64: btoa(bin)});
          }
        }
      }
      await send(reps);
    },
    read: async () => {
      const e = await readEntry();
      const parts = {};
      for (const r of e.reps || []) {
        parts[r.mime] = r.text !== undefined
          ? new Blob([r.text], {type: r.mime})
          : b64ToBlob(r.data_b64, r.mime);
      }
      return Object.keys(parts).length ? [new ClipboardItem(parts)] : [];
    },
  };
  try {
    Object.defineProperty(navigator, 'clipboard', {value: api, configurable: true});
  } catch (e) {
    try {
      navigator.clipboard.writeText = api.writeText;
      navigator.clipboard.readText = api.readText;
      navigator.clipboard.write = api.write;
      navigator.clipboard.read = api.read;
    } catch (e2) {}
  }

  // -- permissions: clipboard is always granted in the virtual world --
  try {
    const q = navigator.permissions.query.bind(navigator.permissions);
    navigator.permissions.query = (d) =>
      (d && /clipboard/.test(String(d.name)))
        ? Promise.resolve({state: 'granted', onchange: null})
        : q(d);
  } catch (e) {}

  // -- copy/cut capture (window bubble phase: runs after page handlers have
  //    setData; preventDefault keeps the OS clipboard untouched) --
  const captureCopy = (e) => {
    try {
      const reps = [];
      if (e.clipboardData) {
        for (const t of Array.from(e.clipboardData.types || [])) {
          const v = e.clipboardData.getData(t);
          if (v) reps.push({mime: t, text: v});
        }
      }
      if (!reps.length) {
        const sel = window.getSelection();
        const text = sel ? sel.toString() : '';
        let html = '';
        try {
          if (sel && sel.rangeCount) {
            const div = document.createElement('div');
            div.appendChild(sel.getRangeAt(0).cloneContents());
            html = div.innerHTML;
          }
        } catch (e2) {}
        if (text) reps.push({mime: 'text/plain', text});
        if (html && html !== text) reps.push({mime: 'text/html', text: html});
      }
      if (reps.length) send(reps);
      e.preventDefault();
      if (e.type === 'cut') {
        // preventDefault also suppressed the native selection deletion
        try { document.execCommand('delete'); } catch (e2) {}
      }
    } catch (e3) {}
  };
  window.addEventListener('copy', captureCopy, false);
  window.addEventListener('cut', captureCopy, false);

  // -- Ctrl/Cmd+V: suppress native OS paste (trusted CDP keys would insert
  //    OS content), synthesize from the store instead --
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'v' || e.key === 'V')) {
      e.preventDefault();
      const plainOnly = e.shiftKey;
      readEntry().then((entry) => window.__v16ClipboardPaste(entry, plainOnly)).catch(() => {});
    }
  }, true);
})();

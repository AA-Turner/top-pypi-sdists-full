// seq eval replay's page: the console's own replay player (the module the body's data-entry names, as the console's
// site serves it) mounted over this machine's server, which reads what the player asks for with the CLI's key.

const root = document.querySelector('[data-hook="replay"]');

function say(text) {
  const p = document.createElement('p');
  p.className = 'rp-say';
  p.textContent = text;
  root.replaceChildren(p);
}

// a response that went well, else an Error saying what the server said
async function ok(url) {
  const r = await fetch(url, { credentials: 'same-origin', cache: 'no-store' });
  if (!r.ok) {
    let why = `HTTP ${r.status}`;
    try { const b = await r.json(); if (b && b.error) why = b.error; } catch (_) { /* not JSON */ }
    throw new Error(why);
  }
  return r;
}

// a body read as it arrives, onBytes(n) told the running total - as the console reads a scene
async function body(res, onBytes) {
  if (!res.body || !onBytes) return new Uint8Array(await res.arrayBuffer());
  const reader = res.body.getReader();
  const parts = [];
  let n = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    parts.push(value);
    n += value.length;
    onBytes(n);
  }
  const out = new Uint8Array(n);
  let at = 0;
  for (const part of parts) { out.set(part, at); at += part.length; }
  return out;
}

async function sha256(buf) {
  const d = await crypto.subtle.digest('SHA-256', buf);
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function save(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

try {
  const { createPlayer, observedCameras } = await import(document.body.dataset.entry);
  const [report, details] = await Promise.all([ok('/api/report').then((r) => r.json()),
    ok('/api/details').then((r) => r.json())]);
  const player = createPlayer({
    initial: new URLSearchParams(location.search).get('ep'),
    onSelect: (index) => {
      const u = new URL(location.href);
      u.searchParams.set('ep', String(index));
      history.replaceState(history.state, '', u);
    },
    io: {
      replay: async (ep) => (await ok(`/api/replays/${encodeURIComponent(ep.index)}`)).arrayBuffer(),
      scene: async (sha, onBytes) => {
        const buf = await body(await ok(`/api/scenes/${encodeURIComponent(sha)}`), onBytes);
        const got = await sha256(buf);
        if (got !== sha) throw new Error(`scene ${sha.slice(0, 12)} arrived as ${got.slice(0, 12)}`);
        return buf;
      },
      video: async (ep) => (await ok(`/api/videos/${encodeURIComponent(ep.index)}.mp4`)).blob(),
      record: async (ep) => (await ok(`/api/episodes/${encodeURIComponent(ep.index)}/record`)).arrayBuffer(),
      save: (blob, name) => save(blob, `${document.body.dataset.name}-${name}`),
      cameras: async () => {
        const r = await fetch('/api/cameras', { credentials: 'same-origin' });
        return r.ok ? observedCameras((await r.json()).observation) : null;
      },
    },
  });
  root.replaceChildren(player.node);
  player.update(report, details);
  player.open();
} catch (err) {
  say(`The replay could not be opened: ${err && err.message ? err.message : err}`);
}

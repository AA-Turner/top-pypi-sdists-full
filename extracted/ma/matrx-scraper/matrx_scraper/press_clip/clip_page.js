// Press-clip page surgery — evaluated inside the page by the renderer.
//
// A port of newsjack skills/press-clip/clip.mjs @092d882 (MIT). Isolates the
// article STRUCTURALLY — keep the article and its ancestor chain, drop every
// sibling of that chain — so no site-specific class names are baked in.
// Publisher-specific junk inside the article is removed only through the
// caller's `drop`. Evaluated with page.evaluate (never a <script> tag), so a
// site's Content-Security-Policy cannot stop it. Installs window.__pressClip.
(() => {
  const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const txtLen = (el) => (el.innerText || '').trim().length;

  // --- selector description of an element, for the record (root_selector_used) ---
  function describe(el) {
    if (!el) return '';
    if (el === document.body) return 'body';
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (typeof el.className === 'string' && el.className.trim()) {
      s += '.' + el.className.trim().split(/\s+/).join('.');
    }
    return s;
  }

  const alnum = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const metaOf = (sel, attr = 'content') => {
    const e = document.querySelector(sel);
    return e ? norm(e.getAttribute(attr)) : '';
  };

  // --- the outlet's own name: og:site_name (when it is a name, not a URL), then the title suffix, then the host ---
  function outletName() {
    let site = metaOf('meta[property="og:site_name"]');
    if (/^https?:\/\//i.test(site)) site = '';
    const fromTitle = /\s[-|–—]\s/.test(document.title) ? norm(document.title.replace(/.*[-|–—]\s*/, '')) : '';
    return site || fromTitle || location.hostname.replace(/^www\./, '');
  }

  function hostCore() {
    const parts = location.hostname.replace(/^www\./, '').split('.');
    return alnum(parts.length > 2 && parts[parts.length - 2].length <= 3 ? parts[parts.length - 3] : parts[0]);
  }

  // A value that is just the outlet's own name ("AOL" on aol.co.uk) is not a person's byline.
  function isOutletName(v) {
    const a = alnum(v);
    if (a.length < 3) return false;
    const o = alnum(outletName());
    return a === o || o.startsWith(a) || a === hostCore() || a === alnum(metaOf('meta[name="twitter:site"]'));
  }

  // "Headline - Outlet" → "Headline" when the suffix names the outlet.
  function stripOutletSuffix(title) {
    const m = /^(.*\S)\s+[-|–—]\s+([^-|–—]{1,40})$/.exec(title || '');
    if (m && isOutletName(m[2])) return norm(m[1]);
    return norm(title);
  }

  function jsonLdArticle() {
    const ld = [];
    document.querySelectorAll('script[type="application/ld+json"]').forEach((s) => {
      try {
        const walk = (n) => {
          if (!n || typeof n !== 'object') return;
          if (Array.isArray(n)) return n.forEach(walk);
          ld.push(n);
          if (n['@graph']) walk(n['@graph']);
        };
        walk(JSON.parse(s.textContent || ''));
      } catch (e) { /* malformed JSON-LD is ignored, never guessed at */ }
    });
    return ld.find((n) => /Article|Report|Posting/i.test([].concat(n['@type'] || []).join(' '))) || null;
  }

  // The headline as the page's metadata states it (no visible-text fallback here).
  function metaHeadline() {
    const art = jsonLdArticle();
    return norm(art && typeof art.headline === 'string' ? art.headline : '')
      || stripOutletSuffix(metaOf('meta[property="og:title"]'))
      || stripOutletSuffix(metaOf('meta[name="twitter:title"]'));
  }

  // The headline ELEMENT: the h1-h3 whose text is the stated headline — never simply the
  // first <h1>, which on many templates is a sidebar section title ("Related stories").
  function headlineElement() {
    const heads = [...document.querySelectorAll('h1, h2, h3')].filter((h) => !h.closest('header, nav, footer, aside'));
    const H = metaHeadline().toLowerCase();
    if (H) {
      const hit = heads.find((h) => {
        const t = norm(h.textContent).toLowerCase();
        return t.length >= 12 && (t === H || H.startsWith(t) || t.startsWith(H));
      });
      if (hit) return hit;
    }
    return heads.find((h) => h.tagName === 'H1') || document.querySelector('h1');
  }

  const DATE_RE = /\b(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?,?\s+\d{4}|\d{4}-\d{2}-\d{2}(?:T[\d:.+-]+Z?)?)\b/i;
  const cleanBy = (t) => norm(t).replace(/^by\s+/i, '').split(/\s*[|•·]\s*|\s+[—–]\s+/)[0].trim();

  function bylineLine(scope) {
    for (const el of scope.querySelectorAll('[rel="author"], [itemprop="author"], [class*="byline" i], [class*="author-name" i], [class*="author" i]')) {
      const t = norm(el.innerText);
      if (t && t.length <= 120 && !isOutletName(cleanBy(t))) return t;
    }
    for (const el of scope.querySelectorAll('p, div, span, a, li')) {
      const t = norm(el.innerText);
      if (/^by\s+\S/i.test(t) && t.length <= 120) return t;
    }
    return '';
  }

  // --- headline / byline / date / outlet: meta tags first, then visible text; null when absent ---
  function readMeta() {
    const art = jsonLdArticle();
    const scope = pickContainer('');
    const ldAuthor = (() => {
      if (!art || !art.author) return '';
      return [].concat(art.author)
        .map((a) => norm((typeof a === 'string' ? a : a && a.name) || ''))
        .filter((n) => n && !isOutletName(n)).join(', ');
    })();
    const notUrl = (v) => (v && !/^https?:\/\//i.test(v) ? v : '');
    const personal = (v) => (v && !isOutletName(v) ? v : '');
    const head = headlineElement();
    const headline = metaHeadline() || (head ? norm(head.innerText || head.textContent) : '');
    const visibleBy = bylineLine(scope) || (scope !== document.body ? bylineLine(document.body) : '');
    const byline = personal(metaOf('meta[name="author"]'))
      || personal(notUrl(metaOf('meta[property="article:author"]')))
      || ldAuthor
      || cleanBy(visibleBy);
    const visibleDate = (() => {
      const t = scope.querySelector('time[datetime]') || document.querySelector('time[datetime]');
      if (t) return norm(t.getAttribute('datetime'));
      const tt = scope.querySelector('time') || document.querySelector('time');
      if (tt && norm(tt.innerText)) return norm(tt.innerText);
      const lines = [visibleBy, ...[...scope.querySelectorAll('[class*="date" i]')].map((e) => norm(e.innerText))];
      for (const line of lines) { const m = DATE_RE.exec(line || ''); if (m) return m[0]; }
      return '';
    })();
    const published = metaOf('meta[property="article:published_time"]')
      || metaOf('meta[name="article:published_time"]')
      || metaOf('meta[itemprop="datePublished"]')
      || metaOf('meta[name="pubdate"]')
      || metaOf('meta[name="publish-date"]')
      || metaOf('meta[name="date"]')
      || norm(art && typeof art.datePublished === 'string' ? art.datePublished : '')
      || visibleDate;
    return {
      outlet_name: outletName() || null,
      headline: headline || null,
      byline: byline || null,
      published_at: published || null,
    };
  }

  // --- masthead logo: the homepage-linking image/svg near the top (upstream detectMastheadLogo) ---
  function detectMastheadLogo() {
    let logoSrc = '', logoSvg = '';
    const badImg = /sprite|emoji|avatar|gravatar|icon-|\/thumbs?\/|uploads\/sites/i;
    const originRe = new RegExp('^' + location.origin.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\/?$');
    const brandCands = [
      ...[...document.querySelectorAll('a')].filter((a) => {
        const href = a.getAttribute('href') || ''; const r = a.getBoundingClientRect();
        return (href === '/' || originRe.test(href)) && r.top < 300 && r.width > 60;
      }),
      ...document.querySelectorAll('[class*="site-logo" i], [class*="masthead" i], [class*="navbar-brand" i], [class*="logo" i]'),
    ];
    for (const c of brandCands) {
      const img = c.matches('img') ? c : c.querySelector('img');
      if (img) { const s = img.currentSrc || img.src || ''; if (s && !badImg.test(s)) { logoSrc = s; break; } }
      const svg = c.matches('svg') ? c : c.querySelector('svg');
      if (svg && svg.getBoundingClientRect().width >= 60) { logoSvg = svg.outerHTML; break; }
    }
    return { logoSrc, logoSvg };
  }

  // --- last-resort logo: og:logo, then the site icon (absolute URL) ---
  function detectLogoFallback() {
    const meta = (sel, attr = 'content') => {
      const e = document.querySelector(sel); if (!e) return '';
      const v = (e.getAttribute(attr) || '').trim(); return v ? new URL(v, location.href).href : '';
    };
    return meta('meta[property="og:logo"]') || meta('link[rel*="icon"]', 'href');
  }

  // --- the article container, chosen structurally (upstream articleRoot) ---
  const SEL = ['article', '[class*="article-body" i]', '[class*="article-content" i]',
    '[class*="post-content" i]', '[class*="entry-content" i]', '[id^="post-" i]', '[class~="post"]', 'main'];

  function candidates() {
    let cands = [];
    SEL.forEach((s) => { try { document.querySelectorAll(s).forEach((el) => cands.push(el)); } catch (e) {} });
    return [...new Set(cands)].filter((el) => !el.closest('header, nav, footer, aside'));
  }

  // A body's worth of text: the ancestor walk stops at the first container holding this much.
  const BODY_MIN_CHARS = 500;

  function chooseContainer() {
    const head = headlineElement();
    const cands = candidates();
    if (cands.length) {
      const maxText = Math.max(...cands.map(txtLen));
      const solid = cands.filter((el) => txtLen(el) >= 0.6 * maxText && (!head || el.contains(head)));
      if (solid.length) return solid.sort((a, b) => txtLen(a) - txtLen(b))[0];   // tightest that qualifies
    }
    // No semantic container holds the headline: the tightest ancestor of the headline
    // that holds a body's worth of text, never inside site chrome.
    if (head) {
      for (let n = head.parentElement; n && n !== document.body; n = n.parentElement) {
        if (n.closest('header, nav, footer, aside')) break;
        if (txtLen(n) >= BODY_MIN_CHARS) return n;
      }
    }
    if (cands.length) return cands.sort((a, b) => txtLen(b) - txtLen(a))[0];  // fallback: most text
    return document.body;
  }

  function pickContainer(root) {
    if (root) { const el = document.querySelector(root); if (el) return el; }
    const marked = document.querySelector('[data-pc-root]');
    if (marked) return marked;
    return chooseContainer();
  }

  // Choose the container BEFORE scrolling: infinite-scroll templates append the next
  // stories into the same <main> on scroll, which would otherwise out-weigh the story.
  function markContainer(root) {
    const el = pickContainer(root);
    if (el !== document.body) el.setAttribute('data-pc-root', '');
    return describe(el);
  }

  // --- the surgery: isolate, de-junk, scope, sweep, stamp. Returns the record. ---
  function clip(o) {
    const outlet = outletName();
    const rootOverrideMatched = !!(o.root && document.querySelector(o.root));
    const articleRoot = pickContainer(o.root);
    const clientName = norm(o.clientName).toLowerCase();
    const clientFound = clientName ? norm(articleRoot.innerText).toLowerCase().includes(clientName) : false;

    const protectedEls = new Set();
    (o.keep || []).forEach((sel) => {
      try { document.querySelectorAll(sel).forEach((n) => protectedEls.add(n)); } catch (e) {}
    });
    const isProtected = (n) => { for (let p = n; p; p = p.parentElement) if (protectedEls.has(p)) return true; return false; };

    // keep the container and its ancestor chain; remove every sibling of that chain
    for (let node = articleRoot; node && node.parentElement && node !== document.body; node = node.parentElement) {
      for (const sib of [...node.parentElement.children]) {
        if (sib === node || sib.contains(articleRoot) || isProtected(sib)) continue;
        if (sib.tagName === 'STYLE' || sib.tagName === 'SCRIPT' || sib.tagName === 'LINK') continue;
        sib.remove();
      }
    }

    // inside the article: only high-confidence junk, plus the caller's drop — never `keep`
    const HARD_JUNK = [
      'iframe', 'ins.adsbygoogle', '.adsbygoogle', 'amp-ad', '[id^="div-gpt"]', '[id*="google_ads"]',
      '[data-ad]', '[aria-label*="advertisement" i]', '[role="dialog"]', '[aria-modal="true"]',
      '[class*="newsletter" i]', '[class*="ez-toc" i]', '[class*="table-of-contents" i]',
    ];
    const invalidDrop = [];
    [...HARD_JUNK, ...(o.drop || [])].forEach((sel) => {
      let found;
      try { found = document.querySelectorAll(sel); } catch (e) { invalidDrop.push(sel); return; }
      found.forEach((n) => { if (!n.contains(articleRoot) && !isProtected(n)) n.remove(); });
    });

    // widen the main column in case a removed sidebar left the article in a narrow grid track
    document.querySelectorAll('[class*="span8"], [class*="main-content"], [class*="content-area"]')
      .forEach((n) => { n.style.width = '100%'; n.style.maxWidth = '100%'; n.style.flex = '0 0 100%'; });

    // section scope: the lead + the section whose heading STARTS WITH the name, to the next same-level heading
    let sectionApplied = false;
    const target = norm(o.sectionHeading).toLowerCase();
    if (target) {
      const heads = [...articleRoot.querySelectorAll('h1,h2,h3,h4')];
      const start = heads.find((h) => norm(h.textContent).toLowerCase().startsWith(target));
      if (start) {
        sectionApplied = true;
        const level = start.tagName;
        const kids = [...start.parentElement.children];
        const sIdx = kids.indexOf(start);
        let eIdx = kids.length;
        for (let i = sIdx + 1; i < kids.length; i++) { if (kids[i].tagName === level) { eIdx = i; break; } }
        for (let i = kids.length - 1; i >= eIdx; i--) if (!isProtected(kids[i])) kids[i].remove();
        const firstHeadIdx = kids.findIndex((n) => /^H[1-4]$/.test(n.tagName));
        if (firstHeadIdx !== -1 && firstHeadIdx < sIdx) {
          for (let i = sIdx - 1; i >= firstHeadIdx; i--) if (!isProtected(kids[i])) kids[i].remove();
        }
      }
    }

    // sweep empty placeholder boxes (rendered size, no text, no media, no caption) — every removal logged
    const removed = [];
    const MEDIA = 'img, picture, video, svg, iframe, embed, object, figcaption, [class*="caption" i]';
    [...articleRoot.querySelectorAll('div, aside, section, blockquote, ins, figure')].forEach((el) => {
      if (!el.isConnected || isProtected(el)) return;
      const r = el.getBoundingClientRect();
      if (r.height < 8 || r.width < 8) return;
      if ((el.innerText || '').trim().length || el.querySelector(MEDIA)) return;
      // a short box holding nothing but line breaks is a blank line of body text — typography, not a slot
      if (r.height <= 48 && ![...el.querySelectorAll('*')].some((c) => c.tagName !== 'BR')) return;
      const cls = (typeof el.className === 'string' && el.className.trim()) ? '.' + el.className.trim().split(/\s+/).join('.') : '';
      removed.push(el.tagName.toLowerCase() + cls + ' [' + Math.round(r.width) + '×' + Math.round(r.height) + ']');
      el.remove();
    });

    // the clip header: the outlet LOGO only, large, above the article
    const esc = (s) => (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
    const LOGO_H = 64;
    const sizer = document.createElement('style');
    sizer.textContent = '.pc-logo svg{height:' + LOGO_H + 'px !important;width:auto !important}';
    (document.head || document.documentElement).appendChild(sizer);
    const logoSvg = o.logoSvg || '';
    const logoSvgDark = logoSvg
      .replace(/fill\s*=\s*"(#fff(fff)?|#ffffff|white)"/gi, 'fill="#111"')
      .replace(/fill\s*:\s*(#fff(fff)?|#ffffff|white)/gi, 'fill:#111');
    const logoHtml = logoSvg
      ? '<span class="pc-logo" style="display:inline-block;height:' + LOGO_H + 'px;line-height:0;color:#111">' + logoSvgDark + '</span>'
      : o.logoSrc
      ? '<img src="' + esc(o.logoSrc) + '" alt="' + esc(outlet) + '" style="height:' + LOGO_H + 'px;max-width:420px;width:auto;object-fit:contain;display:block">'
      : '<span style="font:700 30px/1 Georgia,serif;color:#111">' + esc(outlet) + '</span>';
    const header = document.createElement('div');
    header.className = 'pc-header';
    header.style.cssText = 'background:#fff;padding:4px 4px 16px;margin:0 0 14px;display:flex;justify-content:center;align-items:center';
    header.innerHTML = logoHtml;
    document.body.prepend(header);

    return {
      root_selector_used: o.root && rootOverrideMatched ? o.root : describe(articleRoot),
      root_override_matched: o.root ? rootOverrideMatched : null,
      removed_placeholders: removed,
      section_applied: sectionApplied,
      client_found_in_text: clientFound,
      invalid_selectors: invalidDrop,
      article_text_length: txtLen(articleRoot),
    };
  }

  // --- the last pass before printing: whatever arrived AFTER the surgery (consent managers
  // inject late) and fixed overlays, which would otherwise repeat on every printed page.
  // Returns every removal so nothing vanishes silently. `keep` still wins. ---
  function finalSweep(keep) {
    const root = document.querySelector('[data-pc-root]');
    const protectedEls = new Set();
    (keep || []).forEach((sel) => { try { document.querySelectorAll(sel).forEach((n) => protectedEls.add(n)); } catch (e) {} });
    const isProtected = (n) => { for (let p = n; p; p = p.parentElement) if (protectedEls.has(p)) return true; return false; };
    const spared = (el) => el.classList.contains('pc-header') || (root && el.contains(root)) || isProtected(el)
      || el.tagName === 'STYLE' || el.tagName === 'SCRIPT' || el.tagName === 'LINK';
    const removed = [];
    const drop = (el, why) => { removed.push(describe(el) + ' (' + why + ')'); el.remove(); };
    for (const el of [...document.documentElement.children]) {
      if (el !== document.head && el !== document.body) drop(el, 'outside body');
    }
    if (root && root !== document.body) {
      for (const el of [...document.body.children]) if (!spared(el)) drop(el, 'arrived after surgery');
    }
    for (const el of [...document.body.querySelectorAll('*')]) {
      if (!el.isConnected || spared(el)) continue;
      if (getComputedStyle(el).position === 'fixed') drop(el, 'fixed overlay');
    }
    // Some scripts put their window straight back once it is removed. Mark the story's
    // chain and hide every other top-level box by CSS, which a re-injection cannot undo.
    if (root && root !== document.body) {
      for (let n = root; n && n !== document.body; n = n.parentElement) n.setAttribute('data-pc-chain', '');
      document.querySelectorAll('.pc-header').forEach((h) => h.setAttribute('data-pc-chain', ''));
      protectedEls.forEach((k) => { for (let n = k; n && n !== document.body; n = n.parentElement) n.setAttribute('data-pc-chain', ''); });
      const guard = document.createElement('style');
      guard.id = 'pc-guard';
      guard.textContent = 'body > :not([data-pc-chain]):not(script):not(style):not(link){display:none !important}'
        + 'html > :not(head):not(body){display:none !important}';
      (document.head || document.documentElement).appendChild(guard);
    }
    return removed;
  }

  window.__pressClip = { describe, readMeta, headlineElement, detectMastheadLogo, detectLogoFallback, candidates, pickContainer, markContainer, clip, finalSweep };
})();

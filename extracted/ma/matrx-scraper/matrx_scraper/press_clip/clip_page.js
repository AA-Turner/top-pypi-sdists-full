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

  // --- a selector that matches EXACTLY this element on the page (root_selector_used must be checkable) ---
  // Same order as the server's root finder (aidream/services/press_clip/root_candidates.py stable_selector):
  // tag#id, tag.classes, tag.classes:has(> child.classes), then an :nth-of-type path from the nearest unique ancestor.
  function uniqueSelector(el) {
    if (!el) return '';
    if (el === document.body) return 'body';
    if (el === document.documentElement) return 'html';
    const count = (sel) => { try { return document.querySelectorAll(sel).length; } catch (e) { return -1; } };
    const esc = (v) => (window.CSS && CSS.escape ? CSS.escape(v) : v.replace(/[^\w-]/g, '\\$&'));
    const tag = el.tagName.toLowerCase();
    const classes = typeof el.className === 'string' ? el.className.trim().split(/\s+/).filter(Boolean) : [];
    const simple = tag + (el.id ? '#' + esc(el.id) : '') + classes.map((c) => '.' + esc(c)).join('');
    // The readable describe() form wins whenever it is already unique.
    const plain = describe(el);
    if (count(plain) === 1 && document.querySelector(plain) === el) return plain;
    if (el.id && count(tag + '#' + esc(el.id)) === 1) return tag + '#' + esc(el.id);
    const base = tag + classes.map((c) => '.' + esc(c)).join('');
    if (classes.length && count(base) === 1) return base;
    for (const child of el.children) {
      const cc = typeof child.className === 'string' ? child.className.trim().split(/\s+/).filter(Boolean) : [];
      if (!cc.length) continue;
      const sel = base + ':has(> ' + child.tagName.toLowerCase() + cc.map((c) => '.' + esc(c)).join('') + ')';
      if (count(sel) === 1 && document.querySelector(sel) === el) return sel;
    }
    const parent = el.parentElement;
    if (!parent) return simple;
    const nth = [...parent.children].filter((c) => c.tagName === el.tagName).indexOf(el) + 1;
    return uniqueSelector(parent) + ' > ' + tag + ':nth-of-type(' + nth + ')';
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

  // --- what counts as a photo. A blank ad slot carries a skeleton gradient, a spinner or a tiny
  // inline image as its "background"; none of those is content. The lists come from the host
  // (press.clip knobs) through clip(o).photo; these defaults are the knob seeds. ---
  const PHOTO_DEFAULTS = {
    inlineImageMaxChars: 4096,
    spinnerPatterns: ['spinner', 'loader', 'loading.gif', 'loading.svg', 'loading.png', 'placeholder',
      'skeleton', 'shimmer', 'spacer.gif', 'blank.gif', 'blank.png', 'transparent.gif', 'transparent.png',
      'pixel.gif', '1x1'],
    adSlotSizes: [[300, 250], [300, 600], [728, 90], [970, 250], [970, 90], [320, 50], [320, 100],
      [336, 280], [160, 600], [120, 600], [300, 50], [468, 60], [250, 250], [200, 200], [300, 1050]],
    adSlotTolerancePx: 4,
    // an <img> whose real picture waits in one of these attributes (lazy loading) is a real image
    lazyImageAttributes: ['data-src', 'data-lazy-src', 'data-srcset', 'data-lazy-srcset', 'data-original',
      'data-lazy', 'data-hi-res-src', 'data-full-src', 'srcset'],
    // an <iframe> from one of these hosts is an embedded video: content, never junk or an ad slot
    videoEmbedHosts: ['youtube.com', 'youtube-nocookie.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
      'dai.ly', 'players.brightcove.net', 'jwplayer.com', 'jwplatform.com', 'wistia.com', 'wistia.net',
      'vidyard.com', 'loom.com', 'facebook.com/plugins/video', 'tiktok.com/embed', 'twitch.tv', 'rumble.com',
      'streamable.com', 'cdn.jwplayer.com', 'video.ibm.com', 'ted.com'],
    // an exact ad token (a whole word of a class, id or data-* name, split on - _ and camelCase; "gpt-ad"
    // is two words in a row) marks an ad; ad-hoc, ad-free, no-ads and other negations or compounds never do
    adMarkerWords: ['ad', 'ads', 'advert', 'advertisement', 'sponsored', 'dfp', 'gpt-ad', 'adslot', 'ad-slot',
      'ad-container', 'taboola', 'outbrain'],
    // an <iframe> from one of these hosts is an editorial embed — a chart, audio, a social post: content
    editorialEmbedHosts: ['datawrapper.dwcdn.net', 'dwcdn.net', 'datawrapper.de', 'flo.uri.sh', 'flourish.studio',
      'infogram.com', 'e.infogram.com', 'public.tableau.com', 'open.spotify.com', 'w.soundcloud.com',
      'soundcloud.com', 'embed.podcasts.apple.com', 'platform.twitter.com', 'twitter.com', 'x.com',
      'instagram.com', 'bsky.app', 'embed.bsky.app', 'threads.net', 'tiktok.com/embed', 'google.com/maps/embed',
      'scribd.com', 'documentcloud.org', 'embed.documentcloud.org', 'genially.com', 'knightlab.com'],
    // a link, picture, frame or video from one of these hosts is an ad, whatever media it carries; so is a
    // link whose utm_source names one of them
    adNetworkHosts: ['doubleclick.net', 'googlesyndication.com', 'googleadservices.com', 'googletagservices.com',
      'adservice.google.com', 'taboola.com', 'taboolasyndication.com', 'outbrain.com', 'outbrainimg.com',
      'adnxs.com', 'adsrvr.org', 'criteo.com', 'criteo.net', 'amazon-adsystem.com', 'pubmatic.com',
      'rubiconproject.com', 'openx.net', 'adform.net', 'smartadserver.com', 'teads.tv', 'yieldmo.com',
      'sharethrough.com', 'triplelift.com', '3lift.com', 'moatads.com', 'revcontent.com', 'mgid.com',
      'zergnet.com', 'nativo.com', 'ntv.io', 'spotxchange.com', 'springserve.com', 'primis.tech'],
    // an inline <svg> or <canvas> this many pixels on its shorter side is a drawing (a chart), never a spinner
    drawingMinSidePx: 64,
  };
  let photoRules = PHOTO_DEFAULTS;
  const setPhotoRules = (p) => { photoRules = Object.assign({}, PHOTO_DEFAULTS, p || {}); };

  // A url() worth keeping: not a data-URI under the size threshold, not a spinner FILE. The spinner
  // patterns are matched against the file name only: "/photos/1x1/owner.jpg" (a ratio crop),
  // Cloudinary's "ar_1x1" and a "/placeholders-replaced/" folder are real pictures; "1x1.gif" is not.
  const isRealImageUrl = (url) => {
    const u = (url || '').trim();
    if (!u) return false;
    if (/^data:/i.test(u) && u.length < photoRules.inlineImageMaxChars) return false;
    let probe;
    if (/^data:/i.test(u)) probe = u.slice(0, 64);
    else {
      const path = u.split(/[?#]/)[0];
      probe = path.slice(path.lastIndexOf('/') + 1) || path;
    }
    probe = probe.toLowerCase();
    return !photoRules.spinnerPatterns.some((p) => p && probe.includes(String(p).toLowerCase()));
  };

  // The first URL of a src or srcset value.
  const firstUrl = (v) => (v || '').trim().split(/[\s,]+/)[0] || '';

  // An <iframe> embedding a video from a known player host (see isListedEmbed).
  const isVideoEmbed = (n) => isListedEmbed(n, photoRules.videoEmbedHosts);

  // The url() images of a computed background-image; gradients are never a url().
  const backgroundUrls = (bg) => {
    const out = [];
    const re = /url\(\s*(?:"([^"]*)"|'([^']*)'|([^)]*?))\s*\)/gi;
    let m;
    while ((m = re.exec(bg || ''))) out.push(m[1] ?? m[2] ?? m[3] ?? '');
    return out;
  };

  const hasBackgroundImage = (el) => {
    const bg = getComputedStyle(el).backgroundImage;
    if (!bg || bg === 'none') return false;
    return backgroundUrls(bg).some(isRealImageUrl);
  };

  // A host (or host + path) on one of these lists, matched on the URL's HOST first: "cdn.jwplayer.com" is
  // on "jwplayer.com"; "tiktok.com/embed" needs the host tiktok.com and a path starting /embed, so
  // "adserver-example.com/serve/tiktok.com/embed" is on nothing.
  const hostOnList = (src, list) => {
    if (!src) return false;
    let u;
    try { u = new URL(src, location.href); } catch (e) { return false; }
    const host = u.hostname.toLowerCase();
    const path = u.pathname.toLowerCase();
    return (list || []).some((h) => {
      const want = String(h || '').toLowerCase().replace(/^https?:\/\//, '');
      if (!want) return false;
      const cut = want.indexOf('/');
      const wantHost = cut === -1 ? want : want.slice(0, cut);
      const wantPath = cut === -1 ? '' : want.slice(cut);
      if (!(host === wantHost || host.endsWith('.' + wantHost))) return false;
      return !wantPath || path === wantPath || path.startsWith(wantPath.replace(/\/$/, '') + '/');
    });
  };

  // The words of a name ("dfp-AdSlot_top" -> dfp, ad, slot, top): split on - _ . / space and camelCase.
  // Each word knows whether camelCase glued it to the word before ("headAd": ad is glued to head).
  const nameWords = (v) => {
    const out = [];
    String(v || '').split(/[^A-Za-z0-9]+/).filter(Boolean).forEach((chunk) => {
      chunk.replace(/([a-z0-9])([A-Z])/g, '$1 $2').toLowerCase().split(' ').filter(Boolean)
        .forEach((w, k) => out.push({ w, glued: k > 0 }));
    });
    return out;
  };
  const nameParts = (v) => nameWords(v).map((x) => x.w);
  // Words after an ad word that make it a negation or a compound: ad-hoc, ad-free, ad-blocker, ad-less,
  // ads-disabled, data-ad-exclude, data-ad-position (where an ad goes beside this box, never the box).
  const NOT_AD_AFTER = ['hoc', 'free', 'block', 'blocker', 'blocking', 'blocked', 'less', 'lib', 'libs',
    'disabled', 'disable', 'off', 'exclude', 'excluded', 'position'];
  const NOT_AD_BEFORE = ['no', 'non', 'anti', 'without'];
  // A layout word that "ad" follows in one compound ("headAd", the class pair "lead ad") names a part of the
  // page, never an ad.
  const LAYOUT_BEFORE_AD = ['head', 'header', 'lead', 'masthead', 'hero', 'top', 'side', 'sidebar', 'foot',
    'footer', 'rail', 'inline', 'mid', 'main', 'body'];
  const AD_WORDS = ['ad', 'ads'];
  // An exact ad token (adMarkerWords; "gpt-ad" is the two words gpt, ad in a row) in a name's words.
  const hasAdToken = (v, tokens) => {
    const words = nameWords(v);
    const parts = words.map((x) => x.w);
    return (tokens || photoRules.adMarkerWords || []).some((t) => {
      const want = nameParts(t);
      if (!want.length) return false;
      for (let i = 0; i + want.length <= parts.length; i++) {
        if (!want.every((w, k) => parts[i + k] === w)) continue;
        if (NOT_AD_AFTER.includes(parts[i + want.length]) || NOT_AD_BEFORE.includes(parts[i - 1])) continue;
        if (want.length === 1 && AD_WORDS.includes(want[0]) && words[i].glued
          && LAYOUT_BEFORE_AD.includes(parts[i - 1])) continue;
        return true;
      }
      return false;
    });
  };
  // Ad attributes. Only a KNOWN ad-server attribute is strong alone (the AdSense / GPT slot attributes), plus
  // data-sponsor / data-sponsored with a truthy value. A data-ad-* or data-sponsor-* attribute whose name or
  // value says avoid, skip, ignore, none, break, insertion point, credit or exclude is the site telling its ad
  // code where NOT to go (or crediting a photo): editorial, never an ad mark. Any other data-ad-* is weak.
  const STRONG_AD_ATTRS = ['data-ad-slot', 'data-ad-unit', 'data-ad-client', 'data-google-query-id',
    'data-ad-format', 'data-ad-size', 'data-adunit', 'data-ad-placement-id'];
  const EDITORIAL_AD_ATTR_WORDS = ['avoid', 'skip', 'ignore', 'ignored', 'none', 'break', 'insertion',
    'insert', 'credit', 'credits', 'exclude', 'excluded'];
  const FALSY_ATTR_VALUES = ['', 'false', '0', 'no', 'none', 'off', 'null', 'undefined'];
  const isAdAttrName = (name) => /^data-(ads?|adunit|sponsor|sponsored|sponsorship)(-|$)/.test(name);
  const editorialAdAttr = (a) => {
    const name = a.name.toLowerCase();
    if (!isAdAttrName(name)) return false;
    return [...nameParts(name.slice(5)), ...nameParts(a.value)].some((w) => EDITORIAL_AD_ATTR_WORDS.includes(w));
  };
  const strongAdAttr = (a) => {
    const name = a.name.toLowerCase();
    if (editorialAdAttr(a)) return false;
    if (STRONG_AD_ATTRS.includes(name)) return true;
    if (name === 'data-sponsor' || name === 'data-sponsored') {
      return !FALSY_ATTR_VALUES.includes(String(a.value || '').trim().toLowerCase());
    }
    return false;
  };
  // A STRONG ad mark on one element, enough alone: a class that is exactly "ad" or "ads" (never after a
  // layout class: "lead ad"), an "advertorial" class or id word, or a known ad attribute (strongAdAttr).
  const STRONG_AD_WORDS = ['advertorial', 'advertorials'];
  const strongAdMark = (n) => {
    if (!n || n.nodeType !== 1) return false;
    const cls = (typeof n.className === 'string' ? n.className : (n.className && n.className.baseVal) || '')
      .split(/\s+/).filter(Boolean);
    if (cls.some((c, i) => AD_WORDS.includes(c.toLowerCase())
      && !LAYOUT_BEFORE_AD.includes(String(cls[i - 1] || '').toLowerCase()))) return true;
    if (cls.some((c) => hasAdToken(c, STRONG_AD_WORDS)) || (n.id && hasAdToken(n.id, STRONG_AD_WORDS))) return true;
    return [...n.attributes].some(strongAdAttr);
  };
  // An embed URL that is itself an ad: an ad token in its path ("/widgets/promoted.html",
  // "/players/AdUnit1.html"), or "promoted" / "sponsored" in its query ("?pb=sponsored-pin").
  const EMBED_AD_PATH = ['ad', 'ads', 'advert', 'advertisement', 'sponsored', 'promoted', 'adslot', 'adunit'];
  const embedUrlIsAd = (src) => {
    let u;
    try { u = new URL(src, location.href); } catch (e) { return false; }
    return hasAdToken(u.pathname.replace(/\.[a-z0-9]+$/i, ''), EMBED_AD_PATH)
      || hasAdToken(decodeURIComponent(u.search || ''), ['promoted', 'sponsored', 'advertisement']);
  };
  // An <iframe> from a host on ``list`` whose URL carries no ad mark.
  const isListedEmbed = (n, list) => {
    if (!n || n.tagName !== 'IFRAME') return false;
    const src = n.getAttribute('src') || n.getAttribute('data-src') || '';
    return hostOnList(src, list) && !embedUrlIsAd(src);
  };

  // An <iframe> embedding editorial content — a chart, a podcast, a social post — from a known host.
  // A promoted post from platform.twitter.com is an ad, not editorial.
  const isEditorialEmbed = (n) => isListedEmbed(n, photoRules.editorialEmbedHosts);

  // An inline <svg> or <canvas> drawn big enough to be a chart, not a spinner or an icon.
  const isDrawing = (m) => {
    const r = m.getBoundingClientRect();
    if (Math.min(r.width, r.height) < (photoRules.drawingMinSidePx || 0)) return false;
    const cls = ((typeof m.className === 'string' ? m.className : (m.className && m.className.baseVal) || '') + ' '
      + (m.id || '')).toLowerCase();
    return !photoRules.spinnerPatterns.some((p) => p && cls.includes(String(p).toLowerCase()));
  };

  // One element showing real media: a real src, a real picture waiting in a lazy-loading attribute
  // (data-src, data-lazy-src, srcset…), a <video> with any source (a lazy <source> included), an embedded
  // video player or editorial embed, or an inline chart (<svg>, <canvas>).
  const isRealMediaEl = (m) => {
    const tag = (m.localName || '').toLowerCase();
    if (tag === 'video') {
      return !!(m.currentSrc || m.getAttribute('src') || m.getAttribute('poster') || m.querySelector('source'));
    }
    if (tag === 'iframe') return isVideoEmbed(m) || isEditorialEmbed(m);
    if (tag === 'svg' || tag === 'canvas') return isDrawing(m);
    if (isRealImageUrl(m.currentSrc || m.getAttribute('src') || firstUrl(m.getAttribute('srcset')))) return true;
    return (photoRules.lazyImageAttributes || []).some((a) => isRealImageUrl(firstUrl(m.getAttribute(a))));
  };
  const MEDIA_ELEMENTS = 'img, picture source, video, iframe, svg, canvas';
  const realMedia = (el) => [...el.querySelectorAll(MEDIA_ELEMENTS)].filter(isRealMediaEl);
  const hasRealMedia = (el) => realMedia(el).length > 0;

  // An ad URL: a host on adNetworkHosts, an ad-network sub-domain whose label IS an ad token
  // ("ads.example.net", never "ads-media.example.com"), a utm_source naming a network, or a paid utm_medium.
  const AD_UTM_MEDIUMS = ['cpc', 'ppc', 'paid', 'display', 'native', 'sponsored', 'paidsocial', 'paid_social'];
  const isAdUrl = (src) => {
    if (!src || /^(data|blob|javascript):/i.test(src)) return false;
    if (hostOnList(src, photoRules.adNetworkHosts)) return true;
    let u;
    try { u = new URL(src, location.href); } catch (e) { return false; }
    const marks = (photoRules.adMarkerWords || []).map((w) => String(w).toLowerCase());
    if (u.hostname.toLowerCase().split('.').slice(0, -2).some((l) => marks.includes(l))) return true;
    const networks = (photoRules.adNetworkHosts || []).map((h) => String(h).toLowerCase().split('.')[0]);
    const source = (u.searchParams.get('utm_source') || '').toLowerCase();
    const medium = (u.searchParams.get('utm_medium') || '').toLowerCase();
    return (source && networks.includes(source)) || AD_UTM_MEDIUMS.includes(medium);
  };
  const AD_LABEL_WORDS = ['ad', 'ads', 'advert', 'advertisement', 'advertising', 'advertorial', 'sponsored',
    'promoted', 'paid'];
  const isAdLabel = (text) => {
    const words = norm(text).toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, ' ').split(/\s+/).filter(Boolean);
    return words.length > 0 && words.length <= 4 && AD_LABEL_WORDS.includes(words[0]);
  };
  // An ad TOKEN on one element: an exact ad token (adMarkerWords) in a class, its id or a data-* attribute
  // name ("data-ad-slot", never "data-ad-free"). Negations and compounds never count (hasAdToken), nor an
  // editorial ad attribute ("data-ad-avoid", "data-sponsor-credit": editorialAdAttr).
  const adToken = (n) => {
    if (!n || n.nodeType !== 1) return false;
    const cls = typeof n.className === 'string' ? n.className : (n.className && n.className.baseVal) || '';
    if (cls.split(/\s+/).some((c) => c && hasAdToken(c)) || (n.id && hasAdToken(n.id))) return true;
    return [...n.attributes].some((a) => /^data-/i.test(a.name) && !editorialAdAttr(a) && hasAdToken(a.name.slice(5)));
  };
  // An ad URL on one element: its link, picture, frame or video is served by or goes to an ad network.
  const adLink = (n) => !!n && n.nodeType === 1 && n.tagName === 'A' && isAdUrl(n.getAttribute('href'));
  const adCreative = (n) => !!n && n.nodeType === 1 && n.tagName !== 'A'
    && (['src', 'data-src', 'poster'].some((a) => isAdUrl(n.getAttribute(a))) || isAdUrl(firstUrl(n.getAttribute('srcset'))));
  const adOwn = (n) => strongAdMark(n) || adToken(n) || adLink(n) || adCreative(n) || isAdLabel((n && n.getAttribute && n.getAttribute('aria-label')) || '');

  // The box is an ad whatever media it carries only on TWO independent ad signals, never one: an ad
  // token (class, id, data-* name), a link to an ad network, a creative served by one, and a standard ad
  // size with no caption. An ad label ("Sponsored", "Advertisement") as the box's only text, or as the
  // aria-label around its media, is enough alone. Every piece of real media in the box must sit inside
  // an ad-marked element, so a photo beside an ad is never swept with it.
  const isStrongAd = (el) => {
    if (isAdLabel(el.innerText || '')) return true;
    const all = [el, ...el.querySelectorAll('*')];
    const media = realMedia(el);
    const chain = (m) => { const out = []; for (let p = m; p; p = p.parentElement) { out.push(p); if (p === el) break; } return out; };
    // With no real media (a spinner, a loading gif, an empty frame) one ad mark is enough.
    if (!media.length && !all.some(hasBackgroundImage)) return all.some(adOwn);
    // A strong mark (an exact "ad" class, advertorial, a known ad attribute) on the box, or around every
    // piece of its media, is enough alone.
    if (strongAdMark(el) || (media.length && media.every((m) => chain(m).some(strongAdMark)))) return true;
    if (!media.every((m) => chain(m).some(adOwn))) return false;
    if (media.some((m) => chain(m).some((p) => isAdLabel(p.getAttribute('aria-label') || '')))) return true;
    const signals = new Set();
    if (media.length ? media.every((m) => chain(m).some(adToken)) : all.some(adToken)) signals.add('token');
    if (all.some(adLink)) signals.add('link');
    if (all.some(adCreative)) signals.add('creative');
    const captioned = !!el.querySelector('figcaption, [class*="caption" i]');
    if (!captioned && isAdSlotSize(el.getBoundingClientRect())) signals.add('size');
    // A photo set as a CSS background stays content unless an ad-network URL is one of the signals.
    if (all.some(hasBackgroundImage) && !signals.has('link') && !signals.has('creative')) return false;
    return signals.size >= 2;
  };

  const isAdSlotSize = (r) => photoRules.adSlotSizes.some(([w, h]) =>
    Math.abs(r.width - w) <= photoRules.adSlotTolerancePx && Math.abs(r.height - h) <= photoRules.adSlotTolerancePx);

  // --- is the brand's name in the text as whole words? ("Coach" is not in "Coaching") ---
  function textHasWholeName(text, name) {
    const want = norm(name).toLowerCase();
    if (!want) return false;
    const escaped = want.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/ /g, '\\s+');
    return new RegExp('(^|[^\\p{L}\\p{N}])' + escaped + '(?=$|[^\\p{L}\\p{N}])', 'u').test(norm(text).toLowerCase());
  }

  // --- the surgery: isolate, de-junk, scope, sweep, stamp. Returns the record. ---
  function clip(o) {
    setPhotoRules(o.photo);
    const outlet = outletName();
    const rootOverrideMatched = !!(o.root && document.querySelector(o.root));
    const articleRoot = pickContainer(o.root);
    // Taken before the surgery: the selector must be unique on the page the reviewer will open, not on the clipped one.
    const rootSelectorUnique = uniqueSelector(articleRoot);
    const brandFound = textHasWholeName(articleRoot.innerText, o.brandName);

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
      found.forEach((n) => {
        if (n.contains(articleRoot) || isProtected(n)) return;
        // an embedded video or editorial embed (a chart, audio, a social post) is the story's media; only
        // the caller's own drop may remove it (one inside an ad box goes with the box, in the sweep)
        if (sel === 'iframe' && (isVideoEmbed(n) || isEditorialEmbed(n))) return;
        n.remove();
      });
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
      const text = (el.innerText || '').trim();
      if (text.length && !isAdLabel(text)) return;
      // A strong ad signal (an ad-network link or creative, an ad or sponsor class, id or label around
      // every piece of media in the box) makes it an ad whatever it carries — a picture, a video, a player.
      if (!isStrongAd(el)) {
        // A box holding real media — a real picture, a lazy-loaded one, a video, an embedded player, a
        // chart, an editorial embed — is never swept.
        if (hasRealMedia(el)) return;
        // With no real media, a standard IAB size makes it an ad slot whatever spinner, skeleton or inline
        // pixel it carries.
        const adSlot = isAdSlotSize(r);
        if (!adSlot && el.querySelector(MEDIA)) return;
        // a photo set as a CSS background (on the box or anything inside it) is content, never a slot
        if ([el, ...el.querySelectorAll('*')].some(hasBackgroundImage)) return;
        // a short box holding nothing but line breaks is a blank line of body text — typography, not a slot
        if (r.height <= 48 && ![...el.querySelectorAll('*')].some((c) => c.tagName !== 'BR')) return;
      }
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
      root_selector_used: o.root && rootOverrideMatched && document.querySelectorAll(o.root).length === 1 ? o.root : rootSelectorUnique,
      root_override_matched: o.root ? rootOverrideMatched : null,
      removed_placeholders: removed,
      section_applied: sectionApplied,
      brand_found_in_text: brandFound,
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

  window.__pressClip = { PHOTO_DEFAULTS, describe, uniqueSelector, readMeta, headlineElement, detectMastheadLogo, detectLogoFallback, candidates, pickContainer, markContainer, clip, finalSweep };
})();

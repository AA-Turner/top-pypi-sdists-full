/**
 * Pysae PPTX Helpers — pptxgenjs library with brand presets.
 *
 * Usage: Claude imports these helpers instead of rebuilding boilerplate.
 *
 *   const { createPres, addDarkSlide, addContentSlide, addKpiCards, COLORS, FONTS } = require('./pysae-pptx-helpers');
 *   const pptx = createPres("Mon deck upsell");
 *   addDarkSlide(pptx, { title: "Pysae", subtitle: "Ponctualité en temps réel" });
 *   addContentSlide(pptx, { title: "Le problème terrain", bullets: [...] });
 *   addKpiCards(pptx, [{ stat: "98.5%", label: "Ponctualité" }, ...]);
 *   pptx.writeFile({ fileName: "deck.pptx" });
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ── Brand tokens ──────────────────────────────────────────────────────────────

const COLORS = {
  primary: "00b871",     // Green — CTAs, H1, KPI stats, accents
  dark: "0a4b4d",        // Dark green — backgrounds (with topo only), H2
  body: "1a1a1a",        // Body text on white
  caption: "6b7a74",     // Captions, secondary labels
  lightBg: "f4f9f6",     // Alternating light sections
  white: "FFFFFF",
};

const FONTS = {
  face: "Poppins",
  title: { fontSize: 44, bold: true, color: COLORS.white, fontFace: "Poppins" },
  subtitle: { fontSize: 18, bold: false, color: COLORS.white, fontFace: "Poppins" },
  sectionH1: { fontSize: 18, bold: true, fontFace: "Poppins" }, // bicolor — use addBicolorTitle()
  h2: { fontSize: 13, bold: true, color: COLORS.dark, fontFace: "Poppins" },
  body: { fontSize: 11, color: COLORS.body, fontFace: "Poppins" },
  kpiStat: { fontSize: 28, bold: true, color: COLORS.primary, fontFace: "Poppins" },
  kpiLabel: { fontSize: 9.5, color: COLORS.dark, fontFace: "Poppins" },
  caption: { fontSize: 8.5, italic: true, color: COLORS.caption, fontFace: "Poppins" },
  cta: { fontSize: 11.5, bold: true, color: COLORS.dark, fontFace: "Poppins" },
};

// ── Topographic background ────────────────────────────────────────────────────

function loadTopoBackground() {
  const topoPath = path.resolve(__dirname, "../assets/fond-topo-b64.txt");
  const b64 = fs.readFileSync(topoPath, "utf-8").trim();
  if (b64.startsWith("REPLACE")) {
    throw new Error(
      "fond-topo-b64.txt is still a placeholder. " +
      "Replace it with the actual base64 PNG: base64 -w 0 fond-topo.png > fond-topo-b64.txt"
    );
  }
  return b64;
}

let _topoB64 = null;
function getTopoB64() {
  if (!_topoB64) _topoB64 = loadTopoBackground();
  return _topoB64;
}

// ── Presentation factory ──────────────────────────────────────────────────────

function createPres(title = "Pysae") {
  const pptx = new pptxgen();
  pptx.author = "Pysae";
  pptx.company = "Pysae";
  pptx.title = title;
  pptx.layout = "LAYOUT_16x9";
  return pptx;
}

// ── Dark slide (title, section break, conclusion) ─────────────────────────────

function addDarkSlide(pptx, { title, subtitle, showLogo = true } = {}) {
  const slide = pptx.addSlide();
  const topoB64 = getTopoB64();

  // Topographic background — never plain color
  slide.background = { data: `image/png;base64,${topoB64}` };

  // 2 oval blobs — signature element, positioned off-canvas right
  slide.addShape("ellipse", {
    x: 8.8, y: 0.3, w: 2.8, h: 4.5,
    fill: { color: COLORS.primary, transparency: 85 },
    line: { width: 0 },
  });
  slide.addShape("ellipse", {
    x: 9.5, y: 3.0, w: 2.0, h: 3.5,
    fill: { color: COLORS.primary, transparency: 85 },
    line: { width: 0 },
  });

  // Logo top-left — light version for dark slides
  if (showLogo) {
    const logoPath = path.resolve(__dirname, "../assets/logo-pysae-light.png");
    if (fs.existsSync(logoPath)) {
      slide.addImage({ path: logoPath, x: 0.4, y: 0.3, w: 1.2, h: 0.4 });
    }
  }

  // Title
  if (title) {
    slide.addText(title, {
      x: 0.5, y: 2.0, w: 8.0, h: 1.2,
      ...FONTS.title,
      align: "left",
    });
  }

  // Subtitle
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5, y: 3.2, w: 8.0, h: 0.8,
      ...FONTS.subtitle,
      align: "left",
    });
  }

  return slide;
}

// ── Content slide (white background) ──────────────────────────────────────────

function addContentSlide(pptx, { title, titleKeywords = [], bullets = [], bodyText } = {}) {
  const slide = pptx.addSlide();
  slide.background = { color: COLORS.white };

  // Bicolor section title
  if (title) {
    const titleParts = buildBicolorText(title, titleKeywords);
    slide.addText(titleParts, {
      x: 0.5, y: 0.4, w: 9.0, h: 0.7,
      fontSize: FONTS.sectionH1.fontSize,
      bold: true,
      fontFace: FONTS.face,
    });
  }

  // Bullets or body text
  const yStart = title ? 1.3 : 0.5;
  if (bullets.length > 0) {
    const bulletItems = bullets.map((b) => ({
      text: b,
      options: { ...FONTS.body, bullet: { indent: 15 }, paraSpaceAfter: 6 },
    }));
    slide.addText(bulletItems, {
      x: 0.5, y: yStart, w: 9.0, h: 4.5,
      valign: "top",
    });
  } else if (bodyText) {
    slide.addText(bodyText, {
      x: 0.5, y: yStart, w: 9.0, h: 4.5,
      ...FONTS.body,
      valign: "top",
    });
  }

  return slide;
}

// ── KPI cards slide ───────────────────────────────────────────────────────────

function addKpiCards(pptx, kpis, { darkBackground = false } = {}) {
  const slide = pptx.addSlide();

  if (darkBackground) {
    slide.background = { data: `image/png;base64,${getTopoB64()}` };
    // Add blobs on dark slides
    slide.addShape("ellipse", {
      x: 8.8, y: 0.3, w: 2.8, h: 4.5,
      fill: { color: COLORS.primary, transparency: 85 },
      line: { width: 0 },
    });
    slide.addShape("ellipse", {
      x: 9.5, y: 3.0, w: 2.0, h: 3.5,
      fill: { color: COLORS.primary, transparency: 85 },
      line: { width: 0 },
    });
  } else {
    slide.background = { color: COLORS.white };
  }

  const count = Math.min(kpis.length, 4);
  const cardW = 2.2;
  const gap = (9.0 - count * cardW) / (count + 1);

  kpis.slice(0, 4).forEach((kpi, i) => {
    const x = 0.5 + gap * (i + 1) + cardW * i;
    const y = 1.8;

    // Card shape — always ROUNDED_RECTANGLE
    slide.addShape("roundedRectangle", {
      x, y, w: cardW, h: 1.8,
      rectRadius: 0.12,
      fill: { color: darkBackground ? COLORS.white : "f7f7f7" },
      shadow: { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.1 },
    });

    // Stat value
    slide.addText(kpi.stat, {
      x, y: y + 0.2, w: cardW, h: 0.9,
      ...FONTS.kpiStat,
      align: "center",
    });

    // Label
    slide.addText(kpi.label, {
      x, y: y + 1.1, w: cardW, h: 0.5,
      ...FONTS.kpiLabel,
      align: "center",
      wrap: true,
    });
  });

  return slide;
}

// ── CTA / conclusion slide ────────────────────────────────────────────────────

function addCtaSlide(pptx, { title, ctaText = "Demander une démo", ctaSubtext } = {}) {
  const slide = addDarkSlide(pptx, { title, showLogo: true });

  // CTA button
  slide.addShape("roundedRectangle", {
    x: 0.5, y: 4.0, w: 3.0, h: 0.6,
    rectRadius: 0.12,
    fill: { color: COLORS.primary },
  });
  slide.addText(ctaText, {
    x: 0.5, y: 4.0, w: 3.0, h: 0.6,
    ...FONTS.cta,
    align: "center",
    valign: "middle",
  });

  if (ctaSubtext) {
    slide.addText(ctaSubtext, {
      x: 0.5, y: 4.7, w: 3.0, h: 0.4,
      ...FONTS.caption,
      color: COLORS.white,
      align: "center",
    });
  }

  return slide;
}

// ── Bicolor title helper ──────────────────────────────────────────────────────

function buildBicolorText(text, keywords = []) {
  if (keywords.length === 0) {
    return [{ text, options: { color: COLORS.dark, fontFace: FONTS.face, bold: true } }];
  }

  const parts = [];
  let remaining = text;

  for (const kw of keywords) {
    const idx = remaining.toLowerCase().indexOf(kw.toLowerCase());
    if (idx === -1) continue;

    if (idx > 0) {
      parts.push({
        text: remaining.slice(0, idx),
        options: { color: COLORS.dark, fontFace: FONTS.face, bold: true },
      });
    }
    parts.push({
      text: remaining.slice(idx, idx + kw.length),
      options: { color: COLORS.primary, fontFace: FONTS.face, bold: true },
    });
    remaining = remaining.slice(idx + kw.length);
  }

  if (remaining) {
    parts.push({
      text: remaining,
      options: { color: COLORS.dark, fontFace: FONTS.face, bold: true },
    });
  }

  return parts;
}

// ── Numbered badge helper ─────────────────────────────────────────────────────

function formatBadge(n) {
  return String(n).padStart(2, "0");
}

module.exports = {
  COLORS,
  FONTS,
  createPres,
  addDarkSlide,
  addContentSlide,
  addKpiCards,
  addCtaSlide,
  buildBicolorText,
  formatBadge,
  getTopoB64,
};

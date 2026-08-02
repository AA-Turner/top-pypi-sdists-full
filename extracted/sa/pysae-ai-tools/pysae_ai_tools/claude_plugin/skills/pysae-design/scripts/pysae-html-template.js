/**
 * Pysae HTML Template — generates branded landing pages.
 *
 * Usage:
 *   const { generateHtml, COLORS } = require('./pysae-html-template');
 *   const html = generateHtml({
 *     title: "Ponctualité en temps réel",
 *     heroSubtitle: "Anticipez les retards avant qu'ils n'impactent vos voyageurs",
 *     ctaText: "Demander une démo",
 *     ctaHref: "#contact",
 *     sections: [
 *       { type: "content", title: "Le défi terrain", body: "..." },
 *       { type: "kpis", items: [{ stat: "98.5%", label: "Ponctualité" }] },
 *       { type: "content", title: "Notre approche", body: "...", badge: "01" },
 *     ],
 *   });
 *   fs.writeFileSync("landing.html", html);
 */

const fs = require("fs");
const path = require("path");

const COLORS = {
  primary: "#00b871",
  dark: "#0a4b4d",
  body: "#1a1a1a",
  caption: "#6b7a74",
  lightBg: "#f4f9f6",
  white: "#FFFFFF",
};

function loadTopoB64() {
  const topoPath = path.resolve(__dirname, "../assets/fond-topo-b64.txt");
  const b64 = fs.readFileSync(topoPath, "utf-8").trim();
  if (b64.startsWith("REPLACE")) {
    throw new Error("fond-topo-b64.txt is still a placeholder.");
  }
  return b64;
}

function generateHtml({ title, heroSubtitle, ctaText = "Demander une démo", ctaHref = "#contact", sections = [] }) {
  const topoB64 = loadTopoB64();

  const sectionHtml = sections
    .map((s, i) => {
      const bgColor = i % 2 === 0 ? COLORS.white : COLORS.lightBg;

      if (s.type === "kpis") {
        return `
    <section style="background-color: ${bgColor}; padding: 60px 80px;">
      <div style="display: flex; gap: 24px; justify-content: center; flex-wrap: wrap;">
        ${s.items
          .map(
            (kpi) => `
          <div style="background: ${COLORS.white}; border-radius: 12px; padding: 32px 24px; min-width: 180px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="font-size: 36px; font-weight: 700; color: ${COLORS.primary};">${kpi.stat}</div>
            <div style="font-size: 14px; color: ${COLORS.dark}; margin-top: 8px;">${kpi.label}</div>
          </div>`
          )
          .join("")}
      </div>
    </section>`;
      }

      const badge = s.badge ? `<span style="display: inline-block; background: ${COLORS.primary}; color: white; border-radius: 50%; width: 32px; height: 32px; line-height: 32px; text-align: center; font-weight: 700; font-size: 14px; margin-right: 12px;">${s.badge}</span>` : "";

      return `
    <section style="background-color: ${bgColor}; padding: 60px 80px;">
      <h2 style="font-size: 24px; font-weight: 700; color: ${COLORS.dark}; margin-bottom: 16px;">
        ${badge}${highlightKeywords(s.title, s.keywords || [])}
      </h2>
      <div style="font-size: 16px; color: ${COLORS.body}; line-height: 1.7; max-width: 720px;">
        ${s.body}
      </div>
    </section>`;
    })
    .join("\n");

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — Pysae</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Poppins', sans-serif; color: ${COLORS.body}; }
    a { text-decoration: none; }
  </style>
</head>
<body>

  <!-- Hero — dark with topographic background -->
  <section style="
    background-image: url('data:image/png;base64,${topoB64}');
    background-size: cover;
    background-position: center;
    padding: 100px 80px;
    color: ${COLORS.white};
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  ">
    <h1 style="font-size: 42px; font-weight: 700; max-width: 600px; line-height: 1.2;">
      ${title}
    </h1>
    ${heroSubtitle ? `<p style="font-size: 18px; margin-top: 16px; max-width: 500px; opacity: 0.9;">${heroSubtitle}</p>` : ""}
    <a href="${ctaHref}" style="
      display: inline-block;
      margin-top: 32px;
      padding: 14px 32px;
      background: ${COLORS.primary};
      color: ${COLORS.white};
      font-weight: 700;
      font-size: 16px;
      border-radius: 8px;
      width: fit-content;
    ">${ctaText}</a>
  </section>

  <!-- Content sections -->
  ${sectionHtml}

  <!-- CTA footer — dark with topographic background -->
  <section style="
    background-image: url('data:image/png;base64,${topoB64}');
    background-size: cover;
    background-position: center;
    padding: 60px 80px;
    text-align: center;
    color: ${COLORS.white};
  ">
    <h2 style="font-size: 28px; font-weight: 700;">${title}</h2>
    <a href="${ctaHref}" style="
      display: inline-block;
      margin-top: 24px;
      padding: 14px 32px;
      background: ${COLORS.primary};
      color: ${COLORS.white};
      font-weight: 700;
      font-size: 16px;
      border-radius: 8px;
    ">${ctaText}</a>
  </section>

</body>
</html>`;
}

function highlightKeywords(text, keywords) {
  if (!keywords.length) return text;
  let result = text;
  for (const kw of keywords) {
    result = result.replace(
      new RegExp(`(${kw})`, "gi"),
      `<span style="color: ${COLORS.primary};">$1</span>`
    );
  }
  return result;
}

module.exports = { generateHtml, COLORS, highlightKeywords };

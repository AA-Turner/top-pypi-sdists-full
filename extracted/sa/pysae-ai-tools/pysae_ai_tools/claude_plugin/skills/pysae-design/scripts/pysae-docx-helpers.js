/**
 * Pysae DOCX Helpers — docx-js library with brand presets.
 *
 * Usage: Claude imports these helpers instead of rebuilding boilerplate.
 *
 *   const { createDoc, STYLES, heading1, heading2, bodyParagraph, docMgmtTable, brandTable } = require('./pysae-docx-helpers');
 *   const doc = createDoc("Proposition commerciale", { author: "Marketing Pysae" });
 *   // ... add sections using helpers ...
 *   const buffer = await Packer.toBuffer(doc);
 *   fs.writeFileSync("output.docx", buffer);
 */

const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, BorderStyle, AlignmentType, WidthType,
  ShadingType, Header, Footer, PageNumber, Packer,
} = require("docx");

// ── Brand tokens ──────────────────────────────────────────────────────────────

const COLORS = {
  primary: "00b871",
  dark: "0a4b4d",
  body: "1a1a1a",
  white: "FFFFFF",
  lightGreen: "e8f5ef",
};

const FONT = "Poppins";

// ── Default document styles ───────────────────────────────────────────────────

const STYLES = {
  default: {
    document: {
      run: { font: FONT, size: 22, color: COLORS.body },
      paragraph: { spacing: { after: 120 } },
    },
    heading1: {
      run: { font: FONT, size: 32, bold: true, color: COLORS.primary },
      paragraph: {
        spacing: { before: 240, after: 120 },
        border: {
          bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.primary },
        },
      },
    },
    heading2: {
      run: { font: FONT, size: 26, bold: true, color: COLORS.dark },
      paragraph: { spacing: { before: 200, after: 100 } },
    },
    heading3: {
      run: { font: FONT, size: 24, bold: true, color: COLORS.dark },
      paragraph: { spacing: { before: 160, after: 80 } },
    },
  },
};

// ── Document factory ──────────────────────────────────────────────────────────

function createDoc(title, { author = "Pysae", description = "" } = {}) {
  return new Document({
    creator: author,
    title,
    description,
    styles: STYLES,
    sections: [], // caller fills these
  });
}

// ── Section builder with header/footer ────────────────────────────────────────

function buildSection(children, { headerText = "Pysae", showPageNumbers = true } = {}) {
  return {
    properties: {
      page: {
        margin: { top: 1200, right: 1200, bottom: 1200, left: 1200 },
      },
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            children: [
              new TextRun({ text: headerText, font: FONT, size: 18, color: COLORS.dark, italic: true }),
            ],
            alignment: AlignmentType.LEFT,
          }),
        ],
      }),
    },
    footers: showPageNumbers
      ? {
          default: new Footer({
            children: [
              new Paragraph({
                children: [
                  new TextRun({ text: "Page ", font: FONT, size: 16, color: COLORS.caption || "6b7a74" }),
                  new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: COLORS.caption || "6b7a74" }),
                  new TextRun({ text: " / ", font: FONT, size: 16, color: COLORS.caption || "6b7a74" }),
                  new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: COLORS.caption || "6b7a74" }),
                ],
                alignment: AlignmentType.CENTER,
              }),
            ],
          }),
        }
      : {},
    children,
  };
}

// ── Paragraph helpers ─────────────────────────────────────────────────────────

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, font: FONT, bold: true, color: COLORS.primary, size: 32 })],
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.primary } },
    spacing: { before: 240, after: 120 },
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, font: FONT, bold: true, color: COLORS.dark, size: 26 })],
    spacing: { before: 200, after: 100 },
  });
}

function bodyParagraph(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: 22, color: COLORS.body })],
    spacing: { after: 120 },
  });
}

function bulletPoint(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: 22, color: COLORS.body })],
    bullet: { level: 0 },
    spacing: { after: 80 },
  });
}

// ── Document management block ─────────────────────────────────────────────────

function docMgmtTable({ version = "1.0", date, author = "Pysae", validator = "" } = {}) {
  const cellWidth = 2256; // 9026 / 4
  const headerStyle = { font: FONT, size: 18, bold: true, color: COLORS.white };
  const bodyStyle = { font: FONT, size: 18, color: COLORS.body };

  const headerShading = { type: ShadingType.CLEAR, fill: COLORS.dark };
  const bodyShading = { type: ShadingType.CLEAR, fill: COLORS.white };

  function headerCell(text) {
    return new TableCell({
      children: [new Paragraph({ children: [new TextRun({ text, ...headerStyle })] })],
      width: { size: cellWidth, type: WidthType.DXA },
      shading: headerShading,
    });
  }

  function bodyCell(text) {
    return new TableCell({
      children: [new Paragraph({ children: [new TextRun({ text, ...bodyStyle })] })],
      width: { size: cellWidth, type: WidthType.DXA },
      shading: bodyShading,
    });
  }

  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    rows: [
      new TableRow({ children: [headerCell("Version"), headerCell("Date"), headerCell("Auteur"), headerCell("Valideur")] }),
      new TableRow({ children: [bodyCell(version), bodyCell(date || new Date().toISOString().slice(0, 10)), bodyCell(author), bodyCell(validator)] }),
    ],
  });
}

// ── Brand table helper ────────────────────────────────────────────────────────

function brandTable(headers, rows) {
  const colWidth = Math.floor(9026 / headers.length);

  const headerRow = new TableRow({
    children: headers.map((h) =>
      new TableCell({
        children: [new Paragraph({ children: [new TextRun({ text: h, font: FONT, size: 20, bold: true, color: COLORS.white })] })],
        width: { size: colWidth, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: COLORS.dark },
      })
    ),
  });

  const dataRows = rows.map((row, rowIdx) =>
    new TableRow({
      children: row.map((cell) =>
        new TableCell({
          children: [new Paragraph({ children: [new TextRun({ text: String(cell), font: FONT, size: 20, color: COLORS.body })] })],
          width: { size: colWidth, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill: rowIdx % 2 === 0 ? COLORS.white : COLORS.lightGreen },
        })
      ),
    })
  );

  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    rows: [headerRow, ...dataRows],
  });
}

module.exports = {
  COLORS,
  FONT,
  STYLES,
  createDoc,
  buildSection,
  heading1,
  heading2,
  bodyParagraph,
  bulletPoint,
  docMgmtTable,
  brandTable,
  // Re-export docx classes for composition
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, BorderStyle, AlignmentType, WidthType,
  ShadingType, Header, Footer, PageNumber, Packer,
};

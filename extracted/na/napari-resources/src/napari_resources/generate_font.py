#!/usr/bin/env python3

# /// script
# dependencies = [
#   "fontTools",
# ]
# ///

"""Tool to generate the napari font."""

import sys
from importlib import resources
from pathlib import Path

import click
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

fonts = resources.files("napari_resources.resources.fonts")


@click.command(
    context_settings={"help_option_names": ["-h", "--help"], "show_default": True},
)
@click.argument(
    "output_dir",
    type=click.Path(exists=True, file_okay=False),
)
def generate_font(output_dir):
    """Generate the AlataPlus font (mix of Alata and MPlus)."""
    Mplus = TTFont(fonts / "M_PLUS_1p" / "MPLUS1p-Regular.ttf")
    Alata = TTFont(fonts / "Alata" / "Alata-Regular.ttf")
    AlataPlus = TTFont(fonts / "M_PLUS_1p" / "MPLUS1p-Regular.ttf")

    missing_glyphs = Alata.getGlyphOrder()

    scale_factor = Alata["head"].unitsPerEm / Mplus["head"].unitsPerEm

    for glyph in missing_glyphs:
        g = Alata["glyf"][glyph]
        # rescale glyph (if the unitsPerEm are different the sizes would mismatch)
        pen = TTGlyphPen(Alata.getGlyphSet())
        tpen = TransformPen(pen, (scale_factor, 0, 0, scale_factor, 0, 0))
        g.draw(tpen, Alata.getGlyphSet())

        # copy the glyph and its scale metrics into the new font
        AlataPlus["glyf"][glyph] = pen.glyph()
        width, lsb = Alata["hmtx"][glyph]
        AlataPlus["hmtx"][glyph] = (int(width * scale_factor), int(lsb * scale_factor))

    # we need a format12 cmap in order to store glyphs from unicode above U+10FFFF
    # so we find or create one
    format12 = None
    for t in AlataPlus["cmap"].tables:
        if t.format == 12:
            format12 = t
            break
    if not format12:
        from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

        format12 = CmapSubtable.newSubtable(12)
        format12.platformID = 3  # Windows
        format12.platEncID = 10  # Unicode full repertoire
        format12.language = 0
        format12.cmap = {}
        AlataPlus["cmap"].tables.append(format12)

    # copy codepoints from mplus into format12 cmap
    for table in Mplus["cmap"].tables:
        for codepoint, glyph_name in table.cmap.items():
            if codepoint not in format12.cmap:
                format12.cmap[codepoint] = glyph_name

    # set all the family and name metadata so it can be found correctly by the system
    family_name = "AlataPlus"
    style_name = "Regular"
    full_name = f"{family_name} {style_name}"
    postscript_name = f"{family_name}-{style_name}"

    name_table = AlataPlus["name"]
    for record in name_table.names:
        enc = record.getEncoding()
        if record.nameID in (1, 16):  # Family + Typographic Family
            record.string = family_name.encode(enc)
        elif record.nameID in (2, 17):  # Subfamily + Typographic Subfamily
            record.string = style_name.encode(enc)
        elif record.nameID == 4:  # Full font name
            record.string = full_name.encode(enc)
        elif record.nameID == 6:  # PostScript name
            record.string = postscript_name.encode(enc)
        elif record.nameID == 3:  # Unique identifier
            record.string = postscript_name.encode(enc)
        elif record.nameID == 5:  # Version string
            record.string = b"Version 1.0"

    output = Path(output_dir) / family_name / f"{postscript_name}.ttf"
    if output.exists():
        # check against existing output to not create identical font with simply
        # different timestamps
        OldAlataPlus = TTFont(output)
        if OldAlataPlus["glyf"].compile(OldAlataPlus) == AlataPlus["glyf"].compile(AlataPlus) and OldAlataPlus[
            "hmtx"
        ].compile(OldAlataPlus) == AlataPlus["hmtx"].compile(AlataPlus):
            print("The font seems to be unchanged; not writing it out!")
            sys.exit()
        else:
            AlataPlus["head"].created = OldAlataPlus["head"].created

    output.parent.mkdir(parents=True, exist_ok=True)
    AlataPlus.save(output, reorderTables=True)
    print(f"The font was modified; written out to {output}")


def main() -> None:
    """Generate the font from the command line."""
    generate_font()


if __name__ == "__main__":
    main()

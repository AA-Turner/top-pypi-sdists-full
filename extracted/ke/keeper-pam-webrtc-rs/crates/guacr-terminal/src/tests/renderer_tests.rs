use crate::config::ColorScheme;
use crate::renderer::TerminalRenderer;

#[test]
fn test_renderer_new() {
    let renderer = TerminalRenderer::new();
    assert!(renderer.is_ok());
}

#[test]
fn test_renderer_with_dimensions() {
    let renderer = TerminalRenderer::new_with_dimensions(24, 45, 31.5);
    assert!(renderer.is_ok());
}

#[test]
fn test_vt100_color_to_rgb() {
    let renderer = TerminalRenderer::new().unwrap();
    // Default color scheme is GRAY_BLACK (gray foreground, black background)
    let fg_color = renderer.vt100_color_to_rgb(vt100::Color::Default, true);
    assert_eq!(fg_color.0, [229, 229, 229]); // Gray foreground

    let bg_color = renderer.vt100_color_to_rgb(vt100::Color::Default, false);
    assert_eq!(bg_color.0, [0, 0, 0]); // Black background
}

#[test]
fn test_color_scheme_application() {
    // Test with green-black scheme
    let renderer =
        TerminalRenderer::new_with_dimensions_and_scheme(19, 38, 28.0, ColorScheme::GREEN_BLACK)
            .unwrap();

    let fg_color = renderer.vt100_color_to_rgb(vt100::Color::Default, true);
    assert_eq!(fg_color.0, [0, 255, 0]); // Green foreground

    let bg_color = renderer.vt100_color_to_rgb(vt100::Color::Default, false);
    assert_eq!(bg_color.0, [0, 0, 0]); // Black background
}

// -- Font fallback tests --
//
// Glyph presence cannot be inferred from rasterized dimensions: fontdue rasterizes a
// codepoint the font lacks as glyph 0 (.notdef), and in JetBrains Mono .notdef is a visible
// box, 7 pixels wide with 63 ink pixels at the default font size. Facts these tests rely on,
// probed from the two bundled TTFs: U+2605 BLACK STAR is glyph 0 in JetBrainsMono-Regular
// and glyph 2652 in DejaVuSansMono; U+2500 BOX DRAWINGS LIGHT HORIZONTAL is glyph 1326 in
// JetBrains Mono; U+2800 BRAILLE PATTERN BLANK is glyph 0 in both.

#[test]
fn test_char_missing_from_the_primary_font_uses_the_fallback_font() {
    let renderer = TerminalRenderer::new().unwrap();

    assert!(
        std::ptr::eq(renderer.get_font_for_char('★'), renderer.font_fallback()),
        "U+2605 is absent from JetBrains Mono, so it must be drawn from DejaVu Sans Mono \
         rather than as a .notdef box"
    );
}

#[test]
fn test_char_present_in_the_primary_font_uses_the_primary_font() {
    let renderer = TerminalRenderer::new().unwrap();

    for c in ['a', '─', ' '] {
        assert!(
            !std::ptr::eq(renderer.get_font_for_char(c), renderer.font_fallback()),
            "{:?} is in JetBrains Mono and must not be taken from the fallback font",
            c
        );
    }
}

#[test]
fn test_char_missing_from_both_fonts_uses_the_primary_font() {
    let renderer = TerminalRenderer::new().unwrap();

    // Neither font has braille. There is nothing better to draw than the primary font's
    // .notdef, and the fallback must not be preferred for it.
    assert!(
        !std::ptr::eq(
            renderer.get_font_for_char('\u{2800}'),
            renderer.font_fallback()
        ),
        "a codepoint neither font has must resolve to the primary font"
    );
}

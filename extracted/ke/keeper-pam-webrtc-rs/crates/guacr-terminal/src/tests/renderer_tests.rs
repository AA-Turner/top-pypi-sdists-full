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

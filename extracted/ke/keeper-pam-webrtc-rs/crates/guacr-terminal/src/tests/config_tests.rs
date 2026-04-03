use crate::config::{ColorScheme, TerminalConfig};
use std::collections::HashMap;

#[test]
fn test_default_config() {
    let config = TerminalConfig::default();
    assert_eq!(config.font_size, 12);
    assert_eq!(config.terminal_type, "xterm-256color");
    assert_eq!(config.scrollback_size, 1000);
    assert_eq!(config.backspace_code, 127);
    assert_eq!(config.color_scheme, ColorScheme::GRAY_BLACK);
}

#[test]
fn test_from_params() {
    let mut params = HashMap::new();
    params.insert("font-name".to_string(), "Consolas".to_string());
    params.insert("font-size".to_string(), "14".to_string());
    params.insert("color-scheme".to_string(), "green-black".to_string());
    params.insert("terminal-type".to_string(), "xterm".to_string());
    params.insert("scrollback".to_string(), "500".to_string());
    params.insert("backspace".to_string(), "8".to_string());

    let config = TerminalConfig::from_params(&params);
    assert_eq!(config.font_name, Some("Consolas".to_string()));
    assert_eq!(config.font_size, 14);
    assert_eq!(config.color_scheme, ColorScheme::GREEN_BLACK);
    assert_eq!(config.terminal_type, "xterm");
    assert_eq!(config.scrollback_size, 500);
    assert_eq!(config.backspace_code, 8);
}

#[test]
fn test_font_size_clamping() {
    let mut params = HashMap::new();

    // Too small
    params.insert("font-size".to_string(), "2".to_string());
    let config = TerminalConfig::from_params(&params);
    assert_eq!(config.font_size, 6);

    // Too large
    params.insert("font-size".to_string(), "100".to_string());
    let config = TerminalConfig::from_params(&params);
    assert_eq!(config.font_size, 72);
}

#[test]
fn test_scrollback_clamping() {
    let mut params = HashMap::new();
    params.insert("scrollback".to_string(), "999999".to_string());
    let config = TerminalConfig::from_params(&params);
    assert_eq!(config.scrollback_size, 10000);
}

#[test]
fn test_color_scheme_from_name() {
    assert_eq!(
        ColorScheme::from_name("black-white"),
        ColorScheme::BLACK_WHITE
    );
    assert_eq!(
        ColorScheme::from_name("gray-black"),
        ColorScheme::GRAY_BLACK
    );
    assert_eq!(
        ColorScheme::from_name("green-black"),
        ColorScheme::GREEN_BLACK
    );
    assert_eq!(
        ColorScheme::from_name("white-black"),
        ColorScheme::WHITE_BLACK
    );

    // Case insensitive
    assert_eq!(
        ColorScheme::from_name("BLACK-WHITE"),
        ColorScheme::BLACK_WHITE
    );

    // Unknown defaults to gray-black
    assert_eq!(ColorScheme::from_name("unknown"), ColorScheme::GRAY_BLACK);
}

#[test]
fn test_custom_color_scheme() {
    let scheme = ColorScheme::from_name("255,0,0;0,0,255");
    assert_eq!(scheme.foreground, [255, 0, 0]);
    assert_eq!(scheme.background, [0, 0, 255]);
}

#[test]
fn test_backspace_variants() {
    let mut params = HashMap::new();

    params.insert("backspace".to_string(), "127".to_string());
    assert_eq!(TerminalConfig::from_params(&params).backspace_code, 127);

    params.insert("backspace".to_string(), "DEL".to_string());
    assert_eq!(TerminalConfig::from_params(&params).backspace_code, 127);

    params.insert("backspace".to_string(), "8".to_string());
    assert_eq!(TerminalConfig::from_params(&params).backspace_code, 8);

    params.insert("backspace".to_string(), "BS".to_string());
    assert_eq!(TerminalConfig::from_params(&params).backspace_code, 8);
}

use crate::handler_helpers::parse_display_size;
use std::collections::HashMap;

#[test]
fn test_parse_display_size_default() {
    let params = HashMap::new();
    let (w, h, cols, rows) = parse_display_size(&params);
    assert_eq!(w, 1024);
    assert_eq!(h, 768);
    assert_eq!(cols, (1024 / 9) as u16);
    assert_eq!(rows, (768 / 18) as u16);
}

#[test]
fn test_parse_display_size_custom() {
    let mut params = HashMap::new();
    params.insert("size".to_string(), "1920,1080,96".to_string());
    let (w, h, cols, rows) = parse_display_size(&params);
    assert_eq!(w, 1920);
    assert_eq!(h, 1080);
    assert_eq!(cols, (1920 / 9) as u16);
    assert_eq!(rows, (1080 / 18) as u16);
}

#[test]
fn test_parse_display_size_small() {
    let mut params = HashMap::new();
    // Very small size should be clamped to minimums
    params.insert("size".to_string(), "100,100,96".to_string());
    let (w, h, cols, rows) = parse_display_size(&params);
    assert_eq!(w, 100);
    assert_eq!(h, 100);
    assert_eq!(cols, 80); // (100/9)=11, clamped to 80
    assert_eq!(rows, 24); // (100/18)=5, clamped to 24
}

#[test]
fn test_parse_display_size_invalid() {
    let mut params = HashMap::new();
    params.insert("size".to_string(), "not_a_number".to_string());
    let (w, h, cols, rows) = parse_display_size(&params);
    // Falls back to defaults
    assert_eq!(w, 1024);
    assert_eq!(h, 768);
    assert_eq!(cols, (1024 / 9) as u16);
    assert_eq!(rows, (768 / 18) as u16);
}

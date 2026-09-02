use crate::drawing::{
    format_arc, format_cfill, format_copy, format_curve, format_img, format_line, format_rect,
    format_shade,
};

#[test]
fn test_format_rect() {
    let instr = format_rect(0, 10, 20, 100, 50);
    assert_eq!(instr, "4.rect,1.0,2.10,2.20,3.100,2.50;");
}

#[test]
fn test_format_cfill() {
    let instr = format_cfill(14, 0, 255, 0, 0, 255);
    assert_eq!(instr, "5.cfill,2.14,1.0,3.255,1.0,1.0,3.255;");
}

#[test]
fn test_format_line() {
    let instr = format_line(0, 0, 0, 100, 100);
    assert_eq!(instr, "4.line,1.0,1.0,1.0,3.100,3.100;");
}

#[test]
fn test_format_arc() {
    let instr = format_arc(0, 50, 50, 25, 25, 0.0, std::f64::consts::PI);
    assert!(instr.starts_with("3.arc,"));
    assert!(instr.contains("50"));
}

#[test]
fn test_format_curve() {
    let instr = format_curve(0, 0, 0, 50, 50, 100, 100);
    assert_eq!(instr, "5.curve,1.0,1.0,1.0,2.50,2.50,3.100,3.100;");
}

#[test]
fn test_format_shade() {
    let instr = format_shade(0, 0, 0, 100, 50, 255, 0, 0, 255, 0, 0, 255, 255);
    assert!(instr.starts_with("5.shade,"));
    assert!(instr.contains("255"));
}

#[test]
fn test_format_copy() {
    let instr = format_copy(0, 10, 20, 100, 50, 12, 0, 30, 40);
    assert_eq!(instr, "4.copy,1.0,2.10,2.20,3.100,2.50,2.12,1.0,2.30,2.40;");
}

#[test]
fn test_format_img() {
    let instr = format_img(42, 15, 0, "image/jpeg", 100, 200);
    assert_eq!(instr, "3.img,2.42,2.15,1.0,10.image/jpeg,3.100,3.200;");
}

use crate::advanced::{format_ack, format_error, format_nest, format_pipe, format_transfer};

#[test]
fn test_format_transfer() {
    let instr = format_transfer(0, 0, 0, 100, 50, 12, 0, 10, 20);
    // "transfer" is 8 characters
    assert!(instr.starts_with("8.transfer,"));
    assert!(instr.contains("100"));
}

#[test]
fn test_format_nest() {
    let instr = format_nest("conn-123", 0, 10, 20);
    assert!(instr.starts_with("4.nest,"));
    assert!(instr.contains("conn-123"));
}

#[test]
fn test_format_pipe() {
    let instr = format_pipe(1, "application/octet-stream", "mypipe");
    assert!(instr.starts_with("4.pipe,"));
    assert!(instr.contains("mypipe"));
}

#[test]
fn test_format_ack() {
    let instr = format_ack(1, "ok");
    assert_eq!(instr, "3.ack,1.1,2.ok;");
}

#[test]
fn test_format_error() {
    let instr = format_error("Authentication failed", 769);
    assert_eq!(instr, "5.error,21.Authentication failed,3.769;");

    let instr2 = format_error("Connection timeout", 514);
    assert_eq!(instr2, "5.error,18.Connection timeout,3.514;");
}

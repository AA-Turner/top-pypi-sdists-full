use crate::layers::{format_dispose, format_move};

#[test]
fn test_format_dispose() {
    let instr = format_dispose(0);
    // "dispose" is 7 characters, but instruction format is: <opcode_len>.<opcode>,...
    // So it's "7.dispose,1.0;"
    assert_eq!(instr, "7.dispose,1.0;");
}

#[test]
fn test_format_move() {
    let instr = format_move(1, -1, 10, 20, 0);
    assert_eq!(instr, "4.move,1.1,2.-1,2.10,2.20,1.0;");
}

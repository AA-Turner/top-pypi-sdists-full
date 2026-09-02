use crate::format_instruction;

#[test]
fn test_format_instruction() {
    let instr = format_instruction("key", &["65507", "1"]);
    assert_eq!(instr, "3.key,5.65507,1.1;");
}

#[test]
fn test_format_instruction_empty_args() {
    let instr = format_instruction("sync", &[]);
    assert_eq!(instr, "4.sync;");
}

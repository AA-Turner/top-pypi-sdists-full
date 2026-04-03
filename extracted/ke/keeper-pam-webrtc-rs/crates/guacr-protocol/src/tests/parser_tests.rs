use crate::parser::{GuacamoleParser, ParseError};
use bytes::Bytes;

#[test]
fn test_parse_key_instruction() {
    let data = Bytes::from("3.key,5.65507,1.1;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "key");
    assert_eq!(instr.args, vec!["65507", "1"]);
}

#[test]
fn test_parse_mouse_instruction() {
    let data = Bytes::from("5.mouse,1.0,2.10,2.20,1.1;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "mouse");
    assert_eq!(instr.args, vec!["0", "10", "20", "1"]);
}

#[test]
fn test_parse_img_instruction() {
    let data = Bytes::from("3.img,1.1,1.7,1.0,10.image/jpeg,2.10,2.20;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "img");
    assert_eq!(instr.args.len(), 6);
    assert_eq!(instr.args[3], "image/jpeg");
}

#[test]
fn test_parse_multiple_instructions() {
    let data = Bytes::from("3.key,5.65507,1.1;4.sync,10.1234567890;");
    let instructions = GuacamoleParser::parse_instructions(&data).unwrap();

    assert_eq!(instructions.len(), 2);
    assert_eq!(instructions[0].opcode, "key");
    assert_eq!(instructions[1].opcode, "sync");
}

#[test]
fn test_parse_error_missing_semicolon() {
    let data = Bytes::from("3.key,5.65507,1.1");
    let result = GuacamoleParser::parse_instruction(&data);

    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), ParseError::MissingTerminator);
}

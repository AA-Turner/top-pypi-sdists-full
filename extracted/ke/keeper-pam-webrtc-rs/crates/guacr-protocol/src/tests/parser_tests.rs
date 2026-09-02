use crate::format_instruction;
use crate::parser::{GuacamoleParser, ParseError};
use bytes::Bytes;

// --- T-002: Multi-byte UTF-8 instruction parsing tests ---

#[test]
fn test_parse_multibyte_utf8_value() {
    // "☺" is U+263A, encoded as 3 bytes in UTF-8.
    // LENGTH=3 means 3 codepoints (9 bytes). The parser must extract exactly 3 codepoints.
    let data = Bytes::from("3.☺☺☺;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();
    assert_eq!(instr.opcode, "☺☺☺");
    assert_eq!(instr.opcode.chars().count(), 3);
}

#[test]
fn test_parse_multibyte_utf8_with_ascii_arg() {
    // Instruction: opcode = "☺☺☺" (3 codepoints, 9 bytes), arg = "ok" (2 codepoints)
    // Wire: "3.☺☺☺,2.ok;"
    let data = Bytes::from("3.\u{263A}\u{263A}\u{263A},2.ok;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();
    assert_eq!(instr.opcode.chars().count(), 3);
    assert_eq!(instr.args, vec!["ok"]);
}

#[test]
fn test_parse_multibyte_sequence_boundary() {
    // Two consecutive instructions. First has multi-byte value. Second must parse correctly.
    // "3.☺☺☺;" followed by "3.key;"
    let raw = "3.\u{263A}\u{263A}\u{263A};3.key;".to_string();
    let data = Bytes::from(raw.as_bytes().to_vec());
    let instrs = GuacamoleParser::parse_instructions(&data).unwrap();
    assert_eq!(instrs.len(), 2);
    assert_eq!(instrs[0].opcode.chars().count(), 3);
    assert_eq!(instrs[1].opcode, "key");
}

#[test]
fn test_parse_length_codepoints_not_bytes_ascii_unchanged() {
    // AC-5: ASCII instructions must continue to work exactly as before.
    let data = Bytes::from("3.key,5.65507,1.1;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();
    assert_eq!(instr.opcode, "key");
    assert_eq!(instr.args, vec!["65507", "1"]);
}

#[test]
fn test_parse_length_byte_mismatch_produces_correct_value() {
    // AC-2: byte-count ≠ codepoint-count must not produce different parse results.
    // "é" is U+00E9, 2 bytes in UTF-8. LENGTH=1 means 1 codepoint (2 bytes).
    // Old byte-based code would read only 1 byte ("e" part, 0xC3), truncating the char.
    // New codepoint-based code reads the full "é".
    let data = Bytes::from("1.\u{00e9};");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();
    assert_eq!(instr.opcode, "\u{00e9}");
    assert_eq!(instr.opcode.chars().count(), 1);
}

#[test]
fn test_parse_length_too_short_is_error() {
    // AC-3: LENGTH that would require mid-character byte slice → parse error.
    // "☺" is 3 bytes (1 codepoint). Specifying LENGTH=2 when only 1 codepoint
    // "☺" exists before the semicolon must produce an error.
    // Wire: "2.☺;" — length claims 2 codepoints but only 1 is present.
    let data = Bytes::from("2.\u{263A};");
    let result = GuacamoleParser::parse_instruction(&data);
    assert!(
        result.is_err(),
        "expected error for too-short codepoint count"
    );
}

#[test]
fn test_parse_multibyte_two_instructions_boundary() {
    // AC-4: After parsing multi-byte first value, second instruction boundary correct.
    // "1.é,2.ok;" — opcode is "é" (U+00E9, 2 bytes, 1 codepoint), arg "ok"
    let data = Bytes::from("1.\u{00e9},2.ok;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();
    assert_eq!(instr.opcode, "\u{00e9}");
    assert_eq!(instr.args, vec!["ok"]);
}

// --- End T-002 tests ---

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

// ---------------------------------------------------------------------------
// Element lengths are CHARACTER counts, not byte counts.
//
// Regression guards: this parser previously byte-sliced by the declared length,
// which panicked ("byte index N is not a char boundary") on any multi-byte
// value, and pre-scanned for `;` / split on `,`, which mangled values that
// legitimately contain either. Guacamole carries clipboard text, filenames and
// usernames, so all of these are reachable from ordinary user input.

#[test]
fn test_parse_accented_arg() {
    // "café" is 4 chars / 5 bytes.
    let data = Bytes::from("9.clipboard,4.café;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "clipboard");
    assert_eq!(instr.args, vec!["café"]);
}

#[test]
fn test_parse_emoji_arg() {
    // "hi 👋" is 4 chars / 7 bytes (the emoji is a 4-byte sequence).
    let data = Bytes::from("9.clipboard,4.hi 👋;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.args, vec!["hi 👋"]);
}

#[test]
fn test_parse_cjk_arg() {
    // Each of these is 3 bytes; 4 chars / 12 bytes total.
    let data = Bytes::from("4.name,4.国隊科学;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "name");
    assert_eq!(instr.args, vec!["国隊科学"]);
}

#[test]
fn test_parse_multibyte_opcode() {
    let data = Bytes::from("4.café,1.x;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "café");
    assert_eq!(instr.args, vec!["x"]);
}

#[test]
fn test_parse_semicolon_inside_arg() {
    // The terminator must come from the declared length, not the first `;` byte.
    let data = Bytes::from("9.clipboard,3.a;b;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.args, vec!["a;b"]);
}

#[test]
fn test_parse_comma_inside_arg() {
    let data = Bytes::from("9.clipboard,3.a,b;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.args, vec!["a,b"]);
}

#[test]
fn test_parse_multiple_instructions_with_multibyte() {
    let data = Bytes::from("4.name,4.café;4.sync,4.1234;");
    let instructions = GuacamoleParser::parse_instructions(&data).unwrap();

    assert_eq!(instructions.len(), 2);
    assert_eq!(instructions[0].args, vec!["café"]);
    assert_eq!(instructions[1].opcode, "sync");
    assert_eq!(instructions[1].args, vec!["1234"]);
}

#[test]
fn test_parse_multiple_instructions_with_semicolon_inside_arg() {
    // A `;` inside the first value must not be mistaken for its terminator.
    let data = Bytes::from("9.clipboard,3.a;b;4.sync,1.1;");
    let instructions = GuacamoleParser::parse_instructions(&data).unwrap();

    assert_eq!(instructions.len(), 2);
    assert_eq!(instructions[0].args, vec!["a;b"]);
    assert_eq!(instructions[1].opcode, "sync");
}

// ---------------------------------------------------------------------------
// Truncated vs. malformed.
//
// Because `;` is a legal character *inside* a value, a value shorter than its
// declared length is not evidence of corruption — the remaining characters may
// simply not have arrived. Validity is decided only once the declared count is
// satisfied, by the byte that follows it: `,`, `;`, or malformed.

#[test]
fn test_declared_length_not_yet_satisfied_is_truncation_not_corruption() {
    // 9 chars declared; "abc;" supplies only 4 — and that `;` is data, not the
    // terminator. Five more characters could still complete this value, so the
    // parser must report truncation rather than rejecting the instruction.
    let data = Bytes::from("4.name,9.abc;");
    assert_eq!(
        GuacamoleParser::parse_instruction(&data).unwrap_err(),
        ParseError::MissingTerminator
    );
}

#[test]
fn test_semicolon_inside_value_is_consumed_as_data() {
    // The same value, now complete: "abc;defgh" is 9 chars, so the parser must
    // read straight past the interior `;` and terminate on the one after it.
    let data = Bytes::from("4.name,9.abc;defgh;");
    let instr = GuacamoleParser::parse_instruction(&data).unwrap();

    assert_eq!(instr.opcode, "name");
    assert_eq!(instr.args, vec!["abc;defgh"]);
}

#[test]
fn test_satisfied_length_followed_by_junk_is_malformed() {
    // "abc;defgh" satisfies the declared 9 chars, but the next byte is neither
    // `,` nor `;`. *Now* the instruction is genuinely invalid.
    let data = Bytes::from("4.name,9.abc;defghX;");
    assert_eq!(
        GuacamoleParser::parse_instruction(&data).unwrap_err(),
        ParseError::InvalidFormat
    );
}

#[test]
fn test_non_numeric_length_is_malformed() {
    // A length field that is not a number is unrecoverable — no continuation can
    // rescue it — so it reports as `InvalidFormat`. (`ParseError::InvalidLength`
    // is no longer produced; see its doc comment.)
    let data = Bytes::from("4.name,x.abc;");
    assert_eq!(
        GuacamoleParser::parse_instruction(&data).unwrap_err(),
        ParseError::InvalidFormat
    );
}

/// Ties the encoder to the parser: `format_instruction` writes `chars().count()`,
/// so the parser must read it back the same way. This is the guard that keeps the
/// two halves from drifting apart again — it fails if either side switches to
/// byte counting.
#[test]
fn test_format_instruction_roundtrips_through_parser() {
    let cases: &[(&str, &[&str])] = &[
        ("key", &["65507", "1"]),
        ("clipboard", &["café français naïve"]),
        ("name", &["国隊・科学"]),
        ("text", &["Hello 世界 🌍 café!"]),
        ("user", &["Müller"]),
        ("clipboard", &["semi;colon"]),
        ("clipboard", &["comma,separated"]),
        ("clipboard", &["mixed; é, 🌍"]),
        ("empty", &[""]),
        ("noargs", &[]),
    ];

    for (opcode, args) in cases {
        let wire = format_instruction(opcode, args);
        let bytes = Bytes::from(wire.clone());
        let instr = GuacamoleParser::parse_instruction(&bytes)
            .unwrap_or_else(|e| panic!("failed to parse {wire:?}: {e}"));

        assert_eq!(instr.opcode, *opcode, "opcode mismatch for {wire:?}");
        assert_eq!(instr.args, args.to_vec(), "args mismatch for {wire:?}");
    }
}
/// A declared length far exceeding the actual data must be rejected quickly,
/// not cause the parser to loop billions of times consuming CPU.
/// Before the fix, a length like 9999999 with 3 bytes of data would loop
/// 9999999 times before returning InvalidLength.
#[test]
fn test_parse_huge_length_rejected_immediately() {
    // Declared length is 100 million — actual value is only "abc" (3 codepoints).
    // After the fix, this returns InvalidLength without iterating 100M times.
    let data = bytes::Bytes::from("100000000.abc;");
    let result = GuacamoleParser::parse_instruction(&data);
    assert!(
        result.is_err(),
        "huge declared length must return an error, not loop indefinitely"
    );
}

/// A length value that overflows usize must return an error, not panic.
#[test]
fn test_parse_length_overflow_returns_error() {
    // Larger than usize::MAX on 32-bit, and larger than any reasonable limit.
    let data = bytes::Bytes::from("99999999999999999999.abc;");
    let result = GuacamoleParser::parse_instruction(&data);
    assert!(
        result.is_err(),
        "usize-overflowing length must return an error"
    );
}

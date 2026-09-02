// Security tests — CVE-2023-30575 audit: Guacamole LENGTH field must count
// Unicode codepoints, not UTF-8 bytes.
//
// Wire format: `LENGTH.VALUE` where LENGTH is the number of Unicode codepoints
// in VALUE. For ASCII content, byte count == codepoint count. For any non-ASCII
// content (clipboard data, pipe names, page titles, etc.) they diverge.
//
// Run with:
//   cargo test -p guacr-protocol --test security_test -- --include-ignored

// All tests in security_test.rs MUST have #[ignore] per testing.md.

use guacr_protocol::format_blob;

// Helper: parse the length prefix from a Guacamole element "LENGTH.VALUE"
// Returns the parsed integer or panics.
fn parse_guac_length(field: &str) -> usize {
    let dot = field.find('.').expect("no dot in guacamole element");
    field[..dot]
        .parse()
        .expect("length prefix is not an integer")
}

// Helper: extract argument at index `n` (0-based) from a Guacamole instruction.
// Instruction format: OPLEN.OPCODE,ARG0LEN.ARG0,ARG1LEN.ARG1,...;
#[allow(dead_code)]
fn extract_arg(instruction: &str, n: usize) -> &str {
    // Strip trailing semicolon.
    let body = instruction.trim_end_matches(';');
    // Split on commas that separate elements.
    // Each element is "LEN.VALUE".  We split on ',' to get elements then find '.'
    // to separate length from value.
    let parts: Vec<&str> = body.splitn(n + 3, ',').collect();
    // parts[0] = "OPLEN.OPCODE", parts[1] = first arg, parts[n+1] = nth arg
    let element = parts[n + 1];
    let dot = element.find('.').expect("no dot in element");
    &element[dot + 1..]
}

// Helper: extract the length prefix of argument `n` from a Guacamole instruction.
fn extract_arg_len(instruction: &str, n: usize) -> usize {
    let body = instruction.trim_end_matches(';');
    let parts: Vec<&str> = body.splitn(n + 3, ',').collect();
    let element = parts[n + 1];
    parse_guac_length(element)
}

// ---------------------------------------------------------------------------
// Bug 1: format_blob in streams.rs uses .len() (bytes) instead of
// .chars().count() (codepoints) for the data field.
//
// Proof: "héllo" has 5 codepoints but 6 UTF-8 bytes. The LENGTH field must
// be 5, not 6. Before the fix this test fails because the LENGTH is 6.
// ---------------------------------------------------------------------------

/// format_blob data LENGTH must be codepoint count, not byte count.
///
/// "héllo" = 5 Unicode codepoints, 6 UTF-8 bytes.
/// Correct wire format: `4.blob,1.0,5.héllo;`
/// Buggy wire format:   `4.blob,1.0,6.héllo;`
///
/// This test fails before the fix and passes after.
#[test]
#[ignore]
fn format_blob_data_length_is_codepoints_not_bytes() {
    let data = "héllo"; // 5 codepoints, 6 UTF-8 bytes
    let instr = format_blob(0, data);

    // The second argument (index 1) carries the data.
    let data_len = extract_arg_len(&instr, 1);

    assert_eq!(
        data_len,
        data.chars().count(),
        "format_blob LENGTH field must count Unicode codepoints ({}) not bytes ({}). \
         Instruction was: {}",
        data.chars().count(),
        data.len(),
        instr
    );
}

/// format_blob with Japanese text (3-byte codepoints)
///
/// "日本語" = 3 codepoints, 9 UTF-8 bytes.
/// Correct LENGTH: 3. Buggy LENGTH: 9.
#[test]
#[ignore]
fn format_blob_japanese_length_is_codepoints() {
    let data = "日本語"; // 3 codepoints, 9 UTF-8 bytes
    let instr = format_blob(0, data);

    let data_len = extract_arg_len(&instr, 1);

    assert_eq!(
        data_len,
        data.chars().count(),
        "format_blob LENGTH must be 3 (codepoints), not 9 (bytes). Instruction: {}",
        instr
    );
}

/// The parser must accept the instruction produced by format_blob.
///
/// If the LENGTH field is byte count instead of codepoint count, the parser
/// will fail to parse the resulting instruction (the length fields won't match
/// the actual content boundaries after fix).
#[test]
#[ignore]
fn format_blob_unicode_roundtrip_parses() {
    use bytes::Bytes;
    use guacr_protocol::GuacamoleParser;

    let data = "héllo"; // 5 codepoints, 6 UTF-8 bytes
    let instr = format_blob(0, data);

    let bytes = Bytes::from(instr.clone());
    let parsed = GuacamoleParser::parse_instruction(&bytes)
        .expect("format_blob output must be parseable by GuacamoleParser");

    assert_eq!(
        parsed.opcode, "blob",
        "opcode must be 'blob', got: {}",
        parsed.opcode
    );
    assert_eq!(
        parsed.args.get(1),
        Some(&data),
        "parsed data arg must equal original data '{}'. Instruction: {}",
        data,
        instr
    );
}

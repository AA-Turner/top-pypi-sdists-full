use crate::ebcdic::{decode_string, ebcdic_to_unicode, encode_string, unicode_to_ebcdic, CodePage};

// --- CP 037: Basic character mappings ---

#[test]
fn test_space_all_code_pages() {
    assert_eq!(ebcdic_to_unicode(0x40, CodePage::Cp037), ' ');
    assert_eq!(ebcdic_to_unicode(0x40, CodePage::Cp500), ' ');
    assert_eq!(ebcdic_to_unicode(0x40, CodePage::Cp1047), ' ');
}

#[test]
fn test_uppercase_a_through_i_037() {
    for (i, expected) in ('A'..='I').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0xC1 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0xC1 + i as u8,
            expected
        );
    }
}

#[test]
fn test_uppercase_j_through_r_037() {
    for (i, expected) in ('J'..='R').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0xD1 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0xD1 + i as u8,
            expected
        );
    }
}

#[test]
fn test_uppercase_s_through_z_037() {
    for (i, expected) in ('S'..='Z').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0xE2 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0xE2 + i as u8,
            expected
        );
    }
}

#[test]
fn test_lowercase_a_through_i_037() {
    for (i, expected) in ('a'..='i').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0x81 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0x81 + i as u8,
            expected
        );
    }
}

#[test]
fn test_lowercase_j_through_r_037() {
    for (i, expected) in ('j'..='r').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0x91 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0x91 + i as u8,
            expected
        );
    }
}

#[test]
fn test_lowercase_s_through_z_037() {
    for (i, expected) in ('s'..='z').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0xA2 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0xA2 + i as u8,
            expected
        );
    }
}

#[test]
fn test_digits_037() {
    for (i, expected) in ('0'..='9').enumerate() {
        assert_eq!(
            ebcdic_to_unicode(0xF0 + i as u8, CodePage::Cp037),
            expected,
            "EBCDIC 0x{:02X} should be '{}'",
            0xF0 + i as u8,
            expected
        );
    }
}

#[test]
fn test_common_punctuation_037() {
    assert_eq!(ebcdic_to_unicode(0x4B, CodePage::Cp037), '.');
    assert_eq!(ebcdic_to_unicode(0x4C, CodePage::Cp037), '<');
    assert_eq!(ebcdic_to_unicode(0x4D, CodePage::Cp037), '(');
    assert_eq!(ebcdic_to_unicode(0x4E, CodePage::Cp037), '+');
    assert_eq!(ebcdic_to_unicode(0x50, CodePage::Cp037), '&');
    assert_eq!(ebcdic_to_unicode(0x5A, CodePage::Cp037), '!');
    assert_eq!(ebcdic_to_unicode(0x5B, CodePage::Cp037), '$');
    assert_eq!(ebcdic_to_unicode(0x5C, CodePage::Cp037), '*');
    assert_eq!(ebcdic_to_unicode(0x5D, CodePage::Cp037), ')');
    assert_eq!(ebcdic_to_unicode(0x5E, CodePage::Cp037), ';');
    assert_eq!(ebcdic_to_unicode(0x60, CodePage::Cp037), '-');
    assert_eq!(ebcdic_to_unicode(0x61, CodePage::Cp037), '/');
    assert_eq!(ebcdic_to_unicode(0x6B, CodePage::Cp037), ',');
    assert_eq!(ebcdic_to_unicode(0x6C, CodePage::Cp037), '%');
    assert_eq!(ebcdic_to_unicode(0x6D, CodePage::Cp037), '_');
    assert_eq!(ebcdic_to_unicode(0x6E, CodePage::Cp037), '>');
    assert_eq!(ebcdic_to_unicode(0x6F, CodePage::Cp037), '?');
    assert_eq!(ebcdic_to_unicode(0x7A, CodePage::Cp037), ':');
    assert_eq!(ebcdic_to_unicode(0x7B, CodePage::Cp037), '#');
    assert_eq!(ebcdic_to_unicode(0x7C, CodePage::Cp037), '@');
    assert_eq!(ebcdic_to_unicode(0x7D, CodePage::Cp037), '\'');
    assert_eq!(ebcdic_to_unicode(0x7E, CodePage::Cp037), '=');
    assert_eq!(ebcdic_to_unicode(0x7F, CodePage::Cp037), '"');
}

#[test]
fn test_braces_and_brackets_037() {
    assert_eq!(ebcdic_to_unicode(0xC0, CodePage::Cp037), '{');
    assert_eq!(ebcdic_to_unicode(0xD0, CodePage::Cp037), '}');
    assert_eq!(ebcdic_to_unicode(0xBA, CodePage::Cp037), '[');
    assert_eq!(ebcdic_to_unicode(0xBB, CodePage::Cp037), ']');
    assert_eq!(ebcdic_to_unicode(0xE0, CodePage::Cp037), '\\');
    assert_eq!(ebcdic_to_unicode(0x4F, CodePage::Cp037), '|');
    assert_eq!(ebcdic_to_unicode(0xB0, CodePage::Cp037), '^');
    assert_eq!(ebcdic_to_unicode(0xA1, CodePage::Cp037), '~');
}

// --- Round-trip tests for all code pages ---

#[test]
fn test_roundtrip_printable_ascii_cp037() {
    for ch in ' '..='~' {
        let ebcdic = unicode_to_ebcdic(ch, CodePage::Cp037);
        assert!(
            ebcdic.is_some(),
            "'{}' (U+{:04X}) has no EBCDIC mapping in CP 037",
            ch,
            ch as u32
        );
        let back = ebcdic_to_unicode(ebcdic.unwrap(), CodePage::Cp037);
        assert_eq!(
            back,
            ch,
            "Round-trip failed for '{}' via 0x{:02X}",
            ch,
            ebcdic.unwrap()
        );
    }
}

#[test]
fn test_roundtrip_printable_ascii_cp500() {
    for ch in ' '..='~' {
        let ebcdic = unicode_to_ebcdic(ch, CodePage::Cp500);
        assert!(
            ebcdic.is_some(),
            "'{}' (U+{:04X}) has no EBCDIC mapping in CP 500",
            ch,
            ch as u32
        );
        let back = ebcdic_to_unicode(ebcdic.unwrap(), CodePage::Cp500);
        assert_eq!(
            back,
            ch,
            "Round-trip failed for '{}' via 0x{:02X}",
            ch,
            ebcdic.unwrap()
        );
    }
}

#[test]
fn test_roundtrip_printable_ascii_cp1047() {
    for ch in ' '..='~' {
        let ebcdic = unicode_to_ebcdic(ch, CodePage::Cp1047);
        assert!(
            ebcdic.is_some(),
            "'{}' (U+{:04X}) has no EBCDIC mapping in CP 1047",
            ch,
            ch as u32
        );
        let back = ebcdic_to_unicode(ebcdic.unwrap(), CodePage::Cp1047);
        assert_eq!(
            back,
            ch,
            "Round-trip failed for '{}' via 0x{:02X}",
            ch,
            ebcdic.unwrap()
        );
    }
}

// --- String encoding/decoding tests ---

#[test]
fn test_decode_string_hello_upper() {
    let ebcdic = [0xC8, 0xC5, 0xD3, 0xD3, 0xD6];
    assert_eq!(decode_string(&ebcdic, CodePage::Cp037), "HELLO");
}

#[test]
fn test_decode_string_hello_lower() {
    let ebcdic = [0x88, 0x85, 0x93, 0x93, 0x96];
    assert_eq!(decode_string(&ebcdic, CodePage::Cp037), "hello");
}

#[test]
fn test_decode_string_digits() {
    let ebcdic = [0xF1, 0xF2, 0xF3, 0xF4, 0xF5];
    assert_eq!(decode_string(&ebcdic, CodePage::Cp037), "12345");
}

#[test]
fn test_decode_string_tso() {
    // "TSO" = T(0xE3) S(0xE2) O(0xD6)
    let ebcdic = [0xE3, 0xE2, 0xD6];
    assert_eq!(decode_string(&ebcdic, CodePage::Cp037), "TSO");
}

#[test]
fn test_encode_string_hello() {
    let encoded = encode_string("HELLO", CodePage::Cp037);
    assert_eq!(encoded, vec![0xC8, 0xC5, 0xD3, 0xD3, 0xD6]);
}

#[test]
fn test_encode_string_digits() {
    let encoded = encode_string("12345", CodePage::Cp037);
    assert_eq!(encoded, vec![0xF1, 0xF2, 0xF3, 0xF4, 0xF5]);
}

#[test]
fn test_encode_decode_roundtrip_string() {
    let original = "Hello, World! 123 @#$";
    let encoded = encode_string(original, CodePage::Cp037);
    let decoded = decode_string(&encoded, CodePage::Cp037);
    assert_eq!(decoded, original);
}

#[test]
fn test_encode_mixed_case() {
    let original = "AbCdEf";
    let encoded = encode_string(original, CodePage::Cp037);
    let decoded = decode_string(&encoded, CodePage::Cp037);
    assert_eq!(decoded, original);
}

#[test]
fn test_encode_unmappable_character() {
    // CJK character has no EBCDIC mapping, should become 0x3F (SUB)
    let encoded = encode_string("\u{4E2D}", CodePage::Cp037);
    assert_eq!(encoded, vec![0x3F]);
}

#[test]
fn test_empty_string() {
    assert_eq!(decode_string(&[], CodePage::Cp037), "");
    assert_eq!(encode_string("", CodePage::Cp037), Vec::<u8>::new());
}

// --- Cross-code-page difference tests ---

#[test]
fn test_cp500_bracket_positions() {
    // CP 500 has [ at 0x4A, ] at 0x5A
    assert_eq!(ebcdic_to_unicode(0x4A, CodePage::Cp500), '[');
    assert_eq!(ebcdic_to_unicode(0x5A, CodePage::Cp500), ']');
    // CP 037 has cent-sign at 0x4A, ! at 0x5A
    assert_eq!(ebcdic_to_unicode(0x4A, CodePage::Cp037), '\u{00A2}');
    assert_eq!(ebcdic_to_unicode(0x5A, CodePage::Cp037), '!');
}

#[test]
fn test_cp500_exclamation_position() {
    // CP 500 has ! at 0x4F (where CP 037 has |)
    assert_eq!(ebcdic_to_unicode(0x4F, CodePage::Cp500), '!');
    assert_eq!(ebcdic_to_unicode(0x4F, CodePage::Cp037), '|');
}

#[test]
fn test_cp500_caret_position() {
    // CP 500 has ^ at 0x5F (where CP 037 has not-sign)
    assert_eq!(ebcdic_to_unicode(0x5F, CodePage::Cp500), '^');
    assert_eq!(ebcdic_to_unicode(0x5F, CodePage::Cp037), '\u{00AC}');
}

#[test]
fn test_cp1047_newline_position() {
    // CP 1047 has LF (0x0A) at position 0x15 (Unix newline)
    assert_eq!(ebcdic_to_unicode(0x15, CodePage::Cp1047), '\u{000A}');
    // CP 037 has NEL (0x85) at position 0x15
    assert_eq!(ebcdic_to_unicode(0x15, CodePage::Cp037), '\u{0085}');
}

#[test]
fn test_cp1047_bracket_positions() {
    // CP 1047 has [ at 0xAD, ] at 0xBD
    assert_eq!(ebcdic_to_unicode(0xAD, CodePage::Cp1047), '[');
    assert_eq!(ebcdic_to_unicode(0xBD, CodePage::Cp1047), ']');
    // CP 037 has soft-hyphen at 0xAD (via 0xCA offset area)
    assert_eq!(ebcdic_to_unicode(0xAD, CodePage::Cp037), '\u{00DD}');
}

#[test]
fn test_cp1047_caret_position() {
    // CP 1047 has ^ at 0x5F
    assert_eq!(ebcdic_to_unicode(0x5F, CodePage::Cp1047), '^');
}

// --- Table completeness tests ---

#[test]
fn test_all_tables_fully_populated() {
    // Every byte value should produce a valid char (no panics)
    for byte in 0..=255u8 {
        let _ = ebcdic_to_unicode(byte, CodePage::Cp037);
        let _ = ebcdic_to_unicode(byte, CodePage::Cp500);
        let _ = ebcdic_to_unicode(byte, CodePage::Cp1047);
    }
}

#[test]
fn test_unicode_to_ebcdic_not_found() {
    assert_eq!(unicode_to_ebcdic('\u{1F600}', CodePage::Cp037), None);
    assert_eq!(unicode_to_ebcdic('\u{4E00}', CodePage::Cp500), None);
}

// --- Digits are the same across all code pages ---

#[test]
fn test_digits_same_across_code_pages() {
    for i in 0..10u8 {
        let expected = char::from(b'0' + i);
        let byte = 0xF0 + i;
        assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp037), expected);
        assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp500), expected);
        assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp1047), expected);
    }
}

// --- Letters are the same across all code pages ---

#[test]
fn test_uppercase_letters_same_across_code_pages() {
    let ranges: &[(u8, u8, char)] = &[
        (0xC1, 0xC9, 'A'), // A-I
        (0xD1, 0xD9, 'J'), // J-R
        (0xE2, 0xE9, 'S'), // S-Z
    ];
    for &(start, end, first_char) in ranges {
        for offset in 0..=(end - start) {
            let expected = char::from(first_char as u8 + offset);
            let byte = start + offset;
            assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp037), expected);
            assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp500), expected);
            assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp1047), expected);
        }
    }
}

#[test]
fn test_lowercase_letters_same_across_code_pages() {
    let ranges: &[(u8, u8, char)] = &[
        (0x81, 0x89, 'a'), // a-i
        (0x91, 0x99, 'j'), // j-r
        (0xA2, 0xA9, 's'), // s-z
    ];
    for &(start, end, first_char) in ranges {
        for offset in 0..=(end - start) {
            let expected = char::from(first_char as u8 + offset);
            let byte = start + offset;
            assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp037), expected);
            assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp500), expected);
            assert_eq!(ebcdic_to_unicode(byte, CodePage::Cp1047), expected);
        }
    }
}

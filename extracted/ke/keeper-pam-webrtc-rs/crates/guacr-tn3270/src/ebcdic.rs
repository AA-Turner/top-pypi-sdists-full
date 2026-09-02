//! EBCDIC codec for TN3270 mainframe terminal access.
//!
//! Provides conversion between EBCDIC byte sequences and Unicode characters
//! for the three most common code pages used in TN3270 environments:
//!
//! - CP 037: US/Canada (most common for TN3270)
//! - CP 500: International (CECP for Latin-1 countries)
//! - CP 1047: Unix on z/OS (Open Systems)
//!
//! All lookup tables are derived from IBM's character set references.

/// Supported EBCDIC code pages.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CodePage {
    /// US/Canada - the most common code page for TN3270 sessions.
    Cp037,
    /// International (CECP) - used in Latin-1 countries.
    Cp500,
    /// Unix on z/OS - used by Open Systems on IBM mainframes.
    Cp1047,
}

/// EBCDIC space character (0x40 in all supported code pages).
pub const EBCDIC_SPACE: u8 = 0x40;

/// EBCDIC null character (0x00 in all supported code pages).
pub const EBCDIC_NULL: u8 = 0x00;

/// EBCDIC to Unicode lookup table for Code Page 037 (US/Canada).
///
/// Each index corresponds to an EBCDIC byte value; the value at that index
/// is the corresponding Unicode character. Derived from IBM character data
/// tables for CCSID 037.
#[rustfmt::skip]
pub const EBCDIC_TO_UNICODE_037: [char; 256] = [
    // 0x00-0x0F
    '\u{0000}', '\u{0001}', '\u{0002}', '\u{0003}', '\u{009C}', '\u{0009}', '\u{0086}', '\u{007F}',
    '\u{0097}', '\u{008D}', '\u{008E}', '\u{000B}', '\u{000C}', '\u{000D}', '\u{000E}', '\u{000F}',
    // 0x10-0x1F
    '\u{0010}', '\u{0011}', '\u{0012}', '\u{0013}', '\u{009D}', '\u{0085}', '\u{0008}', '\u{0087}',
    '\u{0018}', '\u{0019}', '\u{0092}', '\u{008F}', '\u{001C}', '\u{001D}', '\u{001E}', '\u{001F}',
    // 0x20-0x2F
    '\u{0080}', '\u{0081}', '\u{0082}', '\u{0083}', '\u{0084}', '\u{000A}', '\u{0017}', '\u{001B}',
    '\u{0088}', '\u{0089}', '\u{008A}', '\u{008B}', '\u{008C}', '\u{0005}', '\u{0006}', '\u{0007}',
    // 0x30-0x3F
    '\u{0090}', '\u{0091}', '\u{0016}', '\u{0093}', '\u{0094}', '\u{0095}', '\u{0096}', '\u{0004}',
    '\u{0098}', '\u{0099}', '\u{009A}', '\u{009B}', '\u{0014}', '\u{0015}', '\u{009E}', '\u{001A}',
    // 0x40-0x4F
    '\u{0020}', '\u{00A0}', '\u{00E2}', '\u{00E4}', '\u{00E0}', '\u{00E1}', '\u{00E3}', '\u{00E5}',
    '\u{00E7}', '\u{00F1}', '\u{00A2}', '\u{002E}', '\u{003C}', '\u{0028}', '\u{002B}', '\u{007C}',
    // 0x50-0x5F
    '\u{0026}', '\u{00E9}', '\u{00EA}', '\u{00EB}', '\u{00E8}', '\u{00ED}', '\u{00EE}', '\u{00EF}',
    '\u{00EC}', '\u{00DF}', '\u{0021}', '\u{0024}', '\u{002A}', '\u{0029}', '\u{003B}', '\u{00AC}',
    // 0x60-0x6F
    '\u{002D}', '\u{002F}', '\u{00C2}', '\u{00C4}', '\u{00C0}', '\u{00C1}', '\u{00C3}', '\u{00C5}',
    '\u{00C7}', '\u{00D1}', '\u{00A6}', '\u{002C}', '\u{0025}', '\u{005F}', '\u{003E}', '\u{003F}',
    // 0x70-0x7F
    '\u{00F8}', '\u{00C9}', '\u{00CA}', '\u{00CB}', '\u{00C8}', '\u{00CD}', '\u{00CE}', '\u{00CF}',
    '\u{00CC}', '\u{0060}', '\u{003A}', '\u{0023}', '\u{0040}', '\u{0027}', '\u{003D}', '\u{0022}',
    // 0x80-0x8F
    '\u{00D8}', '\u{0061}', '\u{0062}', '\u{0063}', '\u{0064}', '\u{0065}', '\u{0066}', '\u{0067}',
    '\u{0068}', '\u{0069}', '\u{00AB}', '\u{00BB}', '\u{00F0}', '\u{00FD}', '\u{00FE}', '\u{00B1}',
    // 0x90-0x9F
    '\u{00B0}', '\u{006A}', '\u{006B}', '\u{006C}', '\u{006D}', '\u{006E}', '\u{006F}', '\u{0070}',
    '\u{0071}', '\u{0072}', '\u{00AA}', '\u{00BA}', '\u{00E6}', '\u{00B8}', '\u{00C6}', '\u{00A4}',
    // 0xA0-0xAF
    '\u{00B5}', '\u{007E}', '\u{0073}', '\u{0074}', '\u{0075}', '\u{0076}', '\u{0077}', '\u{0078}',
    '\u{0079}', '\u{007A}', '\u{00A1}', '\u{00BF}', '\u{00D0}', '\u{00DD}', '\u{00DE}', '\u{00AE}',
    // 0xB0-0xBF
    '\u{005E}', '\u{00A3}', '\u{00A5}', '\u{00B7}', '\u{00A9}', '\u{00A7}', '\u{00B6}', '\u{00BC}',
    '\u{00BD}', '\u{00BE}', '\u{005B}', '\u{005D}', '\u{00AF}', '\u{00A8}', '\u{00B4}', '\u{00D7}',
    // 0xC0-0xCF
    '\u{007B}', '\u{0041}', '\u{0042}', '\u{0043}', '\u{0044}', '\u{0045}', '\u{0046}', '\u{0047}',
    '\u{0048}', '\u{0049}', '\u{00AD}', '\u{00F4}', '\u{00F6}', '\u{00F2}', '\u{00F3}', '\u{00F5}',
    // 0xD0-0xDF
    '\u{007D}', '\u{004A}', '\u{004B}', '\u{004C}', '\u{004D}', '\u{004E}', '\u{004F}', '\u{0050}',
    '\u{0051}', '\u{0052}', '\u{00B9}', '\u{00FB}', '\u{00FC}', '\u{00F9}', '\u{00FA}', '\u{00FF}',
    // 0xE0-0xEF
    '\u{005C}', '\u{00F7}', '\u{0053}', '\u{0054}', '\u{0055}', '\u{0056}', '\u{0057}', '\u{0058}',
    '\u{0059}', '\u{005A}', '\u{00B2}', '\u{00D4}', '\u{00D6}', '\u{00D2}', '\u{00D3}', '\u{00D5}',
    // 0xF0-0xFF
    '\u{0030}', '\u{0031}', '\u{0032}', '\u{0033}', '\u{0034}', '\u{0035}', '\u{0036}', '\u{0037}',
    '\u{0038}', '\u{0039}', '\u{00B3}', '\u{00DB}', '\u{00DC}', '\u{00D9}', '\u{00DA}', '\u{009F}',
];

/// EBCDIC to Unicode lookup table for Code Page 500 (International).
///
/// CP 500 differs from CP 037 primarily in the positions of several
/// punctuation characters: brackets, exclamation, caret, tilde, braces,
/// backslash, pipe, cent sign, and not sign are rearranged.
#[rustfmt::skip]
pub const EBCDIC_TO_UNICODE_500: [char; 256] = [
    // 0x00-0x0F
    '\u{0000}', '\u{0001}', '\u{0002}', '\u{0003}', '\u{009C}', '\u{0009}', '\u{0086}', '\u{007F}',
    '\u{0097}', '\u{008D}', '\u{008E}', '\u{000B}', '\u{000C}', '\u{000D}', '\u{000E}', '\u{000F}',
    // 0x10-0x1F
    '\u{0010}', '\u{0011}', '\u{0012}', '\u{0013}', '\u{009D}', '\u{0085}', '\u{0008}', '\u{0087}',
    '\u{0018}', '\u{0019}', '\u{0092}', '\u{008F}', '\u{001C}', '\u{001D}', '\u{001E}', '\u{001F}',
    // 0x20-0x2F
    '\u{0080}', '\u{0081}', '\u{0082}', '\u{0083}', '\u{0084}', '\u{000A}', '\u{0017}', '\u{001B}',
    '\u{0088}', '\u{0089}', '\u{008A}', '\u{008B}', '\u{008C}', '\u{0005}', '\u{0006}', '\u{0007}',
    // 0x30-0x3F
    '\u{0090}', '\u{0091}', '\u{0016}', '\u{0093}', '\u{0094}', '\u{0095}', '\u{0096}', '\u{0004}',
    '\u{0098}', '\u{0099}', '\u{009A}', '\u{009B}', '\u{0014}', '\u{0015}', '\u{009E}', '\u{001A}',
    // 0x40-0x4F: differs at 0x4A ([ vs cent), 0x4F (! vs |)
    '\u{0020}', '\u{00A0}', '\u{00E2}', '\u{00E4}', '\u{00E0}', '\u{00E1}', '\u{00E3}', '\u{00E5}',
    '\u{00E7}', '\u{00F1}', '\u{005B}', '\u{002E}', '\u{003C}', '\u{0028}', '\u{002B}', '\u{0021}',
    // 0x50-0x5F: differs at 0x5A (] vs !), 0x5F (^ vs not-sign)
    '\u{0026}', '\u{00E9}', '\u{00EA}', '\u{00EB}', '\u{00E8}', '\u{00ED}', '\u{00EE}', '\u{00EF}',
    '\u{00EC}', '\u{00DF}', '\u{005D}', '\u{0024}', '\u{002A}', '\u{0029}', '\u{003B}', '\u{005E}',
    // 0x60-0x6F
    '\u{002D}', '\u{002F}', '\u{00C2}', '\u{00C4}', '\u{00C0}', '\u{00C1}', '\u{00C3}', '\u{00C5}',
    '\u{00C7}', '\u{00D1}', '\u{00A6}', '\u{002C}', '\u{0025}', '\u{005F}', '\u{003E}', '\u{003F}',
    // 0x70-0x7F
    '\u{00F8}', '\u{00C9}', '\u{00CA}', '\u{00CB}', '\u{00C8}', '\u{00CD}', '\u{00CE}', '\u{00CF}',
    '\u{00CC}', '\u{0060}', '\u{003A}', '\u{0023}', '\u{0040}', '\u{0027}', '\u{003D}', '\u{0022}',
    // 0x80-0x8F
    '\u{00D8}', '\u{0061}', '\u{0062}', '\u{0063}', '\u{0064}', '\u{0065}', '\u{0066}', '\u{0067}',
    '\u{0068}', '\u{0069}', '\u{00AB}', '\u{00BB}', '\u{00F0}', '\u{00FD}', '\u{00FE}', '\u{00B1}',
    // 0x90-0x9F
    '\u{00B0}', '\u{006A}', '\u{006B}', '\u{006C}', '\u{006D}', '\u{006E}', '\u{006F}', '\u{0070}',
    '\u{0071}', '\u{0072}', '\u{00AA}', '\u{00BA}', '\u{00E6}', '\u{00B8}', '\u{00C6}', '\u{00A4}',
    // 0xA0-0xAF
    '\u{00B5}', '\u{007E}', '\u{0073}', '\u{0074}', '\u{0075}', '\u{0076}', '\u{0077}', '\u{0078}',
    '\u{0079}', '\u{007A}', '\u{00A1}', '\u{00BF}', '\u{00D0}', '\u{00DD}', '\u{00DE}', '\u{00AE}',
    // 0xB0-0xBF: differs at 0xB0 (cent vs ^), 0xBA (not vs [), 0xBB (| vs ])
    '\u{00A2}', '\u{00A3}', '\u{00A5}', '\u{00B7}', '\u{00A9}', '\u{00A7}', '\u{00B6}', '\u{00BC}',
    '\u{00BD}', '\u{00BE}', '\u{00AC}', '\u{007C}', '\u{00AF}', '\u{00A8}', '\u{00B4}', '\u{00D7}',
    // 0xC0-0xCF
    '\u{007B}', '\u{0041}', '\u{0042}', '\u{0043}', '\u{0044}', '\u{0045}', '\u{0046}', '\u{0047}',
    '\u{0048}', '\u{0049}', '\u{00AD}', '\u{00F4}', '\u{00F6}', '\u{00F2}', '\u{00F3}', '\u{00F5}',
    // 0xD0-0xDF
    '\u{007D}', '\u{004A}', '\u{004B}', '\u{004C}', '\u{004D}', '\u{004E}', '\u{004F}', '\u{0050}',
    '\u{0051}', '\u{0052}', '\u{00B9}', '\u{00FB}', '\u{00FC}', '\u{00F9}', '\u{00FA}', '\u{00FF}',
    // 0xE0-0xEF
    '\u{005C}', '\u{00F7}', '\u{0053}', '\u{0054}', '\u{0055}', '\u{0056}', '\u{0057}', '\u{0058}',
    '\u{0059}', '\u{005A}', '\u{00B2}', '\u{00D4}', '\u{00D6}', '\u{00D2}', '\u{00D3}', '\u{00D5}',
    // 0xF0-0xFF
    '\u{0030}', '\u{0031}', '\u{0032}', '\u{0033}', '\u{0034}', '\u{0035}', '\u{0036}', '\u{0037}',
    '\u{0038}', '\u{0039}', '\u{00B3}', '\u{00DB}', '\u{00DC}', '\u{00D9}', '\u{00DA}', '\u{009F}',
];

/// EBCDIC to Unicode lookup table for Code Page 1047 (Unix on z/OS).
///
/// CP 1047 is designed for Unix environments on z/OS. Key differences from
/// CP 037: LF at 0x15 (instead of NEL), caret at 0x5F, brackets and other
/// punctuation repositioned to better support Unix conventions.
#[rustfmt::skip]
pub const EBCDIC_TO_UNICODE_1047: [char; 256] = [
    // 0x00-0x0F
    '\u{0000}', '\u{0001}', '\u{0002}', '\u{0003}', '\u{009C}', '\u{0009}', '\u{0086}', '\u{007F}',
    '\u{0097}', '\u{008D}', '\u{008E}', '\u{000B}', '\u{000C}', '\u{000D}', '\u{000E}', '\u{000F}',
    // 0x10-0x1F: 0x15 = LF (Unix newline) instead of NEL
    '\u{0010}', '\u{0011}', '\u{0012}', '\u{0013}', '\u{009D}', '\u{000A}', '\u{0008}', '\u{0087}',
    '\u{0018}', '\u{0019}', '\u{0092}', '\u{008F}', '\u{001C}', '\u{001D}', '\u{001E}', '\u{001F}',
    // 0x20-0x2F: 0x25 = NEL (moved from 0x15)
    '\u{0080}', '\u{0081}', '\u{0082}', '\u{0083}', '\u{0084}', '\u{0085}', '\u{0017}', '\u{001B}',
    '\u{0088}', '\u{0089}', '\u{008A}', '\u{008B}', '\u{008C}', '\u{0005}', '\u{0006}', '\u{0007}',
    // 0x30-0x3F
    '\u{0090}', '\u{0091}', '\u{0016}', '\u{0093}', '\u{0094}', '\u{0095}', '\u{0096}', '\u{0004}',
    '\u{0098}', '\u{0099}', '\u{009A}', '\u{009B}', '\u{0014}', '\u{0015}', '\u{009E}', '\u{001A}',
    // 0x40-0x4F
    '\u{0020}', '\u{00A0}', '\u{00E2}', '\u{00E4}', '\u{00E0}', '\u{00E1}', '\u{00E3}', '\u{00E5}',
    '\u{00E7}', '\u{00F1}', '\u{00A2}', '\u{002E}', '\u{003C}', '\u{0028}', '\u{002B}', '\u{007C}',
    // 0x50-0x5F: 0x5F = ^ (caret) instead of not-sign
    '\u{0026}', '\u{00E9}', '\u{00EA}', '\u{00EB}', '\u{00E8}', '\u{00ED}', '\u{00EE}', '\u{00EF}',
    '\u{00EC}', '\u{00DF}', '\u{0021}', '\u{0024}', '\u{002A}', '\u{0029}', '\u{003B}', '\u{005E}',
    // 0x60-0x6F
    '\u{002D}', '\u{002F}', '\u{00C2}', '\u{00C4}', '\u{00C0}', '\u{00C1}', '\u{00C3}', '\u{00C5}',
    '\u{00C7}', '\u{00D1}', '\u{00A6}', '\u{002C}', '\u{0025}', '\u{005F}', '\u{003E}', '\u{003F}',
    // 0x70-0x7F
    '\u{00F8}', '\u{00C9}', '\u{00CA}', '\u{00CB}', '\u{00C8}', '\u{00CD}', '\u{00CE}', '\u{00CF}',
    '\u{00CC}', '\u{0060}', '\u{003A}', '\u{0023}', '\u{0040}', '\u{0027}', '\u{003D}', '\u{0022}',
    // 0x80-0x8F
    '\u{00D8}', '\u{0061}', '\u{0062}', '\u{0063}', '\u{0064}', '\u{0065}', '\u{0066}', '\u{0067}',
    '\u{0068}', '\u{0069}', '\u{00AB}', '\u{00BB}', '\u{00F0}', '\u{00FD}', '\u{00FE}', '\u{00B1}',
    // 0x90-0x9F
    '\u{00B0}', '\u{006A}', '\u{006B}', '\u{006C}', '\u{006D}', '\u{006E}', '\u{006F}', '\u{0070}',
    '\u{0071}', '\u{0072}', '\u{00AA}', '\u{00BA}', '\u{00E6}', '\u{00B8}', '\u{00C6}', '\u{00A4}',
    // 0xA0-0xAF: 0xAD = [ (bracket), differs from CP 037
    '\u{00B5}', '\u{007E}', '\u{0073}', '\u{0074}', '\u{0075}', '\u{0076}', '\u{0077}', '\u{0078}',
    '\u{0079}', '\u{007A}', '\u{00A1}', '\u{00BF}', '\u{00D0}', '\u{005B}', '\u{00DE}', '\u{00AE}',
    // 0xB0-0xBF: 0xB0 = not-sign, 0xBA = Y-acute, 0xBD = ] (bracket)
    '\u{00AC}', '\u{00A3}', '\u{00A5}', '\u{00B7}', '\u{00A9}', '\u{00A7}', '\u{00B6}', '\u{00BC}',
    '\u{00BD}', '\u{00BE}', '\u{00DD}', '\u{00A8}', '\u{00AF}', '\u{005D}', '\u{00B4}', '\u{00D7}',
    // 0xC0-0xCF
    '\u{007B}', '\u{0041}', '\u{0042}', '\u{0043}', '\u{0044}', '\u{0045}', '\u{0046}', '\u{0047}',
    '\u{0048}', '\u{0049}', '\u{00AD}', '\u{00F4}', '\u{00F6}', '\u{00F2}', '\u{00F3}', '\u{00F5}',
    // 0xD0-0xDF
    '\u{007D}', '\u{004A}', '\u{004B}', '\u{004C}', '\u{004D}', '\u{004E}', '\u{004F}', '\u{0050}',
    '\u{0051}', '\u{0052}', '\u{00B9}', '\u{00FB}', '\u{00FC}', '\u{00F9}', '\u{00FA}', '\u{00FF}',
    // 0xE0-0xEF
    '\u{005C}', '\u{00F7}', '\u{0053}', '\u{0054}', '\u{0055}', '\u{0056}', '\u{0057}', '\u{0058}',
    '\u{0059}', '\u{005A}', '\u{00B2}', '\u{00D4}', '\u{00D6}', '\u{00D2}', '\u{00D3}', '\u{00D5}',
    // 0xF0-0xFF
    '\u{0030}', '\u{0031}', '\u{0032}', '\u{0033}', '\u{0034}', '\u{0035}', '\u{0036}', '\u{0037}',
    '\u{0038}', '\u{0039}', '\u{00B3}', '\u{00DB}', '\u{00DC}', '\u{00D9}', '\u{00DA}', '\u{009F}',
];

/// Returns the EBCDIC-to-Unicode lookup table for the given code page.
fn table_for(code_page: CodePage) -> &'static [char; 256] {
    match code_page {
        CodePage::Cp037 => &EBCDIC_TO_UNICODE_037,
        CodePage::Cp500 => &EBCDIC_TO_UNICODE_500,
        CodePage::Cp1047 => &EBCDIC_TO_UNICODE_1047,
    }
}

/// Convert a single EBCDIC byte to its Unicode character representation.
///
/// Uses the lookup table for the specified code page.
pub fn ebcdic_to_unicode(byte: u8, code_page: CodePage) -> char {
    let table = table_for(code_page);
    table[byte as usize]
}

/// Convert a Unicode character to its EBCDIC byte representation.
///
/// Returns `None` if the character has no mapping in the specified code page.
/// Performs a reverse lookup through the 256-entry table. For bulk encoding,
/// prefer `encode_string` which builds an internal reverse map.
pub fn unicode_to_ebcdic(ch: char, code_page: CodePage) -> Option<u8> {
    let table = table_for(code_page);
    for (i, &table_char) in table.iter().enumerate() {
        if table_char == ch {
            return Some(i as u8);
        }
    }
    None
}

/// Decode a byte slice of EBCDIC data into a Unicode `String`.
///
/// Each byte is independently converted using the lookup table for the
/// specified code page.
pub fn decode_string(bytes: &[u8], code_page: CodePage) -> String {
    let table = table_for(code_page);
    bytes.iter().map(|&b| table[b as usize]).collect()
}

/// Encode a Unicode string into EBCDIC bytes.
///
/// Characters that have no mapping in the specified code page are replaced
/// with EBCDIC 0x3F (SUB). This is the standard EBCDIC substitution behavior.
///
/// Builds a reverse lookup map internally for efficient bulk encoding.
pub fn encode_string(text: &str, code_page: CodePage) -> Vec<u8> {
    let table = table_for(code_page);

    // Build reverse lookup: Unicode char -> EBCDIC byte.
    // For characters that appear at multiple positions, the lowest EBCDIC
    // byte value wins (entry() only inserts if not already present).
    let mut reverse: std::collections::HashMap<char, u8> =
        std::collections::HashMap::with_capacity(256);
    for (i, &ch) in table.iter().enumerate() {
        reverse.entry(ch).or_insert(i as u8);
    }

    const EBCDIC_SUB: u8 = 0x3F;

    text.chars()
        .map(|ch| *reverse.get(&ch).unwrap_or(&EBCDIC_SUB))
        .collect()
}

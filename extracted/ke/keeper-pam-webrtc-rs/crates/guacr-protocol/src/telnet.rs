// Telnet IAC (Interpret As Command) constants used by TN3270, TN5250,
// and their integration tests.

/// Interpret As Command — precedes all Telnet control sequences.
pub const IAC: u8 = 0xFF;
/// WILL — sender will use the indicated option.
pub const WILL: u8 = 0xFB;
/// DO — sender requests the peer use the indicated option.
pub const DO: u8 = 0xFD;
/// Subnegotiation Begin — starts option subnegotiation data.
pub const SB: u8 = 0xFA;
/// Subnegotiation End — terminates option subnegotiation data.
pub const SE: u8 = 0xF0;
/// End Of Record — terminates a 3270/5250 data record when sent as IAC EOR.
pub const EOR: u8 = 0xEF;
/// Binary Transmission option (RFC 856).
pub const OPT_BINARY: u8 = 0x00;
/// Terminal Type option (RFC 1091) — negotiates the terminal model string.
pub const OPT_TERMINAL_TYPE: u8 = 0x18;
/// End Of Record option (RFC 885) — enables IAC EOR record framing.
pub const OPT_EOR: u8 = 0x19;

/// Extract one complete Telnet EOR-terminated record from `buf`.
///
/// Parses Telnet framing (IAC EOR, IAC IAC escape, IAC SB…SE subnegotiation,
/// and 3-byte option commands) and returns the unescaped record payload when a
/// complete record is found, draining the consumed bytes from `buf`. Returns
/// `None` when the buffer does not yet contain a complete record.
///
/// Used by the TN3270 and TN5250 handlers, which share identical framing logic.
pub fn extract_record(buf: &mut Vec<u8>) -> Option<Vec<u8>> {
    let mut record = Vec::new();
    let mut i = 0;

    while i < buf.len() {
        if buf[i] != IAC {
            record.push(buf[i]);
            i += 1;
            continue;
        }

        // Need at least one more byte after IAC.
        if i + 1 >= buf.len() {
            return None; // Wait for more data — leave buffer intact.
        }

        match buf[i + 1] {
            EOR => {
                // End of record: drain consumed bytes and return.
                buf.drain(..i + 2);
                return Some(record);
            }
            b if b == IAC => {
                // IAC IAC → literal 0xFF inside record data.
                record.push(IAC);
                i += 2;
            }
            b if b == SB => {
                // Subnegotiation: IAC SB … IAC SE — skip entirely.
                i += 2;
                loop {
                    if i + 1 >= buf.len() {
                        return None; // Incomplete subnegotiation — wait.
                    }
                    if buf[i] == IAC && buf[i + 1] == SE {
                        i += 2;
                        break;
                    }
                    i += 1;
                }
            }
            _ => {
                // 3-byte IAC option command (DO/DONT/WILL/WONT + option).
                if i + 2 >= buf.len() {
                    return None; // Incomplete command — wait.
                }
                i += 3;
            }
        }
    }

    // No EOR seen yet — leave buffer intact for next call.
    None
}

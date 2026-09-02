use bytes::Bytes;

/// Server-side DLP filter for terminal text streams.
///
/// Applied to raw PTY/query bytes before they are sent to the browser as
/// `terminal-data` instructions. Implementations may redact credential
/// patterns, run AI-based analysis, or pass bytes through unchanged.
///
/// Injected at handler construction time so tests can use PassthroughDlp
/// without pulling in the full threat-detection stack.
pub trait TerminalDlp: Send + Sync {
    /// Filter PTY output bytes before they reach the wire.
    ///
    /// Takes ownership of `input` so a no-op implementation can return it
    /// unchanged with zero allocation. Implementations that redact content
    /// may allocate a new buffer and return it instead.
    ///
    /// Returns the cleaned bytes — same content if nothing was redacted,
    /// shorter if sensitive spans were replaced.
    fn filter(&self, input: Bytes) -> Bytes;
}

/// No-op DLP implementation — forwards bytes unchanged without allocating.
///
/// Used in tests and for sessions where DLP is handled at a higher layer.
pub struct PassthroughDlp;

impl TerminalDlp for PassthroughDlp {
    fn filter(&self, input: Bytes) -> Bytes {
        input
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct RedactDlp {
        pattern: Vec<u8>,
        replacement: Vec<u8>,
    }

    impl TerminalDlp for RedactDlp {
        fn filter(&self, input: Bytes) -> Bytes {
            if let Some(pos) = input
                .windows(self.pattern.len())
                .position(|w| w == self.pattern)
            {
                let mut out = Vec::with_capacity(input.len());
                out.extend_from_slice(&input[..pos]);
                out.extend_from_slice(&self.replacement);
                out.extend_from_slice(&input[pos + self.pattern.len()..]);
                Bytes::from(out)
            } else {
                input
            }
        }
    }

    #[test]
    fn test_passthrough_forwards_unchanged() {
        let dlp = PassthroughDlp;
        let raw = b"hello \x1b[32mworld\x1b[0m";
        let input = Bytes::copy_from_slice(raw);
        assert_eq!(dlp.filter(input), raw.as_slice());
    }

    #[test]
    fn test_redact_dlp_replaces_pattern() {
        let dlp = RedactDlp {
            pattern: b"secret".to_vec(),
            replacement: b"[REDACTED]".to_vec(),
        };
        let output = dlp.filter(Bytes::from_static(b"my secret is here"));
        assert_eq!(output, b"my [REDACTED] is here".as_slice());
    }

    #[test]
    fn test_redact_dlp_no_match_passthrough() {
        let dlp = RedactDlp {
            pattern: b"secret".to_vec(),
            replacement: b"[REDACTED]".to_vec(),
        };
        let input = Bytes::from_static(b"nothing sensitive here");
        assert_eq!(dlp.filter(input), b"nothing sensitive here".as_slice());
    }
}

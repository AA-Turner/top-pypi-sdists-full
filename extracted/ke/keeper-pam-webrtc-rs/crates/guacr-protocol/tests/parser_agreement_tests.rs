// Cross-checks the crate's two Guacamole instruction entry points.
//
// `GuacamoleParser` (complete-buffer) and `StreamingParser` (partial-buffer) were
// once separate implementations of the same wire format. That duplication is how
// `GuacamoleParser` came to byte-slice by a character count — panicking on any
// multi-byte value — while `StreamingParser`, which had a unicode test suite,
// stayed correct. `GuacamoleParser` now delegates, so there is one implementation.
//
// What remains worth guarding is the seam: that the complete-buffer front end
// forwards opcode and args faithfully, and that its coarser `ParseError` taxonomy
// maps onto `PeekError` without collapsing truncation into corruption. Each case
// asserts both entry points reach the same verdict, normalising the two error
// enums onto one classification. It would also catch a future re-divergence.

use bytes::Bytes;
use guacr_protocol::{format_instruction, GuacamoleParser, ParseError, PeekError, StreamingParser};

/// The shared verdict both parsers must reach, independent of their error enums.
#[derive(Debug, PartialEq)]
enum Verdict {
    Parsed {
        opcode: String,
        args: Vec<String>,
    },
    /// Buffer does not yet hold a complete instruction; more bytes may complete it.
    Truncated,
    /// Structurally invalid — no continuation can rescue it.
    Malformed,
}

fn full_buffer_verdict(wire: &str) -> Verdict {
    let owned = Bytes::from(wire.to_string());
    match GuacamoleParser::parse_instruction(&owned) {
        Ok(instr) => Verdict::Parsed {
            opcode: instr.opcode.to_string(),
            args: instr.args.iter().map(|s| s.to_string()).collect(),
        },
        Err(ParseError::MissingTerminator) => Verdict::Truncated,
        Err(ParseError::InvalidFormat)
        | Err(ParseError::InvalidLength)
        | Err(ParseError::InvalidUtf8) => Verdict::Malformed,
    }
}

fn streaming_verdict(wire: &str) -> Verdict {
    match StreamingParser::peek_instruction(wire.as_bytes()) {
        Ok(peeked) => Verdict::Parsed {
            opcode: peeked.opcode.to_string(),
            args: peeked.args.iter().map(|s| s.to_string()).collect(),
        },
        Err(PeekError::Incomplete) => Verdict::Truncated,
        Err(_) => Verdict::Malformed,
    }
}

fn assert_agree(label: &str, wire: &str) {
    let full = full_buffer_verdict(wire);
    let streaming = streaming_verdict(wire);
    assert_eq!(
        full, streaming,
        "parsers disagree on {label} ({wire:?}): \
         GuacamoleParser={full:?} StreamingParser={streaming:?}"
    );
}

#[test]
fn parsers_agree_on_wire_shapes() {
    let cases: &[(&str, &str)] = &[
        // Well-formed.
        ("plain ascii", "3.key,5.65507,1.1;"),
        ("no args", "4.sync;"),
        ("empty arg", "4.name,0.;"),
        // Multi-byte values: element lengths are character counts, not byte counts.
        ("accented value", "4.name,4.café;"),
        ("cjk value", "4.name,4.国隊科学;"),
        ("emoji value", "9.clipboard,4.hi 👋;"),
        ("multibyte opcode", "4.café,1.x;"),
        // Separators are legal *inside* values; boundaries come from the length.
        ("semicolon in value", "4.name,9.abc;defgh;"),
        ("comma in value", "9.clipboard,3.a,b;"),
        ("both separators", "9.clipboard,5.a,b;c;"),
        // Truncated: the declared count has not arrived yet.
        ("value short of declared length", "4.name,9.abc;"),
        ("no terminator", "3.key,5.65507,1.1"),
        ("cut mid-multibyte", "4.name,4.caf"),
        // Malformed: declared count satisfied, but what follows is neither , nor ;.
        ("junk after full length", "4.name,9.abc;defghX;"),
        ("non-numeric length", "4.name,x.abc;"),
    ];

    for (label, wire) in cases {
        assert_agree(label, wire);
    }
}

/// `peek_instruction` must cost O(first instruction), not O(whole buffer).
///
/// Its ASCII fast path once scanned to the end of the slice regardless of how many
/// characters were requested, so peeking one short instruction with a large buffer
/// behind it scanned the whole buffer — quadratic for any caller that accumulates
/// bytes and re-peeks, which is every streaming caller. Timing is a blunt
/// instrument, so the bound here is deliberately loose: a 4× tolerance still fails
/// hard against the old behaviour, which was ~300× at 64 KiB.
#[test]
fn peek_instruction_cost_is_independent_of_trailing_bytes() {
    use std::time::Instant;

    let instruction = b"3.key,5.65507,1.1;";
    let iters = 50_000;

    let time_with_trailing = |trailing: usize| {
        let mut buf = instruction.to_vec();
        buf.extend(std::iter::repeat_n(b'x', trailing));
        // Warm up so the first measurement is not paying for page faults.
        for _ in 0..1_000 {
            let _ = StreamingParser::peek_instruction(&buf);
        }
        let start = Instant::now();
        for _ in 0..iters {
            let peeked = StreamingParser::peek_instruction(&buf).expect("frames");
            assert_eq!(peeked.total_length_in_buffer, instruction.len());
        }
        start.elapsed().as_nanos().max(1)
    };

    let baseline = time_with_trailing(0);
    let with_64k = time_with_trailing(64 * 1024);

    assert!(
        with_64k < baseline * 4,
        "peek_instruction scales with trailing bytes: {baseline}ns with none vs \
         {with_64k}ns with 64 KiB behind the instruction — the ASCII scan is \
         probably unbounded again"
    );
}

/// Both parsers must read back whatever `format_instruction` writes. This ties
/// the encoder's `chars().count()` to both decoders at once.
#[test]
fn parsers_agree_on_encoder_output() {
    let cases: &[(&str, &[&str])] = &[
        ("key", &["65507", "1"]),
        ("clipboard", &["café français naïve"]),
        ("name", &["国隊・科学"]),
        ("text", &["Hello 世界 🌍 café!"]),
        ("clipboard", &["semi;colon"]),
        ("clipboard", &["comma,separated"]),
        ("clipboard", &["mixed; é, 🌍"]),
        ("noargs", &[]),
    ];

    for (opcode, args) in cases {
        let wire = format_instruction(opcode, args);
        assert_agree("encoder output", &wire);

        let expected = Verdict::Parsed {
            opcode: opcode.to_string(),
            args: args.iter().map(|s| s.to_string()).collect(),
        };
        assert_eq!(
            full_buffer_verdict(&wire),
            expected,
            "encoder output did not round-trip: {wire:?}"
        );
    }
}

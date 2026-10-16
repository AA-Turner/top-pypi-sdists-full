use crate::advanced::{
    format_ack, format_error, format_msg, format_nest, format_pipe, format_transfer,
    MSG_SECURITY_WARNING,
};

#[test]
fn test_format_transfer() {
    let instr = format_transfer(0, 0, 0, 100, 50, 12, 0, 10, 20);
    // "transfer" is 8 characters
    assert!(instr.starts_with("8.transfer,"));
    assert!(instr.contains("100"));
}

#[test]
fn test_format_nest() {
    let instr = format_nest("conn-123", 0, 10, 20);
    assert!(instr.starts_with("4.nest,"));
    assert!(instr.contains("conn-123"));
}

#[test]
fn test_format_pipe() {
    let instr = format_pipe(1, "application/octet-stream", "mypipe");
    assert!(instr.starts_with("4.pipe,"));
    assert!(instr.contains("mypipe"));
}

#[test]
fn test_format_ack() {
    let instr = format_ack(1, "ok");
    assert_eq!(instr, "3.ack,1.1,2.ok;");
}

#[test]
fn test_format_error() {
    let instr = format_error("Authentication failed", 769);
    assert_eq!(instr, "5.error,21.Authentication failed,3.769;");

    let instr2 = format_error("Connection timeout", 514);
    assert_eq!(instr2, "5.error,18.Connection timeout,3.514;");
}

// ---------------------------------------------------------------------------
// format_msg — the non-fatal client-visible channel
// ---------------------------------------------------------------------------
//
// `error` is the only other server-to-client text instruction and it terminates the session
// (`streaming.rs`: `b"error" => OpcodeAction::CloseConnection`). Anything the user should
// see but survive has to go out as `msg`.

#[test]
fn test_format_msg_wire_format() {
    let instr = format_msg(MSG_SECURITY_WARNING, &["Not verified"]);
    assert_eq!(
        instr, "3.msg,4.4096,12.Not verified;",
        "opcode and every argument carry a length prefix, the code is decimal, and the \
         instruction is semicolon-terminated"
    );
}

#[test]
fn test_format_msg_with_no_arguments() {
    let instr = format_msg(MSG_SECURITY_WARNING, &[]);
    assert_eq!(
        instr, "3.msg,4.4096;",
        "a bare code is a valid msg; the client switches on the code alone"
    );
}

#[test]
fn test_format_msg_with_several_arguments() {
    let instr = format_msg(1, &["alice", "session-7"]);
    assert_eq!(instr, "3.msg,1.1,5.alice,9.session-7;");
}

/// Guacamole LENGTH counts Unicode codepoints, not UTF-8 bytes. A byte count here would
/// desynchronize the client's parser and break the session the message was meant to warn
/// about.
#[test]
fn test_format_msg_lengths_count_codepoints_not_bytes() {
    // "Não verificado" is 14 codepoints but 15 UTF-8 bytes.
    let text = "Não verificado";
    assert_eq!(text.chars().count(), 14);
    assert_eq!(text.len(), 15);

    let instr = format_msg(MSG_SECURITY_WARNING, &[text]);
    assert_eq!(instr, "3.msg,4.4096,14.Não verificado;");
}

/// Commas and semicolons are legal inside an argument precisely because the length prefix
/// delimits it. A warning sentence contains both, so this is on the live path.
#[test]
fn test_format_msg_argument_may_contain_protocol_delimiters() {
    let text = "Not verified; could be intercepted, ask an admin.";
    let instr = format_msg(MSG_SECURITY_WARNING, &[text]);
    assert_eq!(
        instr,
        format!("3.msg,4.4096,{}.{};", text.chars().count(), text)
    );
}

/// Upstream Guacamole defines USER_JOINED=1 and USER_LEFT=2. Keeper's code must stay clear
/// of that range or a client would render a security warning as a join/leave event.
#[test]
fn test_the_security_warning_code_does_not_collide_with_upstream_codes() {
    // A const block rather than a plain assert!: the operand is a constant, so the collision
    // is decidable at compile time and a future edit that lowered the code into upstream's
    // range would fail the build rather than wait for someone to run the tests.
    const {
        assert!(
            MSG_SECURITY_WARNING > 2,
            "must not reuse USER_JOINED (1) or USER_LEFT (2)"
        )
    };
    assert_eq!(MSG_SECURITY_WARNING, 0x1000);
}

// ---------------------------------------------------------------------------
// Status codes
// ---------------------------------------------------------------------------
//
// The client decodes these with guacamole-common-js's `Guacamole.Status.Code`, which carries
// guacd's values, so a wrong number here is shown to the user as a different failure. The
// expected values are copied from guacd's `src/libguac/guacamole/protocol-types.h`, in hex as
// written there.

#[test]
fn status_codes_match_guacd() {
    use crate::advanced::*;
    let table: &[(&str, u32, u32)] = &[
        ("SUCCESS", STATUS_SUCCESS, 0x0000),
        ("UNSUPPORTED", STATUS_UNSUPPORTED, 0x0100),
        ("SERVER_ERROR", STATUS_SERVER_ERROR, 0x0200),
        ("SERVER_BUSY", STATUS_SERVER_BUSY, 0x0201),
        ("UPSTREAM_TIMEOUT", STATUS_UPSTREAM_TIMEOUT, 0x0202),
        ("UPSTREAM_ERROR", STATUS_UPSTREAM_ERROR, 0x0203),
        ("RESOURCE_NOT_FOUND", STATUS_RESOURCE_NOT_FOUND, 0x0204),
        ("RESOURCE_CONFLICT", STATUS_RESOURCE_CONFLICT, 0x0205),
        ("RESOURCE_CLOSED", STATUS_RESOURCE_CLOSED, 0x0206),
        ("UPSTREAM_NOT_FOUND", STATUS_UPSTREAM_NOT_FOUND, 0x0207),
        ("UPSTREAM_UNAVAILABLE", STATUS_UPSTREAM_UNAVAILABLE, 0x0208),
        ("SESSION_CONFLICT", STATUS_SESSION_CONFLICT, 0x0209),
        ("SESSION_TIMEOUT", STATUS_SESSION_TIMEOUT, 0x020A),
        ("SESSION_CLOSED", STATUS_SESSION_CLOSED, 0x020B),
        ("CLIENT_BAD_REQUEST", STATUS_CLIENT_BAD_REQUEST, 0x0300),
        ("CLIENT_UNAUTHORIZED", STATUS_CLIENT_UNAUTHORIZED, 0x0301),
        ("CLIENT_FORBIDDEN", STATUS_CLIENT_FORBIDDEN, 0x0303),
        ("CLIENT_TIMEOUT", STATUS_CLIENT_TIMEOUT, 0x0308),
        ("CLIENT_OVERRUN", STATUS_CLIENT_OVERRUN, 0x030D),
        ("CLIENT_BAD_TYPE", STATUS_CLIENT_BAD_TYPE, 0x030F),
        ("CLIENT_TOO_MANY", STATUS_CLIENT_TOO_MANY, 0x031D),
    ];
    let wrong: Vec<String> = table
        .iter()
        .filter(|(_, ours, guacd)| ours != guacd)
        .map(|(name, ours, guacd)| format!("{name}: {ours} (0x{ours:04X}), guacd 0x{guacd:04X}"))
        .collect();
    assert!(
        wrong.is_empty(),
        "status codes differ from guacd:\n{}",
        wrong.join("\n")
    );
}

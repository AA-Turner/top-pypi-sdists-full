// Advanced instruction formatting for Guacamole protocol
//
// Supports: transfer, nest, pipe, ack, error

use crate::format_instruction;

// ============================================================================
// Guacamole Protocol Status Codes
// ============================================================================
// Values are guacd's, from `src/libguac/guacamole/protocol-types.h`. The client decodes them
// with guacamole-common-js's `Guacamole.Status.Code`, which carries the same table, so a wrong
// number here reaches the user as a different failure. `tests/advanced_tests.rs` pins each one.

/// The operation succeeded (0x0000)
pub const STATUS_SUCCESS: u32 = 0x0000;

/// The requested operation is unsupported (0x0100)
pub const STATUS_UNSUPPORTED: u32 = 0x0100;

/// Internal server error (0x0200)
pub const STATUS_SERVER_ERROR: u32 = 0x0200;

/// The server is busy and cannot take the operation now (0x0201)
pub const STATUS_SERVER_BUSY: u32 = 0x0201;

/// The remote server did not respond in time (0x0202)
pub const STATUS_UPSTREAM_TIMEOUT: u32 = 0x0202;

/// The remote server answered with an error (0x0203)
pub const STATUS_UPSTREAM_ERROR: u32 = 0x0203;

/// The requested resource does not exist (0x0204)
pub const STATUS_RESOURCE_NOT_FOUND: u32 = 0x0204;

/// The resource is already in use or locked (0x0205)
pub const STATUS_RESOURCE_CONFLICT: u32 = 0x0205;

/// The resource has been closed (0x0206)
pub const STATUS_RESOURCE_CLOSED: u32 = 0x0206;

/// The remote server does not appear to exist (0x0207)
pub const STATUS_UPSTREAM_NOT_FOUND: u32 = 0x0207;

/// The remote server is refusing service (0x0208)
pub const STATUS_UPSTREAM_UNAVAILABLE: u32 = 0x0208;

/// The session conflicted with another session (0x0209)
pub const STATUS_SESSION_CONFLICT: u32 = 0x0209;

/// The session appears to be inactive (0x020A)
pub const STATUS_SESSION_TIMEOUT: u32 = 0x020A;

/// The session was forcibly closed (0x020B)
pub const STATUS_SESSION_CLOSED: u32 = 0x020B;

/// Bad request from client (0x0300)
pub const STATUS_CLIENT_BAD_REQUEST: u32 = 0x0300;

/// Client unauthorized (0x0301)
pub const STATUS_CLIENT_UNAUTHORIZED: u32 = 0x0301;

/// Client forbidden (0x0303)
pub const STATUS_CLIENT_FORBIDDEN: u32 = 0x0303;

/// The client took too long to respond (0x0308)
pub const STATUS_CLIENT_TIMEOUT: u32 = 0x0308;

/// The client sent too much data (0x030D)
pub const STATUS_CLIENT_OVERRUN: u32 = 0x030D;

/// The client sent data of an unsupported or unexpected type (0x030F)
pub const STATUS_CLIENT_BAD_TYPE: u32 = 0x030F;

/// The operation would exceed a per-client limit (0x031D)
pub const STATUS_CLIENT_TOO_MANY: u32 = 0x031D;

/// Format `transfer` instruction - Copy/transfer image data between layers
///
/// Format: `7.transfer,{src_layer},{src_x},{src_y},{width},{height},{function},{dst_layer},{dst_x},{dst_y};`
///
/// # Arguments
/// - `src_layer`: Source layer index
/// - `src_x`, `src_y`: Source coordinates
/// - `width`, `height`: Dimensions to transfer
/// - `function`: Transfer function (0-15, typically 12 for SRC)
/// - `dst_layer`: Destination layer index
/// - `dst_x`, `dst_y`: Destination coordinates
#[allow(clippy::too_many_arguments)]
pub fn format_transfer(
    src_layer: i32,
    src_x: u32,
    src_y: u32,
    width: u32,
    height: u32,
    function: u8,
    dst_layer: i32,
    dst_x: u32,
    dst_y: u32,
) -> String {
    let src_layer_str = src_layer.to_string();
    let src_x_str = src_x.to_string();
    let src_y_str = src_y.to_string();
    let width_str = width.to_string();
    let height_str = height.to_string();
    let function_str = function.to_string();
    let dst_layer_str = dst_layer.to_string();
    let dst_x_str = dst_x.to_string();
    let dst_y_str = dst_y.to_string();

    format_instruction(
        "transfer",
        &[
            &src_layer_str,
            &src_x_str,
            &src_y_str,
            &width_str,
            &height_str,
            &function_str,
            &dst_layer_str,
            &dst_x_str,
            &dst_y_str,
        ],
    )
}

/// Format `nest` instruction - Nest another connection
///
/// Format: `4.nest,{connection_id},{layer},{x},{y};`
///
/// # Arguments
/// - `connection_id`: Connection ID to nest
/// - `layer`: Layer index
/// - `x`, `y`: Position
pub fn format_nest(connection_id: &str, layer: i32, x: u32, y: u32) -> String {
    let layer_str = layer.to_string();
    let x_str = x.to_string();
    let y_str = y.to_string();

    format_instruction("nest", &[connection_id, &layer_str, &x_str, &y_str])
}

/// Format `pipe` instruction - Named pipe stream
///
/// Format: `4.pipe,{stream},{mimetype},{name};`
///
/// # Arguments
/// - `stream`: Stream index
/// - `mimetype`: MIME type
/// - `name`: Pipe name
pub fn format_pipe(stream: u32, mimetype: &str, name: &str) -> String {
    let stream_str = stream.to_string();
    format_instruction("pipe", &[&stream_str, mimetype, name])
}

/// Format `ack` instruction - Acknowledge stream data
///
/// Format: `3.ack,{stream},{message};`
///
/// # Arguments
/// - `stream`: Stream index
/// - `message`: Acknowledgment message (typically "ok" or error)
pub fn format_ack(stream: u32, message: &str) -> String {
    let stream_str = stream.to_string();
    format_instruction("ack", &[&stream_str, message])
}

/// Format `error` instruction - Send error message to client
///
/// Format: `5.error,{message},{status_code};`
///
/// `status_code` is one of the `STATUS_*` constants in this module.
///
/// # Arguments
/// - `message`: Error message to display to user
/// - `status_code`: Guacamole protocol status code
///
/// # Example
/// ```
/// use guacr_protocol::format_error;
/// let error_instr = format_error("Authentication failed", 769);
/// assert_eq!(error_instr, "5.error,21.Authentication failed,3.769;");
/// ```
pub fn format_error(message: &str, status_code: u32) -> String {
    let status_str = status_code.to_string();
    format_instruction("error", &[message, &status_str])
}

/// Guacamole `msg` code carrying a human-readable warning for the user.
///
/// The `msg` instruction is the only server-to-client text channel that does **not**
/// terminate the session — `error` does (`streaming.rs`: `b"error" => CloseConnection`).
/// Upstream Guacamole defines just two codes, `USER_JOINED` (1) and `USER_LEFT` (2), and a
/// client ignores a code it does not recognize, so an unknown code is inert rather than
/// fatal. This sits at 0x1000 to leave upstream's low range free: a code added upstream
/// later cannot collide and start rendering Keeper's text as a join/leave event.
pub const MSG_SECURITY_WARNING: u32 = 0x1000;

/// Format a `msg` instruction: a non-fatal, client-visible message.
///
/// `code` tells the client how to present the message; `args` are the code's parameters,
/// which for [`MSG_SECURITY_WARNING`] is a single human-readable string.
///
/// # Example
/// ```
/// use guacr_protocol::{format_msg, MSG_SECURITY_WARNING};
/// let instr = format_msg(MSG_SECURITY_WARNING, &["Not verified"]);
/// assert_eq!(instr, "3.msg,4.4096,12.Not verified;");
/// ```
pub fn format_msg(code: u32, args: &[&str]) -> String {
    let code_str = code.to_string();
    let mut fields = Vec::with_capacity(args.len() + 1);
    fields.push(code_str.as_str());
    fields.extend_from_slice(args);
    format_instruction("msg", &fields)
}

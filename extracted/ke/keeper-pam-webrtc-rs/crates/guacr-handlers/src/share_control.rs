// Session sharing control messages — Phase 6b
//
// Parses incoming `share_*` Guacamole instructions from the vault and
// produces outgoing response bytes. All messages flow through the normal
// Guacamole instruction channel (to_client / from_client).
//
// Incoming (vault → guacr):
//   share_create:<display_name>,<privileges_hex>,<passthrough_b64>
//   share_revoke:<guid>
//   privilege_change:<guid>,<new_privileges_hex>
//   admin_takeover:<display_name>,<admin_privileges_hex>,<owner_new_privileges_hex>
//   share_join:<guid>   (sent by a viewer on connect — checked in connect() dispatch)
//
// Outgoing (guacr → vault):
//   share_created:<guid>,<passthrough_b64>
//   participant_update:<json_participant_list>
//
// Drawing (viewer → guacr → broadcast):
//   draw_event:<event_type>,<x_f32>,<y_f32>,<color_hex>,<thickness>

use base64::{engine::general_purpose::STANDARD as B64, Engine};
use bytes::Bytes;
use guacr_protocol::format_instruction;
use uuid::Uuid;

use crate::share_registry::{Participant, ParticipantStatus};

// ── Incoming message parsing ──────────────────────────────────────────────────

/// A parsed incoming share control instruction.
#[derive(Debug)]
pub enum ShareControl {
    /// Owner wants to create a share invitation.
    Create {
        display_name: String,
        privileges: u8,
        /// Opaque blob to echo back unchanged.
        passthrough: Vec<u8>,
    },
    /// Owner revokes a pending or connected participant.
    Revoke { guid: Uuid },
    /// Owner changes a participant's privilege set.
    PrivilegeChange { guid: Uuid, new_privileges: u8 },
    /// Router-initiated admin takeover.
    AdminTakeover {
        admin_name: String,
        admin_privileges: u8,
        owner_new_privileges: u8,
    },
}

/// Try to parse a Guacamole instruction into a `ShareControl`.
/// Returns `None` if the opcode is not a share control message.
pub fn parse(opcode: &str, args: &[&str]) -> Option<Result<ShareControl, String>> {
    match opcode {
        "share_create" => {
            if args.len() < 3 {
                return Some(Err("share_create requires 3 args".into()));
            }
            let display_name = args[0].to_string();
            let privileges = u8::from_str_radix(args[1], 16)
                .map_err(|_| format!("invalid privileges hex: {}", args[1]));
            let passthrough = B64
                .decode(args[2])
                .map_err(|_| format!("invalid passthrough base64: {}", args[2]));
            Some(match (privileges, passthrough) {
                (Ok(p), Ok(pt)) => Ok(ShareControl::Create {
                    display_name,
                    privileges: p,
                    passthrough: pt,
                }),
                (Err(e), _) | (_, Err(e)) => Err(e),
            })
        }
        "share_revoke" => {
            if args.is_empty() {
                return Some(Err("share_revoke requires guid".into()));
            }
            Some(
                Uuid::parse_str(args[0])
                    .map(|guid| ShareControl::Revoke { guid })
                    .map_err(|e| format!("invalid guid: {e}")),
            )
        }
        "privilege_change" => {
            if args.len() < 2 {
                return Some(Err("privilege_change requires 2 args".into()));
            }
            let guid = Uuid::parse_str(args[0]).map_err(|e| format!("invalid guid: {e}"));
            let priv_val = u8::from_str_radix(args[1], 16)
                .map_err(|_| format!("invalid privileges hex: {}", args[1]));
            Some(match (guid, priv_val) {
                (Ok(g), Ok(p)) => Ok(ShareControl::PrivilegeChange {
                    guid: g,
                    new_privileges: p,
                }),
                (Err(e), _) | (_, Err(e)) => Err(e),
            })
        }
        "admin_takeover" => {
            if args.len() < 3 {
                return Some(Err("admin_takeover requires 3 args".into()));
            }
            let admin_name = args[0].to_string();
            let admin_priv = u8::from_str_radix(args[1], 16)
                .map_err(|_| format!("invalid admin privileges: {}", args[1]));
            let owner_priv = u8::from_str_radix(args[2], 16)
                .map_err(|_| format!("invalid owner privileges: {}", args[2]));
            Some(match (admin_priv, owner_priv) {
                (Ok(ap), Ok(op)) => Ok(ShareControl::AdminTakeover {
                    admin_name,
                    admin_privileges: ap,
                    owner_new_privileges: op,
                }),
                (Err(e), _) | (_, Err(e)) => Err(e),
            })
        }
        _ => None,
    }
}

// ── Outgoing message encoding ─────────────────────────────────────────────────

/// Encode a `share_created` response to send back to the vault.
pub fn encode_share_created(guid: Uuid, passthrough: &[u8]) -> Bytes {
    let guid_str = guid.to_string();
    let pt_b64 = B64.encode(passthrough);
    Bytes::from(format_instruction(
        "share_created",
        &[guid_str.as_str(), pt_b64.as_str()],
    ))
}

/// Encode a `participant_update` broadcast to all connected participants.
///
/// Format: `participant_update:<json_array_of_participants>`
pub fn encode_participant_update(participants: &[Participant], admin_takeover: bool) -> Bytes {
    let list: Vec<serde_json::Value> = participants
        .iter()
        .map(|p| {
            serde_json::json!({
                "display_name": p.display_name,
                "privileges": p.privileges,
                "status": match p.status {
                    ParticipantStatus::Pending => "pending",
                    ParticipantStatus::Connected => "connected",
                    ParticipantStatus::Disconnected => "disconnected",
                },
            })
        })
        .collect();
    let json = serde_json::json!({
        "participants": list,
        "admin_takeover": admin_takeover,
    })
    .to_string();
    Bytes::from(format_instruction("participant_update", &[json.as_str()]))
}

/// Encode a `share_join_accepted` response to a joining viewer.
pub fn encode_join_accepted(privileges: u8) -> Bytes {
    Bytes::from(format_instruction(
        "share_join_accepted",
        &[format!("{:02x}", privileges).as_str()],
    ))
}

/// Encode a `share_join_rejected` response to a joining viewer.
pub fn encode_join_rejected(reason: &str) -> Bytes {
    Bytes::from(format_instruction("share_join_rejected", &[reason]))
}

/// Encode an `admin_takeover_notice` broadcast to all participants.
pub fn encode_admin_takeover_notice(admin_name: &str, owner_new_privileges: u8) -> Bytes {
    Bytes::from(format_instruction(
        "admin_takeover_notice",
        &[admin_name, format!("{:02x}", owner_new_privileges).as_str()],
    ))
}

// ── Drawing events ────────────────────────────────────────────────────────────

/// A parsed `draw_event` from a viewer.
#[derive(Debug, Clone)]
pub struct DrawEvent {
    /// 0=Start, 1=Move, 2=End, 3=Clear
    pub event_type: u8,
    /// Normalized 0.0–1.0 relative to session dimensions
    pub x: f32,
    pub y: f32,
    /// ARGB packed color
    pub color: u32,
    pub thickness: u8,
}

/// Parse a `draw_event` instruction args into a `DrawEvent`.
pub fn parse_draw_event(args: &[&str]) -> Result<DrawEvent, String> {
    if args.len() < 5 {
        return Err(format!("draw_event requires 5 args, got {}", args.len()));
    }
    let event_type = args[0]
        .parse::<u8>()
        .map_err(|_| format!("invalid event_type: {}", args[0]))?;
    let x = args[1]
        .parse::<f32>()
        .map_err(|_| format!("invalid x: {}", args[1]))?;
    let y = args[2]
        .parse::<f32>()
        .map_err(|_| format!("invalid y: {}", args[2]))?;
    let color =
        u32::from_str_radix(args[3], 16).map_err(|_| format!("invalid color hex: {}", args[3]))?;
    let thickness = args[4]
        .parse::<u8>()
        .map_err(|_| format!("invalid thickness: {}", args[4]))?;
    Ok(DrawEvent {
        event_type,
        x,
        y,
        color,
        thickness,
    })
}

/// Encode a `draw_event` broadcast. Echoed back to all participants including the sender
/// so each client's canvas stays in sync with the authoritative server state.
pub fn encode_draw_event(ev: &DrawEvent) -> Bytes {
    Bytes::from(format_instruction(
        "draw_event",
        &[
            format!("{}", ev.event_type).as_str(),
            format!("{:.6}", ev.x).as_str(),
            format!("{:.6}", ev.y).as_str(),
            format!("{:08x}", ev.color).as_str(),
            format!("{}", ev.thickness).as_str(),
        ],
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_share_create() {
        let pt_b64 = B64.encode(b"conv-id:cfg-id");
        let args = ["Alice", "07", pt_b64.as_str()];
        let msg = parse("share_create", &args).unwrap().unwrap();
        match msg {
            ShareControl::Create {
                display_name,
                privileges,
                passthrough,
            } => {
                assert_eq!(display_name, "Alice");
                assert_eq!(privileges, 0x07);
                assert_eq!(passthrough, b"conv-id:cfg-id");
            }
            _ => panic!("wrong variant"),
        }
    }

    #[test]
    fn test_parse_share_revoke() {
        let guid = Uuid::new_v4();
        let msg = parse("share_revoke", &[guid.to_string().as_str()])
            .unwrap()
            .unwrap();
        match msg {
            ShareControl::Revoke { guid: g } => assert_eq!(g, guid),
            _ => panic!("wrong variant"),
        }
    }

    #[test]
    fn test_parse_unknown_opcode_returns_none() {
        assert!(parse("key", &["65507"]).is_none());
    }

    #[test]
    fn test_encode_share_created_roundtrips() {
        let guid = Uuid::new_v4();
        let payload = b"some-passthrough";
        let bytes = encode_share_created(guid, payload);
        let s = std::str::from_utf8(&bytes).unwrap();
        assert!(s.contains("share_created"));
        assert!(s.contains(&guid.to_string()));
    }

    #[test]
    fn test_parse_draw_event() {
        let args = ["1", "0.500000", "0.250000", "ffaa1122", "3"];
        let ev = parse_draw_event(&args).unwrap();
        assert_eq!(ev.event_type, 1);
        assert!((ev.x - 0.5).abs() < 1e-4);
        assert!((ev.y - 0.25).abs() < 1e-4);
        assert_eq!(ev.color, 0xffaa1122);
        assert_eq!(ev.thickness, 3);
    }

    #[test]
    fn test_parse_draw_event_missing_args() {
        let args = ["1", "0.5"];
        assert!(parse_draw_event(&args).is_err());
    }

    #[test]
    fn test_encode_draw_event_roundtrips() {
        let ev = DrawEvent {
            event_type: 0,
            x: 0.1,
            y: 0.9,
            color: 0xaabb_ccdd,
            thickness: 2,
        };
        let bytes = encode_draw_event(&ev);
        let s = std::str::from_utf8(&bytes).unwrap();
        assert!(s.contains("draw_event"));
        assert!(s.contains("aabbccdd"));
    }
}

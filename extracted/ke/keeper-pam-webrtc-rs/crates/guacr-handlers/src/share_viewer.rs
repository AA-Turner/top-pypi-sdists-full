// GUID-based viewer join — Phase 6b
//
// When params["share_guid"] is present, the handler routes the connection
// as a viewer instead of an owner. The viewer receives the broadcast frame
// stream from the session owner.
//
// Call `check_viewer_join()` at the top of every ProtocolHandler::connect()
// before doing any protocol-specific work. If it returns Some(..), return
// that result immediately — the viewer session is complete.

use bytes::Bytes;
use guacr_protocol::GuacamoleParser;
use log::{info, warn};
use std::collections::HashMap;
use tokio::sync::mpsc;
use uuid::Uuid;

use crate::session_sharing::lookup;
use crate::share_control::{
    encode_draw_event, encode_join_accepted, encode_join_rejected, encode_participant_update,
    parse_draw_event,
};
use crate::share_registry::{find_session_by_guid, PRIV_CONTROL, PRIV_DRAWING, PRIV_VIEW};
use crate::{send_disconnect, HandlerError, Result};

/// Try to handle this connection as a GUID-based viewer join.
///
/// Returns `Some(result)` if `share_guid` param is present — the caller must
/// return this immediately. Returns `None` if this is a normal owner connection.
pub async fn check_viewer_join(
    params: &HashMap<String, String>,
    to_client: &mpsc::Sender<Bytes>,
    mut from_client: mpsc::Receiver<Bytes>,
    session_id: &str,
) -> Option<Result<()>> {
    let guid_str = params.get("share_guid")?;

    let guid = match Uuid::parse_str(guid_str) {
        Ok(g) => g,
        Err(_) => {
            warn!(
                "[session={}] share_guid is not a valid UUID: {}",
                session_id, guid_str
            );
            let _ = to_client
                .send(encode_join_rejected("Invalid share GUID format"))
                .await;
            let _ = send_disconnect(to_client).await;
            return Some(Err(HandlerError::InvalidParameter(format!(
                "Invalid share_guid: {}",
                guid_str
            ))));
        }
    };

    // Find the session that owns this GUID.
    let share_session = match find_session_by_guid(guid) {
        Some(s) => s,
        None => {
            warn!(
                "[session={}] share_guid {} not found or session expired",
                session_id, guid
            );
            let _ = to_client
                .send(encode_join_rejected("Session not found or expired"))
                .await;
            let _ = send_disconnect(to_client).await;
            return Some(Err(HandlerError::ConnectionFailed(
                "Session not found or expired".into(),
            )));
        }
    };

    // Accept the join — moves Pending → Connected.
    let participant = match share_session.accept_join(guid) {
        Ok(p) => p,
        Err(reason) => {
            warn!(
                "[session={}] share_guid {} join rejected: {}",
                session_id, guid, reason
            );
            let _ = to_client.send(encode_join_rejected(reason)).await;
            let _ = send_disconnect(to_client).await;
            return Some(Err(HandlerError::ConnectionFailed(reason.into())));
        }
    };

    // Must have at least view privilege.
    if !participant.has_privilege(PRIV_VIEW) {
        let _ = to_client
            .send(encode_join_rejected("No view privilege"))
            .await;
        let _ = send_disconnect(to_client).await;
        return Some(Err(HandlerError::ConnectionFailed(
            "No view privilege".into(),
        )));
    }

    info!(
        "[session={}] Viewer '{}' joined with privileges 0x{:02x}",
        session_id, participant.display_name, participant.privileges
    );

    // Confirm join to viewer.
    let _ = to_client
        .send(encode_join_accepted(participant.privileges))
        .await;

    // Broadcast participant list update to all participants in the session.
    let all = share_session.participant_list();
    let update = encode_participant_update(&all, false);
    // Best-effort: send to the frame broadcast channel (owner will relay to other viewers).
    if let Some(owner_session) = lookup(&share_session.session_id) {
        let _ = owner_session.broadcast(update);
    }

    // Subscribe to the owner's frame broadcast.
    let frame_session = match lookup(&share_session.session_id) {
        Some(s) => s,
        None => {
            let _ = send_disconnect(to_client).await;
            share_session.mark_disconnected(guid);
            return Some(Err(HandlerError::ConnectionFailed(
                "Session frame channel not found".into(),
            )));
        }
    };

    // Send current frame immediately (late-join state sync).
    if let Some(last) = frame_session.last_frame() {
        let _ = to_client.send(last).await;
    }

    let mut frame_rx = frame_session.subscribe();

    // Stream frames to viewer until disconnect.
    loop {
        tokio::select! {
            frame = frame_rx.recv() => {
                match frame {
                    Ok(f) => {
                        if to_client.send(f).await.is_err() {
                            break; // viewer disconnected
                        }
                    }
                    Err(tokio::sync::broadcast::error::RecvError::Lagged(n)) => {
                        warn!("[session={}] viewer '{}' lagged by {} frames", session_id, participant.display_name, n);
                        // Continue — they just miss some frames
                    }
                    Err(tokio::sync::broadcast::error::RecvError::Closed) => {
                        break; // owner disconnected
                    }
                }
            }
            msg = from_client.recv() => {
                match msg {
                    Some(bytes) => {
                        let instr = match GuacamoleParser::parse_instruction(&bytes) {
                            Ok(i) => i,
                            Err(_) => continue,
                        };
                        let opcode: &str = instr.opcode;
                        // Read privileges LIVE from the registry on every input event.
                        // The owner may revoke/change them mid-session; using the snapshot
                        // captured at accept_join would let a revoked viewer keep control/drawing
                        // after it was taken away. A missing GUID (fully revoked) yields 0.
                        let privs = share_session.get_privileges(guid).unwrap_or(0);
                        match opcode {
                            "key" | "mouse" if privs & PRIV_CONTROL != 0 => {
                                // Forward key/mouse to owner's input channel so the owner's
                                // protocol handler sends it to the remote host.
                                if let Some(owner_session) = lookup(&share_session.session_id) {
                                    if !owner_session.forward_viewer_input(bytes) {
                                        warn!(
                                            "[session={}] viewer '{}' control input dropped — \
                                             owner handler has not registered a viewer_input channel",
                                            session_id, participant.display_name
                                        );
                                    }
                                }
                            }
                            "draw_event" if privs & PRIV_DRAWING != 0 => {
                                match parse_draw_event(&instr.args) {
                                    Ok(ev) => {
                                        let encoded = encode_draw_event(&ev);
                                        if let Some(owner_session) =
                                            lookup(&share_session.session_id)
                                        {
                                            let _ = owner_session.broadcast(encoded);
                                        }
                                    }
                                    Err(e) => {
                                        warn!(
                                            "[session={}] viewer '{}' draw_event parse error: {}",
                                            session_id, participant.display_name, e
                                        );
                                    }
                                }
                            }
                            _ => {} // other opcodes silently dropped
                        }
                    }
                    None => break, // viewer closed their side
                }
            }
        }
    }

    share_session.mark_disconnected(guid);

    // Broadcast updated participant list.
    let all = share_session.participant_list();
    let update = encode_participant_update(&all, false);
    if let Some(owner_session) = lookup(&share_session.session_id) {
        let _ = owner_session.broadcast(update);
    }

    info!(
        "[session={}] Viewer '{}' disconnected",
        session_id, participant.display_name
    );

    Some(Ok(()))
}

/// Handle a share_create control message in a running owner session.
///
/// Generates a GUID, stores the invitation, sends `share_created` back to the vault.
pub async fn handle_share_create(
    session_id: &str,
    display_name: String,
    privileges: u8,
    passthrough: Vec<u8>,
    to_client: &mpsc::Sender<Bytes>,
) -> Option<uuid::Uuid> {
    use crate::share_control::encode_share_created;
    use crate::share_registry::get_share_session;

    let share_session = get_share_session(session_id)?;
    let guid = share_session.add_invitation(display_name, privileges, passthrough.clone());

    let response = encode_share_created(guid, &passthrough);
    let _ = to_client.send(response).await;

    info!(
        "[session={}] Share invitation created: guid={}",
        session_id, guid
    );
    Some(guid)
}

/// Handle an incoming share control instruction from the session owner.
///
/// Parses `share_create`, `share_revoke`, `privilege_change`, and `admin_takeover`
/// instructions and applies them to the share registry. Broadcasts participant-list
/// updates back through the session frame channel.
///
/// Returns `true` if the opcode was a share control message (even if malformed),
/// `false` if the caller should continue processing the instruction normally.
pub async fn handle_owner_share_control(
    session_id: &str,
    opcode: &str,
    args: &[&str],
    to_client: &mpsc::Sender<Bytes>,
) -> bool {
    use crate::share_control::{
        encode_admin_takeover_notice, encode_participant_update, parse, ShareControl,
    };
    use crate::share_registry::get_share_session;

    let msg = match parse(opcode, args) {
        Some(Ok(m)) => m,
        Some(Err(e)) => {
            warn!("[session={}] share control parse error: {}", session_id, e);
            return true;
        }
        None => return false,
    };

    match msg {
        ShareControl::Create {
            display_name,
            privileges,
            passthrough,
        } => {
            ensure_share_session(session_id, "Owner");
            handle_share_create(session_id, display_name, privileges, passthrough, to_client).await;
        }
        ShareControl::Revoke { guid } => {
            if let Some(share) = get_share_session(session_id) {
                share.revoke(guid);
                let update = encode_participant_update(&share.participant_list(), false);
                if let Some(owner_session) = lookup(session_id) {
                    let _ = owner_session.broadcast(update);
                } else {
                    let _ = to_client.send(update).await;
                }
            }
        }
        ShareControl::PrivilegeChange {
            guid,
            new_privileges,
        } => {
            if let Some(share) = get_share_session(session_id) {
                share.set_privileges(guid, new_privileges);
                let update = encode_participant_update(&share.participant_list(), false);
                if let Some(owner_session) = lookup(session_id) {
                    let _ = owner_session.broadcast(update);
                } else {
                    let _ = to_client.send(update).await;
                }
            }
        }
        ShareControl::AdminTakeover {
            admin_name,
            admin_privileges,
            owner_new_privileges,
        } => {
            if let Some(share) = get_share_session(session_id) {
                let _admin_guid =
                    share.add_invitation(admin_name.clone(), admin_privileges, vec![]);
                share.set_privileges(share.owner_guid, owner_new_privileges);
                let notice = encode_admin_takeover_notice(&admin_name, owner_new_privileges);
                let update = encode_participant_update(&share.participant_list(), true);
                if let Some(owner_session) = lookup(session_id) {
                    let _ = owner_session.broadcast(notice);
                    let _ = owner_session.broadcast(update);
                } else {
                    let _ = to_client.send(notice).await;
                    let _ = to_client.send(update).await;
                }
            }
        }
    }

    true
}

/// Ensure a share session exists for the owner before handling share_create messages.
/// Creates one lazily the first time a share_create arrives.
pub fn ensure_share_session(session_id: &str, owner_display_name: &str) {
    use crate::share_registry::{
        create_share_session, get_share_session, PRIV_CLIPBOARD, PRIV_CONTROL, PRIV_VIEW,
    };

    if get_share_session(session_id).is_none() {
        create_share_session(
            session_id,
            owner_display_name.to_string(),
            PRIV_VIEW | PRIV_CONTROL | PRIV_CLIPBOARD,
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::share_registry::{get_share_session, remove_share_session, ParticipantStatus};
    use base64::{engine::general_purpose::STANDARD as B64, Engine};
    use tokio::sync::mpsc;

    fn unique_id() -> String {
        use std::sync::atomic::{AtomicU64, Ordering};
        static CTR: AtomicU64 = AtomicU64::new(0);
        format!("$test-viewer-{}", CTR.fetch_add(1, Ordering::Relaxed))
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_create() {
        let id = unique_id();
        let (tx, mut rx) = mpsc::channel(8);

        let pt = B64.encode(b"passthrough-data");
        let args = ["Alice", "03", pt.as_str()];
        let handled = handle_owner_share_control(&id, "share_create", &args, &tx).await;
        assert!(handled);

        // Should have sent share_created back
        let msg = rx.try_recv().expect("share_created not sent");
        let s = std::str::from_utf8(&msg).unwrap();
        assert!(s.contains("share_created"));

        // Registry should now have Alice as Pending
        let share = get_share_session(&id).expect("share session missing");
        let participants = share.participant_list();
        // owner (Connected) + Alice (Pending)
        assert_eq!(participants.len(), 2);
        let alice = participants
            .iter()
            .find(|p| p.display_name == "Alice")
            .expect("Alice not found");
        assert_eq!(alice.status, ParticipantStatus::Pending);
        assert_eq!(alice.privileges, 0x03);

        remove_share_session(&id);
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_revoke() {
        let id = unique_id();
        ensure_share_session(&id, "Owner");
        let share = get_share_session(&id).unwrap();
        let guid = share.add_invitation("Bob".into(), 0x01, vec![]);

        let (tx, _rx) = mpsc::channel(8);
        let handled =
            handle_owner_share_control(&id, "share_revoke", &[guid.to_string().as_str()], &tx)
                .await;
        assert!(handled);

        // Bob should be gone
        assert!(share.accept_join(guid).is_err());
        remove_share_session(&id);
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_privilege_change() {
        let id = unique_id();
        ensure_share_session(&id, "Owner");
        let share = get_share_session(&id).unwrap();
        let guid = share.add_invitation("Carol".into(), 0x01, vec![]);

        let (tx, _rx) = mpsc::channel(8);
        let handled = handle_owner_share_control(
            &id,
            "privilege_change",
            &[guid.to_string().as_str(), "07"],
            &tx,
        )
        .await;
        assert!(handled);

        let carol = share
            .participant_list()
            .into_iter()
            .find(|p| p.guid == guid)
            .unwrap();
        assert_eq!(carol.privileges, 0x07);
        remove_share_session(&id);
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_unknown_opcode() {
        let id = unique_id();
        let (tx, _rx) = mpsc::channel(8);
        let handled = handle_owner_share_control(&id, "key", &["65507", "1"], &tx).await;
        assert!(
            !handled,
            "key opcode should not be handled as share control"
        );
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_admin_takeover() {
        let id = unique_id();
        ensure_share_session(&id, "Owner");
        let share = get_share_session(&id).unwrap();
        let owner_guid = share.owner_guid;

        let (tx, _rx) = mpsc::channel(8);
        let handled =
            handle_owner_share_control(&id, "admin_takeover", &["Admin", "07", "01"], &tx).await;
        assert!(handled);

        // Owner should be demoted to view-only
        let owner = share
            .participant_list()
            .into_iter()
            .find(|p| p.guid == owner_guid)
            .unwrap();
        assert_eq!(owner.privileges, 0x01);

        // Admin slot should exist as Pending
        let admin = share
            .participant_list()
            .into_iter()
            .find(|p| p.display_name == "Admin")
            .unwrap();
        assert_eq!(admin.privileges, 0x07);
        assert_eq!(admin.status, ParticipantStatus::Pending);

        remove_share_session(&id);
    }
}

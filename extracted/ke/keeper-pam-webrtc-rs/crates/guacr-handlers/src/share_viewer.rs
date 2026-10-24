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

use crate::session_sharing::{lookup, ViewerInput};
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

    // Accept the existing invitation; lifetime signals remain sticky across setup races.
    let participant = match share_session.accept_join(guid) {
        Ok(p) => p,
        Err(reason) => {
            let _ = to_client.send(encode_join_rejected(reason)).await;
            let _ = send_disconnect(to_client).await;
            return Some(Err(HandlerError::ConnectionFailed(reason.into())));
        }
    };
    let mut share_ended = share_session.cancellation();
    let Some(mut participant_ended) = share_session.participant_cancellation(guid) else {
        share_session.mark_disconnected(guid);
        return Some(Ok(()));
    };

    // Keep only receivers and a weak capability to THIS generation, never a sender-owning
    // SessionHandle or a lookup by ID that could route input into a replacement owner.
    // The invitation's weak generation identity, not a fresh registry lookup, selects
    // the frame owner. A pending old GUID can never attach to a replacement session.
    let subscription = share_session.subscribe_frames(encode_participant_update(
        &share_session.participant_list(),
        false,
    ));
    let Some((mut subscription, last)) = subscription else {
        share_session.mark_disconnected(guid);
        return Some(Err(HandlerError::ConnectionFailed(
            "Session frame channel not found".into(),
        )));
    };
    let mut frame_ended = subscription.ended.clone();

    info!(
        "[session={}] Viewer '{}' joined with privileges 0x{:02x}",
        session_id, participant.display_name, participant.privileges
    );

    // One cancellation boundary covers EVERY awaited send, including accepted join,
    // cached state and ordinary output, not just the broadcast receive select.
    let result = tokio::select! {
        biased;
        _ = frame_ended.cancelled() => Ok(()),
        _ = share_ended.cancelled() => Ok(()),
        _ = participant_ended.cancelled() => Ok(()),
        result = async {
            if to_client.send(encode_join_accepted(participant.privileges)).await.is_err() {
                return Ok(());
            }
            if let Some(last) = last {
                if to_client.send(last).await.is_err() {
                    return Ok(());
                }
            }

            loop {
                tokio::select! {
                    _ = to_client.closed() => return Ok(()),
                    frame = subscription.rx.recv() => {
                        match frame {
                            Ok(frame) => {
                                if to_client.send(frame).await.is_err() {
                                    return Ok(());
                                }
                            }
                            Err(tokio::sync::broadcast::error::RecvError::Lagged(n)) => {
                                warn!("[session={}] viewer '{}' lost {} instructions", session_id, participant.display_name, n);
                                return Err(HandlerError::ConnectionFailed(
                                    "Viewer output lagged; display stream is incomplete".into(),
                                ));
                            }
                            Err(tokio::sync::broadcast::error::RecvError::Closed) => return Ok(()),
                        }
                    }
                    msg = from_client.recv() => {
                        let Some(bytes) = msg else { return Ok(()); };
                        let instr = match GuacamoleParser::parse_instruction(&bytes) {
                            Ok(i) => i,
                            Err(_) => continue,
                        };
                        let privs = share_session.get_privileges(guid).unwrap_or(0);
                        if privs & PRIV_VIEW == 0 {
                            return Ok(());
                        }
                        match instr.opcode {
                            "key" | "mouse" if privs & PRIV_CONTROL != 0 => {
                                let input = ViewerInput {
                                    bytes,
                                    guid,
                                    display_name: participant.display_name.clone(),
                                };
                                if !subscription.forward_viewer_input(input) {
                                    warn!("[session={}] viewer '{}' input channel unavailable", session_id, participant.display_name);
                                }
                            }
                            "draw_event" if privs & PRIV_DRAWING != 0 => {
                                match parse_draw_event(&instr.args) {
                                    Ok(ev) => { subscription.broadcast_control(encode_draw_event(&ev)); }
                                    Err(e) => warn!("[session={}] viewer '{}' draw_event parse error: {}", session_id, participant.display_name, e),
                                }
                            }
                            _ => {}
                        }
                    }
                }
            }
        } => result,
    };

    // Cleanup never awaits a transport send. Terminal generation weak capabilities
    // are inert; a live generation can still receive the permitted participant update.
    share_session.mark_disconnected(guid);
    subscription.broadcast_control(encode_participant_update(
        &share_session.participant_list(),
        false,
    ));
    info!(
        "[session={}] Viewer '{}' disconnected",
        session_id, participant.display_name
    );
    Some(result)
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
                    let _ = owner_session.broadcast_control(update);
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
                    let _ = owner_session.broadcast_control(update);
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
                    let _ = owner_session.broadcast_control(notice);
                    let _ = owner_session.broadcast_control(update);
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

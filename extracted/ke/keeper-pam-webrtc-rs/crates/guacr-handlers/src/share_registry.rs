// Session sharing privilege registry — Phase 6b
//
// Manages the GUID → participant → privilege map for live shared sessions.
// Distinct from session_sharing.rs (frame broadcast) — this owns the
// invitation lifecycle, privilege enforcement, and viewer join path.
//
// See crates/guacr/docs/SESSION_SHARING.md for the full design.

use dashmap::{mapref::entry::Entry, DashMap};
use once_cell::sync::Lazy;
use std::sync::Arc;
use tokio::sync::watch;

use crate::session_sharing::{
    self, SessionCancellation, SessionGeneration, SessionHandle, SessionSubscription,
};
use uuid::Uuid;

// ── Privilege bitfield ────────────────────────────────────────────────────────

/// `view` — receive the screen stream. All participants have this.
pub const PRIV_VIEW: u8 = 0x01;
/// `control` — send mouse and keyboard to the remote host.
pub const PRIV_CONTROL: u8 = 0x02;
/// `clipboard` — sync clipboard between participant and the session.
pub const PRIV_CLIPBOARD: u8 = 0x04;
/// `drawing` — draw on the canvas overlay visible to all participants.
pub const PRIV_DRAWING: u8 = 0x08;

// ── Participant ───────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParticipantStatus {
    Pending,
    Connected,
    Disconnected,
}

#[derive(Debug, Clone)]
pub struct Participant {
    pub guid: Uuid,
    pub display_name: String,
    pub privileges: u8,
    pub status: ParticipantStatus,
    /// Opaque blob from the `share_create` request, echoed back in `share_created`.
    pub passthrough: Vec<u8>,
}

impl Participant {
    pub fn has_privilege(&self, priv_bit: u8) -> bool {
        self.privileges & priv_bit != 0
    }
}

#[derive(Debug)]
struct ParticipantEntry {
    participant: Participant,
    ended: watch::Sender<bool>,
}

impl ParticipantEntry {
    fn new(participant: Participant) -> Self {
        let (ended, _) = watch::channel(false);
        Self { participant, ended }
    }
}
// ── ShareSession ─────────────────────────────────────────────────────────────

#[derive(Debug)]
pub struct ShareSession {
    /// Session ID that owns this share (for cleanup correlation).
    pub session_id: String,
    /// GUID → participant map.
    participants: DashMap<Uuid, ParticipantEntry>,
    /// The owner's participant GUID.
    pub owner_guid: Uuid,
    ended: watch::Sender<bool>,
    frame_generation: Option<SessionGeneration>,
    lifecycle: parking_lot::Mutex<()>,
}

impl ShareSession {
    fn new(session_id: String, owner_name: String, owner_privileges: u8) -> (Self, Uuid) {
        let owner_guid = Uuid::new_v4();
        let owner = Participant {
            guid: owner_guid,
            display_name: owner_name,
            privileges: owner_privileges,
            status: ParticipantStatus::Connected,
            passthrough: Vec::new(),
        };
        let participants = DashMap::new();
        participants.insert(owner_guid, ParticipantEntry::new(owner));
        let (ended, _) = watch::channel(false);
        let frame_generation =
            session_sharing::lookup(&session_id).map(|handle| handle.generation());
        let session = Self {
            session_id,
            participants,
            owner_guid,
            ended,
            frame_generation,
            lifecycle: parking_lot::Mutex::new(()),
        };
        (session, owner_guid)
    }

    /// Add a pending invitation. Returns the new GUID.
    pub fn add_invitation(
        &self,
        display_name: String,
        privileges: u8,
        passthrough: Vec<u8>,
    ) -> Uuid {
        let _lifecycle = self.lifecycle.lock();
        let guid = Uuid::new_v4();
        if self.is_live() {
            self.participants.insert(
                guid,
                ParticipantEntry::new(Participant {
                    guid,
                    display_name,
                    privileges,
                    status: ParticipantStatus::Pending,
                    passthrough,
                }),
            );
        }
        guid
    }

    /// Accept a viewer join — moves Pending → Connected.
    /// Returns Err if GUID not found, already connected, or already disconnected.
    pub fn accept_join(&self, guid: Uuid) -> Result<Participant, &'static str> {
        let _lifecycle = self.lifecycle.lock();
        if !self.is_live() {
            return Err("Session expired");
        }
        let mut entry = self
            .participants
            .get_mut(&guid)
            .ok_or("GUID not found or session expired")?;
        if !self.is_live() {
            return Err("Session expired");
        }
        if entry.participant.status != ParticipantStatus::Pending {
            return Err("GUID already used or already connected");
        }
        if entry.participant.privileges & PRIV_VIEW == 0 || *entry.ended.borrow() {
            return Err("No view privilege");
        }
        entry.participant.status = ParticipantStatus::Connected;
        Ok(entry.participant.clone())
    }

    /// Revoke a pending or connected participant by GUID.
    pub fn revoke(&self, guid: Uuid) {
        if let Some((_, entry)) = self.participants.remove(&guid) {
            entry.ended.send_replace(true);
        }
    }

    /// Update privileges for a participant.
    pub fn set_privileges(&self, guid: Uuid, new_privileges: u8) -> bool {
        if let Some(mut p) = self.participants.get_mut(&guid) {
            p.participant.privileges = new_privileges;
            if new_privileges & PRIV_VIEW == 0 {
                p.ended.send_replace(true);
            }
            true
        } else {
            false
        }
    }

    /// Current privileges for a participant by GUID, or `None` if the GUID is
    /// not present (revoked / unknown).
    ///
    /// Viewers MUST consult this per input event rather than caching the value
    /// returned by [`accept_join`](Self::accept_join): an owner can revoke or
    /// change privileges mid-session, and a cached snapshot would let a viewer
    /// keep control/drawing after it was taken away.
    pub fn get_privileges(&self, guid: Uuid) -> Option<u8> {
        if !self.is_live() {
            return None;
        }
        self.participants
            .get(&guid)
            .map(|p| p.participant.privileges)
    }

    /// Snapshot of all participants (for broadcast to viewers).
    pub fn participant_list(&self) -> Vec<Participant> {
        self.participants
            .iter()
            .map(|e| e.participant.clone())
            .collect()
    }

    /// Mark a participant disconnected (but keep their slot for audit).
    pub fn mark_disconnected(&self, guid: Uuid) {
        if let Some(mut p) = self.participants.get_mut(&guid) {
            p.participant.status = ParticipantStatus::Disconnected;
            p.ended.send_replace(true);
        }
    }

    pub(crate) fn cancellation(&self) -> SessionCancellation {
        SessionCancellation::subscribe(&self.ended)
    }

    pub(crate) fn participant_cancellation(&self, guid: Uuid) -> Option<SessionCancellation> {
        self.participants
            .get(&guid)
            .map(|p| SessionCancellation::subscribe(&p.ended))
    }

    fn is_live(&self) -> bool {
        !*self.ended.borrow()
            && self
                .frame_generation
                .as_ref()
                .is_none_or(SessionGeneration::is_live)
    }

    pub(crate) fn subscribe_frames(
        &self,
        update: bytes::Bytes,
    ) -> Option<(SessionSubscription, Option<bytes::Bytes>)> {
        if !self.is_live() {
            return None;
        }
        self.frame_generation.as_ref()?.subscribe_viewer(update)
    }

    fn end(&self) {
        let _lifecycle = self.lifecycle.lock();
        self.ended.send_replace(true);
        for mut p in self.participants.iter_mut() {
            p.participant.status = ParticipantStatus::Disconnected;
            p.ended.send_replace(true);
        }
    }
}

// ── Global SessionShareRegistry ───────────────────────────────────────────────

/// Global privilege registry. One entry per live session that has sharing active.
static SHARE_REGISTRY: Lazy<DashMap<String, Arc<ShareSession>>> = Lazy::new(DashMap::new);

/// Create a share session for the given session_id (owner is auto-added as Connected).
/// Returns the `ShareSession` handle and the owner's GUID.
pub fn create_share_session(
    session_id: &str,
    owner_name: String,
    owner_privileges: u8,
) -> (Arc<ShareSession>, Uuid) {
    let (session, owner_guid) =
        ShareSession::new(session_id.to_string(), owner_name, owner_privileges);
    let session = Arc::new(session);
    publish_share_session(&session);
    (session, owner_guid)
}

/// Admission is checked while holding the destination entry. An old captured
/// generation cannot replace/end a fresh share before discovering it is stale.
fn publish_share_session(session: &Arc<ShareSession>) -> bool {
    let previous = match SHARE_REGISTRY.entry(session.session_id.clone()) {
        Entry::Occupied(mut entry) => {
            if !session.is_live()
                || (session.frame_generation.is_none() && entry.get().frame_generation.is_some())
            {
                drop(entry);
                session.end();
                return false;
            }
            Some(entry.insert(Arc::clone(session)))
        }
        Entry::Vacant(entry) => {
            if !session.is_live() {
                drop(entry);
                session.end();
                return false;
            }
            entry.insert(Arc::clone(session));
            None
        }
    };
    // Never hold a registry guard while taking the participant lifecycle lock.
    if let Some(previous) = previous {
        previous.end();
    }
    true
}

/// Look up the share session for a session_id.
pub fn get_share_session(session_id: &str) -> Option<Arc<ShareSession>> {
    SHARE_REGISTRY
        .get(session_id)
        .filter(|e| e.is_live())
        .map(|e| Arc::clone(&e))
}

/// Remove the share session and invalidate all pending GUIDs.
pub fn remove_share_session(session_id: &str) {
    if let Some((_, session)) = SHARE_REGISTRY.remove(session_id) {
        session.end();
    }
}

/// Retire only the share bound to this frame owner, never a replacement share.
pub(crate) fn retire_frame_share(session_id: &str, handle: &SessionHandle) {
    if let Some((_, share)) = SHARE_REGISTRY.remove_if(session_id, |_, share| {
        share
            .frame_generation
            .as_ref()
            .is_some_and(|generation| generation.matches(handle))
    }) {
        share.end();
    }
}

/// Look up a share session by GUID (for viewer join — O(n) scan across sessions).
/// In practice sessions are short-lived and few, so this is acceptable.
pub fn find_session_by_guid(guid: Uuid) -> Option<Arc<ShareSession>> {
    SHARE_REGISTRY
        .iter()
        .find(|e| e.is_live() && e.participants.contains_key(&guid))
        .map(|e| Arc::clone(&e))
}

// private-type test, cannot move to src/tests/: stages private capture/publication separately.
#[cfg(test)]
mod publication_tests {
    use super::*;
    use bytes::Bytes;

    #[tokio::test]
    async fn stale_capture_publication_preserves_fresh_share_guid_and_output() {
        let id = format!("$stale-share-publication-{}", Uuid::new_v4());
        let old_frame = session_sharing::register(&id).unwrap();
        let (stale, _) = ShareSession::new(id.clone(), "Stale Owner".into(), PRIV_VIEW);
        let stale = Arc::new(stale);
        let stale_guid = stale.add_invitation("Stale Viewer".into(), PRIV_VIEW, vec![]);
        // Controlled interleaving: capture A, end A, publish B, then publish stale A.
        session_sharing::deregister(&id);
        let fresh_frame = session_sharing::register(&id).unwrap();
        let (fresh, _) = create_share_session(&id, "Fresh Owner".into(), PRIV_VIEW);
        let fresh_guid = fresh.add_invitation("Fresh Viewer".into(), PRIV_VIEW, vec![]);
        assert!(!publish_share_session(&stale));
        assert!(Arc::ptr_eq(&get_share_session(&id).unwrap(), &fresh));
        assert!(find_session_by_guid(stale_guid).is_none());
        assert!(Arc::ptr_eq(
            &find_session_by_guid(fresh_guid).unwrap(),
            &fresh
        ));
        assert!(stale.accept_join(stale_guid).is_err());
        let params =
            std::collections::HashMap::from([("share_guid".into(), fresh_guid.to_string())]);
        let (tx, mut rx) = tokio::sync::mpsc::channel(8);
        let (input_tx, input_rx) = tokio::sync::mpsc::channel(4);
        let viewer = crate::share_viewer::check_viewer_join(
            &params,
            &tx,
            input_rx,
            "fresh-viewer-transport",
        );
        tokio::pin!(viewer);
        let accepted = tokio::select! {
            result = viewer.as_mut() => panic!("fresh viewer failed to join: {result:?}"),
            accepted = tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv()) => accepted.unwrap().unwrap(),
        };
        assert_eq!(
            guacr_protocol::GuacamoleParser::parse_instruction(&accepted)
                .unwrap()
                .opcode,
            "share_join_accepted"
        );
        let output = Bytes::from_static(b"fresh-generation-output");
        fresh_frame.broadcast(output.clone());
        let delivered = tokio::select! {
            result = viewer.as_mut() => panic!("fresh viewer ended before output: {result:?}"),
            delivered = tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv()) => delivered.unwrap().unwrap(),
        };
        assert_eq!(delivered, output);
        session_sharing::deregister_owner(&id, &old_frame);
        assert!(Arc::ptr_eq(&get_share_session(&id).unwrap(), &fresh));
        session_sharing::deregister(&id);
        assert!(
            tokio::time::timeout(std::time::Duration::from_secs(1), viewer)
                .await
                .unwrap()
                .unwrap()
                .is_ok()
        );
        assert!(input_tx.is_closed());
        remove_share_session(&id);
    }
}

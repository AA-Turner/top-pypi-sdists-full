// Session sharing privilege registry — Phase 6b
//
// Manages the GUID → participant → privilege map for live shared sessions.
// Distinct from session_sharing.rs (frame broadcast) — this owns the
// invitation lifecycle, privilege enforcement, and viewer join path.
//
// See crates/guacr/docs/SESSION_SHARING.md for the full design.

use dashmap::DashMap;
use once_cell::sync::Lazy;
use std::sync::Arc;
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

// ── ShareSession ─────────────────────────────────────────────────────────────

#[derive(Debug)]
pub struct ShareSession {
    /// Session ID that owns this share (for cleanup correlation).
    pub session_id: String,
    /// GUID → participant map.
    participants: DashMap<Uuid, Participant>,
    /// The owner's participant GUID.
    pub owner_guid: Uuid,
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
        participants.insert(owner_guid, owner);
        let session = Self {
            session_id,
            participants,
            owner_guid,
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
        let guid = Uuid::new_v4();
        self.participants.insert(
            guid,
            Participant {
                guid,
                display_name,
                privileges,
                status: ParticipantStatus::Pending,
                passthrough,
            },
        );
        guid
    }

    /// Accept a viewer join — moves Pending → Connected.
    /// Returns Err if GUID not found, already connected, or already disconnected.
    pub fn accept_join(&self, guid: Uuid) -> Result<Participant, &'static str> {
        let mut entry = self
            .participants
            .get_mut(&guid)
            .ok_or("GUID not found or session expired")?;
        if entry.status != ParticipantStatus::Pending {
            return Err("GUID already used or already connected");
        }
        entry.status = ParticipantStatus::Connected;
        Ok(entry.clone())
    }

    /// Revoke a pending or connected participant by GUID.
    pub fn revoke(&self, guid: Uuid) {
        self.participants.remove(&guid);
    }

    /// Update privileges for a participant.
    pub fn set_privileges(&self, guid: Uuid, new_privileges: u8) -> bool {
        if let Some(mut p) = self.participants.get_mut(&guid) {
            p.privileges = new_privileges;
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
        self.participants.get(&guid).map(|p| p.privileges)
    }

    /// Snapshot of all participants (for broadcast to viewers).
    pub fn participant_list(&self) -> Vec<Participant> {
        self.participants.iter().map(|e| e.clone()).collect()
    }

    /// Mark a participant disconnected (but keep their slot for audit).
    pub fn mark_disconnected(&self, guid: Uuid) {
        if let Some(mut p) = self.participants.get_mut(&guid) {
            p.status = ParticipantStatus::Disconnected;
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
    SHARE_REGISTRY.insert(session_id.to_string(), Arc::clone(&session));
    (session, owner_guid)
}

/// Look up the share session for a session_id.
pub fn get_share_session(session_id: &str) -> Option<Arc<ShareSession>> {
    SHARE_REGISTRY.get(session_id).map(|e| Arc::clone(&e))
}

/// Remove the share session and invalidate all pending GUIDs.
pub fn remove_share_session(session_id: &str) {
    SHARE_REGISTRY.remove(session_id);
}

/// Look up a share session by GUID (for viewer join — O(n) scan across sessions).
/// In practice sessions are short-lived and few, so this is acceptable.
pub fn find_session_by_guid(guid: Uuid) -> Option<Arc<ShareSession>> {
    SHARE_REGISTRY
        .iter()
        .find(|e| e.participants.contains_key(&guid))
        .map(|e| Arc::clone(&e))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn session_id() -> String {
        use std::sync::atomic::{AtomicU64, Ordering};
        static CTR: AtomicU64 = AtomicU64::new(0);
        format!("$test-share-{}", CTR.fetch_add(1, Ordering::Relaxed))
    }

    #[test]
    fn test_create_and_get() {
        let id = session_id();
        let (session, _owner) = create_share_session(&id, "Alice".into(), PRIV_VIEW | PRIV_CONTROL);
        assert_eq!(session.participant_list().len(), 1);
        assert!(get_share_session(&id).is_some());
        remove_share_session(&id);
        assert!(get_share_session(&id).is_none());
    }

    #[test]
    fn test_invitation_lifecycle() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);

        let guid = session.add_invitation("Bob".into(), PRIV_VIEW, vec![]);
        assert_eq!(session.participant_list().len(), 2);

        // Accept
        let p = session.accept_join(guid).unwrap();
        assert_eq!(p.status, ParticipantStatus::Connected);

        // Can't join twice
        assert!(session.accept_join(guid).is_err());

        remove_share_session(&id);
    }

    #[test]
    fn test_revoke_pending() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);
        session.revoke(guid);
        assert!(session.accept_join(guid).is_err());
        remove_share_session(&id);
    }

    #[test]
    fn test_privilege_change() {
        let id = session_id();
        let (session, owner_guid) =
            create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);
        session.set_privileges(owner_guid, PRIV_VIEW);
        let p = session
            .participant_list()
            .into_iter()
            .find(|p| p.guid == owner_guid)
            .unwrap();
        assert_eq!(p.privileges, PRIV_VIEW);
        assert!(!p.has_privilege(PRIV_CONTROL));
        remove_share_session(&id);
    }

    #[test]
    fn test_find_by_guid() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);

        let found = find_session_by_guid(guid);
        assert!(found.is_some());
        assert_eq!(found.unwrap().session_id, id);

        let not_found = find_session_by_guid(Uuid::new_v4());
        assert!(not_found.is_none());

        remove_share_session(&id);
    }

    #[test]
    fn test_get_privileges_reflects_revocation() {
        let id = session_id();
        let (session, _owner) = create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW | PRIV_CONTROL, vec![]);
        session.accept_join(guid).unwrap();
        assert_eq!(session.get_privileges(guid), Some(PRIV_VIEW | PRIV_CONTROL));
        assert!(session.set_privileges(guid, PRIV_VIEW));
        let privs = session
            .get_privileges(guid)
            .expect("participant still present");
        assert_eq!(
            privs & PRIV_CONTROL,
            0,
            "PRIV_CONTROL must be gone after revoke"
        );
        assert_eq!(privs & PRIV_VIEW, PRIV_VIEW, "PRIV_VIEW retained");
        remove_share_session(&id);
    }

    #[test]
    fn test_get_privileges_none_after_full_revoke() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW | PRIV_CONTROL, vec![]);
        session.accept_join(guid).unwrap();
        session.revoke(guid);
        assert_eq!(session.get_privileges(guid), None);
        remove_share_session(&id);
    }

    // Regression: forward_viewer_input() must return false if the owner's handler
    // never registered a viewer_input channel. Without registering the channel,
    // viewers with PRIV_CONTROL can send key/mouse events but they are silently
    // dropped. The owner's select! loop never receives them.
    //
    // This test proves the current buggy state (forward returns false before wiring)
    // and validates the fix (forward returns true and delivers bytes after wiring).
    #[test]
    fn test_viewer_input_forwarding_requires_channel_registration() {
        use crate::session_sharing;
        use bytes::Bytes;

        let id = session_id();
        // Register as if we're the owner handler calling session_sharing::register().
        let handle = session_sharing::register(&id).unwrap();

        // Before set_viewer_input_channel: forward_viewer_input returns false.
        let dropped = !handle.forward_viewer_input(Bytes::from_static(b"4.key,1.1,1.0;"));
        assert!(
            dropped,
            "input must be dropped when no channel is registered"
        );

        // Wire the channel (what the owner handler must do at session start).
        let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<Bytes>();
        handle.set_viewer_input_channel(tx);

        // After wiring: forward_viewer_input returns true and the bytes arrive.
        let delivered = handle.forward_viewer_input(Bytes::from_static(b"4.key,1.1,1.0;"));
        assert!(
            delivered,
            "input must be delivered after channel is registered"
        );
        let received = rx.try_recv().expect("bytes must arrive on channel");
        assert_eq!(received.as_ref(), b"4.key,1.1,1.0;");

        session_sharing::deregister(&id);
    }
}

//! Port of `software.amazon.kinesis.coordinator.migration.ClientVersion`.

/// ClientVersion support during upgrade from KCLv2.x to KCLv3.x.
///
/// This enum is **persisted in DynamoDB via its string name** (`name()`), so any
/// changes must be backward compatible: never reorder, remove, or reuse a value
/// name. The declared order is preserved from Java.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ClientVersion {
    /// Transient start state used during initialization of the state machine.
    ClientVersionInit,
    /// Upgrade of an application from KCLv2.x to KCLv3.x: emit WorkerMetricStats,
    /// run KCLv2.x algorithms, monitor for 3.x readiness.
    ClientVersionUpgradeFrom2x,
    /// Rollback to KCLv2.x functionality (initiated by the migration tool).
    ClientVersion2x,
    /// 3.x algorithms after the flip, retaining a rollback safety net.
    ClientVersion3xWithRollback,
    /// Terminal 3.x state, no rollback support.
    ClientVersion3x,
}

impl ClientVersion {
    /// The Java `name()` string used for DynamoDB persistence. **Wire-format
    /// contract** — must match Java exactly.
    pub fn name(&self) -> &'static str {
        match self {
            ClientVersion::ClientVersionInit => "CLIENT_VERSION_INIT",
            ClientVersion::ClientVersionUpgradeFrom2x => "CLIENT_VERSION_UPGRADE_FROM_2X",
            ClientVersion::ClientVersion2x => "CLIENT_VERSION_2X",
            ClientVersion::ClientVersion3xWithRollback => "CLIENT_VERSION_3X_WITH_ROLLBACK",
            ClientVersion::ClientVersion3x => "CLIENT_VERSION_3X",
        }
    }

    /// Java `ClientVersion.valueOf(String)` — returns `None` for unknown names
    /// (Java throws `IllegalArgumentException`; callers here treat unknown as a
    /// deserialization failure).
    pub fn from_name(s: &str) -> Option<Self> {
        match s {
            "CLIENT_VERSION_INIT" => Some(ClientVersion::ClientVersionInit),
            "CLIENT_VERSION_UPGRADE_FROM_2X" => Some(ClientVersion::ClientVersionUpgradeFrom2x),
            "CLIENT_VERSION_2X" => Some(ClientVersion::ClientVersion2x),
            "CLIENT_VERSION_3X_WITH_ROLLBACK" => Some(ClientVersion::ClientVersion3xWithRollback),
            "CLIENT_VERSION_3X" => Some(ClientVersion::ClientVersion3x),
            _ => None,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn name_round_trips_verbatim() {
        for v in [
            ClientVersion::ClientVersionInit,
            ClientVersion::ClientVersionUpgradeFrom2x,
            ClientVersion::ClientVersion2x,
            ClientVersion::ClientVersion3xWithRollback,
            ClientVersion::ClientVersion3x,
        ] {
            assert_eq!(ClientVersion::from_name(v.name()), Some(v));
        }
    }

    #[test]
    fn wire_names_are_exact() {
        assert_eq!(
            ClientVersion::ClientVersionInit.name(),
            "CLIENT_VERSION_INIT"
        );
        assert_eq!(
            ClientVersion::ClientVersionUpgradeFrom2x.name(),
            "CLIENT_VERSION_UPGRADE_FROM_2X"
        );
        assert_eq!(ClientVersion::ClientVersion2x.name(), "CLIENT_VERSION_2X");
        assert_eq!(
            ClientVersion::ClientVersion3xWithRollback.name(),
            "CLIENT_VERSION_3X_WITH_ROLLBACK"
        );
        assert_eq!(ClientVersion::ClientVersion3x.name(), "CLIENT_VERSION_3X");
    }

    #[test]
    fn from_name_unknown_is_none() {
        assert_eq!(ClientVersion::from_name("BOGUS"), None);
    }
}

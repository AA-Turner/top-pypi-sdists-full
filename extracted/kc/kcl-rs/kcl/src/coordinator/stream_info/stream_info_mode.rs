//! Port of `software.amazon.kinesis.coordinator.streamInfo.StreamInfoMode`.

/// Configuration knob controlling whether/how StreamInfo metadata tracking is
/// active.
///
/// Only `Disabled` is checked explicitly (`!= DISABLED`) throughout the
/// codebase; `TrackOnly` (and any future mode) is treated as "enabled".
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum StreamInfoMode {
    /// No metadata tracking or lifecycle control.
    Disabled,
    /// Populate metadata table, but no lifecycle control.
    TrackOnly,
}

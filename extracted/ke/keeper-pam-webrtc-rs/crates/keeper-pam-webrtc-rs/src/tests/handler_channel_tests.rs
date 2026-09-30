// Regression tests for the conversation-id -> data-channel-label mapping used
// by the handler API (open/send/close).
//
// Callers address handler connections by conversation id, but channels are
// stored under their data-channel label. `tube_registry` teardown defines the
// mapping: the "control" channel serves the tube's original conversation, and
// every other channel is keyed by its own label.
//
// A bare exact-match lookup silently misses the control-channel case, which is
// the shape every single-session consumer uses.

use crate::tube::resolve_handler_channel_label;
use std::collections::HashSet;

fn channels(labels: &[&str]) -> HashSet<String> {
    labels.iter().map(|l| l.to_string()).collect()
}

/// The bug: a session whose only channel is labelled "control" is addressed by
/// conversation id, so an exact-match lookup finds nothing and the handler
/// call fails even though the channel is right there.
#[test]
fn control_channel_resolves_from_conversation_id() {
    let present = channels(&["control"]);

    let label = resolve_handler_channel_label(
        |c| present.contains(c),
        "conv-abc",
        "conv-abc", // this tube's original conversation
    );

    assert_eq!(
        label,
        Some("control"),
        "conversation id matching the tube's original conversation must resolve \
         to the control channel"
    );
}

/// Non-control channels are keyed by their own label, so an exact match wins
/// and must take priority over the control-channel rule.
#[test]
fn explicitly_labelled_channel_wins_over_control() {
    let present = channels(&["control", "conv-abc"]);

    let label = resolve_handler_channel_label(|c| present.contains(c), "conv-abc", "conv-abc");

    assert_eq!(
        label,
        Some("conv-abc"),
        "exact label match must take priority"
    );
}

/// A conversation that this tube does not serve must NOT fall through to the
/// control channel, or data would be misrouted onto an unrelated session.
#[test]
fn foreign_conversation_does_not_borrow_the_control_channel() {
    let present = channels(&["control"]);

    let label =
        resolve_handler_channel_label(|c| present.contains(c), "someone-elses-conv", "conv-abc");

    assert_eq!(
        label, None,
        "a conversation this tube does not serve must not resolve to control"
    );
}

/// Guard against reintroducing an "any available channel" fallback: with a
/// non-matching channel present, resolution must still fail closed.
#[test]
fn unknown_conversation_never_falls_back_to_an_arbitrary_channel() {
    let present = channels(&["some-other-session"]);

    let label = resolve_handler_channel_label(|c| present.contains(c), "conv-abc", "conv-abc");

    assert_eq!(
        label, None,
        "resolution must fail closed rather than pick an arbitrary channel"
    );
}

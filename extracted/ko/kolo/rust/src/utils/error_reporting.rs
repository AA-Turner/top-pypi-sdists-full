use pyo3::exceptions::{PyException, PyRecursionError};
use pyo3::intern;
use pyo3::panic::PanicException;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyString, PyTuple};
use std::cell::{Cell, RefCell};
use std::io::Write;
use std::sync::atomic::{AtomicBool, Ordering};

/// C stack Kolo keeps in reserve before handling a tracing event.
///
/// CPython only guarantees a small margin below its recursion limit, and a
/// Kolo callback (serialization, logging, unoptimised builds) can need more
/// than that. Skipping events this close to the end loses some trace data
/// instead of overflowing the stack.
pub(crate) const STACK_RESERVE_BYTES: usize = 256 * 1024;

/// Stack an exit needs to be recorded in full, return value and locals
/// included.
const EXIT_STACK_RESERVE_BYTES: usize = STACK_RESERVE_BYTES * 3 / 4;

/// Stack below which even an exit without values isn't recorded.
///
/// The exit of a recorded entry can arrive deeper than the entry did (e.g.
/// `PY_UNWIND` while a `RecursionError` propagates), so below
/// `EXIT_STACK_RESERVE_BYTES` it is still recorded, just without the values
/// whose serialization needs the stack. Only past this last bar do we drop
/// it, leaving its entry unmatched rather than overflowing the stack.
const MINIMAL_EXIT_STACK_RESERVE_BYTES: usize = STACK_RESERVE_BYTES / 2;

/// Entries made with less stack than this are remembered until they exit.
///
/// Anything entered with more room has exited by the time the stack is this
/// close to its end again, so only this region needs bookkeeping.
pub(crate) const NEAR_STACK_END_BYTES: usize = 2 * STACK_RESERVE_BYTES;

/// How much further from the end of the stack than its entry an event can
/// be while the entered frame is still running.
///
/// An exit is reported at about the depth of its entry; the slack covers
/// CPython reaching the callback through a different path. Anything entered
/// deeper than this below an event has exited.
const ENTRY_DEPTH_SLACK_BYTES: usize = 32 * 1024;

/// Frames entered near the end of the stack on this thread which have not
/// exited yet, innermost last: those Kolo recorded, then those it skipped.
///
/// Once a frame's entry is skipped, every entry until its exit is skipped
/// too, so the skipped frames always follow the recorded ones.
struct NearEndFrames {
    /// The code object (or frame) each entry's exit reports, with the stack
    /// left when it was entered.
    entries: Vec<(usize, usize)>,
    /// How many of `entries`, from the start, Kolo recorded.
    recorded: usize,
}

impl NearEndFrames {
    fn skipping(&self) -> bool {
        self.entries.len() > self.recorded
    }

    fn push(&mut self, id: usize, remaining: usize, recorded: bool) {
        self.entries.push((id, remaining));
        if recorded {
            self.recorded = self.entries.len();
        }
    }

    /// Forget frames entered deeper in the stack than an event now running:
    /// they have exited without Kolo seeing it (e.g. CPython couldn't call
    /// Kolo for an unwind right at the stack limit). Otherwise their ids,
    /// shared by every activation of the same code, would claim the exits
    /// of the frames below them.
    fn forget_exited(&mut self, remaining: usize) {
        let exited = self
            .entries
            .iter()
            .rposition(|&(_, entered_at)| {
                entered_at.saturating_add(ENTRY_DEPTH_SLACK_BYTES) >= remaining
            })
            .map_or(0, |index| index + 1);
        self.truncate(exited);
    }

    fn find(&self, id: usize) -> Option<usize> {
        self.entries.iter().rposition(|&(entered, _)| entered == id)
    }

    fn truncate(&mut self, len: usize) {
        self.entries.truncate(len);
        self.recorded = self.recorded.min(len);
    }
}

/// Per-thread state of the stack check, in one thread-local so a callback
/// pays for a single TLS access.
struct StackGuard {
    frames: RefCell<NearEndFrames>,
    /// Whether the event being handled is recorded without its values
    /// (see `values_omitted`).
    omitting: Cell<bool>,
    /// Lowest usable stack address on this thread: 0 until first needed,
    /// `usize::MAX` when the OS doesn't say.
    #[cfg_attr(target_arch = "wasm32", allow(dead_code))]
    limit: Cell<usize>,
}

thread_local! {
    static STACK_GUARD: StackGuard = const {
        StackGuard {
            frames: RefCell::new(NearEndFrames {
                entries: Vec::new(),
                recorded: 0,
            }),
            omitting: Cell::new(false),
            limit: Cell::new(0),
        }
    };
}

/// An address in the caller's stack frame.
#[cfg(not(target_arch = "wasm32"))]
#[inline(always)]
fn stack_pointer() -> usize {
    let marker = 0u8;
    std::hint::black_box(&marker) as *const u8 as usize
}

impl StackGuard {
    /// Stack left below the caller's frame, `usize::MAX` if unknown.
    ///
    /// The same measure as `stacker::remaining_stack` (which also caches the
    /// OS stack limit per thread), without its second thread-local and its
    /// out-of-line stack pointer read on every call.
    #[cfg(not(target_arch = "wasm32"))]
    #[inline]
    fn remaining(&self) -> usize {
        let sp = stack_pointer();
        let mut limit = self.limit.get();
        if limit == 0 {
            limit = match stacker::remaining_stack() {
                Some(remaining) => sp.saturating_sub(remaining).max(1),
                None => usize::MAX,
            };
            self.limit.set(limit);
        }
        if limit == usize::MAX {
            usize::MAX
        } else {
            sp.saturating_sub(limit)
        }
    }

    #[cfg(target_arch = "wasm32")]
    #[inline]
    fn remaining(&self) -> usize {
        usize::MAX
    }
}

#[cfg(test)]
fn remaining_stack() -> usize {
    STACK_GUARD.with(StackGuard::remaining)
}

/// Run `at_end` with less than `bytes` of stack left on this thread.
#[cfg(test)]
pub(crate) fn with_stack_below(bytes: usize, at_end: &mut dyn FnMut()) {
    let padding = std::hint::black_box([0u8; 16 * 1024]);
    if remaining_stack() < bytes {
        at_end();
    } else {
        with_stack_below(bytes, at_end);
    }
    std::hint::black_box(padding);
}

/// How many frames entered near the end of the stack this thread remembers.
#[cfg(test)]
#[cfg_attr(not(Py_3_12), allow(dead_code))]
pub(crate) fn remembered_entries() -> usize {
    STACK_GUARD.with(|guard| guard.frames.borrow().entries.len())
}

#[derive(Clone, Copy)]
pub(crate) enum StackEvent {
    /// A frame starts or resumes running; identified by its code or frame
    /// pointer, the same one its exit reports (always the frame near the end
    /// of the stack).
    Enter(usize),
    /// A frame returns, yields or unwinds.
    Exit(usize),
    /// Neither, e.g. an instruction event.
    Within,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum StackDecision {
    Record,
    /// Record the exit, but not its return value, exception or locals.
    RecordWithoutValues,
    Skip,
}


/// Whether to handle this event, given how close Kolo is to the end of the
/// C stack.
///
/// Once a frame's entry is skipped we skip everything until its matching
/// exit too, so Kolo's call-frame, plugin and trace-point bookkeeping never
/// sees half of a frame. Every other exit is handled, without its values
/// below `EXIT_STACK_RESERVE_BYTES`, so the exit of an entry Kolo recorded
/// is recorded too; an exit whose entry Kolo didn't record (filtered out, or
/// a repeat after Kolo raised into the program) is ignored by the callback
/// as with room to spare. Only past `MINIMAL_EXIT_STACK_RESERVE_BYTES` is an
/// exit dropped, which costs its entry its pair.
#[inline]
pub(crate) fn check_stack(event: StackEvent) -> (StackDecision, Option<OmittingValues>) {
    let (decision, _, omitting) = check_stack_with(event, Some);
    (decision, omitting)
}

/// `check_stack`, with `near_end_id` mapping the event's id to a finer one
/// (e.g. its frame) where entries are remembered, near the end of the stack,
/// or to `None` for an exit of a frame that never started (so has no entry),
/// which is then skipped without touching the remembered entries.
/// Also returns the event as checked, with that id, and, when it changed the
/// mark `values_omitted` reads (set for `RecordWithoutValues`, cleared for a
/// full event nested in a values-free one), what to restore once the event
/// is handled.
#[inline]
pub(crate) fn check_stack_with(
    event: StackEvent,
    near_end_id: impl FnOnce(usize) -> Option<usize>,
) -> (StackDecision, StackEvent, Option<OmittingValues>) {
    STACK_GUARD.with(|guard| {
        let remaining = guard.remaining();
        // With plenty of room, nothing remembered and no outer event
        // omitting values, every event is recorded in full: the common case,
        // decided without the bookkeeping.
        if remaining >= NEAR_STACK_END_BYTES + ENTRY_DEPTH_SLACK_BYTES
            && !guard.omitting.get()
            && guard.frames.borrow().entries.is_empty()
        {
            return (StackDecision::Record, event, None);
        }
        let (decision, event) = near_end_decision(guard, event, remaining, near_end_id);
        let omit = decision == StackDecision::RecordWithoutValues;
        let omitting = (decision != StackDecision::Skip && (omit || guard.omitting.get()))
            .then(|| OmittingValues(guard.omitting.replace(omit)));
        (decision, event, omitting)
    })
}

#[inline(never)]
fn near_end_decision(
    guard: &StackGuard,
    event: StackEvent,
    remaining: usize,
    near_end_id: impl FnOnce(usize) -> Option<usize>,
) -> (StackDecision, StackEvent) {
    {
        let event = if identifies_frames(remaining) {
            match event {
                StackEvent::Enter(id) => StackEvent::Enter(near_end_id(id).unwrap_or(id)),
                StackEvent::Exit(id) => match near_end_id(id) {
                    Some(id) => StackEvent::Exit(id),
                    None => return (StackDecision::Skip, event),
                },
                StackEvent::Within => StackEvent::Within,
            }
        } else {
            event
        };
        (
            decide(&mut guard.frames.borrow_mut(), event, remaining),
            event,
        )
    }
}

/// Whether, with this much stack left, events are identified by the finer
/// id. Not past the last reserve, where every exit is dropped anyway and
/// finding the frame (which may allocate a frame object) is work Kolo
/// can't afford.
#[inline]
fn identifies_frames(remaining: usize) -> bool {
    (MINIMAL_EXIT_STACK_RESERVE_BYTES..NEAR_STACK_END_BYTES + ENTRY_DEPTH_SLACK_BYTES)
        .contains(&remaining)
}

#[inline]
fn decide(frames: &mut NearEndFrames, event: StackEvent, remaining: usize) -> StackDecision {
    // Frames exit innermost first, so with this much more room any
    // remembered frame missed its exit. (Greenlets, which swap frames on
    // the same stack, also get here: that costs pairing within a switched
    // greenlet, not safety.)
    if frames.entries.last().is_some_and(|&(_, entered_at)| {
        entered_at.saturating_add(ENTRY_DEPTH_SLACK_BYTES) < remaining
    }) {
        frames.forget_exited(remaining);
    }
    match event {
        StackEvent::Enter(id) => {
            if frames.skipping() || remaining < STACK_RESERVE_BYTES {
                frames.push(id, remaining, false);
                return StackDecision::Skip;
            }
            if remaining < NEAR_STACK_END_BYTES {
                frames.push(id, remaining, true);
            }
            StackDecision::Record
        }
        StackEvent::Exit(id) => {
            match frames.find(id) {
                Some(index) => {
                    let skipped = index >= frames.recorded;
                    // Anything entered after this frame has exited too, so a
                    // frame still listed above it missed its exit.
                    frames.truncate(index);
                    if skipped {
                        return StackDecision::Skip;
                    }
                }
                // Inside a skipped frame.
                None if frames.skipping() => return StackDecision::Skip,
                None => {}
            }
            if remaining >= EXIT_STACK_RESERVE_BYTES {
                StackDecision::Record
            } else if remaining >= MINIMAL_EXIT_STACK_RESERVE_BYTES {
                StackDecision::RecordWithoutValues
            } else {
                StackDecision::Skip
            }
        }
        StackEvent::Within if frames.skipping() || remaining < STACK_RESERVE_BYTES => {
            StackDecision::Skip
        }
        StackEvent::Within => StackDecision::Record,
    }
}

/// Whether the event being handled on this thread is recorded without its
/// return value, exception and locals: `StackDecision::RecordWithoutValues`,
/// marked for the event's duration by the `OmittingValues` the stack check
/// returns. Read where the values would be serialized (and by work such an
/// event defers), so the common path carries no extra argument.
#[inline]
pub(crate) fn values_omitted() -> bool {
    STACK_GUARD.with(|guard| guard.omitting.get())
}

/// The outer event's values-omitted mark, to `restore` once the event the
/// stack check marked is handled (callbacks nest last in, first out). Not a
/// drop guard: kept out of the hot callback path, which it would otherwise
/// give an unwind cleanup.
#[must_use]
pub(crate) struct OmittingValues(bool);

impl OmittingValues {
    #[cold]
    #[inline(never)]
    pub(crate) fn restore(self) {
        STACK_GUARD.with(|guard| guard.omitting.set(self.0));
    }

    /// Mark the current event as recorded without its values.
    #[cfg(test)]
    pub(crate) fn start() -> Self {
        Self(STACK_GUARD.with(|guard| guard.omitting.replace(true)))
    }
}

/// Whether there is stack enough to flush a subtree (Python calls, large
/// allocations); checked only once a flush is due.
pub(crate) fn room_to_flush() -> bool {
    STACK_GUARD.with(StackGuard::remaining) >= EXIT_STACK_RESERVE_BYTES
}


/// Forget the innermost entry, just recorded, of a frame Kolo then
/// filtered out of the trace (its later exits skip the stack check).
pub(crate) fn forget_entry(id: usize) {
    STACK_GUARD.with(|guard| {
        let mut frames = guard.frames.borrow_mut();
        if !frames.skipping() && frames.entries.last().map(|&(entered, _)| entered) == Some(id) {
            frames.entries.pop();
            frames.recorded = frames.entries.len();
        }
    })
}

static RECURSION_REPORTED: AtomicBool = AtomicBool::new(false);
const RECURSION_MESSAGE: &[u8] =
    b"Kolo: an internal error could not be logged because the stack is nearly exhausted; \
      further such errors are not reported.\n";

/// Emit a warning on the `kolo` logger without ever failing.
///
/// Kolo reports its own errors from inside tracing callbacks, where a Python
/// exception or Rust panic would surface in (or abort) the host program. The
/// user's logging configuration is outside our control: a handler or filter
/// can raise, and logging may be half torn down at interpreter shutdown. When
/// logging fails we hand both the original error and the logging failure to
/// `sys.unraisablehook`, which prints to stderr and never raises.
pub(crate) fn log_warning(py: Python, args: Bound<'_, PyTuple>, exc_info: Option<PyErr>) {
    let original = exc_info.as_ref().map(|err| err.clone_ref(py));
    // Only the first line: the profiler's message is a multi-line `%s`
    // template whose arguments include user locals we must not repr here.
    let summary = args
        .get_item(0)
        .ok()
        .and_then(|message| message.extract::<String>().ok())
        .and_then(|message| message.lines().next().map(str::to_owned))
        .unwrap_or_else(|| "kolo".to_owned());
    let logged = (|| -> PyResult<()> {
        let kwargs = PyDict::new(py);
        if let Some(err) = exc_info {
            kwargs.set_item(intern!(py, "exc_info"), err)?;
        }
        PyModule::import(py, intern!(py, "logging"))?
            .call_method1(intern!(py, "getLogger"), (intern!(py, "kolo"),))?
            .call_method(intern!(py, "warning"), args, Some(&kwargs))?;
        Ok(())
    })();
    if let Err(logging_error) = logged {
        if logging_error.is_instance_of::<PyRecursionError>(py) {
            // Out of stack: any further Python call, the unraisable hook
            // included, would fail the same way. Write straight to fd 2.
            if !RECURSION_REPORTED.swap(true, Ordering::Relaxed) {
                let _ = std::io::stderr().write_all(RECURSION_MESSAGE);
            }
            return;
        }
        // `write_unraisable` reports "Exception ignored in: <context>", so
        // the warning text itself survives a broken logging setup.
        let context = PyString::new(py, &format!("Kolo: {summary}"));
        if let Some(original) = original {
            original.write_unraisable(py, Some(context.as_any()));
        }
        logging_error.write_unraisable(py, Some(context.as_any()));
    }
}

/// Whether an error from a tracing callback must reach the traced program
/// instead of being logged.
///
/// A `BaseException` that is not an `Exception` (`KeyboardInterrupt`,
/// `SystemExit`, pytest's `Failed` from a timeout's signal handler) usually
/// comes from a signal handler that ran while Kolo called a user `__repr__`.
/// Logging it would swallow the interrupt, so it propagates, as it already
/// does from Kolo's Python serializer and profiler, which only catch
/// `Exception`. A `PanicException` is a Kolo bug, which Kolo reports itself.
pub(crate) fn reaches_program(py: Python, err: &PyErr) -> bool {
    !err.is_instance_of::<PyException>(py) && !err.is_instance_of::<PanicException>(py)
}

/// Report a panic caught at a tracing callback boundary.
///
/// Callers catch the panic and stop tracing; this only tells the user why,
/// through `sys.unraisablehook` so reporting itself cannot raise.
pub(crate) fn report_panic(py: Python, payload: Box<dyn std::any::Any + Send>) {
    let message = if let Some(message) = payload.downcast_ref::<String>() {
        message.clone()
    } else if let Some(message) = payload.downcast_ref::<&str>() {
        (*message).to_string()
    } else {
        "unknown panic".to_string()
    };
    let context = PyString::new(py, "Kolo stopped tracing after an internal error");
    PyErr::new::<PanicException, _>(message).write_unraisable(py, Some(&context));
}

pub(crate) fn stopped_after_panic_error() -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(
        "Kolo stopped tracing after an internal error; no trace is available",
    )
}

#[cfg(all(test, not(target_arch = "wasm32")))]
mod tests {
    use super::{
        check_stack, check_stack_with, decide, forget_entry, values_omitted, with_stack_below,
        NearEndFrames, OmittingValues, StackDecision, StackEvent,
        ENTRY_DEPTH_SLACK_BYTES, EXIT_STACK_RESERVE_BYTES, MINIMAL_EXIT_STACK_RESERVE_BYTES,
        NEAR_STACK_END_BYTES, STACK_RESERVE_BYTES,
    };
    use StackDecision::{Record, RecordWithoutValues, Skip};

    fn decision(event: StackEvent) -> StackDecision {
        check_stack(event).0
    }

    fn near_stack_end(at_end: &mut dyn FnMut()) {
        with_stack_below(STACK_RESERVE_BYTES, at_end);
    }

    fn on_small_thread(test: impl FnOnce() + Send + 'static) {
        std::thread::Builder::new()
            .stack_size(4 << 20)
            .spawn(test)
            .expect("spawn test thread")
            .join()
            .expect("test thread");
    }

    #[test]
    fn stack_skipping_keeps_enter_and_exit_paired() {
        on_small_thread(|| {
            assert_eq!(decision(StackEvent::Enter(1)), Record);
            near_stack_end(&mut || {
                // A frame entered with too little stack is skipped up to and
                // including its exit, with everything inside it.
                assert_eq!(decision(StackEvent::Enter(2)), Skip);
                assert_eq!(decision(StackEvent::Enter(3)), Skip);
                assert_eq!(decision(StackEvent::Within), Skip);
                // An exit without an entry (an undisableable unwind) doesn't
                // end frame 3.
                assert_eq!(decision(StackEvent::Exit(9)), Skip);
                assert_eq!(decision(StackEvent::Exit(3)), Skip);
                assert_eq!(decision(StackEvent::Within), Skip);
                assert_eq!(decision(StackEvent::Exit(2)), Skip);
                // The exit of a frame whose entry was traced is traced.
                assert_eq!(decision(StackEvent::Exit(1)), Record);
                // Leave a skipped frame without its exit.
                assert_eq!(decision(StackEvent::Enter(4)), Skip);
            });
            // With room again, a missed exit doesn't stop tracing.
            assert_eq!(decision(StackEvent::Within), Record);
            assert_eq!(decision(StackEvent::Exit(5)), Record);
        });
    }

    #[test]
    fn recorded_entry_near_the_end_keeps_its_exit() {
        on_small_thread(|| {
            with_stack_below(NEAR_STACK_END_BYTES, &mut || {
                // Recursion: every level reports the same code object.
                assert_eq!(decision(StackEvent::Enter(1)), Record);
                near_stack_end(&mut || {
                    assert_eq!(decision(StackEvent::Enter(2)), Skip);
                    assert_eq!(decision(StackEvent::Enter(1)), Skip);
                    assert_eq!(decision(StackEvent::Exit(1)), Skip);
                    // Frame 2 never reports its exit.
                    with_stack_below(EXIT_STACK_RESERVE_BYTES, &mut || {
                        // E.g. `PY_UNWIND` while a `RecursionError`
                        // propagates, deeper than its entry: recorded,
                        // without the values, and frame 2 is over.
                        assert_eq!(decision(StackEvent::Exit(1)), RecordWithoutValues);
                    });
                });
                assert_eq!(decision(StackEvent::Within), Record);
                assert_eq!(decision(StackEvent::Enter(3)), Record);
                assert_eq!(decision(StackEvent::Exit(3)), Record);
            });
        });
    }

    #[test]
    fn unrecorded_exit_after_its_entry_was_matched_is_still_handled() {
        on_small_thread(|| {
            with_stack_below(NEAR_STACK_END_BYTES, &mut || {
                assert_eq!(decision(StackEvent::Enter(1)), Record);
                with_stack_below(EXIT_STACK_RESERVE_BYTES, &mut || {
                    // The return matches frame 1, but Kolo raises an
                    // interrupt into the program before recording it...
                    assert_eq!(decision(StackEvent::Exit(1)), RecordWithoutValues);
                    // ...so CPython reports frame 1's exit again, now with
                    // no entry left to match. Kolo's callback records it,
                    // as the exit it still owes frame 1.
                    assert_eq!(decision(StackEvent::Exit(1)), RecordWithoutValues);
                });
            });
        });
    }

    #[test]
    fn an_exit_ends_the_frames_entered_after_it() {
        // Decisions at given stack depths (KiB left), without a real stack.
        let mut frames = NearEndFrames {
            entries: Vec::new(),
            recorded: 0,
        };
        let mut at = |event, kib: usize| decide(&mut frames, event, kib * 1024);
        assert_eq!(at(StackEvent::Enter(1), 300), Record);
        // Frame 2 is skipped, and CPython never reports its exit.
        assert_eq!(at(StackEvent::Enter(2), 250), Skip);
        // Frame 1 exits close to frame 2's depth: frame 2 is over too...
        assert_eq!(at(StackEvent::Exit(1), 270), Record);
        // ...so its sibling, entered with room again, is recorded.
        assert_eq!(at(StackEvent::Enter(3), 265), Record);
        assert_eq!(at(StackEvent::Within, 265), Record);
        assert_eq!(at(StackEvent::Exit(3), 265), Record);
    }

    #[test]
    fn forgotten_entry_cannot_be_matched_by_a_later_frame_at_its_address() {
        on_small_thread(|| {
            with_stack_below(NEAR_STACK_END_BYTES, &mut || {
                assert_eq!(decision(StackEvent::Enter(1)), Record);
                // Kolo filtered frame 2 out; its exits skip the check.
                assert_eq!(decision(StackEvent::Enter(2)), Record);
                forget_entry(2);
                assert_eq!(decision(StackEvent::Enter(3)), Record);
                near_stack_end(&mut || {
                    assert_eq!(decision(StackEvent::Enter(4)), Skip);
                    // A frame at frame 2's old address exits: it must not
                    // end frame 4's skipping (or frame 3).
                    assert_eq!(decision(StackEvent::Exit(2)), Skip);
                    assert_eq!(decision(StackEvent::Within), Skip);
                    assert_eq!(decision(StackEvent::Exit(4)), Skip);
                });
                assert_eq!(decision(StackEvent::Exit(3)), Record);
            });
        });
    }

    #[test]
    fn values_omitted_marks_only_the_event_it_was_decided_for() {
        on_small_thread(|| {
            assert!(!values_omitted());
            with_stack_below(EXIT_STACK_RESERVE_BYTES, &mut || {
                let (decision, outer) = check_stack(StackEvent::Exit(1));
                assert_eq!(decision, RecordWithoutValues);
                assert!(values_omitted());
                outer.expect("marked").restore();
            });
            assert!(!values_omitted());
            // A callback nested in a values-free one, with room, records
            // its own event in full.
            let outer = OmittingValues::start();
            let (decision, nested) = check_stack(StackEvent::Exit(2));
            assert_eq!(decision, Record);
            assert!(!values_omitted());
            nested.expect("cleared").restore();
            assert!(values_omitted());
            outer.restore();
            assert!(!values_omitted());
        });
    }

    #[test]
    fn frames_are_only_identified_between_the_last_reserve_and_the_near_end() {
        on_small_thread(|| {
            let identified = |event: StackEvent| {
                let mut called = false;
                check_stack_with(event, |id| {
                    called = true;
                    Some(id)
                });
                called
            };
            assert!(!identified(StackEvent::Within));
            assert!(!identified(StackEvent::Exit(1)));
            with_stack_below(NEAR_STACK_END_BYTES + ENTRY_DEPTH_SLACK_BYTES, &mut || {
                assert!(identified(StackEvent::Exit(1)));
                with_stack_below(MINIMAL_EXIT_STACK_RESERVE_BYTES, &mut || {
                    // Past the last reserve: no frame lookup (it can
                    // allocate), and the exit is dropped.
                    assert!(!identified(StackEvent::Enter(2)));
                    assert!(!identified(StackEvent::Exit(2)));
                    assert_eq!(decision(StackEvent::Exit(3)), Skip);
                });
            });
        });
    }

    #[test]
    fn exit_of_a_frame_that_never_started_leaves_the_entries_alone() {
        on_small_thread(|| {
            with_stack_below(NEAR_STACK_END_BYTES, &mut || {
                // Direct recursion: the caller's frame is remembered.
                assert_eq!(decision(StackEvent::Enter(1)), Record);
                near_stack_end(&mut || {
                    assert_eq!(decision(StackEvent::Enter(2)), Skip);
                    // An unwind from a call that failed before RESUME, which
                    // the frame lookup would attribute to its caller: dropped
                    // without ending frame 1 (and frame 2 above it).
                    let (stack, _, omitting) = check_stack_with(StackEvent::Exit(1), |_| None);
                    assert_eq!(stack, Skip);
                    assert!(omitting.is_none());
                    assert_eq!(decision(StackEvent::Within), Skip);
                    assert_eq!(decision(StackEvent::Exit(2)), Skip);
                });
            });
        });
    }

    #[test]
    fn exit_past_the_last_reserve_is_skipped() {
        on_small_thread(|| {
            with_stack_below(NEAR_STACK_END_BYTES, &mut || {
                assert_eq!(decision(StackEvent::Enter(1)), Record);
                with_stack_below(MINIMAL_EXIT_STACK_RESERVE_BYTES, &mut || {
                    assert_eq!(decision(StackEvent::Exit(1)), Skip);
                });
                // Its entry is gone, so a later exit isn't taken for it.
                assert_eq!(decision(StackEvent::Within), Record);
            });
        });
    }

    #[test]
    fn unmatched_exit_deep_in_the_stack_is_handled_without_values() {
        on_small_thread(|| {
            with_stack_below(EXIT_STACK_RESERVE_BYTES, &mut || {
                // E.g. `PY_UNWIND` from excluded code whose `PY_START` was
                // disabled: nothing was entered on the way down. Handled
                // like any exit this deep, without its values.
                assert_eq!(decision(StackEvent::Exit(7)), RecordWithoutValues);
                // It doesn't start skipping anything else.
                assert_eq!(decision(StackEvent::Exit(7)), RecordWithoutValues);
                with_stack_below(MINIMAL_EXIT_STACK_RESERVE_BYTES, &mut || {
                    assert_eq!(decision(StackEvent::Exit(7)), Skip);
                });
            });
            assert_eq!(decision(StackEvent::Within), Record);
            assert_eq!(decision(StackEvent::Exit(7)), Record);
        });
    }
}

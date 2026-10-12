use pyo3::exceptions::{PyException, PyRecursionError};
use pyo3::intern;
use pyo3::panic::PanicException;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyString, PyTuple};
use std::cell::{Cell, RefCell};
use std::io::Write;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};

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

/// The lowest usable address of the calling thread's stack, `usize::MAX`
/// when the OS doesn't say.
#[cfg(not(any(target_arch = "wasm32", all(target_os = "linux", target_env = "musl"))))]
fn os_stack_limit(sp: usize) -> usize {
    match stacker::remaining_stack() {
        Some(remaining) => sp.saturating_sub(remaining).max(1),
        None => usize::MAX,
    }
}

/// The lowest usable address of the calling thread's stack on musl, where
/// `stacker` can't be used.
///
/// `stacker` asks `pthread_getattr_np`. For a thread musl created, that is
/// its stack. For the stack the process started on, musl reports only the
/// pages mapped so far (about 130 KiB in a fresh process), not what the
/// kernel lets the stack grow to. Taken as the whole stack, that puts every
/// Python frame of the main thread within Kolo's reserve of the end: Kolo
/// 3.5.0 recorded nothing there.
///
/// Never `usize::MAX`: a stack musl won't describe counts as used up for
/// good, so Kolo records nothing on it (and says so, see `StackSkips`)
/// rather than run on a stack it knows nothing about.
#[cfg(all(target_os = "linux", target_env = "musl"))]
fn os_stack_limit(sp: usize) -> usize {
    /// Above any stack pointer, and not the `usize::MAX` that means unknown.
    const USED_UP: usize = usize::MAX - 1;
    let Some((mut lowest, mut top)) = musl_reported_stack() else {
        return USED_UP;
    };
    // Twice: the initial stack can grow between musl's report of it and
    // the reading of the mappings, which then disagree.
    for _ in 0..2 {
        if let Some(grows_to) = musl_initial_stack_lowest(sp, lowest, top) {
            return grows_to.min(lowest).max(1);
        }
        match musl_reported_stack() {
            Some(reported) => (lowest, top) = reported,
            None => return USED_UP,
        }
    }
    lowest.max(1)
}

/// What musl's `pthread_getattr_np` says of the calling thread's stack: its
/// lowest address and the address just past its highest.
#[cfg(all(target_os = "linux", target_env = "musl"))]
fn musl_reported_stack() -> Option<(usize, usize)> {
    let mut attr = std::mem::MaybeUninit::<libc::pthread_attr_t>::uninit();
    // SAFETY: `pthread_getattr_np` initializes `attr` when it succeeds, and
    // only then is it read and destroyed.
    let (lowest, size) = unsafe {
        if libc::pthread_getattr_np(libc::pthread_self(), attr.as_mut_ptr()) != 0 {
            return None;
        }
        let mut address = std::ptr::null_mut();
        let mut size = 0;
        let found = libc::pthread_attr_getstack(attr.as_ptr(), &mut address, &mut size) == 0;
        libc::pthread_attr_destroy(attr.as_mut_ptr());
        found.then_some((address as usize, size))?
    };
    Some((lowest, lowest.checked_add(size)?))
}

/// How far down the stack `sp` is on can grow, if it is the stack the
/// process started on. `None` for any other stack, and whenever that can't
/// be established: then only what musl reported counts.
///
/// As glibc's `pthread_getattr_np` works it out, from `RLIMIT_STACK` and
/// the process's mappings (see `initial_stack_growth_limit`). Like every platform's limit here it is measured
/// once per thread: a limit lowered, or a mapping placed under the stack,
/// after that is not seen.
#[cfg(all(target_os = "linux", target_env = "musl"))]
fn musl_initial_stack_lowest(sp: usize, lowest: usize, top: usize) -> Option<usize> {
    // The kernel puts AT_RANDOM's bytes on the initial stack, just above
    // the auxiliary vector whose page musl takes that stack's top from. Far
    // from them this is a thread's stack, and the mappings needn't be read.
    // (`gettid() == getpid()` alone won't do: after a fork from another
    // thread that thread is the main one, on the stack musl created for it.)
    // SAFETY: `getauxval` only reads the process's auxiliary vector.
    let random = unsafe { libc::getauxval(libc::AT_RANDOM) } as usize;
    if random == 0 || random.abs_diff(top) > INITIAL_STACK_MARGIN_BYTES || sp < lowest {
        return None;
    }
    // Only the main thread runs on the initial stack as such. Another
    // thread can be given a buffer inside it for a stack
    // (`pthread_attr_setstack`), which ends where musl said.
    // SAFETY: both calls take no arguments and cannot fail.
    let (thread, process) = unsafe { (libc::syscall(libc::SYS_gettid), libc::getpid()) };
    if thread != libc::c_long::from(process) {
        return None;
    }
    let mut limit = libc::rlimit {
        rlim_cur: 0,
        rlim_max: 0,
    };
    // SAFETY: `limit` is a valid `rlimit` to write to.
    if unsafe { libc::getrlimit(libc::RLIMIT_STACK, &mut limit) } != 0 {
        return None;
    }
    let limit = if limit.rlim_cur == libc::RLIM_INFINITY {
        usize::MAX
    } else {
        usize::try_from(limit.rlim_cur).unwrap_or(usize::MAX)
    };
    // SAFETY: `sysconf` has no preconditions.
    let page = usize::try_from(unsafe { libc::sysconf(libc::_SC_PAGESIZE) }).ok()?;
    let command_line = std::fs::read_to_string("/proc/cmdline").ok()?;
    let guard_gap = stack_guard_gap_pages(&command_line)?.checked_mul(page)?;
    let mappings = std::fs::read_to_string("/proc/self/smaps").ok()?;
    initial_stack_growth_limit(
        &mappings,
        sp,
        random,
        limit,
        guard_gap,
        INITIAL_STACK_MAX_BYTES,
        lowest,
    )
}

/// Left unused at the low end of the initial stack on musl: its bounds are
/// worked out, not reported.
#[cfg(any(test, all(target_os = "linux", target_env = "musl")))]
const INITIAL_STACK_MARGIN_BYTES: usize = 128 * 1024;

/// How far below where the process started the initial stack is taken to
/// end on musl, whatever more `RLIMIT_STACK` allows.
///
/// CPython 3.14 bounds recursion by the C stack, and Kolo's reserve is laid
/// out for that: where both read the real limit, CPython's own soft limit
/// is 32 KiB above it, well inside the reserve, so Kolo stops recording
/// before Python calls start to fail. On musl CPython doesn't read the
/// limit either. It takes every thread, the main one included, to have as
/// much stack as it links its threads with there, 1 MiB
/// (`_Py_LINKER_THREAD_STACK_SIZE`), below where the interpreter first ran
/// on it. Kolo's limit for the initial stack has to be no lower than that,
/// though the stack goes on (to 8 MiB as a rule), or its callbacks run
/// exactly where every Python call raises `RecursionError`. (3.14.0 took
/// 4 MB, which this is only cautious for.)
#[cfg(all(Py_3_14, target_os = "linux", target_env = "musl"))]
const INITIAL_STACK_MAX_BYTES: usize = 1 << 20;

/// Before 3.14 the C stack doesn't bound recursion: the usual limit.
#[cfg(all(not(Py_3_14), target_os = "linux", target_env = "musl"))]
const INITIAL_STACK_MAX_BYTES: usize = 8 << 20;

/// Pages the kernel keeps free between a growing stack and the mapping
/// below it: 256, unless the kernel was booted with another
/// `stack_guard_gap`. `None` if its command line (`/proc/cmdline`) so much
/// as mentions one: the kernel's own reading of it (quoting, `-` for `_`,
/// what follows `--`) is not second-guessed here.
#[cfg(any(test, all(target_os = "linux", target_env = "musl")))]
fn stack_guard_gap_pages(kernel_command_line: &str) -> Option<usize> {
    let mentioned = kernel_command_line
        .replace('-', "_")
        .contains("stack_guard_gap");
    (!mentioned).then_some(256)
}

/// The lowest address the initial stack may grow down to, given
/// `/proc/self/smaps`, or `None` unless `sp` is on that stack: in the
/// mapping the kernel calls `[stack]`, which grows down (`gd` among its
/// `VmFlags`) and holds the `random` bytes the kernel put on the initial
/// stack, and which begins at `reported_lowest`, where musl has the
/// calling thread's stack begin. A stack that merely sits next to it (one
/// an application made and handed to `pthread_attr_setstack`) is a mapping
/// of its own, one put in its place does not grow, and a buffer inside it
/// used as a thread's stack begins further up.
///
/// The stack can grow until it is `rlimit` bytes long, measured from the
/// end of its mapping, or comes within `guard_gap` bytes of the mapping
/// below it. The limit is short of both by a margin, no more than
/// `max_below_random` bytes below `random` (about where the process
/// started), and never above the start of what is mapped.
#[cfg(any(test, all(target_os = "linux", target_env = "musl")))]
fn initial_stack_growth_limit(
    smaps: &str,
    sp: usize,
    random: usize,
    rlimit: usize,
    guard_gap: usize,
    max_below_random: usize,
    reported_lowest: usize,
) -> Option<usize> {
    let mut mapping_below_ends = 0;
    // The mapping `sp` is in, once its first line has been read.
    let mut stack = None;
    for line in smaps.lines() {
        let mapping = line.split_whitespace().next().and_then(|range| {
            let (start, end) = range.split_once('-')?;
            Some((
                usize::from_str_radix(start, 16).ok()?,
                usize::from_str_radix(end, 16).ok()?,
            ))
        });
        match (mapping, stack) {
            (Some(_), Some(_)) => return None, // No `VmFlags` line for it.
            (Some((start, end)), None) if (start..end).contains(&sp) => {
                if start != reported_lowest
                    || !(start..end).contains(&random)
                    || !line.trim_end().ends_with("[stack]")
                {
                    return None;
                }
                stack = Some((start, end));
            }
            (Some((_, end)), None) => mapping_below_ends = end,
            (None, Some((start, end))) => {
                let Some(flags) = line.strip_prefix("VmFlags:") else {
                    continue;
                };
                if !flags.split_whitespace().any(|flag| flag == "gd") {
                    return None;
                }
                let by_limit = end.saturating_sub(rlimit);
                let by_neighbour = mapping_below_ends.saturating_add(guard_gap);
                return Some(
                    by_limit
                        .max(by_neighbour)
                        .saturating_add(INITIAL_STACK_MARGIN_BYTES)
                        .max(random.saturating_sub(max_below_random))
                        .min(start),
                );
            }
            (None, None) => {}
        }
    }
    None
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
            limit = os_stack_limit(sp);
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

/// The events one tracing session skipped for want of stack.
///
/// Skipping is silent by design: a program recursing to its limit loses the
/// deepest frames and nothing else. A session that skipped events and
/// recorded nothing is something else: a thread whose whole stack is smaller
/// than the reserve, or a stack Kolo misjudged (3.5.0 on musl). It says so
/// when it is saved, instead of leaving an empty trace to be found later.
#[derive(Default)]
pub(crate) struct StackSkips {
    events: AtomicUsize,
    /// Stack left at the latest skip.
    remaining: AtomicUsize,
}

impl StackSkips {
    /// Count an event the stack check skipped on this thread.
    #[cold]
    #[inline(never)]
    pub(crate) fn note(&self) {
        let remaining = STACK_GUARD.with(StackGuard::remaining);
        self.remaining.store(remaining, Ordering::Relaxed);
        self.events.fetch_add(1, Ordering::Relaxed);
    }

    /// Start counting afresh, for a new session.
    pub(crate) fn reset(&self) {
        self.events.store(0, Ordering::Relaxed);
    }

    /// Called when a session's trace is saved: warn if it has no frames and
    /// the stack check is why.
    pub(crate) fn warn_if_nothing_recorded(&self, py: Python, trace_id: &str, no_frames: bool) {
        let events = self.events.swap(0, Ordering::Relaxed);
        if events == 0 || !no_frames {
            return;
        }
        let message = format!(
            "Kolo recorded no frames in trace {trace_id}: it skipped {events} events as too \
             close to the end of the C stack ({} KiB left where it keeps {} KiB in reserve). \
             A thread needs a stack of more than twice that to be traced. If this one has \
             that, this is a bug in Kolo: please report it with your platform and Python \
             version.",
            self.remaining.load(Ordering::Relaxed) / 1024,
            STACK_RESERVE_BYTES / 1024,
        );
        // Logging runs Python code, and plenty of it. Short of stack (a
        // session saved from where its events were skipped), write to fd 2
        // without touching the interpreter.
        if STACK_GUARD.with(StackGuard::remaining) >= STACK_RESERVE_BYTES {
            if let Ok(args) = PyTuple::new(py, [message.as_str()]) {
                log_warning(py, args, None);
                return;
            }
        }
        let _ = std::io::stderr().write_all(format!("{message}\n").as_bytes());
    }
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
        check_stack, check_stack_with, decide, forget_entry, initial_stack_growth_limit,
        remaining_stack, stack_guard_gap_pages, values_omitted, with_stack_below, NearEndFrames,
        OmittingValues, StackDecision, StackEvent, ENTRY_DEPTH_SLACK_BYTES,
        EXIT_STACK_RESERVE_BYTES, INITIAL_STACK_MARGIN_BYTES, MINIMAL_EXIT_STACK_RESERVE_BYTES,
        NEAR_STACK_END_BYTES, STACK_GUARD, STACK_RESERVE_BYTES,
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

    /// `/proc/self/smaps` of a process whose initial stack, 132 KiB mapped,
    /// is the last mapping but one, with `below` under it. Addresses that
    /// fit a 32-bit target too.
    fn smaps_with(below: &str, stack_flags: &str) -> String {
        format!(
            "08048000-08049000 r--p 00000000 fd:01 123 /usr/local/bin/python3.13\n\
             Size:                  4 kB\n\
             VmFlags: rd mr mw me sd\n\
             {below}\
             7f6e9000-7f70a000 rw-p 00000000 00:00 0                          [stack]\n\
             Size:                132 kB\n\
             Rss:                  60 kB\n\
             VmFlags: {stack_flags}\n\
             7f7f0000-7f7f2000 r-xp 00000000 00:00 0                          [vdso]\n\
             Size:                  8 kB\n\
             VmFlags: rd ex mr mw me de sd\n"
        )
    }
    const STACK_FLAGS: &str = "rd wr mr mw me gd ac";
    const STACK_START: usize = 0x7f6e_9000;
    const STACK_END: usize = 0x7f70_a000;
    const SP: usize = STACK_END - 0x3000;
    const RANDOM: usize = STACK_END - 0x800;
    const GAP: usize = 256 * 4096;
    const FAR_BELOW: &str = "40000000-40100000 rw-p 00000000 00:00 0\nVmFlags: rd wr mr mw me ac\n";

    #[test]
    fn the_initial_stack_grows_to_its_rlimit() {
        let smaps = smaps_with(FAR_BELOW, STACK_FLAGS);
        let grows_to = |rlimit| {
            initial_stack_growth_limit(&smaps, SP, RANDOM, rlimit, GAP, 4 << 20, STACK_START)
        };
        assert_eq!(
            grows_to(2 << 20),
            Some(STACK_END - (2 << 20) + INITIAL_STACK_MARGIN_BYTES)
        );
        // No further than CPython takes it to go, whatever is allowed.
        let capped = Some(RANDOM - (4 << 20));
        assert_eq!(grows_to(64 << 20), capped);
        assert_eq!(grows_to(usize::MAX), capped);
        // A limit smaller than what is mapped doesn't take mapped stack away.
        assert_eq!(grows_to(64 * 1024), Some(STACK_START));
        assert_eq!(grows_to(0), Some(STACK_START));
    }

    #[test]
    fn a_mapping_under_the_initial_stack_stops_its_growth() {
        // 2 MiB under the stack's start.
        let below = "7f4e8000-7f4e9000 rw-p 00000000 00:00 0\nVmFlags: rd wr mr mw me ac\n";
        let smaps = smaps_with(below, STACK_FLAGS);
        let neighbour_end = 0x7f4e_9000;
        let grows_to = |guard_gap| {
            initial_stack_growth_limit(&smaps, SP, RANDOM, 3 << 20, guard_gap, 4 << 20, STACK_START)
        };
        assert_eq!(
            grows_to(GAP),
            Some(neighbour_end + GAP + INITIAL_STACK_MARGIN_BYTES)
        );
        // A larger gap (64 KiB pages, or `stack_guard_gap=` on the kernel's
        // command line): nothing to grow into.
        assert_eq!(grows_to(256 * 65536), Some(STACK_START));
        assert_eq!(grows_to(1024 * 4096), Some(STACK_START));
        assert_eq!(grows_to(usize::MAX), Some(STACK_START));
        // Right under the stack.
        let below = "7f6e0000-7f6e9000 rw-p 00000000 00:00 0\nVmFlags: rd wr mr mw me ac\n";
        let smaps = smaps_with(below, STACK_FLAGS);
        assert_eq!(
            initial_stack_growth_limit(&smaps, SP, RANDOM, 3 << 20, GAP, 4 << 20, STACK_START),
            Some(STACK_START)
        );
    }

    #[test]
    fn only_the_initial_stack_is_taken_to_grow() {
        let grows_to = |smaps: &str, sp, random| {
            initial_stack_growth_limit(smaps, sp, random, 8 << 20, GAP, 4 << 20, STACK_START)
        };
        // A stack an application mapped right above the initial one and
        // gave to a thread: near the kernel's random bytes, but a mapping
        // of its own.
        let smaps = "7f6e9000-7f70a000 rw-p 00000000 00:00 0 [stack]\n\
                     VmFlags: rd wr mr mw me gd ac\n\
                     7f70a000-7f71a000 rw-p 00000000 00:00 0\n\
                     VmFlags: rd wr mr mw me ac\n";
        assert_eq!(grows_to(smaps, STACK_END + 0x8000, RANDOM), None);
        // The random bytes are elsewhere: not the stack the kernel set up.
        let smaps = smaps_with(FAR_BELOW, STACK_FLAGS);
        assert_eq!(grows_to(&smaps, SP, STACK_END + 0x10_0000), None);
        // Not called `[stack]`.
        let unnamed = smaps.replace("[stack]", "");
        assert_eq!(grows_to(&unnamed, SP, RANDOM), None);
        // A fixed mapping put where the initial stack was: it keeps the
        // name, but doesn't grow down.
        let fixed = smaps_with(FAR_BELOW, "rd wr mr mw me ac");
        assert_eq!(grows_to(&fixed, SP, RANDOM), None);
        // A buffer inside the initial stack, used as a thread's stack (and
        // then forked from, which makes that thread the main one): musl has
        // it begin above the mapping's start.
        assert_eq!(
            initial_stack_growth_limit(
                &smaps,
                SP,
                RANDOM,
                8 << 20,
                GAP,
                4 << 20,
                STACK_START + 0x4000
            ),
            None
        );
        // No flags to tell (`gd` in another mapping's doesn't count).
        let flagless = smaps.replace("VmFlags: rd wr mr mw me gd ac\n", "");
        assert_eq!(grows_to(&flagless, SP, RANDOM), None);
        let truncated = smaps.split("Rss:").next().expect("the stack's first lines");
        assert_eq!(grows_to(truncated, SP, RANDOM), None);
        // A stack pointer in no mapping, and nothing readable.
        assert_eq!(grows_to(&smaps, 0x1000, RANDOM), None);
        assert_eq!(grows_to("", SP, RANDOM), None);
        assert_eq!(grows_to("not a mapping\n", SP, RANDOM), None);
        // With all of that in order, it grows.
        assert!(grows_to(&smaps, SP, RANDOM).is_some());
    }

    #[test]
    fn a_stack_guard_gap_set_at_boot_is_not_guessed_at() {
        assert_eq!(stack_guard_gap_pages(""), Some(256));
        assert_eq!(
            stack_guard_gap_pages("BOOT_IMAGE=/vmlinuz ro quiet\n"),
            Some(256)
        );
        // Set at boot, in any of the ways the kernel reads: not guessed at.
        for command_line in [
            "ro stack_guard_gap=1024 quiet\n",
            "stack_guard_gap=\"1024\"",
            "stack-guard-gap=1024",
            "stack_guard_gap=1024 -- stack_guard_gap=0",
            "stack_guard_gap=lots",
        ] {
            assert_eq!(stack_guard_gap_pages(command_line), None, "{command_line}");
        }
    }

    /// Run `on_stack` on a thread whose stack is a mapping of exactly `bytes`
    /// made here, and return that stack's lowest address: bounds known
    /// without asking the C library, which also can't hand the thread some
    /// other stack (glibc reuses the stacks of threads that exited). Linux
    /// only: macOS can still be running a joined thread's last instructions
    /// on its stack when the mapping goes.
    #[cfg(target_os = "linux")]
    fn on_stack_of_known_bounds(bytes: usize, on_stack: &mut (dyn FnMut() + Send)) -> usize {
        extern "C" fn run(on_stack: *mut libc::c_void) -> *mut libc::c_void {
            // SAFETY: `on_stack` points to the `&mut dyn FnMut()` below,
            // which outlives this thread: its creator joins it.
            let on_stack = unsafe { &mut *on_stack.cast::<&mut (dyn FnMut() + Send)>() };
            // A panic here would abort the tests: assert after the join.
            on_stack();
            std::ptr::null_mut()
        }
        let mut on_stack = on_stack;
        // SAFETY: plain FFI on a mapping and a thread attribute made and
        // released here; the thread is joined before either goes away.
        unsafe {
            let lowest = libc::mmap(
                std::ptr::null_mut(),
                bytes,
                libc::PROT_READ | libc::PROT_WRITE,
                libc::MAP_PRIVATE | libc::MAP_ANON,
                -1,
                0,
            );
            assert_ne!(lowest, libc::MAP_FAILED);
            let mut attr = std::mem::MaybeUninit::<libc::pthread_attr_t>::uninit();
            assert_eq!(libc::pthread_attr_init(attr.as_mut_ptr()), 0);
            assert_eq!(
                libc::pthread_attr_setstack(attr.as_mut_ptr(), lowest, bytes),
                0
            );
            let mut thread = std::mem::MaybeUninit::<libc::pthread_t>::uninit();
            let created = libc::pthread_create(
                thread.as_mut_ptr(),
                attr.as_ptr(),
                run,
                std::ptr::addr_of_mut!(on_stack).cast(),
            );
            assert_eq!(created, 0);
            assert_eq!(
                libc::pthread_join(thread.assume_init(), std::ptr::null_mut()),
                0
            );
            libc::pthread_attr_destroy(attr.as_mut_ptr());
            assert_eq!(libc::munmap(lowest, bytes), 0);
            lowest as usize
        }
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn a_thread_is_never_credited_with_more_stack_than_it_has() {
        for bytes in [192 << 10, 512 << 10, 1 << 20, 4 << 20, 16 << 20] {
            // Twice: a stale answer from the thread before would show.
            for _ in 0..2 {
                let mut measured = (0, 0);
                let lowest = on_stack_of_known_bounds(bytes, &mut || {
                    measured = (super::stack_pointer(), remaining_stack());
                });
                let (sp, remaining) = measured;
                assert!((lowest..lowest + bytes).contains(&sp), "{sp:#x}");
                // No more than lies below the stack pointer (sampled in the
                // same frame as the measurement, or the one above it).
                assert!(
                    remaining <= sp - lowest + 1024,
                    "{remaining} left with {} below the stack pointer of a {bytes} byte stack",
                    sp - lowest
                );
                // And it is this stack that was measured, from near its top.
                assert!(remaining >= bytes / 2, "{remaining} of {bytes}");
            }
        }
    }

    /// Stack mapped below `address` in the mapping that holds it, from
    /// `/proc/self/maps`: what the kernel says, whatever the C library does.
    #[cfg(target_os = "linux")]
    fn mapped_below(address: usize) -> usize {
        let maps = std::fs::read_to_string("/proc/self/maps").expect("/proc/self/maps");
        maps.lines()
            .find_map(|line| {
                let (start, end) = line.split_whitespace().next()?.split_once('-')?;
                let start = usize::from_str_radix(start, 16).ok()?;
                let end = usize::from_str_radix(end, 16).ok()?;
                (start..end).contains(&address).then(|| address - start)
            })
            .expect("the stack is mapped")
    }

    /// What a thread the standard library starts measures, and what is
    /// really there: the stack the stack check takes it to have left, and
    /// (on Linux) the stack mapped below it.
    fn measured_on_thread_with_stack(bytes: usize) -> (usize, Option<usize>) {
        std::thread::Builder::new()
            .stack_size(bytes)
            .spawn(|| {
                let remaining = remaining_stack();
                #[cfg(target_os = "linux")]
                let mapped = Some(mapped_below(super::stack_pointer()));
                #[cfg(not(target_os = "linux"))]
                let mapped = None;
                (remaining, mapped)
            })
            .expect("spawn test thread")
            .join()
            .expect("test thread")
    }

    /// Slack for the checks on stacks whose exact bounds aren't known here:
    /// sizes are rounded up to pages, and an older glibc reports a stack's
    /// guard page as part of it.
    const ROUNDING_BYTES: usize = 64 * 1024;

    fn assert_measured_within_the_stack(asked_for: usize, measured: (usize, Option<usize>)) {
        let (remaining, mapped) = measured;
        // The OS said where the stack ends, and the thread is near its top.
        assert!(remaining >= asked_for / 4 * 3, "{remaining} of {asked_for}");
        match mapped {
            // Linux: no more than is mapped there. Not "no more than was
            // asked for": glibc gives a new thread the cached stack of one
            // that exited, when that is up to four times the size
            // requested. The thread then has that much stack, and the stack
            // check is right to say so. (The exact check is
            // `a_thread_is_never_credited_with_more_stack_than_it_has`.)
            Some(mapped) => assert!(
                remaining <= mapped + ROUNDING_BYTES,
                "{remaining} left of {mapped} mapped, having asked for {asked_for}"
            ),
            // Elsewhere a thread gets the stack it asked for.
            None => assert!(
                remaining <= asked_for + ROUNDING_BYTES,
                "{remaining} of {asked_for}"
            ),
        }
    }

    #[test]
    fn a_thread_knows_how_much_stack_it_has() {
        assert_measured_within_the_stack(4 << 20, measured_on_thread_with_stack(4 << 20));
    }

    #[test]
    fn threads_coming_and_going_are_never_credited_with_more_stack_than_they_have() {
        // KOLO_STACK_STRESS_ROUNDS: more rounds, for a stress run.
        let rounds = std::env::var("KOLO_STACK_STRESS_ROUNDS")
            .ok()
            .and_then(|rounds| rounds.parse().ok())
            .unwrap_or(200);
        const SIZES: [usize; 7] = [
            16 << 20,
            4 << 20,
            1 << 20,
            8 << 20,
            512 << 10,
            4 << 20,
            2 << 20,
        ];
        let mut on_larger_stacks = 0;
        for round in 0..rounds {
            // Up to three threads parked on stacks of their own meanwhile.
            let parked: Vec<_> = (0..round % 4)
                .map(|index| {
                    let (wake, parked) = std::sync::mpsc::channel::<()>();
                    let thread = std::thread::Builder::new()
                        .stack_size(SIZES[(round + index) % SIZES.len()])
                        .spawn(move || {
                            let _ = parked.recv();
                        })
                        .expect("spawn parked thread");
                    (wake, thread)
                })
                .collect();
            let asked_for = SIZES[round % SIZES.len()];
            let measured = measured_on_thread_with_stack(asked_for);
            assert_measured_within_the_stack(asked_for, measured);
            if measured.0 > asked_for + ROUNDING_BYTES {
                on_larger_stacks += 1;
            }
            for (wake, thread) in parked {
                drop(wake);
                thread.join().expect("parked thread");
            }
        }
        // About half of them on glibc, which reuses stacks; none elsewhere.
        eprintln!("{on_larger_stacks} of {rounds} threads ran on a larger stack than requested");
    }

    #[test]
    fn a_stack_smaller_than_the_reserve_is_never_recorded() {
        // The reserve is not scaled down to fit: Kolo's callbacks need it
        // (serializing a nested value takes stack in proportion).
        let mut decided = None;
        let mut on_small_stack = || {
            decided = Some((
                remaining_stack(),
                decision(StackEvent::Enter(1)),
                decision(StackEvent::Exit(1)),
            ));
        };
        // On Linux a stack made here: glibc may give a thread that asks for
        // 192 KiB the larger stack of one that exited.
        #[cfg(target_os = "linux")]
        on_stack_of_known_bounds(192 * 1024, &mut on_small_stack);
        #[cfg(not(target_os = "linux"))]
        std::thread::scope(|scope| {
            std::thread::Builder::new()
                .stack_size(192 * 1024)
                .spawn_scoped(scope, &mut on_small_stack)
                .expect("spawn test thread");
        });
        let (remaining, enter, exit) = decided.expect("the thread ran");
        assert!(remaining < STACK_RESERVE_BYTES, "{remaining}");
        assert_eq!((enter, exit), (Skip, Skip));
    }

    #[test]
    fn a_stack_pointer_below_the_measured_stack_is_out_of_stack() {
        on_small_thread(|| {
            assert_eq!(decision(StackEvent::Enter(1)), Record);
            assert_eq!(decision(StackEvent::Exit(1)), Record);
            STACK_GUARD.with(|guard| {
                // As when running on another stack than the thread's own,
                // lower in memory: not known to have room.
                let limit = guard.limit.replace(usize::MAX - 1);
                assert_eq!(guard.remaining(), 0);
                assert_eq!(check_stack(StackEvent::Enter(1)).0, Skip);
                assert_eq!(check_stack(StackEvent::Exit(1)).0, Skip);
                guard.limit.set(limit);
            });
        });
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

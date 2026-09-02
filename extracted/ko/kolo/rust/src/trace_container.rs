//! Native storage primitives for the write-once v3 trace container.
//!
//! This module deliberately accepts frame encoders, rather than encoded frame
//! buffers: the successful path writes straight into an arena and commits a
//! boundary only after the encoder returns successfully.

use std::fs::{create_dir_all, remove_file, rename, File, OpenOptions};
use std::io::{self, BufWriter, Write};
use std::ops::Range;
use std::path::{Path, PathBuf};
#[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
use std::sync::atomic::AtomicI32;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
#[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
use std::sync::Once;
use std::sync::{Arc, Condvar, Mutex, OnceLock};
use std::thread::{self, JoinHandle};
use std::time::{Duration, Instant};

use hashbrown::HashMap;

use super::utils::{FrameSequence, SerializedFrame, TraceNameIndex, TraceNameObservation};

#[cfg(unix)]
use std::os::unix::fs::FileExt;
#[cfg(windows)]
use std::os::windows::fs::FileExt;

const HEADER_MAGIC: &[u8; 8] = b"KOLOTRC3";
const RECORD_MAGIC: &[u8; 4] = b"KR3\0";
const FOOTER_MAGIC: &[u8; 8] = b"KOLOEND3";
const HEADER_LEN: u64 = 24;
const RECORD_HEADER_LEN: u64 = 40;
const FOOTER_LEN: u64 = 32;
pub(crate) const DEFAULT_CHUNK_TARGET: usize = 512 * 1024;
const WRITER_BUFFER: usize = 64 * 1024;
const RESIDENT_LIMIT: usize = 16 * 1024 * 1024;
// Account for the channel node, enum, Arcs, and allocator metadata as well as
// payload capacity. This makes the resident budget the sole queue bound even
// when a stalled writer has thousands of tiny value records waiting behind it.
const COMMAND_RESIDENT_OVERHEAD: usize = 256;
const WRITER_STALL_TIMEOUT: Duration = Duration::from_secs(30);
static TEMP_SEQUENCE: AtomicU64 = AtomicU64::new(0);
static PROCESS_WRITER_CIRCUIT_OPEN: AtomicBool = AtomicBool::new(false);

#[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
static PROCESS_FORK_GENERATION: AtomicU64 = AtomicU64::new(0);
#[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
static REGISTER_PROCESS_ATFORK: Once = Once::new();
#[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
static PROCESS_ATFORK_STATUS: AtomicI32 = AtomicI32::new(-1);

#[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
unsafe extern "C" fn advance_process_fork_generation() {
    // pthread_atfork's child callback may only perform async-signal-safe work.
    // The cfg above guarantees that this 64-bit atomic is native and lock-free;
    // this operation does not allocate or acquire a lock.
    PROCESS_FORK_GENERATION.fetch_add(1, Ordering::Relaxed);
}

#[derive(Clone, Copy)]
pub(crate) struct ProcessForkGeneration {
    generation: u64,
    process_id: u32,
    reliable: bool,
}

impl ProcessForkGeneration {
    pub(crate) fn register() -> bool {
        #[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
        {
            REGISTER_PROCESS_ATFORK.call_once(|| {
                let status = unsafe {
                    libc::pthread_atfork(None, None, Some(advance_process_fork_generation))
                };
                PROCESS_ATFORK_STATUS.store(status, Ordering::Relaxed);
            });
            PROCESS_ATFORK_STATUS.load(Ordering::Relaxed) == 0
        }
        #[cfg(all(unix, not(target_arch = "wasm32"), not(target_has_atomic = "64")))]
        {
            // Without a guaranteed lock-free 64-bit atomic, a post-fork child
            // handler could inherit an internal atomic lock held by a vanished
            // thread. Use the correct but slower live-PID check instead.
            false
        }
        #[cfg(any(not(unix), target_arch = "wasm32"))]
        {
            // These platforms cannot inherit a live capture through fork.
            true
        }
    }

    pub(crate) fn current(reliable: bool) -> (u64, u32) {
        #[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
        {
            if reliable {
                (PROCESS_FORK_GENERATION.load(Ordering::Relaxed), 0)
            } else {
                (0, std::process::id())
            }
        }
        #[cfg(all(unix, not(target_arch = "wasm32"), not(target_has_atomic = "64")))]
        {
            let _ = reliable;
            (0, std::process::id())
        }
        #[cfg(any(not(unix), target_arch = "wasm32"))]
        {
            let _ = reliable;
            (0, 0)
        }
    }

    fn capture() -> Self {
        let reliable = Self::register();
        let (generation, process_id) = Self::current(reliable);
        Self {
            generation,
            process_id,
            reliable,
        }
    }

    fn has_changed(&self) -> bool {
        let (generation, process_id) = Self::current(self.reliable);
        self.has_changed_from(generation, process_id)
    }

    fn has_changed_from(&self, generation: u64, process_id: u32) -> bool {
        self.generation != generation || self.process_id != process_id
    }
}

fn frame_bounds(frame_ends: &[u64], index: usize) -> io::Result<(u64, u64)> {
    let end = frame_ends
        .get(index)
        .copied()
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))?;
    let start = if index == 0 { 0 } else { frame_ends[index - 1] };
    if start > end {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "invalid frame boundary",
        ));
    }
    Ok((start, end))
}

#[derive(Debug)]
pub(crate) struct SealedChunk {
    pub thread_token: u32,
    pub sequence: u64,
    bytes: Arc<Vec<u8>>,
    frame_ends: Arc<[u64]>,
}

impl SealedChunk {
    fn resident_len(&self) -> usize {
        self.bytes.capacity() + self.frame_ends.len() * std::mem::size_of::<u64>()
    }

    pub(crate) fn frame_count(&self) -> usize {
        self.frame_ends.len()
    }
}

/// An append-only per-thread arena. A frame is never split between chunks.
pub(crate) struct FrameArena {
    thread_token: u32,
    next_sequence: u64,
    target: usize,
    bytes: Vec<u8>,
    frame_ends: Vec<u64>,
}

#[derive(Debug)]
struct SnapshotFile {
    path: Arc<PathBuf>,
    #[cfg(not(windows))]
    file: OnceLock<File>,
    #[cfg(windows)]
    file: Mutex<Option<File>>,
}

impl SnapshotFile {
    fn new(path: Arc<PathBuf>) -> Self {
        Self {
            path,
            #[cfg(not(windows))]
            file: OnceLock::new(),
            #[cfg(windows)]
            file: Mutex::new(None),
        }
    }

    #[cfg(not(windows))]
    fn install(&self, file: File) {
        self.file
            .set(file)
            .expect("snapshot file installed more than once");
    }

    #[cfg(windows)]
    fn install(&self, file: File) {
        let mut snapshot = self.file.lock().expect("snapshot file mutex poisoned");
        assert!(snapshot.is_none(), "snapshot file installed more than once");
        *snapshot = Some(file);
    }

    #[cfg(not(windows))]
    fn read_exact_at(&self, buf: &mut [u8], offset: u64) -> io::Result<()> {
        if self.file.get().is_none() {
            // Unit-created handles may not have a TraceWriter to install the
            // descriptor. Production writers install it before their worker
            // starts, so a forked child never races a parent rename here.
            let file = File::open(self.path.as_ref())?;
            let _ = self.file.set(file);
        }
        read_exact_at(
            self.file.get().expect("snapshot file was just opened"),
            buf,
            offset,
        )
    }

    #[cfg(windows)]
    fn read_exact_at(&self, buf: &mut [u8], offset: u64) -> io::Result<()> {
        let mut snapshot = self.file.lock().expect("snapshot file mutex poisoned");
        if snapshot.is_none() {
            *snapshot = Some(File::open(self.path.as_ref())?);
        }
        read_exact_at(
            snapshot.as_ref().expect("snapshot file was just opened"),
            buf,
            offset,
        )
    }

    #[cfg(not(windows))]
    fn publish(&self, from: &Path, to: &Path) -> io::Result<()> {
        replace_file(from, to)
    }

    #[cfg(windows)]
    fn publish(&self, from: &Path, to: &Path) -> io::Result<()> {
        let mut snapshot = self.file.lock().expect("snapshot file mutex poisoned");
        // ReplaceFileW opens the replacement path with no sharing mode, so it
        // cannot run while even our read-only snapshot descriptor is open.
        // Hold the mutex across replacement so a concurrent range read cannot
        // reopen the temporary path in this zero-handle window.
        *snapshot = None;
        match replace_file(from, to) {
            Ok(()) => {
                *snapshot = Some(File::open(to)?);
                Ok(())
            }
            Err(error) => {
                *snapshot = File::open(from).ok();
                Err(error)
            }
        }
    }
}

/// Stable logical handle retained by frame-range operations after the writer
/// has released the chunk payload. Reading is deliberately positional and is
/// only used for explicit trace-point/subtree extraction.
#[derive(Debug)]
pub(crate) struct ChunkHandle {
    snapshot: Arc<SnapshotFile>,
    thread_token: u32,
    sequence: u64,
    frame_ends: Arc<[u64]>,
    // Zero means the chunk is still readable from memory. The writer
    // publishes offset + 1 before locking `memory` to release those bytes, so
    // a forked child always bypasses a writer-held mutex.
    committed_offset_plus_one: AtomicU64,
    memory: Mutex<Option<Arc<Vec<u8>>>>,
    failure: OnceLock<String>,
}

impl ChunkHandle {
    fn memory(
        snapshot: Arc<SnapshotFile>,
        thread_token: u32,
        sequence: u64,
        frame_ends: Arc<[u64]>,
        bytes: Arc<Vec<u8>>,
    ) -> Self {
        Self {
            snapshot,
            thread_token,
            sequence,
            frame_ends,
            committed_offset_plus_one: AtomicU64::new(0),
            memory: Mutex::new(Some(bytes)),
            failure: OnceLock::new(),
        }
    }

    fn commit(&self, frame_payload_offset: u64) {
        let published = frame_payload_offset
            .checked_add(1)
            .expect("trace frame payload offset exhausted u64");
        self.committed_offset_plus_one
            .store(published, Ordering::Release);
        self.memory.lock().expect("chunk memory poisoned").take();
    }

    fn fail(&self, error: &io::Error) {
        let _ = self.failure.set(error.to_string());
        // Publish failure before locking `memory`, so a forked child bypasses
        // a writer-held transition lock just as it does after commit.
        self.memory.lock().expect("chunk memory poisoned").take();
    }

    pub(crate) fn frame_count(&self) -> usize {
        self.frame_ends.len()
    }

    pub(crate) fn thread_token(&self) -> u32 {
        self.thread_token
    }

    pub(crate) fn sequence(&self) -> u64 {
        self.sequence
    }

    pub(crate) fn frame_len(&self, index: usize) -> io::Result<usize> {
        let (start, end) = frame_bounds(&self.frame_ends, index)?;
        usize::try_from(end - start).map_err(|_| invalid_size())
    }

    pub(crate) fn read_frame(&self, index: usize, scratch: &mut Vec<u8>) -> io::Result<()> {
        let length = self.frame_len(index)?;
        let (relative_offset, _) = frame_bounds(&self.frame_ends, index)?;
        if let Some(error) = self.failure.get() {
            return Err(io::Error::other(error.clone()));
        }
        let mut published = self.committed_offset_plus_one.load(Ordering::Acquire);
        if published == 0 {
            let memory = self.memory.lock().expect("chunk memory poisoned");
            if let Some(error) = self.failure.get() {
                return Err(io::Error::other(error.clone()));
            }
            published = self.committed_offset_plus_one.load(Ordering::Acquire);
            if published == 0 {
                let bytes = memory.as_ref().ok_or_else(|| {
                    io::Error::new(
                        io::ErrorKind::UnexpectedEof,
                        "missing in-memory trace chunk",
                    )
                })?;
                let start = usize::try_from(relative_offset).map_err(|_| invalid_size())?;
                let end = start.checked_add(length).ok_or_else(invalid_size)?;
                scratch.clear();
                scratch.extend_from_slice(bytes.get(start..end).ok_or_else(|| {
                    io::Error::new(io::ErrorKind::UnexpectedEof, "short in-memory trace read")
                })?);
                return Ok(());
            }
        }
        let frame_payload_offset = published - 1;
        let offset = frame_payload_offset
            .checked_add(relative_offset)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "frame offset overflow"))?;
        scratch.resize(length, 0);
        self.snapshot.read_exact_at(scratch, offset)
    }
}

impl FrameArena {
    pub(crate) fn new(thread_token: u32) -> Self {
        Self::with_target(thread_token, DEFAULT_CHUNK_TARGET)
    }

    fn with_target(thread_token: u32, target: usize) -> Self {
        Self {
            thread_token,
            next_sequence: 0,
            target,
            bytes: Vec::with_capacity(target.min(64 * 1024)),
            frame_ends: Vec::new(),
        }
    }

    fn frame_count(&self) -> usize {
        self.frame_ends.len()
    }

    fn total_bytes(&self) -> usize {
        self.bytes.len()
    }

    fn frame_len(&self, index: usize) -> io::Result<usize> {
        let (start, end) = frame_bounds(&self.frame_ends, index)?;
        usize::try_from(end - start).map_err(|_| invalid_size())
    }

    fn frame(&self, index: usize) -> io::Result<&[u8]> {
        let (start, end) = frame_bounds(&self.frame_ends, index)?;
        let start = usize::try_from(start).map_err(|_| invalid_size())?;
        let end = usize::try_from(end).map_err(|_| invalid_size())?;
        self.bytes.get(start..end).ok_or_else(|| {
            io::Error::new(io::ErrorKind::UnexpectedEof, "short in-memory trace read")
        })
    }

    /// Encode and atomically commit a frame. On serializer failure all bytes
    /// (including bytes written before Python fallback failed) are rolled back.
    pub(crate) fn append_frame<E, F>(&mut self, encode: F) -> Result<Option<SealedChunk>, E>
    where
        F: FnOnce(&mut Vec<u8>) -> Result<(), E>,
    {
        let start = self.bytes.len();
        if let Err(error) = encode(&mut self.bytes) {
            self.bytes.truncate(start);
            return Err(error);
        }
        self.frame_ends.push(self.bytes.len() as u64);
        if self.bytes.len() >= self.target {
            Ok(self.seal())
        } else {
            Ok(None)
        }
    }

    pub(crate) fn seal(&mut self) -> Option<SealedChunk> {
        if self.frame_ends.is_empty() {
            return None;
        }
        let bytes = std::mem::replace(
            &mut self.bytes,
            Vec::with_capacity(self.target.min(64 * 1024)),
        );
        let frame_ends: Arc<[u64]> = std::mem::take(&mut self.frame_ends).into();
        let chunk = SealedChunk {
            thread_token: self.thread_token,
            sequence: self.next_sequence,
            bytes: Arc::new(bytes),
            frame_ends,
        };
        self.next_sequence += 1;
        Some(chunk)
    }
}

struct ResidentState {
    bytes: usize,
    progress_epoch: u64,
}

struct WriterRuntime {
    resident: Mutex<ResidentState>,
    changed: Condvar,
    circuit_open: AtomicBool,
    stall_timeout: Duration,
    poison_process: bool,
}

impl WriterRuntime {
    fn new(stall_timeout: Duration, poison_process: bool) -> Self {
        Self {
            resident: Mutex::new(ResidentState {
                bytes: 0,
                progress_epoch: 0,
            }),
            changed: Condvar::new(),
            circuit_open: AtomicBool::new(false),
            stall_timeout,
            poison_process,
        }
    }

    fn is_open(&self) -> bool {
        self.circuit_open.load(Ordering::Acquire)
    }

    fn open_circuit(&self) {
        if !self.circuit_open.swap(true, Ordering::AcqRel) && self.poison_process {
            PROCESS_WRITER_CIRCUIT_OPEN.store(true, Ordering::Release);
        }
        self.changed.notify_all();
    }

    fn reserve(self: &Arc<Self>, payload_bytes: usize) -> io::Result<ResidentReservation> {
        if self.is_open() {
            return Err(writer_circuit_error());
        }
        let bytes = payload_bytes.saturating_add(COMMAND_RESIDENT_OVERHEAD);
        let mut resident = self.resident.lock().expect("resident budget poisoned");
        let mut observed_progress = resident.progress_epoch;
        let mut deadline: Option<Instant> = None;

        // One oversized frame is allowed to exceed the target and global
        // budget, but only after all ordinary queued commands have drained.
        while resident.bytes != 0 && resident.bytes.saturating_add(bytes) > RESIDENT_LIMIT {
            if self.is_open() {
                return Err(writer_circuit_error());
            }
            let now = Instant::now();
            let wait_deadline = *deadline.get_or_insert_with(|| now + self.stall_timeout);
            if now >= wait_deadline {
                self.open_circuit();
                return Err(writer_circuit_error());
            }
            let remaining = wait_deadline.saturating_duration_since(now);
            let (next, _) = self
                .changed
                .wait_timeout(resident, remaining)
                .expect("resident budget poisoned");
            resident = next;
            if resident.progress_epoch != observed_progress {
                observed_progress = resident.progress_epoch;
                deadline = None;
            }
        }
        if self.is_open() {
            return Err(writer_circuit_error());
        }
        resident.bytes = resident.bytes.saturating_add(bytes);
        Ok(ResidentReservation {
            bytes,
            runtime: Arc::clone(self),
            writer_progress: false,
        })
    }

    fn release(&self, bytes: usize, writer_progress: bool) {
        let mut resident = self.resident.lock().expect("resident budget poisoned");
        resident.bytes = resident.bytes.saturating_sub(bytes);
        if writer_progress {
            resident.progress_epoch = resident.progress_epoch.wrapping_add(1);
        }
        self.changed.notify_all();
    }

    fn notify_writer_exit(&self, progress: &WriterProgress) {
        // Publish the predicate while holding the same mutex used by waiters.
        // This closes the gap between their predicate check and Condvar::wait
        // where an out-of-lock notification could otherwise be lost.
        let _resident = self
            .resident
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner);
        progress.mark_finished();
        self.changed.notify_all();
    }
}

fn writer_runtime() -> &'static Arc<WriterRuntime> {
    static RUNTIME: OnceLock<Arc<WriterRuntime>> = OnceLock::new();
    RUNTIME.get_or_init(|| Arc::new(WriterRuntime::new(WRITER_STALL_TIMEOUT, true)))
}

pub(crate) fn writer_circuit_open() -> bool {
    PROCESS_WRITER_CIRCUIT_OPEN.load(Ordering::Acquire)
}

fn writer_circuit_error() -> io::Error {
    io::Error::new(
        io::ErrorKind::TimedOut,
        "Kolo trace writer stopped making progress while its resident queue was full; tracing is disabled until process restart",
    )
}

/// Queue accounting must follow command ownership: every early writer exit,
/// failed send, and channel drop then releases its bytes automatically.
struct ResidentReservation {
    bytes: usize,
    runtime: Arc<WriterRuntime>,
    writer_progress: bool,
}

impl ResidentReservation {
    #[cfg(test)]
    fn new(bytes: usize) -> io::Result<Self> {
        writer_runtime().reserve(bytes)
    }

    #[cfg(test)]
    fn with_runtime(runtime: &Arc<WriterRuntime>, bytes: usize) -> io::Result<Self> {
        runtime.reserve(bytes)
    }

    /// Release this queued command as work the writer actually completed.
    /// Failed sends, duplicate publications, and commands drained after an
    /// error still release memory, but deliberately do not reset the stall
    /// deadline.
    fn complete_writer_command(mut self) {
        self.writer_progress = true;
    }
}

impl Drop for ResidentReservation {
    fn drop(&mut self) {
        self.runtime.release(self.bytes, self.writer_progress);
    }
}

enum Command {
    Value {
        id: u32,
        encoded: Arc<[u8]>,
        reservation: ResidentReservation,
    },
    Chunk {
        chunk: SealedChunk,
        reservation: ResidentReservation,
        handle: Arc<ChunkHandle>,
    },
    Finish {
        thread_meta: Vec<(u32, Vec<u8>)>,
        metadata: Vec<u8>,
        layouts: Vec<ThreadLayout>,
    },
    #[cfg(test)]
    FailForTest,
    #[cfg(test)]
    StallForTest(Arc<TestWriterStall>),
    #[cfg(test)]
    PanicForTest(std::sync::mpsc::Sender<()>),
}

#[cfg(test)]
struct TestWriterStall {
    entered: std::sync::mpsc::Sender<()>,
    released: Mutex<bool>,
    changed: Condvar,
}

#[cfg(test)]
impl TestWriterStall {
    fn wait(&self) {
        let _ = self.entered.send(());
        let mut released = self.released.lock().expect("test stall poisoned");
        while !*released {
            released = self.changed.wait(released).expect("test stall poisoned");
        }
    }

    fn release(&self) {
        *self.released.lock().expect("test stall poisoned") = true;
        self.changed.notify_all();
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct LayoutSpan {
    pub sequence: u64,
    pub first_frame: u32,
    pub frame_count: u32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct ThreadLayout {
    pub thread_token: u32,
    pub spans: Vec<LayoutSpan>,
}

#[derive(Clone)]
struct IndexEntry {
    kind: u8,
    offset: u64,
    stored_len: u32,
    thread_token: u32,
    sequence: u64,
    frame_count: u32,
}

#[derive(Default)]
struct WriterProgress {
    /// Length ending at the last record boundary known to have reached the
    /// underlying file. A circuit-open publication may contain a partial tail,
    /// but maintained readers will recover no further than this boundary.
    verified_len: AtomicU64,
    finished: AtomicBool,
}

impl WriterProgress {
    fn mark_verified(&self, length: u64) {
        self.verified_len.store(length, Ordering::Release);
    }

    fn verified_len(&self) -> u64 {
        self.verified_len.load(Ordering::Acquire)
    }

    fn mark_finished(&self) {
        self.finished.store(true, Ordering::Release);
    }

    fn is_finished(&self) -> bool {
        self.finished.load(Ordering::Acquire)
    }
}

/// Mark writer completion on success, error, or panic. `JoinHandle::join`
/// still transports the panic once a waiter observes this predicate.
struct WriterExitGuard {
    runtime: Arc<WriterRuntime>,
    progress: Arc<WriterProgress>,
}

impl Drop for WriterExitGuard {
    fn drop(&mut self) {
        self.runtime.notify_writer_exit(&self.progress);
    }
}

/// The sole owner of the named temporary final artifact lives on this thread.
pub(crate) struct TraceWriter {
    sender: Option<std::sync::mpsc::Sender<Command>>,
    join: Option<JoinHandle<io::Result<()>>>,
    destination: PathBuf,
    temporary: Arc<PathBuf>,
    snapshot: Arc<SnapshotFile>,
    runtime: Arc<WriterRuntime>,
    progress: Arc<WriterProgress>,
    preserve_temporary: Arc<AtomicBool>,
    recovery_path: Option<PathBuf>,
    process_id: u32,
}

impl TraceWriter {
    pub(crate) fn start(destination: PathBuf, header_payload: Vec<u8>) -> io::Result<Self> {
        let temporary = Arc::new(Self::temporary_path(&destination));
        let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
        Self::start_at(
            destination,
            temporary,
            snapshot,
            header_payload,
            Arc::clone(writer_runtime()),
        )
    }

    fn temporary_path(destination: &Path) -> PathBuf {
        let name = destination
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("trace.kolo");
        let sequence = TEMP_SEQUENCE.fetch_add(1, Ordering::Relaxed);
        destination.with_file_name(format!(".{name}.{}.{}.tmp", std::process::id(), sequence))
    }

    fn start_at(
        destination: PathBuf,
        temporary: Arc<PathBuf>,
        snapshot: Arc<SnapshotFile>,
        header_payload: Vec<u8>,
        runtime: Arc<WriterRuntime>,
    ) -> io::Result<Self> {
        if let Some(parent) = destination.parent() {
            create_dir_all(parent)?;
        }
        let file = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .open(temporary.as_ref())?;
        // Keep a readable descriptor open before the worker starts. An open
        // descriptor survives a parent's later rename/unlink and is inherited
        // across fork, so committed ChunkHandles never depend on the mutable
        // temporary pathname in a child. Open it separately as read-only:
        // unlike a clone of the writer handle, it does not retain write access
        // across the atomic replacement on Windows.
        snapshot.install(OpenOptions::new().read(true).open(temporary.as_ref())?);
        let (sender, receiver) = std::sync::mpsc::channel();
        let thread_temporary = Arc::clone(&temporary);
        let progress = Arc::new(WriterProgress::default());
        let thread_progress = Arc::clone(&progress);
        let thread_runtime = Arc::clone(&runtime);
        let preserve_temporary = Arc::new(AtomicBool::new(false));
        let thread_preserve_temporary = Arc::clone(&preserve_temporary);
        let join = thread::Builder::new()
            .name("kolo-v3-writer".into())
            .spawn(move || {
                let _exit_guard = WriterExitGuard {
                    runtime: thread_runtime,
                    progress: Arc::clone(&thread_progress),
                };
                writer_main(
                    file,
                    receiver,
                    header_payload,
                    &thread_temporary,
                    &thread_progress,
                    &thread_preserve_temporary,
                )
            })?;
        Ok(Self {
            sender: Some(sender),
            join: Some(join),
            destination,
            temporary,
            snapshot,
            runtime,
            progress,
            preserve_temporary,
            recovery_path: None,
            process_id: std::process::id(),
        })
    }

    /// A fork copies this handle but not its worker thread. Leak the child's
    /// inherited synchronization handles: even dropping the copied channel
    /// sender is not async-signal-safe on platforms such as macOS. This leaks
    /// at most the active writers inherited at fork, which the OS reclaims
    /// when the child exits.
    fn detach_after_fork(&mut self) {
        if let Some(sender) = self.sender.take() {
            std::mem::forget(sender);
        }
        if let Some(join) = self.join.take() {
            std::mem::forget(join);
        }
    }

    pub(crate) fn submit(&self, chunk: SealedChunk) -> io::Result<Arc<ChunkHandle>> {
        let reservation = self.runtime.reserve(chunk.resident_len())?;
        let handle = Arc::new(ChunkHandle::memory(
            Arc::clone(&self.snapshot),
            chunk.thread_token,
            chunk.sequence,
            Arc::clone(&chunk.frame_ends),
            Arc::clone(&chunk.bytes),
        ));
        self.submit_reserved(chunk, Arc::clone(&handle), reservation)?;
        Ok(handle)
    }

    fn submit_reserved(
        &self,
        chunk: SealedChunk,
        handle: Arc<ChunkHandle>,
        reservation: ResidentReservation,
    ) -> io::Result<()> {
        // Deliberately leave the handle in ChunkState::Memory while queued.
        // The command and handle share one allocation, so this adds no payload
        // residency; it only keeps synchronous range reads off the disk path.
        if self
            .sender
            .as_ref()
            .expect("open writer")
            .send(Command::Chunk {
                chunk,
                reservation,
                handle: Arc::clone(&handle),
            })
            .is_err()
        {
            let error = io::Error::new(io::ErrorKind::BrokenPipe, "trace writer failed");
            handle.fail(&error);
            return Err(error);
        }
        Ok(())
    }

    fn publish_value_reserved(
        &self,
        id: u32,
        encoded: Arc<[u8]>,
        reservation: ResidentReservation,
    ) -> io::Result<()> {
        self.sender
            .as_ref()
            .expect("open writer")
            .send(Command::Value {
                id,
                encoded,
                reservation,
            })
            .map_err(|_| io::Error::new(io::ErrorKind::BrokenPipe, "trace writer failed"))
    }

    pub(crate) fn finish(
        mut self,
        thread_meta: Vec<(u32, Vec<u8>)>,
        metadata: Vec<u8>,
        layouts: Vec<ThreadLayout>,
    ) -> io::Result<()> {
        if self.process_id != std::process::id() {
            self.detach_after_fork();
            return Err(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "trace writer cannot be finished in a forked child",
            ));
        }
        if self.runtime.is_open() {
            let recovered = self.abandon_for_circuit();
            return Err(circuit_abandon_error(recovered.as_deref()));
        }
        self.sender
            .as_ref()
            .expect("open writer")
            .send(Command::Finish {
                thread_meta,
                metadata,
                layouts,
            })
            .map_err(|_| io::Error::new(io::ErrorKind::BrokenPipe, "trace writer failed"))?;
        self.sender.take();
        // Wait on the runtime condition rather than joining blindly. Writer
        // exit and circuit-open both notify it, so a process-wide poison that
        // races finalization can detach this writer instead of hanging Kolo
        // teardown forever.
        {
            let mut resident = self
                .runtime
                .resident
                .lock()
                .expect("resident budget poisoned");
            while !self.progress.is_finished() && !self.runtime.is_open() {
                resident = self
                    .runtime
                    .changed
                    .wait(resident)
                    .expect("resident budget poisoned");
            }
        }
        if self.runtime.is_open() && !self.progress.is_finished() {
            let recovered = self.abandon_for_circuit();
            return Err(circuit_abandon_error(recovered.as_deref()));
        }
        let joined = self.join.take().expect("writer joined once").join();
        let result = match joined {
            Ok(result) => result,
            Err(_) => {
                let _ = remove_file(self.temporary.as_ref());
                return Err(io::Error::other("trace writer panicked"));
            }
        };
        if let Err(error) = result {
            let _ = remove_file(self.temporary.as_ref());
            return Err(error);
        }
        self.snapshot
            .publish(self.temporary.as_ref(), &self.destination)?;
        if let Some(parent) = self.destination.parent() {
            sync_directory(parent)?;
        }
        Ok(())
    }

    fn abandon_for_circuit(&mut self) -> Option<PathBuf> {
        // The existing temporary artifact is already unique and contains an
        // immutable verified prefix. Preserve it before disconnecting the
        // channel so the writer cannot remove it if a blocked syscall later
        // returns. The detached writer may then append more records, but its
        // positioned writes never overwrite the published prefix. Readers
        // therefore validate the live artifact as a provisional recovered
        // trace. This adds no filesystem operation to the failure path.
        self.preserve_temporary.store(true, Ordering::Release);
        self.sender.take();
        // Dropping a JoinHandle detaches the thread. It still owns the file,
        // receiver, and already-accounted queued commands, but process poison
        // ensures no callback or later capture can enqueue more work.
        self.join.take();
        if self.recovery_path.is_none() && self.progress.verified_len() != 0 {
            self.recovery_path = Some(self.temporary.as_ref().clone());
        }
        self.recovery_path.clone()
    }
}

impl Drop for TraceWriter {
    fn drop(&mut self) {
        if self.process_id != std::process::id() {
            self.detach_after_fork();
            return;
        }
        if self.join.is_some() {
            if self.runtime.is_open() {
                self.abandon_for_circuit();
                return;
            }
            self.sender.take();
            {
                let mut resident = self
                    .runtime
                    .resident
                    .lock()
                    .expect("resident budget poisoned");
                while !self.progress.is_finished() && !self.runtime.is_open() {
                    resident = self
                        .runtime
                        .changed
                        .wait(resident)
                        .expect("resident budget poisoned");
                }
            }
            if self.runtime.is_open() && !self.progress.is_finished() {
                self.abandon_for_circuit();
                return;
            }
            if let Some(join) = self.join.take() {
                let _ = join.join();
            }
            let _ = remove_file(self.temporary.as_ref());
        }
    }
}

fn circuit_abandon_error(recovered: Option<&Path>) -> io::Error {
    let message = match recovered {
        Some(path) => format!(
            "Kolo trace writer circuit breaker opened; the capture was abandoned and a recovered prefix is available at {}. Tracing is disabled until process restart",
            path.display()
        ),
        None => "Kolo trace writer circuit breaker opened before a recoverable prefix could be published; the capture was abandoned. Tracing is disabled until process restart".to_string(),
    };
    io::Error::new(io::ErrorKind::TimedOut, message)
}

fn writer_main(
    file: File,
    receiver: std::sync::mpsc::Receiver<Command>,
    header_payload: Vec<u8>,
    temporary: &Path,
    progress: &WriterProgress,
    preserve_temporary: &AtomicBool,
) -> io::Result<()> {
    // Keep record headers and sidecars batched, but let a normal 512 KiB chunk
    // bypass BufWriter rather than copying the whole chunk into a second 1 MiB
    // resident buffer before it reaches the final artifact.
    let mut writer = BufWriter::with_capacity(WRITER_BUFFER, PositionedWriter::new(file));
    write_header(&mut writer, &header_payload)?;
    let mut offset = HEADER_LEN + header_payload.len() as u64;
    writer.flush()?;
    progress.mark_verified(offset);
    let mut index = Vec::new();
    loop {
        match receiver.recv() {
            Ok(Command::Value {
                id,
                encoded,
                reservation,
            }) => {
                let (written, entry) =
                    match write_record(&mut writer, offset, 5, 0, id as u64, 1, &encoded) {
                        Ok(written) => written,
                        Err(error) => {
                            fail_queued_chunks(&receiver, &error);
                            return Err(error);
                        }
                    };
                offset += written;
                index.push(entry);
                reservation.complete_writer_command();
            }
            Ok(Command::Chunk {
                chunk,
                reservation,
                handle,
            }) => {
                let result = write_chunk(&mut writer, offset, &chunk);
                let (stored_len, entry, frame_payload_offset) = match result {
                    Ok(written) => written,
                    Err(error) => {
                        handle.fail(&error);
                        fail_queued_chunks(&receiver, &error);
                        return Err(error);
                    }
                };
                if let Err(error) = writer.flush() {
                    handle.fail(&error);
                    fail_queued_chunks(&receiver, &error);
                    return Err(error);
                }
                handle.commit(frame_payload_offset);
                offset += RECORD_HEADER_LEN + stored_len as u64;
                progress.mark_verified(offset);
                index.push(entry);
                reservation.complete_writer_command();
            }
            Ok(Command::Finish {
                thread_meta,
                metadata,
                layouts,
            }) => {
                for (sequence, (token, payload)) in thread_meta.into_iter().enumerate() {
                    let (written, entry) =
                        write_record(&mut writer, offset, 2, token, sequence as u64, 1, &payload)?;
                    offset += written;
                    index.push(entry);
                }
                let (written, entry) = write_record(&mut writer, offset, 3, 0, 0, 1, &metadata)?;
                offset += written;
                index.push(entry);
                let index_offset = offset;
                let payload = encode_index(&index, &layouts);
                let (written, _index_entry) =
                    write_record(&mut writer, offset, 4, 0, 0, index.len() as u32, &payload)?;
                offset += written;
                write_footer(&mut writer, index_offset, offset + FOOTER_LEN)?;
                writer.flush()?;
                writer.get_ref().file.sync_all()?;
                return Ok(());
            }
            #[cfg(test)]
            Ok(Command::FailForTest) => {
                let error = io::Error::new(io::ErrorKind::Other, "injected writer failure");
                fail_queued_chunks(&receiver, &error);
                return Err(error);
            }
            #[cfg(test)]
            Ok(Command::StallForTest(stall)) => stall.wait(),
            #[cfg(test)]
            Ok(Command::PanicForTest(entered)) => {
                let _ = entered.send(());
                panic!("injected writer panic");
            }
            Err(_) => {
                drop(writer);
                if !preserve_temporary.load(Ordering::Acquire) {
                    let _ = remove_file(temporary);
                }
                return Err(io::Error::new(
                    io::ErrorKind::BrokenPipe,
                    "trace capture abandoned",
                ));
            }
        }
    }
}

fn fail_queued_chunks(receiver: &std::sync::mpsc::Receiver<Command>, error: &io::Error) {
    for queued in receiver.try_iter() {
        if let Command::Chunk { handle, .. } = queued {
            handle.fail(error);
        }
    }
}

fn write_header(writer: &mut impl Write, payload: &[u8]) -> io::Result<()> {
    let length = u32::try_from(payload.len()).map_err(|_| invalid_size())?;
    let mut header = Vec::with_capacity(24);
    header.extend_from_slice(HEADER_MAGIC);
    header.extend_from_slice(&3u16.to_le_bytes());
    header.push(2); // frame MessagePack may contain exact value references
    header.push(0); // no compression
    header.extend_from_slice(&0u32.to_le_bytes());
    header.extend_from_slice(&length.to_le_bytes());
    header.extend_from_slice(&crc32(payload).to_le_bytes());
    writer.write_all(&header)?;
    writer.write_all(payload)
}

fn write_chunk(
    writer: &mut impl Write,
    offset: u64,
    chunk: &SealedChunk,
) -> io::Result<(u32, IndexEntry, u64)> {
    let mut sidecar = Vec::with_capacity(chunk.frame_ends.len() * 2);
    let mut frame_start = 0u64;
    for &frame_end in chunk.frame_ends.iter() {
        let length = frame_end
            .checked_sub(frame_start)
            .ok_or_else(invalid_size)?;
        write_uleb128(&mut sidecar, length);
        frame_start = frame_end;
    }
    let stored_len = u32::try_from(
        sidecar
            .len()
            .checked_add(chunk.bytes.len())
            .ok_or_else(invalid_size)?,
    )
    .map_err(|_| invalid_size())?;
    let header = record_header(
        1,
        chunk.thread_token,
        chunk.sequence,
        u32::try_from(chunk.frame_count()).map_err(|_| invalid_size())?,
        stored_len,
        0, // frame chunks stay off the callback's critical path; see format spec
    );
    writer.write_all(&header)?;
    writer.write_all(&sidecar)?;
    writer.write_all(&chunk.bytes)?;
    let frame_payload_offset = offset
        .checked_add(RECORD_HEADER_LEN)
        .and_then(|value| value.checked_add(sidecar.len() as u64))
        .ok_or_else(invalid_size)?;
    Ok((
        stored_len,
        IndexEntry {
            kind: 1,
            offset,
            stored_len,
            thread_token: chunk.thread_token,
            sequence: chunk.sequence,
            frame_count: chunk.frame_count() as u32,
        },
        frame_payload_offset,
    ))
}

fn write_record(
    writer: &mut impl Write,
    offset: u64,
    kind: u8,
    token: u32,
    sequence: u64,
    count: u32,
    payload: &[u8],
) -> io::Result<(u64, IndexEntry)> {
    let length = u32::try_from(payload.len()).map_err(|_| invalid_size())?;
    writer.write_all(&record_header(
        kind,
        token,
        sequence,
        count,
        length,
        crc32(payload),
    ))?;
    writer.write_all(payload)?;
    Ok((
        RECORD_HEADER_LEN + length as u64,
        IndexEntry {
            kind,
            offset,
            stored_len: length,
            thread_token: token,
            sequence,
            frame_count: count,
        },
    ))
}

fn record_header(
    kind: u8,
    token: u32,
    sequence: u64,
    count: u32,
    length: u32,
    payload_crc: u32,
) -> [u8; 40] {
    let mut header = [0; 40];
    header[..4].copy_from_slice(RECORD_MAGIC);
    header[4] = kind;
    header[8..12].copy_from_slice(&token.to_le_bytes());
    header[12..20].copy_from_slice(&sequence.to_le_bytes());
    header[20..24].copy_from_slice(&count.to_le_bytes());
    header[24..28].copy_from_slice(&length.to_le_bytes());
    header[28..32].copy_from_slice(&length.to_le_bytes());
    header[32..36].copy_from_slice(&payload_crc.to_le_bytes());
    let header_crc = crc32(&header[..36]);
    header[36..40].copy_from_slice(&header_crc.to_le_bytes());
    header
}

fn encode_index(entries: &[IndexEntry], layouts: &[ThreadLayout]) -> Vec<u8> {
    let mut out = Vec::new();
    rmp::encode::write_map_len(&mut out, 2).expect("memory write");
    rmp::encode::write_str(&mut out, "records").expect("memory write");
    rmp::encode::write_array_len(&mut out, entries.len() as u32).expect("memory write");
    for entry in entries {
        rmp::encode::write_array_len(&mut out, 6).expect("memory write");
        rmp::encode::write_uint(&mut out, entry.kind as u64).expect("memory write");
        rmp::encode::write_uint(&mut out, entry.offset).expect("memory write");
        rmp::encode::write_uint(&mut out, entry.stored_len as u64).expect("memory write");
        rmp::encode::write_uint(&mut out, entry.thread_token as u64).expect("memory write");
        rmp::encode::write_uint(&mut out, entry.sequence).expect("memory write");
        rmp::encode::write_uint(&mut out, entry.frame_count as u64).expect("memory write");
    }
    rmp::encode::write_str(&mut out, "threads").expect("memory write");
    rmp::encode::write_map_len(&mut out, layouts.len() as u32).expect("memory write");
    for layout in layouts {
        rmp::encode::write_uint(&mut out, layout.thread_token as u64).expect("memory write");
        rmp::encode::write_array_len(&mut out, layout.spans.len() as u32).expect("memory write");
        for span in &layout.spans {
            rmp::encode::write_array_len(&mut out, 3).expect("memory write");
            rmp::encode::write_uint(&mut out, span.sequence).expect("memory write");
            rmp::encode::write_uint(&mut out, span.first_frame as u64).expect("memory write");
            rmp::encode::write_uint(&mut out, span.frame_count as u64).expect("memory write");
        }
    }
    out
}

fn write_footer(writer: &mut impl Write, index_offset: u64, file_len: u64) -> io::Result<()> {
    let mut footer = [0; 32];
    footer[..8].copy_from_slice(FOOTER_MAGIC);
    footer[8..16].copy_from_slice(&index_offset.to_le_bytes());
    footer[16..24].copy_from_slice(&file_len.to_le_bytes());
    let crc = crc32(&footer[..24]);
    footer[24..28].copy_from_slice(&crc.to_le_bytes());
    writer.write_all(&footer)
}

fn write_uleb128(out: &mut Vec<u8>, mut value: u64) {
    loop {
        let mut byte = (value & 0x7f) as u8;
        value >>= 7;
        if value != 0 {
            byte |= 0x80;
        }
        out.push(byte);
        if value == 0 {
            break;
        }
    }
}

fn crc32(bytes: &[u8]) -> u32 {
    crc32fast::hash(bytes)
}
fn invalid_size() -> io::Error {
    io::Error::new(
        io::ErrorKind::InvalidData,
        "v3 field exceeds its declared width",
    )
}

/// Buffered writes whose underlying file position is explicit on every OS.
/// This prevents Windows positional snapshot reads from redirecting a shared
/// writer cursor while a trace-point range is materialized.
struct PositionedWriter {
    file: File,
    offset: u64,
}

impl PositionedWriter {
    fn new(file: File) -> Self {
        Self { file, offset: 0 }
    }
}

impl Write for PositionedWriter {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        let written = write_at(&self.file, buf, self.offset)?;
        self.offset = self
            .offset
            .checked_add(written as u64)
            .ok_or_else(invalid_size)?;
        Ok(written)
    }

    fn flush(&mut self) -> io::Result<()> {
        self.file.flush()
    }
}

#[cfg(unix)]
fn write_at(file: &File, buf: &[u8], offset: u64) -> io::Result<usize> {
    file.write_at(buf, offset)
}

#[cfg(windows)]
fn write_at(file: &File, buf: &[u8], offset: u64) -> io::Result<usize> {
    file.seek_write(buf, offset)
}

#[cfg(unix)]
fn read_exact_at(file: &File, mut buf: &mut [u8], mut offset: u64) -> io::Result<()> {
    while !buf.is_empty() {
        let read = file.read_at(buf, offset)?;
        if read == 0 {
            return Err(io::Error::new(
                io::ErrorKind::UnexpectedEof,
                "short trace read",
            ));
        }
        offset += read as u64;
        buf = &mut buf[read..];
    }
    Ok(())
}

#[cfg(windows)]
fn read_exact_at(file: &File, mut buf: &mut [u8], mut offset: u64) -> io::Result<()> {
    while !buf.is_empty() {
        let read = file.seek_read(buf, offset)?;
        if read == 0 {
            return Err(io::Error::new(
                io::ErrorKind::UnexpectedEof,
                "short trace read",
            ));
        }
        offset += read as u64;
        buf = &mut buf[read..];
    }
    Ok(())
}

#[cfg(not(windows))]
fn replace_file(from: &Path, to: &Path) -> io::Result<()> {
    rename(from, to)
}

#[cfg(windows)]
fn replace_file(from: &Path, to: &Path) -> io::Result<()> {
    use std::os::windows::ffi::OsStrExt;
    type Bool = i32;
    #[link(name = "kernel32")]
    extern "system" {
        fn ReplaceFileW(
            replaced: *const u16,
            replacement: *const u16,
            backup: *const u16,
            flags: u32,
            exclude: *mut std::ffi::c_void,
            reserved: *mut std::ffi::c_void,
        ) -> Bool;
    }
    if !to.exists() {
        return rename(from, to);
    }
    let replaced: Vec<u16> = to.as_os_str().encode_wide().chain(Some(0)).collect();
    let replacement: Vec<u16> = from.as_os_str().encode_wide().chain(Some(0)).collect();
    // ReplaceFileW is the Windows primitive that preserves the no-incomplete-
    // destination guarantee; remove-then-rename would create a visibility gap.
    let ok = unsafe {
        ReplaceFileW(
            replaced.as_ptr(),
            replacement.as_ptr(),
            std::ptr::null(),
            0,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
        )
    };
    if ok == 0 {
        Err(io::Error::last_os_error())
    } else {
        Ok(())
    }
}

#[cfg(unix)]
fn sync_directory(path: &Path) -> io::Result<()> {
    File::open(path)?.sync_all()
}
#[cfg(not(unix))]
fn sync_directory(_path: &Path) -> io::Result<()> {
    Ok(())
}

/// Capture-wide ownership of the one final-artifact writer. Callbacks touch
/// this mutex only when an arena seals, never for each frame.
pub(crate) struct TraceCapture {
    state: Mutex<CaptureState>,
    runtime: Arc<WriterRuntime>,
    process_fork_generation: ProcessForkGeneration,
    in_memory: AtomicBool,
}

struct CaptureState {
    destination: PathBuf,
    temporary: Arc<PathBuf>,
    snapshot: Arc<SnapshotFile>,
    header_payload: Option<Vec<u8>>,
    writer: Option<TraceWriter>,
    published_values: Vec<bool>,
    closed: bool,
    recovery_path: Option<PathBuf>,
}

impl CaptureState {
    fn ensure_writer(&mut self, runtime: &Arc<WriterRuntime>) -> io::Result<()> {
        if self.writer.is_none() {
            let header_payload = self
                .header_payload
                .take()
                .ok_or_else(|| io::Error::new(io::ErrorKind::BrokenPipe, "trace writer closed"))?;
            match TraceWriter::start_at(
                self.destination.clone(),
                Arc::clone(&self.temporary),
                Arc::clone(&self.snapshot),
                header_payload,
                Arc::clone(runtime),
            ) {
                Ok(writer) => self.writer = Some(writer),
                Err(error) => return Err(error),
            }
        }
        Ok(())
    }
}

impl TraceCapture {
    pub(crate) fn for_trace(db_path: &str, trace_id: &str, timestamp: f64) -> Arc<Self> {
        let raw_directory = Path::new(db_path)
            .parent()
            .unwrap_or_else(|| Path::new("."))
            .join("raw");
        let destination = raw_directory.join(format!("{trace_id}.kolo"));
        let header_payload = encode_header_payload(trace_id, timestamp);
        Self::start(destination, header_payload)
    }

    pub(crate) fn start(destination: PathBuf, header_payload: Vec<u8>) -> Arc<Self> {
        Self::start_with_runtime(destination, header_payload, Arc::clone(writer_runtime()))
    }

    #[cfg(test)]
    pub(crate) fn start_with_open_test_circuit(
        destination: PathBuf,
        header_payload: Vec<u8>,
    ) -> Arc<Self> {
        let runtime = Arc::new(WriterRuntime::new(Duration::ZERO, false));
        let capture = Self::start_with_runtime(destination, header_payload, Arc::clone(&runtime));
        runtime.open_circuit();
        capture
    }

    fn start_with_runtime(
        destination: PathBuf,
        header_payload: Vec<u8>,
        runtime: Arc<WriterRuntime>,
    ) -> Arc<Self> {
        let temporary = Arc::new(TraceWriter::temporary_path(&destination));
        let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
        let closed = runtime.is_open();
        Arc::new(Self {
            state: Mutex::new(CaptureState {
                destination,
                temporary,
                snapshot,
                header_payload: Some(header_payload),
                writer: None,
                published_values: Vec::new(),
                closed,
                recovery_path: None,
            }),
            runtime,
            process_fork_generation: ProcessForkGeneration::capture(),
            in_memory: AtomicBool::new(false),
        })
    }

    /// Switch an inherited capture to the synchronous in-memory path. The
    /// worker thread belongs to the parent process and cannot be joined or
    /// reused by the child.
    pub(crate) fn enter_post_fork_mode(&self) -> bool {
        if !self.process_fork_generation.has_changed() {
            return false;
        }
        self.keep_in_memory();
        true
    }

    pub(crate) fn keep_in_memory(&self) {
        if self.in_memory.swap(true, Ordering::AcqRel) {
            return;
        }
        let mut state = self.state.lock().expect("trace writer mutex poisoned");
        if let Some(mut writer) = state.writer.take() {
            writer.detach_after_fork();
        }
    }

    pub(crate) fn is_in_memory(&self) -> bool {
        self.in_memory.load(Ordering::Acquire)
    }

    fn abandon_for_circuit(&self) -> io::Error {
        let mut state = self.state.lock().expect("trace writer mutex poisoned");
        state.closed = true;
        if let Some(mut writer) = state.writer.take() {
            if let Some(recovered) = writer.abandon_for_circuit() {
                state.recovery_path = Some(recovered);
            }
        }
        circuit_abandon_error(state.recovery_path.as_deref())
    }

    fn submit(&self, chunk: SealedChunk) -> io::Result<Arc<ChunkHandle>> {
        // A child cannot use the parent's worker or resident-budget progress.
        // Detect the process boundary before either can block. This runs once
        // per sealed chunk, not once per captured frame.
        self.enter_post_fork_mode();
        let resident = chunk.resident_len();
        #[cfg(not(target_arch = "wasm32"))]
        let reservation = if self.is_in_memory() {
            None
        } else {
            Some(match self.runtime.reserve(resident) {
                Ok(reservation) => reservation,
                Err(_) if self.runtime.is_open() => return Err(self.abandon_for_circuit()),
                Err(error) => return Err(error),
            })
        };
        let mut state = self.state.lock().expect("trace writer mutex poisoned");
        if state.closed {
            return Err(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "trace writer closed",
            ));
        }
        let handle = Arc::new(ChunkHandle::memory(
            Arc::clone(&state.snapshot),
            chunk.thread_token,
            chunk.sequence,
            Arc::clone(&chunk.frame_ends),
            Arc::clone(&chunk.bytes),
        ));
        if self.is_in_memory() {
            return Ok(handle);
        }
        // Pyodide has no native worker threads or durable host filesystem to
        // stream into. Keep its sealed chunks in the same logical store and
        // materialize the v3 container once at save time. Native builds take
        // the bounded background-writer path below.
        #[cfg(target_arch = "wasm32")]
        {
            let _ = resident;
            return Ok(handle);
        }
        #[cfg(not(target_arch = "wasm32"))]
        {
            if let Err(error) = state.ensure_writer(&self.runtime) {
                handle.fail(&error);
                return Err(error);
            }
            state
                .writer
                .as_ref()
                .expect("writer was just created")
                .submit_reserved(
                    chunk,
                    Arc::clone(&handle),
                    reservation.expect("streaming chunks reserve resident bytes"),
                )?;
            Ok(handle)
        }
    }

    pub(crate) fn publish_value(&self, id: u32, encoded: Arc<[u8]>) -> io::Result<()> {
        // Value publication is the first operation that can start a writer.
        // A forked child must switch to synchronous materialization before it
        // can reuse the inherited sender or wait on inherited progress.
        self.enter_post_fork_mode();
        let index = id as usize;
        if self.is_in_memory() {
            let mut state = self.state.lock().expect("trace writer mutex poisoned");
            if state.closed {
                return Err(io::Error::new(
                    io::ErrorKind::BrokenPipe,
                    "trace writer closed",
                ));
            }
            let _ = encoded;
            if state.published_values.len() <= index {
                state.published_values.resize(index + 1, false);
            }
            state.published_values[index] = true;
            return Ok(());
        }
        #[cfg(target_arch = "wasm32")]
        {
            let mut state = self.state.lock().expect("trace writer mutex poisoned");
            if state.closed {
                return Err(io::Error::new(
                    io::ErrorKind::BrokenPipe,
                    "trace writer closed",
                ));
            }
            if state.published_values.get(index).copied().unwrap_or(false) {
                return Ok(());
            }
            let _ = encoded;
            if state.published_values.len() <= index {
                state.published_values.resize(index + 1, false);
            }
            state.published_values[index] = true;
            return Ok(());
        }
        #[cfg(not(target_arch = "wasm32"))]
        {
            // Never wait for the process-wide resident budget while holding
            // capture state. Chunk submission reserves in the same order;
            // reversing it here would deadlock free-threaded publishers and
            // submitters under backpressure.
            {
                let state = self.state.lock().expect("trace writer mutex poisoned");
                if state.closed {
                    return Err(io::Error::new(
                        io::ErrorKind::BrokenPipe,
                        "trace writer closed",
                    ));
                }
                if state.published_values.get(index).copied().unwrap_or(false) {
                    return Ok(());
                }
            }
            let reservation = match self.runtime.reserve(encoded.len()) {
                Ok(reservation) => reservation,
                Err(_) if self.runtime.is_open() => return Err(self.abandon_for_circuit()),
                Err(error) => return Err(error),
            };
            let mut state = self.state.lock().expect("trace writer mutex poisoned");
            // Another publisher or finish may have won while this thread was
            // waiting for resident room. Recheck before sending anything.
            if state.closed {
                return Err(io::Error::new(
                    io::ErrorKind::BrokenPipe,
                    "trace writer closed",
                ));
            }
            if state.published_values.get(index).copied().unwrap_or(false) {
                return Ok(());
            }
            state.ensure_writer(&self.runtime)?;
            state
                .writer
                .as_ref()
                .expect("writer was just created")
                .publish_value_reserved(id, encoded, reservation)?;
            if state.published_values.len() <= index {
                state.published_values.resize(index + 1, false);
            }
            state.published_values[index] = true;
            Ok(())
        }
    }

    pub(crate) fn published_value_ids(&self) -> Vec<u32> {
        self.state
            .lock()
            .expect("trace writer mutex poisoned")
            .published_values
            .iter()
            .enumerate()
            .filter_map(|(id, published)| {
                published.then(|| u32::try_from(id).expect("published value IDs are u32"))
            })
            .collect()
    }

    pub(crate) fn writer_circuit_is_open(&self) -> bool {
        self.runtime.is_open()
    }

    pub(crate) fn publish_table(&self, values: &[(u32, Arc<[u8]>)]) -> io::Result<()> {
        for (id, value) in values {
            self.publish_value(*id, Arc::clone(value))?;
        }
        Ok(())
    }

    pub(crate) fn finish(
        &self,
        thread_meta: Vec<(u32, Vec<u8>)>,
        metadata: Vec<u8>,
        layouts: Vec<ThreadLayout>,
    ) -> io::Result<()> {
        if self.runtime.is_open() {
            return Err(self.abandon_for_circuit());
        }
        let writer = {
            let mut state = self.state.lock().expect("trace writer mutex poisoned");
            if state.closed {
                return Err(io::Error::new(
                    io::ErrorKind::BrokenPipe,
                    "trace writer closed",
                ));
            }
            state.ensure_writer(&self.runtime)?;
            state.closed = true;
            state
                .writer
                .take()
                .expect("finish always starts the writer")
        };
        writer.finish(thread_meta, metadata, layouts)
    }

    #[cfg(test)]
    fn is_streaming(&self) -> bool {
        self.state
            .lock()
            .expect("trace writer mutex poisoned")
            .writer
            .is_some()
    }

    #[cfg(test)]
    fn recovery_path(&self) -> Option<PathBuf> {
        self.state
            .lock()
            .expect("trace writer mutex poisoned")
            .recovery_path
            .clone()
    }
}

fn encode_header_payload(trace_id: &str, timestamp: f64) -> Vec<u8> {
    let mut header_payload = Vec::new();
    rmp::encode::write_map_len(&mut header_payload, 2).expect("memory write");
    rmp::encode::write_str(&mut header_payload, "trace_id").expect("memory write");
    rmp::encode::write_str(&mut header_payload, trace_id).expect("memory write");
    rmp::encode::write_str(&mut header_payload, "timestamp").expect("memory write");
    rmp::encode::write_f64(&mut header_payload, timestamp).expect("memory write");
    header_payload
}

#[derive(Clone)]
struct FrameSpan {
    logical_start: usize,
    handle: Arc<ChunkHandle>,
    first_frame: u32,
    frame_count: u32,
}

impl FrameSpan {
    fn logical_end(&self) -> usize {
        self.logical_start + self.frame_count as usize
    }

    fn frame_index(&self, logical_index: usize) -> io::Result<usize> {
        if logical_index < self.logical_start || logical_index >= self.logical_end() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid frame index",
            ));
        }
        Ok(self.first_frame as usize + logical_index - self.logical_start)
    }

    fn frame_len(&self, logical_index: usize) -> io::Result<usize> {
        self.handle.frame_len(self.frame_index(logical_index)?)
    }

    fn read_frame(&self, logical_index: usize, scratch: &mut Vec<u8>) -> io::Result<()> {
        self.handle
            .read_frame(self.frame_index(logical_index)?, scratch)
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct AppendResult {
    pub start_index: usize,
    pub end_index: usize,
    pub added_bytes: usize,
}

/// Per-thread logical frame sequence backed by one mutable arena plus compact
/// handles for sealed chunks already owned by the writer.
pub(crate) struct FrameStore {
    capture: Option<Arc<TraceCapture>>,
    thread_token: u32,
    arena: Option<FrameArena>,
    spans: Vec<FrameSpan>,
    sealed_frames: usize,
    total_bytes: usize,
    trace_name_index: TraceNameIndex,
    failed: bool,
}

impl FrameStore {
    pub(crate) fn new(capture: Arc<TraceCapture>, thread_token: u32) -> Self {
        Self {
            capture: Some(capture),
            thread_token,
            arena: Some(FrameArena::new(thread_token)),
            spans: Vec::new(),
            sealed_frames: 0,
            total_bytes: 0,
            trace_name_index: TraceNameIndex::default(),
            failed: false,
        }
    }

    #[cfg(test)]
    fn with_target(capture: Arc<TraceCapture>, thread_token: u32, target: usize) -> Self {
        Self {
            capture: Some(capture),
            thread_token,
            arena: Some(FrameArena::with_target(thread_token, target)),
            spans: Vec::new(),
            sealed_frames: 0,
            total_bytes: 0,
            trace_name_index: TraceNameIndex::default(),
            failed: false,
        }
    }

    fn detached(
        &self,
        mut spans: Vec<FrameSpan>,
        total_bytes: usize,
        trace_name_index: TraceNameIndex,
    ) -> Self {
        let sealed_frames = normalize_spans(&mut spans);
        Self {
            capture: Some(Arc::clone(
                self.capture
                    .as_ref()
                    .expect("cannot detach from a retired frame store"),
            )),
            thread_token: self.thread_token,
            arena: None,
            spans,
            sealed_frames,
            total_bytes,
            trace_name_index,
            failed: false,
        }
    }

    pub(crate) fn len(&self) -> usize {
        self.sealed_frames + self.arena.as_ref().map_or(0, FrameArena::frame_count)
    }

    pub(crate) fn is_empty(&self) -> bool {
        self.len() == 0
    }

    pub(crate) fn total_bytes(&self) -> usize {
        self.total_bytes
    }

    pub(crate) fn thread_token(&self) -> u32 {
        self.thread_token
    }

    pub(crate) fn trace_name_observations(&self) -> Option<&[TraceNameObservation]> {
        self.trace_name_index.observations()
    }

    pub(crate) fn capture(&self) -> Option<Arc<TraceCapture>> {
        self.capture.as_ref().map(Arc::clone)
    }

    pub(crate) fn take(&mut self) -> Self {
        let replacement = Self {
            capture: None,
            thread_token: self.thread_token,
            arena: None,
            spans: Vec::new(),
            sealed_frames: 0,
            total_bytes: 0,
            trace_name_index: TraceNameIndex::default(),
            failed: false,
        };
        std::mem::replace(self, replacement)
    }

    pub(crate) fn append_encoded<E, F>(&mut self, encode: F) -> Result<AppendResult, E>
    where
        F: FnOnce(&mut Vec<u8>, &TraceCapture) -> Result<(), E>,
        E: From<io::Error>,
    {
        if self.failed {
            return Err(E::from(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "frame store writer failed",
            )));
        }
        let start_index = self.len();
        let capture = self
            .capture
            .as_deref()
            .expect("cannot append to a retired frame store");
        let arena = self
            .arena
            .as_mut()
            .expect("cannot append to a detached frame range");
        let before = arena.total_bytes();
        let sealed = arena.append_frame(|bytes| encode(bytes, capture))?;
        let added_bytes = arena.total_bytes().saturating_sub(before).max(
            sealed
                .as_ref()
                .map_or(0, |chunk| chunk.bytes.len().saturating_sub(before)),
        );
        self.total_bytes = self.total_bytes.saturating_add(added_bytes);
        if let Some(chunk) = sealed {
            self.commit_chunk(chunk).map_err(E::from)?;
        }
        Ok(AppendResult {
            start_index,
            end_index: start_index + 1,
            added_bytes,
        })
    }

    pub(crate) fn append_serialized(
        &mut self,
        frame: &SerializedFrame,
    ) -> io::Result<AppendResult> {
        self.append_encoded::<io::Error, _>(|arena, _capture| {
            arena.extend_from_slice(frame);
            Ok(())
        })
    }

    pub(crate) fn append_many(
        &mut self,
        frames: &mut Vec<SerializedFrame>,
    ) -> io::Result<AppendResult> {
        let start_index = self.len();
        let before = self.total_bytes;
        for frame in frames.drain(..) {
            self.append_encoded::<io::Error, _>(|arena, _capture| {
                arena.extend_from_slice(&frame);
                Ok(())
            })?;
        }
        Ok(AppendResult {
            start_index,
            end_index: self.len(),
            added_bytes: self.total_bytes.saturating_sub(before),
        })
    }

    pub(crate) fn append_many_with_frame_types(
        &mut self,
        frames: &mut Vec<SerializedFrame>,
        frame_types: &[String],
    ) -> io::Result<AppendResult> {
        if frames.len() != frame_types.len() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "frame data/type count mismatch",
            ));
        }
        let start_index = self.len();
        let mut new_trace_name_index = TraceNameIndex::default();
        if self.trace_name_index.observations().is_some() {
            for (offset, (frame_type, frame)) in frame_types.iter().zip(frames.iter()).enumerate() {
                new_trace_name_index.observe(start_index + offset, frame_type, frame);
            }
        }
        let appended = self.append_many(frames)?;
        debug_assert_eq!(
            appended.end_index - appended.start_index,
            frame_types.len(),
            "a successful batch append consumes every input frame"
        );
        self.trace_name_index.merge(new_trace_name_index);
        Ok(appended)
    }

    fn commit_chunk(&mut self, chunk: SealedChunk) -> io::Result<()> {
        let count = chunk.frame_count();
        let submitted = self
            .capture
            .as_ref()
            .ok_or_else(|| io::Error::new(io::ErrorKind::BrokenPipe, "frame store retired"))?
            .submit(chunk);
        let handle = match submitted {
            Ok(handle) => handle,
            Err(error) => {
                // The sealed bytes have left the arena but were not accepted
                // by the writer. Poison this logical store so later subtree or
                // trace-point operations cannot reinterpret shifted indices
                // and persist the wrong frames through a fresh capture.
                self.failed = true;
                return Err(error);
            }
        };
        let frame_count = u32::try_from(count).map_err(|_| invalid_size())?;
        self.spans.push(FrameSpan {
            logical_start: self.sealed_frames,
            handle,
            first_frame: 0,
            frame_count,
        });
        self.sealed_frames = self
            .sealed_frames
            .checked_add(count)
            .ok_or_else(invalid_size)?;
        Ok(())
    }

    pub(crate) fn seal(&mut self) -> io::Result<()> {
        if self.failed {
            return Err(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "frame store writer failed",
            ));
        }
        let Some(arena) = self.arena.as_mut() else {
            return Ok(());
        };
        if let Some(chunk) = arena.seal() {
            self.commit_chunk(chunk)?;
        }
        Ok(())
    }

    /// Copy a logical range without sealing the current arena.
    ///
    /// Trace points need owned frame bytes for their asynchronous save, but
    /// they do not mutate the parent trace. Sealing here would turn every
    /// tiny trace point into a writer chunk and force otherwise-hot capture
    /// through the channel/disk path. Existing sealed spans are read through
    /// their handles while the open suffix is copied directly from memory.
    pub(crate) fn copy_range(&self, range: Range<usize>) -> io::Result<Vec<SerializedFrame>> {
        if self.failed {
            return Err(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "frame store writer failed",
            ));
        }
        if range.start > range.end || range.end > self.len() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid frame range",
            ));
        }
        let mut frames = Vec::with_capacity(range.len());
        let mut scratch = Vec::new();
        for index in range {
            frames.push(self.frame(index, &mut scratch)?.to_vec());
        }
        Ok(frames)
    }

    pub(crate) fn drain(&mut self, range: Range<usize>) -> io::Result<Self> {
        self.seal()?;
        if range.start > range.end || range.end > self.sealed_frames {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid frame range",
            ));
        }
        let removed = slice_spans(&self.spans, range.clone());
        let total_bytes = span_bytes(&removed)?;
        let mut remaining = slice_spans(&self.spans, 0..range.start);
        remaining.extend(slice_spans(&self.spans, range.end..self.sealed_frames));
        self.sealed_frames = normalize_spans(&mut remaining);
        self.spans = remaining;
        self.total_bytes = self.total_bytes.saturating_sub(total_bytes);
        let removed_trace_name_index = self.trace_name_index.drain(range);
        Ok(self.detached(removed, total_bytes, removed_trace_name_index))
    }

    pub(crate) fn insert_store(&mut self, index: usize, mut other: Self) -> io::Result<()> {
        self.seal()?;
        other.seal()?;
        let same_capture = self
            .capture
            .as_ref()
            .zip(other.capture.as_ref())
            .is_some_and(|(left, right)| Arc::ptr_eq(left, right));
        if index > self.sealed_frames || !same_capture {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "incompatible frame range insertion",
            ));
        }
        // seal() above makes len() equal sealed_frames. Use the semantic
        // quantity here so observation reindexing stays obviously coupled to
        // the number of frames inserted, not the storage representation.
        let inserted_frames = other.len();
        self.trace_name_index
            .shift_for_insert(index, inserted_frames);
        other.trace_name_index.shift_for_insert(0, index);
        self.trace_name_index.merge(other.trace_name_index);
        self.total_bytes = self.total_bytes.saturating_add(other.total_bytes);
        let mut spans = slice_spans(&self.spans, 0..index);
        spans.append(&mut other.spans);
        spans.extend(slice_spans(&self.spans, index..self.sealed_frames));
        self.sealed_frames = normalize_spans(&mut spans);
        self.spans = spans;
        Ok(())
    }

    pub(crate) fn insert_frame(&mut self, index: usize, frame: SerializedFrame) -> io::Result<()> {
        self.seal()?;
        if index > self.sealed_frames {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid frame index",
            ));
        }
        self.append_serialized(&frame)?;
        self.seal()?;
        // Production callers insert synthetic subtree placeholders. Rather
        // than teach this generic range primitive about plugin frame types,
        // conservatively fall back to the exact positional name resolver for
        // any store whose logical layout gained an explicit frame.
        self.trace_name_index.mark_incomplete();
        let inserted = self
            .spans
            .pop()
            .expect("one appended frame must produce one span");
        self.sealed_frames -= 1;
        let mut spans = slice_spans(&self.spans, 0..index);
        spans.push(inserted);
        spans.extend(slice_spans(&self.spans, index..self.sealed_frames));
        self.sealed_frames = normalize_spans(&mut spans);
        self.spans = spans;
        Ok(())
    }

    pub(crate) fn layout(&mut self) -> io::Result<ThreadLayout> {
        self.seal()?;
        let spans = self
            .spans
            .iter()
            .map(|span| LayoutSpan {
                sequence: span.handle.sequence(),
                first_frame: span.first_frame,
                frame_count: span.frame_count,
            })
            .collect();
        Ok(ThreadLayout {
            thread_token: self.thread_token,
            spans,
        })
    }
}

fn normalize_spans(spans: &mut Vec<FrameSpan>) -> usize {
    let mut normalized: Vec<FrameSpan> = Vec::with_capacity(spans.len());
    let mut logical_start = 0usize;
    for mut span in spans.drain(..) {
        if span.frame_count == 0 {
            continue;
        }
        if let Some(last) = normalized.last_mut() {
            if Arc::ptr_eq(&last.handle, &span.handle)
                && last.first_frame + last.frame_count == span.first_frame
            {
                last.frame_count += span.frame_count;
                logical_start += span.frame_count as usize;
                continue;
            }
        }
        span.logical_start = logical_start;
        logical_start += span.frame_count as usize;
        normalized.push(span);
    }
    *spans = normalized;
    logical_start
}

fn slice_spans(spans: &[FrameSpan], range: Range<usize>) -> Vec<FrameSpan> {
    let mut sliced = Vec::new();
    for span in spans {
        let start = range.start.max(span.logical_start);
        let end = range.end.min(span.logical_end());
        if start >= end {
            continue;
        }
        sliced.push(FrameSpan {
            logical_start: 0,
            handle: Arc::clone(&span.handle),
            first_frame: span.first_frame + (start - span.logical_start) as u32,
            frame_count: (end - start) as u32,
        });
    }
    normalize_spans(&mut sliced);
    sliced
}

fn span_bytes(spans: &[FrameSpan]) -> io::Result<usize> {
    let mut total = 0usize;
    for span in spans {
        for frame_index in span.first_frame..span.first_frame + span.frame_count {
            total = total
                .checked_add(span.handle.frame_len(frame_index as usize)?)
                .ok_or_else(invalid_size)?;
        }
    }
    Ok(total)
}

fn find_span(spans: &[FrameSpan], index: usize) -> Option<&FrameSpan> {
    let position = spans.partition_point(|span| span.logical_start <= index);
    position
        .checked_sub(1)
        .and_then(|position| spans.get(position))
        .filter(|span| index < span.logical_end())
}

impl FrameSequence for FrameStore {
    fn len(&self) -> usize {
        FrameStore::len(self)
    }

    fn frame_len(&self, index: usize) -> io::Result<usize> {
        if self.failed {
            return Err(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "frame store writer failed",
            ));
        }
        if index < self.sealed_frames {
            return find_span(&self.spans, index)
                .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))?
                .frame_len(index);
        }
        let open_index = index.saturating_sub(self.sealed_frames);
        self.arena
            .as_ref()
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))?
            .frame_len(open_index)
    }

    fn frame<'a>(&'a self, index: usize, scratch: &'a mut Vec<u8>) -> io::Result<&'a [u8]> {
        if self.failed {
            return Err(io::Error::new(
                io::ErrorKind::BrokenPipe,
                "frame store writer failed",
            ));
        }
        if index < self.sealed_frames {
            find_span(&self.spans, index)
                .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))?
                .read_frame(index, scratch)?;
            return Ok(scratch);
        }
        let open_index = index.saturating_sub(self.sealed_frames);
        self.arena
            .as_ref()
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))?
            .frame(open_index)
    }
}

pub(crate) fn build_container_bytes<S: FrameSequence>(
    trace_id: &str,
    timestamp: f64,
    frames_by_thread: &HashMap<String, S>,
    thread_tokens: &HashMap<String, u32>,
    thread_meta: Vec<(u32, Vec<u8>)>,
    metadata: Vec<u8>,
    value_table: Vec<(u32, Arc<[u8]>)>,
) -> io::Result<Vec<u8>> {
    let header_payload = encode_header_payload(trace_id, timestamp);
    let frame_bytes = frames_by_thread
        .values()
        .try_fold(0usize, |total, frames| {
            let mut sequence_bytes = 0usize;
            for index in 0..frames.len() {
                sequence_bytes = sequence_bytes
                    .checked_add(frames.frame_len(index)?)
                    .ok_or_else(invalid_size)?;
            }
            total.checked_add(sequence_bytes).ok_or_else(invalid_size)
        })?;
    let mut out = Vec::with_capacity(
        frame_bytes
            .saturating_add(header_payload.len())
            .saturating_add(metadata.len())
            .saturating_add(4096),
    );
    write_header(&mut out, &header_payload)?;
    let mut offset = HEADER_LEN + header_payload.len() as u64;
    let mut index = Vec::new();
    let mut layouts = Vec::with_capacity(frames_by_thread.len());

    // Materialized containers publish their complete bounded value table
    // before chunks. The streaming path does the same lazily per referenced
    // ID, preserving this recovery invariant without writing unused values.
    for (id, value) in value_table {
        let (written, entry) = write_record(&mut out, offset, 5, 0, u64::from(id), 1, &value)?;
        offset += written;
        index.push(entry);
    }

    for (thread_id, frames) in frames_by_thread {
        let token = *thread_tokens.get(thread_id).ok_or_else(|| {
            io::Error::new(
                io::ErrorKind::InvalidInput,
                format!("missing v3 thread token for {thread_id}"),
            )
        })?;
        let mut arena = FrameArena::new(token);
        let mut spans = Vec::new();
        let mut scratch = Vec::new();
        for frame_index in 0..frames.len() {
            let frame = frames.frame(frame_index, &mut scratch)?;
            if let Some(chunk) = arena.append_frame::<io::Error, _>(|bytes| {
                bytes.extend_from_slice(frame);
                Ok(())
            })? {
                let frame_count = u32::try_from(chunk.frame_count()).map_err(|_| invalid_size())?;
                let sequence = chunk.sequence;
                let (stored_len, entry, _) = write_chunk(&mut out, offset, &chunk)?;
                offset += RECORD_HEADER_LEN + stored_len as u64;
                index.push(entry);
                spans.push(LayoutSpan {
                    sequence,
                    first_frame: 0,
                    frame_count,
                });
            }
        }
        if let Some(chunk) = arena.seal() {
            let frame_count = u32::try_from(chunk.frame_count()).map_err(|_| invalid_size())?;
            let sequence = chunk.sequence;
            let (stored_len, entry, _) = write_chunk(&mut out, offset, &chunk)?;
            offset += RECORD_HEADER_LEN + stored_len as u64;
            index.push(entry);
            spans.push(LayoutSpan {
                sequence,
                first_frame: 0,
                frame_count,
            });
        }
        layouts.push(ThreadLayout {
            thread_token: token,
            spans,
        });
    }

    for (sequence, (token, payload)) in thread_meta.into_iter().enumerate() {
        let (written, entry) =
            write_record(&mut out, offset, 2, token, sequence as u64, 1, &payload)?;
        offset += written;
        index.push(entry);
    }
    let (written, entry) = write_record(&mut out, offset, 3, 0, 0, 1, &metadata)?;
    offset += written;
    index.push(entry);
    let index_offset = offset;
    let index_payload = encode_index(&index, &layouts);
    let (written, _) = write_record(
        &mut out,
        offset,
        4,
        0,
        0,
        index.len() as u32,
        &index_payload,
    )?;
    offset += written;
    write_footer(&mut out, index_offset, offset + FOOTER_LEN)?;
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static TEST_ID: AtomicUsize = AtomicUsize::new(0);
    static RESIDENT_BUDGET_TEST_LOCK: Mutex<()> = Mutex::new(());

    #[test]
    fn process_fork_generation_detects_generation_and_pid_changes() {
        let generation = ProcessForkGeneration {
            generation: 7,
            process_id: 11,
            reliable: true,
        };

        assert!(!generation.has_changed_from(7, 11));
        assert!(generation.has_changed_from(8, 11));
        assert!(generation.has_changed_from(7, 12));
    }

    #[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
    #[test]
    fn process_fork_generation_uses_registered_atomic_identity() {
        assert!(ProcessForkGeneration::register());
        let generation = ProcessForkGeneration::capture();

        assert!(generation.reliable);
        assert_eq!(generation.process_id, 0);
        assert!(!generation.has_changed());
    }

    #[cfg(all(unix, not(target_arch = "wasm32"), target_has_atomic = "64"))]
    #[test]
    fn process_atfork_callback_advances_generation() {
        assert!(ProcessForkGeneration::register());
        // Mutate the process-global generation only in a child so parallel
        // capture tests in the parent cannot observe a simulated fork.
        let child = unsafe { libc::fork() };
        assert!(child >= 0, "fork failed");
        if child == 0 {
            let before = PROCESS_FORK_GENERATION.load(Ordering::Relaxed);
            // SAFETY: the at-fork callback's entire contract is a lock-free
            // atomic increment. The child performs no non-signal-safe work
            // after fork and exits directly below.
            unsafe { advance_process_fork_generation() };
            let advanced =
                PROCESS_FORK_GENERATION.load(Ordering::Relaxed) == before.wrapping_add(1);
            unsafe { libc::_exit(if advanced { 0 } else { 1 }) };
        }

        let mut status = 0;
        assert_eq!(unsafe { libc::waitpid(child, &mut status, 0) }, child);
        assert_eq!(status, 0, "child did not observe one generation advance");
    }

    struct FailAfterWrites(usize);

    impl Write for FailAfterWrites {
        fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
            if self.0 == 0 {
                return Err(io::Error::other("injected write failure"));
            }
            self.0 -= 1;
            Ok(buf.len())
        }

        fn flush(&mut self) -> io::Result<()> {
            Ok(())
        }
    }

    fn temp_path(name: &str) -> PathBuf {
        std::env::temp_dir().join(format!(
            "kolo-v3-{name}-{}-{}.kolo",
            std::process::id(),
            TEST_ID.fetch_add(1, Ordering::Relaxed)
        ))
    }

    #[test]
    fn arena_preserves_exact_bytes_and_rolls_back() {
        let mut arena = FrameArena::with_target(7, 64);
        assert!(arena
            .append_frame::<(), _>(|out| {
                out.extend_from_slice(b"\x82\xa1a\x01\xa1b\xc3");
                Ok(())
            })
            .unwrap()
            .is_none());
        let error = arena.append_frame::<&str, _>(|out| {
            out.extend_from_slice(b"partial");
            Err("fallback failed")
        });
        assert_eq!(error.unwrap_err(), "fallback failed");
        let chunk = arena.seal().unwrap();
        assert_eq!(chunk.bytes.as_slice(), b"\x82\xa1a\x01\xa1b\xc3");
        assert_eq!(chunk.frame_ends.as_ref(), [7]);
    }

    #[test]
    fn oversized_frame_is_one_chunk() {
        let mut arena = FrameArena::with_target(1, 8);
        let bytes = vec![42; 1024 * 1024];
        let chunk = arena
            .append_frame::<(), _>(|out| {
                out.extend_from_slice(&bytes);
                Ok(())
            })
            .unwrap()
            .unwrap();
        assert_eq!(chunk.frame_count(), 1);
        assert_eq!(chunk.bytes.as_slice(), bytes);
    }

    #[test]
    fn oversized_frame_round_trips_through_the_writer() {
        let path = temp_path("oversized-roundtrip");
        let frame = vec![42; DEFAULT_CHUNK_TARGET + 17];
        let mut arena = FrameArena::with_target(5, DEFAULT_CHUNK_TARGET);
        let chunk = arena
            .append_frame::<(), _>(|out| {
                out.extend_from_slice(&frame);
                Ok(())
            })
            .unwrap()
            .unwrap();
        let writer = TraceWriter::start(path.clone(), b"\x80".to_vec()).unwrap();
        let handle = writer.submit(chunk).unwrap();
        writer
            .finish(
                Vec::new(),
                b"\x80".to_vec(),
                vec![ThreadLayout {
                    thread_token: 5,
                    spans: vec![LayoutSpan {
                        sequence: 0,
                        first_frame: 0,
                        frame_count: 1,
                    }],
                }],
            )
            .unwrap();

        // Handles committed by the background writer must not depend on its
        // temporary pathname after finalization renames that file. A forked
        // child inherits this same open snapshot while the parent may rotate
        // or save its copy of the capture.
        let mut snapshot = Vec::new();
        handle.read_frame(0, &mut snapshot).unwrap();
        assert_eq!(snapshot, frame);

        let data = std::fs::read(&path).unwrap();
        let first_record = HEADER_LEN as usize + 1;
        assert_eq!(&data[first_record..first_record + 4], RECORD_MAGIC);
        assert_eq!(
            u32::from_le_bytes(
                data[first_record + 20..first_record + 24]
                    .try_into()
                    .unwrap()
            ),
            1
        );
        let payload_start = first_record + RECORD_HEADER_LEN as usize;
        let mut length = 0usize;
        let mut shift = 0;
        let mut frame_start = payload_start;
        loop {
            let byte = data[frame_start];
            frame_start += 1;
            length |= ((byte & 0x7f) as usize) << shift;
            if byte & 0x80 == 0 {
                break;
            }
            shift += 7;
        }
        assert_eq!(length, frame.len());
        assert_eq!(&data[frame_start..frame_start + length], frame);
        remove_file(path).unwrap();
    }

    #[test]
    fn final_file_contains_frame_once_and_footer() {
        let path = temp_path("complete");
        let mut arena = FrameArena::with_target(3, 4);
        let frame = b"unique-frame-payload";
        let chunk = arena
            .append_frame::<(), _>(|out| {
                out.extend_from_slice(frame);
                Ok(())
            })
            .unwrap()
            .unwrap();
        let writer = TraceWriter::start(
            path.clone(),
            b"\x82\xa8trace_id\xa1t\xa9timestamp\xcb\0\0\0\0\0\0\0\0".to_vec(),
        )
        .unwrap();
        writer.submit(chunk).unwrap();
        writer
            .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
            .unwrap();
        let data = std::fs::read(&path).unwrap();
        assert_eq!(data.windows(frame.len()).filter(|w| *w == frame).count(), 1);
        assert_eq!(&data[..8], HEADER_MAGIC);
        assert_eq!(&data[data.len() - 32..data.len() - 24], FOOTER_MAGIC);
        assert_eq!(
            u64::from_le_bytes(data[data.len() - 16..data.len() - 8].try_into().unwrap()) as usize,
            data.len()
        );
        remove_file(path).unwrap();
    }

    #[test]
    fn value_is_published_once_before_its_first_referencing_chunk() {
        let path = temp_path("value-before-reference");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        let value: Arc<[u8]> = Arc::from(&b"\xa1x"[..]);
        capture.publish_value(0, Arc::clone(&value)).unwrap();
        capture.publish_value(0, Arc::clone(&value)).unwrap();

        let mut store = FrameStore::with_target(Arc::clone(&capture), 3, 1);
        let reference_frame = b"\x81\xa1v\xd6\x09\0\0\0\0";
        store
            .append_encoded::<io::Error, _>(|out, _capture| {
                out.extend_from_slice(reference_frame);
                Ok(())
            })
            .unwrap();
        let layout = store.layout().unwrap();
        capture
            .finish(Vec::new(), b"\x80".to_vec(), vec![layout])
            .unwrap();

        let data = std::fs::read(&path).unwrap();
        assert_eq!(data[10], 2);
        let payload_len = u32::from_le_bytes(data[16..20].try_into().unwrap()) as usize;
        let mut offset = HEADER_LEN as usize + payload_len;
        let mut kinds = Vec::new();
        while offset + RECORD_HEADER_LEN as usize <= data.len() - FOOTER_LEN as usize {
            assert_eq!(&data[offset..offset + 4], RECORD_MAGIC);
            kinds.push(data[offset + 4]);
            let stored_len =
                u32::from_le_bytes(data[offset + 28..offset + 32].try_into().unwrap()) as usize;
            offset += RECORD_HEADER_LEN as usize + stored_len;
        }
        assert_eq!(kinds, vec![5, 1, 3, 4]);
        assert_eq!(
            data.windows(value.len())
                .filter(|window| *window == &*value)
                .count(),
            1
        );
        remove_file(path).unwrap();
    }

    #[test]
    fn abandoned_writer_does_not_publish_destination() {
        let path = temp_path("abandon");
        let writer = TraceWriter::start(path.clone(), b"\x80".to_vec()).unwrap();
        drop(writer);
        assert!(!path.exists());
    }

    #[test]
    fn temporary_paths_are_unique_for_the_same_trace() {
        let path = temp_path("same-trace");
        let first = TraceWriter::start(path.clone(), b"\x80".to_vec()).unwrap();
        let second = TraceWriter::start(path.clone(), b"\x80".to_vec()).unwrap();

        assert_ne!(first.temporary, second.temporary);
        drop(first);
        drop(second);
        assert!(!path.exists());
    }

    #[test]
    fn finishing_twice_atomically_replaces_an_existing_trace() {
        let path = temp_path("replace-existing");
        let mut handles = Vec::new();
        for frame in [b"first-version-with-tail".as_slice(), b"second-version"] {
            let mut arena = FrameArena::with_target(1, 1);
            let chunk = arena
                .append_frame::<(), _>(|out| {
                    out.extend_from_slice(frame);
                    Ok(())
                })
                .unwrap()
                .unwrap();
            let writer = TraceWriter::start(path.clone(), b"\x80".to_vec()).unwrap();
            let handle = writer.submit(chunk).unwrap();
            writer
                .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
                .unwrap();
            handles.push(handle);
        }

        for (handle, expected) in handles.iter().zip([
            b"first-version-with-tail".as_slice(),
            b"second-version".as_slice(),
        ]) {
            let mut snapshot = Vec::new();
            handle.read_frame(0, &mut snapshot).unwrap();
            assert_eq!(snapshot, expected);
        }

        let data = std::fs::read(&path).unwrap();
        assert_eq!(
            data.windows(b"second-version".len())
                .filter(|window| *window == b"second-version")
                .count(),
            1
        );
        assert!(!data
            .windows(b"first-version-with-tail".len())
            .any(|window| window == b"first-version-with-tail"));
        remove_file(path).unwrap();
    }

    #[test]
    fn failed_submit_releases_its_resident_reservation() {
        let _budget_test = RESIDENT_BUDGET_TEST_LOCK
            .lock()
            .expect("resident budget test lock poisoned");
        let before = writer_runtime()
            .resident
            .lock()
            .expect("resident budget poisoned")
            .bytes;
        let (sender, receiver) = std::sync::mpsc::channel();
        drop(receiver);
        let destination = temp_path("failed-submit");
        let temporary = Arc::new(TraceWriter::temporary_path(&destination));
        let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
        let progress = Arc::new(WriterProgress::default());
        progress.mark_finished();
        let writer = TraceWriter {
            sender: Some(sender),
            join: Some(thread::spawn(|| {
                Err(io::Error::new(
                    io::ErrorKind::BrokenPipe,
                    "injected writer failure",
                ))
            })),
            destination,
            temporary,
            snapshot,
            runtime: Arc::clone(writer_runtime()),
            progress,
            preserve_temporary: Arc::new(AtomicBool::new(false)),
            recovery_path: None,
            process_id: std::process::id(),
        };
        let mut arena = FrameArena::with_target(1, 1);
        let chunk = arena
            .append_frame::<(), _>(|out| {
                out.push(1);
                Ok(())
            })
            .unwrap()
            .unwrap();

        assert!(writer.submit(chunk).is_err());
        assert_eq!(
            writer_runtime()
                .resident
                .lock()
                .expect("resident budget poisoned")
                .bytes,
            before
        );
    }

    #[test]
    fn resident_budget_blocks_until_queued_bytes_are_released() {
        let _budget_test = RESIDENT_BUDGET_TEST_LOCK
            .lock()
            .expect("resident budget test lock poisoned");
        let held = ResidentReservation::new(RESIDENT_LIMIT).unwrap();
        let (started_tx, started_rx) = std::sync::mpsc::channel();
        let (acquired_tx, acquired_rx) = std::sync::mpsc::channel();
        let waiter = thread::spawn(move || {
            started_tx.send(()).unwrap();
            let reservation = ResidentReservation::new(1).unwrap();
            acquired_tx.send(()).unwrap();
            drop(reservation);
        });

        started_rx.recv().unwrap();
        assert!(acquired_rx
            .recv_timeout(std::time::Duration::from_millis(50))
            .is_err());
        drop(held);
        acquired_rx
            .recv_timeout(std::time::Duration::from_secs(5))
            .expect("the blocked producer resumes after resident bytes drain");
        waiter.join().unwrap();
    }

    #[test]
    fn writer_progress_resets_the_saturation_deadline() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(80), false));
        let chunk_bytes = 1024 * 1024;
        let mut held = (0..15)
            .map(|_| ResidentReservation::with_runtime(&runtime, chunk_bytes).unwrap())
            .collect::<Vec<_>>();
        let (started_tx, started_rx) = std::sync::mpsc::channel();
        let (finished_tx, finished_rx) = std::sync::mpsc::channel();
        let waiter_runtime = Arc::clone(&runtime);
        let started_at = Instant::now();
        let waiter = thread::spawn(move || {
            started_tx.send(()).unwrap();
            finished_tx
                .send(ResidentReservation::with_runtime(
                    &waiter_runtime,
                    4 * 1024 * 1024,
                ))
                .unwrap();
        });

        started_rx.recv().unwrap();
        for _ in 0..4 {
            thread::sleep(Duration::from_millis(35));
            held.pop()
                .expect("one simulated writer command remains")
                .complete_writer_command();
        }
        let acquired = finished_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("steady writer progress keeps the circuit closed")
            .expect("the waiter acquires once enough bytes drain");
        assert!(started_at.elapsed() > runtime.stall_timeout);
        assert!(!runtime.is_open());
        drop(acquired);
        drop(held);
        waiter.join().unwrap();
    }

    #[test]
    fn elapsed_time_without_saturation_does_not_open_the_circuit() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(20), false));
        let reservation = ResidentReservation::with_runtime(&runtime, 1).unwrap();
        thread::sleep(Duration::from_millis(50));
        assert!(!runtime.is_open());
        drop(reservation);
    }

    #[test]
    fn wakeups_without_progress_do_not_extend_the_saturation_deadline() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(80), false));
        let held = ResidentReservation::with_runtime(&runtime, RESIDENT_LIMIT).unwrap();
        let notifier_runtime = Arc::clone(&runtime);
        let notifier = thread::spawn(move || {
            for _ in 0..12 {
                thread::sleep(Duration::from_millis(10));
                notifier_runtime.changed.notify_all();
            }
        });
        let started_at = Instant::now();
        let error = match ResidentReservation::with_runtime(&runtime, 1) {
            Err(error) => error,
            Ok(_) => panic!("spurious wakeups are not writer progress"),
        };
        assert_eq!(error.kind(), io::ErrorKind::TimedOut);
        assert!(runtime.is_open());
        assert!(started_at.elapsed() >= runtime.stall_timeout);
        assert!(started_at.elapsed() < Duration::from_millis(200));
        notifier.join().unwrap();
        drop(held);
    }

    fn test_chunk(sequence: u64, byte: u8, bytes: usize) -> SealedChunk {
        SealedChunk {
            thread_token: 1,
            sequence,
            bytes: Arc::new(vec![byte; bytes]),
            frame_ends: Arc::from([bytes as u64]),
        }
    }

    #[test]
    fn stalled_writer_opens_circuit_unblocks_producers_and_preserves_prefix() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(80), false));
        let latent_capture = TraceCapture::start_with_runtime(
            temp_path("writer-circuit-latent"),
            b"\x80".to_vec(),
            Arc::clone(&runtime),
        );
        let path = temp_path("writer-circuit-known-good");
        std::fs::write(&path, b"known-good-destination").unwrap();
        let capture = TraceCapture::start_with_runtime(
            path.clone(),
            encode_header_payload("writer-circuit", 1.0),
            Arc::clone(&runtime),
        );

        let prefix_frame = b"\x81\xa4type\xa5frame";
        capture
            .submit(SealedChunk {
                thread_token: 1,
                sequence: 0,
                bytes: Arc::new(prefix_frame.to_vec()),
                frame_ends: Arc::from([prefix_frame.len() as u64]),
            })
            .unwrap();
        let (entered_tx, entered_rx) = std::sync::mpsc::channel();
        let stall = Arc::new(TestWriterStall {
            entered: entered_tx,
            released: Mutex::new(false),
            changed: Condvar::new(),
        });
        let writer_progress = {
            let state = capture.state.lock().expect("capture state poisoned");
            let writer = state
                .writer
                .as_ref()
                .expect("the prefix started the writer");
            writer
                .sender
                .as_ref()
                .expect("writer sender open")
                .send(Command::StallForTest(Arc::clone(&stall)))
                .unwrap();
            Arc::clone(&writer.progress)
        };
        entered_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("writer reached the injected stall after flushing the prefix");

        let chunk_bytes = 512 * 1024;
        let mut sequence = 1;
        loop {
            let resident = runtime
                .resident
                .lock()
                .expect("resident budget poisoned")
                .bytes;
            if resident
                .saturating_add(chunk_bytes)
                .saturating_add(COMMAND_RESIDENT_OVERHEAD)
                > RESIDENT_LIMIT
            {
                break;
            }
            capture
                .submit(test_chunk(sequence, b'Q', chunk_bytes))
                .unwrap();
            sequence += 1;
        }

        let started_at = Instant::now();
        let producers = (0..8)
            .map(|producer| {
                let capture = Arc::clone(&capture);
                thread::spawn(move || {
                    capture.submit(test_chunk(sequence + producer, b'R', chunk_bytes))
                })
            })
            .collect::<Vec<_>>();
        for producer in producers {
            let error = producer
                .join()
                .expect("concurrent producer did not panic")
                .expect_err("every producer is refused after the circuit opens");
            assert_eq!(error.kind(), io::ErrorKind::TimedOut);
        }
        assert!(runtime.is_open());
        assert_eq!(
            latent_capture
                .publish_value(0, Arc::from(&b"value"[..]))
                .unwrap_err()
                .kind(),
            io::ErrorKind::TimedOut
        );
        assert!(started_at.elapsed() >= runtime.stall_timeout);
        assert!(started_at.elapsed() < Duration::from_secs(2));
        assert!(
            runtime
                .resident
                .lock()
                .expect("resident budget poisoned")
                .bytes
                <= RESIDENT_LIMIT,
            "queued ownership remains within the resident limit"
        );

        let recovery = capture
            .recovery_path()
            .expect("a verified prefix is made discoverable");
        assert_eq!(
            recovery.extension().and_then(|value| value.to_str()),
            Some("tmp")
        );
        assert_eq!(std::fs::read(&path).unwrap(), b"known-good-destination");
        let recovered = std::fs::read(&recovery).unwrap();
        let verified_len = usize::try_from(writer_progress.verified_len()).unwrap();
        assert!(verified_len <= recovered.len());
        assert_eq!(&recovered[..HEADER_MAGIC.len()], HEADER_MAGIC);
        assert!(recovered
            .windows(prefix_frame.len())
            .any(|window| window == prefix_frame));
        assert!(
            recovered.len() < FOOTER_LEN as usize
                || &recovered[recovered.len() - FOOTER_LEN as usize
                    ..recovered.len() - FOOTER_LEN as usize + FOOTER_MAGIC.len()]
                    != FOOTER_MAGIC
        );

        let later = TraceCapture::start_with_runtime(
            temp_path("writer-circuit-later"),
            b"\x80".to_vec(),
            Arc::clone(&runtime),
        );
        assert_eq!(
            later
                .publish_value(0, Arc::from(&b"value"[..]))
                .unwrap_err()
                .kind(),
            io::ErrorKind::BrokenPipe
        );
        assert_eq!(
            later.submit(test_chunk(0, 1, 1)).unwrap_err().kind(),
            io::ErrorKind::TimedOut
        );

        let finish_started = Instant::now();
        assert_eq!(
            capture
                .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
                .unwrap_err()
                .kind(),
            io::ErrorKind::TimedOut
        );
        assert!(finish_started.elapsed() < Duration::from_millis(100));

        let drop_started = Instant::now();
        drop(capture);
        assert!(drop_started.elapsed() < Duration::from_millis(100));
        stall.release();
        let cleanup_deadline = Instant::now() + Duration::from_secs(2);
        while !writer_progress.is_finished() && Instant::now() < cleanup_deadline {
            thread::sleep(Duration::from_millis(10));
        }
        assert!(writer_progress.is_finished());
        assert!(
            recovery.exists(),
            "the recovered artifact survives a later writer unblock"
        );
        let after_unblock = std::fs::read(&recovery).unwrap();
        assert_eq!(
            &after_unblock[..verified_len],
            &recovered[..verified_len],
            "the detached writer may append but never mutates the verified prefix"
        );
        assert_eq!(
            runtime
                .resident
                .lock()
                .expect("resident budget poisoned")
                .bytes,
            0
        );
        let _ = remove_file(recovery);
        remove_file(path).unwrap();
    }

    #[test]
    fn tiny_commands_are_bounded_by_bytes_instead_of_channel_count() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_secs(2), false));
        let destination = temp_path("writer-tiny-command-queue");
        let temporary = Arc::new(TraceWriter::temporary_path(&destination));
        let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
        let writer = Arc::new(
            TraceWriter::start_at(
                destination.clone(),
                temporary,
                snapshot,
                b"\x80".to_vec(),
                Arc::clone(&runtime),
            )
            .unwrap(),
        );
        let (entered_tx, entered_rx) = std::sync::mpsc::channel();
        let stall = Arc::new(TestWriterStall {
            entered: entered_tx,
            released: Mutex::new(false),
            changed: Condvar::new(),
        });
        writer
            .sender
            .as_ref()
            .expect("writer sender open")
            .send(Command::StallForTest(Arc::clone(&stall)))
            .unwrap();
        entered_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("writer reached the injected stall");

        let producer_writer = Arc::clone(&writer);
        let (submitted_tx, submitted_rx) = std::sync::mpsc::channel();
        let producer = thread::spawn(move || {
            for sequence in 0..1024 {
                producer_writer
                    .submit(test_chunk(sequence, b'Q', 1))
                    .unwrap();
            }
            submitted_tx.send(()).unwrap();
        });
        submitted_rx
            .recv_timeout(Duration::from_secs(1))
            .expect("more than 64 tiny commands enqueue without a count-bound stall");
        producer.join().unwrap();
        assert!(!runtime.is_open());
        assert!(
            runtime
                .resident
                .lock()
                .expect("resident budget poisoned")
                .bytes
                < RESIDENT_LIMIT
        );

        stall.release();
        Arc::try_unwrap(writer)
            .unwrap_or_else(|_| panic!("all writer references were released"))
            .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
            .unwrap();
        remove_file(destination).unwrap();
    }

    #[test]
    fn an_already_open_circuit_detaches_writer_finish_and_drop() {
        fn started_writer(name: &str) -> (TraceWriter, Arc<WriterRuntime>, Arc<WriterProgress>) {
            let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(80), false));
            let destination = temp_path(name);
            let temporary = Arc::new(TraceWriter::temporary_path(&destination));
            let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
            let writer = TraceWriter::start_at(
                destination,
                temporary,
                snapshot,
                b"\x80".to_vec(),
                Arc::clone(&runtime),
            )
            .unwrap();
            let progress = Arc::clone(&writer.progress);
            let deadline = Instant::now() + Duration::from_secs(2);
            while progress.verified_len() == 0 && Instant::now() < deadline {
                thread::yield_now();
            }
            assert_ne!(progress.verified_len(), 0, "writer flushed its header");
            (writer, runtime, progress)
        }

        let (writer, runtime, progress) = started_writer("open-circuit-finish");
        let temporary = Arc::clone(&writer.temporary);
        runtime.open_circuit();
        assert_eq!(
            writer
                .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
                .unwrap_err()
                .kind(),
            io::ErrorKind::TimedOut
        );
        let deadline = Instant::now() + Duration::from_secs(2);
        while !progress.is_finished() && Instant::now() < deadline {
            thread::yield_now();
        }
        assert!(progress.is_finished());
        assert!(temporary.exists(), "finish preserves the recovered prefix");
        remove_file(temporary.as_ref()).unwrap();

        let (writer, runtime, progress) = started_writer("open-circuit-drop");
        let temporary = Arc::clone(&writer.temporary);
        runtime.open_circuit();
        let started = Instant::now();
        drop(writer);
        assert!(started.elapsed() < Duration::from_millis(100));
        let deadline = Instant::now() + Duration::from_secs(2);
        while !progress.is_finished() && Instant::now() < deadline {
            thread::yield_now();
        }
        assert!(progress.is_finished());
        assert!(temporary.exists(), "drop preserves the recovered prefix");
        remove_file(temporary.as_ref()).unwrap();
    }

    #[test]
    fn value_publication_waits_for_budget_without_holding_capture_state() {
        let _budget_test = RESIDENT_BUDGET_TEST_LOCK
            .lock()
            .expect("resident budget test lock poisoned");
        let held = ResidentReservation::new(RESIDENT_LIMIT).unwrap();
        let capture = TraceCapture::start(temp_path("value-budget-order"), b"\x80".to_vec());
        let (started_tx, started_rx) = std::sync::mpsc::channel();
        let (published_tx, published_rx) = std::sync::mpsc::channel();
        let publisher_capture = Arc::clone(&capture);
        let publisher = thread::spawn(move || {
            started_tx.send(()).unwrap();
            let result = publisher_capture.publish_value(0, Arc::from(&b"value"[..]));
            published_tx.send(result).unwrap();
        });

        started_rx.recv().unwrap();
        thread::sleep(std::time::Duration::from_millis(50));
        let (probe_tx, probe_rx) = std::sync::mpsc::channel();
        let probe_capture = Arc::clone(&capture);
        let probe = thread::spawn(move || {
            probe_tx.send(probe_capture.published_value_ids()).unwrap();
        });
        let state_was_available = probe_rx
            .recv_timeout(std::time::Duration::from_secs(1))
            .is_ok();

        drop(held);
        assert!(published_rx
            .recv_timeout(std::time::Duration::from_secs(5))
            .expect("publisher resumes after resident bytes drain")
            .is_ok());
        publisher.join().unwrap();
        probe.join().unwrap();
        assert!(
            state_was_available,
            "value publication held capture state while waiting for resident room"
        );
    }

    #[test]
    fn background_writer_failure_never_publishes_a_partial_trace() {
        let path = temp_path("background-failure");
        let mut arena = FrameArena::with_target(1, 1);
        let chunk = arena
            .append_frame::<(), _>(|out| {
                out.extend_from_slice(b"partial-frame");
                Ok(())
            })
            .unwrap()
            .unwrap();
        let writer = TraceWriter::start(path.clone(), b"\x80".to_vec()).unwrap();
        let temporary = Arc::clone(&writer.temporary);
        writer.submit(chunk).unwrap();
        writer
            .sender
            .as_ref()
            .unwrap()
            .send(Command::FailForTest)
            .unwrap();

        let error = writer
            .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
            .expect_err("an asynchronous writer failure reaches finalization");
        assert!(matches!(
            error.kind(),
            io::ErrorKind::Other | io::ErrorKind::BrokenPipe
        ));
        assert!(!path.exists(), "an incomplete trace is never published");
        assert!(!temporary.exists(), "the partial temporary file is removed");
        assert!(
            !writer_runtime().is_open(),
            "ordinary I/O errors do not poison future captures"
        );
    }

    #[test]
    fn writer_panic_cannot_strand_drop_waiting_for_completion() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(80), false));
        let destination = temp_path("writer-panic-drop");
        let temporary = Arc::new(TraceWriter::temporary_path(&destination));
        let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
        let writer = TraceWriter::start_at(
            destination,
            Arc::clone(&temporary),
            snapshot,
            b"\x80".to_vec(),
            runtime,
        )
        .unwrap();
        let (entered_tx, entered_rx) = std::sync::mpsc::channel();
        writer
            .sender
            .as_ref()
            .expect("writer sender open")
            .send(Command::PanicForTest(entered_tx))
            .unwrap();
        entered_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("writer reached the injected panic");

        let (dropped_tx, dropped_rx) = std::sync::mpsc::channel();
        let dropper = thread::spawn(move || {
            drop(writer);
            let _ = dropped_tx.send(());
        });
        dropped_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("writer panic must still wake Drop");
        dropper.join().unwrap();
        let _ = remove_file(temporary.as_ref());
    }

    #[test]
    fn writer_panic_during_finish_removes_the_partial_temporary() {
        let runtime = Arc::new(WriterRuntime::new(Duration::from_millis(80), false));
        let destination = temp_path("writer-panic-finish");
        let temporary = Arc::new(TraceWriter::temporary_path(&destination));
        let snapshot = Arc::new(SnapshotFile::new(Arc::clone(&temporary)));
        std::fs::write(temporary.as_ref(), b"partial").unwrap();
        let (sender, receiver) = std::sync::mpsc::channel();
        let progress = Arc::new(WriterProgress::default());
        progress.mark_finished();
        let writer = TraceWriter {
            sender: Some(sender),
            join: Some(thread::spawn(|| -> io::Result<()> {
                panic!("injected writer panic");
            })),
            destination,
            temporary: Arc::clone(&temporary),
            snapshot,
            runtime,
            progress,
            preserve_temporary: Arc::new(AtomicBool::new(false)),
            recovery_path: None,
            process_id: std::process::id(),
        };

        let error = writer
            .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
            .expect_err("writer panic reaches finish");
        drop(receiver);

        assert_eq!(error.kind(), io::ErrorKind::Other);
        assert!(
            !temporary.exists(),
            "panic cleanup removes the partial file"
        );
    }

    #[test]
    fn frame_store_reads_sealed_frames_before_finalization() {
        let path = temp_path("frame-store-read");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        let mut store = FrameStore::with_target(Arc::clone(&capture), 11, 4);

        let first = store
            .append_encoded::<io::Error, _>(|out, _capture| {
                out.extend_from_slice(b"one");
                Ok(())
            })
            .unwrap();
        let second = store
            .append_encoded::<io::Error, _>(|out, _capture| {
                out.extend_from_slice(b"two");
                Ok(())
            })
            .unwrap();
        assert_eq!(first.start_index..first.end_index, 0..1);
        assert_eq!(second.start_index..second.end_index, 1..2);
        assert_eq!(store.total_bytes(), 6);
        store.seal().unwrap();
        assert!(capture.is_streaming());
        assert!(!path.exists());

        let mut scratch = Vec::new();
        assert_eq!(store.frame(0, &mut scratch).unwrap(), b"one");
        assert_eq!(store.frame(1, &mut scratch).unwrap(), b"two");
        let layout = store.layout().unwrap();
        assert_eq!(
            layout,
            ThreadLayout {
                thread_token: 11,
                spans: vec![LayoutSpan {
                    sequence: 0,
                    first_frame: 0,
                    frame_count: 2,
                }],
            }
        );

        capture
            .finish(Vec::new(), b"\x80".to_vec(), vec![layout])
            .unwrap();
        assert!(path.exists());
        remove_file(path).unwrap();
    }

    #[test]
    fn copying_an_open_range_does_not_seal_or_start_the_writer() {
        let path = temp_path("frame-store-open-copy");
        let capture = TraceCapture::start(path, b"\x80".to_vec());
        let mut store = FrameStore::with_target(Arc::clone(&capture), 13, 64);
        for frame in [b"one".as_slice(), b"two", b"three"] {
            store
                .append_encoded::<io::Error, _>(|out, _capture| {
                    out.extend_from_slice(frame);
                    Ok(())
                })
                .unwrap();
        }

        assert_eq!(
            store.copy_range(1..3).unwrap(),
            [b"two".to_vec(), b"three".to_vec()]
        );
        assert_eq!(store.sealed_frames, 0);
        assert!(store.spans.is_empty());
        assert_eq!(store.arena.as_ref().unwrap().frame_count(), 3);
        assert!(!capture.is_streaming());
    }

    #[test]
    fn frame_store_ranges_preserve_logical_order_without_rewriting() {
        let path = temp_path("frame-store-ranges");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        let mut store = FrameStore::with_target(Arc::clone(&capture), 17, 64);
        for frame in [b"a".as_slice(), b"b", b"c"] {
            store
                .append_encoded::<io::Error, _>(|out, _capture| {
                    out.extend_from_slice(frame);
                    Ok(())
                })
                .unwrap();
        }
        store.seal().unwrap();
        assert_eq!(store.spans.len(), 1, "one span, not one handle per frame");

        let middle = store.drain(1..3).unwrap();
        assert_eq!(store.len(), 1);
        assert_eq!(middle.len(), 2);
        store.insert_store(1, middle).unwrap();
        store.insert_frame(1, b"x".to_vec()).unwrap();
        assert_eq!(
            store.spans.len(),
            3,
            "only logical discontinuities add spans"
        );

        let mut scratch = Vec::new();
        let mut logical = Vec::new();
        for index in 0..store.len() {
            logical.push(store.frame(index, &mut scratch).unwrap().to_vec());
        }
        assert_eq!(logical, [b"a", b"x", b"b", b"c"]);

        let layout = store.layout().unwrap();
        assert_eq!(
            layout,
            ThreadLayout {
                thread_token: 17,
                spans: vec![
                    LayoutSpan {
                        sequence: 0,
                        first_frame: 0,
                        frame_count: 1,
                    },
                    LayoutSpan {
                        sequence: 1,
                        first_frame: 0,
                        frame_count: 1,
                    },
                    LayoutSpan {
                        sequence: 0,
                        first_frame: 1,
                        frame_count: 2,
                    },
                ],
            }
        );

        capture
            .finish(Vec::new(), b"\x80".to_vec(), vec![layout])
            .unwrap();
        remove_file(path).unwrap();
    }

    #[test]
    fn frame_store_trace_name_observations_follow_range_edits() {
        fn pack(entries: Vec<(&str, rmpv::Value)>) -> SerializedFrame {
            let value = rmpv::Value::Map(
                entries
                    .into_iter()
                    .map(|(key, value)| (rmpv::Value::String(key.into()), value))
                    .collect(),
            );
            let mut frame = Vec::new();
            rmpv::encode::write_value(&mut frame, &value).unwrap();
            frame
        }

        let path = temp_path("frame-store-trace-name-observations");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        let mut store = FrameStore::with_target(Arc::clone(&capture), 19, 64);
        let mut frames = vec![
            pack(vec![
                ("type", rmpv::Value::String("django_request".into())),
                ("method", rmpv::Value::String("POST".into())),
                ("path_info", rmpv::Value::String("/vote".into())),
            ]),
            pack(vec![("type", rmpv::Value::String("frame".into()))]),
            pack(vec![
                ("type", rmpv::Value::String("django_response".into())),
                ("status_code", rmpv::Value::Integer(201.into())),
            ]),
        ];
        store
            .append_many_with_frame_types(
                &mut frames,
                &[
                    "django_request".into(),
                    "frame".into(),
                    "django_response".into(),
                ],
            )
            .unwrap();

        let request_range = store.drain(0..2).unwrap();
        assert_eq!(
            request_range.trace_name_observations().unwrap()[0].frame_index,
            0
        );
        assert_eq!(store.trace_name_observations().unwrap()[0].frame_index, 0);
        store.insert_store(0, request_range).unwrap();
        assert_eq!(
            store
                .trace_name_observations()
                .unwrap()
                .iter()
                .map(|observation| observation.frame_index)
                .collect::<Vec<_>>(),
            [0, 2]
        );
        let mut trace_name = None;
        assert_eq!(
            super::super::utils::resolve_full_trace_name(
                &mut trace_name,
                store.trace_name_observations().unwrap(),
                store.len(),
            )
            .as_deref(),
            Some("201 POST /vote")
        );

        store
            .insert_frame(0, pack(vec![("type", rmpv::Value::String("frame".into()))]))
            .unwrap();
        assert_eq!(
            store.trace_name_observations(),
            None,
            "explicit logical edits conservatively restore positional resolution"
        );

        capture
            .finish(Vec::new(), b"\x80".to_vec(), vec![store.layout().unwrap()])
            .unwrap();
        remove_file(path).unwrap();
    }

    #[test]
    fn saturated_trace_name_index_falls_back_to_exact_frame_resolution() {
        fn pack(entries: Vec<(&str, rmpv::Value)>) -> SerializedFrame {
            let value = rmpv::Value::Map(
                entries
                    .into_iter()
                    .map(|(key, value)| (rmpv::Value::String(key.into()), value))
                    .collect(),
            );
            let mut frame = Vec::new();
            rmpv::encode::write_value(&mut frame, &value).unwrap();
            frame
        }

        let request = pack(vec![
            ("type", rmpv::Value::String("django_request".into())),
            ("method", rmpv::Value::String("GET".into())),
            ("path_info", rmpv::Value::String("/bounded".into())),
        ]);
        let response = pack(vec![
            ("type", rmpv::Value::String("django_response".into())),
            ("status_code", rmpv::Value::Integer(200.into())),
        ]);
        let mut frames = vec![request; 65];
        frames.push(response);
        let mut frame_types = vec!["django_request".to_string(); 65];
        frame_types.push("django_response".to_string());

        let path = temp_path("frame-store-trace-name-saturated");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        let mut store = FrameStore::with_target(Arc::clone(&capture), 23, 64);
        store
            .append_many_with_frame_types(&mut frames, &frame_types)
            .unwrap();
        assert_eq!(store.trace_name_observations(), None);

        let mut stores = HashMap::new();
        stores.insert("thread".to_string(), store);
        let mut trace_name = None;
        assert_eq!(
            super::super::utils::resolve_trace_name(&mut trace_name, &stores, "thread", true,)
                .as_deref(),
            Some("200 GET /bounded")
        );

        let mut store = stores.remove("thread").unwrap();
        capture
            .finish(Vec::new(), b"\x80".to_vec(), vec![store.layout().unwrap()])
            .unwrap();
        remove_file(path).unwrap();
    }

    #[test]
    fn malformed_relevant_frames_fall_back_to_exact_precedence() {
        fn pack(entries: Vec<(&str, rmpv::Value)>) -> SerializedFrame {
            let value = rmpv::Value::Map(
                entries
                    .into_iter()
                    .map(|(key, value)| (rmpv::Value::String(key.into()), value))
                    .collect(),
            );
            let mut frame = Vec::new();
            rmpv::encode::write_value(&mut frame, &value).unwrap();
            frame
        }

        fn assert_exact_fallback(
            mut frames: Vec<SerializedFrame>,
            frame_types: Vec<String>,
            suffix: &str,
        ) {
            let path = temp_path(&format!("frame-store-trace-name-malformed-{suffix}"));
            let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
            let mut store = FrameStore::with_target(Arc::clone(&capture), 31, 64);
            store
                .append_many_with_frame_types(&mut frames, &frame_types)
                .unwrap();
            assert_eq!(store.trace_name_observations(), None);

            let mut stores = HashMap::new();
            stores.insert("thread".to_string(), store);
            let mut trace_name = None;
            assert_eq!(
                super::super::utils::resolve_trace_name(&mut trace_name, &stores, "thread", true,),
                None,
                "malformed {suffix} must retain the positional resolver's precedence"
            );

            let mut store = stores.remove("thread").unwrap();
            capture
                .finish(Vec::new(), b"\x80".to_vec(), vec![store.layout().unwrap()])
                .unwrap();
            remove_file(path).unwrap();
        }

        assert_exact_fallback(
            vec![
                pack(vec![
                    ("type", rmpv::Value::String("django_request".into())),
                    ("path_info", rmpv::Value::String("/first".into())),
                ]),
                pack(vec![
                    ("type", rmpv::Value::String("django_request".into())),
                    ("method", rmpv::Value::String("GET".into())),
                    ("path_info", rmpv::Value::String("/later".into())),
                ]),
                pack(vec![
                    ("type", rmpv::Value::String("django_response".into())),
                    ("status_code", rmpv::Value::Integer(200.into())),
                ]),
            ],
            vec![
                "django_request".to_string(),
                "django_request".to_string(),
                "django_response".to_string(),
            ],
            "first-request",
        );

        assert_exact_fallback(
            vec![
                pack(vec![
                    ("type", rmpv::Value::String("django_request".into())),
                    ("method", rmpv::Value::String("GET".into())),
                    ("path_info", rmpv::Value::String("/response".into())),
                ]),
                pack(vec![
                    ("type", rmpv::Value::String("django_response".into())),
                    ("status_code", rmpv::Value::Integer(200.into())),
                ]),
                pack(vec![(
                    "type",
                    rmpv::Value::String("django_response".into()),
                )]),
            ],
            vec![
                "django_request".to_string(),
                "django_response".to_string(),
                "django_response".to_string(),
            ],
            "last-response",
        );

        assert_exact_fallback(
            vec![
                pack(vec![("type", rmpv::Value::String("start_test".into()))]),
                pack(vec![
                    ("type", rmpv::Value::String("start_test".into())),
                    ("test_name", rmpv::Value::String("test_later".into())),
                ]),
            ],
            vec!["start_test".to_string(), "start_test".to_string()],
            "first-test",
        );
    }

    #[test]
    fn typed_batch_rejects_frame_type_mismatch_without_mutation() {
        let path = temp_path("frame-store-trace-name-mismatch");
        let capture = TraceCapture::start(path, b"\x80".to_vec());
        let mut store = FrameStore::with_target(capture, 29, 64);
        let mut frames = vec![b"frame".to_vec()];
        assert_eq!(
            store
                .append_many_with_frame_types(&mut frames, &[])
                .unwrap_err()
                .kind(),
            io::ErrorKind::InvalidInput
        );
        assert_eq!(frames, [b"frame"]);
        assert!(store.is_empty());
        assert_eq!(store.trace_name_observations(), Some(&[][..]));
    }

    #[test]
    fn chunk_handles_snapshot_exact_bytes_and_report_invalid_states() {
        let path = temp_path("chunk-handle");
        std::fs::write(&path, b"prefix-frame").unwrap();
        let snapshot = Arc::new(SnapshotFile::new(Arc::new(path.clone())));
        let handle = ChunkHandle::memory(
            Arc::clone(&snapshot),
            23,
            7,
            Arc::from([5_u64]),
            Arc::new(b"frame".to_vec()),
        );
        assert_eq!(handle.frame_count(), 1);
        assert_eq!(handle.thread_token(), 23);
        assert_eq!(handle.sequence(), 7);

        let mut scratch = Vec::new();
        handle.read_frame(0, &mut scratch).unwrap();
        assert_eq!(scratch, b"frame");
        assert_eq!(
            handle.read_frame(1, &mut scratch).unwrap_err().kind(),
            io::ErrorKind::InvalidInput
        );

        handle.commit(7);
        handle.read_frame(0, &mut scratch).unwrap();
        assert_eq!(scratch, b"frame");
        handle.fail(&io::Error::other("writer failed"));
        assert_eq!(
            handle.read_frame(0, &mut scratch).unwrap_err().kind(),
            io::ErrorKind::Other
        );

        let short = ChunkHandle::memory(
            snapshot,
            23,
            8,
            Arc::from([6_u64]),
            Arc::new(b"short".to_vec()),
        );
        assert_eq!(
            short.read_frame(0, &mut scratch).unwrap_err().kind(),
            io::ErrorKind::UnexpectedEof
        );
        let backwards = ChunkHandle::memory(
            Arc::new(SnapshotFile::new(Arc::new(path.clone()))),
            23,
            9,
            Arc::from([2_u64, 1]),
            Arc::new(b"ab".to_vec()),
        );
        assert_eq!(
            backwards.frame_len(1).unwrap_err().kind(),
            io::ErrorKind::InvalidData
        );
        remove_file(path).unwrap();
    }

    #[test]
    fn committed_chunk_reads_bypass_a_writer_held_memory_mutex() {
        let path = temp_path("chunk-handle-committed-offset");
        std::fs::write(&path, b"prefix-frame").unwrap();
        let snapshot = Arc::new(SnapshotFile::new(Arc::new(path.clone())));
        let handle = Arc::new(ChunkHandle::memory(
            snapshot,
            23,
            7,
            Arc::from([5_u64]),
            Arc::new(b"frame".to_vec()),
        ));

        let memory = handle.memory.lock().unwrap();
        let committing = Arc::clone(&handle);
        let commit = std::thread::spawn(move || committing.commit(7));
        let deadline = Instant::now() + Duration::from_secs(1);
        while handle.committed_offset_plus_one.load(Ordering::Acquire) == 0
            && Instant::now() < deadline
        {
            std::thread::yield_now();
        }
        assert_ne!(
            handle.committed_offset_plus_one.load(Ordering::Acquire),
            0,
            "commit did not publish before locking memory"
        );

        let (sender, receiver) = std::sync::mpsc::channel();
        let reading = Arc::clone(&handle);
        let read = std::thread::spawn(move || {
            let mut scratch = Vec::new();
            sender.send(reading.read_frame(0, &mut scratch).map(|()| scratch))
        });
        assert_eq!(
            receiver
                .recv_timeout(Duration::from_secs(1))
                .unwrap()
                .unwrap(),
            b"frame"
        );

        drop(memory);
        commit.join().unwrap();
        read.join().unwrap().unwrap();
        remove_file(path).unwrap();
    }

    #[test]
    fn closed_capture_rejects_late_values_chunks_and_finalization() {
        let path = temp_path("closed-capture");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        capture
            .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
            .unwrap();

        let value_error = capture
            .publish_value(0, Arc::from(&b"value"[..]))
            .unwrap_err();
        assert_eq!(value_error.kind(), io::ErrorKind::BrokenPipe);
        let table_error = capture
            .publish_table(&[(0, Arc::from(&b"value"[..]))])
            .unwrap_err();
        assert_eq!(table_error.kind(), io::ErrorKind::BrokenPipe);

        let mut arena = FrameArena::with_target(3, 1);
        let chunk = arena
            .append_frame::<io::Error, _>(|out| {
                out.push(1);
                Ok(())
            })
            .unwrap()
            .unwrap();
        assert_eq!(
            capture.submit(chunk).unwrap_err().kind(),
            io::ErrorKind::BrokenPipe
        );
        assert_eq!(
            capture
                .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
                .unwrap_err()
                .kind(),
            io::ErrorKind::BrokenPipe
        );
        remove_file(path).unwrap();
    }

    #[test]
    fn failed_chunk_submission_poisons_frame_store_ranges() {
        let path = temp_path("poisoned-frame-store");
        let capture = TraceCapture::start(path.clone(), b"\x80".to_vec());
        capture
            .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
            .unwrap();
        let mut store = FrameStore::with_target(capture, 29, 1);

        assert_eq!(
            store
                .append_serialized(&b"lost".to_vec())
                .unwrap_err()
                .kind(),
            io::ErrorKind::BrokenPipe
        );
        assert_eq!(
            store
                .append_serialized(&b"later".to_vec())
                .unwrap_err()
                .kind(),
            io::ErrorKind::BrokenPipe
        );
        assert_eq!(
            store.copy_range(0..0).unwrap_err().kind(),
            io::ErrorKind::BrokenPipe
        );
        assert_eq!(
            store.layout().unwrap_err().kind(),
            io::ErrorKind::BrokenPipe
        );
        remove_file(path).unwrap();
    }

    #[test]
    fn frame_store_rejects_invalid_ranges_and_cross_capture_insertion() {
        let capture = TraceCapture::start(temp_path("invalid-ranges"), b"\x80".to_vec());
        let mut store = FrameStore::with_target(Arc::clone(&capture), 31, 64);
        assert!(store.is_empty());
        assert_eq!(store.thread_token(), 31);
        let mut frames = vec![b"one".to_vec(), b"two".to_vec()];
        assert_eq!(store.append_many(&mut frames).unwrap().end_index, 2);
        assert!(frames.is_empty());

        for range in [2..1, 0..3] {
            assert_eq!(
                store.copy_range(range).unwrap_err().kind(),
                io::ErrorKind::InvalidInput
            );
        }
        assert_eq!(
            store.drain(2..1).err().unwrap().kind(),
            io::ErrorKind::InvalidInput
        );
        assert_eq!(
            store.insert_frame(3, b"late".to_vec()).unwrap_err().kind(),
            io::ErrorKind::InvalidInput
        );
        let mut scratch = Vec::new();
        assert_eq!(
            store.frame(9, &mut scratch).unwrap_err().kind(),
            io::ErrorKind::InvalidInput
        );

        let other_capture = TraceCapture::start(temp_path("other-capture"), b"\x80".to_vec());
        let mut other = FrameStore::with_target(other_capture, 31, 64);
        other.append_serialized(&b"other".to_vec()).unwrap();
        assert_eq!(
            store.insert_store(0, other).unwrap_err().kind(),
            io::ErrorKind::InvalidInput
        );

        let taken = store.take();
        assert!(store.is_empty());
        assert_eq!(taken.len(), 2);
    }

    #[test]
    fn queued_chunk_failures_are_propagated_to_every_handle() {
        let path = Arc::new(temp_path("queued-failure"));
        let snapshot = Arc::new(SnapshotFile::new(path));
        let handle = Arc::new(ChunkHandle::memory(
            snapshot,
            1,
            0,
            Arc::from([1_u64]),
            Arc::new(vec![1]),
        ));
        let chunk = SealedChunk {
            thread_token: 1,
            sequence: 0,
            bytes: Arc::new(vec![1]),
            frame_ends: Arc::from([1_u64]),
        };
        let (sender, receiver) = std::sync::mpsc::sync_channel(2);
        sender
            .send(Command::Value {
                id: 0,
                encoded: Arc::from(&b"value"[..]),
                reservation: ResidentReservation::new(5).unwrap(),
            })
            .unwrap();
        sender
            .send(Command::Chunk {
                chunk,
                reservation: ResidentReservation::new(1).unwrap(),
                handle: Arc::clone(&handle),
            })
            .unwrap();
        fail_queued_chunks(&receiver, &io::Error::other("queue failed"));

        assert_eq!(
            handle.read_frame(0, &mut Vec::new()).unwrap_err().kind(),
            io::ErrorKind::Other
        );
    }

    #[test]
    fn record_writers_propagate_each_output_stage_failure() {
        let chunk = SealedChunk {
            thread_token: 1,
            sequence: 2,
            bytes: Arc::new(b"frame".to_vec()),
            frame_ends: Arc::from([5_u64]),
        };
        for successful_writes in 0..2 {
            assert!(write_header(&mut FailAfterWrites(successful_writes), b"header").is_err());
            assert!(write_record(
                &mut FailAfterWrites(successful_writes),
                0,
                3,
                0,
                0,
                1,
                b"metadata"
            )
            .is_err());
        }
        for successful_writes in 0..3 {
            assert!(write_chunk(&mut FailAfterWrites(successful_writes), 0, &chunk).is_err());
        }
        assert!(write_footer(&mut FailAfterWrites(0), 0, FOOTER_LEN).is_err());

        let invalid_chunk = SealedChunk {
            thread_token: 1,
            sequence: 3,
            bytes: Arc::new(b"ab".to_vec()),
            frame_ends: Arc::from([2_u64, 1]),
        };
        assert!(write_chunk(&mut Vec::new(), 0, &invalid_chunk).is_err());
    }

    #[test]
    fn materialized_container_requires_a_token_for_every_thread() {
        let frames = HashMap::from([("thread".to_string(), vec![b"frame".to_vec()])]);
        let error = build_container_bytes(
            "trc_missing_token",
            1.0,
            &frames,
            &HashMap::new(),
            Vec::new(),
            b"\x80".to_vec(),
            Vec::new(),
        )
        .unwrap_err();
        assert_eq!(error.kind(), io::ErrorKind::InvalidInput);
        assert!(error.to_string().contains("missing v3 thread token"));
    }
}

//! Port of `software.amazon.kinesis.checkpoint.ShardRecordProcessorCheckpointer`.

use std::sync::{Arc, Mutex, Weak};

use aws_sdk_kinesis::types::Record;

use crate::checkpoint::does_nothing_prepared_checkpointer::DoesNothingPreparedCheckpointer;
use crate::checkpoint::shard_prepared_checkpointer::ShardPreparedCheckpointer;
use crate::exceptions::KinesisClientLibError;
use crate::leases::ShardInfo;
use crate::processor::{Checkpointer, PreparedCheckpointer, RecordProcessorCheckpointer};
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Enables `ShardRecordProcessor`s to checkpoint their progress. The KCL creates
/// one instance per shard assignment and hands it to the application record
/// processor.
///
/// # State machine
///
/// Tracks three pieces of state (guarded by a single [`Mutex`], matching Java's
/// coarse `synchronized(this)`):
///
/// * `last_checkpoint_value` — the last successfully committed checkpoint
///   (`None` until the first checkpoint).
/// * `largest_permitted_checkpoint_value` — the highest sequence number the
///   processor has been handed (set externally by the shard consumer as records
///   are delivered).
/// * `sequence_number_at_shard_end` — set when the shard has been fully consumed,
///   used to auto-upgrade the final checkpoint to `SHARD_END`.
///
/// Every checkpoint/prepare call validates
/// `lastCheckpointValue <= newValue <= largestPermittedCheckpointValue`
/// (inclusive both ends) plus `subSequenceNumber >= 0`; a violation
/// `panic!`s with the same message Java's `IllegalArgumentException` carries.
///
/// # Construction
///
/// Because [`ShardPreparedCheckpointer`] holds a reference back to its owning
/// checkpointer (so that a prepared checkpoint re-validates against the *current*
/// state at commit time), instances are created via [`new`](Self::new) which
/// returns an `Arc<Self>` and wires the self-reference.
///
/// # Concurrency deviation (documented)
///
/// In the Java source a handful of `prepareCheckpoint(..., byte[])` overloads are
/// **not** marked `synchronized` even though their siblings are — an apparent
/// upstream oversight that opens a narrow race window (they bypass the `this`
/// lock that all other overloads take). This port **closes the gap**: every
/// logical operation acquires the state lock (`with_state`) for its full
/// duration, so all overloads are uniformly serialized. This is faithful to the
/// *intended* single-lock-guards-everything design and is strictly safer.
pub struct ShardRecordProcessorCheckpointer {
    shard_info: ShardInfo,
    checkpointer: Arc<dyn Checkpointer + Send + Sync>,
    state: Mutex<State>,
    /// Weak self-reference handed to prepared checkpointers (avoids a reference
    /// cycle keeping the checkpointer alive forever).
    self_ref: Weak<ShardRecordProcessorCheckpointer>,
}

#[derive(Default)]
struct State {
    /// Set to the last value set via `checkpoint()`.
    last_checkpoint_value: Option<ExtendedSequenceNumber>,
    largest_permitted_checkpoint_value: Option<ExtendedSequenceNumber>,
    sequence_number_at_shard_end: Option<ExtendedSequenceNumber>,
}

impl ShardRecordProcessorCheckpointer {
    /// Create a checkpointer for one shard assignment.
    ///
    /// `checkpointer` is the underlying checkpoint store (Java's `Checkpointer`).
    pub fn new(
        shard_info: ShardInfo,
        checkpointer: Arc<dyn Checkpointer + Send + Sync>,
    ) -> Arc<Self> {
        Arc::new_cyclic(|weak| Self {
            shard_info,
            checkpointer,
            state: Mutex::new(State::default()),
            self_ref: weak.clone(),
        })
    }

    fn with_state<R>(&self, f: impl FnOnce(&mut State) -> R) -> R {
        // Recover from a poisoned lock: the Java code uses `synchronized`, whose
        // monitor is released cleanly when a validation `IllegalArgumentException`
        // is thrown. A Rust `panic!` while holding a `std::sync::Mutex` poisons
        // it, but the state is never mutated on the panic path (validation
        // happens before any mutation), so recovering the guard preserves the
        // exact Java semantics: after a rejected checkpoint the checkpointer is
        // still usable and its state is unchanged.
        let mut guard = self
            .state
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner);
        f(&mut guard)
    }

    /// Package-visible in Java (`setInitialCheckpointValue`).
    pub fn set_initial_checkpoint_value(&self, initial_checkpoint: ExtendedSequenceNumber) {
        self.with_state(|s| s.last_checkpoint_value = Some(initial_checkpoint));
    }

    /// Set the largest permitted checkpoint value (Java setter
    /// `largestPermittedCheckpointValue(ExtendedSequenceNumber)`).
    pub fn set_largest_permitted_checkpoint_value(
        &self,
        largest_permitted_checkpoint_value: ExtendedSequenceNumber,
    ) {
        self.with_state(|s| {
            s.largest_permitted_checkpoint_value = Some(largest_permitted_checkpoint_value)
        });
    }

    /// The largest permitted checkpoint value (Java fluent getter
    /// `largestPermittedCheckpointValue()`).
    pub fn largest_permitted_checkpoint_value(&self) -> Option<ExtendedSequenceNumber> {
        self.with_state(|s| s.largest_permitted_checkpoint_value.clone())
    }

    /// The last successfully committed checkpoint (Java fluent getter
    /// `lastCheckpointValue()`).
    pub fn last_checkpoint_value(&self) -> Option<ExtendedSequenceNumber> {
        self.with_state(|s| s.last_checkpoint_value.clone())
    }

    /// Remember the last extended sequence number before `SHARD_END`, to prevent
    /// the checkpointer from checkpointing at the end of the shard twice (once at
    /// the last sequence number and then again at `SHARD_END`).
    pub fn set_sequence_number_at_shard_end(
        &self,
        extended_sequence_number: ExtendedSequenceNumber,
    ) {
        self.with_state(|s| s.sequence_number_at_shard_end = Some(extended_sequence_number));
    }

    // ---- internal (package-level in Java, exposed here for testing parity) ----

    /// Java `advancePosition(ExtendedSequenceNumber)`. Assumes the state lock is
    /// **not** held; acquires it.
    pub(crate) fn advance_position(
        &self,
        extended_sequence_number: &ExtendedSequenceNumber,
    ) -> Result<(), KinesisClientLibError> {
        self.with_state(|s| self.advance_position_locked(s, extended_sequence_number))
    }

    fn advance_position_locked(
        &self,
        state: &mut State,
        extended_sequence_number: &ExtendedSequenceNumber,
    ) -> Result<(), KinesisClientLibError> {
        let mut checkpoint_to_record = extended_sequence_number.clone();
        if let Some(shard_end) = &state.sequence_number_at_shard_end {
            if shard_end == extended_sequence_number {
                // If we are about to checkpoint the very last sequence number for
                // this shard, we might as well just checkpoint at SHARD_END.
                checkpoint_to_record = ExtendedSequenceNumber::shard_end();
            }
        }

        // Don't checkpoint a value we already successfully checkpointed. Note the
        // skip condition tests the *pre-substitution* value against
        // lastCheckpointValue (matching Java exactly).
        if state.last_checkpoint_value.as_ref() != Some(extended_sequence_number) {
            tracing::debug!(
                "Setting {}, token {:?} checkpoint to {}",
                self.shard_info.lease_key(),
                self.shard_info.concurrency_token(),
                checkpoint_to_record
            );
            let concurrency_token = self.shard_info.concurrency_token().unwrap_or("");
            self.checkpointer
                .set_checkpoint(
                    &self.shard_info.lease_key(),
                    &checkpoint_to_record,
                    concurrency_token,
                )
                .map_err(translate_checkpoint_error)?;
            state.last_checkpoint_value = Some(checkpoint_to_record);
        }
        Ok(())
    }

    /// Java private `doPrepareCheckpoint`. Assumes the state lock is held.
    fn do_prepare_checkpoint(
        &self,
        state: &mut State,
        extended_sequence_number: &ExtendedSequenceNumber,
        application_state: Option<&[u8]>,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        let mut new_prepare_checkpoint = extended_sequence_number.clone();
        if let Some(shard_end) = &state.sequence_number_at_shard_end {
            if shard_end == extended_sequence_number {
                new_prepare_checkpoint = ExtendedSequenceNumber::shard_end();
            }
        }

        // Don't actually prepare a checkpoint if they're trying to checkpoint at
        // the current checkpointed value. NOTE: unlike advance_position, this
        // check is against the *post-substitution* value (matching Java exactly).
        if state.last_checkpoint_value.as_ref() == Some(&new_prepare_checkpoint) {
            return Ok(Box::new(DoesNothingPreparedCheckpointer::new(
                new_prepare_checkpoint,
            )));
        }

        let concurrency_token = self.shard_info.concurrency_token().unwrap_or("");
        let result = match application_state {
            Some(app_state) => self.checkpointer.prepare_checkpoint_with_state(
                &self.shard_info.lease_key(),
                &new_prepare_checkpoint,
                concurrency_token,
                app_state,
            ),
            None => self.checkpointer.prepare_checkpoint(
                &self.shard_info.lease_key(),
                &new_prepare_checkpoint,
                concurrency_token,
            ),
        };
        result.map_err(translate_checkpoint_error)?;

        let self_arc = self
            .self_ref
            .upgrade()
            .expect("ShardRecordProcessorCheckpointer dropped while preparing a checkpoint");
        Ok(Box::new(ShardPreparedCheckpointer::new(
            new_prepare_checkpoint,
            self_arc,
        )))
    }

    /// Shared implementation of the `checkpoint(String, long)` overloads.
    fn checkpoint_seq_sub(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
    ) -> Result<(), KinesisClientLibError> {
        if sub_sequence_number < 0 {
            panic!(
                "Could not checkpoint at invalid, negative subsequence number {}",
                sub_sequence_number
            );
        }

        self.with_state(|state| {
            // If there isn't a last checkpoint value, we only care about checking
            // the upper bound. If there is, we check both bounds.
            let new_checkpoint =
                ExtendedSequenceNumber::new(sequence_number, Some(sub_sequence_number));
            let largest = state
                .largest_permitted_checkpoint_value
                .as_ref()
                .expect("largestPermittedCheckpointValue not set");
            let lower_ok = state
                .last_checkpoint_value
                .as_ref()
                .map(|last| last.compare_to(&new_checkpoint).is_le())
                .unwrap_or(true);
            if lower_ok && new_checkpoint.compare_to(largest).is_le() {
                tracing::debug!(
                    "Checkpointing {}, token {:?} at specific extended sequence number {}",
                    self.shard_info.lease_key(),
                    self.shard_info.concurrency_token(),
                    new_checkpoint
                );
                self.advance_position_locked(state, &new_checkpoint)
            } else {
                panic!(
                    "Could not checkpoint at extended sequence number {} as it did not fall into acceptable range \
                     between the last checkpoint {} and the greatest extended sequence number passed to this \
                     record processor {}",
                    new_checkpoint,
                    display_opt(&state.last_checkpoint_value),
                    display_opt(&state.largest_permitted_checkpoint_value)
                );
            }
        })
    }

    /// Shared implementation of the `prepareCheckpoint(String, long, byte[])`
    /// overloads.
    fn prepare_checkpoint_seq_sub(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
        application_state: Option<&[u8]>,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        if sub_sequence_number < 0 {
            panic!(
                "Could not checkpoint at invalid, negative subsequence number {}",
                sub_sequence_number
            );
        }

        self.with_state(|state| {
            let pending_checkpoint =
                ExtendedSequenceNumber::new(sequence_number, Some(sub_sequence_number));
            let largest = state
                .largest_permitted_checkpoint_value
                .as_ref()
                .expect("largestPermittedCheckpointValue not set");
            let lower_ok = state
                .last_checkpoint_value
                .as_ref()
                .map(|last| last.compare_to(&pending_checkpoint).is_le())
                .unwrap_or(true);
            if lower_ok && pending_checkpoint.compare_to(largest).is_le() {
                tracing::debug!(
                    "Preparing checkpoint {}, token {:?} at specific extended sequence number {}",
                    self.shard_info.lease_key(),
                    self.shard_info.concurrency_token(),
                    pending_checkpoint
                );
                self.do_prepare_checkpoint(state, &pending_checkpoint, application_state)
            } else {
                panic!(
                    "Could not prepare checkpoint at extended sequence number {} as it did not fall into acceptable \
                     range between the last checkpoint {} and the greatest extended sequence number passed \
                     to this record processor {}",
                    pending_checkpoint,
                    display_opt(&state.last_checkpoint_value),
                    display_opt(&state.largest_permitted_checkpoint_value)
                );
            }
        })
    }

    fn largest_sequence_number(&self) -> Option<ExtendedSequenceNumber> {
        self.with_state(|s| s.largest_permitted_checkpoint_value.clone())
    }
}

impl RecordProcessorCheckpointer for ShardRecordProcessorCheckpointer {
    fn checkpoint(&self) -> Result<(), KinesisClientLibError> {
        // Java: `advancePosition(null)` is a silent no-op when no largest
        // permitted checkpoint value has been set yet.
        let Some(largest) = self.largest_sequence_number() else {
            tracing::debug!(
                "Checkpointing {}, token {:?} skipped: no largest permitted value set",
                self.shard_info.lease_key(),
                self.shard_info.concurrency_token(),
            );
            return Ok(());
        };
        tracing::debug!(
            "Checkpointing {}, token {:?} at largest permitted value {}",
            self.shard_info.lease_key(),
            self.shard_info.concurrency_token(),
            largest
        );
        self.advance_position(&largest)
    }

    fn checkpoint_record(&self, record: &Record) -> Result<(), KinesisClientLibError> {
        // TODO(port): UserRecord deprecation — Java handles UserRecord subclass to
        // read a sub-sequence number; the AWS SDK `Record` has none.
        self.checkpoint_seq_sub(record.sequence_number(), 0)
    }

    fn checkpoint_sequence(&self, sequence_number: &str) -> Result<(), KinesisClientLibError> {
        self.checkpoint_seq_sub(sequence_number, 0)
    }

    fn checkpoint_sequence_sub(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
    ) -> Result<(), KinesisClientLibError> {
        self.checkpoint_seq_sub(sequence_number, sub_sequence_number)
    }

    fn prepare_checkpoint(
        &self,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        // Java NPEs here when unset (unlike `checkpoint()`, which no-ops).
        let largest = self
            .largest_sequence_number()
            .expect("largestPermittedCheckpointValue not set");
        self.prepare_checkpoint_seq_sub(
            largest.sequence_number(),
            largest.sub_sequence_number(),
            None,
        )
    }

    fn prepare_checkpoint_state(
        &self,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        // Java NPEs here when unset (unlike `checkpoint()`, which no-ops).
        let largest = self
            .largest_sequence_number()
            .expect("largestPermittedCheckpointValue not set");
        self.prepare_checkpoint_seq_sub(largest.sequence_number(), 0, Some(application_state))
    }

    fn prepare_checkpoint_record(
        &self,
        record: &Record,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_checkpoint_record_impl(record, None)
    }

    fn prepare_checkpoint_record_state(
        &self,
        record: &Record,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_checkpoint_record_impl(record, Some(application_state))
    }

    fn prepare_checkpoint_sequence(
        &self,
        sequence_number: &str,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_checkpoint_seq_sub(sequence_number, 0, None)
    }

    fn prepare_checkpoint_sequence_state(
        &self,
        sequence_number: &str,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_checkpoint_seq_sub(sequence_number, 0, Some(application_state))
    }

    fn prepare_checkpoint_sequence_sub(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_checkpoint_seq_sub(sequence_number, sub_sequence_number, None)
    }

    fn prepare_checkpoint_sequence_sub_state(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_checkpoint_seq_sub(
            sequence_number,
            sub_sequence_number,
            Some(application_state),
        )
    }

    fn checkpointer(&self) -> Box<dyn Checkpointer + Send + Sync> {
        Box::new(CheckpointerHandle(self.checkpointer.clone()))
    }
}

impl ShardRecordProcessorCheckpointer {
    /// Shared body of the `prepareCheckpoint(Record[, byte[]])` overloads.
    fn prepare_checkpoint_record_impl(
        &self,
        record: &Record,
        application_state: Option<&[u8]>,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        // TODO(port): UserRecord deprecation (see checkpoint_record).
        self.prepare_checkpoint_seq_sub(record.sequence_number(), 0, application_state)
    }
}

/// Format an optional [`ExtendedSequenceNumber`] like Java's `String.format`
/// on a `null` field (which prints `null`).
fn display_opt(value: &Option<ExtendedSequenceNumber>) -> String {
    match value {
        Some(v) => v.to_string(),
        None => "null".to_string(),
    }
}

/// Mirror Java's catch blocks in `advancePosition`/`doPrepareCheckpoint`:
/// re-throw `Throttling`/`Shutdown`/`InvalidState`/`Dependency` as-is, and wrap
/// any *other* `KinesisClientLibException` into a
/// `KinesisClientLibDependencyException`.
fn translate_checkpoint_error(err: KinesisClientLibError) -> KinesisClientLibError {
    match err {
        KinesisClientLibError::Throttling { .. }
        | KinesisClientLibError::Shutdown { .. }
        | KinesisClientLibError::InvalidState { .. }
        | KinesisClientLibError::Dependency { .. } => err,
        other => {
            tracing::warn!("Caught exception setting checkpoint. {}", other);
            KinesisClientLibError::dependency_caused_by(
                "Caught exception while checkpointing",
                other,
            )
        }
    }
}

/// A cloneable handle over the shared [`Checkpointer`] returned by
/// [`RecordProcessorCheckpointer::checkpointer`] (Java returns the same instance;
/// a `Box<dyn Checkpointer>` isn't cloneable, so this delegates to the shared
/// `Arc`).
struct CheckpointerHandle(Arc<dyn Checkpointer + Send + Sync>);

impl Checkpointer for CheckpointerHandle {
    fn set_checkpoint(
        &self,
        lease_key: &str,
        checkpoint_value: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError> {
        self.0
            .set_checkpoint(lease_key, checkpoint_value, concurrency_token)
    }

    fn get_checkpoint(
        &self,
        lease_key: &str,
    ) -> Result<Option<ExtendedSequenceNumber>, KinesisClientLibError> {
        self.0.get_checkpoint(lease_key)
    }

    fn get_checkpoint_object(
        &self,
        lease_key: &str,
    ) -> Result<Option<crate::checkpoint::Checkpoint>, KinesisClientLibError> {
        self.0.get_checkpoint_object(lease_key)
    }

    fn prepare_checkpoint(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError> {
        self.0
            .prepare_checkpoint(lease_key, pending_checkpoint, concurrency_token)
    }

    fn prepare_checkpoint_with_state(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
        pending_checkpoint_state: &[u8],
    ) -> Result<(), KinesisClientLibError> {
        self.0.prepare_checkpoint_with_state(
            lease_key,
            pending_checkpoint,
            concurrency_token,
            pending_checkpoint_state,
        )
    }

    fn set_operation(&self, operation: &str) {
        self.0.set_operation(operation)
    }

    fn operation(&self) -> String {
        self.0.operation()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::checkpoint::in_memory_checkpointer::InMemoryCheckpointer;
    use std::panic::{catch_unwind, AssertUnwindSafe};

    const STARTING_SEQUENCE_NUMBER: &str = "13";
    const TEST_CONCURRENCY_TOKEN: &str = "testToken";
    const SHARD_ID: &str = "shardId-123";

    fn esn(sn: &str) -> ExtendedSequenceNumber {
        ExtendedSequenceNumber::from_sequence_number(sn)
    }

    fn starting_esn() -> ExtendedSequenceNumber {
        esn(STARTING_SEQUENCE_NUMBER)
    }

    /// Recreates the JUnit `@Before setup`: a fresh in-memory store seeded with
    /// the starting checkpoint, plus a matching single-stream `ShardInfo`.
    fn setup() -> (Arc<InMemoryCheckpointer>, ShardInfo) {
        let checkpoint = Arc::new(InMemoryCheckpointer::new());
        checkpoint
            .set_checkpoint(SHARD_ID, &starting_esn(), TEST_CONCURRENCY_TOKEN)
            .unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(starting_esn())
        );
        let shard_info = ShardInfo::single_stream(
            SHARD_ID,
            Some(TEST_CONCURRENCY_TOKEN.to_string()),
            Vec::<String>::new(),
            Some(ExtendedSequenceNumber::trim_horizon()),
        );
        (checkpoint, shard_info)
    }

    fn processor(
        checkpoint: &Arc<InMemoryCheckpointer>,
        shard_info: &ShardInfo,
    ) -> Arc<ShardRecordProcessorCheckpointer> {
        ShardRecordProcessorCheckpointer::new(
            shard_info.clone(),
            checkpoint.clone() as Arc<dyn Checkpointer + Send + Sync>,
        )
    }

    fn make_record(seq_num: &str) -> Record {
        Record::builder()
            .sequence_number(seq_num)
            .data(aws_sdk_kinesis::primitives::Blob::new(Vec::new()))
            .partition_key("pk")
            .build()
            .unwrap()
    }

    #[test]
    fn test_checkpoint() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_largest_permitted_checkpoint_value(starting_esn());
        p.checkpoint().unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(starting_esn())
        );

        let sn = esn("5019");
        p.set_largest_permitted_checkpoint_value(sn.clone());
        p.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(sn));
    }

    /// Java: `checkpoint()` before any largest-permitted value is set calls
    /// `advancePosition(null)`, which is a silent no-op.
    #[test]
    fn test_checkpoint_without_largest_permitted_value_is_noop() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.checkpoint().unwrap();
        // The stored checkpoint is untouched (still the seeded starting value).
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(starting_esn())
        );
        assert_eq!(p.last_checkpoint_value(), None);
    }

    #[test]
    fn test_checkpoint_record() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5025");
        let record = make_record("5025");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        p.checkpoint_record(&record).unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_checkpoint_sub_record() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5030");
        let record = make_record("5030");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        p.checkpoint_record(&record).unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_checkpoint_sequence_number() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5035");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        p.checkpoint_sequence("5035").unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_checkpoint_extended_sequence_number() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5040");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        p.checkpoint_sequence_sub("5040", 0).unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_checkpoint_at_shard_end() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = ExtendedSequenceNumber::shard_end();
        p.set_largest_permitted_checkpoint_value(extended.clone());
        p.checkpoint_sequence(ExtendedSequenceNumber::shard_end().sequence_number())
            .unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_prepare_checkpoint() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());

        let sn1 = esn("5001");
        p.set_largest_permitted_checkpoint_value(sn1.clone());
        let prepared = p.prepare_checkpoint().unwrap();
        assert_eq!(prepared.pending_checkpoint(), sn1);
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&sn1)
        );

        let sn2 = esn("5019");
        p.set_largest_permitted_checkpoint_value(sn2.clone());
        let prepared = p.prepare_checkpoint().unwrap();
        assert_eq!(prepared.pending_checkpoint(), sn2);
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&sn2)
        );

        prepared.checkpoint().unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(sn2.clone())
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &sn2
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );
    }

    #[test]
    fn test_prepare_checkpoint_record() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5025");
        let record = make_record("5025");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        let prepared = p.prepare_checkpoint_record(&record).unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(starting_esn())
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &starting_esn()
        );
        assert_eq!(prepared.pending_checkpoint(), extended);
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&extended)
        );

        prepared.checkpoint().unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(extended.clone())
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &extended
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );
    }

    #[test]
    fn test_prepare_checkpoint_sub_record() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5030");
        let record = make_record("5030");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        let prepared = p.prepare_checkpoint_record(&record).unwrap();
        assert_eq!(prepared.pending_checkpoint(), extended);
        prepared.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_prepare_checkpoint_sequence_number() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5035");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        let prepared = p.prepare_checkpoint_sequence("5035").unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(starting_esn())
        );
        assert_eq!(prepared.pending_checkpoint(), extended);
        prepared.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_prepare_checkpoint_extended_sequence_number() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = esn("5040");
        p.set_largest_permitted_checkpoint_value(extended.clone());
        let prepared = p.prepare_checkpoint_sequence_sub("5040", 0).unwrap();
        assert_eq!(prepared.pending_checkpoint(), extended);
        prepared.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_prepare_checkpoint_at_shard_end() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        let extended = ExtendedSequenceNumber::shard_end();
        p.set_largest_permitted_checkpoint_value(extended.clone());
        let prepared = p
            .prepare_checkpoint_sequence(ExtendedSequenceNumber::shard_end().sequence_number())
            .unwrap();
        assert_eq!(prepared.pending_checkpoint(), extended);
        prepared.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(extended));
    }

    #[test]
    fn test_multiple_outstanding_checkpointers_happy_case() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        p.set_largest_permitted_checkpoint_value(esn("6040"));

        let sn1 = esn("6010");
        let first = p.prepare_checkpoint_sequence_sub("6010", 0).unwrap();
        assert_eq!(first.pending_checkpoint(), sn1);

        let sn2 = esn("6020");
        let second = p.prepare_checkpoint_sequence_sub("6020", 0).unwrap();
        assert_eq!(second.pending_checkpoint(), sn2);

        first.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(sn1));

        second.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(sn2));
    }

    #[test]
    fn test_multiple_outstanding_checkpointers_out_of_order() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        p.set_largest_permitted_checkpoint_value(esn("7040"));

        let first = p.prepare_checkpoint_sequence_sub("7010", 0).unwrap();
        let second = p.prepare_checkpoint_sequence_sub("7020", 0).unwrap();

        second.checkpoint().unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(esn("7020"))
        );

        // The first prepared checkpoint is now too low and must panic (Java
        // IllegalArgumentException).
        let result = catch_unwind(AssertUnwindSafe(|| first.checkpoint()));
        assert!(
            result.is_err(),
            "expected checkpoint() to panic because the sequence number was too low"
        );
    }

    #[test]
    fn test_update() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);

        let sn = esn("10");
        p.set_largest_permitted_checkpoint_value(sn.clone());
        assert_eq!(p.largest_permitted_checkpoint_value(), Some(sn));

        let big = esn("90259185948592875928375908214918273491783097");
        p.set_largest_permitted_checkpoint_value(big.clone());
        assert_eq!(p.largest_permitted_checkpoint_value(), Some(big));
    }

    /// The values a client should never be able to checkpoint at, from the
    /// Java test (minus `null`, which has no Rust equivalent).
    fn bad_checkpoint_values() -> Vec<ExtendedSequenceNumber> {
        vec![
            esn("2"),                      // too small — before the first checkpoint
            esn("13"),                     // firstSequenceNumber — can't move back to a used value
            esn("9000"),                   // too big — exceeds largest permitted
            esn("6789"),                   // lastSequenceNumberOfShard — another big value
            esn("bogus-checkpoint-value"), // non-numeric
            ExtendedSequenceNumber::shard_end(),
            ExtendedSequenceNumber::trim_horizon(),
            ExtendedSequenceNumber::latest(),
        ]
    }

    #[test]
    fn test_client_specified_checkpoint() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);

        let first = checkpoint.get_checkpoint(SHARD_ID).unwrap().unwrap(); // 13
        let second = esn("127");
        let third = esn("5019");
        let last_of_shard = esn("6789");

        p.set_initial_checkpoint_value(first.clone());
        p.set_largest_permitted_checkpoint_value(third.clone());

        // Cannot move backward.
        let r = catch_unwind(AssertUnwindSafe(|| p.checkpoint_sequence_sub("2", 0)));
        assert!(r.is_err());

        // Advance to first (twice — idempotent).
        p.checkpoint_sequence_sub(first.sequence_number(), first.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(first.clone())
        );
        p.checkpoint_sequence_sub(first.sequence_number(), first.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(first.clone())
        );

        // Advance to second.
        p.checkpoint_sequence_sub(second.sequence_number(), second.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(second.clone())
        );

        for bad in bad_checkpoint_values() {
            let bad_seq = bad.sequence_number().to_string();
            let bad_sub = bad.sub_sequence_number();
            let pp = p.clone();
            let r = catch_unwind(AssertUnwindSafe(move || {
                pp.checkpoint_sequence_sub(&bad_seq, bad_sub)
            }));
            assert!(
                r.is_err(),
                "checkpointing at bad value {} should have panicked",
                bad
            );
            assert_eq!(
                checkpoint.get_checkpoint(SHARD_ID).unwrap(),
                Some(second.clone())
            );
            assert_eq!(p.last_checkpoint_value(), Some(second.clone()));
            assert_eq!(p.largest_permitted_checkpoint_value(), Some(third.clone()));
        }

        // Advance to third.
        p.checkpoint_sequence_sub(third.sequence_number(), third.sub_sequence_number())
            .unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(third));

        // Prevent checkpointing at SHARD_END twice.
        p.set_largest_permitted_checkpoint_value(last_of_shard.clone());
        p.set_sequence_number_at_shard_end(p.largest_permitted_checkpoint_value().unwrap());
        p.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::shard_end());
        p.checkpoint_sequence_sub(
            last_of_shard.sequence_number(),
            last_of_shard.sub_sequence_number(),
        )
        .unwrap();
        assert_eq!(
            p.last_checkpoint_value(),
            Some(ExtendedSequenceNumber::shard_end())
        );
    }

    #[test]
    fn test_client_specified_two_phase_checkpoint() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);

        let first = checkpoint.get_checkpoint(SHARD_ID).unwrap().unwrap(); // 13
        let second = esn("127");
        let third = esn("5019");
        let last_of_shard = esn("6789");

        p.set_initial_checkpoint_value(first.clone());
        p.set_largest_permitted_checkpoint_value(third.clone());

        // Cannot move backward (prepare or checkpoint).
        let r = catch_unwind(AssertUnwindSafe(|| {
            p.prepare_checkpoint_sequence_sub("2", 0).map(|_| ())
        }));
        assert!(r.is_err());
        let r = catch_unwind(AssertUnwindSafe(|| p.checkpoint_sequence_sub("2", 0)));
        assert!(r.is_err());

        // Advance to first.
        p.checkpoint_sequence_sub(first.sequence_number(), first.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(first.clone())
        );

        // Prepare at the initial checkpoint value → DoesNothingPreparedCheckpointer.
        let does_nothing = p
            .prepare_checkpoint_sequence_sub(first.sequence_number(), first.sub_sequence_number())
            .unwrap();
        assert_eq!(does_nothing.pending_checkpoint(), first);
        // Downcast check: it should be a DoesNothingPreparedCheckpointer, verified
        // behaviorally — it leaves the pending checkpoint unset.
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(first.clone())
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );
        does_nothing.checkpoint().unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(first.clone())
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );

        // A prepare at a genuinely-new value is not a no-op (sanity: assert it
        // is NOT the do-nothing checkpointer by confirming it writes a pending
        // checkpoint below).

        // Advance to second (prepare then checkpoint).
        p.prepare_checkpoint_sequence_sub(second.sequence_number(), second.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&second)
        );
        p.checkpoint_sequence_sub(second.sequence_number(), second.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint.get_checkpoint(SHARD_ID).unwrap(),
            Some(second.clone())
        );
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );

        for bad in bad_checkpoint_values() {
            let bad_seq = bad.sequence_number().to_string();
            let bad_sub = bad.sub_sequence_number();
            let pp = p.clone();
            let r = catch_unwind(AssertUnwindSafe(move || {
                pp.prepare_checkpoint_sequence_sub(&bad_seq, bad_sub)
                    .map(|_| ())
            }));
            assert!(
                r.is_err(),
                "preparing at bad value {} should have panicked",
                bad
            );
            assert_eq!(
                checkpoint.get_checkpoint(SHARD_ID).unwrap(),
                Some(second.clone())
            );
            assert_eq!(p.last_checkpoint_value(), Some(second.clone()));
            assert_eq!(p.largest_permitted_checkpoint_value(), Some(third.clone()));
            assert_eq!(
                checkpoint
                    .get_checkpoint_object(SHARD_ID)
                    .unwrap()
                    .unwrap()
                    .pending_checkpoint(),
                None
            );
        }

        // Advance to third.
        p.prepare_checkpoint_sequence_sub(third.sequence_number(), third.sub_sequence_number())
            .unwrap();
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&third)
        );
        p.checkpoint_sequence_sub(third.sequence_number(), third.sub_sequence_number())
            .unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(third));

        // Prevent (prepared) checkpointing at SHARD_END twice.
        p.set_largest_permitted_checkpoint_value(last_of_shard.clone());
        p.set_sequence_number_at_shard_end(p.largest_permitted_checkpoint_value().unwrap());
        p.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::shard_end());
        p.prepare_checkpoint_sequence_sub(
            last_of_shard.sequence_number(),
            last_of_shard.sub_sequence_number(),
        )
        .unwrap();
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&ExtendedSequenceNumber::shard_end())
        );
    }

    #[derive(Clone, Copy)]
    enum CheckpointAction {
        None,
        NoSequenceNumber,
        WithSequenceNumber,
    }

    #[derive(Clone, Copy)]
    enum CheckpointerType {
        Checkpointer,
        PreparedCheckpointer,
        PrepareThenCheckpointer,
    }

    fn mixed_calls_test_plan() -> Vec<Vec<(String, CheckpointAction)>> {
        use CheckpointAction::*;
        let s = |x: &str| x.to_string();
        vec![
            vec![
                (s("LATEST"), NoSequenceNumber),
                (s("SHARD_END"), NoSequenceNumber),
            ],
            vec![(s("LATEST"), None), (s("SHARD_END"), NoSequenceNumber)],
            vec![
                (s("TRIM_HORIZON"), None),
                (s("1"), None),
                (s("2"), NoSequenceNumber),
                (s("3"), None),
                (s("4"), WithSequenceNumber),
                (s("SHARD_END"), NoSequenceNumber),
            ],
            vec![
                (s("LATEST"), NoSequenceNumber),
                (s("30"), None),
                (s("332"), WithSequenceNumber),
                (s("349"), None),
                (s("4332"), NoSequenceNumber),
                (s("4338"), None),
                (s("5349"), WithSequenceNumber),
                (s("5358"), None),
                (s("64332"), NoSequenceNumber),
                (s("64338"), NoSequenceNumber),
                (s("65358"), WithSequenceNumber),
                (s("764338"), WithSequenceNumber),
                (s("765349"), NoSequenceNumber),
                (s("765358"), None),
                (s("SHARD_END"), NoSequenceNumber),
            ],
        ]
    }

    fn run_mixed_checkpoint_calls(
        checkpoint: &Arc<InMemoryCheckpointer>,
        p: &Arc<ShardRecordProcessorCheckpointer>,
        plan: &[(String, CheckpointAction)],
        checkpointer_type: CheckpointerType,
    ) {
        for (key, action) in plan {
            let last_checkpoint_value = p.last_checkpoint_value();

            if key == "SHARD_END" {
                // Before shard end, do what the shutdown task would do.
                p.set_sequence_number_at_shard_end(p.largest_permitted_checkpoint_value().unwrap());
            }
            p.set_largest_permitted_checkpoint_value(esn(key));
            assert_eq!(p.largest_permitted_checkpoint_value(), Some(esn(key)));

            match action {
                CheckpointAction::None => {
                    assert_eq!(p.last_checkpoint_value(), last_checkpoint_value);
                    continue;
                }
                CheckpointAction::NoSequenceNumber => match checkpointer_type {
                    CheckpointerType::Checkpointer => {
                        p.checkpoint().unwrap();
                    }
                    CheckpointerType::PreparedCheckpointer => {
                        // Java falls through: does BOTH the prepared-checkpoint
                        // path AND the prepare-then-checkpoint path.
                        let prepared = p.prepare_checkpoint().unwrap();
                        prepared.checkpoint().unwrap();
                        let prepared = p.prepare_checkpoint().unwrap();
                        let pc = prepared.pending_checkpoint();
                        p.checkpoint_sequence_sub(pc.sequence_number(), pc.sub_sequence_number())
                            .unwrap();
                    }
                    CheckpointerType::PrepareThenCheckpointer => {
                        let prepared = p.prepare_checkpoint().unwrap();
                        let pc = prepared.pending_checkpoint();
                        p.checkpoint_sequence_sub(pc.sequence_number(), pc.sub_sequence_number())
                            .unwrap();
                    }
                },
                CheckpointAction::WithSequenceNumber => match checkpointer_type {
                    CheckpointerType::Checkpointer => {
                        p.checkpoint_sequence(key).unwrap();
                    }
                    CheckpointerType::PreparedCheckpointer => {
                        let prepared = p.prepare_checkpoint_sequence(key).unwrap();
                        prepared.checkpoint().unwrap();
                        let prepared = p.prepare_checkpoint_sequence(key).unwrap();
                        let pc = prepared.pending_checkpoint();
                        p.checkpoint_sequence_sub(pc.sequence_number(), pc.sub_sequence_number())
                            .unwrap();
                    }
                    CheckpointerType::PrepareThenCheckpointer => {
                        let prepared = p.prepare_checkpoint_sequence(key).unwrap();
                        let pc = prepared.pending_checkpoint();
                        p.checkpoint_sequence_sub(pc.sequence_number(), pc.sub_sequence_number())
                            .unwrap();
                    }
                },
            }

            assert_eq!(p.last_checkpoint_value(), Some(esn(key)));
            assert_eq!(p.largest_permitted_checkpoint_value(), Some(esn(key)));
            assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(esn(key)));
            assert_eq!(
                checkpoint
                    .get_checkpoint_object(SHARD_ID)
                    .unwrap()
                    .unwrap()
                    .checkpoint(),
                &esn(key)
            );
            assert_eq!(
                checkpoint
                    .get_checkpoint_object(SHARD_ID)
                    .unwrap()
                    .unwrap()
                    .pending_checkpoint(),
                None
            );
        }
    }

    #[test]
    fn test_mixed_checkpoint_calls() {
        for plan in mixed_calls_test_plan() {
            let (checkpoint, shard_info) = setup();
            let p = processor(&checkpoint, &shard_info);
            run_mixed_checkpoint_calls(&checkpoint, &p, &plan, CheckpointerType::Checkpointer);
        }
    }

    #[test]
    fn test_mixed_two_phase_checkpoint_calls() {
        for plan in mixed_calls_test_plan() {
            let (checkpoint, shard_info) = setup();
            let p = processor(&checkpoint, &shard_info);
            run_mixed_checkpoint_calls(
                &checkpoint,
                &p,
                &plan,
                CheckpointerType::PreparedCheckpointer,
            );
        }
    }

    #[test]
    fn test_mixed_two_phase_checkpoint_calls2() {
        for plan in mixed_calls_test_plan() {
            let (checkpoint, shard_info) = setup();
            let p = processor(&checkpoint, &shard_info);
            run_mixed_checkpoint_calls(
                &checkpoint,
                &p,
                &plan,
                CheckpointerType::PrepareThenCheckpointer,
            );
        }
    }

    #[test]
    fn test_unset_metrics_scope_during_checkpointing() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        let sn = esn("5019");
        p.set_largest_permitted_checkpoint_value(sn.clone());
        p.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(sn));
    }

    #[test]
    fn test_set_metrics_scope_during_checkpointing() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        let sn = esn("5019");
        p.set_largest_permitted_checkpoint_value(sn.clone());
        p.checkpoint().unwrap();
        assert_eq!(checkpoint.get_checkpoint(SHARD_ID).unwrap(), Some(sn));
    }

    /// Sanity: the checkpointer returned by `checkpointer()` reads through to the
    /// same underlying store.
    #[test]
    fn checkpointer_handle_delegates() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        let handle = p.checkpointer();
        assert_eq!(
            handle.get_checkpoint(SHARD_ID).unwrap(),
            Some(starting_esn())
        );
    }

    /// Verifies `prepare_checkpoint` returns a DoesNothingPreparedCheckpointer
    /// when preparing at the already-committed value (behavioral downcast).
    #[test]
    fn prepare_at_committed_value_is_no_op() {
        let (checkpoint, shard_info) = setup();
        let p = processor(&checkpoint, &shard_info);
        p.set_initial_checkpoint_value(starting_esn());
        p.set_largest_permitted_checkpoint_value(starting_esn());
        let prepared = p.prepare_checkpoint().unwrap();
        assert_eq!(prepared.pending_checkpoint(), starting_esn());
        // No pending checkpoint was written to the store.
        assert_eq!(
            checkpoint
                .get_checkpoint_object(SHARD_ID)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );
    }
}

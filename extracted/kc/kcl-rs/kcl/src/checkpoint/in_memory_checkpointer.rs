//! Test-only port of `software.amazon.kinesis.checkpoint.InMemoryCheckpointer`
//! (a Java test helper). Everything is stored in memory with no fault tolerance.
//!
//! Used by the ported `CheckpointerTest` and
//! `ShardRecordProcessorCheckpointerTest` suites.

use std::collections::HashMap;
use std::sync::Mutex;

use crate::checkpoint::Checkpoint;
use crate::exceptions::KinesisClientLibError;
use crate::processor::Checkpointer;
use crate::retrieval::kpl::ExtendedSequenceNumber;

#[derive(Default)]
struct Inner {
    checkpoints: HashMap<String, ExtendedSequenceNumber>,
    flushpoints: HashMap<String, ExtendedSequenceNumber>,
    pending_checkpoints: HashMap<String, ExtendedSequenceNumber>,
    pending_checkpoint_states: HashMap<String, Option<Vec<u8>>>,
    operation: Option<String>,
}

/// In-memory [`Checkpointer`] for tests.
#[derive(Default)]
pub struct InMemoryCheckpointer {
    inner: Mutex<Inner>,
}

impl InMemoryCheckpointer {
    pub fn new() -> Self {
        Self::default()
    }
}

impl Checkpointer for InMemoryCheckpointer {
    fn set_checkpoint(
        &self,
        lease_key: &str,
        checkpoint_value: &ExtendedSequenceNumber,
        _concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError> {
        let mut inner = self.inner.lock().unwrap();
        inner
            .checkpoints
            .insert(lease_key.to_string(), checkpoint_value.clone());
        inner
            .flushpoints
            .insert(lease_key.to_string(), checkpoint_value.clone());
        inner.pending_checkpoints.remove(lease_key);
        inner.pending_checkpoint_states.remove(lease_key);
        Ok(())
    }

    fn get_checkpoint(
        &self,
        lease_key: &str,
    ) -> Result<Option<ExtendedSequenceNumber>, KinesisClientLibError> {
        let inner = self.inner.lock().unwrap();
        Ok(inner.flushpoints.get(lease_key).cloned())
    }

    fn get_checkpoint_object(
        &self,
        lease_key: &str,
    ) -> Result<Option<Checkpoint>, KinesisClientLibError> {
        let inner = self.inner.lock().unwrap();
        let checkpoint = inner
            .flushpoints
            .get(lease_key)
            .cloned()
            .expect("Checkpoint cannot be null or empty");
        let pending = inner.pending_checkpoints.get(lease_key).cloned();
        let pending_state = inner
            .pending_checkpoint_states
            .get(lease_key)
            .cloned()
            .flatten();
        Ok(Some(Checkpoint::new(checkpoint, pending, pending_state)))
    }

    fn prepare_checkpoint(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError> {
        self.prepare_checkpoint_with_state(lease_key, pending_checkpoint, concurrency_token, &[])
            .map(|_| {
                // Java's 3-arg overload passes null state; the 4-arg above stores
                // Some(&[]) — override to None to match the null semantics.
                let mut inner = self.inner.lock().unwrap();
                inner
                    .pending_checkpoint_states
                    .insert(lease_key.to_string(), None);
            })
    }

    fn prepare_checkpoint_with_state(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        _concurrency_token: &str,
        pending_checkpoint_state: &[u8],
    ) -> Result<(), KinesisClientLibError> {
        let mut inner = self.inner.lock().unwrap();
        inner
            .pending_checkpoints
            .insert(lease_key.to_string(), pending_checkpoint.clone());
        inner.pending_checkpoint_states.insert(
            lease_key.to_string(),
            Some(pending_checkpoint_state.to_vec()),
        );
        Ok(())
    }

    fn set_operation(&self, operation: &str) {
        self.inner.lock().unwrap().operation = Some(operation.to_string());
    }

    fn operation(&self) -> String {
        self.inner
            .lock()
            .unwrap()
            .operation
            .clone()
            .unwrap_or_default()
    }
}

/// Port of `software.amazon.kinesis.checkpoint.CheckpointerTest` — the shared
/// unit tests for [`Checkpointer`] implementations, run against
/// [`InMemoryCheckpointer`].
#[cfg(test)]
mod tests {
    use super::*;

    const TEST_CONCURRENCY_TOKEN: &str = "testToken";

    fn esn(sn: &str) -> ExtendedSequenceNumber {
        ExtendedSequenceNumber::from_sequence_number(sn)
    }

    fn checkpointer() -> InMemoryCheckpointer {
        InMemoryCheckpointer::new()
    }

    #[test]
    fn initial_set_checkpoint() {
        let cp = checkpointer();
        let shard_id = "myShardId";
        cp.set_checkpoint(shard_id, &esn("1"), TEST_CONCURRENCY_TOKEN)
            .unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("1")));
    }

    #[test]
    fn advancing_set_checkpoint() {
        let cp = checkpointer();
        let shard_id = "myShardId";
        for i in 0..10 {
            let sn = i.to_string();
            cp.set_checkpoint(shard_id, &esn(&sn), TEST_CONCURRENCY_TOKEN)
                .unwrap();
            assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn(&sn)));
        }
    }

    #[test]
    fn set_and_get_checkpoint() {
        let cp = checkpointer();
        let shard_id = "testShardId-1";
        cp.set_checkpoint(shard_id, &esn("12345"), "token-1")
            .unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &esn("12345")
        );
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );
    }

    #[test]
    fn initial_prepare_checkpoint() {
        let cp = checkpointer();
        let shard_id = "myShardId";
        cp.set_checkpoint(shard_id, &esn("1"), TEST_CONCURRENCY_TOKEN)
            .unwrap();
        cp.prepare_checkpoint(shard_id, &esn("99999"), TEST_CONCURRENCY_TOKEN)
            .unwrap();

        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("1")));
        let obj = cp.get_checkpoint_object(shard_id).unwrap().unwrap();
        assert_eq!(obj.checkpoint(), &esn("1"));
        assert_eq!(obj.pending_checkpoint(), Some(&esn("99999")));
    }

    #[test]
    fn initial_prepare_checkpoint_with_application_state() {
        let cp = checkpointer();
        let shard_id = "myShardId";
        let app_state = b"applicationState";
        cp.set_checkpoint(shard_id, &esn("1"), TEST_CONCURRENCY_TOKEN)
            .unwrap();
        cp.prepare_checkpoint_with_state(
            shard_id,
            &esn("99999"),
            TEST_CONCURRENCY_TOKEN,
            app_state,
        )
        .unwrap();

        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("1")));
        let obj = cp.get_checkpoint_object(shard_id).unwrap().unwrap();
        assert_eq!(obj.checkpoint(), &esn("1"));
        assert_eq!(obj.pending_checkpoint(), Some(&esn("99999")));
        assert_eq!(obj.pending_checkpoint_state(), Some(app_state.as_slice()));
    }

    #[test]
    fn advancing_prepare_checkpoint() {
        let cp = checkpointer();
        let shard_id = "myShardId";
        cp.set_checkpoint(shard_id, &esn("12345"), TEST_CONCURRENCY_TOKEN)
            .unwrap();

        for i in 0..10 {
            let sn = i.to_string();
            cp.prepare_checkpoint(shard_id, &esn(&sn), TEST_CONCURRENCY_TOKEN)
                .unwrap();
            assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
            let obj = cp.get_checkpoint_object(shard_id).unwrap().unwrap();
            assert_eq!(obj.checkpoint(), &esn("12345"));
            assert_eq!(obj.pending_checkpoint(), Some(&esn(&sn)));
        }
    }

    #[test]
    fn advancing_prepare_checkpoint_with_application_state() {
        let cp = checkpointer();
        let shard_id = "myShardId";
        let app_state = b"applicationState";
        cp.set_checkpoint(shard_id, &esn("12345"), TEST_CONCURRENCY_TOKEN)
            .unwrap();

        for i in 0..10 {
            let sn = i.to_string();
            cp.prepare_checkpoint_with_state(
                shard_id,
                &esn(&sn),
                TEST_CONCURRENCY_TOKEN,
                app_state,
            )
            .unwrap();
            assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
            let obj = cp.get_checkpoint_object(shard_id).unwrap().unwrap();
            assert_eq!(obj.checkpoint(), &esn("12345"));
            assert_eq!(obj.pending_checkpoint(), Some(&esn(&sn)));
            assert_eq!(obj.pending_checkpoint_state(), Some(app_state.as_slice()));
        }
    }

    #[test]
    fn prepare_and_set_checkpoint() {
        let cp = checkpointer();
        let shard_id = "testShardId-1";
        let token = "token-1";

        cp.set_checkpoint(shard_id, &esn("12345"), token).unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &esn("12345")
        );
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );

        cp.prepare_checkpoint(shard_id, &esn("99999"), token)
            .unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &esn("12345")
        );
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            Some(&esn("99999"))
        );

        cp.set_checkpoint(shard_id, &esn("99999"), token).unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("99999")));
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .checkpoint(),
            &esn("99999")
        );
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );
    }

    #[test]
    fn prepare_and_set_checkpoint_with_application_state() {
        let cp = checkpointer();
        let shard_id = "testShardId-1";
        let token = "token-1";
        let app_state = b"applicationState";

        cp.set_checkpoint(shard_id, &esn("12345"), token).unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
        assert_eq!(
            cp.get_checkpoint_object(shard_id)
                .unwrap()
                .unwrap()
                .pending_checkpoint(),
            None
        );

        cp.prepare_checkpoint_with_state(shard_id, &esn("99999"), token, app_state)
            .unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("12345")));
        let obj = cp.get_checkpoint_object(shard_id).unwrap().unwrap();
        assert_eq!(obj.checkpoint(), &esn("12345"));
        assert_eq!(obj.pending_checkpoint(), Some(&esn("99999")));
        assert_eq!(obj.pending_checkpoint_state(), Some(app_state.as_slice()));

        cp.set_checkpoint(shard_id, &esn("99999"), token).unwrap();
        assert_eq!(cp.get_checkpoint(shard_id).unwrap(), Some(esn("99999")));
        let obj = cp.get_checkpoint_object(shard_id).unwrap().unwrap();
        assert_eq!(obj.checkpoint(), &esn("99999"));
        assert_eq!(obj.pending_checkpoint(), None);
        assert_eq!(obj.pending_checkpoint_state(), None);
    }
}

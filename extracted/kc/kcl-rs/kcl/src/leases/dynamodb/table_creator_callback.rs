//! Port of `software.amazon.kinesis.leases.dynamodb.TableCreatorCallback` and
//! `TableCreatorCallbackInput`.
//!
//! A functional callback invoked **exactly once**, only when the lease table was
//! newly created (not if it pre-existed), after the table reaches `ACTIVE`
//! status — used for post-creation actions (enabling TTL, alarms, etc).
//!
//! # Design
//!
//! Java's `@FunctionalInterface TableCreatorCallback` (single method
//! `performAction(TableCreatorCallbackInput)`) maps to the [`TableCreatorCallback`]
//! trait with one method. The `NOOP_TABLE_CREATOR_CALLBACK` constant becomes the
//! zero-sized [`NoopTableCreatorCallback`] struct (a `TableCreatorCallback` that
//! does nothing).
//!
//! `TableCreatorCallbackInput` (Lombok `@Builder`/`@Data`, both fields `@NonNull`)
//! maps to a plain struct with a `bon::Builder`; the two fields are non-`Option`
//! so their presence is enforced by the type system (Java `@NonNull`).

use aws_sdk_dynamodb::Client;
use bon::Builder;

/// Input object passed to [`TableCreatorCallback::perform_action`] after
/// lease-table creation. Carries the DynamoDB client and table name.
///
/// Port of `TableCreatorCallbackInput`. Both fields are `@NonNull` in Java; here
/// they are required (non-`Option`) builder fields.
#[derive(Clone, Builder)]
pub struct TableCreatorCallbackInput {
    /// The DynamoDB client (Java `dynamoDbClient`).
    dynamo_db_client: Client,
    /// The lease table name (Java `tableName`).
    table_name: String,
}

impl TableCreatorCallbackInput {
    /// The DynamoDB client (fluent accessor `dynamoDbClient()`).
    pub fn dynamo_db_client(&self) -> &Client {
        &self.dynamo_db_client
    }

    /// The lease table name (fluent accessor `tableName()`).
    pub fn table_name(&self) -> &str {
        &self.table_name
    }
}

/// Callback interface for interacting with the DynamoDB lease table post
/// creation. Port of `TableCreatorCallback` (`@FunctionalInterface`).
pub trait TableCreatorCallback: Send + Sync {
    /// Actions to perform on the lease table once it has been created and is in
    /// the `ACTIVE` status. Will **not** be called if the table pre-existed.
    fn perform_action(&self, input: &TableCreatorCallbackInput);
}

/// No-op [`TableCreatorCallback`] (Java `NOOP_TABLE_CREATOR_CALLBACK`).
#[derive(Debug, Default, Clone, Copy)]
pub struct NoopTableCreatorCallback;

impl TableCreatorCallback for NoopTableCreatorCallback {
    fn perform_action(&self, _input: &TableCreatorCallbackInput) {
        // Do nothing.
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::sync::Arc;

    #[tokio::test]
    async fn noop_does_nothing() {
        let client = crate::leases::dynamodb::test_support::mock_ddb_client(&[]);
        let input = TableCreatorCallbackInput::builder()
            .dynamo_db_client(client)
            .table_name("t".to_string())
            .build();
        assert_eq!(input.table_name(), "t");
        NoopTableCreatorCallback.perform_action(&input);
    }

    #[tokio::test]
    async fn custom_callback_is_invoked() {
        struct Counting(Arc<AtomicUsize>);
        impl TableCreatorCallback for Counting {
            fn perform_action(&self, input: &TableCreatorCallbackInput) {
                assert_eq!(input.table_name(), "leases");
                self.0.fetch_add(1, Ordering::SeqCst);
            }
        }
        let count = Arc::new(AtomicUsize::new(0));
        let cb = Counting(count.clone());
        let client = crate::leases::dynamodb::test_support::mock_ddb_client(&[]);
        let input = TableCreatorCallbackInput::builder()
            .dynamo_db_client(client)
            .table_name("leases".to_string())
            .build();
        cb.perform_action(&input);
        assert_eq!(count.load(Ordering::SeqCst), 1);
    }
}

//! Minimal single-stream KCL consumer — the example embedded in the README.
//!
//! Run against LocalStack:
//! ```sh
//! AWS_ENDPOINT_URL=http://localhost:4566 AWS_REGION=us-east-1 \
//! AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
//!   cargo run --example single_stream
//! ```

use std::sync::Arc;

use kcl::common::ConfigsBuilder;
use kcl::coordinator::Scheduler;
use kcl::lifecycle::events::{
    InitializationInput, LeaseLostInput, ProcessRecordsInput, ShardEndedInput,
    ShutdownRequestedInput,
};
use kcl::processor::{
    ShardRecordProcessor, ShardRecordProcessorFactory, SingleStreamTracker, StreamTracker,
};

struct MyProcessor;

impl ShardRecordProcessor for MyProcessor {
    fn initialize(&mut self, input: InitializationInput) {
        println!("initializing on shard {:?}", input.shard_id());
    }

    fn process_records(&mut self, input: ProcessRecordsInput) {
        for record in input.records().unwrap_or(&[]) {
            println!(
                "record pk={:?} seq={:?} ({} bytes)",
                record.partition_key(),
                record.sequence_number(),
                record.data().map(|d| d.len()).unwrap_or(0),
            );
        }
        if let Some(checkpointer) = input.checkpointer() {
            checkpointer.checkpoint().expect("checkpoint failed");
        }
    }

    fn lease_lost(&mut self, _input: LeaseLostInput) {
        // The lease was taken by another worker; checkpointing is no longer possible.
    }

    fn shard_ended(&mut self, input: ShardEndedInput) {
        // Required: completing the shard lets its children be processed.
        input
            .checkpointer()
            .checkpoint()
            .expect("checkpoint at shard end failed");
    }

    fn shutdown_requested(&mut self, input: ShutdownRequestedInput) {
        let _ = input.checkpointer().checkpoint();
    }
}

struct MyFactory;

impl ShardRecordProcessorFactory for MyFactory {
    fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        Box::new(MyProcessor)
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Region/credentials/endpoint come from the standard AWS environment
    // (AWS_PROFILE, AWS_REGION, AWS_ENDPOINT_URL, ...).
    let aws = aws_config::load_defaults(aws_config::BehaviorVersion::latest()).await;

    let tracker: Arc<dyn StreamTracker + Send + Sync> =
        Arc::new(SingleStreamTracker::from_stream_name("my-stream"));
    let configs = ConfigsBuilder::new(
        tracker,
        "my-app", // application name = lease table + CloudWatch namespace
        aws_sdk_kinesis::Client::new(&aws),
        aws_sdk_dynamodb::Client::new(&aws),
        aws_sdk_cloudwatch::Client::new(&aws),
        "worker-1",
        Arc::new(MyFactory),
    );

    let scheduler = Scheduler::new(
        configs.checkpoint_config(),
        configs.coordinator_config(),
        configs.lease_management_config(),
        configs.lifecycle_config(),
        configs.metrics_config(),
        configs.processor_config(),
        configs.retrieval_config(),
    )?;

    // Graceful shutdown on Ctrl-C.
    let scheduler_for_signal = Arc::clone(&scheduler);
    tokio::spawn(async move {
        tokio::signal::ctrl_c().await.expect("ctrl-c handler");
        scheduler_for_signal.shutdown().await;
    });

    scheduler.run().await; // blocks until shutdown completes
    Ok(())
}

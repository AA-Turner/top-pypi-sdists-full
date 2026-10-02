//! Rust port of the Amazon Kinesis Client Library (KCL).
//!
//! This crate is a faithful port of the Java `amazon-kinesis-client` library.
//! It runs the full KCL machinery (lease coordination, checkpointing, record
//! retrieval, lifecycle state machine) on its own async runtime, independent of
//! any host language. Language bindings (e.g. the `kcl-python` crate) drive it
//! from the outside.
//!
//! Module layout mirrors the Java package `software.amazon.kinesis`.

pub mod checkpoint;
pub mod common;
pub mod coordinator;
pub mod exceptions;
pub mod leader;
pub mod leases;
pub mod lifecycle;
pub mod metrics;
pub mod processor;
pub mod retrieval;
pub mod schemaregistry;
pub mod utils;
pub mod worker;

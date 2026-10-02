//! Port of `software.amazon.kinesis.retrieval.kpl`.
//!
//! Types related to Kinesis Producer Library (KPL) aggregated records.

pub mod extended_sequence_number;
pub mod messages;

pub use extended_sequence_number::ExtendedSequenceNumber;

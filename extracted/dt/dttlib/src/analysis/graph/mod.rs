//! Analysis graphs
//! The analysis is built up first
//! from an idealized "scheme" graph of a single channel pipeline
//! and another idealized "scheme" graph of the cross-channel pipelines
//! from these two, per-channel and per-channel-pair graphs are combined
//! into a single, connected, directed acyclic graph (DAG)
//! This dag has sources representing the data source, and single sink represent results output.
//! this graph is used to create the entire analysis pipeline set.
//!
//! The following are all errors.
//! 1. A disconnected part of the graph.
//! 2. A cycle in the graph.
//! 3. A source that's not a data source.
//! 4. A sink that's not the result node
//! 5. Input ports that don't have exactly 1 input.

pub mod analysis;
pub mod scheme;

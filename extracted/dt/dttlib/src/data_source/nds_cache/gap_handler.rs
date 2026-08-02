//! Fill in gaps in nds_cache data streams
use crate::data_source::buffer::Buffer;
use core::f32;
use pipelines::complex::{c64, c128};
use std::{collections::HashMap, i16, iter};

use crate::run_context::RunContext;

/// take a channel
pub(super) async fn setup_gap_handler(
    rc: Box<RunContext>,
    mut input: tokio::sync::mpsc::Receiver<Vec<Buffer>>,
    max_size: usize,
) -> tokio::sync::mpsc::Receiver<Vec<Buffer>> {
    let (output_tx, output_rx) = tokio::sync::mpsc::channel(1);

    tokio::spawn(async move {
        loop {
            tokio::select! {
                x = input.recv() => {
                    match x {
                        Some(bufs) => {
                            let total_size = total_filled_buffer_size(&bufs);

                            let out_buffers = if total_size > max_size {
                                rc.user_messages.set_error("REQSIZE", "request is too big for the cache");
                                Vec::new()
                            } else {
                                rc.user_messages.clear_message("REQSIZE");
                                let mut by_channel: HashMap<String, Vec<Buffer>> = HashMap::new();

                                // collect buffers by channel name
                                for buf in bufs.into_iter() {
                                    let key = buf.channel().name().clone();
                                    if let Some(v) = by_channel.get_mut(&key) {
                                        v.push(buf);
                                    } else {
                                        by_channel.insert(key, vec![buf]);
                                    }
                                }

                                let mut out_buf = Vec::with_capacity(by_channel.len());
                                // process any channels that have more than one buffer.
                                for mut buffs in by_channel.into_values() {
                                    if buffs.len() == 1 {
                                        out_buf.push(buffs.remove(0));
                                    } else {
                                        out_buf.push(handle_gaps(&rc, buffs));
                                    }
                                }
                                out_buf
                            };
                            if let Err(_) = output_tx.send(out_buffers).await {
                                break;
                            }
                        },
                        None => break,
                    }
                }
            }
        }
    });

    output_rx
}

/// calculate the total size of the buffers if all gaps were filled
fn total_filled_buffer_size(buffers: &Vec<Buffer>) -> usize {
    let mut total: usize = 0;
    let mut sizes = HashMap::new();
    let mut starts = HashMap::new();
    let mut ends = HashMap::new();
    let mut periods = HashMap::new();
    for buf in buffers {
        let name = buf.channel().name();

        if !sizes.contains_key(name) {
            sizes.insert(name, buf.channel().data_type().size());
        }

        if !periods.contains_key(name) {
            periods.insert(name, buf.period());
        }

        if let Some(s) = starts.get(name) {
            if buf.start() < *s {
                starts.insert(name, buf.start());
            }
        } else {
            starts.insert(name, buf.start());
        }

        if let Some(e) = ends.get(name) {
            if buf.end() > *e {
                ends.insert(name, buf.end());
            }
        } else {
            ends.insert(name, buf.end());
        }
    }

    for (n, z) in sizes {
        match (starts.get(n), ends.get(n), periods.get(n)) {
            (Some(s), Some(e), Some(p)) => total += ((e - s) / p) as usize * z,
            _ => (),
        }
    }

    total
}

/// buffers are all assumed to be of the same channel and non-overlapping
/// return a single buffer with gaps between buffers filled in with an appropriate value
fn handle_gaps(_rc: &Box<RunContext>, mut buffers: Vec<Buffer>) -> Buffer {
    buffers.sort();
    let mut first = buffers.remove(0);
    let period = first.period();
    let mut total_gap_size = 0;
    for buffer in buffers {
        let end_0 = first.end();
        let start_1 = buffer.start();
        let gap_size = ((start_1 - end_0) / period) as usize;
        total_gap_size += gap_size;
        match (&mut first.cache_buffer, buffer.cache_buffer) {
            (nds_cache_rs::buffer::Buffer::Int8(ts1), nds_cache_rs::buffer::Buffer::Int8(ts2)) => {
                ts1.data_mut().extend(iter::repeat(i8::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Int16(ts1),
                nds_cache_rs::buffer::Buffer::Int16(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(i16::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Int32(ts1),
                nds_cache_rs::buffer::Buffer::Int32(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(i32::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Int64(ts1),
                nds_cache_rs::buffer::Buffer::Int64(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(i64::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::UInt8(ts1),
                nds_cache_rs::buffer::Buffer::UInt8(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(u8::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::UInt16(ts1),
                nds_cache_rs::buffer::Buffer::UInt16(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(u16::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::UInt32(ts1),
                nds_cache_rs::buffer::Buffer::UInt32(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(u32::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::UInt64(ts1),
                nds_cache_rs::buffer::Buffer::UInt64(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(u64::MAX).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Float32(ts1),
                nds_cache_rs::buffer::Buffer::Float32(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(f32::NAN).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Float64(ts1),
                nds_cache_rs::buffer::Buffer::Float64(ts2),
            ) => {
                ts1.data_mut().extend(iter::repeat(f64::NAN).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Complex32(ts1),
                nds_cache_rs::buffer::Buffer::Complex32(ts2),
            ) => {
                ts1.data_mut()
                    .extend(iter::repeat(c64::new(f32::NAN, f32::NAN)).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Complex64(ts1),
                nds_cache_rs::buffer::Buffer::Complex64(ts2),
            ) => {
                ts1.data_mut()
                    .extend(iter::repeat(c128::new(f64::NAN, f64::NAN)).take(gap_size));
                ts1.data_mut().extend(ts2.data().iter());
            }
            (
                nds_cache_rs::buffer::Buffer::Unknown(ts1),
                nds_cache_rs::buffer::Buffer::Unknown(ts2),
            ) => {
                ts1.data_mut()
                    .extend(iter::repeat(vec![0; 16]).take(gap_size));
                ts1.data_mut().extend(ts2.take_data().into_iter());
            }
            // by expectation that types of all buffers are the same, this can't be reached.
            _ => {
                log::warn!("buffers from the same channel were of a different type!");
                continue;
            }
        }
    }
    first.fields.total_gap_size = total_gap_size;
    first
}

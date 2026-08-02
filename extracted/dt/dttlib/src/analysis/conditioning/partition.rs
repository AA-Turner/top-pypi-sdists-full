//! Partition incoming data stream into measurement segments
//! The segments may possibly overlap, so the pipeline must retain data
//! Between executions.

use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::timeline::CountSegments;
use futures::future::FutureExt;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use pipeline_macros::box_async;
use pipelines::pipe::Pipe1;
use pipelines::{PipeData, PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

/// This structure assume segments are all of an equal length
/// and are all separated by the same amount of time.
#[derive(Clone, Debug)]
pub struct PartitionPipeline<T: PipeData> {
    /// the start time of the next segment
    next_start_time: PipInstant,

    /// the length of a segment
    length: PipDuration,

    /// the time from the start of one segment to the end of the next segment.
    pitch: PipDuration,

    /// Data saved previously that will be needed for future segments
    history: Option<TimeDomainArray<T>>,

    /// total number of segments we'll collect
    num_segments: CountSegments,

    /// number of segments we've collected so far
    count_segments: u64,
}

impl<T: PipeDataPrimitive> PartitionPipeline<T> {
    #[box_async]
    fn generate(
        rc: Box<dyn UserMsgProvider>,
        state: &mut Self,
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        // align startpoint of input to rate
        let aligned_input = input.as_ref().clone().align_start();

        // Add to existing data
        let old_history = state.history.take();
        let mut history = match old_history {
            Some(mut t) => {
                if t.end_gps_pip() != aligned_input.start_gps_pip {
                    let msg = format!(
                        "Partition Pipeline received non-contiguous data. Previous segment ended just before {}  but new segment started at {}. They should be equal.",
                        t.end_gps_pip(),
                        aligned_input.start_gps_pip
                    );
                    rc.user_message_handle().error(msg);
                    return PipeResult::Close;
                }
                t.data.extend(aligned_input.data);
                t
            }
            None => aligned_input,
        };

        // Make sure they match.  Throw an error if they don't.

        // Generate any output
        let mut out = Vec::new();
        loop {
            let end_gps_pip = state.next_start_time + state.length;
            if end_gps_pip > history.end_gps_pip() {
                break;
            }

            let send_segment = match state.num_segments {
                CountSegments::N(n) => n > state.count_segments,
                CountSegments::Indefinite => true,
            };

            if send_segment {
                out.push(Arc::new(
                    history.copy_from(state.next_start_time, end_gps_pip),
                ));
                state.count_segments += 1;
            }
            state.next_start_time =
                history.snap_to_step_pip_instant(state.next_start_time + state.pitch);
        }
        let ep1 = history.end_gps_pip();
        // save leftover data
        if let Err(_) = history.trim_to(rc, state.next_start_time) {
            // something's gone wrong with the trimming.  The whole calculation is bad.
            // Abort.
            return PipeResult::Close;
        };
        let ep2 = history.end_gps_pip();
        assert_eq!(ep1, ep2);
        state.history = Some(history);

        out.into()
    }

    pub(crate) async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        start_time: PipInstant,
        length: PipDuration,
        pitch: PipDuration,
        num_segments: CountSegments,
        input: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
        let part = Self {
            length,
            pitch,
            next_start_time: start_time,
            history: None,
            num_segments,
            count_segments: 0,
        };

        Ok(Pipe1::create(rc, name, Self::generate, part, None, None, input).await?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::analysis::conditioning::time_delay::tests::RampSource;
    use std::time::Duration;
    use tokio::time::sleep;
    use user_messages::{TestSender, TestUserMessageProvider};

    #[test]
    fn test_partition() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let mut sender = TestSender::default();
        let rc = Box::new(rt.block_on(TestUserMessageProvider::new(sender.clone())));

        const num_chunks: u64 = 5;

        let mut part_out = {
            // setup ramp
            let ramp_out = rt.block_on(async {
                RampSource::create(rc.ump_clone(), "rampsource", num_chunks, 4, 64.0)
            });

            // create subtracter
            let part = rt.block_on(async {
                PartitionPipeline::<f64>::create(
                    rc.clone(),
                    "partition",
                    PipInstant::from_gpst_sec(0),
                    PipDuration::from_seconds(0.0625),
                    PipDuration::from_seconds(0.03125),
                    CountSegments::N(3),
                    &ramp_out,
                )
                .await
                .unwrap()
                .subscribe_or_die(rc.clone())
                .await
            });
            part
        };

        let mut chunk_count = 0;
        let out = rt.block_on(async {
            let mut out = Vec::new();
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting for trim.");
                      },
                    res =  part_out.recv() => match res {
                        Some(value) => {
                                chunk_count += 1;
                                out.append(&mut value.value.data.clone());
                        },
                        None => break,
                    },
                    mh = sender.wait_first() => {
                        println!("{:?}", mh);
                    },
                }
            }
            out
        });

        const target: [f64; 12] = [0.0, 1.0, 2.0, 3.0, 2.0, 3.0, 4.0, 5.0, 4.0, 5.0, 6.0, 7.0];
        assert_eq!(chunk_count, 3);
        assert_eq!(out, target);
    }
}

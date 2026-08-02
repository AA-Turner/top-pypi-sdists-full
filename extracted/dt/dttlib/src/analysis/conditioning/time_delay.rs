//! Timeshift data in a time domain array, but only later in time
//!
//! References
//!
//! 1. gds-sigp time_delay()
//!    https://git.ligo.org/cds/software/gds-sigp/-/blob/ref1/src/SignalProcessing/DecimateBy2/decimate.cc#L291

use crate::AccumulationStats;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use futures::FutureExt;
use num_traits::FromPrimitive;
use pipeline_macros::box_async;
use pipelines::pipe::Pipe1;
use pipelines::{PipeData, PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

#[derive(Clone, Debug)]
pub struct TimeDelay<T: PipeData> {
    delay_length: i32,
    delay_history: Vec<T>,
}

impl<T: PipeDataPrimitive + Default> TimeDelay<T> {
    /// delay_length is the number of samples to delay
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: String,
        delay_length: i32,
        input_sub: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
        let size = usize::from_i32(delay_length).unwrap_or(0);
        let mut delay_history = Vec::with_capacity(size);
        delay_history.resize(size, T::default());

        let td = TimeDelay {
            delay_length,
            delay_history,
        };
        Ok(Pipe1::create(
            rc.ump_clone(),
            name,
            Self::generate,
            td,
            None,
            None,
            input_sub,
        )
        .await?)
    }

    #[box_async]
    fn generate(
        _rc: Box<dyn UserMsgProvider>,
        state: &mut Self,
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        let mut out_data = state.delay_history.clone();
        out_data.append(&mut input.data.clone());
        let drain_start = out_data.len() - usize::from_i32(state.delay_length).unwrap_or(0);

        // we could instead insert some zeroes the first time, then never do anything after that.
        state.delay_history = out_data.drain(drain_start..).collect();
        let out_td_array = TimeDomainArray {
            data: out_data,
            accumulation_stats: AccumulationStats::default(),
            period_pip: input.period_pip,
            start_gps_pip: input.start_gps_pip,
            total_gap_size: input.total_gap_size,
            id: input.id.clone(),
            unit: input.unit.clone(),
            real_end_gps_pip: input.real_end_gps_pip,
        };
        Arc::new(out_td_array).into()
    }
}

#[cfg(test)]
pub mod tests {
    use super::*;
    use crate::analysis::types::time_domain_array::TimeDomainArray;
    use crate::run_context::tests::start_runtime;
    use crate::user::ResponseToUser;
    use ligo_hires_gps_time::{PipDuration, PipInstant};
    use pipelines::PipeResult;
    use pipelines::pipe::Pipe0;
    use std::time::Duration;
    use tokio::time::sleep;
    use user_messages::UserMsgProvider;

    const NUM_CHUNKS: u64 = 3;

    /// output a sequence of TimeDomainArrays with ever-increasing
    /// values stopping when num_chunks is reached.
    #[derive(Debug, Clone)]
    pub struct RampSource {
        pub num_chunks: u64,
        pub chunk_size: usize,
        pub rate_hz: f64,
        pub segment: u64,
    }

    impl RampSource {
        #[box_async]
        fn generate(
            _rc: Box<dyn UserMsgProvider>,
            state: &mut Self,
        ) -> PipeResult<TimeDomainArray<f64>> {
            if state.segment < state.num_chunks {
                let timestep_pip = PipDuration::freq_hz_to_period(state.rate_hz);
                let start = state.segment * state.chunk_size as u64;
                let end = start + state.chunk_size as u64;
                let td_array = TimeDomainArray {
                    start_gps_pip: PipInstant::default()
                        + timestep_pip * state.segment * state.chunk_size,
                    period_pip: timestep_pip,
                    data: (start..end).map(|x| x as f64).collect(),
                    ..TimeDomainArray::default()
                };
                state.segment += 1;
                td_array.into()
            } else {
                PipeResult::Close
            }
        }

        pub fn create<S: Into<String>>(
            rc: Box<dyn UserMsgProvider>,
            name: S,
            num_chunks: u64,
            chunk_size: usize,
            rate_hz: f64,
        ) -> PipelineSubscriber<TimeDomainArray<f64>> {
            let rs = RampSource {
                num_chunks,
                chunk_size,
                rate_hz,
                segment: 0,
            };

            Pipe0::create(rc, name, RampSource::generate, rs, None, None)
        }
    }

    #[test]
    fn time_delay() {
        let (uc, mut or, rc) = start_runtime();

        let mut delay_out = {
            let src_out = uc.runtime.block_on(async {
                RampSource::create(rc.ump_clone(), "ramp source", NUM_CHUNKS, 4, 64.0)
            });
            let delay_out = uc.runtime.block_on(async {
                TimeDelay::<f64>::create(rc.ump_clone(), "time_delay".to_string(), 2, &src_out)
                    .await
                    .unwrap()
                    .subscribe_or_die(rc.ump_clone())
                    .await
            });
            delay_out
        };

        let (out, start_gps_pip) = uc.runtime.block_on(async move {
            let mut count = 0;
            let mut output = Vec::new();
            let mut start_gps_pip: Option<PipInstant> = None;
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting for chunks.  Only got {} of 4 chunks.", count);
                      },
                    res =  delay_out.recv() => match res {
                        Some(value) => {
                            output.append(&mut value.value.data.clone());
                            count += 1;
                            if let None = start_gps_pip {
                                start_gps_pip = Some(value.value.start_gps_pip);
                            }
                            if count > NUM_CHUNKS {
                                panic!("Got too many chunks from pipeline")
                             }
                        },
                        None => break,
                    },
                    Some(m) = or.recv() => {
                          match m {
                                ResponseToUser::AllMessages(mh) =>{
                                        println!("{:?}", mh);
                                    }
                                _ => (),
                            }
                        },
                }
            }
            (output, start_gps_pip)
        });

        const targ_out: [f64; 12] = [0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0];
        assert_eq!(out, targ_out);
        match start_gps_pip {
            None => panic!("No start time found"),
            Some(t) => assert_eq!(t.to_gpst_seconds(), 0.0),
        }
    }
}

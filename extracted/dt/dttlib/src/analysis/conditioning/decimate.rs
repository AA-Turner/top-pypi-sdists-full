//! Decimate channel data down to a given rate.
//!
//! References:
//! 1. cds/software/dtt dataChannel:preprocessing::process
//!    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L575

use crate::AccumulationStats;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::gds_sigp::decimate::{FiltHistory, IsComplex, close_decimate, decimate, open_decimate};
use crate::params::channel_params::decimation_parameters::DecimationParameters;
use futures::future::FutureExt;
use ligo_hires_gps_time::PipDuration;
use pipeline_macros::box_async;
use pipelines::{
    PipeData, PipeDataPrimitive, PipeResult, PipelineError, PipelineSubscriber, pipe::Pipe1,
};
use std::sync::Arc;
use user_messages::UserMsgProvider;

/// Pipeline for decimating a fast incoming data stream to a lower rate
/// Can only decimate by a power of two.
#[derive(Clone, Debug)]
pub struct Decimate<T: PipeData> {
    history: FiltHistory<T>,
    remainder: Vec<T>,

    params: DecimationParameters,
}

impl<T: PipeDataPrimitive + Default + IsComplex> Decimate<T> {
    fn setup(&mut self) -> Result<(), PipelineError> {
        open_decimate(
            self.params.filter.clone(),
            self.params.num_decs,
            &mut self.history,
        )
    }

    fn teardown(&mut self) {
        close_decimate(self.params.filter.clone(), &mut self.history)
    }

    #[box_async]
    pub fn generate(
        rc: Box<dyn UserMsgProvider>,
        state: &mut Self,
        data: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        // Input array
        let in_td_array = data.as_ref();

        // add in any remainder from the last call.
        let rem_size = state.remainder.len();

        // adjust start time backward to account for remainder.
        let remainder_dt_pip: PipDuration = in_td_array.period_pip * rem_size;

        // merge the remainder data
        let mut new_data: Vec<T> = state.remainder.clone();
        new_data.append(&mut in_td_array.data.clone());

        // calculate actual decimation factor
        let decim_factor = 1 << state.params.num_decs; // real decimation factor is 2^n where n = self.factor.

        // gather remainder for the next time.  Submitted length must be equal to the decimation factor.
        let new_rem_size = new_data.len() % decim_factor;
        let drain_range = (new_data.len() - new_rem_size)..;
        state.remainder = new_data.drain(drain_range).collect();

        let td_array = TimeDomainArray {
            start_gps_pip: in_td_array.start_gps_pip - remainder_dt_pip,
            period_pip: in_td_array.period_pip,
            data: new_data,
            accumulation_stats: AccumulationStats::default(),
            total_gap_size: 0,
            id: in_td_array.id.clone(),
            unit: in_td_array.unit.clone(),
            real_end_gps_pip: None,
        };

        // do delay?
        let out_start_pip = td_array.start_gps_pip;

        // decimation
        let out_period_pip = td_array.period_pip * decim_factor;

        let res = decimate(
            state.params.filter,
            td_array.data.as_slice(),
            state.params.num_decs,
            &mut state.history,
        );
        match res {
            Ok(v) => vec![Arc::new(TimeDomainArray {
                start_gps_pip: out_start_pip,
                period_pip: out_period_pip,
                data: v,
                accumulation_stats: AccumulationStats::default(),
                total_gap_size: 0,
                id: in_td_array.id.clone(),
                unit: in_td_array.unit.clone(),
                real_end_gps_pip: None,
            })]
            .into(),
            Err(e) => {
                let err_msg = format!(
                    "Decimation error in time {} pips: {}",
                    td_array.start_gps_pip, e
                );
                rc.user_message_handle().error(err_msg.clone());
                PipeResult::Close
            }
        }
    }

    /// # Decimation pipeline creation

    /// Initialize with the filter used for decimation
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: String,
        params: &DecimationParameters,
        input_sub: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
        let decim = Decimate {
            history: FiltHistory::new(),
            remainder: Vec::new(),
            params: params.clone(),
        };
        Ok(Pipe1::create(
            rc.ump_clone(),
            name,
            Decimate::<T>::generate,
            decim,
            Some(Decimate::<T>::setup),
            Some(Decimate::<T>::teardown),
            input_sub,
        )
        .await?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::run_context::tests::start_runtime;
    use crate::user::ResponseToUser;
    use ligo_hires_gps_time::PipInstant;
    use pipelines::complex::c128;
    use pipelines::pipe::Pipe0;
    use std::fmt::Debug;
    use std::time::Duration;
    use tokio::time::sleep;

    /// output a sequence of TimeDomainArrays with ever-increasing
    /// values stoping when num_chunks is reached.
    #[derive(Clone, Debug)]
    struct DecimSource<T: PipeData> {
        max_iters: u64,
        iter_count: u64,
        chunk_size: usize,
        rate_hz: f64,
        index: usize,
        template: Vec<T>,
        segment: u64,
    }

    impl<T: PipeDataPrimitive> DecimSource<T> {
        #[box_async]
        fn generate(
            _rc: Box<dyn UserMsgProvider>,
            state: &mut Self,
        ) -> PipeResult<TimeDomainArray<T>> {
            if state.iter_count >= state.max_iters {
                return PipeResult::Close;
            }

            let segment = state.segment;

            let mut out_vec = Vec::with_capacity(state.chunk_size);
            while (state.iter_count < state.max_iters) && (out_vec.len() < state.chunk_size) {
                let left = state.chunk_size - out_vec.len();
                let n = left.min(state.template.len() - state.index);
                out_vec.extend_from_slice(&state.template[state.index..state.index + n]);
                state.index += n;
                if state.index >= state.template.len() {
                    state.iter_count += 1;
                    state.index = 0;
                }
            }

            let timestep_pip = PipDuration::freq_hz_to_period(state.rate_hz);
            let td_array = TimeDomainArray {
                start_gps_pip: PipInstant::default()
                    + timestep_pip * segment * state.chunk_size as u64,
                period_pip: timestep_pip,
                data: out_vec,
                ..TimeDomainArray::default()
            };
            state.segment = segment + 1;
            vec![Arc::new(td_array)].into()
        }
    }

    #[test]
    fn decim_pipeline_f64() {
        let (uc, mut or, rc) = start_runtime();
        let decim_source_state = DecimSource {
            max_iters: 3,
            iter_count: 0,
            chunk_size: 4,
            rate_hz: 16.0,
            index: 0,
            template: vec![1.0, -1.0, 1.5, -1.0],
            segment: 0,
        };

        let mut decim_out = {
            let src_out = uc.runtime.block_on(async {
                Pipe0::create(
                    rc.ump_clone(),
                    "decim source",
                    DecimSource::generate,
                    decim_source_state,
                    None,
                    None,
                )
            });

            let decim_out = uc.runtime.block_on(async {
                let params = DecimationParameters {
                    filter: Default::default(),
                    num_decs: 1,
                };
                Decimate::<f64>::create(rc.ump_clone(), "decim".to_string(), &params, &src_out)
                    .await
                    .unwrap()
                    .subscribe_or_die(rc.ump_clone())
                    .await
            });

            decim_out
        };
        let out = uc.runtime.block_on(async move {
            let mut output = vec![0.0, 0.0];
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting decimated data.");
                      },
                    res =  decim_out.recv() => match res {
                        Some(value) => {
                            let out_data = &value.value.data;
                            if out_data.len() >= 2 {
                                let start = out_data.len() - 2;
                                output = out_data[start..start+2].to_vec();
                            }
                            else {
                                let start = out_data.len();
                                output.drain(..start);
                                output.extend_from_slice(out_data);
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
            output
        });

        // taken from gds-sigp decimation tests
        const target_out: [f64; 2] = [0.0020601588869841349, 0.00057130068110256699];
        assert_eq!(out, target_out);
    }

    #[test]
    fn decim_pipeline_odd_f64() {
        let (uc, mut or, rc) = start_runtime();
        let decim_source_state = DecimSource {
            max_iters: 3,
            iter_count: 0,
            chunk_size: 3,
            rate_hz: 16.0,
            index: 0,
            template: vec![1.0, -1.0, 1.5, -1.0],
            segment: 0,
        };

        let mut decim_out = {
            let src_out = uc.runtime.block_on(async {
                Pipe0::create(
                    rc.ump_clone(),
                    "decim source",
                    DecimSource::generate,
                    decim_source_state,
                    None,
                    None,
                )
            });

            let decim_out = uc.runtime.block_on(async {
                let params = DecimationParameters {
                    filter: Default::default(),
                    num_decs: 1,
                };
                Decimate::<f64>::create(rc.ump_clone(), "decim".to_string(), &params, &src_out)
                    .await
                    .unwrap()
                    .subscribe_or_die(rc.ump_clone())
                    .await
            });

            decim_out
        };
        let out = uc.runtime.block_on(async move {
            let mut output = vec![0.0, 0.0];
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting decimated data.");
                      },

                    res =  decim_out.recv() => match res {
                        Some(value) => {
                            let out_data = &value.value.data;
                            if out_data.len() >= 2 {
                                let start = out_data.len() - 2;
                                output = out_data[start..start+2].to_vec();
                            }
                            else {
                                let start = out_data.len();
                                output.drain(..start);
                                output.extend_from_slice(out_data);
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
            output
        });

        // taken from gds-sigp decimation tests
        const target_out: [f64; 2] = [0.0020601588869841349, 0.00057130068110256699];
        assert_eq!(out, target_out);
    }

    #[test]
    fn decim_pipeline_bigchunk_f64() {
        let (uc, mut or, rc) = start_runtime();
        let decim_source_state = DecimSource {
            max_iters: 3,
            iter_count: 0,
            chunk_size: 5,
            rate_hz: 16.0,
            index: 0,
            template: vec![1.0, -1.0, 1.5, -1.0],
            segment: 0,
        };

        let mut decim_out = {
            let src_out = uc.runtime.block_on(async {
                Pipe0::create(
                    rc.ump_clone(),
                    "decim source",
                    DecimSource::generate,
                    decim_source_state,
                    None,
                    None,
                )
            });

            let decim_out = uc.runtime.block_on(async {
                let params = DecimationParameters {
                    filter: Default::default(),
                    num_decs: 1,
                };
                Decimate::<f64>::create(rc.ump_clone(), "decim".to_string(), &params, &src_out)
                    .await
                    .unwrap()
                    .subscribe_or_die(rc.ump_clone())
                    .await
            });

            decim_out
        };
        let out = uc.runtime.block_on(async move {
            let mut output = vec![0.0, 0.0];
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting decimated data.");
                      },
                    res =  decim_out.recv() => match res {
                        Some(value) => {
                            let out_data = &value.value.data;
                            if out_data.len() >= 2 {
                                let start = out_data.len() - 2;
                                output = out_data[start..start+2].to_vec();
                            }
                            else {
                                let start = out_data.len();
                                output.drain(..start);
                                output.extend_from_slice(out_data);
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
            output
        });

        // taken from gds-sigp decimation tests
        const target_out: [f64; 2] = [0.0020601588869841349, 0.00057130068110256699];
        assert_eq!(out, target_out);
    }

    #[test]
    fn decim_pipeline_c128() {
        let (uc, mut or, rc) = start_runtime();
        let template = vec![
            c128::new(1.0, -1.0),
            c128::new(-1.0, 1.0),
            c128::new(1.5, -1.5),
            c128::new(-1.0, 1.0),
        ];

        let decim_source_state = DecimSource {
            max_iters: 3,
            iter_count: 0,
            chunk_size: 4,
            rate_hz: 16.0,
            index: 0,
            template,
            segment: 0,
        };

        let mut decim_out = {
            let src_out = uc.runtime.block_on(async {
                Pipe0::create(
                    rc.ump_clone(),
                    "decim source",
                    DecimSource::generate,
                    decim_source_state,
                    None,
                    None,
                )
            });

            let decim_out = uc.runtime.block_on(async {
                let params = DecimationParameters {
                    filter: Default::default(),
                    num_decs: 1,
                };
                Decimate::<c128>::create(rc.ump_clone(), "decim".to_string(), &params, &src_out)
                    .await
                    .unwrap()
                    .subscribe_or_die(rc.ump_clone())
                    .await
            });

            decim_out
        };
        let out = uc.runtime.block_on(async move {
            let mut output = vec![c128::default(), c128::default()];
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting decimated data.");
                      },
                    res =  decim_out.recv() => match res {
                        Some(value) => {
                            let out_data = &value.value.data;
                            if out_data.len() >= 2 {
                                let start = out_data.len() - 2;
                                output = out_data[start..start+2].to_vec();
                            }
                            else {
                                let start = out_data.len();
                                output.drain(..start);
                                output.extend_from_slice(out_data);
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
            output
        });

        // taken from gds-sigp decimation tests
        const target_out: [c128; 2] = [
            c128::new(0.0020601588869841349, -0.0020601588869841349),
            c128::new(0.00057130068110256699, -0.00057130068110256699),
        ];
        assert_eq!(out, target_out);
    }
}

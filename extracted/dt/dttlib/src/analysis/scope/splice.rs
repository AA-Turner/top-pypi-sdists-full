//! splice incoming data to fit a window.  The data can come in multiple, disparate chunks.
//! Output needs to be a single slice of data
//! This can either be through taking contiguous data, or by filling gaps.

use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use futures::future::FutureExt;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use pipeline_macros::box_async;
use pipelines::pipe::Pipe1;
use pipelines::{PipeData, PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

/// How to handle gaps
#[allow(dead_code)]
pub(crate) enum SpliceMode<T: PipeData + Copy> {
    /// fill gaps with the specified value
    FillGaps(T),
    ContiguousLatest,
    ContiguousOldest,
    ContiguousLongest,
}

pub struct SplicePipeline<T: PipeData + Copy> {
    splice_mode: SpliceMode<T>,
    window_size_pip: PipDuration,
    window_start_pip: PipInstant,

    /// If online, then when new data comes in that's later than the window, shift the window.
    online: bool,

    /// Maintain a collection of previous data that fits the window.
    data: Vec<TimeDomainArray<T>>,
}

impl<T: PipeDataPrimitive + Copy> SplicePipeline<T> {
    #[box_async]
    fn generate(
        rc: Box<dyn UserMsgProvider>,
        state: &mut Self,
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        // advance window if online
        let window_end_pip = state.window_start_pip + state.window_size_pip;
        if state.online && input.end_gps_pip() > window_end_pip {
            // good assumption that end_gps_pip is aligned to step size
            state.window_start_pip = input.end_gps_pip() - state.window_size_pip;

            while !state.data.is_empty() && state.data[0].start_gps_pip < state.window_start_pip {
                if state.data[0].end_gps_pip() < state.window_start_pip {
                    state.data.remove(0);
                } else if state.data[0]
                    .trim_to(rc.ump_clone(), state.window_start_pip)
                    .is_err()
                {
                    return PipeResult::Close;
                }
            }
        }

        let new_window_end_pip = state.window_start_pip + state.window_size_pip;

        // drop input if out of range
        if input.end_gps_pip() <= state.window_start_pip
            || input.start_gps_pip >= new_window_end_pip
        {
            return Vec::new().into();
        }

        // trim input
        let new_start_pip = input.start_gps_pip.max(state.window_start_pip);
        let new_end_pip = input.end_gps_pip().min(new_window_end_pip);
        let inp_data = input.copy_from(new_start_pip, new_end_pip);

        // splice any data into window
        let spliced = inp_data.splice_into(&mut state.data);

        // return data only if something got spliced.
        if state.data.is_empty() || !spliced {
            Vec::new().into()
        } else {
            match state.splice_mode {
                SpliceMode::FillGaps(g) => match TimeDomainArray::<T>::fill_gaps(&state.data, g) {
                    Some(out) => {
                        log::info!("SplicePipeline: FillGaps: {}", out.len());
                        vec![Arc::new(out)].into()
                    }
                    None => Vec::new().into(),
                },
                SpliceMode::ContiguousLatest => vec![Arc::new(
                    state.data.last().expect("should be non-empty").clone(),
                )]
                .into(),
                SpliceMode::ContiguousOldest => vec![Arc::new(
                    state.data.first().expect("should be non-empty").clone(),
                )]
                .into(),
                SpliceMode::ContiguousLongest => {
                    let mut longest_idx = 0;
                    let mut longest_len = 0;
                    for (idx, data) in state.data.iter().enumerate() {
                        if data.len() > longest_len {
                            longest_idx = idx;
                            longest_len = data.len();
                        }
                    }
                    vec![Arc::new(state.data[longest_idx].clone())].into()
                }
            }
        }
    }

    pub(crate) async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        start_time: PipInstant,
        length: PipDuration,
        splice_mode: SpliceMode<T>,
        online: bool,
        input: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
        let part = Self {
            splice_mode,
            window_size_pip: length,
            window_start_pip: start_time,
            online,
            data: Vec::new(),
        };

        Ok(Pipe1::create(rc, name, Self::generate, part, None, None, input).await?)
    }
}

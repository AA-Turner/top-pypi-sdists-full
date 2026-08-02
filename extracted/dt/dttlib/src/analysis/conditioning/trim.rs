//! Pipeline for trimming data from a span of time.
//!
//! Should only be used if the use_active_time flag is true, which may be only swept sine tests
//!
//! ### References
//! 1. https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L589

use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use futures::future::FutureExt;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use pipeline_macros::box_async;
use pipelines::PipelineSubscriber;
use pipelines::stateless::Stateless1;
use pipelines::{PipeDataPrimitive, PipeResult};
use std::fmt::Debug;
use std::marker::PhantomData;
use std::sync::Arc;
use user_messages::UserMsgProvider;

/// Drops inputs that
/// end before the start time or start after the end time.
///
/// Trimmer can't be a pure pipeline because pure pipelines aren't allowed to return
/// None for any input.
#[derive(Clone, Debug)]
struct Trimmer<T> {
    start_gps_pip: PipInstant,

    // if none, then the run length is indefinite and there is no end time.
    end_gps_pip: Option<PipInstant>,
    phantom_data: PhantomData<T>,
}

impl<T: PipeDataPrimitive> Trimmer<T> {
    #[box_async]
    fn generate(
        _rc: Box<dyn UserMsgProvider>,
        _name: String,
        config: &Self,
        data: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        let start_pip = data.start_gps_pip;

        let dt_pip: PipDuration = data.period_pip;

        let end_pip: PipInstant = start_pip + (dt_pip * data.data.len());

        if let Some(et) = config.end_gps_pip {
            if start_pip > et {
                return Vec::new().into();
            }
        }
        if end_pip < config.start_gps_pip {
            Vec::new().into()
        } else {
            data.into()
        }
    }
}

pub async fn create_trim<T: PipeDataPrimitive>(
    rc: Box<dyn UserMsgProvider>,
    name: String,
    start_gps_pip: PipInstant,
    end_gps_pip: Option<PipInstant>,
    input: &PipelineSubscriber<TimeDomainArray<T>>,
) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
    let trimmer = Trimmer::<T> {
        start_gps_pip,
        end_gps_pip,
        phantom_data: PhantomData::default(),
    };
    Ok(Stateless1::create(rc.ump_clone(), name, Trimmer::<T>::generate, trimmer, input).await?)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::analysis::conditioning::time_delay::tests::RampSource;
    use std::time::Duration;
    use tokio::time::sleep;
    use user_messages::{TestSender, TestUserMessageProvider, UserMsgProvider};

    const NUM_CHUNKS: u64 = 3;

    #[test]
    fn trim() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let mut sender = TestSender::default();
        let rc = Box::new(rt.block_on(TestUserMessageProvider::new(sender.clone())));

        let mut trim_out = {
            // setup ramp
            let ramp_out = rt.block_on(async {
                RampSource::create(rc.ump_clone(), "rampsource", NUM_CHUNKS, 4, 64.0)
            });

            // create trimmer
            let test_start = PipInstant::default() + PipDuration::from_seconds(5.0 / 64.0);
            let test_end = PipInstant::default() + PipDuration::from_seconds(6.0 / 64.0);
            let trimmer = rt.block_on(async {
                create_trim(
                    rc.ump_clone(),
                    "trim".to_string(),
                    test_start,
                    Some(test_end),
                    &ramp_out,
                )
                .await
                .unwrap()
                .subscribe_or_die(rc.clone())
                .await
            });
            trimmer
        };
        let out = rt.block_on(async {
            let mut out = Vec::new();
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting for trim.");
                      },
                    res =  trim_out.recv() => match res {
                        Some(value) => {
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

        /// should just get the middle of three chunks
        const target: [f64; 4] = [4.0, 5.0, 6.0, 7.0];
        assert_eq!(out, target);
    }
}

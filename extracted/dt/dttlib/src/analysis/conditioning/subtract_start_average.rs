//! A pipeline for subtracting the average of the first chunk from all chunks
//! this is taken from
//! https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L631
//!
//! Note that the original doesn't care how big the first block is.  It's assuming that the NDS
//! will always return blocks that are "big enough".  
//! This pipeline is only used when the Zoom feature is enabled on a non-complex channel, but
//! It could be that the zoom feature is never used.  I've never seen any evidence that it is used.

use crate::analysis::types::Scalar;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use futures::future::FutureExt;
use pipeline_macros::box_async;
use pipelines::pipe::Pipe1;
use pipelines::{PipeData, PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

#[derive(Clone, Debug, Default)]
pub struct SubtractStartAverage<T: PipeData> {
    first_average: Option<T>,
}

impl<T> SubtractStartAverage<T>
where
    T: PipeDataPrimitive + Scalar,
{
    #[box_async]
    fn generate(
        _rc: Box<dyn UserMsgProvider>,
        state: &mut Self,
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        let avg = match state.first_average {
            Some(a) => a,
            None => {
                let a = input.mean();
                state.first_average = Some(a);
                a
            }
        };
        (input.as_ref().clone() - avg).into()
    }

    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        input: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
        let sa = SubtractStartAverage::default();
        Ok(Pipe1::create(
            rc.ump_clone(),
            name,
            SubtractStartAverage::generate,
            sa,
            None,
            None,
            input,
        )
        .await?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::analysis::conditioning::time_delay::tests::RampSource;
    use pipelines::pipe::Pipe1;
    use std::time::Duration;
    use tokio::time::sleep;
    use user_messages::{TestSender, TestUserMessageProvider};

    #[test]
    fn test_sub_mean() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let mut sender = TestSender::default();
        let rc = Box::new(rt.block_on(TestUserMessageProvider::new(sender.clone())));

        let mut sub_out = {
            // setup ramp
            let ramp_out =
                rt.block_on(async { RampSource::create(rc.ump_clone(), "rampsource", 2, 4, 64.0) });

            // create subtracter
            let sub_state = SubtractStartAverage::<f64>::default();

            let subber = rt.block_on(async {
                Pipe1::create(
                    rc.ump_clone(),
                    "sub_mean",
                    SubtractStartAverage::<f64>::generate,
                    sub_state,
                    None,
                    None,
                    &ramp_out,
                )
                .await
                .unwrap()
                .subscribe_or_die(rc.clone())
                .await
            });
            subber
        };

        let out = rt.block_on(async {
            let mut out = Vec::new();
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                        panic!("Timeout waiting for trim.");
                      },
                    res =  sub_out.recv() => match res {
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

        const target: [f64; 8] = [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5];
        assert_eq!(out, target);
    }
}

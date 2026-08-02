//! Pure stateless pipelines can be created with only a function from output type and input type
//!

use crate::stateless::{Stateless1, Stateless2};
use crate::{PipeData, PipeResult, PipelineError, PipelineOutput, PipelineSubscriber};
use futures::FutureExt;
use futures::future::BoxFuture;
use std::sync::Arc;
use tokio::runtime::Handle;
use user_messages::{UserMsgProvider, panic_report};

/// # One input pipelines
type Pipe1GenFn<T, U> = fn(Box<dyn UserMsgProvider>, String, Arc<T>) -> Arc<U>;

#[derive(Debug, Clone)]
pub struct PureStatelessPipeline1<T: PipeData, U: PipeData> {
    generate_ptr: Pipe1GenFn<T, U>,
}

impl<T: PipeData, U: PipeData> PureStatelessPipeline1<T, U> {
    fn generate(
        rc: Box<dyn UserMsgProvider>,
        name: String,
        config: &'_ Self,
        input: PipelineOutput<T>,
    ) -> BoxFuture<'_, PipeResult<U>> {
        async move {
            let g = config.generate_ptr;
            let inp = input.clone();
            let rc2 = rc.ump_clone();
            let jh = Handle::current().spawn_blocking(move || g(rc, name, inp.value));
            let value = match jh.await {
                Ok(r) => r,
                Err(e) => panic_report!(
                    rc2.user_message_handle(),
                    "Error in 'pure' pipeline calculation function: {}",
                    e
                ),
            };
            vec![value].into()
        }
        .boxed()
    }

    pub async fn start(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        input: &PipelineSubscriber<T>,
        generate: Pipe1GenFn<T, U>,
    ) -> Result<PipelineSubscriber<U>, PipelineError> {
        let config = PureStatelessPipeline1 {
            generate_ptr: generate,
        };
        Stateless1::create(rc, name.into(), Self::generate, config, input).await
    }
}

/// # Two input pipelines
type Pipe2GenFn<T, S, U> = fn(Box<dyn UserMsgProvider>, String, Arc<T>, Arc<S>) -> Arc<U>;

#[derive(Clone, Debug)]
pub struct PureStatelessPipeline2<T: PipeData, S: PipeData, U: PipeData> {
    generate_ptr: Pipe2GenFn<T, S, U>,
}

impl<T: PipeData, S: PipeData, U: PipeData> PureStatelessPipeline2<T, S, U> {
    fn generate(
        rc: Box<dyn UserMsgProvider>,
        name: String,
        config: &'_ Self,
        input1: PipelineOutput<T>,
        input2: PipelineOutput<S>,
    ) -> BoxFuture<'_, PipeResult<U>> {
        async move {
            let g = config.generate_ptr;
            let inp1 = input1.clone();
            let inp2 = input2.clone();
            let rc2 = rc.ump_clone();
            let jh = Handle::current().spawn_blocking(move || g(rc, name, inp1.value, inp2.value));
            let value = match jh.await {
                Ok(v) => v,
                Err(e) => panic_report!(
                    rc2.user_message_handle(),
                    "Error running calculation function for pure pipeline: {}",
                    e
                ),
            };
            value.into()
        }
        .boxed()
    }

    pub async fn start(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        input1: &PipelineSubscriber<T>,
        input2: &PipelineSubscriber<S>,
        generate: Pipe2GenFn<T, S, U>,
    ) -> Result<PipelineSubscriber<U>, PipelineError> {
        let config = PureStatelessPipeline2 {
            generate_ptr: generate,
        };
        Stateless2::create(rc, name.into(), Self::generate, config, input1, input2).await
    }
}

#[cfg(test)]
mod tests {
    use std::time::Duration;

    use pipeline_macros::box_async;
    use tokio::time::sleep;
    use user_messages::TestUserMessageProvider;

    use crate::pipe::Pipe0;

    use super::*;

    #[derive(Clone, Debug)]
    struct ConstantData {
        value: f64,
        count: usize,
        max_count: usize,
    }

    impl ConstantData {
        fn start(
            rc: Box<dyn UserMsgProvider>,
            value: f64,
            max_count: usize,
        ) -> PipelineSubscriber<f64> {
            let ds = Self {
                value,
                max_count,
                count: 0,
            };

            Pipe0::create(
                rc,
                "constant_data_source".to_string(),
                Self::generate,
                ds,
                None,
                None,
            )
        }

        #[box_async]
        fn generate(_rc: Box<dyn UserMsgProvider>, state: &'_ mut Self) -> PipeResult<f64> {
            if state.count < state.max_count {
                state.count += 1;
                Arc::new(state.value).into()
            } else {
                PipeResult::Close
            }
        }
    }

    #[test]
    fn test_input_correctness() {
        let rt = tokio::runtime::Runtime::new().expect("could not crate tokio runttime");
        let rc = Box::new(rt.block_on(TestUserMessageProvider::default()));
        let mut dif_out = {
            let (ds1, ds2) = rt.block_on(async {
                let ds1 = ConstantData::start(rc.clone(), 1.0, 1);
                let ds2 = ConstantData::start(rc.clone(), 2.0, 1);
                (ds1, ds2)
            });

            let ps2 = rt
                .block_on(PureStatelessPipeline2::start(
                    rc.clone(),
                    "pure_stateless_2",
                    &ds2,
                    &ds1,
                    |_rc, _name, a, b| {
                        let c = *a - *b;
                        Arc::new(c)
                    },
                ))
                .unwrap();

            rt.block_on(ps2.subscribe_or_die(rc))
        };

        // collect output
        let mut result = Vec::new();
        result = rt.block_on(async {
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                      panic!("Timed out waiting for pipelines to finish");
                    },
                    res = dif_out.recv() => match res {
                        Some(value) => {
                            let f = *value.value.as_ref();
                            result.push(f);
                        },
                        None => break,
                    }
                }
            }
            result
        });

        assert!(result.len() == 1);
        assert!(result[0] > 0.0);
    }
}

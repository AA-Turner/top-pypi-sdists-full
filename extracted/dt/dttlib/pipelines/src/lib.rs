//! Pipelines
pub mod accumulator;
pub mod complex;
pub mod pipe;
pub mod publisher;
pub mod stateless;
pub mod unsynced_pipe;

pub mod python;

use crate::publisher::{MaybeInitialized, Publisher, Subscriber};
use num_complex::Complex;
#[cfg(feature = "python")]
use numpy::Element;
#[cfg(feature = "python")]
use pyo3::{FromPyObject, IntoPyObject};
use std::fmt::Debug;
use std::sync::Arc;
use thiserror::Error;
use tokio::sync::{mpsc, watch};

#[cfg(feature = "python")]
pub trait PipeData:
    Debug + Sync + Send + Clone + for<'py> IntoPyObject<'py> + for<'py> FromPyObject<'py> + 'static
{
}

#[cfg(feature = "python")]
pub trait PipeDataPrimitive: PipeData + Element {}

#[cfg(not(feature = "python"))]
pub trait PipeData: Debug + Sync + Send + Clone + 'static {}
#[cfg(not(feature = "python"))]
pub trait PipeDataPrimitive: PipeData {}

/// PipeData can't be blanket applied to types
/// without forgoing nice handling of Result and Option types
/// converting to PipeOutput
impl PipeData for i64 {}
impl PipeData for i32 {}
impl PipeData for i16 {}
impl PipeData for i8 {}
impl PipeData for f64 {}
impl PipeData for f32 {}
impl PipeData for Complex<f32> {}
impl PipeData for Complex<f64> {}

impl PipeData for u8 {}
impl PipeData for u16 {}
impl PipeData for u32 {}
impl PipeData for u64 {}

impl PipeData for String {}

impl PipeDataPrimitive for i64 {}
impl PipeDataPrimitive for i32 {}
impl PipeDataPrimitive for i16 {}
impl PipeDataPrimitive for i8 {}
impl PipeDataPrimitive for f64 {}
impl PipeDataPrimitive for f32 {}
impl PipeDataPrimitive for Complex<f32> {}
impl PipeDataPrimitive for Complex<f64> {}

impl PipeDataPrimitive for u8 {}
impl PipeDataPrimitive for u16 {}
impl PipeDataPrimitive for u32 {}
impl PipeDataPrimitive for u64 {}

impl<T: PipeData, U: PipeData> PipeData for (T, U) {}

pub trait StateData: Sync + Send + 'static {}
pub trait ConfigData: Sync + Send + Clone + 'static {}

/// # Useful to have basic numeric types as PipeData
impl<T: Sync + Send + 'static> StateData for T {}
impl<T: Sync + Send + Clone + 'static> ConfigData for T {}

/// Data passed out of o pipeline
#[derive(Clone, Debug)]
pub struct PipelineOutput<T: PipeData> {
    //pub segment: u64,
    pub value: Arc<T>,
}

impl<T: PipeData> From<PipelineOutput<T>> for Arc<T> {
    fn from(value: PipelineOutput<T>) -> Self {
        value.value
    }
}

///  # shorthand for types that can be converted from PipelineOutput
pub trait PipeOut<T: PipeData>: From<PipelineOutput<T>> + Sync + Send + 'static {}

impl<T: PipeData> PipeOut<T> for Arc<T> {}

impl<T: PipeData> PipeOut<T> for PipelineOutput<T> {}

/// Tokio sender for pipeline data
type PipelineSender<T> = Publisher<PipelineOutput<T>>;

/// Tokio Receiver for pipeline data
type PipelineReceiver<T> = mpsc::Receiver<PipelineOutput<T>>;

type PipelineWatchReceiver<T> = watch::Receiver<MaybeInitialized<PipelineOutput<T>>>;

pub type PipelineSubscriber<T> = Subscriber<PipelineOutput<T>>;

/// number of values to keep in the pipeline before we stall the producer
const PIPELINE_SIZE: usize = 1;

#[derive(Error, Debug, Clone)]
pub enum PipelineError {
    #[error("Bad Argument in {0}: {1} {2}")]
    BadArgument(&'static str, &'static str, &'static str),
    #[error("Subscription failed")]
    Subscription(&'static str),
}

pub(crate) trait PipelineBase: Send + Sync + 'static {
    type Output: PipeData;

    // /// Mutable state that's passed by ref
    // /// to each call to generate
    // type State: StateData;
    //
    // /// Immutable configuration that's past to each call to generate
    // type Config: ConfigData;

    fn name(&self) -> &str;
}

/// Possible return values for a pipeline generate function
#[derive(Debug)]
pub enum PipeResult<T: PipeData> {
    /// Pipeline should output value of type T, but pass it the same input again.
    /// This allows a pipeline to generate multiple inputs from the same output
    Output(Vec<PipelineOutput<T>>),

    /// Stream is  finished.  Pipeline should close.
    Close,
}

impl<T: PipeData> From<Vec<Arc<T>>> for PipeResult<T> {
    fn from(values: Vec<Arc<T>>) -> Self {
        PipeResult::Output(
            values
                .into_iter()
                .map(|value| PipelineOutput { value })
                .collect(),
        )
    }
}

impl<T: PipeData> From<Arc<T>> for PipeResult<T> {
    fn from(value: Arc<T>) -> Self {
        vec![value].into()
    }
}

impl<T: PipeData, S: Into<Self>> From<Option<S>> for PipeResult<T> {
    fn from(value: Option<S>) -> Self {
        match value {
            Some(v) => v.into(),
            None => Vec::new().into(),
        }
    }
}

impl<T: PipeData, S: Into<Self>, E> From<Result<S, E>> for PipeResult<T> {
    fn from(value: Result<S, E>) -> Self {
        match value {
            Ok(v) => v.into(),
            Err(_) => PipeResult::Close,
        }
    }
}

impl<T: PipeData> From<T> for PipeResult<T> {
    fn from(value: T) -> Self {
        Arc::new(value).into()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::accumulator::Accumulator;
    use crate::pipe::Pipe0;
    use crate::stateless::pure::{PureStatelessPipeline1, PureStatelessPipeline2};
    use futures::future::FutureExt;
    use num_traits::FromPrimitive;
    use pipeline_macros::box_async;
    use std::time::Duration;
    use tokio::time::sleep;
    use user_messages::{TestSender, TestUserMessageProvider, UserMsgProvider};

    #[derive(Clone, Debug)]
    pub(crate) struct DataSource {
        value: f64,
        max_count: u64,
        count: u64,
    }

    impl DataSource {
        #[box_async]
        fn generate(_rc: Box<dyn UserMsgProvider>, state: &'_ mut Self) -> PipeResult<f64> {
            if state.count < state.max_count {
                let x = state.value * state.count as f64;
                state.count += 1;
                Arc::new(x).into()
            } else {
                PipeResult::Close
            }
        }

        pub(crate) fn create(value: f64, max_count: u64) -> Self {
            DataSource {
                value,
                max_count,
                count: 0,
            }
        }

        #[cfg(feature = "python")]
        pub(crate) fn start(
            rc: Box<dyn UserMsgProvider>,
            value: f64,
            max_count: u64,
        ) -> PipelineSubscriber<f64> {
            let ds = Self::create(value, max_count);

            Pipe0::create(
                rc,
                "data_source".to_string(),
                Self::generate,
                ds,
                None,
                None,
            )
        }
    }

    #[test]
    fn pipeline_0() {
        let rt = tokio::runtime::Runtime::new().expect("could not crate tokio runttime");
        let rc = Box::new(rt.block_on(TestUserMessageProvider::default()));

        let src_state = DataSource::create(NEAR_PI, 3);

        let _pr = rt.block_on(async {
            Pipe0::create(
                rc.ump_clone(),
                "src",
                DataSource::generate,
                src_state,
                None,
                None,
            )
        });
    }

    const SEGMENT_COUNT: u64 = 10;
    const NEAR_PI: f64 = std::f64::consts::PI;

    #[derive(Debug, Clone)]
    pub struct PipelineError(String);

    impl<T> From<T> for PipelineError
    where
        T: Into<String>,
    {
        fn from(value: T) -> Self {
            Self(value.into())
        }
    }

    #[test]
    fn run_pipelines_fast() {
        let rt = tokio::runtime::Runtime::new().expect("could not crate tokio runttime");
        let rc = Box::new(rt.block_on(TestUserMessageProvider::default()));

        let src_state = DataSource::create(NEAR_PI, SEGMENT_COUNT);

        let mut sum_out = {
            let pr = rt.block_on(async {
                Pipe0::create(
                    rc.ump_clone(),
                    "src",
                    DataSource::generate,
                    src_state,
                    None,
                    None,
                )
            });
            // start square of pi output
            let sqr_out = rt
                .block_on(async {
                    PureStatelessPipeline1::start(
                        rc.clone(),
                        "Square".to_string(),
                        &pr,
                        |_rc: Box<dyn UserMsgProvider>, _name: String, input: Arc<f64>| {
                            Arc::new(input.as_ref() * input.as_ref())
                        },
                    )
                    .await
                })
                .unwrap();

            // start adder
            let adder_out = rt
                .block_on(async {
                    PureStatelessPipeline2::start(
                        rc.clone(),
                        "Add".to_string(),
                        &pr,
                        &sqr_out,
                        |_rc: Box<dyn UserMsgProvider>,
                         _name: String,
                         input1: Arc<f64>,
                         input2: Arc<f64>| {
                            Arc::new(input1.as_ref() + input2.as_ref())
                        },
                    )
                    .await
                })
                .unwrap();

            let sum_out = rt.block_on(async {
                Accumulator::start(
                    rc.clone(),
                    "Sum".to_string(),
                    &adder_out,
                    |_rc: Box<dyn UserMsgProvider>,
                     input: Arc<f64>,
                     sum: Option<Arc<f64>>,
                     _n: f64| {
                        let r = Arc::new(match sum {
                            None => *input.as_ref(),
                            Some(v) => input.as_ref() + v.as_ref(),
                        });
                        (r.clone(), 1.0, r.into())
                    },
                )
                .await
                .unwrap()
                .subscribe_or_die(rc.clone())
                .await
            });
            sum_out
        };

        // collect output
        let mut result = Vec::new();
        result = rt.block_on(async {
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(2)) => {
                      panic!("Timed out waiting for pipelines to finish");
                    },
                    res = sum_out.recv() => match res {
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

        // check results
        assert_eq!(u64::from_usize(result.len()).unwrap(), SEGMENT_COUNT);
        let mut test_sum = 0.0;
        for i in 0..usize::from_u64(SEGMENT_COUNT).unwrap() {
            let x = NEAR_PI * f64::from_usize(i).unwrap();
            test_sum += x + x * x;
            assert_eq!(test_sum, result[i]);
        }
    }

    #[test]
    fn run_pipelines_with_backpressure() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let mut sender = TestSender::default();
        let rc = Box::new(rt.block_on(TestUserMessageProvider::new(sender.clone())));

        let src_state = DataSource::create(NEAR_PI, SEGMENT_COUNT);

        let mut sum_out = {
            let pr = rt.block_on(async {
                Pipe0::create(
                    rc.ump_clone(),
                    "src",
                    DataSource::generate,
                    src_state,
                    None,
                    None,
                )
            });

            // start square of pi output
            let sqr_out = rt
                .block_on(async {
                    PureStatelessPipeline1::start(
                        rc.clone(),
                        "Square".to_string(),
                        &pr,
                        |_rc: Box<dyn UserMsgProvider>, _name: String, input: Arc<f64>| {
                            Arc::new(input.as_ref() * input.as_ref())
                        },
                    )
                    .await
                })
                .unwrap();

            // start adder
            // sleep for 1 second each cycle to build up back pressure
            let adder_out = rt
                .block_on(async {
                    PureStatelessPipeline2::start(
                        rc.clone(),
                        "Add".to_string(),
                        &pr,
                        &sqr_out,
                        |_rc: Box<dyn UserMsgProvider>,
                         _name: String,
                         input1: Arc<f64>,
                         input2: Arc<f64>| {
                            std::thread::sleep(Duration::from_millis(100));
                            Arc::new(input1.as_ref() + input2.as_ref())
                        },
                    )
                    .await
                })
                .unwrap();

            let sum_out = rt.block_on(async {
                Accumulator::start(
                    rc.clone(),
                    "Sum".to_string(),
                    &adder_out,
                    |_rc: Box<dyn UserMsgProvider>,
                     input: Arc<f64>,
                     sum: Option<Arc<f64>>,
                     _n: f64| {
                        let r = Arc::new(match sum {
                            None => *input.as_ref(),
                            Some(v) => input.as_ref() + v.as_ref(),
                        });
                        (r.clone(), 1.0, r.into())
                    },
                )
                .await
                .unwrap()
                .subscribe_or_die(rc.clone())
                .await
            });
            sum_out
        };

        // collect results
        let mut result = Vec::new();
        result = rt.block_on(async {
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_secs(20)) => {
                      panic!("Timed out waiting for pipelines to finish");
                    },
                    res = sum_out.recv() => match res {
                        Some(value) => {
                            let f = *value.value.as_ref();
                            result.push(f);
                        },
                        None => break,
                    },
                    mh = sender.wait_first() => {

                                      println!("{:?}", mh);
                    },
                }
            }
            result
        });

        // check results
        assert_eq!(u64::from_usize(result.len()).unwrap(), SEGMENT_COUNT);
        let mut test_sum = 0.0;
        for i in 0..usize::from_u64(SEGMENT_COUNT).unwrap() {
            let x = NEAR_PI * f64::from_usize(i).unwrap();
            test_sum += x + x * x;
            assert_eq!(test_sum, result[i]);
        }
    }
}

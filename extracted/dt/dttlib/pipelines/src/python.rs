//! A pipe that runs a python function as a generator
#![cfg(feature = "python")]

use crate::pipe::Pipe1;
use crate::{PipeData, PipeResult, PipelineError, PipelineSubscriber};
use futures::FutureExt;
use pipeline_macros::box_async;
use pyo3::prelude::*;
use std::sync::Arc;
use user_messages::{UserMsgProvider, panic_report};

pub struct PythonPipeState {
    python_fn: Py<PyAny>,
}

impl PythonPipeState {
    #[box_async]
    fn generate<'a, T: PipeData, U: PipeData>(
        rc: Box<dyn UserMsgProvider>,
        state: &mut PythonPipeState,
        input: Arc<T>,
    ) -> PipeResult<U> {
        Python::with_gil(|py| {
            let kwargs = pyo3::types::PyDict::new(py);
            match kwargs.set_item("input", input.as_ref().clone()) {
                Ok(_) => (),
                Err(e) => {
                    // ok to panic here.  Doing so merely crashes the pipeline, which we need to do anyway
                    panic_report!(
                        rc.user_message_handle(),
                        "Error while binding input value to custom python pipeline: {}",
                        e.to_string()
                    );
                }
            };

            let py_val = match state.python_fn.call(py, (), Some(&kwargs)) {
                Ok(p) => p,
                Err(e) => panic_report!(
                    rc.user_message_handle(),
                    "Custom python pipeline function returned an error: {}",
                    e
                ),
            };
            let rv: U = match py_val.extract(py) {
                Ok(u) => u,
                Err(e) => panic_report!(
                    rc.user_message_handle(),
                    "Error extracting output value from custom python pipeline: {}",
                    e
                ),
            };
            rv.into()
        })
    }

    pub async fn create<T, U>(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        py_module: &Py<PyModule>,
        input: &PipelineSubscriber<T>,
    ) -> Result<PipelineSubscriber<U>, PipelineError>
    where
        T: PipeData,
        U: PipeData,
    {
        let rc2 = rc.ump_clone();
        let pyfun: Py<PyAny> = Python::with_gil(|py| {
            match py_module.bind(py).getattr("dtt_generate") {
                Ok(p) => p,
                Err(e) => panic_report!(
                    rc2.user_message_handle(),
                    "failed to bind python function 'dtt_generate' in custom python pipeline: {}",
                    e
                ),
            }
            .into()
        });

        let state = PythonPipeState { python_fn: pyfun };

        Pipe1::create(
            rc,
            name.into(),
            PythonPipeState::generate,
            state,
            None,
            None,
            input,
        )
        .await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::PipelineOutput;
    use crate::tests::DataSource;
    use std::ffi::CString;
    use std::time::Duration;
    use user_messages::TestUserMessageProvider;

    const SEGMENT_COUNT: u64 = 10;
    const NEAR_PI: f64 = std::f64::consts::PI;

    #[test]
    fn python_pipe_test() {
        let rt = tokio::runtime::Runtime::new().expect("could not crate tokio runttime");
        let rc = Box::new(rt.block_on(TestUserMessageProvider::default()));

        pyo3::prepare_freethreaded_python();

        let py_module = Python::with_gil(|py| {
            PyModule::from_code(
                py,
                CString::new("def dtt_generate(input): return input * input")
                    .expect("could not create C string")
                    .as_ref(),
                CString::new("")
                    .expect("could not create C string")
                    .as_ref(),
                CString::new("")
                    .expect("could not create C string")
                    .as_ref(),
            )
            .expect("could not create python module from code")
            .unbind()
        });

        let mut py_out = {
            let pr =
                rt.block_on(async { DataSource::start(rc.ump_clone(), NEAR_PI, SEGMENT_COUNT) });

            rt.block_on(async {
                PythonPipeState::create::<f64, f64>(rc.ump_clone(), "python_pipe", &py_module, &pr)
                    .await
                    .unwrap()
                    .subscribe_or_die(rc.ump_clone())
                    .await
            })
        };

        let mut result: Vec<f64> = Vec::new();

        rt.block_on(async {
            loop {
                tokio::select! {
                    _ = tokio::time::sleep(Duration::from_secs(2)) => {
                        panic!("ran out of time waiting for python pipeline to finish")
                    },
                    m = py_out.recv() => {
                        match m {
                            Some(PipelineOutput{value: v}) => {
                                result.push(*v.as_ref());
                            },
                            None => break,
                        }
                    },
                }
            }
        });

        let target: Vec<f64> = (0..SEGMENT_COUNT)
            .map(|i| {
                let x = i as f64 * NEAR_PI;
                x * x
            })
            .collect();

        assert_eq!(target, result);
    }
}

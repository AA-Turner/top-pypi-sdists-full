//! parameters for setting up custom python analysis pipelines
#![cfg(feature = "python-pipe")]
use crate::analysis::result::EdgeDataType;
use crate::errors::DTTError;
use pyo3::types::PyModule;
use pyo3::{Py, pyclass};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;
use std::collections::HashMap;
use std::sync::Arc;
use user_messages::{UserMessagesHandle, UserMsgProvider};

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[pyclass]
#[derive(Clone, Debug)]
pub struct CustomPipeline {
    pub(crate) name: String,
    pub inputs: Vec<String>,
    pub py_module: Arc<Py<PyModule>>,

    /// this should properly return CustomFreqDomainXXXX or TimeDomainXXXX
    pub determine_result_type: Option<fn(&Vec<EdgeDataType>) -> EdgeDataType>,
}

impl CustomPipeline {
    pub fn new(name: impl Into<String>, inputs: &[String], py_module: Py<PyModule>) -> Self {
        Self {
            name: name.into(),
            inputs: inputs.to_vec(),
            py_module: Arc::new(py_module),
            determine_result_type: None,
        }
    }
}

impl CustomPipeline {
    pub fn determine_result_type(&self, input_types: &Vec<EdgeDataType>) -> EdgeDataType {
        match self.determine_result_type {
            None => Self::default_determine_result_type(input_types),
            Some(m) => m(input_types),
        }
    }

    fn default_determine_result_type(input_types: &Vec<EdgeDataType>) -> EdgeDataType {
        input_types[0].clone()
    }

    pub fn port_count(&self) -> usize {
        self.inputs.len()
    }
}

#[derive(Clone)]
enum Marks {
    Sourced,
    NotVisited(Vec<String>),
    #[allow(dead_code)]
    Visited,
}

/// Each pipeline name must be unique and there must not be a cyclic dependency
/// Also, each pipeline must have at least one source
pub fn check_constraints(
    rc: Box<dyn UserMsgProvider>,
    pipes: &[CustomPipeline],
    sources: &[String],
) -> Result<(), DTTError> {
    let mut marks = HashMap::new();

    let um = rc.user_message_handle().clone();

    for source in sources {
        if marks.contains_key(source) {
            let msg = format!(
                "Duplicate pipeline name in analysis [{}].  All pipelines must have unique names",
                source
            );
            um.set_error("CustomPipelineError", msg);
            return Err(DTTError::UnsatisfiedConstraint);
        }
        marks.insert(source, Marks::Sourced);
    }

    for pipe in pipes {
        if marks.contains_key(&pipe.name) {
            let msg = format!(
                "Duplicate pipeline name in analysis [{}].  All pipelines must have unique names",
                pipe.name
            );
            um.set_error("CustomPipelineError", msg);
            return Err(DTTError::UnsatisfiedConstraint);
        }

        if pipe.inputs.len() == 0 {
            let msg = format!(
                "Pipeline {} had no inputs.  Each custom pipeline must have at least 1 input",
                &pipe.name
            );
            um.set_error("CustomPipelineError", msg);
            return Err(DTTError::UnsatisfiedConstraint);
        }

        marks.insert(&pipe.name, Marks::NotVisited(pipe.inputs.clone()));
    }

    for pipe in pipes {
        match marks.get(&pipe.name).map(|x| x.clone()) {
            Some(Marks::Sourced) => (),
            Some(Marks::Visited) => {
                return Err(DTTError::AnalysisPipelineError(format!(
                    "pipe '{}' was visited twice in custom pipe check",
                    pipe.name
                )));
            }
            Some(Marks::NotVisited(i)) => visit(um.clone(), &mut marks, &pipe.name, i.clone())?,
            None => {
                return Err(DTTError::AnalysisPipelineError(format!(
                    "pipe '{}' not found in marks container",
                    pipe.name
                )));
            }
        }
    }

    um.clear_message("CustomPipelineError");
    Ok(())
}

fn visit(
    um: UserMessagesHandle,
    marks: &mut HashMap<&String, Marks>,
    name: &String,
    inputs: Vec<String>,
) -> Result<(), DTTError> {
    for input in inputs {
        match marks.get(&input) {
            Some(Marks::Sourced) => (),
            Some(Marks::Visited) => {
                let msg = format!(
                    "Circular dependency detected in custom pipelines. [{}, {}] are mutually dependent.",
                    name, input
                );
                um.set_error("CustomPipelineError", msg);
                return Err(DTTError::UnsatisfiedConstraint);
            }
            Some(Marks::NotVisited(i)) => visit(um.clone(), marks, &input, i.clone())?,
            None => {
                return Err(DTTError::AnalysisPipelineError(format!(
                    "'{}' not found in marks table while visiting a node",
                    input
                )));
            }
        }
    }

    Ok(())
}

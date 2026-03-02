mod value;

use pyo3::prelude::*;

use pyo3::{
    types::PyAny,
    exceptions::PyValueError,
    PyErr,
};
use std::collections::BTreeMap;
use vrl::{
    compiler::{state::RuntimeState, Context, TargetValue, TimeZone, Program, compile},
    value::{Secrets, Value},
    diagnostic::Formatter,
};

use value::VrlValue;

#[pyclass]
#[derive(Clone)]
struct Transform {
    #[pyo3(get)]
    pub source: String,
    program: Program,
}

#[pymethods]
impl Transform {

    #[new]
    fn __new__(source: String) -> PyResult<Self> {
        let fns = vrl::stdlib::all();
        let result = compile(&source, &fns)
            .map_err(|d| {
                PyErr::new::<PyValueError, _>(
                    Formatter::new(&source, d).to_string()
                )})?;
        Ok(Self { source: source, program: result.program })
    }

    fn remap(&mut self, py: Python, data: &PyAny) -> PyResult<Py<PyAny>> {
        let vrl_value: VrlValue = data.extract()?;

        let mut target = TargetValue {
            value: vrl_value.inner,
            metadata: Value::Object(BTreeMap::new()),
            secrets: Secrets::default(),
        };

        let timezone = TimeZone::default();
        let mut state = RuntimeState::default();
        let mut ctx = Context::new(&mut target, &mut state, &timezone);

        let resolution = self.program.resolve(&mut ctx)
                                     .map_err(|e| {
                                        PyErr::new::<PyValueError, _>(
                                            format!("remap failure: {}", e))})?;

        let ret: VrlValue = VrlValue::new(resolution);

        ret.into_py_object(py)
    }
}

#[pymodule]
fn pyvrl(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Transform>()?;
    Ok(())
}

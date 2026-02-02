#[macro_export]
macro_rules! oneoff_functions {
    ($macro:ident $(,$arg:ident)* $(,)?) => {
        $macro!(
            pyreqwest_get, GET $(, $arg)*,
            pyreqwest_post, POST $(, $arg)*,
            pyreqwest_put, PUT $(, $arg)*,
            pyreqwest_patch, PATCH $(, $arg)*,
            pyreqwest_delete, DELETE $(, $arg)*,
            pyreqwest_head, HEAD $(, $arg)*,
        );
    }
}

#[macro_export]
macro_rules! impl_oneoff {
    ($($name:ident, $method:ident, $builder:ident),* $(,)?) => {
        $(#[pyfunction]
        fn $name(py: Python, url: Bound<PyAny>) -> PyResult<Py<$builder>> {
            $builder::new(py, reqwest::Method::$method.into(), url)
        })*
    }
}

#[macro_export]
macro_rules! impl_oneoff_functions {
    ($builder:ident) => {
        oneoff_functions!(impl_oneoff, $builder);
        #[pyfunction]
        fn pyreqwest_request(py: Python, method: Method, url: Bound<PyAny>) -> PyResult<Py<$builder>> {
            $builder::new(py, method, url)
        }
    };
}

#[macro_export]
macro_rules! register_oneoff {
    ($($name:ident, $method:ident, $module:ident),* $(,)?) => {
        $($module.add_function(wrap_pyfunction!($name, $module)?)?;)*
    }
}

#[macro_export]
macro_rules! register_oneoff_functions {
    ($module:ident) => {
        oneoff_functions!(register_oneoff, $module);
        $module.add_function(wrap_pyfunction!(pyreqwest_request, $module)?)?;
    };
}

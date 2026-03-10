//! Declarative PyO3 submodule definitions.
//!
//! Each submodule is a standalone `#[pymodule]` that delegates to its
//! `register()` function for populating functions and classes.

// Required for `#[pymodule]` attribute resolution inside the macro.
use pyo3::prelude::*;

macro_rules! define_submodule {
    ($name:ident) => {
        #[doc = concat!("The `", stringify!($name), "` submodule.")]
        #[pymodule]
        pub mod $name {
            use pyo3::prelude::*;

            #[pymodule_init]
            fn init(module: &Bound<'_, PyModule>) -> PyResult<()> {
                crate::python::$name::register(module)
            }
        }
    };
}

// Keep in sync with lib.rs #[pymodule_export] uses and stub_gen.rs submodules array
define_submodule!(bonding);
define_submodule!(cell);
define_submodule!(chempot);
define_submodule!(composition);
define_submodule!(convex_hull);
define_submodule!(coordination);
define_submodule!(defects);
define_submodule!(elastic);
define_submodule!(io);
define_submodule!(lattice);
define_submodule!(lmdb);
define_submodule!(md);
define_submodule!(mp);
define_submodule!(neighbors);
define_submodule!(optimizers);
define_submodule!(order_params);
define_submodule!(oxidation);
define_submodule!(potentials);
define_submodule!(properties);
define_submodule!(rdf);
define_submodule!(species);
define_submodule!(structure);
define_submodule!(surfaces);
define_submodule!(symmetry);
define_submodule!(trajectory);
define_submodule!(units);
define_submodule!(vasp);
define_submodule!(xrd);

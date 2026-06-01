use ndarray::Array2;
use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;

use rayon::prelude::*;
use rand::rngs::ChaCha8Rng;

use crate::cube2x2::Cube2x2;
use crate::cube3x3::Cube3x3;
use crate::cube::Cube;

mod pymethods;

#[derive(Clone)]
enum CubeBatchStorage {
    Cube2x2(Vec<Cube2x2>),
    Cube3x3(Vec<Cube3x3>),
}

#[pyclass(sequence)]
pub struct CubeBatch {
    cubes: CubeBatchStorage,
}

impl CubeBatchStorage {
    fn len(&self) -> usize {
        match self {
            Self::Cube2x2(cubes) => cubes.len(),
            Self::Cube3x3(cubes) => cubes.len(),
        }
    }

    fn get_py_internal(&self, py: Python<'_>, index: usize) -> PyResult<Py<PyAny>> {
        match self {
            Self::Cube2x2(cubes) => Ok(Py::new(py, cubes[index])?.into_any()),
            Self::Cube3x3(cubes) => Ok(Py::new(py, cubes[index])?.into_any()),
        }
    }
}

impl CubeBatch {
    pub(crate) fn from_count_internal(count: usize, cube_type: usize) -> PyResult<Self> {
        let cubes = match cube_type {
            2 => CubeBatchStorage::Cube2x2(vec![Cube2x2::new_solved(); count]),
            3 => CubeBatchStorage::Cube3x3(vec![Cube3x3::new_solved(); count]),
            _ => {
                return Err(PyTypeError::new_err(
                    "unknown cube type: expected 2 or 3",
                ));
            }
        };

        Ok(Self { cubes })
    }

    pub(crate) fn len_internal(&self) -> usize {
        self.cubes.len()
    }

    pub(crate) fn item_at_internal(&self, py: Python<'_>, index: usize) -> PyResult<Py<PyAny>> {
        self.cubes.get_py_internal(py, index)
    }

    pub(crate) fn apply_move_indexes_internal(&mut self, move_indexes: &[usize]) -> PyResult<()> {
        match &mut self.cubes {
            CubeBatchStorage::Cube2x2(cubes) => {
                cubes.par_iter_mut()
                    .zip(move_indexes.par_iter())
                    .for_each(|(cube, &move_index)| {
                        cube.apply_move_index_internal(move_index);
                    });
                Ok(())
            }
            CubeBatchStorage::Cube3x3(cubes) => {
                cubes.par_iter_mut()
                    .zip(move_indexes.par_iter())
                    .for_each(|(cube, &move_index)| {
                        cube.apply_move_index_internal(move_index);
                    });
                Ok(())
            }
        }
    }

    pub(crate) fn next_states_internal(&self) -> PyResult<Array2<i64>> {
        match &self.cubes {
            CubeBatchStorage::Cube2x2(cubes) => Ok(crate::cube::next_states_internal(cubes)),
            CubeBatchStorage::Cube3x3(cubes) => Ok(crate::cube::next_states_internal(cubes)),
        }
    }

    pub(crate) fn sticker_arrays_internal(&self) -> PyResult<Array2<i64>> {
        match &self.cubes {
            CubeBatchStorage::Cube2x2(cubes) => Ok(crate::cube::sticker_arrays_internal(cubes)),
            CubeBatchStorage::Cube3x3(cubes) => Ok(crate::cube::sticker_arrays_internal(cubes)),
        }
    }

    pub(crate) fn scramble_batch_internal(&mut self, scramble_lengths: &[i64]) -> PyResult<()> {
        match &mut self.cubes {
            CubeBatchStorage::Cube2x2(cubes) => {
                cubes.par_iter_mut()
                    .zip(scramble_lengths.par_iter())
                    .for_each_init(
                        || rand::make_rng::<ChaCha8Rng>(), 
                        |rng, (cube, &length)| {
                            cube.scramble_internal(length, rng);
                        }
                    );
                Ok(())
            }
            CubeBatchStorage::Cube3x3(cubes) => {
                cubes.par_iter_mut()
                    .zip(scramble_lengths.par_iter())
                    .for_each_init(
                        || rand::make_rng::<ChaCha8Rng>(), 
                        |rng, (cube, &length)| {
                            cube.scramble_internal(length, rng);
                        }
                    );
                Ok(())
            }
        }
    }
}


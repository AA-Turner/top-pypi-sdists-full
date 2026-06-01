use numpy::{IntoPyArray, PyArray2};
use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::PyList;

mod cube;
mod cube2x2;
mod cube3x3;
#[allow(non_snake_case)]
mod cubeBatch;

use crate::cube::next_states_internal;
use cube2x2::Cube2x2;
use cube3x3::Cube3x3;
use cubeBatch::CubeBatch;

/// Return the inverse of the given scramble string.
#[pyfunction]
fn inverse_scramble(scramble: &str) -> String {
    let mut inverse_moves = Vec::new();
    for move_str in scramble.split_whitespace().rev() {
        let (base_move, suffix) = if move_str.ends_with("2") {
            (&move_str[..move_str.len() - 1], "2")
        } else if move_str.ends_with("'") {
            (&move_str[..move_str.len() - 1], "'")
        } else {
            (move_str, "")
        };

        let inverse_base = match base_move {
            "U" => "U'",
            "U'" => "U",
            "R" => "R'",
            "R'" => "R",
            "F" => "F'",
            "F'" => "F",
            "D" => "D'",
            "D'" => "D",
            "L" => "L'",
            "L'" => "L",
            "B" => "B'",
            "B'" => "B",
            _ => base_move,
        };
        inverse_moves.push(format!("{}{}", inverse_base, suffix));
    }
    inverse_moves.join(" ")
}

/// Return quarter-turn successors for a batch of 2x2 or 3x3 cubes.
#[pyfunction]
fn get_next_states(py: Python<'_>, cubes: &Bound<'_, PyList>) -> PyResult<Py<PyArray2<i64>>> {
    let first = cubes
        .iter()
        .next()
        .ok_or_else(|| PyTypeError::new_err("get_next_states() requires at least one cube to infer the cube type"))?;

    if first.extract::<PyRef<'_, Cube2x2>>().is_ok() {
        let cubes: Vec<Cube2x2> = cubes
            .iter()
            .map(|item| {
                let cube: PyRef<'_, Cube2x2> = item.extract()?;
                Ok(Cube2x2 { state: cube.state })
            })
            .collect::<PyResult<Vec<_>>>()?;

        let states = next_states_internal(&cubes);
        return Ok(states.into_pyarray(py).unbind());
    }

    if first.extract::<PyRef<'_, Cube3x3>>().is_ok() {
        let cubes: Vec<Cube3x3> = cubes
            .iter()
            .map(|item| {
                let cube: PyRef<'_, Cube3x3> = item.extract()?;
                Ok(cube.state_copy_internal())
            })
            .collect::<PyResult<Vec<_>>>()?;

        let states = next_states_internal(&cubes);
        return Ok(states.into_pyarray(py).unbind());
    }

    Err(PyTypeError::new_err(
        "get_next_states() expects a list of rapidcube.Cube2x2 or rapidcube.Cube3x3 instances",
    ))
}

#[pymodule]
fn rapidcube(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CubeBatch>()?;
    m.add_class::<Cube2x2>()?;
    m.add_class::<Cube3x3>()?;
    m.add_function(wrap_pyfunction!(inverse_scramble, m)?)?;
    m.add_function(wrap_pyfunction!(get_next_states, m)?)?;
    Ok(())
}

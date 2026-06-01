use pyo3::prelude::*;

mod moves;
mod pymethods;
mod render;
mod utils;

/// A compact 2x2 Rubik's Cube model with fast move operations.
#[pyclass(skip_from_py_object)]
#[derive(Clone, Copy)]
pub struct Cube2x2 {
    #[pyo3(get)]
    pub state: u64,
}

impl Cube2x2 {
    // Internal helper without Python errors for fast access.
    fn get_corner_internal(&self, index: usize) -> (u8, u8) {
        let shift = index * 5;
        let data = (self.state >> shift) & 0b11111;
        ((data & 0b111) as u8, ((data >> 3) & 0b11) as u8)
    }

    fn add_ori(corner: u64, amount: u64) -> u64 {
        let pos = corner & 0b111;
        let ori = corner >> 3;
        let new_ori = (ori + amount) % 3;
        pos | (new_ori << 3)
    }
}

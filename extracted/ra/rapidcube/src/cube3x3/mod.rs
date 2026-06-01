use pyo3::prelude::*;

mod moves;
mod pymethods;
mod render;
mod utils;

#[pyclass(skip_from_py_object)]
#[derive(Clone, Copy)]
pub struct Cube3x3 {
    #[pyo3(get)]
    pub corners: u64,
    pub edges: u64,
}

impl Cube3x3 {
    // Internal helper without Python errors for fast access.
    fn get_corner_internal(&self, index: usize) -> (u8, u8) {
        let shift = index * 5;
        let data = (self.corners >> shift) & 0b11111;
        ((data & 0b111) as u8, ((data >> 3) & 0b11) as u8)
    }

    fn get_edge_internal(&self, index: usize) -> (u8, u8) {
        let shift = index * 5;
        let data = (self.edges >> shift) & 0b11111;
        ((data & 0b1111) as u8, ((data >> 4) & 0b1) as u8)
    }

    fn add_ori_corner(corner: u64, amount: u64) -> u64 {
        let pos = corner & 0b111;
        let ori = corner >> 3;
        let new_ori = (ori + amount) % 3;
        pos | (new_ori << 3)
    }

    fn add_ori_edge(edge: u64, amount: u64) -> u64 {
        let pos = edge & 0b1111;
        let ori = edge >> 4;
        let new_ori = (ori + amount) % 2;
        pos | (new_ori << 4)
    }

    pub(crate) fn state_copy_internal(&self) -> Self {
        Self {
            corners: self.corners,
            edges: self.edges,
        }
    }
}

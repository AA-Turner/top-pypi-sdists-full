use pyo3::prelude::*;

use crate::cube::Cube;
use super::Cube3x3;

#[pymethods]
impl Cube3x3 {
    #[new]
    /// Create a solved 3x3 cube state.
    pub fn new() -> PyResult<Self> {
        Ok(Self::new_solved())
    }

    /// Return an ANSI-colored string rendering of the cube.
    fn __str__(&self) -> String {
        Cube::render_ansi_internal(self)
    }

    /// Return the corner state as a 64-bit binary string.
    pub fn to_binary_corners(&self) -> PyResult<String> {
        Ok(self.binary_corners_string())
    }

    /// Return the edge state as a 64-bit binary string.
    pub fn to_binary_edges(&self) -> PyResult<String> {
        Ok(self.binary_edges_string())
    }

    /// Return the corner and edge states as a tuple of 64-bit binary strings.
    pub fn to_binary(&self) -> PyResult<(String, String)> {
        Ok(self.binary_state())
    }

    /// Return the corner state as an array.
    pub fn get_corners(&self) -> PyResult<Vec<(u8, u8)>> {
        Ok(Cube::corners_state_internal(self))
    }

    /// Return the edge state as an array.
    pub fn get_edges(&self) -> PyResult<Vec<(u8, u8)>> {
        Ok(self.edges_state())
    }

    /// Return the cube state as an array of 54 sticker colors.
    /// The stickers are ordered as follows: U face (9 stickers), R face (9 stickers), D face (9 stickers), L face (9 stickers), L face (9 stickers), B face (9 stickers).
    pub fn to_sticker_array(&self) -> PyResult<[usize; 54]> {
        Ok(self.to_sticker_array_internal())
    }

    /// Return true if the cube is solved.
    pub fn is_solved(&self) -> PyResult<bool> {
        Ok(Cube::is_solved_internal(self))
    }

    /// Apply the U move (clockwise top face turn).
    pub fn do_u_move(&mut self) -> PyResult<()> {
        Cube::do_u_move_internal(self);
        Ok(())
    }

    /// Apply the U' move (counterclockwise top face turn).
    pub fn do_u_prime_move(&mut self) -> PyResult<()> {
        Cube::do_u_prime_move_internal(self);
        Ok(())
    }

    /// Apply the D move (clockwise bottom face turn).
    pub fn do_d_move(&mut self) -> PyResult<()> {
        Cube::do_d_move_internal(self);
        Ok(())
    }

    /// Apply the D' move (counterclockwise bottom face turn).
    pub fn do_d_prime_move(&mut self) -> PyResult<()> {
        Cube::do_d_prime_move_internal(self);
        Ok(())
    }

    /// Apply the R move (clockwise right face turn).
    pub fn do_r_move(&mut self) -> PyResult<()> {
        Cube::do_r_move_internal(self);
        Ok(())
    }

    /// Apply the R' move (counterclockwise right face turn).
    pub fn do_r_prime_move(&mut self) -> PyResult<()> {
        Cube::do_r_prime_move_internal(self);
        Ok(())
    }

    /// Apply the L move (clockwise left face turn).
    pub fn do_l_move(&mut self) -> PyResult<()> {
        Cube::do_l_move_internal(self);
        Ok(())
    }

    /// Apply the L' move (counterclockwise left face turn).
    pub fn do_l_prime_move(&mut self) -> PyResult<()> {
        Cube::do_l_prime_move_internal(self);
        Ok(())
    }

    /// Apply the F move (clockwise front face turn).
    pub fn do_f_move(&mut self) -> PyResult<()> {
        Cube::do_f_move_internal(self);
        Ok(())
    }

    /// Apply the F' move (counterclockwise front face turn).
    pub fn do_f_prime_move(&mut self) -> PyResult<()> {
        Cube::do_f_prime_move_internal(self);
        Ok(())
    }

    /// Apply the B move (clockwise back face turn).
    pub fn do_b_move(&mut self) -> PyResult<()> {
        Cube::do_b_move_internal(self);
        Ok(())
    }

    /// Apply the B' move (counterclockwise back face turn).
    pub fn do_b_prime_move(&mut self) -> PyResult<()> {
        Cube::do_b_prime_move_internal(self);
        Ok(())
    }

    /// Apply a whitespace-separated sequence of cube moves.
    pub fn do_moves(&mut self, moves: String) -> PyResult<()> {
        Cube::do_moves_internal(self, &moves);
        Ok(())
    }

    /// Apply a random scramble of the given length.
    #[pyo3(signature = (scramble_length=20))]
    pub fn scramble(&mut self, scramble_length: i64) -> PyResult<()> {
        let mut local_rng = rand::rng();
        Cube::scramble_internal(self, scramble_length, &mut local_rng);
        Ok(())
    }
}

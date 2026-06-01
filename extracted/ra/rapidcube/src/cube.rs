use ndarray::Array2;
use rayon::prelude::*;
use rand::prelude::*;
use rand::Rng;

pub(crate) trait Cube: Sized {
    const STICKER_DIM: usize;

    fn corners_state_internal(&self) -> Vec<(u8, u8)>;
    fn is_solved_internal(&self) -> bool;
    fn render_ansi_internal(&self) -> String;
    fn state_copy_internal(&self) -> Self;
    fn sticker_array_internal(&self) -> Vec<i64>;

    fn do_u_move_internal(&mut self);
    fn do_u_prime_move_internal(&mut self);
    fn do_d_move_internal(&mut self);
    fn do_d_prime_move_internal(&mut self);
    fn do_r_move_internal(&mut self);
    fn do_r_prime_move_internal(&mut self);
    fn do_l_move_internal(&mut self);
    fn do_l_prime_move_internal(&mut self);
    fn do_f_move_internal(&mut self);
    fn do_f_prime_move_internal(&mut self);
    fn do_b_move_internal(&mut self);
    fn do_b_prime_move_internal(&mut self);

    fn do_moves_internal(&mut self, moves: &str) {
        for mv in moves.split_whitespace() {
            match mv {
                "U" => self.do_u_move_internal(),
                "U'" | "U!" => self.do_u_prime_move_internal(),
                "U2" => {
                    self.do_u_move_internal();
                    self.do_u_move_internal();
                }
                "D" => self.do_d_move_internal(),
                "D'" | "D!" => self.do_d_prime_move_internal(),
                "D2" => {
                    self.do_d_move_internal();
                    self.do_d_move_internal();
                }
                "R" => self.do_r_move_internal(),
                "R'" | "R!" => self.do_r_prime_move_internal(),
                "R2" => {
                    self.do_r_move_internal();
                    self.do_r_move_internal();
                }
                "L" => self.do_l_move_internal(),
                "L'" | "L!" => self.do_l_prime_move_internal(),
                "L2" => {
                    self.do_l_move_internal();
                    self.do_l_move_internal();
                }
                "F" => self.do_f_move_internal(),
                "F'" | "F!" => self.do_f_prime_move_internal(),
                "F2" => {
                    self.do_f_move_internal();
                    self.do_f_move_internal();
                }
                "B" => self.do_b_move_internal(),
                "B'" | "B!" => self.do_b_prime_move_internal(),
                "B2" => {
                    self.do_b_move_internal();
                    self.do_b_move_internal();
                }
                _ => continue,
            }
        }
    }

    fn apply_move_index_internal(&mut self, move_index: usize) {
        match move_index {
            0 => self.do_u_move_internal(),
            1 => self.do_u_prime_move_internal(),
            2 => self.do_d_move_internal(),
            3 => self.do_d_prime_move_internal(),
            4 => self.do_r_move_internal(),
            5 => self.do_r_prime_move_internal(),
            6 => self.do_l_move_internal(),
            7 => self.do_l_prime_move_internal(),
            8 => self.do_f_move_internal(),
            9 => self.do_f_prime_move_internal(),
            10 => self.do_b_move_internal(),
            11 => self.do_b_prime_move_internal(),
            _ => {}
        }
    }

    fn _undo_move_index_internal(&mut self, move_index: usize) {
        match move_index { 
            0 => self.do_u_prime_move_internal(),
            1 => self.do_u_move_internal(),
            2 => self.do_d_prime_move_internal(),
            3 => self.do_d_move_internal(),
            4 => self.do_r_prime_move_internal(),
            5 => self.do_r_move_internal(),
            6 => self.do_l_prime_move_internal(),
            7 => self.do_l_move_internal(),
            8 => self.do_f_prime_move_internal(),
            9 => self.do_f_move_internal(),
            10 => self.do_b_prime_move_internal(),
            11 => self.do_b_move_internal(),
            _ => {}
        }
    }

    fn scramble_internal(&mut self, scramble_length: i64, rng: &mut impl Rng) {
        for _ in 0..scramble_length {
            let move_index = rng.random_range(0..12); 
            self.apply_move_index_internal(move_index);
        }
    }
}

pub(crate) fn next_states_internal<C: Cube + Sync>(cubes: &[C]) -> Array2<i64> {
    const NUM_MOVES: usize = 12;

    let rows = cubes.len() * NUM_MOVES;
    let mut array = Array2::<i64>::zeros((rows, C::STICKER_DIM));

    array
        .as_slice_mut()
        .expect("Array2 must be contiguous")
        .par_chunks_mut(C::STICKER_DIM)
        .enumerate()
        .for_each(|(row_index, row)| {
            let cube_index = row_index / NUM_MOVES;
            let move_index = row_index % NUM_MOVES;

            let mut next_cube = cubes[cube_index].state_copy_internal();
            next_cube.apply_move_index_internal(move_index);

            let sticker_array = next_cube.sticker_array_internal();
            for (sticker_index, sticker_value) in sticker_array.iter().enumerate() {
                row[sticker_index] = *sticker_value;
            }
        });

    array
}

pub(crate) fn sticker_arrays_internal<C: Cube + Sync>(cubes: &[C]) -> Array2<i64> {
    let rows = cubes.len();
    let mut array = Array2::<i64>::zeros((rows, C::STICKER_DIM));

    array
        .as_slice_mut()
        .expect("Array2 must be contiguous")
        .par_chunks_mut(C::STICKER_DIM)
        .enumerate()
        .for_each(|(row_index, row)| {
            let sticker_array = cubes[row_index].sticker_array_internal();
            for (sticker_index, sticker_value) in sticker_array.iter().enumerate() {
                row[sticker_index] = *sticker_value;
            }
        });

    array
}

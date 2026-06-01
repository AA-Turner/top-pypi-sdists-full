use crate::cube::Cube;
use super::Cube2x2;

impl Cube2x2 {
    /// Return the corner and edge states as a tuple of 64-bit binary strings.
    pub(crate) fn binary_state(&self) -> String {
        format!("{:064b}", self.state)
    }

    /// Return the corner state as an array
    pub(crate) fn corners_state(&self) -> Vec<(u8, u8)> {
        let mut corners = Vec::new();
        for i in 0..8 {
            corners.push(self.get_corner_internal(i));
        }
        corners
    }

    /// Return True if the cube is solved
    pub(crate) fn is_solved_internal(&self) -> bool {
        let mut solved_state: u64 = 0;
        for i in 0..8 {
            solved_state |= (i as u64) << (i * 5);
        }

        self.state == solved_state
    }

    pub(super) fn get_corner_sticker_idx(&self, pos: usize, face_index: usize) -> usize {
        const CORNER_IDX: [[usize; 3]; 8] = [
            [0, 5, 4], // 0: UBL
            [0, 1, 5], // 1: UBR
            [0, 2, 1], // 2: UFR
            [0, 4, 2], // 3: UFL
            [3, 4, 5], // 4: DBL
            [3, 5, 1], // 5: DBR
            [3, 1, 2], // 6: DFR
            [3, 2, 4], // 7: DFL
        ];

        let (piece, orientation) = self.get_corner_internal(pos);
        let color_index = (face_index + orientation as usize) % 3;
        CORNER_IDX[piece as usize][color_index]
    }

    pub(super) fn to_sticker_array_internal(&self) -> [usize; 24] {
        [
            // U face
            self.get_corner_sticker_idx(0, 0),
            self.get_corner_sticker_idx(1, 0),
            self.get_corner_sticker_idx(3, 0),
            self.get_corner_sticker_idx(2, 0),
            // R face
            self.get_corner_sticker_idx(2, 2),
            self.get_corner_sticker_idx(1, 1),
            self.get_corner_sticker_idx(6, 1),
            self.get_corner_sticker_idx(5, 2),
            // F face
            self.get_corner_sticker_idx(3, 2),
            self.get_corner_sticker_idx(2, 1),
            self.get_corner_sticker_idx(7, 1),
            self.get_corner_sticker_idx(6, 2),
            // D face
            self.get_corner_sticker_idx(7, 0),
            self.get_corner_sticker_idx(6, 0),
            self.get_corner_sticker_idx(4, 0),
            self.get_corner_sticker_idx(5, 0),
            // L face
            self.get_corner_sticker_idx(0, 2),
            self.get_corner_sticker_idx(3, 1),
            self.get_corner_sticker_idx(4, 1),
            self.get_corner_sticker_idx(7, 2),
            // B face
            self.get_corner_sticker_idx(1, 2),
            self.get_corner_sticker_idx(0, 1),
            self.get_corner_sticker_idx(5, 1),
            self.get_corner_sticker_idx(4, 2),
        ]
    }
}

impl Cube for Cube2x2 {
    const STICKER_DIM: usize = 24;

    fn corners_state_internal(&self) -> Vec<(u8, u8)> {
        Cube2x2::corners_state(self)
    }

    fn is_solved_internal(&self) -> bool {
        Cube2x2::is_solved_internal(self)
    }

    fn render_ansi_internal(&self) -> String {
        Cube2x2::render_ansi(self)
    }

    fn state_copy_internal(&self) -> Self {
        Cube2x2 { state: self.state }
    }

    fn sticker_array_internal(&self) -> Vec<i64> {
        self.to_sticker_array_internal()
            .into_iter()
            .map(|value| value as i64)
            .collect()
    }

    fn do_u_move_internal(&mut self) {
        Cube2x2::do_u_move_internal(self);
    }

    fn do_u_prime_move_internal(&mut self) {
        Cube2x2::do_u_prime_move_internal(self);
    }

    fn do_d_move_internal(&mut self) {
        Cube2x2::do_d_move_internal(self);
    }

    fn do_d_prime_move_internal(&mut self) {
        Cube2x2::do_d_prime_move_internal(self);
    }

    fn do_r_move_internal(&mut self) {
        Cube2x2::do_r_move_internal(self);
    }

    fn do_r_prime_move_internal(&mut self) {
        Cube2x2::do_r_prime_move_internal(self);
    }

    fn do_l_move_internal(&mut self) {
        Cube2x2::do_l_move_internal(self);
    }

    fn do_l_prime_move_internal(&mut self) {
        Cube2x2::do_l_prime_move_internal(self);
    }

    fn do_f_move_internal(&mut self) {
        Cube2x2::do_f_move_internal(self);
    }

    fn do_f_prime_move_internal(&mut self) {
        Cube2x2::do_f_prime_move_internal(self);
    }

    fn do_b_move_internal(&mut self) {
        Cube2x2::do_b_move_internal(self);
    }

    fn do_b_prime_move_internal(&mut self) {
        Cube2x2::do_b_prime_move_internal(self);
    }
}

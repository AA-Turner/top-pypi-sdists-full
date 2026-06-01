use crate::cube::Cube;
use super::Cube3x3;

impl Cube3x3 {
    /// Return the corner state as a 64-bit binary string.
    pub(crate) fn binary_corners_string(&self) -> String {
        format!("{:064b}", self.corners)
    }

    /// Return the edge state as a 64-bit binary string.
    pub(crate) fn binary_edges_string(&self) -> String {
        format!("{:064b}", self.edges)
    }

    /// Return the corner and edge states as a tuple of 64-bit binary strings.
    pub(crate) fn binary_state(&self) -> (String, String) {
        (
            format!("{:064b}", self.corners),
            format!("{:064b}", self.edges),
        )
    }

    /// Return the corner state as an array
    pub(crate) fn corners_state(&self) -> Vec<(u8, u8)> {
        let mut corners = Vec::new();
        for i in 0..8 {
            corners.push(self.get_corner_internal(i));
        }
        corners
    }

    /// Return the edge state as an array
    pub(crate) fn edges_state(&self) -> Vec<(u8, u8)> {
        let mut edges = Vec::new();
        for i in 0..12 {
            edges.push(self.get_edge_internal(i));
        }
        edges
    }

    /// Return True if the cube is solved
    pub(crate) fn is_solved_internal(&self) -> bool {
        let mut solved_corners: u64 = 0;
        for i in 0..8 {
            solved_corners |= (i as u64) << (i * 5);
        }

        let mut solved_edges: u64 = 0;
        for i in 0..12 {
            solved_edges |= (i as u64) << (i * 5);
        }

        self.corners == solved_corners && self.edges == solved_edges
    }

    // Read the visible sticker color for a piece position and local face index.
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

    pub(super) fn get_edge_sticker_idx(&self, pos: usize, face_index: usize) -> usize {
        const EDGE_IDX: [[usize; 2]; 12] = [
            [0, 5], // 0:  UB
            [0, 1], // 1:  UR
            [0, 2], // 2:  UF
            [0, 4], // 3:  UL
            [3, 5], // 4:  DB
            [3, 1], // 5:  DR
            [3, 2], // 6:  DF
            [3, 4], // 7:  DL
            [5, 4], // 8:  BL
            [5, 1], // 9:  BR
            [2, 1], // 10: FR
            [2, 4], // 11: FL
        ];

        let (piece, orientation) = self.get_edge_internal(pos);
        let color_index = (face_index + orientation as usize) % 2;
        EDGE_IDX[piece as usize][color_index]
    }

    pub(super) fn to_sticker_array_internal(&self) -> [usize; 54] {
        [
            // U face
            self.get_corner_sticker_idx(0, 0),
            self.get_edge_sticker_idx(0, 0),
            self.get_corner_sticker_idx(1, 0),
            self.get_edge_sticker_idx(3, 0),
            0,
            self.get_edge_sticker_idx(1, 0),
            self.get_corner_sticker_idx(3, 0),
            self.get_edge_sticker_idx(2, 0),
            self.get_corner_sticker_idx(2, 0),

            // R face
            self.get_corner_sticker_idx(2, 2),
            self.get_edge_sticker_idx(1, 1),
            self.get_corner_sticker_idx(1, 1),
            self.get_edge_sticker_idx(10, 1),
            1,
            self.get_edge_sticker_idx(9, 1),
            self.get_corner_sticker_idx(6, 1),
            self.get_edge_sticker_idx(5, 1),
            self.get_corner_sticker_idx(5, 2),

            // F face
            self.get_corner_sticker_idx(3, 2),
            self.get_edge_sticker_idx(2, 1),
            self.get_corner_sticker_idx(2, 1),
            self.get_edge_sticker_idx(11, 0),
            2,
            self.get_edge_sticker_idx(10, 0),
            self.get_corner_sticker_idx(7, 1),
            self.get_edge_sticker_idx(6, 1),
            self.get_corner_sticker_idx(6, 2),

            // D face
            self.get_corner_sticker_idx(7, 0),
            self.get_edge_sticker_idx(6, 0),
            self.get_corner_sticker_idx(6, 0),
            self.get_edge_sticker_idx(7, 0),
            3,
            self.get_edge_sticker_idx(5, 0),
            self.get_corner_sticker_idx(4, 0),
            self.get_edge_sticker_idx(4, 0),
            self.get_corner_sticker_idx(5, 0),

            // L face
            self.get_corner_sticker_idx(0, 2),
            self.get_edge_sticker_idx(3, 1),
            self.get_corner_sticker_idx(3, 1),
            self.get_edge_sticker_idx(8, 1),
            4,
            self.get_edge_sticker_idx(11, 1),
            self.get_corner_sticker_idx(4, 1),
            self.get_edge_sticker_idx(7, 1),
            self.get_corner_sticker_idx(7, 2),

            // B face
            self.get_corner_sticker_idx(1, 2),
            self.get_edge_sticker_idx(0, 1),
            self.get_corner_sticker_idx(0, 1),
            self.get_edge_sticker_idx(9, 0),
            5,
            self.get_edge_sticker_idx(8, 0),
            self.get_corner_sticker_idx(5, 1),
            self.get_edge_sticker_idx(4, 1),
            self.get_corner_sticker_idx(4, 2),
        ]
    }
}

impl Cube for Cube3x3 {
    const STICKER_DIM: usize = 54;

    fn corners_state_internal(&self) -> Vec<(u8, u8)> {
        Cube3x3::corners_state(self)
    }

    fn is_solved_internal(&self) -> bool {
        Cube3x3::is_solved_internal(self)
    }

    fn render_ansi_internal(&self) -> String {
        Cube3x3::render_ansi_string(self)
    }

    fn state_copy_internal(&self) -> Self {
        Cube3x3 {
            corners: self.corners,
            edges: self.edges,
        }
    }

    fn sticker_array_internal(&self) -> Vec<i64> {
        self.to_sticker_array_internal()
            .into_iter()
            .map(|value| value as i64)
            .collect()
    }

    fn do_u_move_internal(&mut self) {
        self.do_u_move_corners();
        self.do_u_move_edges();
    }

    fn do_u_prime_move_internal(&mut self) {
        self.do_u_prime_move_corners();
        self.do_u_prime_move_edges();
    }

    fn do_d_move_internal(&mut self) {
        self.do_d_move_corners();
        self.do_d_move_edges();
    }

    fn do_d_prime_move_internal(&mut self) {
        self.do_d_prime_move_corners();
        self.do_d_prime_move_edges();
    }

    fn do_r_move_internal(&mut self) {
        self.do_r_move_corners();
        self.rotate_edges(5, 45, 25, 50, 0);
    }

    fn do_r_prime_move_internal(&mut self) {
        self.do_r_prime_move_corners();
        self.rotate_edges_prime(5, 45, 25, 50, 0);
    }

    fn do_l_move_internal(&mut self) {
        self.do_l_move_corners();
        self.rotate_edges(15, 55, 35, 40, 0);
    }

    fn do_l_prime_move_internal(&mut self) {
        self.do_l_prime_move_corners();
        self.rotate_edges_prime(15, 55, 35, 40, 0);
    }

    fn do_f_move_internal(&mut self) {
        self.do_f_move_corners();
        self.rotate_edges(10, 50, 30, 55, 1);
    }

    fn do_f_prime_move_internal(&mut self) {
        self.do_f_prime_move_corners();
        self.rotate_edges_prime(10, 50, 30, 55, 1);
    }

    fn do_b_move_internal(&mut self) {
        self.do_b_move_corners();
        self.rotate_edges(0, 40, 20, 45, 1);
    }

    fn do_b_prime_move_internal(&mut self) {
        self.do_b_prime_move_corners();
        self.rotate_edges_prime(0, 40, 20, 45, 1);
    }
}

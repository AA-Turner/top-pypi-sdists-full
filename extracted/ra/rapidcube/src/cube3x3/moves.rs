use super::Cube3x3;

impl Cube3x3 {
    pub(crate) fn new_solved() -> Self {
        let mut corners: u64 = 0;
        for i in 0..8 {
            corners |= (i as u64) << (i * 5);
        }

        let mut edges: u64 = 0;
        for i in 0..12 {
            edges |= (i as u64) << (i * 5);
        }

        Cube3x3 { corners, edges }
    }

    pub(super) fn rotate_edges(&mut self, i0: u64, i1: u64, i2: u64, i3: u64, ori: u64) {
        let e0 = (self.edges >> i0) & 0b11111;
        let e1 = (self.edges >> i1) & 0b11111;
        let e2 = (self.edges >> i2) & 0b11111;
        let e3 = (self.edges >> i3) & 0b11111;

        let new_e0 = Self::add_ori_edge(e3, ori);
        let new_e1 = Self::add_ori_edge(e0, ori);
        let new_e2 = Self::add_ori_edge(e1, ori);
        let new_e3 = Self::add_ori_edge(e2, ori);

        let clear_mask = !((0b11111 << i0) | (0b11111 << i1) | (0b11111 << i2) | (0b11111 << i3));
        self.edges &= clear_mask;

        self.edges |= new_e0 << i0;
        self.edges |= new_e1 << i1;
        self.edges |= new_e2 << i2;
        self.edges |= new_e3 << i3;
    }

    pub(super) fn rotate_edges_prime(
        &mut self,
        i0: u64,
        i1: u64,
        i2: u64,
        i3: u64,
        ori: u64,
    ) {
        let e0 = (self.edges >> i0) & 0b11111;
        let e1 = (self.edges >> i1) & 0b11111;
        let e2 = (self.edges >> i2) & 0b11111;
        let e3 = (self.edges >> i3) & 0b11111;

        let new_e0 = Self::add_ori_edge(e1, ori);
        let new_e1 = Self::add_ori_edge(e2, ori);
        let new_e2 = Self::add_ori_edge(e3, ori);
        let new_e3 = Self::add_ori_edge(e0, ori);

        let clear_mask = !((0b11111 << i0) | (0b11111 << i1) | (0b11111 << i2) | (0b11111 << i3));
        self.edges &= clear_mask;

        self.edges |= new_e0 << i0;
        self.edges |= new_e1 << i1;
        self.edges |= new_e2 << i2;
        self.edges |= new_e3 << i3;
    }

    pub(super) fn do_u_move_corners(&mut self) {
        let u_mask = 0xFFFFF;
        let u_face = self.corners & u_mask;
        let rest = self.corners & !u_mask;
        let rotated_u = ((u_face << 5) | (u_face >> 15)) & u_mask;
        self.corners = rest | rotated_u;
    }

    pub(super) fn do_u_move_edges(&mut self) {
        let u_mask = 0xFFFFF;
        let u_face = self.edges & u_mask;
        let rest = self.edges & !u_mask;
        let rotated_u = ((u_face << 5) | (u_face >> 15)) & u_mask;
        self.edges = rest | rotated_u;
    }

    pub(super) fn do_u_prime_move_corners(&mut self) {
        let u_mask = 0xFFFFF;
        let u_face = self.corners & u_mask;
        let rest = self.corners & !u_mask;
        let rotated_u = ((u_face >> 5) | (u_face << 15)) & u_mask;
        self.corners = rest | rotated_u;
    }

    pub(super) fn do_u_prime_move_edges(&mut self) {
        let u_mask = 0xFFFFF;
        let u_face = self.edges & u_mask;
        let rest = self.edges & !u_mask;
        let rotated_u = ((u_face >> 5) | (u_face << 15)) & u_mask;
        self.edges = rest | rotated_u;
    }

    pub(super) fn do_d_move_corners(&mut self) {
        let d_mask = 0xFFFFF00000;
        let d_face = self.corners & d_mask;
        let rest = self.corners & !d_mask;
        let rotated_d = ((d_face >> 5) | (d_face << 15)) & d_mask;
        self.corners = rest | rotated_d;
    }

    pub(super) fn do_d_move_edges(&mut self) {
        let d_mask = 0xFFFFF00000;
        let d_face = self.edges & d_mask;
        let rest = self.edges & !d_mask;
        let rotated_d = ((d_face >> 5) | (d_face << 15)) & d_mask;
        self.edges = rest | rotated_d;
    }

    pub(super) fn do_d_prime_move_corners(&mut self) {
        let d_mask = 0xFFFFF00000;
        let d_face = self.corners & d_mask;
        let rest = self.corners & !d_mask;
        let rotated_d = ((d_face << 5) | (d_face >> 15)) & d_mask;
        self.corners = rest | rotated_d;
    }

    pub(super) fn do_d_prime_move_edges(&mut self) {
        let d_mask = 0xFFFFF00000;
        let d_face = self.edges & d_mask;
        let rest = self.edges & !d_mask;
        let rotated_d = ((d_face << 5) | (d_face >> 15)) & d_mask;
        self.edges = rest | rotated_d;
    }

    pub(super) fn do_r_move_corners(&mut self) {
        let c1 = (self.corners >> 5) & 0b11111;
        let c2 = (self.corners >> 10) & 0b11111;
        let c5 = (self.corners >> 25) & 0b11111;
        let c6 = (self.corners >> 30) & 0b11111;

        let new_c1 = Self::add_ori_corner(c2, 1);
        let new_c5 = Self::add_ori_corner(c1, 2);
        let new_c6 = Self::add_ori_corner(c5, 1);
        let new_c2 = Self::add_ori_corner(c6, 2);

        let clear_mask = !((0b11111 << 5) | (0b11111 << 10) | (0b11111 << 25) | (0b11111 << 30));
        self.corners &= clear_mask;

        self.corners |= new_c1 << 5;
        self.corners |= new_c2 << 10;
        self.corners |= new_c5 << 25;
        self.corners |= new_c6 << 30;
    }

    pub(super) fn do_r_prime_move_corners(&mut self) {
        let c1 = (self.corners >> 5) & 0b11111;
        let c2 = (self.corners >> 10) & 0b11111;
        let c5 = (self.corners >> 25) & 0b11111;
        let c6 = (self.corners >> 30) & 0b11111;

        let new_c2 = Self::add_ori_corner(c1, 2);
        let new_c1 = Self::add_ori_corner(c5, 1);
        let new_c5 = Self::add_ori_corner(c6, 2);
        let new_c6 = Self::add_ori_corner(c2, 1);

        let clear_mask = !((0b11111 << 5) | (0b11111 << 10) | (0b11111 << 25) | (0b11111 << 30));
        self.corners &= clear_mask;

        self.corners |= new_c1 << 5;
        self.corners |= new_c2 << 10;
        self.corners |= new_c5 << 25;
        self.corners |= new_c6 << 30;
    }

    pub(super) fn do_l_move_corners(&mut self) {
        let c0 = self.corners & 0b11111;
        let c3 = (self.corners >> 15) & 0b11111;
        let c4 = (self.corners >> 20) & 0b11111;
        let c7 = (self.corners >> 35) & 0b11111;

        let new_c3 = Self::add_ori_corner(c0, 1);
        let new_c7 = Self::add_ori_corner(c3, 2);
        let new_c4 = Self::add_ori_corner(c7, 1);
        let new_c0 = Self::add_ori_corner(c4, 2);

        let clear_mask = !((0b11111) | (0b11111 << 15) | (0b11111 << 20) | (0b11111 << 35));
        self.corners &= clear_mask;

        self.corners |= new_c0;
        self.corners |= new_c3 << 15;
        self.corners |= new_c4 << 20;
        self.corners |= new_c7 << 35;
    }

    pub(super) fn do_l_prime_move_corners(&mut self) {
        let c0 = self.corners & 0b11111;
        let c3 = (self.corners >> 15) & 0b11111;
        let c4 = (self.corners >> 20) & 0b11111;
        let c7 = (self.corners >> 35) & 0b11111;

        let new_c0 = Self::add_ori_corner(c3, 2);
        let new_c4 = Self::add_ori_corner(c0, 1);
        let new_c7 = Self::add_ori_corner(c4, 2);
        let new_c3 = Self::add_ori_corner(c7, 1);

        let clear_mask = !((0b11111) | (0b11111 << 15) | (0b11111 << 20) | (0b11111 << 35));
        self.corners &= clear_mask;

        self.corners |= new_c0;
        self.corners |= new_c3 << 15;
        self.corners |= new_c4 << 20;
        self.corners |= new_c7 << 35;
    }

    pub(super) fn do_f_move_corners(&mut self) {
        let c2 = (self.corners >> 10) & 0b11111;
        let c3 = (self.corners >> 15) & 0b11111;
        let c6 = (self.corners >> 30) & 0b11111;
        let c7 = (self.corners >> 35) & 0b11111;

        let new_c2 = Self::add_ori_corner(c3, 1);
        let new_c6 = Self::add_ori_corner(c2, 2);
        let new_c7 = Self::add_ori_corner(c6, 1);
        let new_c3 = Self::add_ori_corner(c7, 2);

        let clear_mask = !((0b11111 << 10) | (0b11111 << 15) | (0b11111 << 30) | (0b11111 << 35));
        self.corners &= clear_mask;

        self.corners |= new_c2 << 10;
        self.corners |= new_c3 << 15;
        self.corners |= new_c6 << 30;
        self.corners |= new_c7 << 35;
    }

    pub(super) fn do_f_prime_move_corners(&mut self) {
        let c2 = (self.corners >> 10) & 0b11111;
        let c3 = (self.corners >> 15) & 0b11111;
        let c6 = (self.corners >> 30) & 0b11111;
        let c7 = (self.corners >> 35) & 0b11111;

        let new_c3 = Self::add_ori_corner(c2, 2);
        let new_c7 = Self::add_ori_corner(c3, 1);
        let new_c6 = Self::add_ori_corner(c7, 2);
        let new_c2 = Self::add_ori_corner(c6, 1);

        let clear_mask = !((0b11111 << 10) | (0b11111 << 15) | (0b11111 << 30) | (0b11111 << 35));
        self.corners &= clear_mask;

        self.corners |= new_c2 << 10;
        self.corners |= new_c3 << 15;
        self.corners |= new_c6 << 30;
        self.corners |= new_c7 << 35;
    }

    pub(super) fn do_b_move_corners(&mut self) {
        let c0 = self.corners & 0b11111;
        let c1 = (self.corners >> 5) & 0b11111;
        let c4 = (self.corners >> 20) & 0b11111;
        let c5 = (self.corners >> 25) & 0b11111;

        let new_c0 = Self::add_ori_corner(c1, 1);
        let new_c4 = Self::add_ori_corner(c0, 2);
        let new_c5 = Self::add_ori_corner(c4, 1);
        let new_c1 = Self::add_ori_corner(c5, 2);

        let clear_mask = !((0b11111) | (0b11111 << 5) | (0b11111 << 20) | (0b11111 << 25));
        self.corners &= clear_mask;

        self.corners |= new_c0;
        self.corners |= new_c1 << 5;
        self.corners |= new_c4 << 20;
        self.corners |= new_c5 << 25;
    }

    pub(super) fn do_b_prime_move_corners(&mut self) {
        let c0 = self.corners & 0b11111;
        let c1 = (self.corners >> 5) & 0b11111;
        let c4 = (self.corners >> 20) & 0b11111;
        let c5 = (self.corners >> 25) & 0b11111;

        let new_c1 = Self::add_ori_corner(c0, 2);
        let new_c5 = Self::add_ori_corner(c1, 1);
        let new_c4 = Self::add_ori_corner(c5, 2);
        let new_c0 = Self::add_ori_corner(c4, 1);

        let clear_mask = !((0b11111) | (0b11111 << 5) | (0b11111 << 20) | (0b11111 << 25));
        self.corners &= clear_mask;

        self.corners |= new_c0;
        self.corners |= new_c1 << 5;
        self.corners |= new_c4 << 20;
        self.corners |= new_c5 << 25;
    }
}


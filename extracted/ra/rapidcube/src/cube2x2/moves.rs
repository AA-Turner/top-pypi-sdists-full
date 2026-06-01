use super::Cube2x2;

impl Cube2x2 {
    pub(crate) fn new_solved() -> Self {
        let mut state: u64 = 0;
        for i in 0..8 {
            state |= (i as u64) << (i * 5);
        }
        Cube2x2 { state }
    }

    pub(super) fn do_u_move_internal(&mut self) {
        let u_mask = 0xFFFFF;
        let u_face = self.state & u_mask;
        let rest = self.state & !u_mask;
        let rotated_u = ((u_face << 5) | (u_face >> 15)) & u_mask;
        self.state = rest | rotated_u;
    }

    pub(super) fn do_u_prime_move_internal(&mut self) {
        let u_mask = 0xFFFFF;
        let u_face = self.state & u_mask;
        let rest = self.state & !u_mask;
        let rotated_u = ((u_face >> 5) | (u_face << 15)) & u_mask;
        self.state = rest | rotated_u;
    }

    pub(super) fn do_d_move_internal(&mut self) {
        let d_mask = 0xFFFFF00000;
        let d_face = self.state & d_mask;
        let rest = self.state & !d_mask;
        let rotated_d = ((d_face >> 5) | (d_face << 15)) & d_mask;
        self.state = rest | rotated_d;
    }

    pub(super) fn do_d_prime_move_internal(&mut self) {
        let d_mask = 0xFFFFF00000;
        let d_face = self.state & d_mask;
        let rest = self.state & !d_mask;
        let rotated_d = ((d_face << 5) | (d_face >> 15)) & d_mask;
        self.state = rest | rotated_d;
    }

    pub(super) fn do_r_move_internal(&mut self) {
        let c1 = (self.state >> 5) & 0b11111;
        let c2 = (self.state >> 10) & 0b11111;
        let c5 = (self.state >> 25) & 0b11111;
        let c6 = (self.state >> 30) & 0b11111;

        let new_c1 = Self::add_ori(c2, 1);
        let new_c5 = Self::add_ori(c1, 2);
        let new_c6 = Self::add_ori(c5, 1);
        let new_c2 = Self::add_ori(c6, 2);

        let clear_mask = !((0b11111 << 5) | (0b11111 << 10) | (0b11111 << 25) | (0b11111 << 30));
        self.state &= clear_mask;

        self.state |= new_c1 << 5;
        self.state |= new_c2 << 10;
        self.state |= new_c5 << 25;
        self.state |= new_c6 << 30;
    }

    pub(super) fn do_r_prime_move_internal(&mut self) {
        let c1 = (self.state >> 5) & 0b11111;
        let c2 = (self.state >> 10) & 0b11111;
        let c5 = (self.state >> 25) & 0b11111;
        let c6 = (self.state >> 30) & 0b11111;

        let new_c2 = Self::add_ori(c1, 2);
        let new_c1 = Self::add_ori(c5, 1);
        let new_c5 = Self::add_ori(c6, 2);
        let new_c6 = Self::add_ori(c2, 1);

        let clear_mask = !((0b11111 << 5) | (0b11111 << 10) | (0b11111 << 25) | (0b11111 << 30));
        self.state &= clear_mask;

        self.state |= new_c1 << 5;
        self.state |= new_c2 << 10;
        self.state |= new_c5 << 25;
        self.state |= new_c6 << 30;
    }

    pub(super) fn do_l_move_internal(&mut self) {
        let c0 = self.state & 0b11111;
        let c3 = (self.state >> 15) & 0b11111;
        let c4 = (self.state >> 20) & 0b11111;
        let c7 = (self.state >> 35) & 0b11111;

        let new_c3 = Self::add_ori(c0, 1);
        let new_c7 = Self::add_ori(c3, 2);
        let new_c4 = Self::add_ori(c7, 1);
        let new_c0 = Self::add_ori(c4, 2);

        let clear_mask = !((0b11111) | (0b11111 << 15) | (0b11111 << 20) | (0b11111 << 35));
        self.state &= clear_mask;

        self.state |= new_c0;
        self.state |= new_c3 << 15;
        self.state |= new_c4 << 20;
        self.state |= new_c7 << 35;
    }

    pub(super) fn do_l_prime_move_internal(&mut self) {
        let c0 = self.state & 0b11111;
        let c3 = (self.state >> 15) & 0b11111;
        let c4 = (self.state >> 20) & 0b11111;
        let c7 = (self.state >> 35) & 0b11111;

        let new_c0 = Self::add_ori(c3, 2);
        let new_c4 = Self::add_ori(c0, 1);
        let new_c7 = Self::add_ori(c4, 2);
        let new_c3 = Self::add_ori(c7, 1);

        let clear_mask = !((0b11111) | (0b11111 << 15) | (0b11111 << 20) | (0b11111 << 35));
        self.state &= clear_mask;

        self.state |= new_c0;
        self.state |= new_c3 << 15;
        self.state |= new_c4 << 20;
        self.state |= new_c7 << 35;
    }

    pub(super) fn do_f_move_internal(&mut self) {
        let c2 = (self.state >> 10) & 0b11111;
        let c3 = (self.state >> 15) & 0b11111;
        let c6 = (self.state >> 30) & 0b11111;
        let c7 = (self.state >> 35) & 0b11111;

        let new_c2 = Self::add_ori(c3, 1);
        let new_c6 = Self::add_ori(c2, 2);
        let new_c7 = Self::add_ori(c6, 1);
        let new_c3 = Self::add_ori(c7, 2);

        let clear_mask = !((0b11111 << 10) | (0b11111 << 15) | (0b11111 << 30) | (0b11111 << 35));
        self.state &= clear_mask;

        self.state |= new_c2 << 10;
        self.state |= new_c3 << 15;
        self.state |= new_c6 << 30;
        self.state |= new_c7 << 35;
    }

    pub(super) fn do_f_prime_move_internal(&mut self) {
        let c2 = (self.state >> 10) & 0b11111;
        let c3 = (self.state >> 15) & 0b11111;
        let c6 = (self.state >> 30) & 0b11111;
        let c7 = (self.state >> 35) & 0b11111;

        let new_c3 = Self::add_ori(c2, 2);
        let new_c7 = Self::add_ori(c3, 1);
        let new_c6 = Self::add_ori(c7, 2);
        let new_c2 = Self::add_ori(c6, 1);

        let clear_mask = !((0b11111 << 10) | (0b11111 << 15) | (0b11111 << 30) | (0b11111 << 35));
        self.state &= clear_mask;

        self.state |= new_c2 << 10;
        self.state |= new_c3 << 15;
        self.state |= new_c6 << 30;
        self.state |= new_c7 << 35;
    }

    pub(super) fn do_b_move_internal(&mut self) {
        let c0 = self.state & 0b11111;
        let c1 = (self.state >> 5) & 0b11111;
        let c4 = (self.state >> 20) & 0b11111;
        let c5 = (self.state >> 25) & 0b11111;

        let new_c0 = Self::add_ori(c1, 1);
        let new_c4 = Self::add_ori(c0, 2);
        let new_c5 = Self::add_ori(c4, 1);
        let new_c1 = Self::add_ori(c5, 2);

        let clear_mask = !((0b11111) | (0b11111 << 5) | (0b11111 << 20) | (0b11111 << 25));
        self.state &= clear_mask;

        self.state |= new_c0;
        self.state |= new_c1 << 5;
        self.state |= new_c4 << 20;
        self.state |= new_c5 << 25;
    }

    pub(super) fn do_b_prime_move_internal(&mut self) {
        let c0 = self.state & 0b11111;
        let c1 = (self.state >> 5) & 0b11111;
        let c4 = (self.state >> 20) & 0b11111;
        let c5 = (self.state >> 25) & 0b11111;

        let new_c1 = Self::add_ori(c0, 2);
        let new_c5 = Self::add_ori(c1, 1);
        let new_c4 = Self::add_ori(c5, 2);
        let new_c0 = Self::add_ori(c4, 1);

        let clear_mask = !((0b11111) | (0b11111 << 5) | (0b11111 << 20) | (0b11111 << 25));
        self.state &= clear_mask;

        self.state |= new_c0;
        self.state |= new_c1 << 5;
        self.state |= new_c4 << 20;
        self.state |= new_c5 << 25;
    }
}

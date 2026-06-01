use super::Cube2x2;

impl Cube2x2 {
    // Convert sticker char to ANSI-colored output.
    fn ansi_color(c: char) -> String {
        match c {
            'W' => format!("\x1b[37;1m{}\x1b[0m", c),
            'Y' => format!("\x1b[33;1m{}\x1b[0m", c),
            'G' => format!("\x1b[32;1m{}\x1b[0m", c),
            'B' => format!("\x1b[34;1m{}\x1b[0m", c),
            'O' => format!("\x1b[38;5;208m{}\x1b[0m", c),
            'R' => format!("\x1b[31;1m{}\x1b[0m", c),
            _ => c.to_string(),
        }
    }

    // Read the visible sticker color for a piece position and local face index.
    pub(super) fn get_sticker(&self, pos: usize, face_index: usize) -> String {
        const PIECE_COLORS: [[char; 3]; 8] = [
            ['W', 'B', 'O'], // 0: UBL
            ['W', 'R', 'B'], // 1: UBR
            ['W', 'G', 'R'], // 2: UFR
            ['W', 'O', 'G'], // 3: UFL
            ['Y', 'O', 'B'], // 4: DBL
            ['Y', 'B', 'R'], // 5: DBR
            ['Y', 'R', 'G'], // 6: DFR
            ['Y', 'G', 'O'], // 7: DFL
        ];

        let (piece, orientation) = self.get_corner_internal(pos);
        let color_index = (face_index + orientation as usize) % 3;
        let char_color = PIECE_COLORS[piece as usize][color_index];

        Self::ansi_color(char_color)
    }

    pub(super) fn render_ansi(&self) -> String {
        let u0 = self.get_sticker(0, 0);
        let u1 = self.get_sticker(1, 0);
        let u2 = self.get_sticker(3, 0);
        let u3 = self.get_sticker(2, 0);

        let l0 = self.get_sticker(0, 2);
        let l1 = self.get_sticker(3, 1);
        let l2 = self.get_sticker(4, 1);
        let l3 = self.get_sticker(7, 2);

        let f0 = self.get_sticker(3, 2);
        let f1 = self.get_sticker(2, 1);
        let f2 = self.get_sticker(7, 1);
        let f3 = self.get_sticker(6, 2);

        let r0 = self.get_sticker(2, 2);
        let r1 = self.get_sticker(1, 1);
        let r2 = self.get_sticker(6, 1);
        let r3 = self.get_sticker(5, 2);

        let b0 = self.get_sticker(1, 2);
        let b1 = self.get_sticker(0, 1);
        let b2 = self.get_sticker(5, 1);
        let b3 = self.get_sticker(4, 2);

        let d0 = self.get_sticker(7, 0);
        let d1 = self.get_sticker(6, 0);
        let d2 = self.get_sticker(4, 0);
        let d3 = self.get_sticker(5, 0);

        format!(
            "      {} {}\n      {} {}\n{} {}   {} {}   {} {}   {} {}\n{} {}   {} {}   {} {}   {} {}\n      {} {}\n      {} {}\n",
            u0,
            u1,
            u2,
            u3,
            l0,
            l1,
            f0,
            f1,
            r0,
            r1,
            b0,
            b1,
            l2,
            l3,
            f2,
            f3,
            r2,
            r3,
            b2,
            b3,
            d0,
            d1,
            d2,
            d3
        )
    }
}

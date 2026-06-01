use super::Cube3x3;

impl Cube3x3 {
    // Convert sticker char to ANSI-colored output.
    pub(super) fn ansi_color(c: char) -> String {
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
    pub(super) fn get_corner_sticker(&self, pos: usize, face_index: usize) -> String {
        const CORNER_COLORS: [[char; 3]; 8] = [
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
        let char_color = CORNER_COLORS[piece as usize][color_index];

        Self::ansi_color(char_color)
    }

    pub(super) fn get_edge_sticker(&self, pos: usize, face_index: usize) -> String {
        const EDGE_COLORS: [[char; 2]; 12] = [
            ['W', 'B'], // 0:  UB
            ['W', 'R'], // 1:  UR
            ['W', 'G'], // 2:  UF
            ['W', 'O'], // 3:  UL
            ['Y', 'B'], // 4:  DB
            ['Y', 'R'], // 5:  DR
            ['Y', 'G'], // 6:  DF
            ['Y', 'O'], // 7:  DL
            ['B', 'O'], // 8:  BL
            ['B', 'R'], // 9:  BR
            ['G', 'R'], // 10: FR
            ['G', 'O'], // 11: FL
        ];

        let (piece, orientation) = self.get_edge_internal(pos);
        let color_index = (face_index + orientation as usize) % 2;
        let char_color = EDGE_COLORS[piece as usize][color_index];

        Self::ansi_color(char_color)
    }
}

impl Cube3x3 {
    /// Return an ANSI-colored string rendering of the cube.
    pub(crate) fn render_ansi_string(&self) -> String {
        let uc = Self::ansi_color('W');
        let lc = Self::ansi_color('O');
        let fc = Self::ansi_color('G');
        let rc = Self::ansi_color('R');
        let bc = Self::ansi_color('B');
        let dc = Self::ansi_color('Y');

        // U face
        let u00 = self.get_corner_sticker(0, 0);
        let u01 = self.get_edge_sticker(0, 0);
        let u02 = self.get_corner_sticker(1, 0);
        let u10 = self.get_edge_sticker(3, 0);
        let u12 = self.get_edge_sticker(1, 0);
        let u20 = self.get_corner_sticker(3, 0);
        let u21 = self.get_edge_sticker(2, 0);
        let u22 = self.get_corner_sticker(2, 0);

        // L face
        let l00 = self.get_corner_sticker(0, 2);
        let l01 = self.get_edge_sticker(3, 1);
        let l02 = self.get_corner_sticker(3, 1);
        let l10 = self.get_edge_sticker(8, 1);
        let l12 = self.get_edge_sticker(11, 1);
        let l20 = self.get_corner_sticker(4, 1);
        let l21 = self.get_edge_sticker(7, 1);
        let l22 = self.get_corner_sticker(7, 2);

        // F face
        let f00 = self.get_corner_sticker(3, 2);
        let f01 = self.get_edge_sticker(2, 1);
        let f02 = self.get_corner_sticker(2, 1);
        let f10 = self.get_edge_sticker(11, 0);
        let f12 = self.get_edge_sticker(10, 0);
        let f20 = self.get_corner_sticker(7, 1);
        let f21 = self.get_edge_sticker(6, 1);
        let f22 = self.get_corner_sticker(6, 2);

        // R face
        let r00 = self.get_corner_sticker(2, 2);
        let r01 = self.get_edge_sticker(1, 1);
        let r02 = self.get_corner_sticker(1, 1);
        let r10 = self.get_edge_sticker(10, 1);
        let r12 = self.get_edge_sticker(9, 1);
        let r20 = self.get_corner_sticker(6, 1);
        let r21 = self.get_edge_sticker(5, 1);
        let r22 = self.get_corner_sticker(5, 2);

        // B face
        let b00 = self.get_corner_sticker(1, 2);
        let b01 = self.get_edge_sticker(0, 1);
        let b02 = self.get_corner_sticker(0, 1);
        let b10 = self.get_edge_sticker(9, 0);
        let b12 = self.get_edge_sticker(8, 0);
        let b20 = self.get_corner_sticker(5, 1);
        let b21 = self.get_edge_sticker(4, 1);
        let b22 = self.get_corner_sticker(4, 2);

        // D face
        let d00 = self.get_corner_sticker(7, 0);
        let d01 = self.get_edge_sticker(6, 0);
        let d02 = self.get_corner_sticker(6, 0);
        let d10 = self.get_edge_sticker(7, 0);
        let d12 = self.get_edge_sticker(5, 0);
        let d20 = self.get_corner_sticker(4, 0);
        let d21 = self.get_edge_sticker(4, 0);
        let d22 = self.get_corner_sticker(5, 0);

        format!(
            "       {} {} {}\n       {} {} {}\n       {} {} {}\n{} {} {}  {} {} {}  {} {} {}  {} {} {}\n{} {} {}  {} {} {}  {} {} {}  {} {} {}\n{} {} {}  {} {} {}  {} {} {}  {} {} {}\n       {} {} {}\n       {} {} {}\n       {} {} {}\n",
            u00,
            u01,
            u02,
            u10,
            uc,
            u12,
            u20,
            u21,
            u22,
            l00,
            l01,
            l02,
            f00,
            f01,
            f02,
            r00,
            r01,
            r02,
            b00,
            b01,
            b02,
            l10,
            lc,
            l12,
            f10,
            fc,
            f12,
            r10,
            rc,
            r12,
            b10,
            bc,
            b12,
            l20,
            l21,
            l22,
            f20,
            f21,
            f22,
            r20,
            r21,
            r22,
            b20,
            b21,
            b22,
            d00,
            d01,
            d02,
            d10,
            dc,
            d12,
            d20,
            d21,
            d22,
        )
    }
}


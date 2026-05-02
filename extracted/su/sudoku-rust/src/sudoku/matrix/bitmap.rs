pub type Bitmap = u16;

pub const BITMAP_DIGIT: usize = 9;
pub const FULL_BIT: Bitmap = 0b111_111_111;

pub struct EachBit {
    bitmap: Bitmap,
    next_bit: Bitmap,
}

impl EachBit {
    pub fn new(bitmap: Bitmap) -> Self {
        EachBit {
            bitmap,
            next_bit: 0b100_000_000,
        }
    }
}

impl Iterator for EachBit {
    type Item = Bitmap;
    fn next(&mut self) -> Option<Self::Item> {
        while self.bitmap & self.next_bit == 0 && self.next_bit != 0 {
            self.next_bit >>= 1;
        }

        if self.next_bit == 0 {
            None
        } else {
            let cur = self.next_bit;
            self.next_bit >>= 1;
            Some(cur)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn split_single_bit_test() {
        let v = EachBit::new(0b000_000_000).next();
        assert_eq!(v, None);

        let mut bits = Vec::<Bitmap>::new();
        for v in EachBit::new(0b100_100_101) {
            bits.push(v);
        }
        assert_eq!(bits, [256, 32, 4, 1]);

        let mut bits = Vec::<Bitmap>::new();
        for v in EachBit::new(FULL_BIT) {
            bits.push(v);
        }
        assert_eq!(bits, [256, 128, 64, 32, 16, 8, 4, 2, 1]);
    }
}

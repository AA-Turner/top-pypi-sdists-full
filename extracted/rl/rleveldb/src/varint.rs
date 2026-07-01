/// LevelDB-style varint reading and a cursor helper for sequential byte slice parsing.

/// Read a varint from a byte slice, returning (value, bytes_consumed).
/// If `is_google_32bit` is true, limits to 5 bytes (32-bit); otherwise 10 bytes (64-bit).
/// Returns `None` if no data is available.
pub fn read_le_varint(data: &[u8], is_google_32bit: bool) -> Option<(u64, usize)> {
    let limit = if is_google_32bit { 5 } else { 10 };
    let mut result: u64 = 0;
    for i in 0..limit {
        if i >= data.len() {
            return None;
        }
        let tmp = data[i];
        result |= ((tmp & 0x7F) as u64) << (i * 7);
        if (tmp & 0x80) == 0 {
            return Some((result, i + 1));
        }
    }
    Some((result, limit))
}

/// Read a length-prefixed blob from a byte slice.
/// Returns `(blob_data, total_bytes_consumed)` or `None`.
pub fn read_length_prefixed_blob(data: &[u8]) -> Option<(&[u8], usize)> {
    let (length, varint_size) = read_le_varint(data, false)?;
    let length = length as usize;
    let end = varint_size + length;
    if end > data.len() {
        return None;
    }
    Some((&data[varint_size..end], end))
}

/// A cursor over a byte slice that tracks a read position for sequential parsing.
pub struct SliceCursor<'a> {
    data: &'a [u8],
    pos: usize,
}

impl<'a> SliceCursor<'a> {
    pub fn new(data: &'a [u8]) -> Self {
        Self { data, pos: 0 }
    }

    pub fn position(&self) -> usize {
        self.pos
    }

    pub fn remaining(&self) -> &'a [u8] {
        &self.data[self.pos..]
    }

    pub fn is_empty(&self) -> bool {
        self.pos >= self.data.len()
    }

    pub fn read_bytes(&mut self, n: usize) -> Option<&'a [u8]> {
        if self.pos + n > self.data.len() {
            return None;
        }
        let result = &self.data[self.pos..self.pos + n];
        self.pos += n;
        Some(result)
    }

    pub fn read_byte(&mut self) -> Option<u8> {
        if self.pos >= self.data.len() {
            return None;
        }
        let b = self.data[self.pos];
        self.pos += 1;
        Some(b)
    }

    pub fn read_u16_le(&mut self) -> Option<u16> {
        let bytes = self.read_bytes(2)?;
        Some(u16::from_le_bytes([bytes[0], bytes[1]]))
    }

    pub fn read_u32_le(&mut self) -> Option<u32> {
        let bytes = self.read_bytes(4)?;
        Some(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }

    pub fn read_u64_le(&mut self) -> Option<u64> {
        let bytes = self.read_bytes(8)?;
        Some(u64::from_le_bytes(bytes.try_into().ok()?))
    }

    pub fn read_varint(&mut self, is_google_32bit: bool) -> Option<u64> {
        let (value, consumed) = read_le_varint(&self.data[self.pos..], is_google_32bit)?;
        self.pos += consumed;
        Some(value)
    }

    pub fn read_length_prefixed_blob(&mut self) -> Option<&'a [u8]> {
        let (blob, consumed) = read_length_prefixed_blob(&self.data[self.pos..])?;
        self.pos += consumed;
        Some(blob)
    }

    pub fn seek(&mut self, pos: usize) {
        self.pos = pos;
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_byte_varint() {
        assert_eq!(read_le_varint(&[0x00], false), Some((0, 1)));
        assert_eq!(read_le_varint(&[0x01], false), Some((1, 1)));
        assert_eq!(read_le_varint(&[0x7F], false), Some((127, 1)));
    }

    #[test]
    fn test_multi_byte_varint() {
        // 300 = 0b100101100 => varint bytes: [0xAC, 0x02]
        assert_eq!(read_le_varint(&[0xAC, 0x02], false), Some((300, 2)));
    }

    #[test]
    fn test_varint_empty_input() {
        assert_eq!(read_le_varint(&[], false), None);
    }

    #[test]
    fn test_length_prefixed_blob() {
        // length=3 as varint (0x03), then 3 bytes of data
        let data = [0x03, b'a', b'b', b'c', 0xFF];
        let (blob, consumed) = read_length_prefixed_blob(&data).unwrap();
        assert_eq!(blob, b"abc");
        assert_eq!(consumed, 4);
    }

    #[test]
    fn test_length_prefixed_blob_truncated() {
        let data = [0x05, b'a', b'b'];
        assert_eq!(read_length_prefixed_blob(&data), None);
    }

    #[test]
    fn test_slice_cursor_sequential_reads() {
        let data = [0x01, 0x02, 0x03, 0x04, 0x05];
        let mut cursor = SliceCursor::new(&data);
        assert_eq!(cursor.position(), 0);
        assert_eq!(cursor.len(), 5);
        assert!(!cursor.is_empty());

        assert_eq!(cursor.read_byte(), Some(0x01));
        assert_eq!(cursor.position(), 1);

        assert_eq!(cursor.read_bytes(2), Some(&[0x02, 0x03][..]));
        assert_eq!(cursor.position(), 3);

        assert_eq!(cursor.remaining(), &[0x04, 0x05]);

        cursor.seek(0);
        assert_eq!(cursor.position(), 0);
    }

    #[test]
    fn test_slice_cursor_le_integers() {
        let data = [0x01, 0x00, 0x02, 0x00, 0x00, 0x00];
        let mut cursor = SliceCursor::new(&data);
        assert_eq!(cursor.read_u16_le(), Some(1));
        assert_eq!(cursor.read_u32_le(), Some(2));
        assert!(cursor.is_empty());
    }

    #[test]
    fn test_slice_cursor_varint() {
        let data = [0xAC, 0x02, 0x01];
        let mut cursor = SliceCursor::new(&data);
        assert_eq!(cursor.read_varint(false), Some(300));
        assert_eq!(cursor.read_varint(false), Some(1));
        assert!(cursor.is_empty());
    }
}

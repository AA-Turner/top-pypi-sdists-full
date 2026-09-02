use std::io;

pub const STRING_KEY: &str = "a string is always a valid dict key";

/// A serialized frame is a sequence of msgpack-encoded bytes.
pub type SerializedFrame = Vec<u8>;

/// Read-only logical frame storage. Implementations may keep frames in native
/// arenas or in the write-once v3 temporary file; `scratch` is reusable space
/// for file-backed reads.
pub trait FrameSequence {
    fn len(&self) -> usize;
    fn frame_len(&self, index: usize) -> io::Result<usize>;
    fn frame<'a>(&'a self, index: usize, scratch: &'a mut Vec<u8>) -> io::Result<&'a [u8]>;

    fn is_empty(&self) -> bool {
        self.len() == 0
    }
}

impl FrameSequence for Vec<SerializedFrame> {
    fn len(&self) -> usize {
        Vec::len(self)
    }

    fn frame_len(&self, index: usize) -> io::Result<usize> {
        self.get(index)
            .map(Vec::len)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))
    }

    fn frame<'a>(&'a self, index: usize, _scratch: &'a mut Vec<u8>) -> io::Result<&'a [u8]> {
        self.get(index)
            .map(Vec::as_slice)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))
    }
}

impl FrameSequence for [SerializedFrame] {
    fn len(&self) -> usize {
        <[SerializedFrame]>::len(self)
    }

    fn frame_len(&self, index: usize) -> io::Result<usize> {
        self.get(index)
            .map(Vec::len)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))
    }

    fn frame<'a>(&'a self, index: usize, _scratch: &'a mut Vec<u8>) -> io::Result<&'a [u8]> {
        self.get(index)
            .map(Vec::as_slice)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "invalid frame index"))
    }
}

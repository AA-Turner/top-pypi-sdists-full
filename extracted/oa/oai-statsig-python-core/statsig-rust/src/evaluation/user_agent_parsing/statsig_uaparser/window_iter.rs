use memchr::memchr2;

pub struct WindowIter<'a> {
    iter: AsciiDelimiterSplit<'a>,
    window: [Option<&'a str>; 4],
}

type Window<'a> = (
    Option<&'a str>,
    Option<&'a str>,
    Option<&'a str>,
    Option<&'a str>,
);

impl<'a> WindowIter<'a> {
    pub fn new(input: &'a str) -> Self {
        let mut iter = AsciiDelimiterSplit::new(input);
        let window = std::array::from_fn(|_| iter.next());

        Self { iter, window }
    }

    pub fn get_window(&self) -> Window<'a> {
        let [curr, next1, next2, next3] = self.window;
        (curr, next1, next2, next3)
    }

    pub fn slide_window_by(&mut self, n: usize) {
        for _ in 0..n {
            self.window.rotate_left(1);
            self.window[3] = self.iter.next();
        }
    }

    pub fn is_empty(&self) -> bool {
        self.window[0].is_none()
    }
}

struct AsciiDelimiterSplit<'a> {
    remainder: Option<&'a str>,
}

impl<'a> AsciiDelimiterSplit<'a> {
    fn new(input: &'a str) -> Self {
        Self {
            remainder: Some(input),
        }
    }
}

impl<'a> Iterator for AsciiDelimiterSplit<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        let remainder = self.remainder.take()?;
        let Some(delimiter) = memchr2(b';', b' ', remainder.as_bytes()) else {
            return Some(remainder);
        };

        let (word, rest) = remainder.split_at(delimiter);
        self.remainder = Some(&rest[1..]);
        Some(word)
    }
}

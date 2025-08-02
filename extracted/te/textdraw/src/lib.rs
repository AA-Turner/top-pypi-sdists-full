#![allow(clippy::too_many_arguments)]
#![allow(dead_code)]
use std::{
    cmp::Ordering,
    collections::{BinaryHeap, HashMap, HashSet},
    fmt::{Debug, Display},
    ops::{Add, AddAssign},
    str::FromStr,
};

use auto_ops::{impl_op_ex, impl_op_ex_commutative};
use itertools::Itertools;
use owo_colors::{AnsiColors, Effect, OwoColorize, Style};
use pyo3::{
    exceptions::{PyTypeError, PyValueError},
    prelude::*,
    types::{PyList, PyTuple},
};
use regex::Regex;

/// Represents a 2D point with integer coordinates.
///
/// Parameters
/// ----------
/// x : int
///     The x-coordinate of the point.
/// y : int
///     The y-coordinate of the point.
///
/// Attributes
/// ----------
/// x : int
///     The x-coordinate of the point.
/// y : int
///     The y-coordinate of the point.
///
/// Examples
/// --------
/// >>> p = Point(1, 2)
/// >>> p.x
/// 1
/// >>> p.y
/// 2
/// >>> p + Point(3, 4)
/// (4, 6)
///
#[pyclass]
#[derive(Default, Clone, Copy, Eq, PartialEq, Hash)]
struct Point(isize, isize);
#[pymethods]
impl Point {
    #[new]
    fn new(x: isize, y: isize) -> Self {
        Self(x, y)
    }
    #[getter]
    fn x(&self) -> isize {
        self.0
    }
    #[getter]
    fn y(&self) -> isize {
        self.1
    }
    fn __add__(&self, rhs: Bound<PyAny>) -> PyResult<Point> {
        Ok(self + rhs.extract::<Point>()?)
    }
    fn __radd__(&self, rhs: Bound<PyAny>) -> PyResult<Point> {
        Ok(rhs.extract::<Point>()? + self)
    }
    fn __sub__(&self, rhs: Bound<PyAny>) -> PyResult<Point> {
        Ok(self - rhs.extract::<Point>()?)
    }
    fn __rsub__(&self, rhs: Bound<PyAny>) -> PyResult<Point> {
        Ok(rhs.extract::<Point>()? - self)
    }
    fn __repr__(&self) -> String {
        self.to_string()
    }
    fn __str__(&self) -> String {
        self.to_string()
    }
    /// Calculates the midpoint between this point and another point.
    ///
    /// Parameters
    /// ----------
    /// other : Point
    ///     The other point.
    ///
    /// Returns
    /// -------
    /// Point
    ///     The midpoint.
    ///
    /// Examples
    /// --------
    /// >>> p1 = Point(0, 0)
    /// >>> p2 = Point(2, 2)
    /// >>> p1.midpoint(p2)
    /// (1, 1)
    ///
    #[pyo3(name = "midpoint")]
    fn py_midpoint(&self, other: Bound<PyAny>) -> PyResult<Point> {
        Ok(self.midpoint(&Point::extract_bound(&other)?))
    }
}
impl Point {
    fn midpoint(&self, other: &Point) -> Point {
        Point((self.0 + other.0) / 2, (self.1 + other.1) / 2)
    }
}
impl Debug for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.0, self.1)
    }
}
impl Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}
impl Point {
    fn extract_bound<'py>(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        if let Ok(tup) = ob.extract::<(isize, isize)>() {
            Ok(tup.into())
        } else {
            Ok(ob.extract::<Point>()?)
        }
    }
}
impl From<(isize, isize)> for Point {
    fn from(value: (isize, isize)) -> Self {
        Self(value.0, value.1)
    }
}
#[rustfmt::skip]
impl_op_ex!(+ |a: &Point, b: &Point| -> Point { Point(a.0 + b.0, a.1 + b.1) });
#[rustfmt::skip]
impl_op_ex!(- |a: &Point, b: &Point| -> Point { Point(a.0 - b.0, a.1 - b.1) });
#[rustfmt::skip]
impl_op_ex!(+= |a: &mut Point, b: &Point| { a.0 += b.0; a.1 += b.1; });
#[rustfmt::skip]
impl_op_ex!(-= |a: &mut Point, b: &Point| { a.0 -= b.0; a.1 -= b.1; });
#[rustfmt::skip]
impl_op_ex_commutative!(+ |a: &Point, b: &(isize, isize)| -> Point { Point(a.0 + b.0, a.1 + b.1) });
#[rustfmt::skip]
impl_op_ex_commutative!(- |a: &Point, b: &(isize, isize)| -> Point { Point(a.0 + b.0, a.1 + b.1) });
#[rustfmt::skip]
impl_op_ex!(+= |a: &mut Point, b: &(isize, isize)| { a.0 += b.0; a.1 += b.1; });
#[rustfmt::skip]
impl_op_ex!(-= |a: &mut Point, b: &(isize, isize)| { a.0 -= b.0; a.1 -= b.1; });

/// Represents a rectangular bounding box with integer coordinates.
///
/// Parameters
/// ----------
/// top : int
///     The top y-coordinate of the bounding box.
/// right : int
///     The right x-coordinate of the bounding box.
/// bottom : int
///     The bottom y-coordinate of the bounding box.
/// left : int
///     The left x-coordinate of the bounding box.
///
/// Attributes
/// ----------
/// top : int
///     The top y-coordinate.
/// right : int
///     The right x-coordinate.
/// bottom : int
///     The bottom y-coordinate.
/// left : int
///     The left x-coordinate.
/// width : int
///     The width of the bounding box.
/// height : int
///     The height of the bounding box.
/// center : Point
///     The center point of the bounding box.
/// top_left : Point
///     The top-left corner point.
/// top_center : Point
///     The top-center point.
/// top_right : Point
///     The top-right corner point.
/// bottom_left : Point
///     The bottom-left corner point.
/// bottom_center : Point
///     The bottom-center point.
/// bottom_right : Point
///     The bottom-right corner point.
/// center_left : Point
///     The center-left point.
/// center_right : Point
///     The center-right point.
///
/// Examples
/// --------
/// >>> bbox = BoundingBox(top=10, right=20, bottom=0, left=0)
/// >>> bbox.width
/// 20
/// >>> bbox.height
/// 10
/// >>> bbox.center
/// (10, 5)
///
#[pyclass]
#[derive(Default, Copy, Clone, Debug)]
struct BoundingBox {
    #[pyo3(get, set)]
    top: isize,
    #[pyo3(get, set)]
    right: isize,
    #[pyo3(get, set)]
    bottom: isize,
    #[pyo3(get, set)]
    left: isize,
}
impl BoundingBox {
    fn contains_point(&self, p: &Point) -> bool {
        p.0 >= self.left && p.0 <= self.right && p.1 >= self.bottom && p.1 <= self.top
    }
    fn contains_bounding_box(&self, bbox: BoundingBox) -> bool {
        bbox.left >= self.left
            && bbox.right <= self.right
            && bbox.bottom >= self.bottom
            && bbox.top <= self.top
    }
    fn as_map(
        &self,
        border_style: &TextStyle,
        fill_style: &TextStyle,
        line_style: Option<LineStyle>,
        weight: Option<usize>,
        transparent: bool,
    ) -> HashMap<Point, Pixel> {
        let mut pixels = HashMap::default();
        for i in self.left + 1..self.right {
            pixels.insert(
                Point(i, self.top),
                Pixel {
                    character: line_style.map_or(' ', |ls| ls.get_char((false, true, false, true))),
                    position: Point(i, self.top),
                    style: border_style.clone(),
                    weight,
                },
            );
            pixels.insert(
                Point(i, self.bottom),
                Pixel {
                    character: line_style.map_or(' ', |ls| ls.get_char((false, true, false, true))),
                    position: Point(i, self.bottom),
                    style: border_style.clone(),
                    weight,
                },
            );
        }
        for j in self.bottom + 1..self.top {
            pixels.insert(
                Point(self.left, j),
                Pixel {
                    character: line_style.map_or(' ', |ls| ls.get_char((true, false, true, false))),
                    position: Point(self.left, j),
                    style: border_style.clone(),
                    weight,
                },
            );
            pixels.insert(
                Point(self.right, j),
                Pixel {
                    character: line_style.map_or(' ', |ls| ls.get_char((true, false, true, false))),
                    position: Point(self.right, j),
                    style: border_style.clone(),
                    weight,
                },
            );
        }
        pixels.insert(
            Point(self.right, self.top),
            Pixel {
                character: line_style.map_or(' ', |ls| ls.get_char((false, false, true, true))),
                position: Point(self.right, self.top),
                style: border_style.clone(),
                weight,
            },
        );
        pixels.insert(
            Point(self.right, self.bottom),
            Pixel {
                character: line_style.map_or(' ', |ls| ls.get_char((true, false, false, true))),
                position: Point(self.right, self.bottom),
                style: border_style.clone(),
                weight,
            },
        );
        pixels.insert(
            Point(self.left, self.top),
            Pixel {
                character: line_style.map_or(' ', |ls| ls.get_char((false, true, true, false))),
                position: Point(self.left, self.top),
                style: border_style.clone(),
                weight,
            },
        );
        pixels.insert(
            Point(self.left, self.bottom),
            Pixel {
                character: line_style.map_or(' ', |ls| ls.get_char((true, true, false, false))),
                position: Point(self.left, self.bottom),
                style: border_style.clone(),
                weight,
            },
        );
        if !transparent {
            for i in self.left + 1..self.right {
                for j in self.bottom + 1..self.top {
                    pixels.insert(
                        Point(i, j),
                        Pixel {
                            character: ' ',
                            position: Point(i, j),
                            style: fill_style.clone(),
                            weight,
                        },
                    );
                }
            }
        }
        pixels
    }
    fn duplicate_shifted(&self, position: Point) -> Self {
        Self {
            top: self.top + position.1,
            right: self.right + position.0,
            bottom: self.bottom + position.1,
            left: self.left + position.0,
        }
    }
}
#[pymethods]
impl BoundingBox {
    #[new]
    fn new(top: isize, right: isize, bottom: isize, left: isize) -> Self {
        Self {
            top,
            right,
            bottom,
            left,
        }
    }
    /// Creates a BoundingBox that wraps around a collection of objects.
    ///
    /// Parameters
    /// ----------
    /// objs : list
    ///     A list of objects to fill the BoundingBox. Each object must be an instance of TextPath, Box, Pixel, or PixelGroup.
    ///
    /// Returns
    /// -------
    /// BoundingBox
    ///     A new BoundingBox that encompasses all provided objects.
    ///
    /// Examples
    /// --------
    /// >>> BoundingBox.wrap(Point(0,0), Point(10,10))
    /// BoundingBox(top=10, right=10, bottom=0, left=0)
    /// >>> BoundingBox.wrap(BoundingBox(0,0,0,0), BoundingBox(10,10,10,10))
    /// BoundingBox(top=10, right=10, bottom=0, left=0)
    ///
    #[staticmethod]
    fn wrap(objs: Bound<'_, PyAny>) -> PyResult<BoundingBox> {
        let map = objs_to_map(&objs)?;
        let bbox = map_to_bounding_box(&map);
        Ok(bbox)
    }
    fn __contains__(&self, other: Bound<PyAny>) -> PyResult<bool> {
        if let Ok(point) = other.extract::<Point>() {
            Ok(self.contains_point(&point))
        } else if let Ok(bbox) = other.extract::<BoundingBox>() {
            Ok(self.contains_bounding_box(bbox))
        } else {
            Err(PyTypeError::new_err(
                "Expected either a Point or a BoundingBox",
            ))
        }
    }
    fn __add__(&self, other: Bound<PyAny>) -> PyResult<BoundingBox> {
        if let Ok(point) = other.extract::<Point>() {
            Ok(*self + point)
        } else if let Ok(bbox) = other.extract::<BoundingBox>() {
            Ok(*self + bbox)
        } else {
            Err(PyTypeError::new_err(
                "Expected either a Point or a BoundingBox",
            ))
        }
    }
    fn __str__(&self) -> String {
        format!(
            "BoundingBox(top={}, right={}, bottom={}, left={})",
            self.top, self.right, self.bottom, self.left
        )
    }
    #[getter]
    fn width(&self) -> usize {
        (self.right - self.left) as usize
    }
    #[getter]
    fn height(&self) -> usize {
        (self.top - self.bottom) as usize
    }
    #[getter]
    fn center(&self) -> Point {
        Point((self.left + self.right) / 2, (self.bottom + self.top) / 2)
    }
    #[getter]
    fn top_left(&self) -> Point {
        Point(self.left, self.top)
    }
    #[getter]
    fn top_center(&self) -> Point {
        Point((self.left + self.right) / 2, self.top)
    }
    #[getter]
    fn top_right(&self) -> Point {
        Point(self.right, self.top)
    }
    #[getter]
    fn bottom_left(&self) -> Point {
        Point(self.left, self.bottom)
    }
    #[getter]
    fn bottom_center(&self) -> Point {
        Point((self.left + self.right) / 2, self.bottom)
    }
    #[getter]
    fn bottom_right(&self) -> Point {
        Point(self.right, self.bottom)
    }
    #[getter]
    fn center_left(&self) -> Point {
        Point(self.left, (self.bottom + self.top) / 2)
    }
    #[getter]
    fn center_right(&self) -> Point {
        Point(self.right, (self.bottom + self.top) / 2)
    }
    /// Duplicate a BoundingBox shifted by the given delta.
    ///
    /// Parameters
    /// ----------
    /// delta : Point or tuple of ints
    ///     The (x, y) shift difference.
    ///
    /// Returns
    /// -------
    /// BoundingBox
    ///     A new BoundingBox shifted by the given delta.
    ///
    #[pyo3(name = "duplicate_shifted")]
    fn py_duplicate_shifted(&self, delta: Bound<PyAny>) -> PyResult<Self> {
        Ok(self.duplicate_shifted(Point::extract_bound(&delta)?))
    }
}
#[rustfmt::skip]
impl_op_ex!(+ |a: &BoundingBox, b: &BoundingBox| -> BoundingBox { BoundingBox { top: a.top.max(b.top), right: a.right.max(b.right), bottom: a.bottom.min(b.bottom), left: a.left.min(b.left) } });
#[rustfmt::skip]
impl_op_ex!(+= |a: &mut BoundingBox, b: &BoundingBox| {
        a.top =a.top.max(b.top);
        a.right =a.right.max(b.right);
        a.bottom =a.bottom.min(b.bottom);
        a.left =a.left.min(b.left);

});
#[rustfmt::skip]
impl_op_ex_commutative!(+ |a: &BoundingBox, b: &Point| -> BoundingBox {
        BoundingBox {
            top:a.top.max(b.1),
            right:a.right.max(b.0),
            bottom:a.bottom.min(b.1),
            left:a.left.min(b.0),
        }
});
#[rustfmt::skip]
impl_op_ex!(+= |a: &mut BoundingBox, b: &Point| {
        a.top =a.top.max(b.1);
        a.right =a.right.max(b.0);
        a.bottom =a.bottom.min(b.1);
        a.left =a.left.min(b.0);
});
impl From<(isize, isize, isize, isize)> for BoundingBox {
    fn from(value: (isize, isize, isize, isize)) -> Self {
        Self {
            top: value.0,
            right: value.1,
            bottom: value.2,
            left: value.3,
        }
    }
}
impl From<BoundingBox> for (isize, isize, isize, isize) {
    fn from(value: BoundingBox) -> Self {
        (value.top, value.right, value.bottom, value.left)
    }
}

#[derive(Debug, Clone, Copy)]
enum Color {
    Ansi(AnsiColors),
    Rgb(color_art::Color),
}
impl Default for Color {
    fn default() -> Self {
        Self::Ansi(AnsiColors::Default)
    }
}
impl Color {
    fn is_default(&self) -> bool {
        match self {
            Color::Ansi(ansi_colors) => ansi_colors == &AnsiColors::Default,
            Color::Rgb(_) => false,
        }
    }
    fn or(self, other: Self) -> Self {
        if self.is_default() {
            other
        } else {
            self
        }
    }
    fn update_style_fg(&self, style: Style) -> Style {
        match self {
            Color::Ansi(ansi_colors) => match ansi_colors {
                AnsiColors::Black => style.black(),
                AnsiColors::Red => style.red(),
                AnsiColors::Green => style.green(),
                AnsiColors::Yellow => style.yellow(),
                AnsiColors::Blue => style.blue(),
                AnsiColors::Magenta => style.magenta(),
                AnsiColors::Cyan => style.cyan(),
                AnsiColors::White => style.white(),
                AnsiColors::Default => style.default_color(),
                AnsiColors::BrightBlack => style.bright_black(),
                AnsiColors::BrightRed => style.bright_red(),
                AnsiColors::BrightGreen => style.bright_green(),
                AnsiColors::BrightYellow => style.bright_yellow(),
                AnsiColors::BrightBlue => style.bright_blue(),
                AnsiColors::BrightMagenta => style.bright_magenta(),
                AnsiColors::BrightCyan => style.bright_cyan(),
                AnsiColors::BrightWhite => style.bright_white(),
            },
            Color::Rgb(color) => style.truecolor(color.red(), color.green(), color.blue()),
        }
    }
    fn update_style_bg(&self, style: Style) -> Style {
        match self {
            Color::Ansi(ansi_colors) => match ansi_colors {
                AnsiColors::Black => style.on_black(),
                AnsiColors::Red => style.on_red(),
                AnsiColors::Green => style.on_green(),
                AnsiColors::Yellow => style.on_yellow(),
                AnsiColors::Blue => style.on_blue(),
                AnsiColors::Magenta => style.on_magenta(),
                AnsiColors::Cyan => style.on_cyan(),
                AnsiColors::White => style.on_white(),
                AnsiColors::Default => style.on_default_color(),
                AnsiColors::BrightBlack => style.on_bright_black(),
                AnsiColors::BrightRed => style.on_bright_red(),
                AnsiColors::BrightGreen => style.on_bright_green(),
                AnsiColors::BrightYellow => style.on_bright_yellow(),
                AnsiColors::BrightBlue => style.on_bright_blue(),
                AnsiColors::BrightMagenta => style.on_bright_magenta(),
                AnsiColors::BrightCyan => style.on_bright_cyan(),
                AnsiColors::BrightWhite => style.on_bright_white(),
            },
            Color::Rgb(color) => style.on_truecolor(color.red(), color.green(), color.blue()),
        }
    }
}
impl FromStr for Color {
    type Err = PyErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "black" => Ok(Color::Ansi(AnsiColors::Black)),
            "red" => Ok(Color::Ansi(AnsiColors::Red)),
            "green" => Ok(Color::Ansi(AnsiColors::Green)),
            "yellow" => Ok(Color::Ansi(AnsiColors::Yellow)),
            "blue" => Ok(Color::Ansi(AnsiColors::Blue)),
            "magenta" => Ok(Color::Ansi(AnsiColors::Magenta)),
            "cyan" => Ok(Color::Ansi(AnsiColors::Cyan)),
            "white" => Ok(Color::Ansi(AnsiColors::White)),
            "default" => Ok(Color::Ansi(AnsiColors::Default)),
            "bright_black" => Ok(Color::Ansi(AnsiColors::BrightBlack)),
            "bright_red" => Ok(Color::Ansi(AnsiColors::BrightRed)),
            "bright_green" => Ok(Color::Ansi(AnsiColors::BrightGreen)),
            "bright_yellow" => Ok(Color::Ansi(AnsiColors::BrightYellow)),
            "bright_blue" => Ok(Color::Ansi(AnsiColors::BrightBlue)),
            "bright_magenta" => Ok(Color::Ansi(AnsiColors::BrightMagenta)),
            "bright_cyan" => Ok(Color::Ansi(AnsiColors::BrightCyan)),
            "bright_white" => Ok(Color::Ansi(AnsiColors::BrightWhite)),
            _ => Ok(Color::Rgb(
                s.parse()
                    .map_err(|e| PyValueError::new_err(format!("{}", e)))?,
            )),
        }
    }
}
impl Display for Color {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Color::Ansi(color) => match color {
                    AnsiColors::Black => "black",
                    AnsiColors::Red => "red",
                    AnsiColors::Green => "green",
                    AnsiColors::Yellow => "yellow",
                    AnsiColors::Blue => "blue",
                    AnsiColors::Magenta => "magenta",
                    AnsiColors::Cyan => "cyan",
                    AnsiColors::White => "white",
                    AnsiColors::Default => "default",
                    AnsiColors::BrightBlack => "bright_black",
                    AnsiColors::BrightRed => "bright_red",
                    AnsiColors::BrightGreen => "bright_green",
                    AnsiColors::BrightYellow => "bright_yellow",
                    AnsiColors::BrightBlue => "bright_blue",
                    AnsiColors::BrightMagenta => "bright_magenta",
                    AnsiColors::BrightCyan => "bright_cyan",
                    AnsiColors::BrightWhite => "bright_white",
                }
                .to_string(),
                Color::Rgb(color) => color.hex(),
            }
        )
    }
}
/// Represents a text style with foreground and background colors and text effects.
///
/// Parameters
/// ----------
/// s : str
///     A string representation of the style. Can include color names (e.g., "red", "blue",
///     "bright_green"), hex color codes (e.g., "#RRGGBB"), and effects (e.g., "bold", "italic",
///     "underline"). Effects and colors can be combined (e.g., "bold red on blue",
///     "underline #FF00FF").
///
/// Attributes
/// ----------
/// effects : set of str
///     A set of strings representing the active text effects (e.g., "bold", "italic").
/// fg : str
///     The foreground color of the text.
/// bg : str
///     The background color of the text.
///
/// Examples
/// --------
/// >>> style = Style("bold red on blue")
/// >>> style("Hello")
/// '\x1b[1m\x1b[31m\x1b[44mHello\x1b[49m\x1b[39m\x1b[22m'
/// >>> style = Style("#FF00FF underline")
/// >>> style.fg
/// '#FF00FF'
/// >>> style.effects
/// {'underline'}
///
#[pyclass(name = "Style")]
#[derive(Default, Clone, Debug)]
struct TextStyle {
    effects: HashSet<String>,
    fg: Color,
    bg: Color,
}
#[pymethods]
impl TextStyle {
    #[new]
    fn new(s: &str) -> PyResult<Self> {
        s.parse()
    }
    fn __add__(&self, obj: Bound<PyAny>) -> PyResult<Self> {
        Ok(self.clone() + obj.try_into()?)
    }
    /// TODO:
    fn __call__(&self, text: &str) -> PyResult<String> {
        self.render(text)
    }
    fn __str__(&self) -> String {
        format!(
            "Style(fg={}, bg={}, effects=[{}])",
            self.fg,
            self.bg,
            self.effects
                .clone()
                .into_iter()
                .collect::<Vec<String>>()
                .join(", ")
        )
    }
    #[getter]
    fn get_effects(&self) -> HashSet<String> {
        self.effects.clone()
    }
    #[getter]
    fn get_fg(&self) -> String {
        self.fg.to_string()
    }
    #[getter]
    fn get_bg(&self) -> String {
        self.bg.to_string()
    }
}
impl TextStyle {
    fn render(&self, text: &str) -> PyResult<String> {
        let effects = self
            .effects
            .iter()
            .map(|style| match style.as_str() {
                "bold" => Ok(Effect::Bold),
                "dimmed" => Ok(Effect::Dimmed),
                "italic" => Ok(Effect::Italic),
                "underline" => Ok(Effect::Underline),
                "blink" => Ok(Effect::Blink),
                "blinkfast" => Ok(Effect::BlinkFast),
                "reversed" => Ok(Effect::Reversed),
                "hidden" => Ok(Effect::Hidden),
                "strikethrough" => Ok(Effect::Strikethrough),
                _ => unreachable!(),
            })
            .collect::<PyResult<Vec<_>>>()?;
        let mut style = Style::new().effects(&effects);
        style = self.fg.update_style_fg(style);
        style = self.bg.update_style_bg(style);
        Ok(text.style(style).to_string())
    }
}
impl<'py> TryFrom<Bound<'py, PyAny>> for TextStyle {
    type Error = PyErr;

    fn try_from(value: Bound<PyAny>) -> Result<Self, Self::Error> {
        if let Ok(s) = value.extract::<String>() {
            s.parse()
        } else if let Ok(ts) = value.extract::<TextStyle>() {
            Ok(ts)
        } else {
            Err(PyTypeError::new_err("Expected either a str or a Style"))
        }
    }
}
impl<'a, 'py> TryFrom<&'a Bound<'py, PyAny>> for TextStyle {
    type Error = PyErr;

    fn try_from(value: &'a Bound<PyAny>) -> Result<Self, Self::Error> {
        if let Ok(s) = value.extract::<String>() {
            s.parse()
        } else if let Ok(ts) = value.extract::<TextStyle>() {
            Ok(ts)
        } else {
            Err(PyTypeError::new_err("Expected either a str or a Style"))
        }
    }
}
impl Add for TextStyle {
    type Output = TextStyle;

    fn add(self, rhs: Self) -> Self::Output {
        let mut effects = self.effects;
        effects.extend(rhs.effects);
        let fg = rhs.fg.or(self.fg);
        let bg = rhs.bg.or(self.bg);
        Self { effects, fg, bg }
    }
}
impl AddAssign for TextStyle {
    fn add_assign(&mut self, rhs: Self) {
        self.effects.extend(rhs.effects);
        self.fg = rhs.fg.or(self.fg);
        self.bg = rhs.bg.or(self.bg);
    }
}
impl FromStr for TextStyle {
    type Err = PyErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let all_effects = [
            "bold",
            "dimmed",
            "italic",
            "underline",
            "blinkfast",
            "blink",
            "reversed",
            "hidden",
            "strikethrough",
        ];
        let effects_re = all_effects.join("|");
        let re = Regex::new(&format!(
            r"^(?P<styles>(?:({effects_re})\s*)*)?(?P<fg>#[\da-f]{{6}}|\w+)?(?:\s*on\s+(?P<bg>#[\da-f]{{6}}|\w+))?$"
)).unwrap();
        let mut effects = HashSet::new();
        if let Some(captures) = re.captures(s.to_lowercase().trim()) {
            if let Some(matched_effects) = captures.name("styles") {
                effects = matched_effects
                    .as_str()
                    .split_whitespace()
                    .map(|s| s.to_string())
                    .collect::<HashSet<String>>();
            }
            let mut fg = Color::default();
            if let Some(fg_str) = captures.name("fg").map(|m| m.as_str()) {
                fg = fg_str.parse()?;
            }
            let mut bg = Color::default();
            if let Some(bg_str) = captures.name("bg").map(|m| m.as_str()) {
                bg = bg_str.parse()?;
            }
            return Ok(TextStyle { effects, fg, bg });
        }
        Err(PyValueError::new_err("Failed to parse style string"))
    }
}

/// Represents a single character pixel with a position, style, and weight.
///
/// Parameters
/// ----------
/// character : str
///     The character to display for the pixel.
/// position : Point or tuple of ints, optional
///     The (x, y) coordinates of the pixel.
/// style : str, optional
///     The style (colors, effects) to apply to the character.
/// weight : int, optional
///     An optional weight for the pixel, used for rendering order.
///
/// Attributes
/// ----------
/// character : str
///     The character of the pixel.
/// position : Point
///     The position of the pixel.
/// style : TextStyle
///     The style of the pixel.
/// weight : int or None
///     The weight of the pixel.
///
/// Examples
/// --------
/// >>> pixel = Pixel('A', position=(0, 0), style='red')
/// >>> pixel.character
/// 'A'
///
#[pyclass]
#[derive(Clone, Debug)]
struct Pixel {
    #[pyo3(get, set)]
    character: char,
    #[pyo3(get)]
    position: Point,
    #[pyo3(get, set)]
    style: TextStyle,
    #[pyo3(get, set)]
    weight: Option<usize>,
}
#[pymethods]
impl Pixel {
    #[new]
    #[pyo3(signature = (character, position = None, style = None, *, weight = None))]
    fn new(
        character: char,
        position: Option<Bound<PyAny>>,
        style: Option<String>,
        weight: Option<usize>,
    ) -> PyResult<Self> {
        Ok(Self {
            character,
            position: position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
            style: style.unwrap_or_default().parse()?,
            weight,
        })
    }
    /// Duplicate a Pixel at a given position.
    ///
    /// Parameters
    /// ----------
    /// position : Point or tuple of ints, optional
    ///     The (x, y) coordinates of the new Pixel.
    ///
    /// Returns
    /// -------
    /// Pixel
    ///     A new Pixel at the given position.
    ///
    #[pyo3(name = "duplicate", signature = (position = None))]
    fn py_duplicate(&self, position: Option<Bound<PyAny>>) -> PyResult<Self> {
        Ok(self.duplicate(
            position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
        ))
    }
    /// Duplicate a Pixel shifted by the given delta.
    ///
    /// Parameters
    /// ----------
    /// delta : Point or tuple of ints
    ///     The (x, y) shift difference.
    ///
    /// Returns
    /// -------
    /// Pixel
    ///     A new Pixel shifted by the given delta.
    ///
    #[pyo3(name = "duplicate_shifted")]
    fn py_duplicate_shifted(&self, delta: Bound<PyAny>) -> PyResult<Self> {
        Ok(self.duplicate_shifted(Point::extract_bound(&delta)?))
    }
    fn __str__(&self) -> PyResult<String> {
        self.render()
    }
    #[setter]
    fn set_position(&mut self, point: Bound<PyAny>) -> PyResult<()> {
        self.position = Point::extract_bound(&point)?;
        Ok(())
    }
}
impl Pixel {
    fn render(&self) -> PyResult<String> {
        self.style.render(&self.character.to_string())
    }
    fn with_weight(&self, weight: Option<usize>) -> Self {
        let mut new_pixel = self.clone();
        new_pixel.weight = weight;
        new_pixel
    }
    fn duplicate(&self, position: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position = position;
        new_obj
    }
    fn duplicate_shifted(&self, delta: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position += delta;
        new_obj
    }
}

/// A group of pixels that can be rendered together.
///
/// Parameters
/// ----------
/// pixels : list of Pixel, optional
///     A list of Pixel objects to initialize the group.
/// position : Point or tuple of ints, optional
///     A position to offset the group of pixels.
/// style : str, optional
///     A style to apply to the group of pixels (can overwrite).
/// weight : int, optional
///     A weight to apply to the group of pixels (overwrites if None, otherwise adds to existing pixel weight).
///
/// Attributes
/// ----------
/// pixels : list of Pixel
///     A list of Pixel objects in the group.
/// bbox : BoundingBox
///     The bounding box that encompasses all pixels in the group.
///
/// Examples
/// --------
/// >>> p1 = Pixel('A', (0,0), "red")
/// >>> pg = PixelGroup([p1, p1.at((0, 2))])
/// >>> pg.bbox
/// BoundingBox(top=2, right=0, bottom=0, left=0)
///
#[pyclass(sequence)]
#[derive(Clone)]
struct PixelGroup {
    #[pyo3(get, set)]
    pixels: Vec<Pixel>,
    position: Point,
    style: TextStyle,
    weight: Option<usize>,
}
#[pymethods]
impl PixelGroup {
    #[new]
    #[pyo3(signature = (pixels, position = None, style = None, *, weight = 0))]
    fn new(
        pixels: Vec<Pixel>,
        position: Option<Bound<PyAny>>,
        style: Option<String>,
        weight: Option<usize>,
    ) -> PyResult<Self> {
        Ok(Self {
            pixels,
            position: position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
            style: style.unwrap_or_default().parse()?,
            weight,
        })
    }
    fn __len__(&self) -> usize {
        self.pixels.len()
    }
    fn __getitem__(&self, index: usize) -> Pixel {
        self.pixels[index].clone()
    }
    fn __setitem__(&mut self, index: usize, value: Pixel) {
        self.pixels[index] = value;
    }
    #[getter]
    fn bbox(&self) -> BoundingBox {
        pixels_to_bounding_box(&self.pixels)
    }
    /// Duplicate a PixelGroup at a given position.
    ///
    /// Parameters
    /// ----------
    /// position : Point or tuple of ints, optional
    ///     The (x, y) coordinates of the new PixelGroup.
    ///
    /// Returns
    /// -------
    /// PixelGroup
    ///     A new PixelGroup at the given position.
    ///
    #[pyo3(name = "duplicate", signature = (position = None))]
    fn py_duplicate(&self, position: Option<Bound<PyAny>>) -> PyResult<Self> {
        Ok(self.duplicate(
            position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
        ))
    }
    /// Duplicate a PixelGroup shifted by the given delta.
    ///
    /// Parameters
    /// ----------
    /// delta : Point or tuple of ints
    ///     The (x, y) shift difference.
    ///
    /// Returns
    /// -------
    /// PixelGroup
    ///     A new PixelGroup shifted by the given delta.
    ///
    #[pyo3(name = "duplicate_shifted")]
    fn py_duplicate_shifted(&self, delta: Bound<PyAny>) -> PyResult<Self> {
        Ok(self.duplicate_shifted(Point::extract_bound(&delta)?))
    }
}
impl PixelGroup {
    fn duplicate(&self, position: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position = position;
        new_obj
    }
    fn duplicate_shifted(&self, delta: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position += delta;
        new_obj
    }
}

/// Generate a PixelGroup from a string.
///
/// Parameters
/// ----------
/// text : str
///     The text to convert to a PixelGroup.
/// position : Point or tuple of ints, optional
///     A position to offset the text.
/// style : str, optional
///     A style to apply to the text.
/// weight : int, optional
///     A weight to apply to the text.
///
/// Returns
/// -------
/// PixelGroup
///     A PixelGroup object containing the text.
///
#[pyfunction(signature = (text, position = None, style = None, *, weight = 0))]
fn text(
    text: String,
    position: Option<Bound<PyAny>>,
    style: Option<String>,
    weight: Option<usize>,
) -> PyResult<PixelGroup> {
    Ok(PixelGroup {
        pixels: text
            .chars()
            .enumerate()
            .map(|(i, c)| {
                Ok(Pixel {
                    character: c,
                    position: Point(i as isize, 0),
                    style: style.clone().unwrap_or_default().parse()?,
                    weight: weight.clone(),
                })
            })
            .collect::<PyResult<Vec<_>>>()?,
        position: position
            .map(|p| Point::extract_bound(&p))
            .transpose()?
            .unwrap_or_default(),
        style: style.unwrap_or_default().parse()?,
        weight,
    })
}

fn pixels_to_map(pixels: &[Pixel]) -> HashMap<Point, Pixel> {
    pixels.iter().map(|p| (p.position, p.clone())).collect()
}

fn objs_to_map(args: &Bound<'_, PyAny>) -> PyResult<HashMap<Point, Pixel>> {
    let mut map: HashMap<Point, Pixel> = HashMap::new();
    let objs: Vec<Bound<PyAny>> = if let Ok(it) = args.downcast::<PyTuple>() {
        it.iter().collect()
    } else if let Ok(it) = args.downcast::<PyList>() {
        it.iter().collect()
    } else {
        return Err(PyTypeError::new_err("Expected either a list or a tuple"));
    };
    for obj in objs {
        if let Ok(pixel) = obj.extract::<Pixel>() {
            map.insert(pixel.position, pixel);
        } else if let Ok(group) = obj.extract::<PixelGroup>() {
            for p in &group.pixels {
                let mut new_pixel = p.clone();
                new_pixel.position = new_pixel.position + group.position;
                new_pixel.style += group.style.clone();
                new_pixel.weight = match (new_pixel.weight, group.weight) {
                    (None, _) | (_, None) => None,
                    (Some(w1), Some(w2)) => Some(w1 + w2),
                };
                map.insert(new_pixel.position, new_pixel);
            }
        } else if let Ok(textpath) = obj.extract::<TextPath>() {
            let group = textpath.as_group()?;
            for p in &group.pixels {
                let mut new_pixel = p.clone();
                new_pixel.position = new_pixel.position + group.position;
                new_pixel.style += group.style.clone();
                new_pixel.weight = match (new_pixel.weight, group.weight) {
                    (None, _) | (_, None) => None,
                    (Some(w1), Some(w2)) => Some(w1 + w2),
                };
                map.insert(new_pixel.position, new_pixel);
            }
        } else if let Ok(textbox) = obj.extract::<Box>() {
            let group = textbox.as_group();
            for p in &group.pixels {
                let mut new_pixel = p.clone();
                new_pixel.position = new_pixel.position + group.position;
                new_pixel.style += group.style.clone();
                new_pixel.weight = match (new_pixel.weight, group.weight) {
                    (None, _) | (_, None) => None,
                    (Some(w1), Some(w2)) => Some(w1 + w2),
                };
                map.insert(new_pixel.position, new_pixel);
            }
        } else {
            return Err(PyTypeError::new_err(
                "Expected either Pixels, PixelGroups, TextPaths, or Boxes as arguments",
            ));
        }
    }
    Ok(map)
}

fn map_to_bounding_box(map: &HashMap<Point, Pixel>) -> BoundingBox {
    let min_x = map.keys().map(|p| p.0).min().unwrap_or_default();
    let min_y = map.keys().map(|p| p.1).min().unwrap_or_default();
    let max_x = map.keys().map(|p| p.0).max().unwrap_or_default();
    let max_y = map.keys().map(|p| p.1).max().unwrap_or_default();
    BoundingBox {
        top: max_y,
        right: max_x,
        bottom: min_y,
        left: min_x,
    }
}
fn pixels_to_bounding_box(pixels: &[Pixel]) -> BoundingBox {
    BoundingBox {
        top: pixels
            .iter()
            .map(|p| p.position.1)
            .max()
            .unwrap_or_default(),
        right: pixels
            .iter()
            .map(|p| p.position.0)
            .max()
            .unwrap_or_default(),
        bottom: pixels
            .iter()
            .map(|p| p.position.1)
            .min()
            .unwrap_or_default(),
        left: pixels
            .iter()
            .map(|p| p.position.0)
            .min()
            .unwrap_or_default(),
    }
}

/// Renders a list of objects (TextPath, Box, Pixel, or PixelGroup) into a single string.
///
/// Parameters
/// ----------
/// objs: list
///     A list of objects to render. Each object must be an instance of TextPath, Box, Pixel, or PixelGroup.
/// default_style: str, optional
///     A style to apply to empty space.
///
/// Returns
/// -------
/// str
///     The rendered string with ANSI escape codes.
///
/// Raises
/// ------
/// TypeError
///     If an object in the list is not a TextPath, Box, Pixel, or PixelGroup.
///
/// Examples
/// --------
/// >>> from textdraw import render, text, Style
/// >>> text = text("Hello", (0,0), "green")
/// >>> render([text])
/// '\x1b[32mHello\x1b[39m'
///
#[pyfunction(signature = (objs, default_style = None))]
fn render(objs: Bound<'_, PyAny>, default_style: Option<String>) -> PyResult<String> {
    let map = objs_to_map(&objs)?;
    let bb = map_to_bounding_box(&map);
    let empty_style: TextStyle = default_style
        .map(|s| s.parse())
        .transpose()?
        .unwrap_or_default();
    let empty_space = empty_style.render(" ")?;
    let mut output = String::new();
    for y in (bb.bottom..=bb.top).rev() {
        for x in bb.left..=bb.right {
            if let Some(p) = map.get(&Point(x, y)) {
                output.push_str(&p.render()?);
            } else {
                output.push_str(&empty_space);
            }
        }
        output.push('\n')
    }
    Ok(output)
}
/// Takes a list of objects (TextPath, Box, Pixel, or PixelGroup) and duplicates them shifted by a
/// given delta amount.
///
/// Parameters
/// ----------
/// objects : list
///     A list of objects to duplicate. Each object must be an instance of TextPath, Box, Pixel, or PixelGroup.
/// delta : Point or tuple of ints, optional
///     The (x, y) shift difference.
///
/// Returns
/// -------
/// objects : list
///     Duplicated objects shifted by the given delta.
///
/// Raises
/// ------
/// TypeError
///     If an object in the list is not a TextPath, Box, Pixel, or PixelGroup.
///
#[pyfunction]
fn duplicate_shifted<'py>(
    py: Python<'py>,
    objects: Vec<Bound<'py, PyAny>>,
    delta: Bound<PyAny>,
) -> PyResult<Vec<Bound<'py, PyAny>>> {
    let mut res = Vec::with_capacity(objects.len());
    for obj in objects {
        if let Ok(obj) = obj.extract::<Pixel>() {
            res.push(
                Bound::new(py, obj.py_duplicate_shifted(delta.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else if let Ok(obj) = obj.extract::<PixelGroup>() {
            res.push(
                Bound::new(py, obj.py_duplicate_shifted(delta.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else if let Ok(obj) = obj.extract::<TextPath>() {
            res.push(
                Bound::new(py, obj.py_duplicate_shifted(delta.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else if let Ok(obj) = obj.extract::<Box>() {
            res.push(
                Bound::new(py, obj.py_duplicate_shifted(delta.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else {
            return Err(PyTypeError::new_err(
                "Expected objects to be a list of Pixels, PixelGroups, TextPaths, and/or Boxes",
            ));
        }
    }
    Ok(res)
}

/// Takes a list of objects (TextPath, Box, Pixel, or PixelGroup) and duplicates them at a new
/// location.
///
/// Parameters
/// ----------
/// objects : list
///     A list of objects to duplicate. Each object must be an instance of TextPath, Box, Pixel, or PixelGroup.
///
/// Returns
/// -------
/// objects : list
///     Duplicated objects at the specified location.
///
/// Raises
/// ------
/// TypeError
///     If an object in the list is not a TextPath, Box, Pixel, or PixelGroup.
///
#[pyfunction]
fn duplicate<'py>(
    py: Python<'py>,
    objects: Vec<Bound<'py, PyAny>>,
    position: Option<Bound<PyAny>>,
) -> PyResult<Vec<Bound<'py, PyAny>>> {
    let mut res = Vec::with_capacity(objects.len());
    for obj in objects {
        if let Ok(obj) = obj.extract::<Pixel>() {
            res.push(
                Bound::new(py, obj.py_duplicate(position.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else if let Ok(obj) = obj.extract::<PixelGroup>() {
            res.push(
                Bound::new(py, obj.py_duplicate(position.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else if let Ok(obj) = obj.extract::<TextPath>() {
            res.push(
                Bound::new(py, obj.py_duplicate(position.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else if let Ok(obj) = obj.extract::<Box>() {
            res.push(
                Bound::new(py, obj.py_duplicate(position.clone())?)?
                    .as_any()
                    .clone(),
            );
        } else {
            return Err(PyTypeError::new_err(
                "Expected objects to be a list of Pixels, PixelGroups, TextPaths, and/or Boxes",
            ));
        }
    }
    Ok(res)
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, Default)]
enum Direction {
    #[default]
    Up,
    Right,
    Down,
    Left,
}
impl Direction {
    fn delta(self) -> Point {
        match self {
            Direction::Up => (0, 1),
            Direction::Right => (1, 0),
            Direction::Down => (0, -1),
            Direction::Left => (-1, 0),
        }
        .into()
    }

    fn all() -> [Direction; 4] {
        [
            Direction::Up,
            Direction::Right,
            Direction::Down,
            Direction::Left,
        ]
    }
}
impl Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Direction::Up => "up",
                Direction::Right => "right",
                Direction::Down => "down",
                Direction::Left => "left",
            }
        )
    }
}
impl FromStr for Direction {
    type Err = PyErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "up" => Ok(Direction::Up),
            "right" => Ok(Direction::Right),
            "down" => Ok(Direction::Down),
            "left" => Ok(Direction::Left),
            _ => Err(PyValueError::new_err("Invalid direction")),
        }
    }
}

#[derive(Clone, Copy, Default)]
enum LineStyle {
    #[default]
    Light,
    Heavy,
    Double,
}
impl LineStyle {
    fn get_char(&self, neighbors: (bool, bool, bool, bool)) -> char {
        let chars: Vec<char> = match self {
            LineStyle::Light => " ─│┐──┌┬│┘│┤└┴├┼",
            LineStyle::Heavy => " ━┃┓━━┏┳┃┛┃┫┗┻┣╋",
            LineStyle::Double => " ═║╗══╔╦║╝║╣╚╩╠╬",
        }
        .to_string()
        .chars()
        .collect();
        let index = (neighbors.0 as usize) << 3
            | (neighbors.1 as usize) << 2
            | (neighbors.2 as usize) << 1
            | (neighbors.3 as usize);
        chars[index]
    }
}
impl Display for LineStyle {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                LineStyle::Light => "light",
                LineStyle::Heavy => "heavy",
                LineStyle::Double => "double",
            }
        )
    }
}
impl FromStr for LineStyle {
    type Err = PyErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "light" => Ok(LineStyle::Light),
            "heavy" => Ok(LineStyle::Heavy),
            "double" => Ok(LineStyle::Double),
            other => Err(PyValueError::new_err(format!(
                "Invalid line style [{}]",
                other
            ))),
        }
    }
}

#[derive(Clone, Copy, Default)]
enum ArrowType {
    #[default]
    Arrow,
    OpenArrow,
    Custom {
        up: char,
        right: char,
        down: char,
        left: char,
    },
}
impl ArrowType {
    fn render(&self, direction: &Direction) -> String {
        match self {
            ArrowType::Arrow => match direction {
                Direction::Up => "▲",
                Direction::Right => "▶",
                Direction::Down => "▼",
                Direction::Left => "◀",
            }
            .to_string(),
            ArrowType::OpenArrow => match direction {
                Direction::Up => "△",
                Direction::Right => "▷",
                Direction::Down => "▽",
                Direction::Left => "◁",
            }
            .to_string(),
            ArrowType::Custom {
                up,
                right,
                down,
                left,
            } => match direction {
                Direction::Up => up,
                Direction::Right => right,
                Direction::Down => down,
                Direction::Left => left,
            }
            .to_string(),
        }
    }
}

/// Parses a string to generate an arrow-like character
///
/// This is intended to be used with the Pixel class to render a
/// styled arrow. Eventually the TextPath class will support arrow
/// endings in a more convenient manner, but for now, they must be
/// placed manually.
///
/// The arrow format is a direction ('up', 'right', 'down', or 'left')
/// followed by an arrow type ('arrow', 'openarrow', or 'custom[<chars>]'),
/// where the first of these lists will be used if either part is ommitted.
///
/// Custom characters can be used by specifying them inside the 'custom[<chars>]'
/// brackets, so 'custom[urdl]' would give unique letters for each direction and
/// 'custom[X]' would use 'X' for every direction. Right now, this is not very
/// useful, but it is the format which will be used in the TextPath class in a
/// future update.
///
/// Parameters
/// ----------
/// fmt : str
///     The arrow format string.
///
/// Returns
/// -------
/// str
///     The parsed arrow character.
///
/// Examples
/// --------
/// >>> from textdraw import arrow
/// >>> print(arrow("up arrow"))
/// '▲'
///
#[pyfunction]
fn arrow(fmt: &str) -> PyResult<String> {
    let all_arrow_types = ["openarrow", "arrow", "custom"];
    let arrow_types_re = all_arrow_types.join("|");
    let re = Regex::new(&format!(
            r"^(?P<direction>(?:(up|right|down|left))\s*)?(?P<arrows>(?:({arrow_types_re}))|(custom\[(?P<customs>.{{4}})\])|(custom\[(?P<custom>.)\])\s*)?$"
)).unwrap();
    let mut direction = Direction::default();
    let mut arrow = ArrowType::default();
    if let Some(captures) = re.captures(fmt.to_lowercase().trim()) {
        if let Some(matched_direction) = captures.name("direction") {
            match matched_direction.as_str() {
                "up" => direction = Direction::Up,
                "right" => direction = Direction::Right,
                "down" => direction = Direction::Down,
                "left" => direction = Direction::Left,
                _ => unreachable!(),
            }
        }
        if let Some(matched_arrow) = captures.name("arrows") {
            match matched_arrow.as_str() {
                "arrow" => arrow = ArrowType::Arrow,
                "openarrow" => arrow = ArrowType::OpenArrow,
                _ => {
                    if let Some(matched_custom) = captures.name("custom") {
                        let custom_char = matched_custom.as_str().chars().next().unwrap();
                        arrow = ArrowType::Custom {
                            up: custom_char,
                            right: custom_char,
                            down: custom_char,
                            left: custom_char,
                        }
                    } else if let Some(matched_customs) = captures.name("customs") {
                        let custom_chars = matched_customs.as_str().chars().collect::<Vec<char>>();
                        arrow = ArrowType::Custom {
                            up: custom_chars[0],
                            right: custom_chars[1],
                            down: custom_chars[2],
                            left: custom_chars[3],
                        }
                    } else {
                        unreachable!()
                    }
                }
            }
        }
        return Ok(arrow.render(&direction));
    }
    Err(PyValueError::new_err("Failed to parse style string"))
}

#[derive(Eq, PartialEq)]
struct State {
    cost: usize,
    pos: Point,
    dir: Option<Direction>,
}
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
    }
}
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// A set of pixels which represent a path between two points.
///
/// Parameters
/// ----------
/// start : Point or tuple of ints
///     The starting point of the path.
/// end : Point or tuple of ints
///     The ending point of the path.
/// position : Point or tuple of ints, optional
///     The (x, y) coordinates of the new TextPath.
/// style : str, optional
///     The style to apply to the path.
/// line_style : {'light', 'heavy', 'double'}, optional
///     The set of characters to use for the path.
/// weight : int, optional
///     The weights to apply to each pixel in the path.
/// start_direction : {'up', 'right', 'down', 'left'}, optional
///     The direction to use for the start pixel.
/// end_direction : {'up', 'right', 'down', 'left'}, optional
///     The direction to use for the end pixel.
/// bend_penalty : int, default=1
///     The penalty weight to apply to bends in the path.
/// environment : list
///     A list of objects (TextPath, Box, Pixel, or PixelGroup) which the pathfinding algorithm can
///     see with their given weights.
/// barriers : list
///     A list of objects (TextPath, Box, Pixel, or PixelGroup) which the pathfinding algorithm
///     considers impassible.
/// paths : list
///     A list of objects (TextPath, Box, Pixel, or PixelGroup) which the pathfinding algorithm
///     will try to follow (these objects have no additional weight cost but also count when
///     determining neighbors for generating path characters).
/// bbox : BoundingBox, optional
///     If provided, limits the search to the bounding box.
///
/// Attributes
/// ----------
/// style : Style
///     The style to apply to the path.
/// line_style : {'light', 'heavy', 'double'}
///     The set of characters to use for the path.
/// weight : int or None
///     The weight to apply to each pixel in the path.
/// start_direction : {'up', 'right', 'down', 'left'} or None
///     The direction to use for the start pixel.
/// end_direction : {'up', 'right', 'down', 'left'} or None
///     The direction to use for the end pixel.
///
/// Examples
/// --------
/// >>> from textdraw import TextPath, render
/// >>> p = TextPath((0, 0), (3, 5))
/// >>> print(render(p))
/// ┌──╴
/// │
/// │
/// │
/// │
/// ╵
///
///

#[pyclass]
#[derive(Clone)]
struct TextPath {
    path: Vec<Point>,
    #[pyo3(get, set)]
    position: Point,
    #[pyo3(get, set)]
    style: TextStyle,
    line_style: LineStyle,
    #[pyo3(get, set)]
    weight: Option<usize>,
    start_direction: Option<Direction>,
    end_direction: Option<Direction>,
    start: Point,
    end: Point,
    paths: HashMap<Point, Pixel>,
    #[pyo3(get)]
    cost: usize,
}

#[pymethods]
impl TextPath {
    #[new]
    #[pyo3(signature = (start, end, position = None, style = None, *, line_style = "light".to_string(), weight = None, start_direction = None, end_direction = None, bend_penalty = 1, environment = None, barriers = None, paths = None, bbox = None))]
    fn new(
        py: Python,
        start: Bound<PyAny>,
        end: Bound<PyAny>,
        position: Option<Bound<PyAny>>,
        style: Option<String>,
        line_style: String,
        weight: Option<usize>,
        start_direction: Option<String>,
        end_direction: Option<String>,
        bend_penalty: usize,
        environment: Option<Bound<'_, PyAny>>,
        barriers: Option<Bound<'_, PyAny>>,
        paths: Option<Bound<'_, PyAny>>,
        bbox: Option<Bound<'_, PyAny>>,
    ) -> PyResult<Self> {
        let start = Point::extract_bound(&start)?;
        let end = Point::extract_bound(&end)?;
        let environment = objs_to_map(&environment.unwrap_or(PyTuple::empty(py).as_any().clone()))?;
        let barriers = objs_to_map(&barriers.unwrap_or(PyTuple::empty(py).as_any().clone()))?;
        let paths = objs_to_map(&paths.unwrap_or(PyTuple::empty(py).as_any().clone()))?;
        let bbox = bbox
            .map(|bb| {
                if let Ok(boundingbox) = bb.extract::<BoundingBox>() {
                    Ok(boundingbox)
                } else if let Ok(tuple_bbox) = bb.extract::<(isize, isize, isize, isize)>() {
                    Ok(BoundingBox::new(
                        tuple_bbox.0,
                        tuple_bbox.1,
                        tuple_bbox.2,
                        tuple_bbox.3,
                    ))
                } else {
                    return Err(PyValueError::new_err(
                        "bbox must be a BoundingBox or a tuple[int, int, int, int]",
                    ));
                }
            })
            .transpose()?;
        TextPath::calculate_path(
            start,
            end,
            position.map(|p| Point::extract_bound(&p)).transpose()?,
            style,
            line_style,
            weight,
            start_direction,
            end_direction,
            bend_penalty,
            &environment,
            &barriers,
            &paths,
            bbox,
        )
    }
    #[getter]
    fn get_start_direction(&self) -> String {
        self.start_direction
            .map_or("None".to_string(), |d| d.to_string())
    }
    #[setter]
    fn set_start_direction(&mut self, start_direction: Option<String>) -> PyResult<()> {
        self.start_direction = start_direction.map(|s| s.parse()).transpose()?;
        Ok(())
    }
    #[getter]
    fn get_end_direction(&self) -> String {
        self.end_direction
            .map_or("None".to_string(), |d| d.to_string())
    }
    #[setter]
    fn set_end_direction(&mut self, end_direction: Option<String>) -> PyResult<()> {
        self.end_direction = end_direction.map(|s| s.parse()).transpose()?;
        Ok(())
    }
    #[getter]
    fn get_line_style(&self) -> String {
        self.line_style.to_string()
    }
    #[setter]
    fn set_line_style(&mut self, line_style: String) -> PyResult<()> {
        self.line_style = line_style.parse()?;
        Ok(())
    }
    #[getter]
    fn get_bbox(&self) -> BoundingBox {
        let mut bbox = BoundingBox::default();
        for point in &self.path {
            bbox += point;
        }
        bbox
    }
    /// Duplicate a TextPath at a given position.
    ///
    /// Parameters
    /// ----------
    /// position : Point or tuple of ints, optional
    ///     The (x, y) coordinates of the new TextPath.
    ///
    /// Returns
    /// -------
    /// TextPath
    ///     A new TextPath at the given position.
    ///
    #[pyo3(name = "duplicate", signature = (position = None))]
    fn py_duplicate(&self, position: Option<Bound<PyAny>>) -> PyResult<Self> {
        Ok(self.duplicate(
            position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
        ))
    }
    /// Duplicate a TextPath shifted by the given delta.
    ///
    /// Parameters
    /// ----------
    /// delta : Point or tuple of ints
    ///     The (x, y) shift difference.
    ///
    /// Returns
    /// -------
    /// TextPath
    ///     A new TextPath shifted by the given delta.
    ///
    #[pyo3(name = "duplicate_shifted")]
    fn py_duplicate_shifted(&self, delta: Bound<PyAny>) -> PyResult<Self> {
        Ok(self.duplicate_shifted(Point::extract_bound(&delta)?))
    }
}
impl TextPath {
    fn duplicate(&self, position: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position = position;
        new_obj
    }
    fn duplicate_shifted(&self, delta: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position += delta;
        new_obj
    }
    fn calculate_path(
        start: Point,
        end: Point,
        position: Option<Point>,
        style: Option<String>,
        line_style: String,
        weight: Option<usize>,
        start_direction: Option<String>,
        end_direction: Option<String>,
        bend_penalty: usize,
        environment: &HashMap<Point, Pixel>,
        barriers: &HashMap<Point, Pixel>,
        paths: &HashMap<Point, Pixel>,
        bbox: Option<BoundingBox>,
    ) -> PyResult<Self> {
        let mut environment = environment.clone();
        for (pos, pixel) in barriers {
            environment.insert(*pos, pixel.with_weight(None));
        }
        for (pos, pixel) in paths {
            environment.insert(*pos, pixel.with_weight(Some(0)));
        }
        let mut bb = bbox.unwrap_or(map_to_bounding_box(&environment));
        bb += start;
        bb += end;
        let mut heap = BinaryHeap::new();
        let mut came_from = HashMap::new();
        let mut cost_so_far = HashMap::new();

        heap.push(State {
            cost: 0,
            pos: start,
            dir: None,
        });
        cost_so_far.insert(start, 0);
        while let Some(State { cost, pos, dir }) = heap.pop() {
            if pos == end {
                let mut path = vec![pos];
                let mut current = (pos, dir);
                while let Some(&(previous_pos, previous_dir)) = came_from.get(&current) {
                    path.push(previous_pos);
                    current = (previous_pos, previous_dir);
                }
                path.reverse();
                return Ok(Self {
                    path,
                    position: position.unwrap_or_default(),
                    style: style.unwrap_or_default().parse()?,
                    line_style: line_style.parse()?,
                    weight,
                    start_direction: start_direction.map(|s| s.parse().unwrap()),
                    end_direction: end_direction.map(|s| s.parse().unwrap()),
                    start,
                    end,
                    paths: paths.clone(),
                    cost,
                });
            }

            for new_dir in Direction::all() {
                let delta = new_dir.delta();
                let next = pos + delta;
                if !bb.contains_point(&next) {
                    continue;
                }
                let weight = match environment.get(&next) {
                    Some(Pixel { weight: None, .. }) => continue,
                    Some(Pixel {
                        weight: Some(w), ..
                    }) => *w,
                    None => 1,
                };
                let bend_cost = if Some(new_dir) != dir && dir.is_some() {
                    bend_penalty
                } else {
                    0
                };
                let new_cost = cost + weight + bend_cost;
                let entry = cost_so_far.entry(next).or_insert(usize::MAX);
                let heuristic = |pos: Point| -> usize {
                    ((end.0 - pos.0).abs() + (end.1 - pos.1).abs()) as usize
                };
                if new_cost < *entry {
                    *entry = new_cost;
                    heap.push(State {
                        cost: new_cost + heuristic(next),
                        pos: next,
                        dir: Some(new_dir),
                    });
                    came_from.insert((next, Some(new_dir)), (pos, dir));
                }
            }
        }
        Err(PyValueError::new_err("No path found"))
    }
    fn as_group(&self) -> PyResult<PixelGroup> {
        let mut path_map: HashSet<Point> = self.path.clone().into_iter().collect();
        for (pos, _) in self.paths.iter() {
            path_map.insert(*pos);
        }
        if let Some(start_dir) = self.start_direction {
            path_map.insert(self.start + start_dir.delta());
        }
        if let Some(end_dir) = self.end_direction {
            path_map.insert(self.end + end_dir.delta());
        }
        let path_neighbors: Vec<(bool, bool, bool, bool)> = self
            .path
            .iter()
            .map(|pos| {
                (
                    path_map.contains(&(pos + Direction::Up.delta())),
                    path_map.contains(&(pos + Direction::Right.delta())),
                    path_map.contains(&(pos + Direction::Down.delta())),
                    path_map.contains(&(pos + Direction::Left.delta())),
                )
            })
            .collect();
        let pixels = self
            .path
            .iter()
            .zip(path_neighbors)
            .map(|(pos, n)| Pixel {
                character: self.line_style.get_char(n),
                position: *pos,
                weight: self.weight,
                style: self.style.clone(),
            })
            .collect();
        Ok(PixelGroup {
            pixels,
            position: self.position,
            style: TextStyle::default(),
            weight: Some(0),
        })
    }
}

/// Generate a list of TextPaths between multiple start and end points.
///
/// Parameters
/// ----------
/// start : list of Point or tuple of ints
///     The starting point of the path.
/// end : list of Point or tuple of ints
///     The ending point of the path.
/// style : str, optional
///     The style to apply to the path.
/// line_style : {'light', 'heavy', 'double'}, optional
///     The set of characters to use for the path.
/// weight : int, optional
///     The weights to apply to each pixel in the path.
/// start_direction : list of {'up', 'right', 'down', 'left'}, optional
///     The direction to use for the start pixel.
/// end_direction : list of {'up', 'right', 'down', 'left'}, optional
///     The direction to use for the end pixel.
/// bend_penalty : int, default=1
///     The penalty weight to apply to bends in the path.
/// environment : list
///     A list of objects (TextPath, Box, Pixel, or PixelGroup) which the pathfinding algorithm can
///     see with their given weights.
/// barriers : list
///     A list of objects (TextPath, Box, Pixel, or PixelGroup) which the pathfinding algorithm
///     considers impassible.
/// paths : list
///     A list of objects (TextPath, Box, Pixel, or PixelGroup) which the pathfinding algorithm
///     will try to follow (these objects have no additional weight cost but also count when
///     determining neighbors for generating path characters).
/// bbox : BoundingBox, optional
///     If provided, limits the search to the bounding box.
/// optimize : bool, default=False
///     If True, iterate through all permutations of path orderings to minimize total cost.
///
#[pyfunction]
#[pyo3(signature = (starts, ends, position = None, style = None, *, line_style = "light".to_string(), weight = None, start_directions = None, end_directions = None, bend_penalty = 1, environment = None, barriers = None, paths = None, bbox = None, optimize = false))]
fn multipath(
    py: Python,
    starts: Bound<PyAny>,
    ends: Bound<PyAny>,
    position: Option<Bound<PyAny>>,
    style: Option<String>,
    line_style: String,
    weight: Option<usize>,
    start_directions: Option<Vec<Option<String>>>,
    end_directions: Option<Vec<Option<String>>>,
    bend_penalty: usize,
    environment: Option<Bound<'_, PyAny>>,
    barriers: Option<Bound<'_, PyAny>>,
    paths: Option<Bound<'_, PyAny>>,
    bbox: Option<Bound<'_, PyAny>>,
    optimize: bool,
) -> PyResult<Vec<TextPath>> {
    let starts: Vec<Point> = starts
        .downcast::<PyList>()?
        .iter()
        .map(|p| Point::extract_bound(&p))
        .collect::<PyResult<Vec<_>>>()?;
    let ends: Vec<Point> = ends
        .downcast::<PyList>()?
        .iter()
        .map(|p| Point::extract_bound(&p))
        .collect::<PyResult<Vec<_>>>()?;
    if starts.len() != ends.len() {
        return Err(PyValueError::new_err(
            "The number of start and end points must be equal",
        ));
    }
    let position = position.map(|p| Point::extract_bound(&p)).transpose()?;
    let start_directions = start_directions.unwrap_or(vec![None; starts.len()]);
    if starts.len() != start_directions.len() {
        return Err(PyValueError::new_err(
            "The number of start points and starting directions must be equal",
        ));
    }
    let end_directions = end_directions.unwrap_or(vec![None; ends.len()]);
    if ends.len() != end_directions.len() {
        return Err(PyValueError::new_err(
            "The number of end points and ending directions must be equal",
        ));
    }
    let environment = objs_to_map(&environment.unwrap_or(PyTuple::empty(py).as_any().clone()))?;
    let barriers = objs_to_map(&barriers.unwrap_or(PyTuple::empty(py).as_any().clone()))?;
    let paths = objs_to_map(&paths.unwrap_or(PyTuple::empty(py).as_any().clone()))?;
    let bbox = bbox
        .map(|bb| {
            if let Ok(boundingbox) = bb.extract::<BoundingBox>() {
                Ok(boundingbox)
            } else if let Ok(tuple_bbox) = bb.extract::<(isize, isize, isize, isize)>() {
                Ok(BoundingBox::new(
                    tuple_bbox.0,
                    tuple_bbox.1,
                    tuple_bbox.2,
                    tuple_bbox.3,
                ))
            } else {
                return Err(PyValueError::new_err(
                    "bbox must be a BoundingBox or a tuple[int, int, int, int]",
                ));
            }
        })
        .transpose()?;
    let mut best_paths: Vec<TextPath> = Vec::with_capacity(starts.len());
    let mut best_cost: usize = usize::MAX;
    let order: Vec<usize> = (0..starts.len()).collect();
    let permutations = if optimize {
        order
            .iter()
            .permutations(order.len())
            .map(|p| p.into_iter().copied().collect())
            .collect_vec()
    } else {
        vec![order]
    };
    for permutation in permutations {
        let mut local_cost = 0;
        let mut local_paths: Vec<TextPath> = Vec::with_capacity(starts.len());
        let mut local_groups: Vec<PixelGroup> = Vec::with_capacity(starts.len());
        for i in permutation {
            let local_path_map: HashMap<Point, Pixel> = local_groups
                .iter()
                .map(|g| pixels_to_map(&g.pixels))
                .flatten()
                .collect();
            let all_paths = local_path_map
                .into_iter()
                .chain(paths.clone().into_iter())
                .collect();
            let textpath = TextPath::calculate_path(
                starts[i],
                ends[i],
                position,
                style.clone(),
                line_style.clone(),
                weight,
                start_directions[i].clone(),
                end_directions[i].clone(),
                bend_penalty,
                &environment,
                &barriers,
                &all_paths,
                bbox,
            )?;
            local_cost += textpath.cost;
            local_groups.push(textpath.as_group()?);
            local_paths.push(textpath);
        }
        if local_cost < best_cost {
            best_cost = local_cost;
            best_paths = local_paths;
        }
    }
    Ok(best_paths)
}

#[derive(Clone, Copy, Default)]
enum Alignment {
    #[default]
    Top,
    Center,
    Bottom,
}
impl FromStr for Alignment {
    type Err = PyErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "top" => Ok(Alignment::Top),
            "center" => Ok(Alignment::Center),
            "bottom" => Ok(Alignment::Bottom),
            _ => Err(PyValueError::new_err("Invalid alignment")),
        }
    }
}
impl Display for Alignment {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Alignment::Top => "top",
                Alignment::Center => "center",
                Alignment::Bottom => "bottom",
            }
        )
    }
}
#[derive(Clone, Copy, Default)]
enum Justification {
    #[default]
    Right,
    Center,
    Left,
}
impl FromStr for Justification {
    type Err = PyErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "right" => Ok(Justification::Right),
            "center" => Ok(Justification::Center),
            "left" => Ok(Justification::Left),
            _ => Err(PyValueError::new_err("Invalid alignment")),
        }
    }
}
impl Display for Justification {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Justification::Right => "right",
                Justification::Center => "center",
                Justification::Left => "left",
            }
        )
    }
}

/// A box which can contain some text in a border.
///
/// Parameters
/// ----------
/// text : str, default=''
///     The text contained in the box.
/// position : Point or tuple of ints, optional
///     The position of the box (bottom-left corner).
/// width : int, optional
///     The width of the box (automatically determined by text if None).
/// height : int, optional
///     The height of the box (automatically determined by text if None).
/// style : str, optional
///     The style to apply to the text.
/// border_style : str, optional
///     The style to apply to the border.
/// line_style : {'light', 'heavy', 'double'}, optional
///     The set of characters to use for the border.
/// weight : int, optional
///     The weight to apply to each pixel in the box.
/// padding : tuple of ints, default=(0, 1, 0, 1)
///     The padding applied to each side of the text (top, right, bottom, left).
/// padding_style : str, optional
///     The style to apply to the padding.
/// align : {'top', 'center', 'bottom'}
///     The alignment of the text in the box.
/// justify : {'left', 'center', 'right'}
///     The justification of the text in the box.
/// truncate_string : str, optional
///     String to use if text is truncated.
/// transparent : bool, default=False
///     If True, the space inside the bounding box of the text will be transparent.
/// transparent_padding : bool, default=False
///     If True, the padding space will be transparent.
///
/// Attributes
/// ----------
/// text : str
///     The text contained in the box.
/// position : Point or None
///     The position of the box (bottom-left corner).
/// width : int or None
///     The width of the box (automatically determined by text if None).
/// height : int or None
///     The height of the box (automatically determined by text if None).
/// style : str or None
///     The style to apply to the text.
/// border_style : str or None
///     The style to apply to the border.
/// line_style : {'light', 'heavy', 'double'} or None
///     The set of characters to use for the border.
/// weight : int or None
///     The weight to apply to each pixel in the box.
/// padding : tuple of ints
///     The padding applied to each side of the text (top, right, bottom, left).
/// padding_style : str or None
///     The style to apply to the padding.
/// align : {'top', 'center', 'bottom'}
///     The alignment of the text in the box.
/// justify : {'left', 'center', 'right'}
///     The justification of the text in the box.
/// truncate_string : str or None
///     String to use if text is truncated.
/// transparent : bool
///     If True, the space inside the bounding box of the text will be transparent.
/// transparent_padding : bool
///     If True, the padding space will be transparent.
/// bbox : BoundingBox
///     The bounding box of the box itself.
///
#[pyclass]
#[derive(Clone)]
struct Box {
    #[pyo3(get, set)]
    text: String,
    #[pyo3(get, set)]
    position: Point,
    #[pyo3(get, set)]
    width: Option<usize>,
    #[pyo3(get, set)]
    height: Option<usize>,
    #[pyo3(get, set)]
    style: TextStyle,
    #[pyo3(get, set)]
    border_style: TextStyle,
    line_style: Option<LineStyle>,
    #[pyo3(get, set)]
    weight: Option<usize>,
    #[pyo3(get, set)]
    padding: Option<(usize, usize, usize, usize)>,
    #[pyo3(get, set)]
    padding_style: TextStyle,
    align: Alignment,
    justify: Justification,
    #[pyo3(get, set)]
    truncate_string: Option<String>,
    #[pyo3(get, set)]
    transparent: bool,
    #[pyo3(get, set)]
    transparent_padding: bool,
}
#[pymethods]
impl Box {
    #[new]
    #[pyo3(signature = (text = "", position = None, width = None, height = None, style = None, *, border_style = None, line_style = Some("light".to_string()), weight = 1, padding = None, padding_style = None, align = "top", justify= "left", truncate_string = None, transparent = false, transparent_padding = false))]
    fn new(
        text: &str,
        position: Option<Bound<PyAny>>,
        width: Option<usize>,
        height: Option<usize>,
        style: Option<String>,
        border_style: Option<String>,
        line_style: Option<String>,
        weight: Option<usize>,
        padding: Option<(usize, usize, usize, usize)>,
        padding_style: Option<String>,
        align: &str,
        justify: &str,
        truncate_string: Option<String>,
        transparent: bool,
        transparent_padding: bool,
    ) -> PyResult<Self> {
        let pad = padding.unwrap_or_default();
        if let Some(w) = width {
            let min_width = pad.1 + pad.3 + 2;
            if w < min_width {
                return Err(PyValueError::new_err(format!(
                    "Width {} is too small. Minimum width with current padding is {}",
                    w, min_width
                )));
            }
        }

        if let Some(h) = height {
            let min_height = pad.0 + pad.2 + 2;
            if h < min_height {
                return Err(PyValueError::new_err(format!(
                    "Height {} is too small. Minimum height with current padding is {}",
                    h, min_height
                )));
            }
        }
        Ok(Self {
            text: text.to_string(),
            position: position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
            width,
            height,
            style: style.unwrap_or_default().parse()?,
            border_style: border_style.unwrap_or_default().parse()?,
            line_style: line_style.map(|s| s.parse()).transpose()?,
            weight,
            padding,
            padding_style: padding_style.unwrap_or_default().parse()?,
            align: align.parse()?,
            justify: justify.parse()?,
            truncate_string,
            transparent,
            transparent_padding,
        })
    }
    #[getter]
    fn get_line_style(&self) -> Option<String> {
        self.line_style.map(|s| s.to_string())
    }
    #[setter]
    fn set_line_style(&mut self, line_style: Option<String>) -> PyResult<()> {
        self.line_style = line_style.map(|s| s.parse()).transpose()?;
        Ok(())
    }
    #[getter]
    fn get_align(&self) -> String {
        self.align.to_string()
    }
    #[setter]
    fn set_align(&mut self, align: String) -> PyResult<()> {
        self.align = align.parse()?;
        Ok(())
    }
    #[getter]
    fn get_justify(&self) -> String {
        self.justify.to_string()
    }
    #[setter]
    fn set_justify(&mut self, justify: String) -> PyResult<()> {
        self.justify = justify.parse()?;
        Ok(())
    }
    #[getter]
    fn get_bbox(&self) -> BoundingBox {
        let (_, bbox) = self.format_box();
        bbox
    }
    #[getter]
    fn get_text_bbox(&self) -> BoundingBox {
        let (_, bbox) = self.format_text();
        bbox
    }
    /// Duplicate a Box at a given position.
    ///
    /// Parameters
    /// ----------
    /// position : Point or tuple of ints, optional
    ///     The (x, y) coordinates of the new Box.
    ///
    /// Returns
    /// -------
    /// Box
    ///     A new Box at the given position.
    ///
    #[pyo3(name = "duplicate", signature = (position = None))]
    fn py_duplicate(&self, position: Option<Bound<PyAny>>) -> PyResult<Self> {
        Ok(self.duplicate(
            position
                .map(|p| Point::extract_bound(&p))
                .transpose()?
                .unwrap_or_default(),
        ))
    }
    /// Duplicate a Box shifted by the given delta.
    ///
    /// Parameters
    /// ----------
    /// delta : Point or tuple of ints
    ///     The (x, y) shift difference.
    ///
    /// Returns
    /// -------
    /// Box
    ///     A new Box shifted by the given delta.
    ///
    #[pyo3(name = "duplicate_shifted")]
    fn py_duplicate_shifted(&self, delta: Bound<PyAny>) -> PyResult<Self> {
        Ok(self.duplicate_shifted(Point::extract_bound(&delta)?))
    }
}
impl Box {
    fn duplicate(&self, position: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position = position;
        new_obj
    }
    fn duplicate_shifted(&self, delta: Point) -> Self {
        let mut new_obj = self.clone();
        new_obj.position += delta;
        new_obj
    }
    fn format_box(&self) -> (HashMap<Point, Pixel>, BoundingBox) {
        let padding = self.padding.unwrap_or_default();
        let (text, bb_text) = self.format_text();
        let (total_width, total_height) = if let (Some(w), Some(h)) = (self.width, self.height) {
            (w, h)
        } else {
            let width = self
                .width
                .unwrap_or_else(|| bb_text.width() as usize + padding.1 + padding.3 + 2);
            let height = self
                .height
                .unwrap_or_else(|| bb_text.height() as usize + padding.0 + padding.2 + 2);
            (width, height)
        };
        let bb_border = BoundingBox::new(
            self.position.1 + total_height as isize - 1,
            self.position.0 + total_width as isize - 1,
            self.position.1,
            self.position.0,
        );
        let mut pixels: HashMap<Point, Pixel> = bb_border.as_map(
            &self.border_style,
            &self.padding_style,
            self.line_style,
            self.weight,
            self.transparent_padding,
        );
        pixels.extend(text);
        (pixels, bb_border)
    }
    fn as_group(&self) -> PixelGroup {
        PixelGroup {
            pixels: self.format_box().0.into_values().collect(),
            position: Point::default(),
            style: TextStyle::default(),
            weight: self.weight,
        }
    }
    fn format_text(&self) -> (HashMap<Point, Pixel>, BoundingBox) {
        let trunc = self.truncate_string.clone().unwrap_or("".to_string());
        let mut raw_lines = Vec::new();
        let padding = self.padding.unwrap_or_default();

        let content_width = if let Some(total_width) = self.width {
            total_width.saturating_sub(2 + padding.3 + padding.1)
        } else {
            self.text.lines().map(|line| line.len()).max().unwrap_or(0)
        };

        for line in self.text.lines() {
            if content_width > 0 {
                let mut processed_line = line.to_string();

                if processed_line.len() > content_width {
                    if !trunc.is_empty() && trunc.len() <= content_width {
                        processed_line.truncate(content_width - trunc.len());
                        processed_line.push_str(&trunc);
                    } else if !trunc.is_empty() && trunc.len() > content_width {
                        processed_line.clear();
                    } else {
                        processed_line.truncate(content_width);
                    }
                }

                raw_lines.push(processed_line);
            } else {
                raw_lines.push(String::new());
            }
        }

        // This doesn't seem necessary
        let effective_width = if self.width.is_some() {
            content_width
        } else {
            raw_lines.iter().map(|l| l.len()).max().unwrap_or(0)
        };

        let effective_height = if let Some(total_height) = self.height {
            total_height.saturating_sub(2 + padding.0 + padding.2)
        } else {
            raw_lines.len().max(0)
        };

        if raw_lines.len() > effective_height {
            raw_lines.truncate(effective_height);
        }

        let pad_line = |line: &str| -> Vec<Option<String>> {
            let padding_chars = effective_width.saturating_sub(line.len());
            let (left_pad, right_pad) = match self.justify {
                Justification::Left => (0, padding_chars),
                Justification::Right => (padding_chars, 0),
                Justification::Center => (padding_chars / 2, padding_chars - padding_chars / 2),
            };
            let mut row = vec![None; left_pad];
            row.extend(line.chars().map(|c| Some(c.to_string())));
            row.extend(std::iter::repeat_n(None, right_pad));
            row
        };

        let padded_lines: Vec<Vec<Option<String>>> =
            raw_lines.iter().map(|l| pad_line(l)).collect();

        let blank_row: Vec<Option<String>> = vec![None; effective_width];
        let vertical_padding = effective_height.saturating_sub(padded_lines.len());
        let (top_pad, bottom_pad) = match self.align {
            Alignment::Top => (0, vertical_padding),
            Alignment::Bottom => (vertical_padding, 0),
            Alignment::Center => (
                vertical_padding / 2,
                vertical_padding - vertical_padding / 2,
            ),
        };

        let mut result = Vec::new();
        result.extend(std::iter::repeat_n(blank_row.clone(), bottom_pad));
        result.extend(padded_lines.into_iter().rev().collect::<Vec<_>>());
        result.extend(std::iter::repeat_n(blank_row, top_pad));

        let text_start_x = self.position.0 + 1 + padding.3 as isize;
        let text_start_y = self.position.1 + 1 + padding.2 as isize;

        (
            result
                .iter()
                .enumerate()
                .flat_map(|(j, chars)| {
                    chars
                        .iter()
                        .enumerate()
                        .filter_map(|(i, c)| match c {
                            Some(chr) => Some(Pixel {
                                character: chr.chars().collect::<Vec<char>>()[0],
                                position: Point::new(
                                    text_start_x + i as isize,
                                    text_start_y + j as isize,
                                ),
                                style: self.style.clone(),
                                weight: self.weight,
                            }),
                            None => {
                                if self.transparent {
                                    None
                                } else {
                                    Some(Pixel {
                                        character: ' ',
                                        position: Point::new(
                                            text_start_x + i as isize,
                                            text_start_y + j as isize,
                                        ),
                                        style: self.style.clone(),
                                        weight: self.weight,
                                    })
                                }
                            }
                        })
                        .collect::<Vec<Pixel>>()
                })
                .map(|p| (p.position, p))
                .collect(),
            BoundingBox {
                top: text_start_y + effective_height as isize,
                right: text_start_x + effective_width as isize,
                bottom: text_start_y,
                left: text_start_x,
            },
        )
    }
}

#[pymodule]
fn textdraw(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<BoundingBox>()?;
    m.add_class::<PixelGroup>()?;
    m.add_class::<TextStyle>()?;
    m.add_class::<Pixel>()?;
    m.add_function(wrap_pyfunction!(render, m)?)?;
    m.add_function(wrap_pyfunction!(arrow, m)?)?;
    m.add_function(wrap_pyfunction!(text, m)?)?;
    m.add_function(wrap_pyfunction!(multipath, m)?)?;
    m.add_function(wrap_pyfunction!(duplicate_shifted, m)?)?;
    m.add_class::<TextPath>()?;
    m.add_class::<Box>()?;
    m.add_class::<Point>()?;
    Ok(())
}

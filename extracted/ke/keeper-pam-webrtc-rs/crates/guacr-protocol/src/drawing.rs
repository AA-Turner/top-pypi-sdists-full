// Drawing instruction formatting for Guacamole protocol
//
// Supports: img, rect, cfill, line, arc, curve, shade, copy, cursor

/// Generates a Guacamole drawing instruction function from a compact declaration.
///
/// Each invocation expands to a `pub fn` that converts every argument to its
/// string representation and calls `format_instruction` with the given opcode.
/// Doc comments and attributes (e.g. `#[allow(clippy::too_many_arguments)]`) on
/// the invocation are forwarded to the generated function unchanged.
macro_rules! drawing_instruction {
    (
        $(#[$attr:meta])*
        fn $fn_name:ident($opcode:literal $(, $arg:ident : $type:ty)*)
    ) => {
        $(#[$attr])*
        pub fn $fn_name($($arg: $type),*) -> String {
            crate::format_instruction($opcode, &[$(&$arg.to_string()),*])
        }
    };
}

drawing_instruction! {
    /// Format `img` instruction - Start image stream (modern protocol)
    ///
    /// Format: `3.img,{stream},{mask},{layer},{mimetype},{x},{y};`
    ///
    /// This starts a modern image stream. Must be followed by `blob` chunks and `end` instruction.
    /// Use `format_chunked_blobs` from the streams module to send the data.
    ///
    /// # Arguments
    /// - `stream`: Stream ID (must be unique per image)
    /// - `mask`: Channel mask (15 = RGBA, 3 = RGB)
    /// - `layer`: Layer index
    /// - `mimetype`: MIME type (e.g., "image/jpeg", "image/png")
    /// - `x`: X coordinate
    /// - `y`: Y coordinate
    fn format_img("img", stream: u32, mask: u32, layer: i32, mimetype: &str, x: i32, y: i32)
}

drawing_instruction! {
    /// Format `rect` instruction - Draw rectangle
    ///
    /// Format: `4.rect,{layer},{x},{y},{width},{height};`
    ///
    /// # Arguments
    /// - `layer`: Layer index (typically 0 for default layer)
    /// - `x`: X coordinate in pixels
    /// - `y`: Y coordinate in pixels
    /// - `width`: Width in pixels
    /// - `height`: Height in pixels
    fn format_rect("rect", layer: i32, x: u32, y: u32, width: u32, height: u32)
}

drawing_instruction! {
    /// Format `cfill` instruction - Fill current path with color
    ///
    /// Format: `5.cfill,{mask},{layer},{r},{g},{b},{a};`
    ///
    /// # Arguments
    /// - `mask`: Compositing operation (14 = GUAC_COMP_OVER, 12 = GUAC_COMP_SRC)
    /// - `layer`: Layer index
    /// - `r`: Red component (0-255)
    /// - `g`: Green component (0-255)
    /// - `b`: Blue component (0-255)
    /// - `a`: Alpha component (0-255, typically 255 for opaque)
    fn format_cfill("cfill", mask: u32, layer: i32, r: u8, g: u8, b: u8, a: u8)
}

drawing_instruction! {
    /// Format `line` instruction - Draw line
    ///
    /// Format: `4.line,{layer},{x1},{y1},{x2},{y2};`
    ///
    /// # Arguments
    /// - `layer`: Layer index
    /// - `x1`: Start X coordinate
    /// - `y1`: Start Y coordinate
    /// - `x2`: End X coordinate
    /// - `y2`: End Y coordinate
    fn format_line("line", layer: i32, x1: u32, y1: u32, x2: u32, y2: u32)
}

drawing_instruction! {
    /// Format `arc` instruction - Draw arc/ellipse
    ///
    /// Format: `3.arc,{layer},{x},{y},{radius_x},{radius_y},{start_angle},{end_angle};`
    ///
    /// # Arguments
    /// - `layer`: Layer index
    /// - `x`: Center X coordinate
    /// - `y`: Center Y coordinate
    /// - `radius_x`: Horizontal radius
    /// - `radius_y`: Vertical radius
    /// - `start_angle`: Start angle in radians
    /// - `end_angle`: End angle in radians
    fn format_arc("arc", layer: i32, x: u32, y: u32, radius_x: u32, radius_y: u32, start_angle: f64, end_angle: f64)
}

drawing_instruction! {
    /// Format `curve` instruction - Draw cubic Bezier curve
    ///
    /// Format: `5.curve,{layer},{x1},{y1},{x2},{y2},{x3},{y3};`
    ///
    /// # Arguments
    /// - `layer`: Layer index
    /// - `x1`, `y1`: First control point
    /// - `x2`, `y2`: Second control point
    /// - `x3`, `y3`: Third control point (end point)
    fn format_curve("curve", layer: i32, x1: u32, y1: u32, x2: u32, y2: u32, x3: u32, y3: u32)
}

drawing_instruction! {
    /// Format `shade` instruction - Draw shaded rectangle (gradient)
    ///
    /// Format: `5.shade,{layer},{x},{y},{width},{height},{r1},{g1},{b1},{a1},{r2},{g2},{b2},{a2};`
    ///
    /// # Arguments
    /// - `layer`: Layer index
    /// - `x`, `y`: Top-left corner
    /// - `width`, `height`: Rectangle dimensions
    /// - `r1`, `g1`, `b1`, `a1`: Start color (top)
    /// - `r2`, `g2`, `b2`, `a2`: End color (bottom)
    #[allow(clippy::too_many_arguments)]
    fn format_shade("shade", layer: i32, x: u32, y: u32, width: u32, height: u32, r1: u8, g1: u8, b1: u8, a1: u8, r2: u8, g2: u8, b2: u8, a2: u8)
}

drawing_instruction! {
    /// Format `copy` instruction - Copy pixels between layers
    ///
    /// Format: `4.copy,{srclayer},{srcx},{srcy},{srcw},{srch},{mask},{dstlayer},{dstx},{dsty};`
    ///
    /// The JS client handles this as a canvas drawImage operation, which is GPU-accelerated.
    /// This is extremely cheap (~50 bytes) compared to re-encoding and transmitting image data.
    ///
    /// # Arguments
    /// - `src_layer`: Source layer index (0 = default layer)
    /// - `src_x`: Source X coordinate
    /// - `src_y`: Source Y coordinate
    /// - `width`: Width of region to copy
    /// - `height`: Height of region to copy
    /// - `mask`: Compositing operation (12 = GUAC_COMP_SRC, 14 = GUAC_COMP_OVER)
    /// - `dst_layer`: Destination layer index (0 = default layer)
    /// - `dst_x`: Destination X coordinate
    /// - `dst_y`: Destination Y coordinate
    #[allow(clippy::too_many_arguments)]
    fn format_copy("copy", src_layer: i32, src_x: u32, src_y: u32, width: u32, height: u32, mask: u32, dst_layer: i32, dst_x: u32, dst_y: u32)
}

drawing_instruction! {
    /// Format `cursor` instruction - Set client cursor
    ///
    /// Format: `6.cursor,{x},{y},{srclayer},{srcx},{srcy},{srcwidth},{srcheight};`
    ///
    /// Sets the client's cursor to the image data from the specified rectangle of a layer,
    /// with the specified hotspot coordinates.
    ///
    /// # Arguments
    /// - `hotspot_x`: X coordinate of the cursor's hotspot (click point)
    /// - `hotspot_y`: Y coordinate of the cursor's hotspot (click point)
    /// - `src_layer`: Layer index to copy cursor image from
    /// - `src_x`: X coordinate of upper-left corner of source rectangle
    /// - `src_y`: Y coordinate of upper-left corner of source rectangle
    /// - `src_width`: Width of the cursor image
    /// - `src_height`: Height of the cursor image
    ///
    /// # Example
    /// ```
    /// use guacr_protocol::format_cursor;
    /// // Set cursor to 32x32 image from layer 1 at (0,0), with hotspot at (16,16)
    /// let instr = format_cursor(16, 16, 1, 0, 0, 32, 32);
    /// assert_eq!(instr, "6.cursor,2.16,2.16,1.1,1.0,1.0,2.32,2.32;");
    /// ```
    fn format_cursor("cursor", hotspot_x: i32, hotspot_y: i32, src_layer: i32, src_x: i32, src_y: i32, src_width: u32, src_height: u32)
}

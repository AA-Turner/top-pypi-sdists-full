// VNC protocol implementation
// Implements RFB protocol 3.8 (most common version)

use log::{info, warn};
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};

/// Maximum desktop name length accepted in ServerInit.
/// The RFB spec allows up to u32::MAX but allocating that would exhaust memory.
/// 64 KiB is more than enough for any real VNC server name.
pub const MAX_VNC_NAME_LEN: usize = 64 * 1024;

/// VNC protocol version
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum VncVersion {
    V38, // RFB 003.008 (most common)
    V37, // RFB 003.007
    V33, // RFB 003.003
}

impl VncVersion {
    pub fn as_bytes(&self) -> &[u8] {
        match self {
            VncVersion::V38 => b"RFB 003.008\n",
            VncVersion::V37 => b"RFB 003.007\n",
            VncVersion::V33 => b"RFB 003.003\n",
        }
    }

    pub fn from_bytes(bytes: &[u8]) -> Option<Self> {
        match bytes {
            b"RFB 003.008\n" => Some(VncVersion::V38),
            b"RFB 003.007\n" => Some(VncVersion::V37),
            b"RFB 003.003\n" => Some(VncVersion::V33),
            _ => None,
        }
    }
}

/// VNC security type
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum VncSecurityType {
    None = 1,
    VncAuth = 2,
    Tight = 16,
    VeNCrypt = 19,
    RealVnc = 113,
}

impl VncSecurityType {
    pub fn from_u8(value: u8) -> Option<Self> {
        match value {
            1 => Some(VncSecurityType::None),
            2 => Some(VncSecurityType::VncAuth),
            16 => Some(VncSecurityType::Tight),
            19 => Some(VncSecurityType::VeNCrypt),
            113 => Some(VncSecurityType::RealVnc),
            _ => None,
        }
    }
}

/// VNC pixel format
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct VncPixelFormat {
    pub bits_per_pixel: u8,
    pub depth: u8,
    pub big_endian: bool,
    pub true_color: bool,
    pub red_max: u16,
    pub green_max: u16,
    pub blue_max: u16,
    pub red_shift: u8,
    pub green_shift: u8,
    pub blue_shift: u8,
}

impl Default for VncPixelFormat {
    fn default() -> Self {
        // Standard 24-bit RGB format
        Self {
            bits_per_pixel: 32,
            depth: 24,
            big_endian: false,
            true_color: true,
            red_max: 255,
            green_max: 255,
            blue_max: 255,
            red_shift: 16,
            green_shift: 8,
            blue_shift: 0,
        }
    }
}

/// VNC encoding types
#[allow(dead_code)]
pub mod encodings {
    /// Raw encoding
    pub const RAW: i32 = 0;
    /// CopyRect encoding
    pub const COPYRECT: i32 = 1;
    /// RRE encoding
    pub const RRE: i32 = 2;
    /// Hextile encoding
    pub const HEXTILE: i32 = 5;
    /// Tight encoding
    pub const TIGHT: i32 = 7;
    /// ZRLE encoding
    pub const ZRLE: i32 = 16;
    /// Cursor pseudo-encoding (cursor shape update)
    pub const CURSOR: i32 = -239;
    /// DesktopSize pseudo-encoding
    pub const DESKTOP_SIZE: i32 = -223;
    /// X Cursor pseudo-encoding (X11 cursor format)
    pub const X_CURSOR: i32 = -240;
    /// Rich Cursor pseudo-encoding (RGBA cursor with alpha)
    pub const RICH_CURSOR: i32 = -239;
}

/// Pixel payload for a VNC rectangle update.
#[derive(Debug, Clone)]
pub enum VncPixelData {
    Raw(Vec<u8>),            // 3-bytes/pixel RGB (Raw, Hextile, RRE decoded output)
    ZrleCompressed(Vec<u8>), // Raw zlib bytes — caller decompresses with per-session ZrleState
    Fill(u8, u8, u8),        // Tight FillRect — solid color
    TightJpeg(Vec<u8>),      // Tight JPEG — forward directly
    Empty,                   // Pseudo-encoding or unimplemented
}

/// VNC protocol handler
pub struct VncProtocol;

/// Select the best available VNC security type offered by the server.
///
/// Prefers VncAuth over None. If the server only offers None and the client
/// has a password configured, the connection is rejected — accepting None auth
/// silently discards the password and allows unauthenticated access.
pub(crate) fn select_security_type(
    offered: &[u8],
    has_password: bool,
) -> Result<VncSecurityType, String> {
    if offered.contains(&(VncSecurityType::VncAuth as u8)) {
        return Ok(VncSecurityType::VncAuth);
    }
    if offered.contains(&(VncSecurityType::None as u8)) {
        if has_password {
            return Err(
                "Server only offers None authentication, but a password is configured. \
                 Refusing to connect without VNC password authentication — \
                 the remote VNC server may be misconfigured."
                    .to_string(),
            );
        }
        return Ok(VncSecurityType::None);
    }
    // Unknown type — use the first offered
    VncSecurityType::from_u8(offered[0])
        .ok_or_else(|| format!("Unsupported VNC security type: {}", offered[0]))
}

impl VncProtocol {
    /// Decode a Tight "compact length" field (1–3 bytes, 7-bit groups).
    pub(crate) fn parse_tight_length(data: &[u8]) -> Option<(usize, usize)> {
        if data.is_empty() {
            return None;
        }
        let b0 = data[0] as usize;
        if b0 < 0x80 {
            return Some((b0, 1));
        }
        if data.len() < 2 {
            return None;
        }
        let b1 = data[1] as usize;
        let len = (b0 & 0x7F) | ((b1 & 0x7F) << 7);
        if b1 < 0x80 {
            return Some((len, 2));
        }
        if data.len() < 3 {
            return None;
        }
        let b2 = data[2] as usize;
        Some(((b0 & 0x7F) | ((b1 & 0x7F) << 7) | (b2 << 14), 3))
    }

    /// Perform VNC handshake
    ///
    /// Returns (version, security_type, pixel_format, width, height, name)
    pub async fn handshake<S>(
        stream: &mut S,
        password: Option<&str>,
    ) -> Result<(VncVersion, VncPixelFormat, u16, u16, String), String>
    where
        S: AsyncRead + AsyncWrite + Unpin,
    {
        // 1. Read server version
        let mut version_buf = [0u8; 12];
        stream
            .read_exact(&mut version_buf)
            .await
            .map_err(|e| format!("Failed to read version: {}", e))?;

        let version = VncVersion::from_bytes(&version_buf).ok_or_else(|| {
            format!(
                "Unsupported VNC version: {:?}",
                String::from_utf8_lossy(&version_buf)
            )
        })?;

        info!("VNC: Server version: {:?}", version);

        // 2. Send client version — always negotiate 3.8 to use proper security handshake.
        // Echoing the server's version (e.g. 3.3) causes TigerVNC to send security
        // type=0 (failure); sending 3.8 lets it use VNC auth correctly.
        let negotiated = if version == VncVersion::V33 {
            VncVersion::V38
        } else {
            version
        };
        stream
            .write_all(negotiated.as_bytes())
            .await
            .map_err(|e| format!("Failed to send version: {}", e))?;
        let version = negotiated;

        // 3. Read security types — format differs by version.
        // RFB 3.3: server sends 4-byte big-endian security type directly (no count, no client selection).
        // RFB 3.7/3.8: server sends 1-byte count then that many 1-byte type values.
        let selected_type = if version == VncVersion::V33 {
            let mut sec_type_buf = [0u8; 4];
            stream
                .read_exact(&mut sec_type_buf)
                .await
                .map_err(|e| format!("Failed to read V33 security type: {}", e))?;
            let type_u32 = u32::from_be_bytes(sec_type_buf);
            info!("VNC: V33 security type: {}", type_u32);
            // In RFB 3.3 the server dictates the type; client does not send a selection.
            VncSecurityType::from_u8(type_u32 as u8).unwrap_or(VncSecurityType::None)
        } else {
            let mut num_security_types = [0u8; 1];
            stream
                .read_exact(&mut num_security_types)
                .await
                .map_err(|e| format!("Failed to read security types count: {}", e))?;

            let num_types = num_security_types[0] as usize;
            if num_types == 0 {
                return Err("Server sent no security types".to_string());
            }

            let mut security_types = vec![0u8; num_types];
            stream
                .read_exact(&mut security_types)
                .await
                .map_err(|e| format!("Failed to read security types: {}", e))?;

            // 4. Select security type — reject None when a password is configured.
            let has_password = password.is_some();
            let t = select_security_type(&security_types, has_password)?;

            // Send selected security type (3.7/3.8 only — 3.3 server dictates it)
            stream
                .write_all(&[t as u8])
                .await
                .map_err(|e| format!("Failed to send security type: {}", e))?;

            t
        };

        info!("VNC: Selected security type: {:?}", selected_type);

        // 5. Handle authentication
        match selected_type {
            VncSecurityType::VncAuth => {
                Self::authenticate_vnc(stream, password).await?;
            }
            VncSecurityType::None => {
                // No authentication needed
            }
            _ => {
                return Err(format!("Unsupported security type: {:?}", selected_type));
            }
        }

        // 6. Send ClientInit with shared=1 so the server keeps other sessions alive.
        // RFB spec: shared=0 (exclusive) may cause the server to disconnect all other
        // viewers before sending ServerInit, which on some implementations stalls the
        // handshake.  shared=1 is the correct default.
        stream
            .write_all(&[1u8])
            .await
            .map_err(|e| format!("Failed to send ClientInit: {}", e))?;

        // 7. Read ServerInit fixed header (24 bytes) with timeout.
        //
        // RFB ServerInit layout:
        //   [0..2]   width  (u16 big-endian)
        //   [2..4]   height (u16 big-endian)
        //   [4..20]  PixelFormat (16 bytes)
        //   [20..24] NameLength (u32 big-endian)
        //
        // All 24 bytes are read in a single call; NameLength is extracted from
        // server_init[20..24].  A second read_exact for name_len_buf would consume
        // bytes from the name string itself and must NOT be done.
        let mut server_init = [0u8; 24];
        tokio::time::timeout(
            std::time::Duration::from_secs(15),
            stream.read_exact(&mut server_init),
        )
        .await
        .map_err(|_| "VNC ServerInit timed out (server did not respond within 15s)".to_string())?
        .map_err(|e| format!("Failed to read ServerInit: {}", e))?;

        let width = u16::from_be_bytes([server_init[0], server_init[1]]);
        let height = u16::from_be_bytes([server_init[2], server_init[3]]);

        // Parse pixel format (16 bytes starting at offset 4)
        let pixel_format = Self::parse_pixel_format(&server_init[4..20])?;

        // NameLength is already in the 24-byte buffer at bytes 20..24.
        let name_len = u32::from_be_bytes([
            server_init[20],
            server_init[21],
            server_init[22],
            server_init[23],
        ]) as usize;
        if name_len > MAX_VNC_NAME_LEN {
            return Err(format!(
                "VNC ServerInit name length {} exceeds maximum {} bytes",
                name_len, MAX_VNC_NAME_LEN
            ));
        }
        let mut name_buf = vec![0u8; name_len];
        stream
            .read_exact(&mut name_buf)
            .await
            .map_err(|e| format!("Failed to read name: {}", e))?;

        let name = String::from_utf8_lossy(&name_buf).to_string();

        info!("VNC: ServerInit - {}x{}, name: {}", width, height, name);

        Ok((version, pixel_format, width, height, name))
    }

    /// Authenticate using VNC Auth
    async fn authenticate_vnc<S>(stream: &mut S, password: Option<&str>) -> Result<(), String>
    where
        S: AsyncRead + AsyncWrite + Unpin,
    {
        // Read challenge (16 bytes)
        let mut challenge = [0u8; 16];
        stream
            .read_exact(&mut challenge)
            .await
            .map_err(|e| format!("Failed to read challenge: {}", e))?;

        // Encrypt challenge with password
        let password = password.ok_or_else(|| "VNC Auth requires password".to_string())?;
        let response = Self::encrypt_vnc_password(&challenge, password);

        // Send response
        stream
            .write_all(&response)
            .await
            .map_err(|e| format!("Failed to send response: {}", e))?;

        // Read authentication result
        let mut result = [0u8; 4];
        stream
            .read_exact(&mut result)
            .await
            .map_err(|e| format!("Failed to read auth result: {}", e))?;

        let auth_result = u32::from_be_bytes(result);
        if auth_result != 0 {
            return Err("VNC authentication failed".to_string());
        }

        info!("VNC: Authentication successful");
        Ok(())
    }

    /// Encrypt VNC password using DES with bit-reversed key bytes (RFB quirk).
    pub(crate) fn encrypt_vnc_password(challenge: &[u8; 16], password: &str) -> [u8; 16] {
        use des::cipher::{BlockEncrypt, KeyInit};
        use des::Des;

        let mut key = [0u8; 8];
        let pw = password.as_bytes();
        let len = pw.len().min(8);
        key[..len].copy_from_slice(&pw[..len]);

        // VNC quirk: reverse bit order in each key byte
        for b in key.iter_mut() {
            *b = b.reverse_bits();
        }

        let cipher = Des::new_from_slice(&key).expect("DES key is always 8 bytes");
        let mut response = [0u8; 16];
        let mut block = des::cipher::generic_array::GenericArray::from([0u8; 8]);
        block.copy_from_slice(&challenge[..8]);
        cipher.encrypt_block(&mut block);
        response[..8].copy_from_slice(&block);
        block.copy_from_slice(&challenge[8..]);
        cipher.encrypt_block(&mut block);
        response[8..].copy_from_slice(&block);
        response
    }

    /// Parse pixel format from bytes
    fn parse_pixel_format(data: &[u8]) -> Result<VncPixelFormat, String> {
        if data.len() < 16 {
            return Err("Pixel format data too short".to_string());
        }

        Ok(VncPixelFormat {
            bits_per_pixel: data[0],
            depth: data[1],
            big_endian: data[2] != 0,
            true_color: data[3] != 0,
            red_max: u16::from_be_bytes([data[4], data[5]]),
            green_max: u16::from_be_bytes([data[6], data[7]]),
            blue_max: u16::from_be_bytes([data[8], data[9]]),
            red_shift: data[10],
            green_shift: data[11],
            blue_shift: data[12],
        })
    }

    /// Read FramebufferUpdate message from buffer (for buffered reading)
    pub fn parse_framebuffer_update_from_buffer(
        data: &[u8],
    ) -> Result<(Vec<VncRectangle>, usize), String> {
        if data.len() < 4 {
            return Err("FramebufferUpdate message too short".to_string());
        }

        // Check message type
        if data[0] != 0 {
            return Err(format!("Expected FramebufferUpdate (0), got {}", data[0]));
        }

        // Read padding
        let _padding = data[1];

        // Read number of rectangles
        let num_rects = u16::from_be_bytes([data[2], data[3]]) as usize;

        let mut offset = 4;
        let mut rectangles = Vec::new();

        for _ in 0..num_rects {
            if offset + 12 > data.len() {
                break; // Not enough data
            }

            let x = u16::from_be_bytes([data[offset], data[offset + 1]]);
            let y = u16::from_be_bytes([data[offset + 2], data[offset + 3]]);
            let width = u16::from_be_bytes([data[offset + 4], data[offset + 5]]);
            let height = u16::from_be_bytes([data[offset + 6], data[offset + 7]]);
            let encoding = i32::from_be_bytes([
                data[offset + 8],
                data[offset + 9],
                data[offset + 10],
                data[offset + 11],
            ]);

            offset += 12;

            let (pixel_data, pixels, src_x, src_y) = match encoding {
                1 => {
                    // CopyRect encoding: parse 4 bytes for source coordinates
                    if offset + 4 > data.len() {
                        break;
                    }
                    let sx = u16::from_be_bytes([data[offset], data[offset + 1]]);
                    let sy = u16::from_be_bytes([data[offset + 2], data[offset + 3]]);
                    offset += 4;
                    (VncPixelData::Empty, vec![], sx, sy)
                }
                7 => {
                    // Tight encoding
                    if offset >= data.len() {
                        break;
                    }
                    let compression_control = data[offset];
                    offset += 1;
                    let subtype = compression_control & 0xF0;
                    match subtype {
                        0x80 => {
                            // Fill subtype (0x08 << 4 = 0x80)
                            if offset + 3 > data.len() {
                                break;
                            }
                            let r = data[offset];
                            let g = data[offset + 1];
                            let b = data[offset + 2];
                            offset += 3;
                            (VncPixelData::Fill(r, g, b), vec![], 0, 0)
                        }
                        0x90 => {
                            // JPEG subtype (0x09 << 4 = 0x90)
                            if let Some((jpeg_len, consumed)) =
                                Self::parse_tight_length(&data[offset..])
                            {
                                offset += consumed;
                                if offset + jpeg_len > data.len() {
                                    break;
                                }
                                let jpeg_bytes = data[offset..offset + jpeg_len].to_vec();
                                offset += jpeg_len;
                                (VncPixelData::TightJpeg(jpeg_bytes), vec![], 0, 0)
                            } else {
                                break;
                            }
                        }
                        _ => (VncPixelData::Empty, vec![], 0, 0),
                    }
                }
                0 => {
                    // Raw encoding
                    let bytes_per_pixel: usize = 3; // RGB
                                                    // AC-1/AC-5: use checked arithmetic to prevent overflow on
                                                    // adversarial width/height values (e.g. 65535 × 65535).
                    let pixel_count = match (width as usize).checked_mul(height as usize) {
                        Some(n) => n,
                        None => break, // overflow → skip remaining rectangles
                    };
                    let pixel_size = match pixel_count.checked_mul(bytes_per_pixel) {
                        Some(n) => n,
                        None => break,
                    };

                    if offset + pixel_size > data.len() {
                        break;
                    }

                    let raw_bytes = data[offset..offset + pixel_size].to_vec();
                    offset += pixel_size;
                    (VncPixelData::Raw(raw_bytes.clone()), raw_bytes, 0, 0)
                }
                // ZRLE encoding (T-013 to T-015):
                // Extract the compressed payload; the per-session ZrleState lives in
                // VncClient, so decompression happens in handle_framebuffer_rectangle.
                16 => {
                    // First 4 bytes: big-endian compressed length.
                    if offset + 4 > data.len() {
                        break;
                    }
                    let compressed_len = u32::from_be_bytes([
                        data[offset],
                        data[offset + 1],
                        data[offset + 2],
                        data[offset + 3],
                    ]) as usize;
                    offset += 4;
                    if offset + compressed_len > data.len() {
                        break;
                    }
                    let compressed = data[offset..offset + compressed_len].to_vec();
                    offset += compressed_len;
                    (VncPixelData::ZrleCompressed(compressed), vec![], 0, 0)
                }

                // Hextile encoding (T-016, T-017):
                // Fully decode here — Hextile state (bg/fg colors) is per-rectangle only.
                5 => {
                    // Hextile payload length is variable — we must decode in-place.
                    // Pass a slice starting at offset; decoder tracks its own position.
                    // We don't know the length upfront, so we pass all remaining data
                    // and use a dedicated parser that reports how many bytes it consumed.
                    let remaining = &data[offset..];
                    match crate::encodings::decode_hextile_from_stream(remaining, width, height) {
                        Ok((pixels, consumed)) => {
                            offset += consumed;
                            (VncPixelData::Raw(pixels), vec![], 0, 0)
                        }
                        Err(e) => {
                            warn!("VNC: Hextile decode error: {}", e);
                            break;
                        }
                    }
                }

                // RRE encoding (T-018, T-019):
                // Payload: 4-byte count + 3-byte bg + N × 11-byte subrects.
                2 => {
                    if offset + 7 > data.len() {
                        break;
                    }
                    let num_subrects = u32::from_be_bytes([
                        data[offset],
                        data[offset + 1],
                        data[offset + 2],
                        data[offset + 3],
                    ]) as usize;
                    // Use saturating arithmetic to prevent u32→usize overflow on hostile num_subrects
                    let rre_len = 7usize.saturating_add(num_subrects.saturating_mul(11));
                    if offset + rre_len > data.len() {
                        break;
                    }
                    let rre_data = &data[offset..offset + rre_len];
                    match crate::encodings::decode_rre(rre_data, width, height) {
                        Ok(pixels) => {
                            offset += rre_len;
                            (VncPixelData::Raw(pixels), vec![], 0, 0)
                        }
                        Err(e) => {
                            warn!("VNC: RRE decode error: {}", e);
                            break;
                        }
                    }
                }

                // T-020, T-022: unrecognized encoding — terminate to prevent desync.
                enc if enc != 0
                    && enc != 1
                    && enc != 5
                    && enc != 7
                    && enc != 16
                    && enc != encodings::CURSOR
                    && enc != encodings::X_CURSOR
                    && enc != encodings::DESKTOP_SIZE =>
                {
                    // T-022: log warning identifying the encoding type.
                    // T-020: terminate the connection (return early from the parser
                    // with the rectangles collected so far, caller will handle error).
                    warn!(
                        "VNC: unrecognized encoding type {} — stream cannot be recovered, \
                         triggering disconnect",
                        enc
                    );
                    // Return an error so handle_framebuffer_rectangle terminates the session.
                    return Err(crate::encodings::unrecognized_encoding(enc));
                }

                _ => {
                    // Unknown or pseudo-encoding with no parseable payload.
                    // We cannot know how many bytes to skip, so stop parsing to
                    // prevent stream desync — return what we have so far.
                    warn!("VNC: unknown encoding {} in buffer parser — stopping rectangle parse to prevent desync", encoding);
                    break;
                }
            };

            rectangles.push(VncRectangle {
                x,
                y,
                width,
                height,
                encoding,
                pixels,
                pixel_data,
                src_x,
                src_y,
            });
        }

        Ok((rectangles, offset))
    }

    /// Parse cursor pseudo-encoding data
    ///
    /// VNC cursor format (Rich Cursor encoding -239):
    /// - width x height pixels in server pixel format (RGBA or RGB)
    /// - width x height bitmask (1 bit per pixel, packed into bytes)
    ///
    /// The x,y from the rectangle header are the hotspot coordinates.
    pub fn parse_cursor_data(
        x: u16,
        y: u16,
        width: u16,
        height: u16,
        data: &[u8],
        pixel_format: &VncPixelFormat,
    ) -> Result<VncCursor, String> {
        // 0×0 cursor = "hide cursor" — valid in RFB; return empty cursor.
        if width == 0 || height == 0 {
            return Ok(VncCursor {
                width: 0,
                height: 0,
                hotspot_x: 0,
                hotspot_y: 0,
                rgba_data: vec![],
            });
        }

        // Validate bits_per_pixel before division to avoid integer truncation
        // producing bytes_per_pixel=0 (which would skip the data-size check).
        if !matches!(pixel_format.bits_per_pixel, 8 | 16 | 24 | 32) {
            return Err(format!(
                "VNC cursor: unsupported bits_per_pixel {} (must be 8, 16, 24, or 32)",
                pixel_format.bits_per_pixel
            ));
        }
        // AC-1/AC-5: use checked arithmetic — adversarial cursor PDUs could overflow.
        let pixel_count = (width as usize)
            .checked_mul(height as usize)
            .ok_or_else(|| format!("VNC cursor: dimension overflow ({width}x{height})"))?;
        let bytes_per_pixel = (pixel_format.bits_per_pixel / 8) as usize;
        let pixel_data_size = pixel_count
            .checked_mul(bytes_per_pixel)
            .ok_or_else(|| "VNC cursor: pixel data size overflow".to_string())?;

        // Bitmask size: each row is padded to a full byte boundary (RFB spec).
        // stride is the number of bytes per row in the bitmask.
        let mask_stride = (width as usize).div_ceil(8);
        let bitmask_size = mask_stride * height as usize;

        let expected_size = pixel_data_size + bitmask_size;
        if data.len() < expected_size {
            return Err(format!(
                "Cursor data too short: expected {}, got {}",
                expected_size,
                data.len()
            ));
        }

        // Extract pixel data and bitmask
        let pixel_data = &data[..pixel_data_size];
        let bitmask = &data[pixel_data_size..pixel_data_size + bitmask_size];

        // Convert to RGBA format
        let mut rgba_data = Vec::with_capacity(pixel_count * 4);

        for row in 0..(height as usize) {
            for col in 0..(width as usize) {
                let i = row * width as usize + col;
                let pixel_offset = i * bytes_per_pixel;

                // Check bitmask using RFB row-stride layout:
                // stride = (width + 7) / 8 bytes per row; bit 7 is the leftmost pixel.
                let mask_byte = row * mask_stride + col / 8;
                let is_visible = if mask_byte < bitmask.len() {
                    (bitmask[mask_byte] >> (7 - col % 8)) & 1 != 0
                } else {
                    false
                };

                // Extract RGB from pixel data based on pixel format
                let (r, g, b) = if pixel_format.true_color {
                    // True color - extract RGB from pixel data
                    let pixel_bytes = &pixel_data[pixel_offset..pixel_offset + bytes_per_pixel];

                    // Read pixel value (big-endian or little-endian based on format)
                    let pixel_value = if pixel_format.big_endian {
                        match bytes_per_pixel {
                            4 => u32::from_be_bytes([
                                pixel_bytes[0],
                                pixel_bytes[1],
                                pixel_bytes[2],
                                pixel_bytes[3],
                            ]),
                            2 => u16::from_be_bytes([pixel_bytes[0], pixel_bytes[1]]) as u32,
                            _ => pixel_bytes[0] as u32,
                        }
                    } else {
                        match bytes_per_pixel {
                            4 => u32::from_le_bytes([
                                pixel_bytes[0],
                                pixel_bytes[1],
                                pixel_bytes[2],
                                pixel_bytes[3],
                            ]),
                            2 => u16::from_le_bytes([pixel_bytes[0], pixel_bytes[1]]) as u32,
                            _ => pixel_bytes[0] as u32,
                        }
                    };

                    // Extract RGB components using shifts and masks
                    let r = ((pixel_value >> pixel_format.red_shift) & pixel_format.red_max as u32)
                        as u8;
                    let g = ((pixel_value >> pixel_format.green_shift)
                        & pixel_format.green_max as u32) as u8;
                    let b = ((pixel_value >> pixel_format.blue_shift)
                        & pixel_format.blue_max as u32) as u8;

                    // Scale to 8-bit (0-255)
                    let r = (r as u32 * 255 / pixel_format.red_max as u32) as u8;
                    let g = (g as u32 * 255 / pixel_format.green_max as u32) as u8;
                    let b = (b as u32 * 255 / pixel_format.blue_max as u32) as u8;

                    (r, g, b)
                } else {
                    // Color map mode - not commonly used for cursors
                    warn!("VNC: Color map mode not supported for cursors, using black");
                    (0, 0, 0)
                };

                // Add RGBA pixel
                rgba_data.push(r);
                rgba_data.push(g);
                rgba_data.push(b);
                rgba_data.push(if is_visible { 255 } else { 0 }); // Alpha channel
            } // for col
        } // for row

        Ok(VncCursor {
            width,
            height,
            hotspot_x: x,
            hotspot_y: y,
            rgba_data,
        })
    }

    /// Send SetEncodings message.
    ///
    /// Encoding preference order:
    ///   1. CopyRect  — server avoids sending pixels when regions are copied
    ///   2. Tight     — server-compressed JPEG (low bandwidth)
    ///   3. Raw       — fallback
    ///
    /// Cursor pseudo-encodings are appended when `enable_cursor` is true.
    pub async fn send_set_encodings<S>(stream: &mut S, enable_cursor: bool) -> Result<(), String>
    where
        S: AsyncWrite + Unpin,
    {
        // Only advertise encodings the streaming reader handles.
        // RRE (2) and Hextile (5) are omitted — the streaming reader does not yet
        // implement their variable-length bodies. The server falls back to ZRLE or Raw.
        let mut enc_list = vec![
            encodings::ZRLE,     // zlib RFC 1950 compressed tile RLE (preferred)
            encodings::COPYRECT, // server avoids sending pixels for region copies
            encodings::RAW,      // fallback
        ];

        // Add cursor pseudo-encoding if requested (for client-side cursor)
        if enable_cursor {
            enc_list.push(encodings::CURSOR); // Rich cursor with alpha
            enc_list.push(encodings::X_CURSOR); // X11 cursor format (fallback)
        }

        let mut message = vec![
            2u8, // Message type: SetEncodings
            0u8, // Padding
        ];

        // Number of encodings (2 bytes, big-endian)
        message.extend_from_slice(&(enc_list.len() as u16).to_be_bytes());

        // Encoding types (4 bytes each, big-endian)
        for encoding in enc_list {
            message.extend_from_slice(&encoding.to_be_bytes());
        }

        stream
            .write_all(&message)
            .await
            .map_err(|e| format!("Failed to send SetEncodings: {}", e))?;

        info!("VNC: Sent SetEncodings (cursor support: {})", enable_cursor);
        Ok(())
    }

    /// Send FramebufferUpdateRequest
    pub async fn send_framebuffer_update_request<S>(
        stream: &mut S,
        incremental: bool,
        x: u16,
        y: u16,
        width: u16,
        height: u16,
    ) -> Result<(), String>
    where
        S: AsyncWrite + Unpin,
    {
        let mut request = vec![
            3u8, // Message type: FramebufferUpdateRequest
            incremental as u8,
        ];

        request.extend_from_slice(&x.to_be_bytes());
        request.extend_from_slice(&y.to_be_bytes());
        request.extend_from_slice(&width.to_be_bytes());
        request.extend_from_slice(&height.to_be_bytes());

        stream
            .write_all(&request)
            .await
            .map_err(|e| format!("Failed to send FramebufferUpdateRequest: {}", e))?;

        Ok(())
    }

    /// Send PointerEvent (mouse)
    pub async fn send_pointer_event<S>(
        stream: &mut S,
        x: u16,
        y: u16,
        button_mask: u8,
    ) -> Result<(), String>
    where
        S: AsyncWrite + Unpin,
    {
        let mut event = vec![
            5u8, // Message type: PointerEvent
            button_mask,
        ];

        event.extend_from_slice(&x.to_be_bytes());
        event.extend_from_slice(&y.to_be_bytes());

        stream
            .write_all(&event)
            .await
            .map_err(|e| format!("Failed to send PointerEvent: {}", e))?;

        Ok(())
    }

    /// Send KeyEvent (keyboard)
    pub async fn send_key_event<S>(stream: &mut S, key: u32, down: bool) -> Result<(), String>
    where
        S: AsyncWrite + Unpin,
    {
        let mut event = vec![
            4u8, // Message type: KeyEvent
            down as u8, 0u8, // padding
            0u8, // padding
        ];

        event.extend_from_slice(&key.to_be_bytes());

        stream
            .write_all(&event)
            .await
            .map_err(|e| format!("Failed to send KeyEvent: {}", e))?;

        Ok(())
    }
}

/// VNC rectangle (framebuffer update)
#[derive(Debug, Clone)]
pub struct VncRectangle {
    pub x: u16,
    pub y: u16,
    pub width: u16,
    pub height: u16,
    pub encoding: i32,
    pub pixels: Vec<u8>,
    pub pixel_data: VncPixelData,
    pub src_x: u16,
    pub src_y: u16,
}

/// VNC cursor data (from cursor pseudo-encoding)
#[derive(Debug, Clone)]
#[allow(dead_code)] // TODO: Used when parsing cursor updates from VNC server
pub struct VncCursor {
    /// Cursor width in pixels
    pub width: u16,
    /// Cursor height in pixels
    pub height: u16,
    /// X coordinate of hotspot (click point)
    pub hotspot_x: u16,
    /// Y coordinate of hotspot (click point)
    pub hotspot_y: u16,
    /// RGBA pixel data (4 bytes per pixel)
    pub rgba_data: Vec<u8>,
}

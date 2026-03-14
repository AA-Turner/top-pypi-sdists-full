// Minimal fragmented MP4 (ISO BMFF) muxer for H.264 + input event data track.
//
// Produces a streaming fMP4 suitable for upload to the recording router.
// Initialization segment (ftyp + moov) is written once on the first IDR frame.
// Each video frame becomes a moof+mdat pair.
// Input events (key/mouse) are written to a second text track for keystroke logging.
//
// H.264 input is Annex B (start-code prefixed); fMP4 requires AVCC (length-prefixed).

/// A single H.264 frame in AVCC format plus metadata.
pub struct Mp4Frame {
    pub avcc: Vec<u8>,
    pub pts: u32, // 90kHz clock units (wraps at ~13 hours, fine for PAM)
    pub is_keyframe: bool,
}

/// Fragmented MP4 muxer state.
pub struct Fmp4Writer {
    width: u32,
    height: u32,
    sequence_number: u32,
    prev_pts: Option<u32>,
    initialized: bool,
}

impl Fmp4Writer {
    pub fn new(width: u32, height: u32) -> Self {
        Self {
            width,
            height,
            sequence_number: 0,
            prev_pts: None,
            initialized: false,
        }
    }

    pub fn is_initialized(&self) -> bool {
        self.initialized
    }

    /// Build the initialization segment from the SPS and PPS of the first IDR frame.
    /// Returns ftyp + moov bytes, or None if SPS/PPS cannot be extracted.
    pub fn init_segment(&mut self, annex_b: &[u8]) -> Option<Vec<u8>> {
        let (sps, pps) = extract_parameter_sets(annex_b)?;
        self.initialized = true;
        let mut out = Vec::with_capacity(1200);
        out.extend(ftyp());
        out.extend(moov(self.width, self.height, &sps, &pps));
        Some(out)
    }

    /// Convert an Annex B frame to AVCC and return the prepared Mp4Frame.
    /// Returns None if AVCC conversion yields no data.
    pub fn prepare_frame(
        &mut self,
        annex_b: &[u8],
        pts_90khz: u64,
        is_keyframe: bool,
    ) -> Option<Mp4Frame> {
        let avcc = annex_b_to_avcc(annex_b);
        if avcc.is_empty() {
            return None;
        }
        let pts = pts_90khz as u32; // truncate; fine for sessions < 13 hours
        Some(Mp4Frame {
            avcc,
            pts,
            is_keyframe,
        })
    }

    /// Write a video fragment (moof + mdat). Returns the bytes to write.
    pub fn write_video_fragment(&mut self, frame: &Mp4Frame) -> Vec<u8> {
        self.sequence_number += 1;
        let duration = match self.prev_pts {
            Some(prev) => frame.pts.wrapping_sub(prev),
            None => 3000, // ~33ms at 90kHz ≈ 30fps
        };
        let duration = if duration == 0 { 3000 } else { duration };
        self.prev_pts = Some(frame.pts);

        let moof = moof_video(
            self.sequence_number,
            frame.pts,
            duration,
            frame.avcc.len() as u32,
            frame.is_keyframe,
        );
        let mdat_size = (8u32 + frame.avcc.len() as u32).to_be_bytes();

        let mut out = Vec::with_capacity(moof.len() + 8 + frame.avcc.len());
        out.extend(&moof);
        out.extend(&mdat_size);
        out.extend(b"mdat");
        out.extend(&frame.avcc);
        out
    }

    /// Write a data fragment for a batch of input events.
    /// Events are: (timestamp_ms, guacamole_instruction_string).
    /// Returns the bytes to write, or empty if events is empty.
    pub fn write_data_fragment(&mut self, events: &[(u64, String)]) -> Vec<u8> {
        if events.is_empty() {
            return Vec::new();
        }
        self.sequence_number += 1;

        // Serialize events as: "<ts_ms>\n<instruction>\n" per event
        let payload: Vec<u8> = events
            .iter()
            .flat_map(|(ts, instr)| format!("{}\n{}\n", ts, instr).into_bytes())
            .collect();

        let first_ts_ms = events[0].0;
        let last_ts_ms = events.last().unwrap().0;
        let duration = (last_ts_ms.saturating_sub(first_ts_ms) + 1) as u32;

        let moof = moof_data(
            self.sequence_number,
            first_ts_ms as u32,
            payload.len() as u32,
            duration,
        );
        let mdat_size = (8u32 + payload.len() as u32).to_be_bytes();

        let mut out = Vec::with_capacity(moof.len() + 8 + payload.len());
        out.extend(&moof);
        out.extend(&mdat_size);
        out.extend(b"mdat");
        out.extend(&payload);
        out
    }
}

// ---------------------------------------------------------------------------
// Annex B / AVCC helpers
// ---------------------------------------------------------------------------

/// Convert Annex B (start-code prefixed) to AVCC (4-byte BE length prefixed).
pub fn annex_b_to_avcc(annex_b: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(annex_b.len());
    let mut pos = 0;
    while pos + 4 <= annex_b.len() {
        if annex_b[pos..pos + 4] == [0x00, 0x00, 0x00, 0x01] {
            pos += 4;
            // Find end of this NAL unit (next start code or end of data)
            let mut end = pos;
            while end + 4 <= annex_b.len() {
                if annex_b[end..end + 4] == [0x00, 0x00, 0x00, 0x01] {
                    break;
                }
                end += 1;
            }
            if end > pos {
                let nal_len = (end - pos) as u32;
                out.extend_from_slice(&nal_len.to_be_bytes());
                out.extend_from_slice(&annex_b[pos..end]);
            }
            pos = end;
        } else {
            pos += 1;
        }
    }
    out
}

/// Extract SPS (NAL type 7) and PPS (NAL type 8) from an Annex B stream.
fn extract_parameter_sets(annex_b: &[u8]) -> Option<(Vec<u8>, Vec<u8>)> {
    let mut sps: Option<Vec<u8>> = None;
    let mut pps: Option<Vec<u8>> = None;
    let mut pos = 0;
    while pos + 4 <= annex_b.len() {
        if annex_b[pos..pos + 4] == [0x00, 0x00, 0x00, 0x01] {
            pos += 4;
            if pos >= annex_b.len() {
                break;
            }
            let nal_type = annex_b[pos] & 0x1f;
            // Find end of NAL
            let mut end = pos + 1;
            while end + 4 <= annex_b.len() {
                if annex_b[end..end + 4] == [0x00, 0x00, 0x00, 0x01] {
                    break;
                }
                end += 1;
            }
            // Include any trailing bytes up to end of data
            if end + 4 > annex_b.len() {
                end = annex_b.len();
            }
            match nal_type {
                7 => sps = Some(annex_b[pos..end].to_vec()),
                8 => pps = Some(annex_b[pos..end].to_vec()),
                _ => {}
            }
            pos = end;
        } else {
            pos += 1;
        }
    }
    match (sps, pps) {
        (Some(s), Some(p)) => Some((s, p)),
        _ => None,
    }
}

// ---------------------------------------------------------------------------
// ISO BMFF box builders
// ---------------------------------------------------------------------------

fn write_box(buf: &mut Vec<u8>, fourcc: &[u8; 4], payload: &[u8]) {
    let size = 8u32 + payload.len() as u32;
    buf.extend_from_slice(&size.to_be_bytes());
    buf.extend_from_slice(fourcc);
    buf.extend_from_slice(payload);
}

fn write_full_box(buf: &mut Vec<u8>, fourcc: &[u8; 4], version: u8, flags: u32, payload: &[u8]) {
    let mut full = Vec::with_capacity(4 + payload.len());
    full.push(version);
    full.push(((flags >> 16) & 0xff) as u8);
    full.push(((flags >> 8) & 0xff) as u8);
    full.push((flags & 0xff) as u8);
    full.extend_from_slice(payload);
    write_box(buf, fourcc, &full);
}

// ftyp: iso5, avc1 compatible
fn ftyp() -> Vec<u8> {
    let mut p = Vec::new();
    p.extend_from_slice(b"iso5"); // major brand
    p.extend_from_slice(&1u32.to_be_bytes()); // minor version
    p.extend_from_slice(b"iso5");
    p.extend_from_slice(b"avc1");
    p.extend_from_slice(b"iso2");
    let mut out = Vec::new();
    write_box(&mut out, b"ftyp", &p);
    out
}

// moov: movie box with video track (1) and data track (2)
fn moov(width: u32, height: u32, sps: &[u8], pps: &[u8]) -> Vec<u8> {
    let mut p = Vec::new();

    // mvhd: timescale = 90000, duration = 0 (unknown), next_track_id = 3
    {
        let mut mvhd_p = Vec::new();
        mvhd_p.extend_from_slice(&0u32.to_be_bytes()); // creation_time
        mvhd_p.extend_from_slice(&0u32.to_be_bytes()); // modification_time
        mvhd_p.extend_from_slice(&90000u32.to_be_bytes()); // timescale
        mvhd_p.extend_from_slice(&0u32.to_be_bytes()); // duration
        mvhd_p.extend_from_slice(&0x00010000u32.to_be_bytes()); // rate = 1.0
        mvhd_p.extend_from_slice(&0x0100u16.to_be_bytes()); // volume = 1.0
        mvhd_p.extend_from_slice(&[0u8; 10]); // reserved
                                              // identity matrix: {0x10000,0, 0, 0,0x10000,0, 0,0,0x40000000}
        for v in &[0x00010000u32, 0, 0, 0, 0x00010000, 0, 0, 0, 0x40000000u32] {
            mvhd_p.extend_from_slice(&v.to_be_bytes());
        }
        mvhd_p.extend_from_slice(&[0u8; 24]); // pre_defined
        mvhd_p.extend_from_slice(&3u32.to_be_bytes()); // next_track_id
        write_full_box(&mut p, b"mvhd", 0, 0, &mvhd_p);
    }

    // trak for video (track_id=1)
    p.extend(trak_video(1, width, height, sps, pps));

    // trak for data track (track_id=2)
    p.extend(trak_data(2));

    // mvex: movie extends (required for fragmented MP4)
    {
        let mut mvex_p = Vec::new();
        // trex for video track
        mvex_p.extend(trex(1));
        // trex for data track
        mvex_p.extend(trex(2));
        write_box(&mut p, b"mvex", &mvex_p);
    }

    let mut out = Vec::new();
    write_box(&mut out, b"moov", &p);
    out
}

fn trex(track_id: u32) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend_from_slice(&track_id.to_be_bytes());
    p.extend_from_slice(&1u32.to_be_bytes()); // default_sample_description_index
    p.extend_from_slice(&0u32.to_be_bytes()); // default_sample_duration
    p.extend_from_slice(&0u32.to_be_bytes()); // default_sample_size
    p.extend_from_slice(&0u32.to_be_bytes()); // default_sample_flags
    let mut out = Vec::new();
    write_full_box(&mut out, b"trex", 0, 0, &p);
    out
}

fn trak_video(track_id: u32, width: u32, height: u32, sps: &[u8], pps: &[u8]) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend(tkhd_video(track_id, width, height));
    p.extend(mdia_video(width, height, sps, pps));
    let mut out = Vec::new();
    write_box(&mut out, b"trak", &p);
    out
}

fn trak_data(track_id: u32) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend(tkhd_data(track_id));
    p.extend(mdia_data());
    let mut out = Vec::new();
    write_box(&mut out, b"trak", &p);
    out
}

fn tkhd(track_id: u32, duration: u32, width: u32, height: u32, flags: u32) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend_from_slice(&0u32.to_be_bytes()); // creation_time
    p.extend_from_slice(&0u32.to_be_bytes()); // modification_time
    p.extend_from_slice(&track_id.to_be_bytes());
    p.extend_from_slice(&0u32.to_be_bytes()); // reserved
    p.extend_from_slice(&duration.to_be_bytes());
    p.extend_from_slice(&[0u8; 8]); // reserved
    p.extend_from_slice(&0u16.to_be_bytes()); // layer
    p.extend_from_slice(&0u16.to_be_bytes()); // alternate_group
    p.extend_from_slice(&0u16.to_be_bytes()); // volume (0 for video)
    p.extend_from_slice(&0u16.to_be_bytes()); // reserved
                                              // identity matrix
    for v in &[0x00010000u32, 0, 0, 0, 0x00010000, 0, 0, 0, 0x40000000u32] {
        p.extend_from_slice(&v.to_be_bytes());
    }
    p.extend_from_slice(&(width << 16).to_be_bytes()); // width (16.16)
    p.extend_from_slice(&(height << 16).to_be_bytes()); // height (16.16)
    let mut out = Vec::new();
    write_full_box(&mut out, b"tkhd", 0, flags, &p);
    out
}

fn tkhd_video(track_id: u32, width: u32, height: u32) -> Vec<u8> {
    tkhd(track_id, 0, width, height, 3) // flags=3: enabled + in_movie
}

fn tkhd_data(track_id: u32) -> Vec<u8> {
    tkhd(track_id, 0, 0, 0, 3)
}

fn mdhd(timescale: u32) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend_from_slice(&0u32.to_be_bytes()); // creation_time
    p.extend_from_slice(&0u32.to_be_bytes()); // modification_time
    p.extend_from_slice(&timescale.to_be_bytes());
    p.extend_from_slice(&0u32.to_be_bytes()); // duration
    p.extend_from_slice(&0x55c4u16.to_be_bytes()); // language 'und'
    p.extend_from_slice(&0u16.to_be_bytes()); // pre_defined
    let mut out = Vec::new();
    write_full_box(&mut out, b"mdhd", 0, 0, &p);
    out
}

fn hdlr(handler_type: &[u8; 4], name: &[u8]) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend_from_slice(&0u32.to_be_bytes()); // pre_defined
    p.extend_from_slice(handler_type);
    p.extend_from_slice(&[0u8; 12]); // reserved
    p.extend_from_slice(name);
    p.push(0); // null terminator
    let mut out = Vec::new();
    write_full_box(&mut out, b"hdlr", 0, 0, &p);
    out
}

fn dinf_url() -> Vec<u8> {
    // url box with flags=1 (self-contained)
    let mut url = Vec::new();
    write_full_box(&mut url, b"url ", 0, 1, &[]);

    // dref with entry_count=1 and url entry
    let mut dref_p = Vec::new();
    dref_p.extend_from_slice(&1u32.to_be_bytes()); // entry_count
    dref_p.extend(&url);
    let mut dref = Vec::new();
    write_full_box(&mut dref, b"dref", 0, 0, &dref_p);

    let mut out = Vec::new();
    write_box(&mut out, b"dinf", &dref);
    out
}

fn stbl_empty_video(sps: &[u8], pps: &[u8], width: u32, height: u32) -> Vec<u8> {
    let mut p = Vec::new();

    // stsd: sample description (avc1 entry)
    {
        let avcc = avcc_box(sps, pps);
        let mut avc1_p = Vec::new();
        avc1_p.extend_from_slice(&[0u8; 6]); // reserved
        avc1_p.extend_from_slice(&1u16.to_be_bytes()); // data_reference_index
        avc1_p.extend_from_slice(&[0u8; 16]); // pre_defined + reserved
        avc1_p.extend_from_slice(&(width as u16).to_be_bytes()); // width
        avc1_p.extend_from_slice(&(height as u16).to_be_bytes()); // height
        avc1_p.extend_from_slice(&0x00480000u32.to_be_bytes()); // horiz resolution 72dpi
        avc1_p.extend_from_slice(&0x00480000u32.to_be_bytes()); // vert resolution 72dpi
        avc1_p.extend_from_slice(&0u32.to_be_bytes()); // reserved
        avc1_p.extend_from_slice(&1u16.to_be_bytes()); // frame_count = 1
        avc1_p.extend_from_slice(&[0u8; 32]); // compressorname (empty)
        avc1_p.extend_from_slice(&0x0018u16.to_be_bytes()); // depth = 24
        avc1_p.extend_from_slice(&0xffffu16.to_be_bytes()); // pre_defined = -1
        avc1_p.extend(&avcc);
        let mut avc1 = Vec::new();
        write_box(&mut avc1, b"avc1", &avc1_p);

        let mut stsd_p = Vec::new();
        stsd_p.extend_from_slice(&1u32.to_be_bytes()); // entry_count
        stsd_p.extend(&avc1);
        let mut stsd = Vec::new();
        write_full_box(&mut stsd, b"stsd", 0, 0, &stsd_p);
        p.extend(&stsd);
    }

    // stts, stsc, stsz, stco — all empty (required by spec)
    let mut stts = Vec::new();
    write_full_box(&mut stts, b"stts", 0, 0, &0u32.to_be_bytes()); // entry_count=0
    p.extend(&stts);

    let mut stsc = Vec::new();
    write_full_box(&mut stsc, b"stsc", 0, 0, &0u32.to_be_bytes());
    p.extend(&stsc);

    let mut stsz = Vec::new();
    // stsz: sample_size=0, sample_count=0
    let mut stsz_p = Vec::new();
    stsz_p.extend_from_slice(&0u32.to_be_bytes()); // sample_size
    stsz_p.extend_from_slice(&0u32.to_be_bytes()); // sample_count
    write_full_box(&mut stsz, b"stsz", 0, 0, &stsz_p);
    p.extend(&stsz);

    let mut stco = Vec::new();
    write_full_box(&mut stco, b"stco", 0, 0, &0u32.to_be_bytes());
    p.extend(&stco);

    let mut out = Vec::new();
    write_box(&mut out, b"stbl", &p);
    out
}

fn avcc_box(sps: &[u8], pps: &[u8]) -> Vec<u8> {
    let mut p = vec![
        1u8,                                 // configurationVersion
        sps.get(1).copied().unwrap_or(0x42), // AVCProfileIndication
        sps.get(2).copied().unwrap_or(0xe0), // profile_compatibility
        sps.get(3).copied().unwrap_or(0x1f), // AVCLevelIndication
        0xff,                                // lengthSizeMinusOne=3 | reserved 0b111111
        0xe1,                                // numSPS=1 | reserved 0b111
    ];
    p.extend_from_slice(&(sps.len() as u16).to_be_bytes());
    p.extend_from_slice(sps);
    p.push(1u8); // numPPS = 1
    p.extend_from_slice(&(pps.len() as u16).to_be_bytes());
    p.extend_from_slice(pps);
    let mut out = Vec::new();
    write_box(&mut out, b"avcC", &p);
    out
}

fn stbl_empty_data() -> Vec<u8> {
    let mut p = Vec::new();

    // stsd: use 'mett' (MPEG-4 Timed Text generic)
    {
        let mut mett_p = Vec::new();
        mett_p.extend_from_slice(&[0u8; 6]); // reserved
        mett_p.extend_from_slice(&1u16.to_be_bytes()); // data_reference_index
        mett_p.extend_from_slice(b"text/plain\0"); // mime type
        let mut mett = Vec::new();
        write_box(&mut mett, b"mett", &mett_p);

        let mut stsd_p = Vec::new();
        stsd_p.extend_from_slice(&1u32.to_be_bytes());
        stsd_p.extend(&mett);
        let mut stsd = Vec::new();
        write_full_box(&mut stsd, b"stsd", 0, 0, &stsd_p);
        p.extend(&stsd);
    }

    let mut stts = Vec::new();
    write_full_box(&mut stts, b"stts", 0, 0, &0u32.to_be_bytes());
    p.extend(&stts);

    let mut stsc = Vec::new();
    write_full_box(&mut stsc, b"stsc", 0, 0, &0u32.to_be_bytes());
    p.extend(&stsc);

    let mut stsz = Vec::new();
    let mut stsz_p = Vec::new();
    stsz_p.extend_from_slice(&0u32.to_be_bytes());
    stsz_p.extend_from_slice(&0u32.to_be_bytes());
    write_full_box(&mut stsz, b"stsz", 0, 0, &stsz_p);
    p.extend(&stsz);

    let mut stco = Vec::new();
    write_full_box(&mut stco, b"stco", 0, 0, &0u32.to_be_bytes());
    p.extend(&stco);

    let mut out = Vec::new();
    write_box(&mut out, b"stbl", &p);
    out
}

fn mdia_video(width: u32, height: u32, sps: &[u8], pps: &[u8]) -> Vec<u8> {
    let mut p = Vec::new();
    p.extend(mdhd(90000));
    p.extend(hdlr(b"vide", b"Video"));
    // minf
    {
        let mut minf_p = Vec::new();
        // vmhd
        {
            let mut vmhd_p = Vec::new();
            vmhd_p.extend_from_slice(&0u16.to_be_bytes()); // graphicsMode
            vmhd_p.extend_from_slice(&[0u8; 6]); // opcolor
            let mut vmhd = Vec::new();
            write_full_box(&mut vmhd, b"vmhd", 0, 1, &vmhd_p);
            minf_p.extend(&vmhd);
        }
        minf_p.extend(dinf_url());
        minf_p.extend(stbl_empty_video(sps, pps, width, height));
        write_box(&mut p, b"minf", &minf_p);
    }
    let mut out = Vec::new();
    write_box(&mut out, b"mdia", &p);
    out
}

fn mdia_data() -> Vec<u8> {
    let mut p = Vec::new();
    p.extend(mdhd(1000)); // millisecond timescale for events
    p.extend(hdlr(b"text", b"InputEvents"));
    // minf with nmhd (null media header)
    {
        let mut minf_p = Vec::new();
        let mut nmhd = Vec::new();
        write_full_box(&mut nmhd, b"nmhd", 0, 0, &[]);
        minf_p.extend(&nmhd);
        minf_p.extend(dinf_url());
        minf_p.extend(stbl_empty_data());
        write_box(&mut p, b"minf", &minf_p);
    }
    let mut out = Vec::new();
    write_box(&mut out, b"mdia", &p);
    out
}

// ---------------------------------------------------------------------------
// moof + mdat builders
// ---------------------------------------------------------------------------

// Video fragment: single sample, fixed moof size = 96 bytes → data_offset = 104
//
// Precomputed moof layout:
//   moof header:  8
//   mfhd:        16  (8 + 4 version+flags + 4 seq)
//   traf:
//     traf header: 8
//     tfhd:       16  (8 + 4 v+f + 4 track_id)   flags=0x000020
//     tfdt:       16  (8 + 4 v+f + 4 base_decode_time)  version=0
//     trun:       32  (8 + 4 v+f + 4 count + 4 data_offset + 4 first_sample_flags
//                         + 4 duration + 4 size)  flags=0x0305
//   traf total:  8 + 16 + 16 + 32 = 72
//   moof total:  8 + 16 + 72 = 96
//   data_offset: 96 + 8 = 104
const MOOF_VIDEO_SIZE: u32 = 96;
const VIDEO_DATA_OFFSET: i32 = (MOOF_VIDEO_SIZE + 8) as i32;

// Sample flags for keyframes and non-keyframes
const SAMPLE_FLAGS_KEYFRAME: u32 = 0x02000000; // sample_depends_on=2 (independent)
const SAMPLE_FLAGS_DELTA: u32 = 0x01010000; // sample_depends_on=1 + non_sync=1

fn moof_video(seq: u32, pts: u32, duration: u32, sample_size: u32, is_keyframe: bool) -> Vec<u8> {
    let mut out = Vec::with_capacity(MOOF_VIDEO_SIZE as usize);

    // moof header (written last once we know size — but size is fixed at 96)
    let moof_size = MOOF_VIDEO_SIZE.to_be_bytes();
    out.extend_from_slice(&moof_size);
    out.extend_from_slice(b"moof");

    // mfhd
    {
        let mut p = Vec::new();
        p.extend_from_slice(&seq.to_be_bytes());
        write_full_box(&mut out, b"mfhd", 0, 0, &p);
    }

    // traf
    {
        let mut traf_p = Vec::new();

        // tfhd: flags=0x000020 (default-base-is-moof)
        {
            let mut p = Vec::new();
            p.extend_from_slice(&1u32.to_be_bytes()); // track_id
            write_full_box(&mut traf_p, b"tfhd", 0, 0x000020, &p);
        }

        // tfdt: base_media_decode_time = pts (version=0, u32)
        {
            let mut p = Vec::new();
            p.extend_from_slice(&pts.to_be_bytes());
            write_full_box(&mut traf_p, b"tfdt", 0, 0, &p);
        }

        // trun: 1 sample, flags=0x0305
        //   0x0001: data-offset-present
        //   0x0004: first-sample-flags-present
        //   0x0100: sample-duration-present
        //   0x0200: sample-size-present
        {
            let first_sample_flags = if is_keyframe {
                SAMPLE_FLAGS_KEYFRAME
            } else {
                SAMPLE_FLAGS_DELTA
            };
            let mut p = Vec::new();
            p.extend_from_slice(&1u32.to_be_bytes()); // sample_count
            p.extend_from_slice(&VIDEO_DATA_OFFSET.to_be_bytes()); // data_offset
            p.extend_from_slice(&first_sample_flags.to_be_bytes());
            p.extend_from_slice(&duration.to_be_bytes());
            p.extend_from_slice(&sample_size.to_be_bytes());
            write_full_box(&mut traf_p, b"trun", 0, 0x0305, &p);
        }

        write_box(&mut out, b"traf", &traf_p);
    }

    debug_assert_eq!(
        out.len(),
        MOOF_VIDEO_SIZE as usize,
        "moof_video size mismatch"
    );
    out
}

// Data fragment: 1 bundled sample for all events in this batch
// moof size: 8 + mfhd(16) + traf(8 + tfhd(16) + tfdt(16) + trun(28)) = 8+16+68 = 92
// data_offset: 92 + 8 = 100
const MOOF_DATA_SIZE: u32 = 92;
const DATA_DATA_OFFSET: i32 = (MOOF_DATA_SIZE + 8) as i32;

fn moof_data(seq: u32, base_ts_ms: u32, payload_size: u32, duration: u32) -> Vec<u8> {
    let mut out = Vec::with_capacity(MOOF_DATA_SIZE as usize);

    out.extend_from_slice(&MOOF_DATA_SIZE.to_be_bytes());
    out.extend_from_slice(b"moof");

    // mfhd
    {
        let mut p = Vec::new();
        p.extend_from_slice(&seq.to_be_bytes());
        write_full_box(&mut out, b"mfhd", 0, 0, &p);
    }

    // traf
    {
        let mut traf_p = Vec::new();

        // tfhd: track_id=2, flags=0x000020
        {
            let mut p = Vec::new();
            p.extend_from_slice(&2u32.to_be_bytes()); // track_id
            write_full_box(&mut traf_p, b"tfhd", 0, 0x000020, &p);
        }

        // tfdt: base_media_decode_time = base_ts_ms
        {
            let mut p = Vec::new();
            p.extend_from_slice(&base_ts_ms.to_be_bytes());
            write_full_box(&mut traf_p, b"tfdt", 0, 0, &p);
        }

        // trun: 1 bundled sample, flags=0x0301 (data-offset + duration + size)
        {
            let mut p = Vec::new();
            p.extend_from_slice(&1u32.to_be_bytes()); // sample_count
            p.extend_from_slice(&DATA_DATA_OFFSET.to_be_bytes()); // data_offset
            p.extend_from_slice(&duration.to_be_bytes()); // sample_duration
            p.extend_from_slice(&payload_size.to_be_bytes()); // sample_size
            write_full_box(&mut traf_p, b"trun", 0, 0x0301, &p);
        }

        write_box(&mut out, b"traf", &traf_p);
    }

    debug_assert_eq!(
        out.len(),
        MOOF_DATA_SIZE as usize,
        "moof_data size mismatch"
    );
    out
}

use crate::audio::{float_to_pcm, AudioConfig, AudioPacket, AudioStream};

#[test]
fn test_audio_config_default() {
    let config = AudioConfig::default();
    assert!(!config.enabled);
    assert_eq!(config.sample_rate, 44100);
    assert_eq!(config.bits_per_sample, 16);
    assert_eq!(config.channels, 2);
}

#[test]
fn test_audio_config_bytes() {
    let config = AudioConfig::default();
    assert_eq!(config.bytes_per_frame(), 4); // 16-bit stereo
    assert_eq!(config.bytes_per_second(), 176400);
}

#[test]
fn test_audio_stream() {
    let config = AudioConfig {
        enabled: true,
        ..Default::default()
    };
    let mut stream = AudioStream::new(config, 1);

    let start = stream.start();
    assert!(start.is_some());
    assert!(stream.is_active());

    let packet = AudioPacket {
        data: vec![0u8; 100],
        timestamp: 0,
    };
    let blob = stream.send_packet(&packet);
    assert!(blob.is_some());

    let stop = stream.stop();
    assert!(stop.is_some());
    assert!(!stream.is_active());
}

#[test]
fn test_float_to_pcm_16bit() {
    let samples = vec![0.0f32, 0.5, -0.5, 1.0, -1.0];
    let pcm = float_to_pcm(&samples, 1, 16);

    // 0.0 -> 0
    assert_eq!(pcm[0], 0);
    assert_eq!(pcm[1], 0);

    // 0.5 -> ~16383 (0x3FFF)
    assert!(pcm[2] > 0xF0);
    assert!(pcm[3] > 0x3E);
}

#[test]
fn test_float_to_pcm_8bit() {
    let samples = vec![0.0f32, 1.0, -1.0];
    let pcm = float_to_pcm(&samples, 1, 8);

    // 0.0 -> 128
    assert_eq!(pcm[0], 128);
    // 1.0 -> ~255
    assert!(pcm[1] > 250);
    // -1.0 -> ~0
    assert!(pcm[2] < 5);
}

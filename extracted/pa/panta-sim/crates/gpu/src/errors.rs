//! GPU 백엔드 에러 타입.

use std::fmt;

/// GPU 백엔드 에러.
#[derive(Debug)]
pub enum GpuError {
    /// wgpu adapter 를 찾지 못함 (Vulkan / Metal / DX12 ICD 부재).
    NoAdapter,
    /// wgpu device request 실패.
    DeviceCreation(String),
    /// shader compile / pipeline creation 실패.
    Shader(String),
    /// buffer mapping / IO 에러.
    Buffer(String),
    /// 지원되지 않는 game/feature.
    Unsupported(String),
    /// 일반 wgpu 에러.
    Other(String),
}

impl fmt::Display for GpuError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            GpuError::NoAdapter => write!(
                f,
                "no GPU adapter found (Vulkan / Metal / DX12 ICD 부재 — \
                 mesa-vulkan-drivers 같은 software adapter 설치 필요할 수 있음)"
            ),
            GpuError::DeviceCreation(s) => write!(f, "wgpu device 생성 실패: {s}"),
            GpuError::Shader(s) => write!(f, "shader compile / pipeline 실패: {s}"),
            GpuError::Buffer(s) => write!(f, "buffer IO 실패: {s}"),
            GpuError::Unsupported(s) => write!(f, "지원되지 않음: {s}"),
            GpuError::Other(s) => write!(f, "GPU error: {s}"),
        }
    }
}

impl std::error::Error for GpuError {}

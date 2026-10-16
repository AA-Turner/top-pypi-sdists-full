use crate::config::{find_unique_path, RecordingConfig};
use crate::ses::RecordingError;
use crate::writer_thread::SinkTarget;
use rustix::fs::{fcntl_getfl, fcntl_setfl, open, Mode, OFlags};
use rustix::io::Errno;
use std::collections::HashMap;
use std::fs::File;
use std::io;
use std::os::unix::fs::{FileTypeExt, MetadataExt};
use std::path::PathBuf;
use std::time::{Duration, Instant};

#[derive(Clone, Copy)]
enum Destination {
    Ses,
    Asciicast,
    Typescript,
    Timing,
    Video,
}

pub(crate) async fn open_video(path: PathBuf, wait: Duration) -> Result<File, RecordingError> {
    open_one(
        path,
        Destination::Video,
        RecordingConfig::default(),
        Instant::now() + wait,
    )
    .await
}

pub(super) async fn prepare(
    config: &RecordingConfig,
    params: &HashMap<String, String>,
    protocol: &str,
    wait: Duration,
) -> Result<[Option<SinkTarget>; 4], RecordingError> {
    let deadline = Instant::now() + wait;
    let ses = if config.ses_zmq_addr.is_some() {
        None
    } else {
        config.get_ses_path(params, protocol)
    };
    let asciicast = config.get_asciicast_path(params, protocol);
    let typescript = config.get_typescript_path(params, protocol);
    let timing = typescript.as_ref().map(|path| {
        let mut name = path.file_name().unwrap_or_default().to_os_string();
        name.push(".timing");
        path.with_file_name(name)
    });

    let mut targets: [Option<SinkTarget>; 4] = [None, None, None, None];
    for (index, path, kind) in [
        (0, ses, Destination::Ses),
        (1, asciicast, Destination::Asciicast),
        (2, typescript, Destination::Typescript),
        (3, timing, Destination::Timing),
    ] {
        if let Some(path) = path {
            targets[index] = Some(SinkTarget::File(
                open_one(path, kind, config.clone(), deadline).await?,
            ));
        }
    }
    Ok(targets)
}

async fn open_one(
    path: PathBuf,
    kind: Destination,
    config: RecordingConfig,
    deadline: Instant,
) -> Result<File, RecordingError> {
    let mut expected_fifo = false;
    loop {
        let path = path.clone();
        let config = config.clone();
        let result =
            tokio::task::spawn_blocking(move || open_once(&path, kind, &config, expected_fifo))
                .await
                .map_err(|err| RecordingError::Unrecordable(err.to_string()))?;
        match result {
            Err(RecordingError::Io(ref err))
                if err.raw_os_error() == io::Error::from(Errno::NXIO).raw_os_error() =>
            {
                expected_fifo = true;
                if Instant::now() >= deadline {
                    return Err(io::Error::new(
                        io::ErrorKind::TimedOut,
                        "recording FIFO has no reader before admission deadline",
                    )
                    .into());
                }
                tokio::time::sleep_until(tokio::time::Instant::from_std(
                    deadline.min(Instant::now() + Duration::from_millis(25)),
                ))
                .await;
            }
            other => return other,
        }
    }
}

fn open_once(
    path: &PathBuf,
    kind: Destination,
    config: &RecordingConfig,
    expected_fifo: bool,
) -> Result<File, RecordingError> {
    let create_parent = match kind {
        Destination::Ses | Destination::Asciicast => config.create_recording_path,
        Destination::Typescript | Destination::Timing => config.create_typescript_path,
        Destination::Video => false,
    };
    if let Some(parent) = path.parent() {
        if !parent.exists() {
            if create_parent {
                std::fs::create_dir_all(parent)?;
            } else if matches!(kind, Destination::Ses) {
                return Err(RecordingError::PathCreation(format!(
                    "Directory does not exist: {parent:?}"
                )));
            }
        }
    }

    let existing = std::fs::metadata(path).ok();
    let fifo = existing
        .as_ref()
        .is_some_and(|meta| meta.file_type().is_fifo());
    if expected_fifo && !fifo {
        return Err(io::Error::other("recording FIFO disappeared or was replaced").into());
    }
    let write_existing = match kind {
        Destination::Ses | Destination::Asciicast => config.recording_write_existing,
        Destination::Typescript | Destination::Timing => config.typescript_write_existing,
        Destination::Video => true,
    };
    let actual = match kind {
        Destination::Ses if existing.is_some() && !fifo && !write_existing => {
            find_unique_path(path, 255).ok_or_else(|| {
                RecordingError::FileExists(format!("All candidate paths exhausted for: {path:?}"))
            })?
        }
        Destination::Asciicast | Destination::Typescript
            if existing.is_some() && !fifo && !write_existing =>
        {
            return Err(RecordingError::FileExists(format!("File exists: {path:?}")))
        }
        _ => path.clone(),
    };

    // O_NONBLOCK prevents an unread FIFO from parking the opening thread; O_NOFOLLOW
    // ensures a replaced FIFO cannot redirect recording bytes into a symlink target.
    let flags = OFlags::WRONLY
        | OFlags::NONBLOCK
        | OFlags::CLOEXEC
        | if fifo {
            OFlags::NOFOLLOW
        } else {
            OFlags::CREATE | OFlags::TRUNC
        };
    let fd = open(&actual, flags, Mode::from_raw_mode(0o666)).map_err(io::Error::from)?;
    let file = File::from(fd);
    if fifo {
        let opened = file.metadata()?;
        let current = std::fs::metadata(path)?;
        if !opened.file_type().is_fifo()
            || !current.file_type().is_fifo()
            || opened.dev() != current.dev()
            || opened.ino() != current.ino()
        {
            return Err(io::Error::other("recording FIFO was replaced during open").into());
        }
    }
    let mut status = fcntl_getfl(&file).map_err(io::Error::from)?;
    status.remove(OFlags::NONBLOCK);
    fcntl_setfl(&file, status).map_err(io::Error::from)?;
    Ok(file)
}

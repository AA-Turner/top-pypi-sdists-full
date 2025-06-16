use crate::cli::{FreezeOptions, Process};
use crate::lockfile::v0::LockfileV0;
use crate::lockfile::v1::LockfileV1;
use anyhow::bail;
use core::fmt::Debug;
use serde::Serialize;

static LATEST_VERSION: &str = "1";

pub trait Freeze {
    async fn freeze(options: &FreezeOptions) -> anyhow::Result<i32>
    where
        Self: Sized + Debug + Serialize;
}

impl Process for FreezeOptions {
    async fn process(self) -> anyhow::Result<i32> {
        let version = self.version.as_ref().map_or(LATEST_VERSION, |ver| ver);

        match version {
            #[cfg(debug_assertions)]
            "0" => LockfileV0::freeze(&self).await,
            "1" => LockfileV1::freeze(&self).await,
            _ => {
                bail!("Unsupported version!")
            },
        }
    }
}

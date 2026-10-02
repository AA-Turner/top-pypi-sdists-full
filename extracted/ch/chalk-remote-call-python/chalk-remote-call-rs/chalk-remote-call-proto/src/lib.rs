#[allow(clippy::all, clippy::empty_docs)]
pub mod chalk {
    pub mod auth {
        pub mod v1 {
            include!("gen/chalk.auth.v1.rs");
        }
    }
    pub mod common {
        pub mod v1 {
            include!("gen/chalk.common.v1.rs");
        }
    }
    pub mod runtime {
        pub mod v1 {
            include!("gen/chalk.runtime.v1.rs");

            pub const FILE_DESCRIPTOR_SET: &[u8] = include_bytes!("gen/descriptor.bin");
        }
    }
    pub mod utils {
        pub mod v1 {
            include!("gen/chalk.utils.v1.rs");
        }
    }
}

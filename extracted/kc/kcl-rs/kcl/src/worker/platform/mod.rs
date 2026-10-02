//! Port of `software.amazon.kinesis.worker.platform`.
//!
//! Compute-platform detection (EC2/ECS/EKS) and operating-range provider
//! selection.

pub mod ec2_resource;
pub mod ecs_resource;
pub mod eks_resource;
pub mod operating_range_data_provider;
pub mod resource_metadata_provider;
pub mod url_opener;

pub use ec2_resource::Ec2Resource;
pub use ecs_resource::{EcsResource, ECS_METADATA_KEY_V3, ECS_METADATA_KEY_V4};
pub use eks_resource::EksResource;
pub use operating_range_data_provider::OperatingRangeDataProvider;
pub use resource_metadata_provider::{ComputePlatform, ResourceMetadataProvider};
pub use url_opener::{HttpConnection, UrlOpener};

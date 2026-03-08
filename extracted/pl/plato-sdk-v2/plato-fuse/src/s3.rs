use crate::config::S3Config;
use std::sync::Arc;
use tokio::sync::Semaphore;

pub struct S3Downloader {
    config: S3Config,
    client: aws_sdk_s3::Client,
    runtime: tokio::runtime::Runtime,
    semaphore: Arc<Semaphore>,
}

impl S3Downloader {
    pub fn new(config: S3Config) -> Self {
        let runtime = tokio::runtime::Builder::new_multi_thread()
            .worker_threads(4)
            .enable_all()
            .build()
            .expect("Failed to create tokio runtime");

        let client = runtime.block_on(async {
            let region = config
                .credentials
                .get("AWS_DEFAULT_REGION")
                .expect("AWS_DEFAULT_REGION not set in s3_config credentials")
                .clone();

            let access_key = config
                .credentials
                .get("AWS_ACCESS_KEY_ID")
                .expect("AWS_ACCESS_KEY_ID not set in s3_config credentials")
                .clone();
            let secret_key = config
                .credentials
                .get("AWS_SECRET_ACCESS_KEY")
                .expect("AWS_SECRET_ACCESS_KEY not set in s3_config credentials")
                .clone();

            let cred_provider = aws_credential_types::Credentials::new(
                access_key,
                secret_key,
                config.credentials.get("AWS_SESSION_TOKEN").cloned(),
                None,
                "plato-fuse",
            );

            let aws_config = aws_config::defaults(aws_config::BehaviorVersion::latest())
                .region(aws_config::Region::new(region))
                .credentials_provider(cred_provider)
                .load()
                .await;

            aws_sdk_s3::Client::new(&aws_config)
        });

        S3Downloader {
            config,
            client,
            runtime,
            semaphore: Arc::new(Semaphore::new(32)),
        }
    }

    pub fn download(&self, md5: &str) -> Result<Vec<u8>, Box<dyn std::error::Error + Send + Sync>> {
        let key = self.config.file_key(md5);
        let sem = self.semaphore.clone();

        self.runtime.block_on(async {
            let _permit = sem.acquire().await?;

            let resp = self
                .client
                .get_object()
                .bucket(&self.config.bucket)
                .key(&key)
                .send()
                .await?;

            let bytes = resp.body.collect().await?.into_bytes().to_vec();
            Ok(bytes)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    fn s3_config() -> S3Config {
        let mut credentials = HashMap::new();
        credentials.insert("AWS_DEFAULT_REGION".to_string(), "us-east-1".to_string());
        credentials.insert(
            "AWS_ACCESS_KEY_ID".to_string(),
            "test-access-key".to_string(),
        );
        credentials.insert(
            "AWS_SECRET_ACCESS_KEY".to_string(),
            "test-secret-key".to_string(),
        );
        credentials.insert(
            "AWS_SESSION_TOKEN".to_string(),
            "test-session-token".to_string(),
        );

        S3Config {
            bucket: "test-bucket".to_string(),
            prefix: "workspace/test".to_string(),
            credentials,
        }
    }

    #[test]
    fn new_should_build_downloader_with_complete_credentials() {
        let downloader = S3Downloader::new(s3_config());
        assert_eq!(downloader.config.bucket, "test-bucket");
        assert_eq!(
            downloader.config.file_key("abcdef"),
            "workspace/test/dvc-cache/files/md5/ab/cdef"
        );
    }

    #[test]
    #[should_panic(expected = "AWS_DEFAULT_REGION not set in s3_config credentials")]
    fn new_should_panic_without_region() {
        let mut config = s3_config();
        config.credentials.remove("AWS_DEFAULT_REGION");
        let _ = S3Downloader::new(config);
    }

    #[test]
    #[should_panic(expected = "AWS_ACCESS_KEY_ID not set in s3_config credentials")]
    fn new_should_panic_without_access_key() {
        let mut config = s3_config();
        config.credentials.remove("AWS_ACCESS_KEY_ID");
        let _ = S3Downloader::new(config);
    }

    #[test]
    #[should_panic(expected = "AWS_SECRET_ACCESS_KEY not set in s3_config credentials")]
    fn new_should_panic_without_secret_key() {
        let mut config = s3_config();
        config.credentials.remove("AWS_SECRET_ACCESS_KEY");
        let _ = S3Downloader::new(config);
    }
}

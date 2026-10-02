//! Port of `software.amazon.kinesis.retrieval.DataFetchingStrategy`.

/// The record-fetching strategy: classic direct polling or background prefetch.
///
/// Port of the Java C-like enum.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum DataFetchingStrategy {
    /// Fetch records on demand.
    Default,
    /// Prefetch records into a bounded cache in the background.
    PrefetchCached,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn variants_are_distinct() {
        assert_ne!(
            DataFetchingStrategy::Default,
            DataFetchingStrategy::PrefetchCached
        );
    }
}

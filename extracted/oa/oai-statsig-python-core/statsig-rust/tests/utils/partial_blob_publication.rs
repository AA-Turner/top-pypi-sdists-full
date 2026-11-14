// These integration binaries exercise the opted-in policy. Set it before the test harness starts threads.
ctor::declarative::ctor!(
    #[ctor(unsafe)]
    fn enable_partial_blob_publication() {
        std::env::set_var("STATSIG_ENABLE_PARTIAL_BLOB_PUBLICATION", "true");
    }
);

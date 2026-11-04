use statsig_rust::statsig_global::StatsigGlobal;

#[test]
fn repeated_gets_share_the_same_process_global() {
    let global = StatsigGlobal::get();
    let global_again = StatsigGlobal::get();

    assert!(std::sync::Arc::ptr_eq(&global, &global_again));
}

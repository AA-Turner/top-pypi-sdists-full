use statsig_rust::statsig_global::StatsigGlobal;

#[test]
fn test_get_runtime() {
    let global = StatsigGlobal::get();
    let global_again = StatsigGlobal::get();

    assert_eq!(global.pid, global_again.pid);
}

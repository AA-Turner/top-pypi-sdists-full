// Performance tests for database query execution and rendering.
// Run with: cargo test -p guacr-database --test performance_test -- --include-ignored
#[cfg(test)]
mod performance_tests {
    use std::time::Instant;

    #[tokio::test]
    #[ignore]
    async fn test_query_executor_render_throughput() {
        use guacr_database::QueryExecutor;
        use guacr_terminal::QueryResult;

        let mut executor = QueryExecutor::new_with_size("mysql> ", "mysql", 40, 120)
            .expect("executor must construct");

        let mut result = QueryResult::new(vec![
            "id".to_string(),
            "name".to_string(),
            "value".to_string(),
        ]);
        for i in 0..100 {
            result.add_row(vec![
                i.to_string(),
                format!("row_{}", i),
                format!("val_{}", i),
            ]);
        }
        executor.write_result(&result).unwrap();

        let iterations = 60;
        let start = Instant::now();

        for _ in 0..iterations {
            let (_, instructions) = executor.render_screen().await.expect("render must succeed");
            assert!(!instructions.is_empty());
        }

        let elapsed = start.elapsed();
        println!(
            "QueryExecutor render throughput: {} renders in {:?} ({:.1} renders/sec)",
            iterations,
            elapsed,
            iterations as f64 / elapsed.as_secs_f64()
        );
    }

    #[test]
    #[ignore]
    fn test_result_set_rendering_speed() {
        use guacr_terminal::QueryResult;

        let start = Instant::now();
        let iterations = 1000;

        for i in 0..iterations {
            let mut result = QueryResult::new(vec![
                "id".to_string(),
                "name".to_string(),
                "data".to_string(),
            ]);
            for j in 0..50 {
                result.add_row(vec![
                    j.to_string(),
                    format!("user_{}", j),
                    format!("data_{}_{}", i, j),
                ]);
            }
            // Simulate serialization overhead
            let _ = serde_json::to_string(&result.columns).unwrap();
        }

        let elapsed = start.elapsed();
        println!(
            "Result set construction: {} iterations in {:?} ({:.0} ops/sec)",
            iterations,
            elapsed,
            iterations as f64 / elapsed.as_secs_f64()
        );
    }
}

use crate::buffer_pool::BufferPool;

#[test]
fn test_buffer_pool_acquire_release() {
    let pool = BufferPool::new(2, 1024);

    let buf1 = pool.acquire();
    assert_eq!(buf1.capacity(), 1024);

    let buf2 = pool.acquire();
    assert_eq!(buf2.capacity(), 1024);

    // Pool should be empty now
    let buf3 = pool.acquire();
    assert_eq!(buf3.capacity(), 1024); // New allocation

    // Release buffers
    pool.release(buf1);
    pool.release(buf2);

    // Should get pre-allocated buffers now
    let buf4 = pool.acquire();
    assert_eq!(buf4.capacity(), 1024);
}

#[test]
fn test_buffer_pool_stats() {
    let pool = BufferPool::new(4, 2048);
    let stats = pool.stats();

    assert_eq!(stats.pool_size, 4);
    assert_eq!(stats.buffer_size, 2048);
    assert_eq!(stats.available, 4); // All available initially
}

"""Tests for SHM Ring Buffer implementation.

Run with: pytest tests/test_shm_ring_buffer.py -v
"""
import pytest
import time
import threading
import multiprocessing
import numpy as np
from multiprocessing import shared_memory

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from matrice_common.stream.shm_ring_buffer import (
    ShmRingBuffer,
    bgr_to_nv12,
    nv12_to_bgr,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def cleanup_shm():
    """Cleanup any leftover SHM segments after tests."""
    created_buffers = []
    yield created_buffers
    for buf in created_buffers:
        try:
            buf.close()
        except Exception:
            pass


@pytest.fixture
def sample_frame():
    """Create a sample BGR frame (640x480)."""
    return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)


@pytest.fixture
def small_frame():
    """Create a small BGR frame for faster tests (64x64)."""
    return np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)


# =============================================================================
# Unit Tests: Basic Functionality
# =============================================================================

class TestShmRingBufferBasic:
    """Test basic SHM ring buffer operations."""

    def test_create_and_attach(self, cleanup_shm):
        """Test producer creates, consumer attaches."""
        camera_id = "test_basic_001"
        width, height = 64, 64

        # Producer creates
        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=5,
            create=True
        )
        cleanup_shm.append(producer)

        # Consumer attaches
        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=5,
            create=False
        )
        cleanup_shm.append(consumer)

        assert producer.shm_name == consumer.shm_name
        assert producer.frame_size == consumer.frame_size

    def test_write_and_read_frame(self, cleanup_shm, small_frame):
        """Test writing and reading a frame."""
        camera_id = "test_write_read_001"
        width, height = small_frame.shape[1], small_frame.shape[0]

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=5,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=5,
            create=False
        )
        cleanup_shm.append(consumer)

        # Write frame
        frame_bytes = small_frame.tobytes()
        frame_idx, slot = producer.write_frame(frame_bytes)

        assert frame_idx == 1
        assert slot == 1  # frame_idx % slot_count

        # Read frame
        read_bytes = consumer.read_frame_copy(frame_idx)
        assert read_bytes is not None
        assert read_bytes == frame_bytes

    def test_frame_validity(self, cleanup_shm, small_frame):
        """Test frame validity checking."""
        camera_id = "test_validity_001"
        width, height = small_frame.shape[1], small_frame.shape[0]

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,  # Small buffer
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=False
        )
        cleanup_shm.append(consumer)

        frame_bytes = small_frame.tobytes()

        # Write first frame
        frame_idx_1, _ = producer.write_frame(frame_bytes)
        assert consumer.is_frame_valid(frame_idx_1)

        # Write more frames to overwrite
        for _ in range(5):
            producer.write_frame(frame_bytes)

        # First frame should be invalid (overwritten)
        assert not consumer.is_frame_valid(frame_idx_1)

    def test_ring_buffer_wrapping(self, cleanup_shm, small_frame):
        """Test ring buffer wraps correctly."""
        camera_id = "test_wrap_001"
        width, height = small_frame.shape[1], small_frame.shape[0]
        slot_count = 3

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=slot_count,
            create=True
        )
        cleanup_shm.append(producer)

        frame_bytes = small_frame.tobytes()

        # Write more frames than slot_count
        slots_used = []
        for i in range(10):
            frame_idx, slot = producer.write_frame(frame_bytes)
            slots_used.append(slot)
            assert frame_idx == i + 1
            assert slot == (i + 1) % slot_count

        # Verify slots wrap around
        assert slots_used == [1, 2, 0, 1, 2, 0, 1, 2, 0, 1]


# =============================================================================
# Unit Tests: Torn Frame Detection
# =============================================================================

class TestTornFrameDetection:
    """Test torn frame detection with sequence counters."""

    def test_sequence_counters_initialized(self, cleanup_shm):
        """Test sequence counters are initialized to 0."""
        camera_id = "test_seq_init_001"

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=64,
            height=64,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=True
        )
        cleanup_shm.append(producer)

        # Check all slots have seq_start == seq_end == 0
        for slot in range(3):
            assert producer._read_slot_seq_start(slot) == 0
            assert producer._read_slot_seq_end(slot) == 0

    def test_sequence_counters_increment(self, cleanup_shm, small_frame):
        """Test sequence counters increment correctly on write."""
        camera_id = "test_seq_inc_001"
        width, height = small_frame.shape[1], small_frame.shape[0]

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=True
        )
        cleanup_shm.append(producer)

        frame_bytes = small_frame.tobytes()

        # Write first frame (goes to slot 1)
        frame_idx, slot = producer.write_frame(frame_bytes)
        assert slot == 1

        # Check sequence counters for slot 1
        seq_start = producer._read_slot_seq_start(slot)
        seq_end = producer._read_slot_seq_end(slot)
        assert seq_start == 1
        assert seq_end == 1
        assert seq_start == seq_end  # No torn frame

    def test_is_frame_torn(self, cleanup_shm, small_frame):
        """Test is_frame_torn() method."""
        camera_id = "test_torn_check_001"
        width, height = small_frame.shape[1], small_frame.shape[0]

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=False
        )
        cleanup_shm.append(consumer)

        frame_bytes = small_frame.tobytes()
        frame_idx, _ = producer.write_frame(frame_bytes)

        # Frame should not be torn after complete write
        assert not consumer.is_frame_torn(frame_idx)

    def test_torn_frame_detection_simulated(self, cleanup_shm, small_frame):
        """Test torn frame detection by simulating incomplete write."""
        camera_id = "test_torn_sim_001"
        width, height = small_frame.shape[1], small_frame.shape[0]

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=False
        )
        cleanup_shm.append(consumer)

        # Simulate torn frame by manually incrementing only seq_start
        slot = 1
        producer._increment_slot_seq_start(slot)
        # Don't increment seq_end - simulates interrupted write

        # Consumer should detect torn frame
        assert consumer.is_frame_torn(1)  # frame_idx 1 would use slot 1


# =============================================================================
# Unit Tests: Page Alignment
# =============================================================================

class TestPageAlignment:
    """Test page alignment for hardware efficiency."""

    def test_page_size_constant(self):
        """Test PAGE_SIZE is 4KB."""
        assert ShmRingBuffer.PAGE_SIZE == 4096

    def test_slot_alignment(self, cleanup_shm):
        """Test slot sizes are page-aligned."""
        camera_id = "test_align_001"

        # 64x64 BGR = 12,288 bytes, should align to 12,288 (3 pages)
        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=64,
            height=64,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=5,
            create=True
        )
        cleanup_shm.append(producer)

        assert producer._aligned_slot_size % ShmRingBuffer.PAGE_SIZE == 0
        assert producer._aligned_slot_size >= producer.frame_size

    def test_alignment_various_sizes(self, cleanup_shm):
        """Test alignment for various frame sizes."""
        test_cases = [
            (64, 64),    # 12,288 bytes
            (100, 100),  # 30,000 bytes
            (640, 480),  # 921,600 bytes
            (1920, 1080),  # 6,220,800 bytes
        ]

        for i, (width, height) in enumerate(test_cases):
            camera_id = f"test_align_size_{i}"
            producer = ShmRingBuffer(
                camera_id=camera_id,
                width=width,
                height=height,
                frame_format=ShmRingBuffer.FORMAT_BGR,
                slot_count=2,
                create=True
            )
            cleanup_shm.append(producer)

            # Verify page alignment
            assert producer._aligned_slot_size % ShmRingBuffer.PAGE_SIZE == 0
            # Verify aligned size >= frame size
            assert producer._aligned_slot_size >= producer.frame_size
            # Verify alignment overhead is < PAGE_SIZE
            overhead = producer._aligned_slot_size - producer.frame_size
            assert overhead < ShmRingBuffer.PAGE_SIZE


# =============================================================================
# Unit Tests: Format Conversion
# =============================================================================

class TestFormatConversion:
    """Test BGR/NV12 conversion functions."""

    def test_bgr_to_nv12_size(self, small_frame):
        """Test NV12 output size is correct."""
        nv12_bytes = bgr_to_nv12(small_frame)
        height, width = small_frame.shape[:2]
        expected_size = int(width * height * 1.5)
        assert len(nv12_bytes) == expected_size

    def test_nv12_roundtrip(self, small_frame):
        """Test BGR -> NV12 -> BGR roundtrip (lossy due to color space)."""
        height, width = small_frame.shape[:2]

        # Convert to NV12
        nv12_bytes = bgr_to_nv12(small_frame)

        # Convert back to BGR
        recovered = nv12_to_bgr(nv12_bytes, width, height)

        assert recovered.shape == small_frame.shape
        # Allow some difference due to color space conversion
        # NV12 (YUV420) is lossy, especially for random data - threshold relaxed
        diff = np.abs(small_frame.astype(float) - recovered.astype(float))
        assert diff.mean() < 60  # Average difference < 60 (lossy conversion with random data)


# =============================================================================
# Unit Tests: Default Format (BGR)
# =============================================================================

class TestDefaultFormat:
    """Test BGR is the default format."""

    def test_default_format_is_bgr(self, cleanup_shm):
        """Test default frame_format is BGR."""
        camera_id = "test_default_fmt_001"

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=64,
            height=64,
            slot_count=3,
            create=True
            # Note: frame_format not specified
        )
        cleanup_shm.append(producer)

        assert producer.frame_format == ShmRingBuffer.FORMAT_BGR

    def test_bgr_no_conversion_needed(self, cleanup_shm, small_frame):
        """Test BGR frames need no conversion."""
        camera_id = "test_bgr_direct_001"
        width, height = small_frame.shape[1], small_frame.shape[0]

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=3,
            create=False
        )
        cleanup_shm.append(consumer)

        # Write BGR frame directly
        frame_bytes = small_frame.tobytes()
        frame_idx, _ = producer.write_frame(frame_bytes)

        # Read should return exact same bytes
        read_bytes = consumer.read_frame_copy(frame_idx)
        assert read_bytes == frame_bytes

        # Reconstruct frame
        recovered = np.frombuffer(read_bytes, dtype=np.uint8).reshape(small_frame.shape)
        assert np.array_equal(recovered, small_frame)


# =============================================================================
# E2E Tests: Producer-Consumer
# =============================================================================

class TestE2EProducerConsumer:
    """End-to-end tests with producer and consumer."""

    def test_single_producer_single_consumer(self, cleanup_shm, small_frame):
        """Test basic producer-consumer flow."""
        camera_id = "test_e2e_single_001"
        width, height = small_frame.shape[1], small_frame.shape[0]
        num_frames = 20

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=10,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=10,
            create=False
        )
        cleanup_shm.append(consumer)

        # Produce and consume frames
        for i in range(num_frames):
            # Modify frame slightly for each iteration
            frame = small_frame.copy()
            frame[0, 0, 0] = i % 256

            frame_bytes = frame.tobytes()
            frame_idx, _ = producer.write_frame(frame_bytes)

            # Consumer reads
            read_bytes = consumer.read_frame_copy(frame_idx)
            assert read_bytes is not None
            assert read_bytes == frame_bytes

    def test_multiple_consumers(self, cleanup_shm, small_frame):
        """Test one producer, multiple consumers."""
        camera_id = "test_e2e_multi_001"
        width, height = small_frame.shape[1], small_frame.shape[0]
        num_consumers = 3

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=10,
            create=True
        )
        cleanup_shm.append(producer)

        consumers = []
        for _ in range(num_consumers):
            consumer = ShmRingBuffer(
                camera_id=camera_id,
                width=width,
                height=height,
                frame_format=ShmRingBuffer.FORMAT_BGR,
                slot_count=10,
                create=False
            )
            consumers.append(consumer)
            cleanup_shm.append(consumer)

        # Write frame
        frame_bytes = small_frame.tobytes()
        frame_idx, _ = producer.write_frame(frame_bytes)

        # All consumers should read same frame
        for consumer in consumers:
            read_bytes = consumer.read_frame_copy(frame_idx)
            assert read_bytes == frame_bytes

    def test_concurrent_producer_consumer(self, cleanup_shm, small_frame):
        """Test concurrent producer and consumer in threads."""
        camera_id = "test_e2e_concurrent_001"
        width, height = small_frame.shape[1], small_frame.shape[0]
        num_frames = 100
        slot_count = 30

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=slot_count,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=slot_count,
            create=False
        )
        cleanup_shm.append(consumer)

        produced_frames = []
        consumed_frames = []
        errors = []

        def producer_thread():
            for i in range(num_frames):
                frame = small_frame.copy()
                frame[0, 0, 0] = i % 256
                frame_bytes = frame.tobytes()
                frame_idx, _ = producer.write_frame(frame_bytes)
                produced_frames.append((frame_idx, frame_bytes))
                time.sleep(0.001)  # Simulate 1ms frame time

        def consumer_thread():
            last_idx = 0
            attempts = 0
            max_attempts = num_frames * 10

            while len(consumed_frames) < num_frames and attempts < max_attempts:
                attempts += 1
                current_idx = consumer.get_current_frame_idx()

                if current_idx > last_idx:
                    # Try to read latest frame
                    frame_bytes = consumer.read_frame_copy(current_idx)
                    if frame_bytes is not None:
                        consumed_frames.append((current_idx, frame_bytes))
                        last_idx = current_idx
                    # Frame might be torn or overwritten - that's OK
                time.sleep(0.0005)

        # Run threads
        p_thread = threading.Thread(target=producer_thread)
        c_thread = threading.Thread(target=consumer_thread)

        p_thread.start()
        c_thread.start()

        p_thread.join()
        c_thread.join(timeout=5)

        # Verify we got some frames (not all due to timing)
        assert len(consumed_frames) > 0
        assert len(errors) == 0

        # Verify consumed frames match produced frames
        produced_dict = {idx: data for idx, data in produced_frames}
        for idx, data in consumed_frames:
            if idx in produced_dict:
                assert data == produced_dict[idx]


# =============================================================================
# E2E Tests: Multiprocess
# =============================================================================

def _producer_process(camera_id, width, height, num_frames, ready_event, done_event):
    """Producer process for multiprocess test."""
    producer = ShmRingBuffer(
        camera_id=camera_id,
        width=width,
        height=height,
        frame_format=ShmRingBuffer.FORMAT_BGR,
        slot_count=30,
        create=True
    )

    ready_event.set()  # Signal ready

    for i in range(num_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[0, 0, 0] = i % 256
        producer.write_frame(frame.tobytes())
        time.sleep(0.01)

    done_event.set()
    time.sleep(0.1)  # Wait for consumer to finish
    producer.close()


def _consumer_process(camera_id, width, height, ready_event, done_event, result_queue):
    """Consumer process for multiprocess test."""
    ready_event.wait(timeout=5)  # Wait for producer

    consumer = ShmRingBuffer(
        camera_id=camera_id,
        width=width,
        height=height,
        frame_format=ShmRingBuffer.FORMAT_BGR,
        slot_count=30,
        create=False
    )

    frames_read = 0
    torn_frames = 0
    last_idx = 0

    while not done_event.is_set() or consumer.get_current_frame_idx() > last_idx:
        current_idx = consumer.get_current_frame_idx()
        if current_idx > last_idx:
            data = consumer.read_frame_copy(current_idx)
            if data is not None:
                frames_read += 1
            else:
                torn_frames += 1
            last_idx = current_idx
        time.sleep(0.005)

    consumer.close()
    result_queue.put({"frames_read": frames_read, "torn_frames": torn_frames})


class TestE2EMultiprocess:
    """End-to-end tests with separate processes."""

    def test_multiprocess_producer_consumer(self):
        """Test producer and consumer in separate processes."""
        camera_id = "test_e2e_mp_001"
        width, height = 64, 64
        num_frames = 50

        ready_event = multiprocessing.Event()
        done_event = multiprocessing.Event()
        result_queue = multiprocessing.Queue()

        producer_proc = multiprocessing.Process(
            target=_producer_process,
            args=(camera_id, width, height, num_frames, ready_event, done_event)
        )
        consumer_proc = multiprocessing.Process(
            target=_consumer_process,
            args=(camera_id, width, height, ready_event, done_event, result_queue)
        )

        try:
            producer_proc.start()
            consumer_proc.start()

            producer_proc.join(timeout=10)
            consumer_proc.join(timeout=5)

            assert not producer_proc.is_alive()
            assert not consumer_proc.is_alive()

            # Get results
            result = result_queue.get(timeout=1)
            print(f"Frames read: {result['frames_read']}, Torn: {result['torn_frames']}")

            # Should have read some frames
            assert result["frames_read"] > 0

        finally:
            if producer_proc.is_alive():
                producer_proc.terminate()
            if consumer_proc.is_alive():
                consumer_proc.terminate()

            # Cleanup SHM
            try:
                shm = shared_memory.SharedMemory(name=f"shm_cam_{camera_id}", create=False)
                shm.close()
                shm.unlink()
            except Exception:
                pass


# =============================================================================
# Performance Tests
# =============================================================================

class TestPerformance:
    """Performance benchmarks."""

    def test_write_throughput(self, cleanup_shm):
        """Benchmark write throughput."""
        camera_id = "test_perf_write_001"
        width, height = 640, 480
        num_frames = 100

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=30,
            create=True
        )
        cleanup_shm.append(producer)

        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        frame_bytes = frame.tobytes()

        start = time.time()
        for _ in range(num_frames):
            producer.write_frame(frame_bytes)
        elapsed = time.time() - start

        fps = num_frames / elapsed
        print(f"\nWrite throughput: {fps:.1f} FPS ({elapsed*1000/num_frames:.2f}ms/frame)")
        assert fps > 100  # Should be > 100 FPS for 640x480

    def test_read_throughput(self, cleanup_shm):
        """Benchmark read throughput."""
        camera_id = "test_perf_read_001"
        width, height = 640, 480
        num_frames = 100

        producer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=30,
            create=True
        )
        cleanup_shm.append(producer)

        consumer = ShmRingBuffer(
            camera_id=camera_id,
            width=width,
            height=height,
            frame_format=ShmRingBuffer.FORMAT_BGR,
            slot_count=30,
            create=False
        )
        cleanup_shm.append(consumer)

        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        frame_bytes = frame.tobytes()

        # Write frames first
        frame_indices = []
        for _ in range(num_frames):
            idx, _ = producer.write_frame(frame_bytes)
            frame_indices.append(idx)

        # Benchmark reads
        start = time.time()
        for idx in frame_indices[-30:]:  # Read last 30 (still valid)
            consumer.read_frame_copy(idx)
        elapsed = time.time() - start

        fps = 30 / elapsed
        print(f"\nRead throughput: {fps:.1f} FPS ({elapsed*1000/30:.2f}ms/frame)")
        assert fps > 100  # Should be > 100 FPS


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

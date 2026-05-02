"""Minimal example to test filehandle access with new factory pattern."""

from roastcoffea.decorator import track_metrics
from roastcoffea.instrumentation import track_bytes


# Mock classes simulating the new coffea structure
class MockFileSource:
    """Mock FSSpecSource from uproot."""

    def __init__(self, start_bytes=1000):
        self._bytes = start_bytes

    @property
    def num_requested_bytes(self):
        return self._bytes

    def simulate_read(self, bytes_to_read):
        """Simulate reading bytes from file."""
        self._bytes += bytes_to_read


class MockFile:
    """Mock file object containing source."""

    def __init__(self, source):
        self.source = source


class MockFileHandle:
    """Mock filehandle object."""

    def __init__(self, source):
        self.file = MockFile(source)


class MockEventsFactory:
    """Mock events factory that holds the filehandle (new coffea pattern)."""

    def __init__(self, filehandle):
        self.filehandle = filehandle


class MockEvents:
    """Mock events object with filehandle in events factory."""

    def __init__(self, num_events=100, filename="data.root", start=0, stop=100):
        source = MockFileSource(start_bytes=5000)
        filehandle = MockFileHandle(source)
        self.metadata = {
            "dataset": "test_dataset",
            "filename": filename,
            "entrystart": start,
            "entrystop": stop,
            "uuid": "test-uuid",
        }
        self.attrs = {
            "@events_factory": MockEventsFactory(filehandle),
        }
        self._num_events = num_events

    def __len__(self):
        return self._num_events


class TestProcessor:
    """Test processor with metrics collection enabled."""

    _roastcoffea_collect_metrics = True

    @track_metrics
    def process(self, events):
        # Get factory to simulate reads
        factory = events.attrs.get("@events_factory")

        # Simulate reading data during processing
        print("Simulating 2500 bytes read...")
        factory.filehandle.file.source.simulate_read(2500)

        # Use track_bytes for fine-grained tracking
        print("Tracking 'jet_loading' section (1000 bytes)...")
        with track_bytes(self, events, "jet_loading"):
            factory.filehandle.file.source.simulate_read(1000)

        print("Tracking 'muon_loading' section (500 bytes)...")
        with track_bytes(self, events, "muon_loading"):
            factory.filehandle.file.source.simulate_read(500)

        return {"sum": len(events)}


def main():
    print("=" * 60)
    print("Testing filehandle access with new factory pattern")
    print("=" * 60)

    # Create processor and events
    processor = TestProcessor()
    events = MockEvents(num_events=1000, filename="test.root", start=0, stop=1000)

    # Verify the factory structure
    print("\n1. Checking events structure:")
    print(f"   events.attrs keys: {list(events.attrs.keys())}")
    factory = events.attrs.get("@events_factory")
    print(f"   Factory exists: {factory is not None}")
    print(f"   Factory has filehandle: {hasattr(factory, 'filehandle')}")
    if factory and hasattr(factory, "filehandle"):
        fh = factory.filehandle
        print(f"   Filehandle has .file: {hasattr(fh, 'file')}")
        if hasattr(fh, "file"):
            print(f"   File has .source: {hasattr(fh.file, 'source')}")
            if hasattr(fh.file, "source"):
                print(
                    f"   Source has num_requested_bytes: {hasattr(fh.file.source, 'num_requested_bytes')}"
                )
                print(
                    f"   Initial bytes: {fh.file.source.num_requested_bytes}"
                )

    # Process the events
    print("\n2. Processing events...")
    result = processor.process(events)

    # Check if metrics were captured
    print("\n3. Checking results:")
    print(f"   Result keys: {list(result.keys())}")

    if "__roastcoffea_metrics__" in result:
        chunk_metrics = result["__roastcoffea_metrics__"]
        print(f"   Number of chunk metrics: {len(chunk_metrics)}")

        chunk = chunk_metrics[0]
        print("\n4. Chunk metrics:")
        print(f"   bytes_read: {chunk.get('bytes_read')} (expected: 4000)")
        print(f"   num_events: {chunk.get('num_events')} (expected: 1000)")
        print(f"   duration: {chunk.get('duration'):.4f}s")

        print("\n5. Fine-grained bytes tracking:")
        bytes_sections = chunk.get("bytes", {})
        print(f"   Sections tracked: {list(bytes_sections.keys())}")
        for section, bytes_val in bytes_sections.items():
            print(f"   - {section}: {bytes_val} bytes")

        # Verify expected values
        print("\n6. Verification:")
        total_bytes = chunk.get("bytes_read", 0)
        jet_bytes = bytes_sections.get("jet_loading", 0)
        muon_bytes = bytes_sections.get("muon_loading", 0)

        all_pass = True
        if total_bytes == 4000:
            print("   [PASS] Total bytes_read = 4000")
        else:
            print(f"   [FAIL] Total bytes_read = {total_bytes}, expected 4000")
            all_pass = False

        if jet_bytes == 1000:
            print("   [PASS] jet_loading = 1000")
        else:
            print(f"   [FAIL] jet_loading = {jet_bytes}, expected 1000")
            all_pass = False

        if muon_bytes == 500:
            print("   [PASS] muon_loading = 500")
        else:
            print(f"   [FAIL] muon_loading = {muon_bytes}, expected 500")
            all_pass = False

        print("\n" + "=" * 60)
        if all_pass:
            print("SUCCESS: All byte tracking tests passed!")
        else:
            print("FAILURE: Some byte tracking tests failed!")
        print("=" * 60)
    else:
        print("   [FAIL] No __roastcoffea_metrics__ in result!")


if __name__ == "__main__":
    main()

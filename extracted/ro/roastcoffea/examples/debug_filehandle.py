"""Debug script to inspect events structure from coffea."""

from __future__ import annotations

from coffea import processor
from dask.distributed import Client, LocalCluster


class DebugProcessor(processor.ProcessorABC):
    """Processor to debug events structure."""

    def process(self, events):
        """Inspect events structure."""
        print("\n" + "=" * 60)
        print("EVENTS OBJECT INSPECTION")
        print("=" * 60)

        # Check metadata
        print("\n1. events.metadata:")
        for key, value in events.metadata.items():
            val_type = type(value).__name__
            val_repr = repr(value)[:100] if len(repr(value)) > 100 else repr(value)
            print(f"   {key}: ({val_type}) {val_repr}")

        # Check attrs
        print("\n2. events.attrs:")
        if hasattr(events, "attrs"):
            for key, value in events.attrs.items():
                val_type = type(value).__name__
                print(f"   {key}: ({val_type})")
                if key == "@events_factory":
                    factory = value
                    print(f"      Factory attributes: {[a for a in dir(factory) if not a.startswith('_')]}")
                    if hasattr(factory, "file_handle"):
                        fh = factory.file_handle
                        print(f"      file_handle: {fh}")
                        print(f"      file_handle type: {type(fh)}")
                        if fh is not None:
                            print(f"      file_handle attrs: {[a for a in dir(fh) if not a.startswith('_')]}")
                            if hasattr(fh, "file"):
                                print(f"      file_handle.file: {fh.file}")
                                if hasattr(fh.file, "source"):
                                    src = fh.file.source
                                    print(f"      source: {src}")
                                    if hasattr(src, "num_requested_bytes"):
                                        print(
                                            f"      num_requested_bytes: {src.num_requested_bytes}"
                                        )
                    else:
                        print("      file_handle attribute not found!")
        else:
            print("   events has no 'attrs' attribute!")

        # Check other attributes that might have filehandle
        print("\n3. Looking for filehandle in other locations:")
        for attr in ["_events_factory", "factory", "_factory", "behavior"]:
            if hasattr(events, attr):
                val = getattr(events, attr)
                print(f"   events.{attr}: {type(val).__name__}")

        print("\n" + "=" * 60)

        return {"nevents": len(events)}

    def postprocess(self, accumulator):
        return accumulator


def main():
    """Run debug inspection."""
    fileset = {
        "test": {
            "files": {
                "root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraph-pythiaMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v1/270000/22BAB5D2-9E3F-E440-AB30-AE6DBFDF6C83.root": "Events",
            }
        }
    }

    cluster = LocalCluster(n_workers=1, threads_per_worker=1, processes=False)
    client = Client(cluster)

    print("Running debug processor to inspect events structure...")
    print("(Using processes=False to see print output)")

    proc = DebugProcessor()
    executor = processor.DaskExecutor(client=client)
    runner = processor.Runner(executor=executor, chunksize=10000, maxchunks=1)

    output, report = runner(
        fileset,
        treename="Events",
        processor_instance=proc,
    )

    print("\nDone!")

    client.close()
    cluster.close()


if __name__ == "__main__":
    main()

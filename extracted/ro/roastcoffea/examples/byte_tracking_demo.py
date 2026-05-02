"""Demonstration of byte and branch access tracking.

This example shows:
1. Using @track_metrics decorator to automatically track bytes read per chunk
2. Per-chunk branch access metrics (accessed_branches, accessed_bytes, percentages)
3. Fine-grained byte tracking with track_bytes() context manager
4. Generating throughput and data access plots

Requires: coffea >= 2025.12.0
"""

from __future__ import annotations

from pathlib import Path

from coffea import processor
from coffea.nanoevents import NanoAODSchema
from dask.distributed import Client, LocalCluster

from roastcoffea import MetricsCollector, track_bytes, track_metrics, track_time
from roastcoffea.visualization.plots import (
    plot_branch_access_per_chunk,
    plot_bytes_accessed_per_chunk,
    plot_data_access_percentage,
    plot_throughput_timeline,
)

# Suppress NanoAOD cross-reference warnings
NanoAODSchema.warn_missing_crossrefs = False


class ByteTrackingProcessor(processor.ProcessorABC):
    """Demo processor with variable branch access per chunk.

    Different chunks access different branches to demonstrate
    per-chunk branch tracking granularity.
    """

    @track_metrics
    def process(self, events):
        """Process events with varying branch access patterns."""
        entry_start = events.metadata.get("entrystart", 0)

        # Always access Jets
        with track_bytes(self, events, "jet_loading"):
            with track_time(self, "jet_selection"):
                jets = events.Jet
                selected_jets = jets[jets.pt > 30]

        result = {"nevents": len(events), "njets": len(selected_jets)}

        # Vary branch access based on chunk position
        if entry_start % 10000 < 5000:
            # First half of chunks: access Muons
            with track_bytes(self, events, "muon_loading"):
                with track_time(self, "muon_selection"):
                    muons = events.Muon
                    result["nmuons"] = len(muons[muons.pt > 20])
        else:
            # Second half: access Electrons and Photons
            with track_bytes(self, events, "electron_loading"):
                with track_time(self, "electron_selection"):
                    electrons = events.Electron
                    result["nelectrons"] = len(electrons[electrons.pt > 25])

            with track_bytes(self, events, "photon_loading"):
                with track_time(self, "photon_selection"):
                    photons = events.Photon
                    result["nphotons"] = len(photons[photons.pt > 30])

        return result

    def postprocess(self, accumulator):
        return accumulator


def main():
    """Run demo workflow with byte tracking."""
    # Example fileset
    fileset = {
        "ttbar": {
            "files": {
                "root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraph-pythiaMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v1/270000/22BAB5D2-9E3F-E440-AB30-AE6DBFDF6C83.root": "Events",
            }
        }
    }

    # Setup Dask cluster
    cluster = LocalCluster(n_workers=4, threads_per_worker=1, processes=True)
    client = Client(cluster)
    print(f"Dask Dashboard: {client.dashboard_link}\n")

    # Setup output directory
    output_dir = Path("benchmark_results")
    output_dir.mkdir(exist_ok=True)

    # Create processor and run with metrics collection
    proc = ByteTrackingProcessor()

    with MetricsCollector(client, processor_instance=proc) as collector:
        executor = processor.DaskExecutor(client=client)
        runner = processor.Runner(executor=executor, savemetrics=True, chunksize=5000)

        output, report = runner(
            fileset,
            treename="Events",
            processor_instance=proc,
        )

        collector.extract_metrics_from_output(output)
        collector.set_coffea_report(report)

    metrics = collector.metrics

    # Print summary
    print("=" * 60)
    print("METRICS SUMMARY")
    print("=" * 60)
    print(f"Total events: {metrics.get('total_events', 0):,}")
    print(f"Total bytes read: {metrics.get('total_bytes_read', 0) / 1e6:.2f} MB")
    print(f"Elapsed time: {metrics.get('elapsed_time_seconds', 0):.2f}s")
    print()

    # Show per-chunk branch access metrics (new feature)
    if "raw_chunk_metrics" in metrics and metrics["raw_chunk_metrics"]:
        print("PER-CHUNK BRANCH ACCESS METRICS")
        print("-" * 80)
        print(
            f"{'Chunk':<30} {'Branches':<10} {'Compressed':<14} {'Uncompressed':<14}"
        )
        print("-" * 80)

        for chunk in metrics["raw_chunk_metrics"][:5]:  # Show first 5 chunks
            filename = Path(chunk.get("file", "unknown")).name[:25]
            entry_start = chunk.get("entry_start", 0)
            entry_stop = chunk.get("entry_stop", 0)
            chunk_name = f"{filename}[{entry_start}:{entry_stop}]"

            num_branches = chunk.get("num_branches_accessed", 0)
            compressed_mb = chunk.get("accessed_bytes", 0) / 1e6
            uncompressed_mb = chunk.get("accessed_uncompressed_bytes", 0) / 1e6

            print(
                f"{chunk_name:<30} {num_branches:<10} {compressed_mb:<14.2f} {uncompressed_mb:<14.2f}"
            )

        # Show accessed branches from first chunk
        first_chunk = metrics["raw_chunk_metrics"][0]
        accessed = first_chunk.get("accessed_branches", [])
        if accessed:
            print(f"\nAccessed branches: {', '.join(sorted(accessed)[:10])}")
            if len(accessed) > 10:
                print(f"  ... and {len(accessed) - 10} more")
        print()

    # Show aggregated branch coverage metrics (merged at top level)
    if "total_branches_read" in metrics:
        print("BRANCH COVERAGE SUMMARY")
        print("-" * 60)
        print(f"Unique branches accessed: {metrics.get('total_branches_read', 0)}")
        print(f"Avg branches read %: {metrics.get('avg_branches_read_percent', 0):.1f}%")
        print(f"Avg bytes read %: {metrics.get('avg_bytes_read_percent', 0):.1f}%")
        print()

    # Generate plots
    if "chunk_info" in metrics and metrics["chunk_info"]:
        print("Generating throughput timeline plot...")
        plot_throughput_timeline(
            chunk_info=metrics["chunk_info"],
            tracking_data=metrics.get("tracking_data"),
            output_path=output_dir / "throughput_timeline.png",
        )
        print(f"  Saved: {output_dir}/throughput_timeline.png")

    if metrics.get("bytes_read_percent_per_file"):
        print("Generating data access percentage plot...")
        plot_data_access_percentage(
            metrics=metrics,
            output_path=output_dir / "data_access_percentage.png",
        )
        print(f"  Saved: {output_dir}/data_access_percentage.png")

    # Generate per-chunk plots
    if "raw_chunk_metrics" in metrics and metrics["raw_chunk_metrics"]:
        print("Generating per-chunk branch access plot...")
        plot_branch_access_per_chunk(
            chunk_metrics=metrics["raw_chunk_metrics"],
            output_path=output_dir / "branch_access_per_chunk.png",
        )
        print(f"  Saved: {output_dir}/branch_access_per_chunk.png")

        print("Generating per-chunk bytes accessed plot...")
        plot_bytes_accessed_per_chunk(
            chunk_metrics=metrics["raw_chunk_metrics"],
            output_path=output_dir / "bytes_accessed_per_chunk.png",
        )
        print(f"  Saved: {output_dir}/bytes_accessed_per_chunk.png")

    print()
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)

    client.close()
    cluster.close()


if __name__ == "__main__":
    main()

/* Capacity benchmark runner.
 * Uses binary search to efficiently find the maximum concurrent runs target in (0, rampEnd].
 * Stops when the optimal target is found and reports max successful target + avg execution latency.
 *
 * Supports running multiple workloads sequentially for a single cluster.
 * Set WORKLOAD_NAMES as a comma-separated list (e.g., "parallel-small,parallel-tiny,sequential-small")
 * or use WORKLOAD_NAME for a single workload (backwards compatible).
 * Optionally set BENCHMARK_PROFILE (e.g., "etsy", "metaview") to force a profile globally.
 */

import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { clean } from './clean.js';
import { get_profile } from './benchmark-runners/dist/benchmark_profiles.js';

// Minimum success rate to consider a target successful (allows some failures)
const MIN_SUCCESS_RATE = 99;

// Cooldown period to let the cluster stabilize
const CLUSTER_COOLDOWN_SECONDS_AFTER_TEST = 60; // 60s to let remaining runs timeout
const CLUSTER_COOLDOWN_SECONDS_AFTER_WORKLOAD = 240; // 4 minutes because there are runs from prev tests still pending

// Configuration mappings
const clusterNameToSettings = {

  // Python runtime multi-node scaling benchmarks
  'py-1-node': {
    url: 'https://cap-bench-py-1-node-77fbc06f80695b81af35a15f6270409e.staging.langgraph.app',
    rampEndMultiplier: 1,
  },
  'py-7-node': {
    url: 'https://cap-bench-py-7-node-5f471cdb8a725e0bbb076cc9fb32b76d.staging.langgraph.app',
    rampEndMultiplier: 5,
  },
  'py-20-node': {
    url: 'https://cap-bench-py-20-node-0970dd3e458059e488db99d48c69ca69.staging.langgraph.app',
    rampEndMultiplier: 10,
  },
  // Distributed runtime multi-node scaling benchmarks
  'dr-1-node': {
    url: 'https://cap-bench-dr-1-node-49e9ad9e573e55f38c51a11626e72e89.staging.langgraph.app',
    rampEndMultiplier: 1,
  },
  'localhost': {
    url: 'http://localhost:9123',
    rampEndMultiplier: 1.8,
  },
  'dr-7-node': {
    url: 'https://cap-bench-dr-7-node-fbf64b46fc9b57239764478187abe534.staging.langgraph.app',
    rampEndMultiplier: 5,
  },
  'dr-20-node': {
    url: 'https://cap-bench-dr-20-node-7cea036a01a25a9caec0be0b873f9b0a.staging.langgraph.app',
    rampEndMultiplier: 10,
  },
};

function profileWorkload(profileName, overrides = {}) {
  const resolved = get_profile({ BENCHMARK_PROFILE: profileName });
  return {
    benchmarkProfile: profileName,
    runMode: resolved.runMode,
    resumable: resolved.resumable,
    delay: resolved.context.delay,
    expand: resolved.context.expand,
    steps: resolved.context.steps,
    rampEndBase: resolved.capacity.rampEndBase,
    runExecutionTimeoutSeconds: resolved.capacity.runExecutionTimeoutSeconds,
    ...overrides,
  };
}

const workloadNameToAgentParams = {
  'stateless-parallel-small': profileWorkload('stateless-parallel-small'),
  'stateless-parallel-medium': profileWorkload('stateless-parallel-medium'),
  'parallel-small': profileWorkload('parallel-small'),
  'parallel-medium': profileWorkload('parallel-medium'),
  'default': profileWorkload('default'),
  'streaming-long': profileWorkload('streaming-long'),
};

// Environment variables
const CLUSTER_NAME = process.env.CLUSTER_NAME;
// Support both WORKLOAD_NAMES (comma-separated) and WORKLOAD_NAME (single, backwards compatible)
const WORKLOAD_NAMES = process.env.WORKLOAD_NAMES
  ? process.env.WORKLOAD_NAMES.split(',').map(w => w.trim()).filter(w => w)
  : process.env.WORKLOAD_NAME
    ? [process.env.WORKLOAD_NAME]
    : [];
// Run mode: 'stateless' (default) or 'stateful' (creates thread first)
const RUN_MODE = process.env.RUN_MODE || 'stateless';
const BENCHMARK_PROFILE = process.env.BENCHMARK_PROFILE;

// Validate inputs
validateInputs();

const clusterSettings = clusterNameToSettings[CLUSTER_NAME];

console.log(`\n=== Cluster Configuration ===`);
console.log(`Cluster: ${CLUSTER_NAME} (rampEndMultiplier: ${clusterSettings.rampEndMultiplier}x)`);
console.log(`URL: ${clusterSettings.url}`);
console.log(`Run mode: ${RUN_MODE}`);
console.log(`Workloads to run: ${WORKLOAD_NAMES.join(', ')}`);

// Helper functions (in order of usage)

function validateInputs() {
  if (!CLUSTER_NAME || !clusterNameToSettings[CLUSTER_NAME]) {
    throw new Error(`Invalid CLUSTER_NAME: "${CLUSTER_NAME}". Must be one of: ${Object.keys(clusterNameToSettings).join(', ')}`);
  }
  if (WORKLOAD_NAMES.length === 0) {
    throw new Error(`No workloads specified. Set WORKLOAD_NAMES (comma-separated) or WORKLOAD_NAME. Valid workloads: ${Object.keys(workloadNameToAgentParams).join(', ')}`);
  }
  for (const workloadName of WORKLOAD_NAMES) {
    if (!workloadNameToAgentParams[workloadName]) {
      throw new Error(`Invalid workload: "${workloadName}". Must be one of: ${Object.keys(workloadNameToAgentParams).join(', ')}`);
    }
  }
}

function runK6(target, workloadName) {
  const baseUrl = clusterNameToSettings[CLUSTER_NAME].url;
  const agentParams = workloadNameToAgentParams[workloadName];
  const resolved = get_profile({
    ...process.env,
    BENCHMARK_PROFILE: agentParams.benchmarkProfile || BENCHMARK_PROFILE,
    RUN_MODE: agentParams.runMode || RUN_MODE,
    STREAM_RESUMABLE: agentParams.resumable != null ? String(agentParams.resumable) : process.env.STREAM_RESUMABLE,
    DELAY: agentParams.delay != null ? String(agentParams.delay) : process.env.DELAY,
    EXPAND: agentParams.expand != null ? String(agentParams.expand) : process.env.EXPAND,
    STEPS: agentParams.steps != null ? String(agentParams.steps) : process.env.STEPS,
    CHECKPOINT_SIZE: process.env.CHECKPOINT_SIZE,
    LLM_ENABLED: process.env.LLM_ENABLED,
    STREAM_SIZE: process.env.STREAM_SIZE,
    CHUNK_SIZE: process.env.CHUNK_SIZE,
    BURST_MODE: process.env.BURST_MODE,
    BURST_PROBABILITY: process.env.BURST_PROBABILITY,
    BURST_SIZE: process.env.BURST_SIZE,
  });

  const envVars = {
    ...process.env,
    BASE_URL: baseUrl,
    TARGET: String(target),
    BENCHMARK_PROFILE: resolved.name,
    RUN_MODE: resolved.runMode,
    DELAY: String(resolved.context.delay),
    EXPAND: String(resolved.context.expand),
    STEPS: String(resolved.context.steps),
    CHECKPOINT_SIZE: String(resolved.context.checkpoint_size),
    LLM_ENABLED: String(resolved.context.llm_enabled),
    STREAM_SIZE: String(resolved.context.stream_size),
    CHUNK_SIZE: String(resolved.context.chunk_size),
    BURST_MODE: String(resolved.context.burst_mode),
    BURST_PROBABILITY: String(resolved.context.burst_probability),
    BURST_SIZE: String(resolved.context.burst_size),
    STREAM_RESUMABLE: String(resolved.resumable),
    RUN_EXECUTION_TIMEOUT_SECONDS: String(agentParams.runExecutionTimeoutSeconds),
  };
  if (agentParams.benchmarkType) {
    envVars.BENCHMARK_TYPE = agentParams.benchmarkType;
  }

  let result;
  try {
    result = execFileSync('k6', ['run', 'capacity_k6.js'], {
      cwd: process.cwd(),
      env: envVars,
      encoding: 'utf-8',
      stdio: ['inherit', 'pipe', 'inherit'],  // Inherit stdin and stderr, pipe stdout
    });
  } catch (error) {
    console.log(`\n⚠️  K6 failed at target=${target}`);
    console.error(error);
    return null;
  }

  // Print the output to console for visibility
  console.log(result);

  // Find the JSON line from handleSummary output
  const lines = result.split('\n');
  const jsonLine = lines.find(line => {
    const trimmed = line.trim();
    return trimmed.startsWith('{') && trimmed.includes('"target"');
  });

  if (!jsonLine) {
    throw new Error(`No JSON output found in k6 results. Output: ${result.substring(0, 500)}`);
  }

  return { stdout: jsonLine.trim() };
}

function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

/**
 * Run benchmark for a single workload using binary search.
 * Returns the result object or null if no successful runs.
 */
async function runWorkloadBenchmark(workloadName) {
  const workloadConfig = workloadNameToAgentParams[workloadName];
  const resolved = get_profile({
    ...process.env,
    BENCHMARK_PROFILE: workloadConfig.benchmarkProfile || BENCHMARK_PROFILE,
    RUN_MODE: workloadConfig.runMode || RUN_MODE,
    STREAM_RESUMABLE: workloadConfig.resumable != null ? String(workloadConfig.resumable) : process.env.STREAM_RESUMABLE,
    DELAY: workloadConfig.delay != null ? String(workloadConfig.delay) : process.env.DELAY,
    EXPAND: workloadConfig.expand != null ? String(workloadConfig.expand) : process.env.EXPAND,
    STEPS: workloadConfig.steps != null ? String(workloadConfig.steps) : process.env.STEPS,
  });
  const rampEnd = workloadConfig.rampEndBase * clusterSettings.rampEndMultiplier;

  console.log(`\n${'='.repeat(60)}`);
  console.log(`=== Workload: ${workloadName} ===`);
  console.log(`${'='.repeat(60)}`);
  console.log(`  - Search Range: (0, ${rampEnd}] (${workloadConfig.rampEndBase} × ${clusterSettings.rampEndMultiplier}) (using binary search)`);
  console.log(`  - Timeout: ${workloadConfig.runExecutionTimeoutSeconds}s`);
  console.log(`  - Expand: ${resolved.context.expand}`);
  console.log(`  - Steps: ${resolved.context.steps}`);
  console.log(`  - Delay: ${resolved.context.delay}s`);
  console.log(`  - LLM Enabled: ${resolved.context.llm_enabled}`);
  console.log(`  - Stream Size: ${resolved.context.stream_size} bytes`);
  console.log(`  - Chunk Size: ${resolved.context.chunk_size} bytes`);
  console.log(`  - Burst Mode: ${resolved.context.burst_mode}`);
  console.log(`  - Burst Probability: ${resolved.context.burst_probability}`);
  console.log(`  - Burst Size: ${resolved.context.burst_size} bytes`);
  console.log(`  - Stream Resumable: ${resolved.resumable}`);
  if (workloadConfig.runMode) {
    console.log(`  - Run Mode: ${workloadConfig.runMode} (workload-specific)`);
  }
  if (workloadConfig.benchmarkType) {
    console.log(`  - Benchmark Type: ${workloadConfig.benchmarkType}`);
  }
  console.log(`  - Benchmark Profile: ${resolved.name}`);

  // Clean up threads/assistants before stateful workloads
  const runMode = workloadConfig.runMode || RUN_MODE;
  if (runMode === 'stateful') {
    console.log(`\n  Cleaning up threads and assistants before stateful workload...`);
    await clean(clusterSettings.url, process.env.LANGSMITH_API_KEY);
    console.log(`  Cleanup completed.`);
  }

  let low = 0;
  let high = rampEnd;
  let lastSuccessfulTarget = null;
  let lastSuccessfulLatency = null;
  let lastSuccessfulP95Latency = null;
  let lastSuccessfulP99Latency = null;
  let testCount = 0;

  // Binary search to find the maximum successful target
  while (low < high) {
    // Calculate mid point (round up to prefer higher values)
    const currentTarget = Math.ceil((low + high) / 2);
    testCount++;

    console.log(`\n=== Test #${testCount}: target=${currentTarget} [range: (${low}, ${high}]] ===`);

    // Run K6
    console.log(`Running k6 with target=${currentTarget}...`);
    const result = runK6(currentTarget, workloadName);

    // Check if k6 command failed (capacity limit reached)
    if (result === null) {
      console.log(`❌ Failed at target ${currentTarget} (k6 error)`);
      high = currentTarget - 1;
      continue;
    }

    // Parse JSON output
    const metrics = JSON.parse(result.stdout);

    // Check if succeeded (allow some failures, but must meet minimum success rate)
    if (metrics.successRate < MIN_SUCCESS_RATE || !metrics.avgExecutionLatencySeconds) {
      console.log(`❌ Failed at target ${currentTarget} (success rate: ${metrics.successRate.toFixed(2)}%, avg latency: ${metrics.avgExecutionLatencySeconds || 'N/A'})`);
      // Search in lower half: (low, currentTarget - 1]
      high = currentTarget - 1;
      // if it fails, wait for the cluster to stabilize
      await sleep(CLUSTER_COOLDOWN_SECONDS_AFTER_TEST);
    } else {
      // Success! Record it and search higher
      lastSuccessfulTarget = currentTarget;
      lastSuccessfulLatency = metrics.avgExecutionLatencySeconds;
      lastSuccessfulP95Latency = metrics.p95ExecutionLatencySeconds;
      lastSuccessfulP99Latency = metrics.p99ExecutionLatencySeconds;
      console.log(`✅ Success: avg: ${metrics.avgExecutionLatencySeconds.toFixed(3)}s, p95: ${metrics.p95ExecutionLatencySeconds?.toFixed(3) || 'N/A'}s, p99: ${metrics.p99ExecutionLatencySeconds?.toFixed(3) || 'N/A'}s (${metrics.successRate.toFixed(2)}% success rate)`);
      // Search in upper half: (currentTarget, high]
      low = currentTarget;
    }

    // Check if we're done (when low and high are adjacent or equal)
    if (high - low <= 0) {
      break;
    }
  }

  // Validate results
  if (lastSuccessfulTarget === null) {
    console.log(`⚠️  No successful runs for workload ${workloadName} - capacity may be too low or search range is too high`);
    return null;
  }

  console.log(`\n🎯 Binary search complete after ${testCount} tests`);
  console.log(`   Max successful target: ${lastSuccessfulTarget}`);

  const result = {
    maxSuccessfulTarget: lastSuccessfulTarget,
    avgExecutionLatencySeconds: Number(lastSuccessfulLatency.toFixed(3)),
  };
  if (lastSuccessfulP95Latency != null) {
    result.p95ExecutionLatencySeconds = Number(lastSuccessfulP95Latency.toFixed(3));
  }
  if (lastSuccessfulP99Latency != null) {
    result.p99ExecutionLatencySeconds = Number(lastSuccessfulP99Latency.toFixed(3));
  }
  return result;
}

// Main function - runs all workloads sequentially
async function main() {
  const allResults = {};
  const errors = [];

  for (let i = 0; i < WORKLOAD_NAMES.length; i++) {
    const workloadName = WORKLOAD_NAMES[i];

    try {
      const result = await runWorkloadBenchmark(workloadName);

      if (result) {
        allResults[workloadName] = result;
        console.log(`\n✅ Completed ${workloadName}`);
      } else {
        errors.push(`${workloadName}: No successful runs`);
      }
    } catch (e) {
      console.error(`\n❌ Error running workload ${workloadName}: ${e.message}`);
      errors.push(`${workloadName}: ${e.message}`);
    }

    // Cooldown between workloads (skip after last workload)
    if (i < WORKLOAD_NAMES.length - 1) {
      console.log(`\n⏳ Cooling down for ${CLUSTER_COOLDOWN_SECONDS_AFTER_WORKLOAD}s before next workload...`);
      await sleep(CLUSTER_COOLDOWN_SECONDS_AFTER_WORKLOAD);
    }
  }

  // Print summary
  console.log('\n' + '='.repeat(60));
  console.log('=== Final Summary ===');
  console.log('='.repeat(60));

  for (const [workloadName, result] of Object.entries(allResults)) {
    console.log(`\n${workloadName}:`);
    console.log(JSON.stringify(result, null, 2));
  }

  if (errors.length > 0) {
    console.log('\n⚠️  Errors:');
    for (const error of errors) {
      console.log(`  - ${error}`);
    }
  }

  // Fail if no workloads succeeded
  if (Object.keys(allResults).length === 0) {
    throw new Error('All workloads failed - no successful runs');
  }

  // Write single summary file with all workload results
  const summaryOutput = {
    clusterName: CLUSTER_NAME,
    workloads: allResults,
  };
  writeFileSync('capacity_summary.json', JSON.stringify(summaryOutput, null, 2));
  console.log('\nResults written to capacity_summary.json');

  return allResults;
}

// Run
main().catch((e) => {
  console.error(`\nError: ${e.message}`);
  process.exit(1);
});


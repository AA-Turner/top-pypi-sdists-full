/* Capacity benchmark runner.
 * Uses binary search to efficiently find the maximum concurrent runs target in (0, rampEnd].
 * Stops when the optimal target is found and reports max successful target + avg execution latency.
 *
 * Supports running multiple workloads sequentially for a single cluster.
 * Set WORKLOAD_NAMES as a comma-separated list (e.g., "parallel-small,parallel-tiny,sequential-small")
 * or use WORKLOAD_NAME for a single workload (backwards compatible).
 */

import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { clean } from './clean.js';

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
  'py-3-node': {
    url: 'https://cap-bench-py-3-node-3faf368e14ad50d2806dba0e7807d2df.staging.langgraph.app',
    rampEndMultiplier: 1.2,
  },
  'py-5-node': {
    url: 'https://cap-bench-py-5-node-bb59e89d2cd252fa9336cd88843c763a.staging.langgraph.app',
    rampEndMultiplier: 1.5,
  },
  'py-7-node': {
    url: 'https://cap-bench-py-7-node-5f471cdb8a725e0bbb076cc9fb32b76d.staging.langgraph.app',
    rampEndMultiplier: 1.8,
  },
  'py-10-node': {
    url: 'https://cap-bench-py-10-node-cf91dbee24535985a8fa50062acfb917.staging.langgraph.app',
    rampEndMultiplier: 2.0,
  },
  'py-15-node': {
    url: 'https://cap-bench-py-15-node-fdd2802964f756a09a7a5cb90a0762ae.staging.langgraph.app',
    rampEndMultiplier: 2.2,
  },
  'py-20-node': {
    url: 'https://cap-bench-py-20-node-0970dd3e458059e488db99d48c69ca69.staging.langgraph.app',
    rampEndMultiplier: 2.4,
  },
  // Distributed runtime multi-node scaling benchmarks
  'dr-1-node': {
    url: 'https://cap-bench-dr-1-node-49e9ad9e573e55f38c51a11626e72e89.staging.langgraph.app',
    rampEndMultiplier: 1,
  },
  'dr-3-node': {
    url: 'https://cap-bench-dr-3-node-467456b54e7f5606bca4cf4466ed2c9a.staging.langgraph.app',
    rampEndMultiplier: 1.2,
  },
  'dr-5-node': {
    url: 'https://cap-bench-dr-5-node-f3c7580d25e65a6ba48dc640f3a9922e.staging.langgraph.app',
    rampEndMultiplier: 1.5,
  },
  'localhost': {
    url: 'http://localhost:9123',
    rampEndMultiplier: 1.8,
  },
  'dr-7-node': {
    url: 'https://cap-bench-dr-7-node-fbf64b46fc9b57239764478187abe534.staging.langgraph.app',
    rampEndMultiplier: 1.8,
  },
  'dr-10-node': {
    url: 'https://cap-bench-dr-10-node-f6a3fb40c33f533fbcfafeee02f9ed68.staging.langgraph.app',
    rampEndMultiplier: 2.0,
  },
  'dr-15-node': {
    url: 'https://cap-bench-dr-15-node-38c2ba919c73556c9b2e64d8c2e8f839.staging.langgraph.app',
    rampEndMultiplier: 2.2,
  },
  'dr-20-node': {
    url: 'https://cap-bench-dr-20-node-7cea036a01a25a9caec0be0b873f9b0a.staging.langgraph.app',
    rampEndMultiplier: 2.4,
  },
};

const workloadNameToAgentParams = {
  'stateless-parallel-small': {
    expand: 100,  // 100 parallel branches
    steps: 1,    // 1 supserstep only
    dataSize: 1000, // 1KB per step × 100 = 100KB total
    delay: 0,
    rampEndBase: 200,
    runExecutionTimeoutSeconds: 60,
  },
  'stateless-parallel-medium': {
    expand: 100,  // 100 parallel branches
    steps: 1,    // 1 supserstep only
    dataSize: 10000, // 10KB per step × 100 = 1MB total
    delay: 0,
    rampEndBase: 200,
    runExecutionTimeoutSeconds: 60,
  },
  'parallel-small': {
    runMode: 'stateful',
    expand: 100,
    steps: 1,    // 1 supserstep only
    dataSize: 1000, // 1KB * 100 = 100KB total
    delay: 0,
    rampEndBase: 200,
    runExecutionTimeoutSeconds: 60,
  },
  'parallel-medium': {
    runMode: 'stateful',
    expand: 100,
    steps: 1,    // 1 supserstep only
    dataSize: 10000, // 10KB * 100 = 1MB total
    delay: 0,
    rampEndBase: 200,
    runExecutionTimeoutSeconds: 60,
  }
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

  const envVars = {
    ...process.env,
    BASE_URL: baseUrl,
    TARGET: String(target),
    DATA_SIZE: String(agentParams.dataSize),
    DELAY: String(agentParams.delay),
    EXPAND: String(agentParams.expand),
    STEPS: String(agentParams.steps),
    RUN_EXECUTION_TIMEOUT_SECONDS: String(agentParams.runExecutionTimeoutSeconds),
    // Use workload-specific runMode if set, otherwise use global RUN_MODE
    RUN_MODE: agentParams.runMode || RUN_MODE,
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
  const rampEnd = workloadConfig.rampEndBase * clusterSettings.rampEndMultiplier;

  console.log(`\n${'='.repeat(60)}`);
  console.log(`=== Workload: ${workloadName} ===`);
  console.log(`${'='.repeat(60)}`);
  console.log(`  - Search Range: (0, ${rampEnd}] (${workloadConfig.rampEndBase} × ${clusterSettings.rampEndMultiplier}) (using binary search)`);
  console.log(`  - Timeout: ${workloadConfig.runExecutionTimeoutSeconds}s`);
  console.log(`  - Expand: ${workloadConfig.expand}`);
  console.log(`  - Steps: ${workloadConfig.steps}`);
  console.log(`  - Data Size: ${workloadConfig.dataSize} bytes`);
  console.log(`  - Delay: ${workloadConfig.delay}s`);
  if (workloadConfig.runMode) {
    console.log(`  - Run Mode: ${workloadConfig.runMode} (workload-specific)`);
  }
  if (workloadConfig.benchmarkType) {
    console.log(`  - Benchmark Type: ${workloadConfig.benchmarkType}`);
  }

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
      console.log(`✅ Success: ${metrics.avgExecutionLatencySeconds.toFixed(3)}s avg latency (${metrics.successRate.toFixed(2)}% success rate)`);
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

  return {
    maxSuccessfulTarget: lastSuccessfulTarget,
    avgExecutionLatencySeconds: Number(lastSuccessfulLatency.toFixed(3)),
  };
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


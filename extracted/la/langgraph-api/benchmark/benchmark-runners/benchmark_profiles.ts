export interface BenchmarkContext {
  delay: number;
  delay_jitter_ratio: number;
  expand: number;
  steps: number;
  checkpoint_size: number;
  llm_enabled: boolean;
  stream_size: number;
  chunk_size: number;
  burst_mode: boolean;
  burst_probability: number;
  burst_size: number;
}

export interface BenchmarkProfileEnv {
  BENCHMARK_PROFILE?: string;
  BENCHMARK_TYPE?: string;
  RUN_MODE?: string;
  STREAM_RESUMABLE?: string;
  DELAY?: string;
  DELAY_JITTER_RATIO?: string;
  EXPAND?: string;
  STEPS?: string;
  CHECKPOINT_SIZE?: string;
  LLM_ENABLED?: string;
  STREAM_SIZE?: string;
  CHUNK_SIZE?: string;
  BURST_MODE?: string;
  BURST_PROBABILITY?: string;
  BURST_SIZE?: string;
}

export interface CapacityProfileSettings {
  runMode: 'stateless' | 'stateful';
  rampEndBase: number;
  runExecutionTimeoutSeconds: number;
}

export interface BenchmarkProfile {
  context: BenchmarkContext;
  resumable: boolean;
  capacity: CapacityProfileSettings;
}

export interface ParsedBenchmarkProfile {
  name: string;
  benchmarkType: string;
  runMode: 'stateless' | 'stateful';
  resumable: boolean;
  context: BenchmarkContext;
  capacity: CapacityProfileSettings;
}

const DEFAULT_PROFILE_NAME = 'default';

export const BENCHMARK_PROFILES: Record<string, BenchmarkProfile> = {
  default: {
    resumable: false,
    context: {
      delay: 0,
      delay_jitter_ratio: 0.2,
      expand: 1,
      steps: 1,
      checkpoint_size: 1024,
      llm_enabled: false,
      stream_size: 0,
      chunk_size: 1,
      burst_mode: false,
      burst_probability: 0,
      burst_size: 0,
    },
    capacity: {
      runMode: 'stateless',
      rampEndBase: 200,
      runExecutionTimeoutSeconds: 60,
    },
  },
  'streaming-long': {
    resumable: true,
    context: {
      delay: 0.5,
      delay_jitter_ratio: 0.2,
      expand: 1,
      steps: 300,
      checkpoint_size: 0,
      llm_enabled: true,
      stream_size: 2 * 1024,
      chunk_size: 2 * 1024,
      burst_mode: true,
      burst_probability: 0.05,
      burst_size: 2 * 1024 * 1024,
    },
    capacity: {
      runMode: 'stateful',
      rampEndBase: 20,
      runExecutionTimeoutSeconds: 1000,
    },
  },
  'stateless-parallel-small': {
    resumable: false,
    context: {
      delay: 0,
      delay_jitter_ratio: 0.2,
      expand: 100,
      steps: 1,
      checkpoint_size: 1_000,
      llm_enabled: false,
      stream_size: 0,
      chunk_size: 1,
      burst_mode: false,
      burst_probability: 0,
      burst_size: 0,
    },
    capacity: {
      runMode: 'stateless',
      rampEndBase: 200,
      runExecutionTimeoutSeconds: 60,
    },
  },
  'stateless-parallel-medium': {
    resumable: false,
    context: {
      delay: 0,
      delay_jitter_ratio: 0.2,
      expand: 100,
      steps: 1,
      checkpoint_size: 10_000,
      llm_enabled: false,
      stream_size: 0,
      chunk_size: 1,
      burst_mode: false,
      burst_probability: 0,
      burst_size: 0,
    },
    capacity: {
      runMode: 'stateless',
      rampEndBase: 200,
      runExecutionTimeoutSeconds: 60,
    },
  },
  'parallel-small': {
    resumable: false,
    context: {
      delay: 0,
      delay_jitter_ratio: 0.2,
      expand: 100,
      steps: 1,
      checkpoint_size: 1_000,
      llm_enabled: false,
      stream_size: 0,
      chunk_size: 1,
      burst_mode: false,
      burst_probability: 0,
      burst_size: 0,
    },
    capacity: {
      runMode: 'stateful',
      rampEndBase: 200,
      runExecutionTimeoutSeconds: 60,
    },
  },
  'parallel-medium': {
    resumable: false,
    context: {
      delay: 0,
      delay_jitter_ratio: 0.2,
      expand: 100,
      steps: 1,
      checkpoint_size: 10_000,
      llm_enabled: false,
      stream_size: 0,
      chunk_size: 1,
      burst_mode: false,
      burst_probability: 0,
      burst_size: 0,
    },
    capacity: {
      runMode: 'stateful',
      rampEndBase: 200,
      runExecutionTimeoutSeconds: 60,
    },
  },
};

export function getBenchmarkProfile(profileName?: string): { name: string; profile: BenchmarkProfile } {
  const resolvedName = profileName || DEFAULT_PROFILE_NAME;
  const profile = BENCHMARK_PROFILES[resolvedName];
  if (!profile) {
    throw new Error(
      `Unknown BENCHMARK_PROFILE: "${profileName}". Must be one of: ${Object.keys(BENCHMARK_PROFILES).join(', ')}`
    );
  }
  return { name: resolvedName, profile };
}

export function resolveBenchmarkContext(
  profileName: string | undefined,
  overrides: Partial<BenchmarkContext> = {}
): BenchmarkContext {
  const { profile } = getBenchmarkProfile(profileName);
  return {
    ...profile.context,
    ...overrides,
  };
}

/**
 * There are two possible counts for expected events: normal and burst.
 * ratio * (expected_steps * expand) + 2 will be the min, but could be larger if we hit bursts.
 */
export function getExpectedEvents(context: BenchmarkContext): number {
  return (3 + context.stream_size / context.chunk_size) * (context.steps * context.expand) + 2;
}

function parseOptionalInt(value?: string): number | undefined {
  if (value == null || value === '') return undefined;
  return parseInt(value, 10);
}

function parseOptionalFloat(value?: string): number | undefined {
  if (value == null || value === '') return undefined;
  return parseFloat(value);
}

function parseOptionalBool(value?: string): boolean | undefined {
  if (value == null || value === '') return undefined;
  return value === 'true';
}

export function get_profile(env: BenchmarkProfileEnv): ParsedBenchmarkProfile {
  const profileName = env.BENCHMARK_PROFILE;
  const { name, profile } = getBenchmarkProfile(profileName);
  const context = resolveBenchmarkContext(name, {
    ...(parseOptionalFloat(env.DELAY) !== undefined ? { delay: parseOptionalFloat(env.DELAY)! } : {}),
    ...(parseOptionalFloat(env.DELAY_JITTER_RATIO) !== undefined
      ? { delay_jitter_ratio: parseOptionalFloat(env.DELAY_JITTER_RATIO)! }
      : {}),
    ...(parseOptionalInt(env.EXPAND) !== undefined ? { expand: parseOptionalInt(env.EXPAND)! } : {}),
    ...(parseOptionalInt(env.STEPS) !== undefined ? { steps: parseOptionalInt(env.STEPS)! } : {}),
    ...(parseOptionalInt(env.CHECKPOINT_SIZE) !== undefined ? { checkpoint_size: parseOptionalInt(env.CHECKPOINT_SIZE)! } : {}),
    ...(parseOptionalBool(env.LLM_ENABLED) !== undefined ? { llm_enabled: parseOptionalBool(env.LLM_ENABLED)! } : {}),
    ...(parseOptionalInt(env.STREAM_SIZE) !== undefined ? { stream_size: parseOptionalInt(env.STREAM_SIZE)! } : {}),
    ...(parseOptionalInt(env.CHUNK_SIZE) !== undefined ? { chunk_size: parseOptionalInt(env.CHUNK_SIZE)! } : {}),
    ...(parseOptionalBool(env.BURST_MODE) !== undefined ? { burst_mode: parseOptionalBool(env.BURST_MODE)! } : {}),
    ...(parseOptionalFloat(env.BURST_PROBABILITY) !== undefined
      ? { burst_probability: parseOptionalFloat(env.BURST_PROBABILITY)! }
      : {}),
    ...(parseOptionalInt(env.BURST_SIZE) !== undefined ? { burst_size: parseOptionalInt(env.BURST_SIZE)! } : {}),
  });

  return {
    name,
    benchmarkType: env.BENCHMARK_TYPE || 'wait_write',
    runMode: env.RUN_MODE ? (env.RUN_MODE === 'stateful' ? 'stateful' : 'stateless') : profile.capacity.runMode,
    resumable: env.STREAM_RESUMABLE != null && env.STREAM_RESUMABLE !== ''
      ? parseOptionalBool(env.STREAM_RESUMABLE) ?? profile.resumable
      : profile.resumable,
    context,
    capacity: profile.capacity,
  };
}



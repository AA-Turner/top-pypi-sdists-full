import { defineConfig } from '@hey-api/openapi-python'
import { recoverDroppedNullability } from '../packages/codegen/src/core/nullable'

/**
 * Python model generation. Emits pydantic v2 models for
 * the whole spec — the same checked-in snapshot and the same unfiltered scope
 * as the TypeScript `openapi-ts.config.ts`, so both languages regenerate from
 * one source on the daily spec-sync cron.
 *
 * Only the `pydantic` plugin runs: hey-api's Python SDK/client layer is still
 * embryonic (no typed params, unsubstituted path templates,
 * sync-only, no errors/retries), so the runtime is hand-written in
 * `src/composio_client/` with the landed TS MVP as the golden
 * reference. The generated models are the one alpha output that is solid today.
 *
 * `output.clean` is off so the hand-written `_generated/__init__.py` package
 * marker survives regen; the single `pydantic_gen.py` file is fully rewritten
 * each run. `@hey-api/openapi-python` is pinned exactly (pre-1.0) in the root
 * package.json, alongside `@hey-api/openapi-ts`.
 */
// Paths are resolved from the process working directory — the repo root, where
// `pnpm generate:python` runs — not from this config file.
export default defineConfig({
  input: './spec/openapi.json',
  output: {
    path: './python/src/composio_client/_generated',
    clean: false,
  },
  parser: {
    // No operation filter: the models cover every operation in the spec, which
    // is what the TypeScript lane has always done. The resource renderer
    // (`packages/codegen/src/core/python-plan.ts`) plans the same forest, so
    // the two lanes cannot be generated from different scopes without one of
    // them declaring a filter — and neither does.
    //
    // The same in-memory nullability recovery the TypeScript config applies
    // (openapi-ts.config.ts): both languages read one spec, so they must read
    // it the same way. Without it `custom_connection_data`'s `expires_in` /
    // `scope` generate as `Optional[Union[float, str, Any]]`, which pydantic
    // collapses to "anything goes" — that is the generator losing a declared
    // union, not the documented Python type relaxation (pydantic models rather
    // than Stainless TypedDicts, and lossless extra-field round-trips).
    // `spec/openapi.json` on disk stays byte-identical.
    patch: {
      input: (spec) => {
        const { nullableOnlyBranches, nullTypeBranches, nullableEnums } =
          recoverDroppedNullability(spec)
        console.info(
          `openapi-python: recovered nullability on ${nullableOnlyBranches} bare-nullable branch(es), ` +
            `${nullTypeBranches} null-type branch(es), ${nullableEnums} enum(s)`,
        )
      },
    },
  },
  plugins: ['pydantic'],
})

/**
 * DataRef — frontend utility for attaching system-table data to AI messages.
 *
 * Usage: build a DataRef (or array of DataRefs) and include them in the
 * `input_data` structured input block when sending a message.
 *
 * Quick example
 * -------------
 *   import { DataRef, buildDataInputBlock } from "@/utils/data_ref_utils";
 *
 *   const block = buildDataInputBlock([
 *     DataRef.record("projects", projectId),
 *     DataRef.query("tasks", {
 *       filter: { project_id: projectId, status: "incomplete" },
 *       fields: ["id", "title", "priority", "due_date"],
 *       sort: { field: "due_date", direction: "asc" },
 *       limit: 20,
 *       label: "Open Tasks",
 *     }),
 *   ]);
 *
 *   // Include `block` in the `content` array of the user message.
 */

// ---------------------------------------------------------------------------
// Allowed tables (mirrors the Python allowlist in data_ref.py).
// The backend enforces this — this list is for IDE autocomplete only.
// ---------------------------------------------------------------------------

export type AllowedTable =
  | "notes"
  | "tasks"
  | "projects"
  | "workspaces"
  | "organizations"
  | "contacts"
  | "contact_groups";

// ---------------------------------------------------------------------------
// Core DataRef types
// ---------------------------------------------------------------------------

/** Fetch one full row from a system table by primary key. */
export interface DbRecordRef {
  ref_type: "db_record";
  table: AllowedTable;
  id: string;
  /** Override the label shown in XML context (defaults to the table name). */
  label?: string;
  /** Subset of fields to include. Omit for all allowed fields. */
  fields?: string[];
  /** If true, a fetch failure silently drops this ref instead of aborting. */
  optional_context?: boolean;
}

/** Fetch multiple rows from a system table with optional filters. */
export interface DbQueryRef {
  ref_type: "db_query";
  table: AllowedTable;
  /** Equality filters: { field: value }. All conditions are ANDed. */
  filter?: Record<string, string | number | boolean | null>;
  /** Subset of fields to include. Omit for all allowed fields. */
  fields?: string[];
  /** Sort order. */
  sort?: { field: string; direction?: "asc" | "desc" };
  /** Maximum rows to return (default 50, max 200). */
  limit?: number;
  /** Label shown in the XML <records> tag. */
  label?: string;
  optional_context?: boolean;
}

/** Fetch a single field value from one row. */
export interface DbFieldRef {
  ref_type: "db_field";
  table: AllowedTable;
  id: string;
  /** The column name to fetch. */
  field_name: string;
  /** Label shown in the XML <field> tag (defaults to field_name). */
  label?: string;
  optional_context?: boolean;
}

export type DataRef = DbRecordRef | DbQueryRef | DbFieldRef;

// ---------------------------------------------------------------------------
// Builder helpers — clean API for constructing refs
// ---------------------------------------------------------------------------

export const DataRef = {
  /**
   * Attach one full record.
   *
   * @example
   *   DataRef.record("projects", projectId)
   *   DataRef.record("tasks", taskId, { fields: ["title", "status", "priority"] })
   */
  record(
    table: AllowedTable,
    id: string,
    opts?: Pick<DbRecordRef, "label" | "fields" | "optional_context">,
  ): DbRecordRef {
    return { ref_type: "db_record", table, id, ...opts };
  },

  /**
   * Attach a filtered set of rows.
   *
   * @example
   *   DataRef.query("tasks", {
   *     filter: { project_id: "abc", status: "incomplete" },
   *     fields: ["id", "title", "priority"],
   *     sort: { field: "priority", direction: "asc" },
   *     limit: 10,
   *     label: "Open Tasks",
   *   })
   */
  query(
    table: AllowedTable,
    opts?: Omit<DbQueryRef, "ref_type" | "table">,
  ): DbQueryRef {
    return { ref_type: "db_query", table, ...opts };
  },

  /**
   * Attach a single field value.
   *
   * @example
   *   DataRef.field("projects", projectId, "description", { label: "Project Goal" })
   */
  field(
    table: AllowedTable,
    id: string,
    field_name: string,
    opts?: Pick<DbFieldRef, "label" | "optional_context">,
  ): DbFieldRef {
    return { ref_type: "db_field", table, id, field_name, ...opts };
  },
} as const;

// ---------------------------------------------------------------------------
// Structured input block builder
// ---------------------------------------------------------------------------

/** Options for the input_data block itself. */
export interface DataInputBlockOptions {
  /**
   * If true, individual ref failures are silently dropped at the block level.
   * Individual refs can also set optional_context independently.
   */
  optional_context?: boolean;
  /**
   * If true, the backend re-fetches on every turn even if already resolved.
   * Use for live data (e.g. task status) that changes between turns.
   */
  keep_fresh?: boolean;
}

/** The structured input content block — include this in the message content array. */
export interface DataInputBlock {
  type: "input_data";
  refs: DataRef[];
  convert_to_text: true;
  optional_context: boolean;
  keep_fresh: boolean;
}

/**
 * Build the `input_data` content block to include in a message's content array.
 *
 * @example
 *   const content = [
 *     { type: "input_text", text: userMessage },
 *     buildDataInputBlock([
 *       DataRef.record("projects", currentProjectId),
 *       DataRef.query("tasks", { filter: { project_id: currentProjectId, status: "incomplete" } }),
 *     ]),
 *   ];
 */
export function buildDataInputBlock(
  refs: DataRef[],
  opts?: DataInputBlockOptions,
): DataInputBlock {
  return {
    type: "input_data",
    refs,
    convert_to_text: true,
    optional_context: opts?.optional_context ?? false,
    keep_fresh: opts?.keep_fresh ?? false,
  };
}

// ---------------------------------------------------------------------------
// What the model receives — for documentation purposes only
// ---------------------------------------------------------------------------

/**
 * The XML the model sees after resolution.  You do NOT need to produce this —
 * the backend generates it.  This is shown here for understanding only.
 *
 * db_record  → <record table="projects" label="Project" id="..."> ... </record>
 * db_query   → <records table="tasks" label="Open Tasks" count="4"> <row ...> ... </row> </records>
 * db_field   → <field table="projects" record_id="..." name="description" label="...">...</field>
 *
 * All refs are wrapped in:
 *   <data_context>
 *     ... resolved XML blocks ...
 *   </data_context>
 */
export type _DocumentationOnly_ModelOutput = never;

/**
 * What the Products tab's two tag editors share: the one-product editor beneath a row
 * (`ProductsPage.tsx::TagEditor`) and the bulk bar above the table (`BulkTagEdit.tsx`).
 * Kept apart from both so neither imports the other.
 */
import type { PickerOption } from './CompanyPicker'
import type { Company, ProductCatalog } from './api'

/** The two owners that are not a customer. Anything else is a customer company key. */
export const SHARED = 'shared'
export const INTERNAL = 'internal'

/** The companies a tag edit picks from (`/api/manage/companies`): the RBAC service's
 *  enabled customers. Read once per page load, and only where edits are offered. */
export type Companies =
  | { status: 'loading' }
  | { status: 'ready'; list: Company[] }
  | { status: 'error'; message: string }

/** The owners that are not a customer, first in the owner picker. */
export const FIXED_OWNERS: PickerOption[] = [
  { value: SHARED, label: 'Shared', hint: 'every customer' },
  { value: INTERNAL, label: 'Internal', hint: 'EdgeScale only' },
]

/** What the editors need from the page. Stable across keystrokes, so the memoized rows
 *  do not all re-render while someone types in the search. */
export type EditContext = {
  csrfToken: string
  companies: Companies
  onEdit: (productId: string | null) => void
  onCatalog: (data: ProductCatalog) => void
  onReload: () => void
  onExpired: () => void
}

/** When this tab last made a tag edit (sessionStorage, so it outlives a reload). The
 *  server caches tags per ECS task and an edit clears only the task that made it, so
 *  for a while after one the page asks for them fresh (`?fresh=1`, which the server
 *  bounds per person). Longer than the server's 30-second cache, with room to spare. */
const EDITED_AT = 'console.products.editedAt'
const FRESH_FOR_MS = 60_000

export function markEdited() {
  try {
    sessionStorage.setItem(EDITED_AT, String(Date.now()))
  } catch {
    // No storage (private window, blocked): the next read may be up to 30s old.
  }
}

export function editedRecently(): boolean {
  try {
    const at = Number(sessionStorage.getItem(EDITED_AT))
    return at > 0 && Date.now() - at < FRESH_FOR_MS
  } catch {
    return false
  }
}

/** What the pickers say in place of customers while the list is not there. */
export function companiesNote(c: Companies): string | undefined {
  if (c.status === 'loading') return 'Loading the companies…'
  if (c.status === 'error') return `No customers to choose from: ${c.message}`
  return undefined
}

/** The customers in a picker group, from the companies list (none until it is read). */
export function customerOptions(c: Companies): PickerOption[] {
  return c.status === 'ready' ? c.list.map(x => ({ value: x.company, label: x.display_name })) : []
}

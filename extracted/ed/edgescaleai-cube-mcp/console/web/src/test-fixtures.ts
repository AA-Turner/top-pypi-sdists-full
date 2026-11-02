/**
 * Shared test fixtures for the inventory join (OI-2).
 *
 * `INVENTORY_OFF` is the default every pre-existing test wants: the join disabled, so
 * the console renders exactly what it rendered before the feature existed. Keeping it
 * here rather than inline in each suite means the *default* is one edit away if the
 * server's descriptor shape changes, while any test that cares about inventory has to
 * name a different fixture explicitly — which is the direction that keeps the
 * interesting cases visible.
 */

import type { Hardware, Inventory, InventorySource } from './api'

/** The join is not enabled on this stack. No banner, no fields. */
export const INVENTORY_OFF: InventorySource = {
  enabled: false,
  available: true,
  simulated: false,
}

/** Enabled, live, and answering. */
export const INVENTORY_LIVE: InventorySource = {
  enabled: true,
  available: true,
  simulated: false,
}

/** Enabled but the backend could not be reached. */
export const INVENTORY_UNAVAILABLE: InventorySource = {
  enabled: true,
  available: false,
  simulated: false,
}

/** Enabled and serving deterministic fictional records. */
export const INVENTORY_SIMULATED: InventorySource = {
  enabled: true,
  available: true,
  simulated: true,
}

/** A complete inventory record, overridable field by field. */
export function inventoryRecord(over: Partial<Inventory> = {}): Inventory {
  return {
    customer: 'Northwind Foods',
    label: 'Northwind-Toledo-1',
    environment: 'prod',
    serial: 'ES000123',
    status: 'allocated',
    location: 'Toledo, OH',
    router_mac: '10:56:CA:12:34:56',
    ...over,
  }
}


/** A fully-specced hardware record. Values are REAL ones read off prod cube
 *  `cube-jycodbbv`, so the table is exercised against what it will actually get. */
export function hardwareRecord(over: Partial<Hardware> = {}): Hardware {
  return {
    server_manufacturer: 'Supermicro',
    server_model: 'Super Server',
    motherboard_manufacturer: 'Supermicro',
    motherboard_model: 'X14SBM-TF',
    cpu_manufacturer: 'Intel',
    cpu_model: 'Intel(R) Xeon(R) 6521P',
    cpu_cores: '24',
    cpu_threads: '48',
    cpu_max_clock: '4100',
    memory_total: '128 GB',
    memory_type: 'DDR5',
    memory_speed: '6400 MHz',
    memory_manufacturer: 'Samsung',
    memory_ecc: 'ECC',
    memory_dimm_count: '4',
    memory_dimm_size: '32 GB',
    memory_dimm_locators: ['DIMMA1', 'DIMMC1', 'DIMME1', 'DIMMG1'],
    ssd_manufacturer: 'Kingston',
    ssd_model: 'KINGSTON SEDC3000ME3T8',
    ssd_type: 'NVMe',
    ssd_capacities: ['3.84 TB', '3.84 TB', '3.84 TB', '3.84 TB'],
    gpu_manufacturers: ['NVIDIA'],
    gpu_models: ['NVIDIA RTX Pro 5000 Blackwell'],
    gpu_memories: [],
    ...over,
  }
}

/** The sparse shape most of the fleet actually has: a server model and nothing else.
 *  67 of 72 prod cubes carry SOMETHING; only 31 have 10+ of the 24 fields. */
export function sparseHardwareRecord(): Hardware {
  return hardwareRecord({
    motherboard_manufacturer: '', motherboard_model: '',
    cpu_manufacturer: '', cpu_model: '', cpu_cores: '', cpu_threads: '',
    cpu_max_clock: '', memory_total: '', memory_type: '', memory_speed: '',
    memory_manufacturer: '', memory_ecc: '', memory_dimm_count: '',
    memory_dimm_size: '', memory_dimm_locators: [],
    ssd_manufacturer: '', ssd_model: '', ssd_type: '', ssd_capacities: [],
    gpu_manufacturers: [], gpu_models: [], gpu_memories: [],
    server_manufacturer: 'EdgescaleAI', server_model: 'Cube v2',
  })
}

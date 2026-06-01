import { ref } from 'vue'
import { listItems, getItem, createItem, updateItem, deleteItem, type Item, type ItemCreate } from '../api/items'

export type { Item, ItemCreate }

export function useItems() {
  const items = ref<Item[]>([])
  const loading = ref(false)
  const error = ref('')

  async function loadAll() {
    loading.value = true
    error.value = ''
    try {
      items.value = await listItems()
    } catch (e: any) {
      error.value = e.message || 'Failed to load items'
    } finally {
      loading.value = false
    }
  }

  async function load(id: string): Promise<Item | null> {
    loading.value = true
    error.value = ''
    try {
      return await getItem(id)
    } catch (e: any) {
      error.value = e.message || 'Failed to load item'
      return null
    } finally {
      loading.value = false
    }
  }

  async function save(payload: ItemCreate, id?: string): Promise<boolean> {
    error.value = ''
    try {
      if (id) {
        await updateItem(id, payload)
      } else {
        await createItem(payload)
      }
      return true
    } catch (e: any) {
      error.value = e.message || 'Failed to save item'
      return false
    }
  }

  async function remove(item: Item): Promise<boolean> {
    error.value = ''
    try {
      await deleteItem(item.id)
      items.value = items.value.filter((i) => i.id !== item.id)
      return true
    } catch (e: any) {
      error.value = e.message || 'Failed to delete item'
      return false
    }
  }

  return { items, loading, error, loadAll, load, save, remove }
}

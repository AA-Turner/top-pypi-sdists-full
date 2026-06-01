import { request } from './client'

export interface Item {
  id: string
  name: string
  description: string
}

export interface ItemCreate {
  name: string
  description: string
}

export async function listItems(): Promise<Item[]> {
  return request<Item[]>('/items')
}

export async function getItem(id: string): Promise<Item> {
  return request<Item>(`/items/$${id}`)
}

export async function createItem(payload: ItemCreate): Promise<Item> {
  return request<Item>('/items', {
    method: 'POST',
    body: payload,
  })
}

export async function updateItem(id: string, payload: ItemCreate): Promise<Item> {
  return request<Item>(`/items/$${id}`, {
    method: 'PUT',
    body: payload,
  })
}

export async function deleteItem(id: string): Promise<void> {
  return request<void>(`/items/$${id}`, {
    method: 'DELETE',
  })
}

import { request } from './client'

export interface User {
  id: string
  username: string
}

export interface UserRoles {
  userId: string
  roles: string[]
}

export async function listUsers(): Promise<User[]> {
  return request<User[]>('/users')
}

export async function getUser(userId: string): Promise<User> {
  return request<User>(`/users/$${userId}`)
}

export async function getUserRoles(userId: string): Promise<UserRoles> {
  return request<UserRoles>(`/users/$${userId}/roles`)
}

export async function addUserRole(userId: string, role: string): Promise<UserRoles> {
  return request<UserRoles>(`/users/$${userId}/roles`, {
    method: 'POST',
    body: { role },
  })
}

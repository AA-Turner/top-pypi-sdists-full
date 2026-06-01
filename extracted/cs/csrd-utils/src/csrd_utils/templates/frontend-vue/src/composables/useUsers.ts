import { ref } from 'vue'
import { listUsers, getUser, getUserRoles, addUserRole, type User, type UserRoles } from '../api/users'

export type { User, UserRoles }

export function useUsers() {
  const users = ref<User[]>([])
  const userInfo = ref<User | null>(null)
  const userRoles = ref<UserRoles | null>(null)
  const loading = ref(false)
  const error = ref('')
  const successMsg = ref('')

  async function loadAll() {
    loading.value = true
    error.value = ''
    try {
      users.value = await listUsers()
    } catch (e: any) {
      error.value = e.message || 'Failed to load users'
    } finally {
      loading.value = false
    }
  }

  async function lookup(userId: string) {
    error.value = ''
    successMsg.value = ''
    userInfo.value = null
    userRoles.value = null
    loading.value = true
    try {
      const [user, roles] = await Promise.all([
        getUser(userId),
        getUserRoles(userId),
      ])
      userInfo.value = user
      userRoles.value = roles
    } catch (e: any) {
      error.value = e.message || 'User not found'
    } finally {
      loading.value = false
    }
  }

  async function addRole(role: string): Promise<boolean> {
    if (!userRoles.value) return false
    error.value = ''
    successMsg.value = ''
    try {
      const updated = await addUserRole(userRoles.value.userId, role)
      userRoles.value = updated
      successMsg.value = `Role "${role}" added.`
      return true
    } catch (e: any) {
      error.value = e.message || 'Failed to add role'
      return false
    }
  }

  return { users, userInfo, userRoles, loading, error, successMsg, loadAll, lookup, addRole }
}

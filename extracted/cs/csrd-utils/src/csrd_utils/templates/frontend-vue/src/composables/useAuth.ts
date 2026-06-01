import { ref, computed } from 'vue'
import { setToken, getToken, onAuthCleared } from '../api/client'
import { login as apiLogin, signup as apiSignup } from '../api/auth'

interface UserInfo {
  sub: string
  username: string
  authorities?: string[]
}

function decodeToken(jwt: string): UserInfo | null {
  try {
    const payload = JSON.parse(atob(jwt.split('.')[1]))
    return { sub: payload.sub, username: payload.userName || payload.sub, authorities: payload.authorities }
  } catch {
    return null
  }
}

function isTokenExpired(jwt: string): boolean {
  try {
    const payload = JSON.parse(atob(jwt.split('.')[1]))
    if (!payload.exp) return false
    return payload.exp * 1000 < Date.now() - 30_000
  } catch {
    return true
  }
}

// Restore from localStorage on app init, but discard expired tokens
const savedToken = getToken()
const validToken = savedToken && !isTokenExpired(savedToken) ? savedToken : null
if (savedToken && !validToken) {
  setToken(null)
}
const token = ref<string | null>(validToken)
const user = ref<UserInfo | null>(validToken ? decodeToken(validToken) : null)

// Register callback so client.ts can clear reactive state on 401
// without importing useAuth (avoids circular dependency).
// Handles: DB wiped, JWKS rotated, or any other server-side invalidation.
onAuthCleared(() => {
  token.value = null
  user.value = null
})

export function useAuth() {
  const isAuthenticated = computed(() => token.value !== null)
  const isAdmin = computed(() =>
    user.value?.authorities?.includes('ADMIN') ?? false,
  )

  async function login(username: string, password: string) {
    const response = await apiLogin(username, password)
    token.value = response.accessToken
    user.value = decodeToken(response.accessToken)
    setToken(response.accessToken)
    // Lazy import to break circular dependency: useAuth → router → useAuth
    const { router } = await import('../router')
    router.push('/')
  }

  async function signup(username: string, password: string) {
    await apiSignup({ username, password })
    await login(username, password)
  }

  async function logout() {
    token.value = null
    user.value = null
    setToken(null)
    const { router } = await import('../router')
    router.push('/login')
  }

  return { isAuthenticated, isAdmin, user, login, signup, logout }
}

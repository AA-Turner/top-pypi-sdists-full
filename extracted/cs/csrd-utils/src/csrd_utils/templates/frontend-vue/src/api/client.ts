import { useToast } from '../composables/useToast'

const BASE_URL = '/api'
const TOKEN_KEY = 'auth_token'

interface RequestOptions {
  method?: string
  body?: unknown
  headers?: Record<string, string>
  skipAuthRedirect?: boolean
}

// Auth-clear callback — set by useAuth to avoid circular import
let _onAuthCleared: (() => void) | null = null

export function onAuthCleared(callback: () => void) {
  _onAuthCleared = callback
}

export function setToken(token: string | null) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer $${token}`
  }

  const response = await fetch(`$${BASE_URL}$${path}`, {
    method: options.method || 'GET',
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  })

  if (response.status === 401 && !options.skipAuthRedirect) {
    const detail = await response.json().catch(() => null)
    const message = detail?.detail || 'Session expired — please log in again.'
    const { error } = useToast()
    error(message)
    setToken(null)
    _onAuthCleared?.()
    // Lazy import to break circular dependency: client → router → useAuth → client
    const { router } = await import('../router')
    router.push('/login')
    throw new Error(message)
  }

  if (response.status === 403) {
    const detail = await response.json().catch(() => null)
    const message = detail?.detail || 'Access denied — insufficient permissions.'
    const { error } = useToast()
    error(message)
    throw new Error(message)
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(error.detail || `$${response.status} $${response.statusText}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

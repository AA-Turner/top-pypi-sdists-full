import { request } from './client'

interface TokenResponse {
  accessToken: string
  tokenType: string
}

interface SignupPayload {
  username: string
  password: string
}

export async function login(username: string, password: string): Promise<TokenResponse> {
  return request<TokenResponse>('/token', {
    method: 'POST',
    body: { username, password },
    skipAuthRedirect: true,
  })
}

export async function signup(payload: SignupPayload): Promise<void> {
  return request<void>('/signup', {
    method: 'POST',
    body: payload,
    skipAuthRedirect: true,
  })
}

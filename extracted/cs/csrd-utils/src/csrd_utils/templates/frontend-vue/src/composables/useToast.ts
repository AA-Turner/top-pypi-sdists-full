import { ref } from 'vue'

export interface Toast {
  id: number
  message: string
  type: 'error' | 'info' | 'success'
}

let _nextId = 0
const toasts = ref<Toast[]>([])

export function useToast() {
  function show(message: string, type: Toast['type'] = 'info', duration = 4000) {
    const id = _nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      toasts.value = toasts.value.filter((t) => t.id !== id)
    }, duration)
  }

  function error(message: string) {
    show(message, 'error', 5000)
  }

  function info(message: string) {
    show(message, 'info')
  }

  function success(message: string) {
    show(message, 'success')
  }

  return { toasts, show, error, info, success }
}

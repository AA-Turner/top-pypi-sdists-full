import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { useToast } from '../composables/useToast'

// Lazy-loaded views — each route is code-split into its own chunk.
// To add a new page: define a lazy import and add a route entry below.
const LoginView = () => import('../views/LoginView.vue')
const SignupView = () => import('../views/SignupView.vue')
const DashboardView = () => import('../views/DashboardView.vue')
const ItemListView = () => import('../views/items/ItemListView.vue')
const ItemFormView = () => import('../views/items/ItemFormView.vue')
const UserAdminView = () => import('../views/admin/UserAdminView.vue')

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { public: true } },
  { path: '/signup', name: 'signup', component: SignupView, meta: { public: true } },
  { path: '/', name: 'dashboard', component: DashboardView },
  { path: '/items', name: 'items', component: ItemListView },
  { path: '/items/new', name: 'item-create', component: ItemFormView },
  { path: '/items/:id/edit', name: 'item-edit', component: ItemFormView },
  { path: '/admin/users', name: 'admin-users', component: UserAdminView, meta: { admin: true } },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const { isAuthenticated, isAdmin } = useAuth()
  if (!to.meta.public && !isAuthenticated.value) {
    return { name: 'login' }
  }
  if (to.meta.admin && !isAdmin.value) {
    const { error } = useToast()
    error('Access denied — admin role required.')
    return { name: 'dashboard' }
  }
})

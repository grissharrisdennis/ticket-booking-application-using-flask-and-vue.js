import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import UserDashboard from '../views/UserDashboard.vue'
import NewShow from '../views/NewShow.vue'
import NewVenue from '../views/NewVenue.vue'
import UpdateShow from '../views/UpdateShow.vue'
import UpdateVenue from '../views/UpdateVenue.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import BookingPage from '../views/BookingPage.vue'
import UserBookings from '../views/UserBookings.vue'
import SearchPage from '../views/SearchPage.vue'
import SummaryPage from '../views/SummaryPage.vue'

const routes = [
  {
    path:'/:id/admin/summary',
    name:'SummaryPage',
    component:SummaryPage
  },
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path:'/register',
    name:'RegisterPage',
    component:RegisterPage
  },
  {
    path:'/login',
    name:'LoginPage',
    component:LoginPage
  },
  {
    path: '/:id/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true },
  },
  {
    path:'/:id/admin/createvenue',
    name:'NewVenue',
    component:NewVenue,
    props:true
  },
  {
    path:'/admin/:admin_id/:venue_id/createshow',
    name:'NewShow',
    component:NewShow,
    props:true
  },
  {
    path:'/admin/:admin_id/:venue_id/:show_id/updateshow',
    name:'UpdateShow',
    component:UpdateShow
  },
  {
    path:'/admin/:admin_id/:venue_id/updatevenue',
    name:'UpdateVenue',
    component:UpdateVenue
  },
  {
    path: '/:id/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    props:true,
    meta: { requiresAuth: true },
  },
  {
    path:'/:user_id/show/:venue_id/:show_id/book',
    name:'BookingPage',
    component:BookingPage,
    props:true
  },
  {
    path:'/user/:id/bookings/',
    name:'UserBookings',
    component:UserBookings,
    props:true
  },
  {
  path:'/user/:user_id/:id/search',
  name:'SearchPage',
  component:SearchPage
  }
]


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

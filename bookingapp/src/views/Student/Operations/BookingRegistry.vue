<template>
  <div class="p-4 sm:p-6 lg:p-8 bg-gray-200 min-h-screen poppins">
    <!-- Header -->
    <div class="mb-6 sm:mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 sm:p-6 rounded-[2px] border border-gray-200 shadow-sm relative overflow-hidden group">
      <div class="absolute inset-y-0 left-0 w-1.5 bg-[#fe3787]"></div>
      <div>
        <h1 class="text-3xl font-black text-[#002D1E] tracking-tight italic uppercase">Booking Registry</h1>
        <p class="text-[10px] text-gray-400 font-bold uppercase tracking-[0.2em] mt-1">Simulation Control Ledger • Real-time Records</p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button 
          @click="fetchBookings" 
          class="bg-[#002D1E] text-white px-4 sm:px-5 py-2.5 rounded-[2px] text-[10px] font-black uppercase tracking-widest hover:bg-black transition-all flex items-center gap-2 shadow-lg shadow-gray-200"
          :disabled="loading"
        >
          <i class="ph ph-arrows-clockwise" :class="{'animate-spin': loading}"></i>
          <span class="hidden sm:inline">Sync Registry</span>
          <span class="sm:hidden">Sync</span>
        </button>
        <button 
          @click="$router.push('/student/dashboard')" 
          class="bg-white border border-gray-200 text-gray-600 px-4 sm:px-5 py-2.5 rounded-[2px] text-[10px] font-black uppercase tracking-widest hover:bg-gray-50 transition-all shadow-sm"
        >
          <span class="hidden sm:inline">Exit Ledger</span>
          <span class="sm:hidden">Exit</span>
        </button>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 mb-6 sm:mb-8">
      <div 
        v-for="(count, label) in statsItems" 
        :key="label" 
        class="bg-white p-6 border border-gray-200 rounded-[2px] shadow-sm hover:shadow-md transition-all group"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-[10px] uppercase font-black text-gray-400 tracking-widest leading-none mb-3">{{ label }}</p>
            <p class="text-3xl font-black text-[#002D1E] tracking-tighter">{{ count }}</p>
          </div>
          <div :class="statIconClass(label)" class="w-14 h-14 rounded-[2px] flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform">
            <i :class="[statIcon(label), 'text-2xl']"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Table Section -->
    <div class="bg-white border border-gray-200 rounded-[2px] shadow-sm overflow-hidden flex flex-col min-h-[400px] sm:min-h-[500px]">
      <div class="overflow-x-auto -webkit-overflow-scrolling-touch">
        <table class="w-full text-left min-w-[700px]">
          <thead class="bg-gray-50 text-gray-500 text-[10px] uppercase font-black tracking-[0.15em] border-b border-gray-200">
            <tr>
              <th class="px-4 sm:px-8 py-4 sm:py-5">Global ID</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5">PNR Reference</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5">Manifest User</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5">Sector Flow</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5 text-right">Value</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5 text-center">Status</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5 text-right">Timestamp</th>
              <th class="px-4 sm:px-8 py-4 sm:py-5 text-center">Action</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-100 italic font-medium">
            <tr
              v-for="booking in paginatedBookings"
              :key="booking.id"
              class="hover:bg-gray-50/50 transition-all text-sm group/row"
            >
              <td class="px-4 sm:px-8 py-3 sm:py-5">
                <span class="font-black text-[#fe3787] font-mono tracking-tighter">#{{ booking.id }}</span>
              </td>

              <td class="px-4 sm:px-8 py-3 sm:py-5">
                <span class="font-black text-slate-800 font-mono tracking-[0.2em] uppercase">{{ booking.pnr || '——' }}</span>
              </td>

              <td class="px-4 sm:px-8 py-3 sm:py-5">
                <div class="flex items-center gap-2 sm:gap-4">
                  <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-[2px] bg-slate-100 flex items-center justify-center border border-slate-200 group-hover/row:bg-pink-100 transition-colors shrink-0">
                    <i class="ph ph-user text-slate-400 group-hover/row:text-pink-600 transition-colors"></i>
                  </div>
                  <div class="font-black text-slate-900 uppercase text-xs tracking-tight truncate max-w-[100px] sm:max-w-none">
                    {{ booking.user_name || 'System Generated' }}
                  </div>
                </div>
              </td>

              <td class="px-4 sm:px-8 py-3 sm:py-5">
                 <span class="bg-slate-100 text-slate-500 px-2 sm:px-3 py-1 rounded-[2px] text-[9px] font-black uppercase tracking-widest border border-slate-200 whitespace-nowrap">
                   {{ booking.trip_type?.replace('_', ' ') || 'Single' }}
                 </span>
              </td>

              <td class="px-4 sm:px-8 py-3 sm:py-5 text-right">
                 <span class="font-black text-slate-900 font-mono whitespace-nowrap">₱{{ parseFloat(booking.total_amount).toLocaleString() }}</span>
              </td>

              <td class="px-4 sm:px-8 py-3 sm:py-5 text-center">
                <span
                  class="px-4 py-1.5 text-[9px] font-black uppercase rounded-[2px] border"
                  :class="statusBadge(booking.status)"
                >
                  {{ booking.status }}
                </span>
              </td>

              <td class="px-4 sm:px-8 py-3 sm:py-5 text-right text-gray-400 font-black text-[10px] uppercase whitespace-nowrap">
                {{ formatDate(booking.created_at) }}
              </td>

              <!-- Action Column -->
              <td class="px-8 py-5 text-center">
                <template v-if="booking.status?.toLowerCase() === 'pending'">
                  <!-- Within 24 hours: show Pay Now -->
                  <button
                    v-if="isWithin24Hours(booking.created_at)"
                    @click="continueToPayment(booking)"
                    :disabled="payingBookingId === booking.id"
                    class="inline-flex items-center gap-1.5 px-4 py-2 bg-[#fe3787] hover:bg-pink-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-[9px] font-black uppercase tracking-widest rounded-[2px] transition-all shadow-lg shadow-pink-100 active:scale-95"
                  >
                    <span v-if="payingBookingId === booking.id" class="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                    <i v-else class="ph ph-credit-card"></i>
                    {{ payingBookingId === booking.id ? 'Redirecting...' : 'Pay Now' }}
                  </button>

                  <!-- Over 24 hours: expired, cannot pay -->
                  <div v-else class="flex flex-col items-center gap-1">
                    <span class="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-100 text-gray-400 border border-gray-200 text-[9px] font-black uppercase tracking-widest rounded-[2px]">
                      <i class="ph ph-clock-countdown"></i>
                      Expired
                    </span>
                    <span class="text-[8px] text-gray-300 font-bold uppercase tracking-wider">Window closed</span>
                  </div>
                </template>
                <span v-else class="text-[9px] text-gray-300 font-black uppercase tracking-widest">—</span>
              </td>
            </tr>

            <tr v-if="bookings.length === 0 && !loading">
              <td colspan="8" class="px-8 py-20 text-center">
                <div class="flex flex-col items-center gap-4">
                  <i class="ph ph-scroll text-5xl text-gray-200"></i>
                  <p class="text-gray-400 text-xs font-black uppercase tracking-widest">Registry Empty — No simulation data found</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Section -->
      <div v-if="bookings.length > itemsPerPage" class="mt-auto px-4 sm:px-8 py-4 sm:py-6 border-t border-gray-100 bg-gray-50/30 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="text-[10px] font-black text-gray-400 uppercase tracking-widest flex items-center gap-3">
          <span class="w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
          <span class="hidden sm:inline">Showing entries {{ startIndex + 1 }} to {{ endIndex }} of {{ bookings.length }}</span>
          <span class="sm:hidden">{{ startIndex + 1 }}–{{ endIndex }} / {{ bookings.length }}</span>
        </div>
        <div class="flex gap-1.5 flex-wrap justify-center">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
            class="px-4 sm:px-6 py-2.5 bg-white border border-gray-200 rounded-[2px] text-[10px] font-black uppercase tracking-widest hover:bg-black hover:text-white disabled:opacity-30 disabled:hover:bg-white disabled:hover:text-gray-400 transition-all shadow-sm"
          >
            Prev
          </button>
          <div class="flex gap-1">
            <button 
              v-for="page in visiblePages" 
              :key="page"
              @click="goToPage(page)"
              :disabled="page === '...'"
              :class="[
                'w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center border rounded-[2px] text-[10px] font-black uppercase transition-all shadow-sm',
                page === '...' ? 'bg-white border-gray-200 text-gray-400' : 
                currentPage === page ? 'bg-[#fe3787] text-white border-[#fe3787] shadow-lg shadow-pink-100' : 'bg-white border-gray-200 text-slate-900 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
          </div>
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages"
            class="px-4 sm:px-6 py-2.5 bg-white border border-gray-200 rounded-[2px] text-[10px] font-black uppercase tracking-widest hover:bg-black hover:text-white disabled:opacity-30 disabled:hover:bg-white disabled:hover:text-gray-400 transition-all shadow-sm"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Payment Error Toast -->
    <transition name="toast">
      <div
        v-if="toastMessage"
        class="fixed bottom-6 right-6 z-50 bg-rose-600 text-white text-xs font-black uppercase tracking-widest px-6 py-4 rounded-[2px] shadow-2xl flex items-center gap-3 max-w-sm"
      >
        <i class="ph ph-warning-circle text-lg"></i>
        {{ toastMessage }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"
import AuthStorage from "@/utils/authStorage"
import api from "@/services/booking/api"

const bookings = ref([])
const loading = ref(false)
const payingBookingId = ref(null)
const toastMessage = ref('')
let toastTimer = null

// Pagination State
const currentPage = ref(1);
const itemsPerPage = 8;

const statsItems = computed(() => {
  return {
    'Total Operations': bookings.value.length,
    'Confirmed Flow': bookings.value.filter(b => b.status?.toLowerCase() === 'confirmed').length,
    'Simulation Pending': bookings.value.filter(b => b.status?.toLowerCase() === 'pending').length,
    'Aborted Sessions': bookings.value.filter(b => b.status?.toLowerCase() === 'cancelled').length,
  };
});

// Pagination Logic
const totalPages = computed(() => Math.ceil(bookings.value.length / itemsPerPage));
const paginatedBookings = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return bookings.value.slice(start, start + itemsPerPage);
});
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => Math.min(currentPage.value * itemsPerPage, bookings.value.length));

const visiblePages = computed(() => {
  const pages = [];
  const t = totalPages.value;
  const c = currentPage.value;
  if (t <= 5) {
    for (let i = 1; i <= t; i++) pages.push(i);
  } else {
    if (c <= 3) {
      for (let i = 1; i <= 4; i++) pages.push(i);
      pages.push('...', t);
    } else if (c >= t - 2) {
      pages.push(1, '...');
      for (let i = t - 3; i <= t; i++) pages.push(i);
    } else {
      pages.push(1, '...', c - 1, c, c + 1, '...', t);
    }
  }
  return pages;
});

const statIcon = (label) => {
  if (label === 'Total Operations') return 'ph ph-notebook';
  if (label === 'Confirmed Flow') return 'ph ph-check-circle';
  if (label === 'Simulation Pending') return 'ph ph-clock';
  return 'ph ph-warning-circle';
};

const statIconClass = (label) => {
  if (label === 'Total Operations') return 'bg-blue-50 text-blue-600';
  if (label === 'Confirmed Flow') return 'bg-emerald-50 text-emerald-600';
  if (label === 'Simulation Pending') return 'bg-amber-50 text-amber-600';
  return 'bg-rose-50 text-rose-600';
};

const fetchBookings = async () => {
  loading.value = true
  try {
    const baseURL = (import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : 'https://fbs-backend-production.up.railway.app')).replace(/\/$/, '')
    const res = await axios.get(`${baseURL}/api/bookings/`, {
      headers: AuthStorage.getApiHeaders()
    })
    bookings.value = (res.data.results || res.data).sort((a, b) => b.id - a.id)
  } catch (err) {
    console.error("Fetch failed", err);
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-PH', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// Check if a booking is still within the 24-hour payment window
const PAYMENT_WINDOW_MS = 24 * 60 * 60 * 1000 // 24 hours in milliseconds
const isWithin24Hours = (createdAt) => {
  if (!createdAt) return false
  const age = Date.now() - new Date(createdAt).getTime()
  return age <= PAYMENT_WINDOW_MS
}

// How much time is left in the payment window (for display)
const timeLeft = (createdAt) => {
  if (!createdAt) return ''
  const expiresAt = new Date(createdAt).getTime() + PAYMENT_WINDOW_MS
  const diff = expiresAt - Date.now()
  if (diff <= 0) return 'Expired'
  const hrs = Math.floor(diff / (1000 * 60 * 60))
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  return `${hrs}h ${mins}m left`
}

const statusBadge = (status) => {
  if (!status) return 'bg-gray-100 text-gray-500 border-gray-200'
  switch (status.toLowerCase()) {
    case "pending":
      return "bg-amber-50 text-amber-700 border-amber-200"
    case "confirmed":
      return "bg-emerald-50 text-emerald-700 border-emerald-200"
    case "cancelled":
      return "bg-rose-50 text-rose-700 border-rose-200"
    default:
      return "bg-gray-100 text-gray-600 border-gray-200"
  }
}

const showToast = (message, duration = 4000) => {
  toastMessage.value = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toastMessage.value = '' }, duration)
}

/**
 * Resume payment for a pending booking using the same PayMongo flow as PaymentView.vue
 * Calls POST flightapp/create-checkout-session/ with booking_id + amount, then redirects.
 */
const continueToPayment = async (booking) => {
  if (payingBookingId.value) return // prevent double-click

  // Enforce the 24-hour payment window
  if (!isWithin24Hours(booking.created_at)) {
    showToast('Payment window has expired. This booking can no longer be paid (>24 hours old).')
    return
  }

  payingBookingId.value = booking.id

  try {
    const amount = parseFloat(booking.total_amount)
    if (!amount || amount <= 0) {
      showToast('Invalid booking amount. Cannot process payment.')
      return
    }

    const payload = {
      booking_id: booking.id,
      amount: amount,
      customer_email: booking.contact_email || booking.user_email || 'student@fbs.edu',
      customer_name: booking.user_name || 'Student',
      customer_phone: booking.contact_phone || '09171234567'
    }

    const response = await api.post('flightapp/create-checkout-session/', payload)

    if (response.data?.success && response.data?.checkout_url) {
      // Save session so PaymentCallback can restore state
      localStorage.setItem('payment_session', JSON.stringify({
        checkout_url: response.data.checkout_url,
        booking_id: booking.id,
        booking_reference: booking.pnr,
        amount: amount,
        timestamp: Date.now()
      }))
      // Redirect to PayMongo checkout
      window.location.href = response.data.checkout_url
    } else {
      const errMsg = response.data?.error || 'Failed to create checkout session.'
      showToast(`Payment error: ${typeof errMsg === 'string' ? errMsg : JSON.stringify(errMsg)}`)
    }
  } catch (err) {
    console.error('Payment initiation failed:', err)
    showToast(err?.response?.data?.error || 'Could not connect to payment gateway. Please try again.')
  } finally {
    payingBookingId.value = null
  }
}

const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++; };
const goToPage = (p) => { if (p !== '...') currentPage.value = p; };

onMounted(fetchBookings)
</script>

<style scoped>
.poppins { font-family: 'Poppins', sans-serif; }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateY(20px); }
.toast-leave-to { opacity: 0; transform: translateY(20px); }
</style>

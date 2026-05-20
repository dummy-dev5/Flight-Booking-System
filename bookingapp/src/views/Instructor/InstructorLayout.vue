<template>
  <div class="flex flex-col h-screen bg-[#F9FAFB] font-sans">
    <!-- Premium Loading Overlay -->
    <LoadingOverlay :loading="isLoading" />
    
    <InstructorHeader 
      class="no-print"
      :full-name="userStore.userFullName || 'Instructor'"
      :initials="initials"
      :profile-picture="profilePictureUrl"
      :dropdown-open="dropdownOpen"
      :notifications-open="notificationDropdownOpen"
      :unseen-count="unseenCount"
      :notifications="allNotifications"
      @toggle-sidebar="toggleSidebar"
      @toggle-dropdown="toggleDropdown"
      @toggle-notifications="toggleNotificationDropdown"
      @go-to-profile="router.push('/instructor/profile')"
      @logout="handleLogout"
    />

    <div class="flex flex-1 overflow-hidden">
      <InstructorSidebar 
        class="no-print"
        :sidebar-open="sidebarOpen"
        :sections="sections"
        :profile-picture="profilePictureUrl"
        @nav="router.push($event)"
        @go-to-section="goToSection"
      />

      <div class="flex-1 overflow-auto bg-[#F9FAFB]">
        <!-- Render the matched child component -->
        <router-view 
          v-if="!isLoading"
          :sections="sections" 
          @refresh-data="fetchInstructorData"
        />
      </div>
    </div>

    <!-- Real-time Schedule Alert Modal (Global) -->
    <div v-if="showScheduleAlert" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-md px-4 p-20">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in duration-300 border border-white/20">
        <div class="bg-gradient-to-br from-slate-900 to-slate-800 p-8 text-center relative overflow-hidden">
          <div class="absolute inset-0 bg-pink-500/10 animate-pulse"></div>
          <div class="relative z-10">
            <div class="w-16 h-16 bg-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 rotate-3 shadow-lg shadow-pink-500/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-white text-xl font-black uppercase tracking-widest mb-1">Schedule Alert</h3>
            <p class="text-pink-400 text-[10px] font-bold uppercase tracking-[0.3em] font-sans">Cabagan State University • {{ currentTimeDisplay }}</p>
          </div>
        </div>

        <div class="p-8 text-center bg-white">
          <p class="text-slate-500 text-sm font-medium mb-2 uppercase tracking-tight">You have a Schedule today in</p>
          <h2 class="text-3xl font-black text-slate-800 mb-2 leading-tight">{{ currentAlertSchedule?.sectionName }}</h2>
          <div class="inline-flex flex-center items-center gap-2 bg-pink-50 px-4 py-2 rounded-full border border-pink-100 mb-8">
            <span class="w-2 h-2 bg-pink-500 rounded-full animate-ping"></span>
            <span class="text-pink-600 font-black text-xs uppercase tracking-widest">
              {{ formatTimeOnly(currentAlertSchedule?.start_time) }} - {{ formatTimeOnly(currentAlertSchedule?.end_time) }}
            </span>
          </div>

          <div class="space-y-3">
             <button 
               @click="acknowledgeSchedule" 
               class="w-full py-4 bg-pink-500 hover:bg-pink-600 text-white rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-xl shadow-pink-200 transition-all active:scale-[0.98]"
             >
               Dismiss
             </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { instructorDashboardService } from '@/services/instructor/instructorDashboardService'
import InstructorHeader from '@/components/instructor/InstructorHeader.vue'
import InstructorSidebar from '@/components/instructor/InstructorSidebar.vue'
import LoadingOverlay from '@/components/instructor/LoadingOverlay.vue'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'

const router = useRouter()
const userStore = useUserStore()
const notificationStore = useNotificationStore()

const isLoading = ref(false)
const sidebarOpen = ref(true) // Sidebar default open in layout
const dropdownOpen = ref(false)
const sections = ref([])
const lastSyncTime = ref(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))

// Notification & Alert State
const dismissedSchedules = ref(new Set())
const shownAlerts = ref(new Set())
const readNotificationIds = ref(new Set())
const showScheduleAlert = ref(false)
const notificationDropdownOpen = ref(false)
const currentAlertSchedule = ref(null)
const currentTimeDisplay = ref(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }))
let scheduleInterval = null

// Helper to get user-specific storage keys
const getStorageKey = (base) => {
  const userId = userStore.user?.id || 'anon'
  return `${base}_${userId}`
}

// Function to load user-specific state
const loadUserState = async () => {
  const userId = userStore.user?.id
  if (!userId) return

  // Load from LocalStorage for immediate UI feedback
  dismissedSchedules.value = new Set(JSON.parse(localStorage.getItem(getStorageKey('dismissedSchedules')) || '[]'))
  shownAlerts.value = new Set(JSON.parse(localStorage.getItem(getStorageKey('shownAlerts')) || '[]'))
  readNotificationIds.value = new Set(JSON.parse(localStorage.getItem(getStorageKey('readNotificationIds')) || '[]'))

  // Sync with Backend for true persistence across devices/logouts
  try {
    const data = await instructorDashboardService.getReadStatuses();
    if (data.read_notification_ids) {
      data.read_notification_ids.forEach(id => readNotificationIds.value.add(id));
      readNotificationIds.value = new Set(readNotificationIds.value);
    }
  } catch (error) {
    console.error("Failed to sync notifications with backend:", error);
  }
}

watch(dismissedSchedules, (newVal) => {
  if (userStore.user?.id) {
    localStorage.setItem(getStorageKey('dismissedSchedules'), JSON.stringify([...newVal]))
  }
}, { deep: true })

watch(shownAlerts, (newVal) => {
  if (userStore.user?.id) {
    localStorage.setItem(getStorageKey('shownAlerts'), JSON.stringify([...newVal]))
  }
}, { deep: true })

watch(readNotificationIds, (newVal) => {
  if (userStore.user?.id) {
    localStorage.setItem(getStorageKey('readNotificationIds'), JSON.stringify([...newVal]))
  }
}, { deep: true })

watch(() => userStore.user?.id, async (newUserId) => {
  if (newUserId) await loadUserState()
})

const formatTimeOnly = (t) => {
  if (!t) return ''
  const [h, m] = t.split(':')
  const hour = parseInt(h)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const h12 = hour % 12 || 12
  return `${h12}:${m} ${ampm}`
}

const parsedSectionSchedule = (scheduleData) => {
  if (!scheduleData) return null
  try {
    const schedules = typeof scheduleData === 'string' ? JSON.parse(scheduleData) : scheduleData
    if (Array.isArray(schedules) && schedules.length > 0) return schedules
  } catch (e) {}
  return null
}

const getMostRecentOccurrence = (dayName, timeStr, now = new Date()) => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  const shortDays = ['su', 'mo', 'tu', 'we', 'th', 'fr', 'sa']
  
  let targetDayIndex = days.findIndex(d => d.toLowerCase() === dayName.toLowerCase())
  if (targetDayIndex === -1) {
    targetDayIndex = shortDays.findIndex(d => d === dayName.toLowerCase().substring(0, 2))
  }
  
  if (targetDayIndex === -1) return null
  
  const [hours, minutes] = timeStr.split(':').map(Number)
  const occurrence = new Date(now)
  occurrence.setHours(hours, minutes, 0, 0)
  
  const currentDayIndex = now.getDay()
  const daysDiff = (currentDayIndex - targetDayIndex + 7) % 7
  occurrence.setDate(now.getDate() - daysDiff)
  
  if (occurrence > now) {
    occurrence.setDate(occurrence.getDate() - 7)
  }
  
  return occurrence
}

const currentFullTime = ref(new Date())

const allNotifications = computed(() => {
  const now = currentFullTime.value
  const notifications = []
  
  sections.value.forEach(section => {
    const schedules = parsedSectionSchedule(section.schedule)
    if (schedules) {
      schedules.forEach(s => {
        const occurrence = getMostRecentOccurrence(s.day, s.start_time, now)
        if (!occurrence) return
        
        const diffMs = now - occurrence
        const isPast = occurrence < now
        const isWithinWindow = diffMs < 48 * 60 * 60 * 1000 
        
        if (isPast && isWithinWindow) {
          const scheduleId = `${section.id}-${s.day}-${s.start_time}`
          const dateStr = occurrence.toDateString().replace(/\s+/g, '_')
          const notificationId = `${scheduleId}_${dateStr}_missed`
          
          if (!dismissedSchedules.value.has(scheduleId)) {
            notifications.push({
              ...s,
              type: 'missed',
              sectionId: section.id,
              sectionName: section.section_name,
              scheduleId,
              id: notificationId,
              read: readNotificationIds.value.has(notificationId),
              occurrenceTime: occurrence,
              displayMessage: `You missed your ${formatTimeOnly(s.start_time)} session.`
            })
          }
        }
      })
    }
  })
  
  return notifications.sort((a, b) => b.occurrenceTime - a.occurrenceTime)
})

const unseenCount = computed(() => {
  return allNotifications.value.filter(n => !n.read).length
})

const initials = computed(() => {
  const u = userStore.user?.username || userStore.user?.first_name || 'I'
  return u[0].toUpperCase()
})

const profilePictureUrl = computed(() => {
  const avatar = userStore.user?.avatar
  if (!avatar) return null
  if (avatar.startsWith('http')) return avatar
  const baseURL = import.meta.env.VITE_API_URL || 'https://fbs-backend-production.up.railway.app'
  return `${baseURL}${avatar}`
})

const toggleSidebar = () => { sidebarOpen.value = !sidebarOpen.value }
const toggleDropdown = () => { 
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) notificationDropdownOpen.value = false
}
const toggleNotificationDropdown = async () => {
  notificationDropdownOpen.value = !notificationDropdownOpen.value
  if (notificationDropdownOpen.value) {
    dropdownOpen.value = false
    
    // Find unread notification IDs
    const unreadIds = allNotifications.value
      .filter(n => !n.read)
      .map(n => n.id)
      
    if (unreadIds.length > 0) {
      // Mark as read locally
      unreadIds.forEach(id => readNotificationIds.value.add(id))
      readNotificationIds.value = new Set(readNotificationIds.value)
      
      // Persist to backend
      try {
        await instructorDashboardService.markNotificationsRead(unreadIds)
      } catch (error) {
        console.error("Failed to mark notifications read in backend:", error)
      }
    }
  }
}

const goToSection = (id) => {
  router.push(`/instructor/section/${id}`)
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const acknowledgeSchedule = () => {
  if (currentAlertSchedule.value) {
    const scheduleId = `${currentAlertSchedule.value.sectionId}-${currentAlertSchedule.value.day}-${currentAlertSchedule.value.start_time}`
    dismissedSchedules.value.add(scheduleId)
    dismissedSchedules.value = new Set(dismissedSchedules.value)
  }
  showScheduleAlert.value = false
}

const checkScheduleAlerts = () => {
  const now = new Date()
  currentFullTime.value = now 
  currentTimeDisplay.value = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  
  const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  const today = days[now.getDay()]

  sections.value.forEach(section => {
    const schedules = parsedSectionSchedule(section.schedule)
    if (schedules) {
      schedules.forEach(s => {
        if (s.day === today && s.start_time === currentTime) {
          const alertId = `${section.id}-${s.day}-${s.start_time}-${now.toDateString()}`
          if (!shownAlerts.value.has(alertId)) {
            currentAlertSchedule.value = {
              ...s,
              sectionId: section.id,
              sectionName: section.section_name,
              scheduleId: alertId
            }
            showScheduleAlert.value = true
            shownAlerts.value.add(alertId)
            shownAlerts.value = new Set(shownAlerts.value)
          }
        }
      })
    }
  })
}

const fetchInstructorData = async () => {
  // Use a slight delay or only show loading if it takes long
  // For standard nav, we might not want full screen overlay everytime
  try {
    const data = await instructorDashboardService.getDashboard();
    sections.value = data.sections;
    if (data.user) {
      userStore.user = data.user;
    }
    lastSyncTime.value = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch (error) {
    if (error.response?.status === 401 || error.response?.status === 403) {
      handleLogout();
    }
  }
}

onMounted(async () => {
  isLoading.value = true
  await userStore.ensureUserLoaded();
  await loadUserState(); 
  await fetchInstructorData();
  isLoading.value = false
  
  checkScheduleAlerts()
  scheduleInterval = setInterval(checkScheduleAlerts, 1000)
})

onUnmounted(() => {
  if (scheduleInterval) clearInterval(scheduleInterval)
})
</script>

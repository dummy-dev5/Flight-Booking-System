<template>
  <div class="min-h-screen py-10 px-4 sm:px-8">
    <div class="max-w-3xl mx-auto space-y-6">

      <!-- Header -->
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-[#FF579A]/10 rounded-2xl flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#FF579A]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div>
          <h2 class="text-2xl font-black text-slate-800 tracking-tight">Profile Settings</h2>
          <p class="text-sm text-slate-500 font-medium">Manage your account information and preferences.</p>
        </div>
      </div>

      <div class="bg-white shadow-sm rounded-2xl overflow-hidden border border-gray-100">
        <!-- Tabs -->
        <div class="border-b border-gray-100 px-6">
          <nav class="flex gap-1 -mb-px">
            <button
              v-for="tab in currentTabs"
              :key="tab.name"
              @click="activeTab = tab.name"
              :class="[
                'flex items-center gap-2 py-4 px-3 text-sm font-semibold border-b-2 transition-all',
                activeTab === tab.name
                  ? 'border-[#FF579A] text-[#FF579A]'
                  : 'border-transparent text-slate-400 hover:text-slate-600 hover:border-slate-300',
              ]"
            >
              <component :is="'svg'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" v-html="tab.icon"></component>
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- ─── Personal Details Tab ─── -->
        <div v-if="activeTab === 'details'" class="p-6 space-y-6">

          <!-- Avatar Section -->
          <div class="flex items-center gap-5 p-4 bg-slate-50 rounded-xl border border-slate-100">
            <div class="relative group cursor-pointer flex-shrink-0" @click="$refs.fileInput.click()">
              <div class="w-20 h-20 rounded-2xl overflow-hidden bg-pink-100 border-2 border-white shadow-sm flex items-center justify-center">
                <img
                  v-if="displayAvatar"
                  :src="displayAvatar"
                  alt="Avatar"
                  class="w-full h-full object-cover"
                />
                <span v-else class="text-[#FF579A] text-2xl font-black">
                  {{ initials }}
                </span>
              </div>
              <div class="absolute inset-0 bg-black/40 rounded-2xl flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
            </div>
            <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleFileChange" />
            <div>
              <h3 class="text-sm font-bold text-slate-800">Profile Photo</h3>
              <p class="text-xs text-slate-500 mt-0.5">Click the photo to upload a new one. JPG, GIF or PNG · Max 2MB.</p>
              <button v-if="previewAvatar" @click="previewAvatar = null; selectedFile = null" class="mt-2 text-xs text-red-400 hover:text-red-600 font-semibold">Remove new photo</button>
            </div>
          </div>

          <!-- Form Fields -->
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1.5 uppercase tracking-wide">First Name</label>
              <input
                v-model="form.first_name"
                type="text"
                class="block w-full border border-gray-200 rounded-xl shadow-sm py-2.5 px-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#FF579A]/30 focus:border-[#FF579A] transition-all"
                placeholder="First name"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1.5 uppercase tracking-wide">Last Name</label>
              <input
                v-model="form.last_name"
                type="text"
                class="block w-full border border-gray-200 rounded-xl shadow-sm py-2.5 px-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#FF579A]/30 focus:border-[#FF579A] transition-all"
                placeholder="Last name"
              />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-bold text-slate-600 mb-1.5 uppercase tracking-wide">Email Address</label>
              <input
                v-model="form.email"
                type="email"
                class="block w-full border border-gray-200 rounded-xl shadow-sm py-2.5 px-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#FF579A]/30 focus:border-[#FF579A] transition-all"
                placeholder="email@example.com"
              />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-bold text-slate-600 mb-1.5 uppercase tracking-wide">
                Username
                <span class="ml-1.5 text-[9px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded-full normal-case font-semibold tracking-normal">Read Only</span>
              </label>
              <input
                v-model="form.username"
                type="text"
                readonly
                class="block w-full bg-slate-50 border border-gray-200 rounded-xl py-2.5 px-3.5 text-sm text-slate-400 cursor-not-allowed"
              />
            </div>
          </div>

          <div class="flex justify-end pt-2">
            <button
              @click="saveProfile"
              :disabled="loading"
              class="inline-flex items-center gap-2 justify-center py-2.5 px-6 border border-transparent shadow-sm text-sm font-bold rounded-xl text-white bg-[#FF579A] hover:bg-[#e04d8b] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FF579A] disabled:opacity-50 transition-all"
            >
              <svg v-if="loading" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>

        <!-- ─── Security Tab ─── -->
        <div v-if="activeTab === 'security'" class="p-6 space-y-5">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-9 h-9 bg-slate-100 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-bold text-slate-800">Change Password</h3>
              <p class="text-xs text-slate-500">After update, your current session will remain active.</p>
            </div>
          </div>

          <div class="space-y-4 max-w-sm">
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1.5 uppercase tracking-wide">New Password</label>
              <div class="relative">
                <input
                  v-model="passwordForm.newPassword"
                  :type="showNewPwd ? 'text' : 'password'"
                  placeholder="At least 8 characters"
                  class="block w-full border border-gray-200 rounded-xl shadow-sm py-2.5 px-3.5 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-[#FF579A]/30 focus:border-[#FF579A] transition-all"
                />
                <button type="button" @click="showNewPwd = !showNewPwd" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  <svg v-if="!showNewPwd" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                </button>
              </div>
              <!-- Strength Indicator -->
              <div v-if="passwordForm.newPassword" class="mt-2 flex gap-1">
                <div v-for="i in 4" :key="i" :class="['h-1 flex-1 rounded-full transition-colors', i <= passwordStrength ? strengthColor : 'bg-slate-100']"></div>
              </div>
              <p v-if="passwordForm.newPassword" class="text-[10px] font-semibold mt-1" :class="strengthTextColor">{{ strengthLabel }}</p>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1.5 uppercase tracking-wide">Confirm New Password</label>
              <div class="relative">
                <input
                  v-model="passwordForm.confirmPassword"
                  :type="showConfirmPwd ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="block w-full border border-gray-200 rounded-xl shadow-sm py-2.5 px-3.5 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-[#FF579A]/30 focus:border-[#FF579A] transition-all"
                  :class="{ 'border-red-300 focus:border-red-400 focus:ring-red-200': passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword }"
                />
                <button type="button" @click="showConfirmPwd = !showConfirmPwd" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  <svg v-if="!showConfirmPwd" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                </button>
              </div>
              <p v-if="passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword" class="text-[11px] text-red-500 font-semibold mt-1">Passwords do not match.</p>
              <p v-else-if="passwordForm.confirmPassword && passwordForm.newPassword === passwordForm.confirmPassword" class="text-[11px] text-emerald-500 font-semibold mt-1">✓ Passwords match.</p>
            </div>
          </div>

          <div class="flex justify-end pt-2">
            <button
              @click="updatePassword"
              :disabled="loading || !passwordForm.newPassword || !passwordForm.confirmPassword || passwordForm.newPassword !== passwordForm.confirmPassword"
              class="inline-flex items-center gap-2 justify-center py-2.5 px-6 border border-transparent shadow-sm text-sm font-bold rounded-xl text-white bg-[#FF579A] hover:bg-[#e04d8b] focus:outline-none disabled:opacity-50 transition-all"
            >
              <svg v-if="loading" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Updating...' : 'Update Password' }}
            </button>
          </div>
        </div>

        <!-- ─── Instructor Info Tab ─── -->
        <div v-if="activeTab === 'instructor'" class="p-6 space-y-6">
          <!-- Loading state -->
          <div v-if="instructorInfoLoading" class="flex items-center justify-center py-10">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#FF579A]"></div>
          </div>

          <template v-else>
            <!-- Stats Row -->
            <div class="grid grid-cols-3 gap-3">
              <div class="bg-slate-50 rounded-xl p-4 text-center border border-slate-100">
                <p class="text-2xl font-black text-[#FF579A]">{{ instructorStats.totalSections }}</p>
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mt-0.5">Sections</p>
              </div>
              <div class="bg-slate-50 rounded-xl p-4 text-center border border-slate-100">
                <p class="text-2xl font-black text-[#FF579A]">{{ instructorStats.totalStudents }}</p>
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mt-0.5">Students</p>
              </div>
              <div class="bg-slate-50 rounded-xl p-4 text-center border border-slate-100">
                <p class="text-2xl font-black text-[#FF579A]">{{ instructorStats.totalActivities }}</p>
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mt-0.5">Activities</p>
              </div>
            </div>

            <!-- Section Cards -->
            <div>
              <h3 class="text-xs font-black text-slate-500 uppercase tracking-widest mb-3">My Sections</h3>
              <div v-if="instructorSections.length === 0" class="text-center py-8 text-slate-400 text-sm">No sections yet.</div>
              <div class="space-y-2">
                <div
                  v-for="section in instructorSections"
                  :key="section.id"
                  class="flex items-center gap-4 p-4 bg-slate-50 border border-slate-100 rounded-xl hover:border-[#FF579A]/20 hover:bg-[#FF579A]/5 transition-all cursor-pointer group"
                  @click="goToSection(section.id)"
                >
                  <div class="w-10 h-10 rounded-xl bg-[#FF579A]/10 flex items-center justify-center text-[#FF579A] font-black text-sm flex-shrink-0 group-hover:bg-[#FF579A] group-hover:text-white transition-colors">
                    {{ section.section_name?.charAt(0)?.toUpperCase() }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-slate-800 truncate">{{ section.section_name }}</p>
                    <p class="text-[11px] text-slate-500 truncate">{{ section.section_code }} · {{ section.semester }} · {{ section.academic_year }}</p>
                  </div>
                  <div class="flex flex-col items-end gap-1">
                    <span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-bold">{{ section.enrolled_count || 0 }} students</span>
                    <span :class="['text-[9px] px-2 py-0.5 rounded-full font-black uppercase tracking-wide', section.is_active ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-400']">
                      {{ section.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-300 group-hover:text-[#FF579A] flex-shrink-0 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <polyline points="9 18 15 12 9 6"/>
                  </svg>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- ─── Enrollment Tab (Students only) ─── -->
        <div v-if="activeTab === 'enrollment'" class="p-6 space-y-6">
          <div class="flex items-center gap-3 mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#FF579A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <h3 class="text-lg font-medium text-gray-900">Section Enrollment</h3>
            <span class="ml-auto inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-100">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Active
            </span>
          </div>
          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
            <div class="sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Section Name</label>
              <input :value="section.section_name" type="text" readonly class="mt-1 block w-full bg-gray-50 border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-600 sm:text-sm cursor-default" />
            </div>
            <div class="sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Section Code</label>
              <input :value="section.section_code" type="text" readonly class="mt-1 block w-full bg-gray-50 border border-gray-300 rounded-md shadow-sm py-2 px-3 text-pink-700 font-bold sm:text-sm cursor-default tracking-widest" />
            </div>
            <div v-if="section.semester" class="sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Semester</label>
              <input :value="section.semester" type="text" readonly class="mt-1 block w-full bg-gray-50 border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-600 sm:text-sm cursor-default" />
            </div>
            <div v-if="section.academic_year" class="sm:col-span-3">
              <label class="block text-sm font-medium text-gray-700">Academic Year</label>
              <input :value="section.academic_year" type="text" readonly class="mt-1 block w-full bg-gray-50 border border-gray-300 rounded-md shadow-sm py-2 px-3 text-gray-600 sm:text-sm cursor-default" />
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notification'
import { useUserStore } from '@/stores/user'
import api from '@/services/api/axios'

const props = defineProps({
  section: {
    type: Object,
    default: null
  }
})

const router = useRouter()
const notificationStore = useNotificationStore()
const userStore = useUserStore()

const activeTab = ref('details')
const loading = ref(false)
const previewAvatar = ref(null)
const selectedFile = ref(null)
const showNewPwd = ref(false)
const showConfirmPwd = ref(false)

// Instructor info state
const instructorInfoLoading = ref(false)
const instructorSections = ref([])

// Detect role
const isInstructor = computed(() => userStore.role === 'instructor' || userStore.user?.role === 'instructor')

const currentTabs = computed(() => {
  const tabs = [
    {
      name: 'details',
      label: 'Personal Details',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />'
    },
    {
      name: 'security',
      label: 'Security',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />'
    },
  ]
  if (isInstructor.value) {
    tabs.push({
      name: 'instructor',
      label: 'Teaching Info',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />'
    })
  }
  if (props.section) {
    tabs.push({
      name: 'enrollment',
      label: 'My Enrollment',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />'
    })
  }
  return tabs
})

const form = ref({ username: '', first_name: '', last_name: '', email: '', avatar: null })
const passwordForm = ref({ newPassword: '', confirmPassword: '' })

const initials = computed(() => {
  const f = form.value.first_name?.charAt(0) || ''
  const l = form.value.last_name?.charAt(0) || ''
  return (f + l).toUpperCase()
})

const displayAvatar = computed(() => {
  if (previewAvatar.value) return previewAvatar.value
  if (!form.value.avatar) return null
  if (form.value.avatar.startsWith('http')) return form.value.avatar
  const baseURL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : 'https://fbs-backend-production.up.railway.app')
  return `${baseURL}${form.value.avatar}`
})

// Password strength logic
const passwordStrength = computed(() => {
  const p = passwordForm.value.newPassword
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  return score
})

const strengthColor = computed(() => {
  const s = passwordStrength.value
  if (s <= 1) return 'bg-red-400'
  if (s === 2) return 'bg-orange-400'
  if (s === 3) return 'bg-yellow-400'
  return 'bg-emerald-500'
})

const strengthTextColor = computed(() => {
  const s = passwordStrength.value
  if (s <= 1) return 'text-red-500'
  if (s === 2) return 'text-orange-500'
  if (s === 3) return 'text-yellow-600'
  return 'text-emerald-600'
})

const strengthLabel = computed(() => {
  const s = passwordStrength.value
  if (s <= 1) return 'Weak password'
  if (s === 2) return 'Fair password'
  if (s === 3) return 'Good password'
  return 'Strong password ✓'
})

// Instructor stats
const instructorStats = computed(() => ({
  totalSections: instructorSections.value.length,
  totalStudents: instructorSections.value.reduce((t, s) => t + (s.enrolled_count || 0), 0),
  totalActivities: instructorSections.value.reduce((t, s) => t + (s.activity_count || 0), 0)
}))

const parsedSchedules = computed(() => {
  if (!props.section?.schedule) return []
  try {
    const s = typeof props.section.schedule === 'string' ? JSON.parse(props.section.schedule) : props.section.schedule
    return Array.isArray(s) ? s : []
  } catch { return [] }
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

const goToSection = (id) => {
  router.push(`/instructor/section/${id}`)
}

const fetchProfile = async () => {
  loading.value = true
  try {
    const response = await api.get('api/profile/update/')
    const data = response.data
    form.value = {
      username: data.username,
      first_name: data.first_name,
      last_name: data.last_name,
      email: data.email,
      avatar: data.avatar
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
    notificationStore.error('Failed to load profile data.')
  } finally {
    loading.value = false
  }
}

const fetchInstructorSections = async () => {
  if (!isInstructor.value) return
  instructorInfoLoading.value = true
  try {
    const response = await api.get('api/instructor/dashboard/')
    instructorSections.value = response.data.sections || []
  } catch (error) {
    console.error('Failed to fetch instructor sections:', error)
  } finally {
    instructorInfoLoading.value = false
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) {
    notificationStore.warn('Image size should be less than 2MB.')
    return
  }
  selectedFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => { previewAvatar.value = e.target.result }
  reader.readAsDataURL(file)
}

const saveProfile = async () => {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('first_name', form.value.first_name)
    formData.append('last_name', form.value.last_name)
    formData.append('email', form.value.email)
    if (selectedFile.value) formData.append('avatar', selectedFile.value)

    const response = await api.patch('api/profile/update/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    const data = response.data
    form.value = {
      username: data.username,
      first_name: data.first_name,
      last_name: data.last_name,
      email: data.email,
      avatar: data.avatar
    }
    // Update store
    if (userStore.user) {
      userStore.user.first_name = data.first_name
      userStore.user.last_name = data.last_name
      userStore.user.avatar = data.avatar
    }
    selectedFile.value = null
    previewAvatar.value = null
    notificationStore.success('Profile updated successfully!')
  } catch (error) {
    console.error('Update failed:', error)
    notificationStore.error('Failed to update profile. Please try again.')
  } finally {
    loading.value = false
  }
}

const updatePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    notificationStore.error('Passwords do not match.')
    return
  }
  if (passwordForm.value.newPassword.length < 8) {
    notificationStore.warn('Password must be at least 8 characters long.')
    return
  }
  loading.value = true
  try {
    await api.patch('api/profile/update/', { new_password: passwordForm.value.newPassword })
    notificationStore.success('Password updated successfully!')
    passwordForm.value.newPassword = ''
    passwordForm.value.confirmPassword = ''
  } catch (error) {
    console.error('Password update failed:', error)
    notificationStore.error(error.response?.data?.error || 'Failed to update password.')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchProfile()
  if (isInstructor.value) {
    await fetchInstructorSections()
  }
})
</script>

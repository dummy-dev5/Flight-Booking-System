<template>
  <div class="bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden max-w-4xl w-full">
    <!-- Header -->
    <div class="bg-pink-500 p-4 flex justify-between items-center text-white">
      <div class="flex items-center gap-3">
        <svg class="w-6 h-6 border-2 border-white rounded-full p-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <h2 class="text-xl font-bold uppercase tracking-wider italic">Low Fare Calendar</h2>
      </div>
      <div class="flex items-center gap-4">
        <div class="flex items-center bg-white/20 rounded-full px-3 py-1">
          <button @click="prevMonth" class="hover:text-pink-200 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7m0 0l7-7" />
            </svg>
          </button>
          <span class="mx-4 font-bold min-w-[120px] text-center uppercase tracking-widest text-sm">
            {{ currentMonthName }} {{ currentYear }}
          </span>
          <button @click="nextMonth" class="hover:text-pink-200 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
        <button @click="$emit('close')" class="text-white/80 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Route Info & Legend -->
    <div class="p-4 bg-gray-50 border-b border-gray-200 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="text-xs font-bold text-gray-500 uppercase tracking-widest">Route:</div>
        <div class="flex items-center gap-2">
          <span class="text-lg font-black text-gray-800">{{ origin }}</span>
          <svg class="w-4 h-4 text-pink-500 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
          <span class="text-lg font-black text-gray-800">{{ destination }}</span>
        </div>
      </div>
      
      <div class="flex items-center gap-4 text-[10px] font-bold uppercase tracking-tight">
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 bg-green-500 rounded-sm"></div>
          <span class="text-green-700">Cheapest</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 bg-pink-500 rounded-sm shadow-sm"></div>
          <span class="text-pink-700">Selected</span>
        </div>
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 bg-gray-200 rounded-sm"></div>
          <span class="text-gray-400">Not Available</span>
        </div>
      </div>
    </div>

    <!-- Calendar Grid -->
    <div class="p-4 lg:p-6 bg-white relative min-h-[400px]">
      <!-- Loading Overlay -->
      <div v-if="loading" class="absolute inset-0 bg-white/80 z-20 flex flex-col items-center justify-center backdrop-blur-sm">
        <div class="w-12 h-12 border-4 border-pink-200 border-t-pink-500 rounded-full animate-spin mb-4"></div>
        <div class="text-pink-600 font-black tracking-widest uppercase animate-pulse text-sm">Hunting for Low Fares...</div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-4 text-center">
        {{ error }}
        <button @click="fetchMonthPrices" class="ml-2 underline font-bold">Retry</button>
      </div>

      <!-- Days Header -->
      <div class="grid grid-cols-7 gap-1 lg:gap-2 mb-2">
        <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" 
          class="text-center text-[10px] font-black text-gray-400 uppercase tracking-widest py-2">
          {{ day }}
        </div>
      </div>

      <!-- Calendar Body -->
      <div class="grid grid-cols-7 gap-1 lg:gap-2">
        <!-- Empty slots for previous month -->
        <div v-for="n in firstDayOfMonth" :key="'empty-'+n" class="aspect-square bg-gray-50/50 rounded-sm lg:rounded-md"></div>
        
        <!-- Day cards -->
        <div 
          v-for="day in calendarDays" 
          :key="day.date"
          @click="selectDate(day)"
          :class="[
            'aspect-square relative rounded-sm lg:rounded-md border p-1 lg:p-2 transition-all duration-200 cursor-pointer flex flex-col justify-between overflow-hidden group',
            !day.available ? 'bg-gray-50 border-gray-100 cursor-not-allowed grayscale' : 'hover:shadow-lg hover:-translate-y-1',
            day.isToday ? 'border-pink-200 ring-1 ring-pink-100 ring-inset' : 'border-gray-100',
            day.isSelected ? 'bg-pink-500 border-pink-600 shadow-pink-200 text-white z-10 scale-105' : 'bg-white hover:border-pink-300',
            day.isLowest && !day.isSelected ? 'bg-green-50 border-green-200' : ''
          ]"
        >
          <!-- Day Number -->
          <div class="flex justify-between items-start">
            <span :class="['text-[11px] lg:text-sm font-black', day.isSelected ? 'text-white' : 'text-gray-400']">
              {{ day.dayNumber }}
            </span>
            <div v-if="day.isToday && !day.isSelected" class="w-1.5 h-1.5 bg-pink-500 rounded-full"></div>
            <div v-if="day.isLowest && !day.isSelected" class="text-[8px] bg-green-500 text-white px-1 rounded-full font-bold uppercase py-0.5">
              Low
            </div>
          </div>

          <!-- Price -->
          <div v-if="day.available" class="text-center">
            <div :class="['text-[11px] lg:text-base font-black tracking-tight', 
              day.isSelected ? 'text-white' : (day.isLowest ? 'text-green-600' : 'text-gray-800')
            ]">
              <span class="text-[9px] lg:text-xs">₱</span>{{ day.price.toLocaleString() }}
            </div>
          </div>
          <div v-else class="text-center opacity-30">
             <div class="h-0.5 w-4 bg-gray-300 mx-auto"></div>
          </div>

          <!-- Highlight Bar -->
          <div v-if="day.isSelected" class="absolute bottom-0 left-0 w-full h-1 bg-white/30"></div>
          <div v-else-if="day.isLowest" class="absolute bottom-0 left-0 w-full h-0.5 bg-green-500/20 group-hover:bg-green-500/50 transition-colors"></div>
        </div>
      </div>
    </div>

    <!-- Footer Action -->
    <div class="p-6 bg-gray-50 border-t border-gray-200 flex flex-col sm:flex-row justify-between items-center gap-4">
      <div v-if="selectedDay" class="flex items-center gap-4">
        <div class="text-sm font-medium text-gray-500">Selected Departure:</div>
        <div class="px-3 py-1.5 bg-white border-2 border-pink-500 rounded-lg shadow-sm">
          <span class="font-black text-gray-800 uppercase tracking-widest text-sm">
            {{ formatFullDate(selectedDay.date) }}
          </span>
        </div>
      </div>
      <div v-else class="text-sm italic text-gray-400">
        Choose a date with a price to continue...
      </div>
      
      <button 
        @click="confirmDate"
        :disabled="!selectedDay || !selectedDay.available"
        :class="[
          'px-8 py-3 rounded-md font-black uppercase tracking-widest text-sm shadow-xl transition-all active:scale-95',
          selectedDay && selectedDay.available 
            ? 'bg-pink-500 text-white hover:bg-pink-600 shadow-pink-200' 
            : 'bg-gray-200 text-gray-400 cursor-not-allowed shadow-none'
        ]"
      >
        Select this flight
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import api from '@/services/api/axios';

const props = defineProps({
  origin: String,
  destination: String,
  initialDate: {
    type: String,
    default: () => new Date().toISOString().split('T')[0]
  }
});

const emit = defineEmits(['close', 'select']);

const currentYear = ref(new Date(props.initialDate).getFullYear());
const currentMonth = ref(new Date(props.initialDate).getMonth());
const loading = ref(false);
const error = ref(null);
const prices = ref([]);
const selectedDate = ref(props.initialDate);

// Computed month properties
const currentMonthName = computed(() => {
  return new Intl.DateTimeFormat('en-US', { month: 'long' }).format(new Date(currentYear.value, currentMonth.value));
});

const firstDayOfMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value, 1).getDay();
});

const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate();
});

const lowestPrice = computed(() => {
  const availablePrices = prices.value.filter(p => p.available && p.price).map(p => p.price);
  return availablePrices.length ? Math.min(...availablePrices) : null;
});

const calendarDays = computed(() => {
  const days = [];
  const today = new Date().toISOString().split('T')[0];

  for (let d = 1; d <= daysInMonth.value; d++) {
    const dateStr = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    const priceData = prices.value.find(p => p.date === dateStr);
    
    days.push({
      date: dateStr,
      dayNumber: d,
      price: priceData?.price || null,
      available: priceData?.available || false,
      isToday: dateStr === today,
      isSelected: dateStr === selectedDate.value,
      isLowest: priceData?.available && priceData?.price && priceData.price === lowestPrice.value
    });
  }
  return days;
});

const selectedDay = computed(() => {
  return calendarDays.value.find(d => d.isSelected);
});

// Methods
const fetchMonthPrices = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const startDate = new Date(currentYear.value, currentMonth.value, 1).toISOString().split('T')[0];
    const endDate = new Date(currentYear.value, currentMonth.value + 1, 0).toISOString().split('T')[0];
    
    const response = await api.get('flightapp/api/schedules/price-calendar/', {
      params: {
        origin: props.origin,
        destination: props.destination,
        start_date: startDate,
        end_date: endDate
      }
    });
    
    if (response.data.success) {
      prices.value = response.data.calendar;
    } else {
      error.value = "Failed to load low fares.";
    }
  } catch (err) {
    console.error("Price calendar error:", err);
    error.value = "Unable to connect to service.";
  } finally {
    loading.value = false;
  }
};

const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value--;
  } else {
    currentMonth.value--;
  }
  fetchMonthPrices();
};

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value++;
  } else {
    currentMonth.value++;
  }
  fetchMonthPrices();
};

const selectDate = (day) => {
  if (day.available) {
    selectedDate.value = day.date;
  }
};

const confirmDate = () => {
  if (selectedDay.value && selectedDay.value.available) {
    emit('select', selectedDay.value.date);
  }
};

const formatFullDate = (dateStr) => {
  return new Intl.DateTimeFormat('en-US', { 
    weekday: 'short', 
    month: 'long', 
    day: 'numeric',
    year: 'numeric'
  }).format(new Date(dateStr));
};

onMounted(() => {
  fetchMonthPrices();
});

watch([() => props.origin, () => props.destination], () => {
  fetchMonthPrices();
});
</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse-slow {
  animation: pulse-slow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>

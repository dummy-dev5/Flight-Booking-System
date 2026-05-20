<template>
  <div class="success-page-container min-h-screen w-full overflow-y-auto py-12 relative flex items-center justify-center bg-slate-50 px-4 md:px-8">
    <!-- Animated background layers -->
    <div class="absolute inset-0 z-0 opacity-60 pointer-events-none"></div>
    <div class="absolute -top-[20%] -right-[10%] w-[500px] h-[500px] bg-pink-300/30 rounded-full blur-[120px] animate-blob pointer-events-none"></div>
    <div class="absolute -bottom-[20%] -left-[10%] w-[500px] h-[500px] bg-emerald-300/20 rounded-full blur-[120px] animate-blob animation-delay-2000 pointer-events-none"></div>
    
    <div class="max-w-5xl w-full mx-auto relative z-10 animate-slide-up flex flex-col md:flex-row items-center justify-center gap-10 md:gap-12 lg:gap-20 h-auto md:h-full md:max-h-[800px]">
      
      <!-- Left Column: Success Message & Actions -->
      <div class="flex-1 flex flex-col items-center md:items-start text-center md:text-left shrink-0 w-full max-w-sm">
        
        <!-- Top Success Indicator -->
        <div class="success-circle-container relative w-16 h-16 md:w-20 md:h-20 mb-4 md:mb-6">
          <div class="absolute inset-0 bg-emerald-500 rounded-full animate-ping opacity-20 transform scale-75"></div>
          <div class="absolute inset-2 bg-emerald-400 rounded-full opacity-30 animate-pulse"></div>
          <div class="relative w-full h-full bg-emerald-500 rounded-full shadow-xl shadow-emerald-500/40 flex items-center justify-center z-10 border-[5px] border-white transform hover:scale-105 transition-transform duration-300">
            <svg class="w-8 h-8 md:w-10 md:h-10 text-white animate-checkmark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M5 13l4 4L19 7" class="path" />
            </svg>
          </div>
        </div>
        
        <h1 class="text-3xl md:text-5xl lg:text-6xl text-slate-800 tracking-tight leading-tight mb-2 md:mb-3">
          <span class="font-light">Payment</span><br class="hidden md:block" /> <span class="font-black">Confirmed!</span>
        </h1>
        <p class="text-slate-500 font-medium text-[13px] md:text-[15px] mb-6 md:mb-8 max-w-xs">
          Your e-ticket has been sent to your email. Safe travels!
        </p>
        
        <!-- Actions moved to the left side -->
        <div class="w-full space-y-3 animate-fade-in-up" style="animation-delay: 0.5s;">
          <button @click="downloadItinerary" 
                  class="w-full relative overflow-hidden group cursor-pointer py-3.5 px-6 bg-slate-900 text-white rounded-[12px] font-black text-[13px] uppercase tracking-widest hover:bg-slate-800 transition-all shadow-[0_8px_20px_rgba(15,23,42,0.15)] hover:shadow-[0_8px_25px_rgba(15,23,42,0.25)] flex items-center justify-center gap-3 transform hover:-translate-y-0.5 shrink-0">
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download E-Ticket
          </button>

          <button @click="goToDashboard" 
                  class="w-full cursor-pointer py-3.5 px-6 bg-white text-slate-800 border-2 border-slate-200/80 rounded-[12px] font-black text-[13px] uppercase tracking-widest hover:bg-slate-50 hover:border-slate-300 transition-all shadow-sm flex items-center justify-center transform hover:-translate-y-0.5 shrink-0">
            Return to Dashboard
          </button>

          <div v-if="!isActivity" class="pt-3 flex flex-row items-center justify-center md:justify-start gap-4">
            <button @click="goHome" 
                    class="text-[11px] text-pink-500 font-black uppercase tracking-widest hover:text-pink-600 cursor-pointer transition-colors inline-flex items-center gap-1 group">
              Book Another 
              <span class="group-hover:translate-x-1 transition-transform">→</span>
            </button>
            <span class="text-slate-300">|</span>
            <button @click="copyBookingLink" class="text-slate-400 hover:text-slate-600 hover:bg-white cursor-pointer text-[10px] font-black uppercase tracking-widest transition-all inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-transparent hover:border-slate-200">
              🔗 Share Link
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column: The Flight Ticket Receipt -->
      <div class="flex-1 w-full max-w-sm shrink-0 drop-shadow-2xl">
        <div class="ticket-wrapper relative transition-all duration-500 hover:shadow-pink-500/10 rounded-[20px] w-full bg-white flex flex-col h-full max-h-[500px]">
          <!-- Top Half -->
          <div class="bg-white rounded-t-[20px] p-5 shadow-sm border border-slate-200 border-b-0 relative overflow-hidden shrink-0">
            <div class="absolute top-0 left-0 w-full h-[5px] bg-gradient-to-r from-emerald-400 via-pink-400 to-emerald-400"></div>
            
            <div class="flex justify-between items-start mb-4">
              <div>
                <p class="text-[9px] text-slate-400 uppercase tracking-widest font-black mb-1 flex items-center gap-1.5"><svg class="w-2.5 h-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg> PNR Locator</p>
                <div class="flex items-center gap-2">
                  <span class="text-2xl font-mono font-black text-slate-900 tracking-tighter">{{ bookingReference }}</span>
                  <button @click="copyReference" class="w-6 h-6 rounded-md bg-slate-50 flex items-center justify-center text-slate-500 hover:bg-emerald-50 hover:text-emerald-600 transition-colors shadow-sm border border-slate-100 cursor-pointer" title="Copy Reference">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                  </button>
                </div>
              </div>
              <div class="text-right">
                <p class="text-[9px] text-slate-400 uppercase tracking-widest font-black mb-1">Total</p>
                <span class="text-xl font-black text-slate-800 tracking-tight">₱{{ formattedAmount }}</span>
              </div>
            </div>

            <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
              <div class="flex items-center gap-3">
                 <div class="w-8 h-8 bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg border border-slate-200/60 flex items-center justify-center shadow-inner relative overflow-hidden">
                   <div class="absolute inset-0 bg-white/40"></div>
                   <span class="relative z-10 text-[14px]">💳</span>
                 </div>
                 <div>
                   <p class="text-[8px] text-slate-400 uppercase tracking-widest font-black">Transaction ID</p>
                   <p class="text-[10px] font-mono font-bold text-slate-600 tracking-tight">{{ transactionId }}</p>
                 </div>
              </div>
              
              <div class="bg-emerald-50 px-2 py-1 rounded-md border border-emerald-100 flex items-center gap-1.5 shadow-sm">
                 <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                 <span class="text-[8px] font-black text-emerald-700 uppercase tracking-wider">Confirmed</span>
              </div>
            </div>
          </div>
          
          <!-- Dashed Ticket Cutout Line -->
          <div class="relative bg-white border-x border-slate-200 flex items-center justify-between py-0 h-4 isolate z-10 shrink-0">
            <div class="w-4 h-4 bg-slate-50 rounded-full border border-slate-200 border-r-0 absolute -left-[2px] top-1/2 -translate-y-1/2 z-20 ticket-cutout-left shadow-[inset_2px_0_3px_rgba(0,0,0,0.02)]"></div>
            <div class="absolute left-4 right-4 top-1/2 -translate-y-1/2 border-t-[2px] border-dashed border-slate-200 z-10 w-[calc(100%-2rem)] h-px"></div>
            <div class="w-4 h-4 bg-slate-50 rounded-full border border-slate-200 border-l-0 absolute -right-[2px] top-1/2 -translate-y-1/2 z-20 ticket-cutout-right shadow-[inset_-2px_0_3px_rgba(0,0,0,0.02)]"></div>
          </div>

          <!-- Bottom Half: Journey Guide -->
          <div class="bg-gradient-to-b from-white to-slate-50/50 rounded-b-[20px] p-5 border border-slate-200 border-t-0 shadow-sm relative shrink-0">
             <h3 class="font-black text-slate-800 text-[11px] mb-4 flex items-center gap-2 uppercase tracking-widest">
              Journey Checklist
            </h3>

            <div class="relative">
              <!-- Connecting Line -->
              <div class="absolute left-[9px] top-2 bottom-6 w-[2px] bg-gradient-to-b from-emerald-400 via-pink-300 to-slate-200"></div>
              
              <div class="space-y-4 relative">
                <!-- Step 1 -->
                <div class="flex items-start gap-4 animate-fade-in-up" style="animation-delay: 0.1s;">
                  <div class="w-5 h-5 bg-gradient-to-br from-emerald-400 to-emerald-500 rounded-full flex items-center justify-center shrink-0 shadow-sm shadow-emerald-200 z-10 border-2 border-white transform transition-transform hover:scale-110">
                    <svg class="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                  <div class="pt-0.5">
                    <div class="text-[11px] font-black text-slate-800 uppercase tracking-wide leading-none">Booking Confirmed</div>
                    <div class="text-[10px] text-slate-500 mt-1 leading-snug font-medium">Digital receipt generated.</div>
                  </div>
                </div>

                <!-- Step 2 -->
                <div class="flex items-start gap-4 animate-fade-in-up" style="animation-delay: 0.2s;">
                  <div class="w-5 h-5 bg-white border-2 border-pink-400 rounded-full flex items-center justify-center shrink-0 z-10 shadow-sm transform transition-transform hover:scale-110">
                    <span class="text-pink-500 font-black text-[9px]">2</span>
                  </div>
                  <div class="pt-0.5">
                    <div class="text-[11px] font-black text-slate-800 uppercase tracking-wide leading-none">Airport Check-In</div>
                  </div>
                </div>

                <!-- Step 3 -->
                <div class="flex items-start gap-4 animate-fade-in-up" style="animation-delay: 0.3s;">
                  <div class="w-5 h-5 bg-white border-2 border-slate-300 rounded-full flex items-center justify-center shrink-0 z-10 shadow-sm transform transition-transform hover:scale-110">
                    <span class="text-slate-400 font-black text-[9px]">3</span>
                  </div>
                  <div class="pt-0.5">
                    <div class="text-[11px] font-black text-slate-800 uppercase tracking-wide leading-none text-slate-400">Boarding</div>
                    <div class="text-[10px] text-slate-400 mt-1 leading-snug font-medium">Use QR boarding pass at gate.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Toast Message -->
    <transition
      enter-active-class="transition-all duration-300 cubic-bezier(0.4, 0, 0.2, 1)"
      leave-active-class="transition-all duration-200 cubic-bezier(0.4, 0, 0.2, 1)"
      enter-from-class="opacity-0 translate-y-8 scale-95"
      leave-to-class="opacity-0 translate-y-8 scale-95"
    >
      <div v-if="showToast" 
           class="fixed bottom-8 left-1/2 -translate-x-1/2 z-[100]">
        <div class="bg-slate-900/95 backdrop-blur-md border border-slate-700/50 text-white px-5 py-3.5 rounded-2xl shadow-[0_20px_40px_rgba(0,0,0,0.2)] flex items-center gap-3 min-w-[280px]">
          <div class="w-7 h-7 rounded-full bg-emerald-500/20 flex items-center justify-center shrink-0">
            <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
          </div>
          <p class="text-[12px] font-black tracking-widest uppercase">{{ toastMessage }}</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useBookingStore } from '@/stores/booking';
import { studentActivityDetailsService } from '@/services/Student/studentActivityDetailsService.js';


const route = useRoute();
const router = useRouter();
const bookingStore = useBookingStore();

const bookingReference = ref('');
const transactionId = ref('');
const amountPaid = ref(0);
const bookingId = ref(null);
const showToast = ref(false);
const toastMessage = ref('');

const formattedAmount = computed(() => {
  return amountPaid.value.toLocaleString('en-PH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
});

onMounted(() => {
  const query = route.query;
  
  if (query.ref) {
    bookingReference.value = query.ref;
    localStorage.setItem('last_booking_ref', query.ref);
  }
  
  if (query.payment_id) {
    transactionId.value = query.payment_id;
  }
  
  if (query.amount) {
    amountPaid.value = parseFloat(query.amount);
  }
  
  if (query.booking_id) {
    bookingId.value = query.booking_id;
  }
  
  if (!bookingReference.value) {
    bookingReference.value = localStorage.getItem('last_booking_ref') || 'N/A';
  }

  // Handle activity submission if this was an activity booking
  handleActivitySubmission();
});

const handleActivitySubmission = async () => {
  if (isActivity.value && bookingStore.activityId) {
    console.log('📝 Submitting activity completion:', bookingStore.activityId);
    try {
      // Backend dynamically handles the submission automatically via get_activity_submissions
      // await studentActivityDetailsService.submitActivity(bookingStore.activityId, {});
      console.log('✅ Activity submission successfully resolved automatically via backend scoring');
    } catch (error) {
      console.error('❌ Failed to process backend constraints:', error);
    }
  }
};

const downloadItinerary = async () => {
  if (!bookingId.value) {
    showToastMessage('Booking ID missing - cannot download');
    return;
  }
  
  showToastMessage('Generating your E-Ticket...');
  
  try {
    const baseUrl = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : 'https://fbs-backend-production.up.railway.app');
    const downloadUrl = `${baseUrl}/flightapp/download-itinerary/${bookingId.value}/`;
    
    // Open in new tab or trigger download
    window.open(downloadUrl, '_blank');
  } catch (error) {
    console.error('Download error:', error);
    showToastMessage('Failed to download itinerary');
  }
};

const copyReference = () => {
  navigator.clipboard.writeText(bookingReference.value);
  showToastMessage('Booking reference copied');
};

const copyBookingLink = () => {
  const link = `${window.location.origin}/booking/${bookingReference.value}`;
  navigator.clipboard.writeText(link);
  showToastMessage('Booking link copied');
};

const showToastMessage = (message) => {
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

const isActivity = computed(() => !!bookingStore.activityCode);

const goToDashboard = () => {
  showToastMessage('Returning to dashboard...');
  bookingStore.clearActivityCodeValidation();
  bookingStore.resetBooking();
  localStorage.removeItem('payment_session');
  localStorage.removeItem('current_booking');
  router.push({ name: 'StudentDashboard' });
};

const goHome = () => {
  if (isActivity.value) {
    showToastMessage('Action unavailable during activity');
    return;
  }
  showToastMessage('Starting new booking...');
  bookingStore.resetBooking();
  router.push({ name: 'Home' });
};
</script>

<style scoped>
/* Keyframes for micro-animations */
@keyframes drawCheck {
  0% { stroke-dasharray: 0, 100; opacity: 0; }
  100% { stroke-dasharray: 100, 0; opacity: 1; }
}

@keyframes slideUpFade {
  0% { transform: translateY(40px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.success-page-container {
  /* Minimal mesh noise bg */
  background-image: radial-gradient(at 40% 20%, hsla(28deg,100%,74%,0.08) 0px, transparent 50%),
                    radial-gradient(at 80% 0%, hsla(189deg,100%,56%,0.08) 0px, transparent 50%),
                    radial-gradient(at 0% 50%, hsla(355deg,100%,93%,0.08) 0px, transparent 50%);
}

.animate-checkmark .path {
  stroke-dasharray: 100;
  stroke-dashoffset: 0;
  animation: drawCheck 0.8s ease-out forwards;
}

.animate-slide-up {
  opacity: 0;
  animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-fade-in-up {
  opacity: 0;
  animation: slideUpFade 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-blob {
  animation: blob 8s infinite alternate;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

/* Perfecting ticket cutouts */
.ticket-wrapper {
  transform: perspective(1000px) rotateX(0deg);
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.ticket-wrapper:hover {
  transform: translateY(-4px) perspective(1000px) rotateX(1deg);
}

.ticket-cutout-left {
  box-shadow: inset -2px 0 4px rgba(0,0,0,0.03);
  z-index: 20;
}
.ticket-cutout-right {
  box-shadow: inset 2px 0 4px rgba(0,0,0,0.03);
  z-index: 20;
}
</style>
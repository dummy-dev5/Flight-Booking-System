import axios from 'axios';

const rawBaseUrl = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : 'https://fbs-vue.onrender.com');
const cleanBaseUrl = rawBaseUrl.endsWith('/') ? rawBaseUrl.slice(0, -1) : rawBaseUrl;

const api = axios.create({
  baseURL: `${cleanBaseUrl}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Automatically add the Token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken'); // Assuming you save it here on login
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
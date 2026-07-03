import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  define: {
    // Provide fallback for process.env references (like process.env.REACT_APP_API_URL)
    'process.env': {
      REACT_APP_API_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000'
    }
  }
});

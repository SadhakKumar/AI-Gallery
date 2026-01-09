import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [["babel-plugin-react-compiler"]],
      },
    }),
  ],
  server: {
    host: true, // important
    port: 5173,
    hmr: {
      protocol: "wss",
      host: "deciduously-prepositional-maranda.ngrok-free.dev",
      clientPort: 443, // 👈 THIS is the key
    },
  },
});

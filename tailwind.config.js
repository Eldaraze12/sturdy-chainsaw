/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./shop/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#fbf4ea",
        surface: "#fffaf3",
        brand: {
          DEFAULT: "#a9603b",
          dark: "#6e3b24",
          soft: "#f3e2d5",
        },
        accent: "#b24c63",
        ink: "#3a2a20",
        muted: "#8a7767",
        border: "#ecdfce",
      },
      fontFamily: {
        display: ["'Playfair Display'", "Georgia", "serif"],
        body: ["'Nunito'", "system-ui", "sans-serif"],
      },
      borderRadius: {
        brand: "16px",
      },
      boxShadow: {
        brand: "0 10px 30px -12px rgba(110, 59, 36, 0.25)",
        "brand-lg": "0 18px 40px -14px rgba(110, 59, 36, 0.35)",
      },
      keyframes: {
        "fade-in-up": {
          "0%": { opacity: 0, transform: "translateY(18px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-8px)" },
        },
        "scale-in": {
          "0%": { opacity: 0, transform: "scale(.92)" },
          "100%": { opacity: 1, transform: "scale(1)" },
        },
        "pulse-dot": {
          "0%, 80%, 100%": { transform: "scale(0.8)", opacity: 0.5 },
          "40%": { transform: "scale(1)", opacity: 1 },
        },
        "gradient-x": {
          "0%, 100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
        },
      },
      animation: {
        "fade-in-up": "fade-in-up .8s cubic-bezier(.16,1,.3,1) both",
        float: "float 4s ease-in-out infinite",
        "scale-in": "scale-in .5s cubic-bezier(.16,1,.3,1) both",
        "pulse-dot": "pulse-dot 1.2s infinite ease-in-out",
        "gradient-x": "gradient-x 6s ease infinite",
      },
    },
  },
  plugins: [],
};

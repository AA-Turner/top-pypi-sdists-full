/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./js/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        dark: {
          ...require("daisyui/src/theming/themes")["dark"],
          primary: "#4F46E5", // Custom primary color
          "primary-focus": "#4338CA", // Darker shade for hover/focus
          "primary-content": "#ffffff", // Text on primary background

          secondary: "#6B7280", // Gray-500
          "secondary-focus": "#4B5563", // Gray-600 for hover
          "secondary-content": "#ffffff", // Text on secondary background

          // Background colors
          "base-100": "#111111", // Darkest - for sidebar
          "base-200": "#1a1a1a", // Dark - for content areas
          "base-300": "#2a2a2a", // Lighter - for borders etc

          // Text colors
          "base-content": "#ffffff", // Primary text color
          "text-base": "#ffffff", // Alternative text color
          "text-muted": "#a3a3a3", // Muted text color
        },
      },
    ],
  },
};

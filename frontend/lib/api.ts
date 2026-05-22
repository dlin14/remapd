/**
 * Single source of truth for the backend API base URL.
 *
 * Development: defaults to http://localhost:8000
 * Production:  set NEXT_PUBLIC_API_URL in Vercel environment variables
 *              (e.g. https://remapd-api.railway.app)
 */
export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

// Service Worker — Cấp Tốc — Toán Cá Chép
// Cache-first strategy cho shell, network-first cho đề thi

const CACHE_NAME = 'cachep-captoc-20260520-v2';
const SHELL_ASSETS = [
  './',
  './index.html',
  './manifest.json',
];

// Install: cache shell assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(SHELL_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate: cleanup old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      );
    })
  );
  self.clients.claim();
});

// Fetch: cache-first for shell, network-first for exams
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Exam files (de/*.html) — always network-first
  if (url.pathname.includes('/de/') || url.pathname.includes('/chuyende/')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Shell assets — cache-first
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      });
    })
  );
});

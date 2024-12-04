// sw.js (Service Worker)
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('my-cache').then((cache) => {
            return cache.addAll([
                '/', // Main HTML file
                '/index.html',
                '/styles.css',
                '/bundle.js',
                '/images/logo.png', // Add other assets
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse; // Serve from cache
            }
            return fetch(event.request); // Fetch from network if not cached
        })
    );
});

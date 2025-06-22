self.addEventListener('install', e => {
  e.waitUntil(
    caches.open('mi-cache').then(cache => {
      return cache.addAll([
        '/',
        '/static/css/styles.css',
        '/static/js/app.js'
      ]);
    })
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(response => response || fetch(e.request))
  );
});


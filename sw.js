/* Service worker SakuArab: halaman dan data bekerja offline.
   Naikkan VERSION setiap kali index.html atau words.json diubah agar cache lama dibuang. */
const VERSION = "sakuarab-20261011-0858";
const CORE = ["./", "index.html", "words.json", "manifest.webmanifest", "icon.svg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const sameOrigin = url.origin === location.origin;
  const isFont = url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com";
  if (!sameOrigin && !isFont) return;
  // words.json & halaman: jaringan dulu supaya revisi kosakata cepat sampai, cache sebagai cadangan offline
  // font: cache dulu karena jarang berubah
  const networkFirst = sameOrigin;
  e.respondWith(
    networkFirst
      ? fetch(req).then(res => { const copy = res.clone(); if (res.ok) caches.open(VERSION).then(c => c.put(req, copy)); return res; })
          .catch(() => caches.match(req).then(r => r || caches.match("index.html")))
      : caches.match(req).then(hit => hit || fetch(req).then(res => { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); return res; }))
  );
});

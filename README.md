# SakuArab · Kamus Saku Arab untuk SMK

> *Arab buat dunia kerja, bukan cuma hafalan.*

**SakuArab** adalah kamus saku digital Bahasa Arab untuk siswa SMK. Kosakatanya disusun menurut **jurusan**: Rekayasa Perangkat Lunak (RPL), Akuntansi, Teknik Bodi Kendaraan Ringan (TBKR), dan Teknik Sepeda Motor (TSM), ditambah kosakata umum dunia kerja.

**Demo:** https://sultanbaguspermadi-a11y.github.io/sakuarab/

## Mengapa dibuat?

Pelajaran Bahasa Arab di SMK sering terasa jauh dari dunia yang sedang dipelajari siswa. Siswa RPL setiap hari berurusan dengan server dan kode, siswa Akuntansi dengan jurnal dan laporan, siswa TBKR dengan cat dan las, siswa TSM dengan mesin dan rem. Kosakata di kelas jarang menyentuh semua itu. SakuArab menjembatani jarak itu dengan kosakata, transliterasi, dan contoh kalimat yang dekat dengan pekerjaan sehari-hari.

## Fitur

- **2.165 kata** (RPL 537, Akuntansi 510, TBKR 512, TSM 504, ditambah 102 kata umum dunia kerja) dan **24 pasangan "mirip tapi beda"**. Hampir semua kata punya contoh kalimat.
- Pencarian dari tulisan Arab (dengan atau tanpa harakat), Latin, atau Indonesia, lengkap dengan saran ejaan. Daftar kata bisa disaring "belum dikuasai", dan kategori panjang diringkas dulu.
- Kartu kata: harakat bisa dimatikan, transliterasi, contoh kalimat dengan kata target disorot, tag huruf sulit (ع غ ق ح ص ض ط), salin, dan bagikan sebagai gambar.
- Belajar: **flashcard** (pengulangan berjarak sederhana), **kuis kilat**, **susun huruf**, **mirip tapi beda**, target harian, dan streak.
- Favorit, riwayat pencarian, ekspor/impor progres (file JSON) untuk pindah perangkat.
- Mode gelap/terang/auto, tiga paket font (Modern, Klasik, Editorial), ukuran teks Arab bisa diatur.
- Responsif (HP, tablet, desktop), tanpa audio, tanpa akun, tanpa pelacakan. Semua data belajar tersimpan **hanya di perangkat siswa**.
- PWA: bisa di-install dan berjalan offline.

## Menjalankan

Tidak perlu build. Buka lewat server statis agar `words.json` dan PWA berfungsi:

```bash
python -m http.server 8000
# buka http://localhost:8000
```

`index.html` juga bisa dibuka langsung dari berkas; kosakata diambil dari salinan yang tertanam di dalamnya.

## Deploy ke GitHub Pages

*Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/ (root)`.* Semua path bersifat relatif sehingga tidak perlu pengaturan lain.

## Struktur

```
index.html              aplikasi (satu berkas) + salinan kosakata tertanam
words.json              sumber kosakata (ubah di sini)
sw.js, manifest.webmanifest, icon.svg   PWA
scripts/validate.py     validasi words.json
scripts/build.py        tanam ulang words.json ke index.html + naikkan versi cache
scripts/tambah_kata.py  tambah kata dari terminal (latin dibuat otomatis)
scripts/normalisasi.py  merapikan draf kosakata besar menjadi words.json (lihat di bawah)
data/contoh_*.txt       contoh kalimat yang dipakai normalisasi.py
.github/                templat usulan kata dan workflow otomatis
```

## Menambah kosakata

Format tiap entri di `words.json`:

```json
["مِحْوَر", "miḥwar", "poros", "Rangka & Alat", "الْمِحْوَرُ مَكْسُورٌ", "Porosnya patah"]
```

`[arab berharakat, latin, arti, kategori, contoh arab, contoh indonesia]`

Aturan penting:

1. **Tambahkan di akhir daftar jurusan**, jangan disisipkan atau diurutkan ulang. ID kata dibuat dari nomor urut, sehingga menyisipkan akan menggeser favorit dan progres siswa.
2. Tulis lema tanpa tanwin akhir (حَاسُوب, bukan حَاسُوبٌ). Harakat selengkap mungkin.
3. Nama kategori bebas; kategori baru muncul otomatis.
4. Contoh kalimat sebaiknya pendek dan memuat kata targetnya.

Cara cepat dari terminal (latin dibuat otomatis dari harakat):

```bash
python scripts/tambah_kata.py tsm "مِحْوَر" "poros" "Rangka & Alat" "الْمِحْوَرُ مَكْسُورٌ" "Porosnya patah"
python scripts/validate.py
python scripts/build.py
```

Untuk penambahan **massal** (mis. draf hasil kerja bersama), jalankan `python scripts/normalisasi.py draf.json`. Skrip ini menyeragamkan Unicode, membuang tanwin akhir, membuang contoh berpola templat, menggabungkan kategori yang tumpang tindih, membuat ulang transliterasi, dan membuang entri ganda. Tambahan `--legacy words.json` memastikan ID rilis lama tidak bergeser.

Jika `words.json` diubah di GitHub (bukan lokal), workflow **Tanam ulang data** menjalankan validasi dan `build.py` otomatis lalu meng-commit hasilnya.

## Konfigurasi

Blok `CONFIG` di awal `<script>` pada `index.html` mengatur nama, tagline, tema, font, fitur yang aktif (flashcard, kuis, susun huruf, dll.), panjang sesi, target harian, frekuensi sampul, dan sumber data. Warna, ikon, dan kata kunci placeholder jurusan ada di `TRACKS`.

## Catatan kualitas

Teks Arab, harakat, dan contoh kalimat disusun tanpa pemeriksaan penutur asli. **Mohon tinjau oleh guru Bahasa Arab** sebelum dipakai di kelas, terutama padanan istilah teknis. Usulan koreksi sangat diterima lewat [Issue](../../issues/new/choose); lihat [CONTRIBUTING.md](CONTRIBUTING.md).

## Lisensi

- **Kode** (`index.html` di luar data, `sw.js`, `scripts/`, workflow): [MIT](LICENSE).
- **Kosakata** (`words.json` dan salinannya di dalam `index.html`): [CC BY-NC-SA 4.0](LICENSE-DATA.md). Boleh dibagikan dan diadaptasi dengan mencantumkan penulis, untuk tujuan nonkomersial, dan hasilnya dibagikan dengan lisensi yang sama.

## Penulis

**Sultan Bagus Permadi** · SMK Muhammadiyah Pencongan · 2026

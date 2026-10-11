# Changelog

## 4.0 · 2026
- Kosakata menjadi 2.165 kata: RPL 537, Akuntansi 510, TBKR 512, TSM 504, Umum 102 (draf 3.0 berisi 2.203 entri; 38 duplikat dibuang).
- 1.029 contoh kalimat berpola templat ("يَرِدُ الْمُصْطَلَحُ «…»") dibuang; 841 contoh kalimat sungguhan ditulis untuk entri baru.
- 61 salah-harakat dikoreksi berdasarkan selisih Arab–Latin pada draf; kategori yang tumpang tindih digabung (RPL 16, Akuntansi 14, TBKR 9, TSM 14 kategori).
- Transliterasi dibuat ulang dari harakat dengan satu skema; perbaikan untuk "ال + alif wasal" (الِاسْتِخْدَام → al-istikhdām).
- Aplikasi: indeks kategori, saringan "belum dikuasai", ringkasan kategori, kategori tampil di tiap baris hasil.
- `scripts/normalisasi.py` ditambahkan; `validate.py` menolak contoh berpola templat.
- ID 1.324 entri rilis 2.0 tidak bergeser.

## 2.0 · 2026
- Kosakata diperluas menjadi 1.324 kata (±300 per jurusan + 102 umum) dan 24 pasangan "mirip tapi beda".
- Semua contoh kalimat ditulis ulang; beberapa lema dan harakat dikoreksi; transliterasi diseragamkan.
- Fitur baru: susun huruf, mirip tapi beda, target harian, riwayat pencarian, saran ejaan, pilihan sumber kata.
- Data dimuat dari `words.json` dengan cadangan tertanam; PWA offline; skrip validasi dan build; workflow GitHub.

## 1.0 · 2026
- Versi awal: 4 jurusan, pencarian, flashcard, kuis, favorit, sampul, paket font.

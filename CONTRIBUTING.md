# Berkontribusi

Terima kasih sudah membantu menambah dan memperbaiki kosakata SakuArab.

## Cara paling mudah
Buka [Issue → Usul kata baru](../../issues/new/choose) dan isi formulirnya. Tidak perlu menyentuh kode.

## Lewat Pull Request
1. Fork repo, lalu tambahkan entri **di akhir** daftar jurusan di `words.json` (lihat format di [README](README.md#menambah-kosakata)).
2. Jalankan `python scripts/validate.py`. Workflow yang sama berjalan otomatis di setiap PR.
3. Jelaskan sumber istilah (buku, jobsheet, manual) di deskripsi PR.

## Penambahan massal
Untuk daftar kata yang banyak, kumpulkan dalam format yang sama dengan `words.json`, lalu jalankan `python scripts/normalisasi.py draf.json --legacy words.json` sebelum membuka PR. Contoh kalimat sebaiknya ditulis sungguhan; contoh berpola templat ditolak oleh validasi.

## Aturan peninjauan
- Kata baru dan koreksi **ditinjau guru Bahasa Arab** sebelum digabung. Harakat dan padanan istilah teknis tidak boleh lolos tanpa pemeriksaan.
- Jangan menyisipkan atau mengurutkan ulang entri lama; ID kata bergantung pada urutan.
- Kontribusi kosakata dilisensikan di bawah [CC BY-NC-SA 4.0](LICENSE-DATA.md); kontribusi kode di bawah [MIT](LICENSE).

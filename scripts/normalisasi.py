#!/usr/bin/env python3
"""Merapikan draf kosakata (mis. hasil ekspor/penambahan massal) menjadi words.json siap rilis.

  python scripts/normalisasi.py draf.json            # hasil ke words.json
  python scripts/normalisasi.py draf.json --legacy words.json   # sekaligus cek ID rilis lama tidak bergeser

Yang dilakukan (deterministik, bisa diulang):
  1. Unicode NFC pada semua teks Arab.
  2. Membuang tanwin di akhir kata pada lema (bentuk kamus).
  3. Memperbaiki salah-harakat/ejaan yang sudah diketahui (daftar TYPO).
  4. Membuang contoh kalimat berpola templat ("يَرِدُ الْمُصْطَلَحُ «…» فِي دُرُوسِ…") karena tidak mengajarkan apa pun.
  5. Menggabungkan kategori yang tumpang tindih (daftar GABUNG_KATEGORI).
  6. Membuat ulang transliterasi Latin dari harakat, dengan satu skema.
  7. Membuang entri ganda (lema sama setelah harakat dibuang); yang pertama dipertahankan.
  8. Mengisi contoh kalimat dari data/contoh_<jurusan>.txt (format: lema tanpa harakat | contoh arab | terjemahan)
     untuk entri yang contohnya masih kosong.
"""
import json, re, sys, pathlib, unicodedata, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from translit import tr

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACKS = ["RPL", "Akuntansi", "TBKR", "TSM"]
HARAKAT = re.compile(r"[\u064B-\u065F\u0670\u0640]")
nfc = lambda s: unicodedata.normalize("NFC", s)

def key(s):
    s = HARAKAT.sub("", nfc(s))
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"), ("ة", "ه"), ("ى", "ي")): s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

def strip_tanwin(a):
    return re.sub("[\u064C\u064D](?=\u0651?(\\s|$|[؟،.!]))", "", a)

# salah-harakat/ejaan yang terdeteksi dari selisih Arab-vs-Latin pada draf; (salah, benar), diterapkan pada lema
TYPO = [
 ("مُعْمَارِيَّةُ", "مِعْمَارِيَّةُ"), ("حَلْقَةُ تَكْرَار", "حَلْقَةُ تِكْرَار"), ("رَسَالَةُ", "رِسَالَةُ"),
 ("نِقْطَةُ النِّهَايَةِ", "نُقْطَةُ النِّهَايَةِ"), ("تَحَدِيدُ", "تَحْدِيدُ"), ("تَسْلُسُلُ", "تَسَلْسُلُ"),
 ("فَهْرَسُ", "فِهْرِسُ"), ("مُفْتَاح", "مِفْتَاح"), ("مُنْعَكَسَة", "مُنْعَكِسَة"), ("مَعْيَار", "مِعْيَار"),
 ("قَفْل مُتَعَاقِب", "قُفْل مُتَعَاقِب"), ("وَصُولِيَّة", "وُصُولِيَّة"), ("تَشْعُّبِيّ", "تَشَعُّبِيّ"),
 ("تَصْفُّح", "تَصَفُّح"), ("مَحَاسَبِي", "مُحَاسَبِي"), ("تَوْقُّفُ", "تَوَقُّفُ"), ("الصُّنْفِ", "الصِّنْفِ"),
 ("خِرْدِيَّة", "خُرْدِيَّة"), ("مُرْهُونَة", "مَرْهُونَة"), ("عَمُولَة", "عُمُولَة"), ("مِصْدُّ", "مِصَدّ"),
 ("مَرْكَّب", "مُرَكَّب"), ("مِقْصّ", "مِقَصّ"), ("مِقْصُّ", "مِقَصُّ"), ("مَرْشَحُ", "مُرَشِّحُ"), ("مِرْشَحُ", "مُرَشِّحُ"),
 ("مُثَبِّتُ الْبَطَانَةِ", "مُثَبِّتُ الْبِطَانَةِ"), ("مُشْبَكُ", "مِشْبَكُ"), ("الْحَمُوضَةِ", "الْحُمُوضَةِ"),
 ("مَطَابَقَةُ", "مُطَابَقَةُ"), ("قَفَاز", "قُفَّاز"), ("السِّيْلِيكُونِ", "السِّيلِيكُونِ"),
 ("التَّرْسِ", "التُّرْسِ"), ("تَرْسُ", "تُرْسُ"), ("الْقُطْعَةِ", "الْقِطْعَةِ"), ("تَشَغِيل", "تَشْغِيل"),
 ("صَفْرُ", "صِفْرُ"), ("قَطْعَة اِسْتِهْلَاكِيَّة", "قِطْعَة اِسْتِهْلَاكِيَّة"), ("مَضَخَّةُ", "مِضَخَّةُ"),
 ("مُوجِّهُ", "مُوَجِّهُ"), ("قَطْبِيَّةُ", "قُطْبِيَّةُ"), ("الْوَقُودِ", "الْوُقُودِ"), ("وَقُود", "وُقُود"),
]
TYPO = [(nfc(a), nfc(b)) for a, b in TYPO]

# kategori yang tumpang tindih digabung ke satu nama
GABUNG_KATEGORI = {
 "RPL": {"Pengujian dan mutu": "Pengujian dan pemeliharaan", "Basis data dan penyimpanan": "Basis data",
         "Git dan kolaborasi": "Kolaborasi dan manajemen proyek", "Manajemen proyek": "Kolaborasi dan manajemen proyek"},
 "Akuntansi": {"Pajak dan kepatuhan": "Pajak", "Akrual dan penyesuaian": "Jurnal dan buku besar",
               "Dokumen dan pencatatan": "Dasar akuntansi", "Pelaporan dan kerja": "Laporan dan analisis",
               "Laporan keuangan dan analisis": "Laporan dan analisis"},
 "TBKR": {"Pengelasan dan pemotongan": "Pengelasan", "K3 dan perlindungan": "K3 bengkel",
          "Bodi dan panel kendaraan": "Bodi kendaraan", "Alat ukur dan inspeksi": "Pemeriksaan dan mutu",
          "Pengukuran bodi dan rangka": "Pemeriksaan dan mutu"},
 "TSM": {"Sasis, kemudi, dan suspensi": "Sasis dan rem", "Sasis, roda, dan ban": "Sasis dan rem", "Sistem pengereman": "Sasis dan rem",
         "Sistem bahan bakar dan udara": "Mesin dan sistem bahan bakar",
         "Sistem pendingin dan pelumasan": "Pendinginan, pelumasan, dan pembuangan", "Sistem pembuangan": "Pendinginan, pelumasan, dan pembuangan",
         "Kelistrikan dan pengapian": "Kelistrikan", "Diagnosis dan pemindaian": "Diagnosis kerusakan", "Layanan pelanggan": "Percakapan pelanggan"},
}

def muat_contoh(track):
    p = ROOT / "data" / f"contoh_{track.lower()}.txt"
    out = {}
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            part = [x.strip() for x in ln.split("|")]
            if len(part) == 3 and all(part): out[key(part[0])] = (nfc(part[1]), part[2])
    return out

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args: sys.exit(__doc__)
    legacy_path = sys.argv[sys.argv.index("--legacy") + 1] if "--legacy" in sys.argv else None
    draf = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    out = {}
    laporan = collections.OrderedDict()
    for t in TRACKS + ["Umum"]:
        seen, rows = {}, []
        n_ex = n_typo = n_dup = n_cat = 0
        for r in draf[t]:
            ar, _lat, mean, cat, exa, exi = [nfc(x) for x in r[:6]]
            ar = strip_tanwin(ar)
            for bad, good in TYPO:
                if bad in ar: ar = ar.replace(bad, good); n_typo += 1
            if "«" in exa or "«" in exi: exa = exi = ""; n_ex += 1
            c2 = GABUNG_KATEGORI.get(t, {}).get(cat, cat)
            n_cat += c2 != cat
            k = key(ar)
            if k in seen: n_dup += 1; laporan.setdefault(t + " duplikat dibuang", []).append(ar); continue
            seen[k] = len(rows)
            rows.append([ar, tr(ar), mean, c2, exa, exi])
        contoh = muat_contoh(t)
        n_isi = 0
        for r in rows:
            c = contoh.pop(key(r[0]), None)
            if c and not r[4]: r[4], r[5] = c; n_isi += 1
        if contoh: laporan[t + " contoh tak cocok"] = [str(k) for k in contoh]
        out[t] = rows
        laporan[t] = f"{len(rows)} kata | {len(set(r[3] for r in rows))} kategori | koreksi {n_typo} | contoh templat dibuang {n_ex} | digabung kategori {n_cat} | duplikat {n_dup} | contoh diisi {n_isi}"
    out["Mirip"] = [[nfc(p[0]), tr(nfc(p[0])), p[2], nfc(p[3]), tr(nfc(p[3])), p[5], p[6], p[7]] for p in draf.get("Mirip", [])]
    out["_meta"] = {
        "versi": "4.0",
        "format": "[arab, latin, arti, kategori, contoh_arab, contoh_indonesia]",
        "Mirip": "[arab1, latin1, arti1, arab2, latin2, arti2, tips, cakupan]",
        "catatan": "Tambahkan kosakata baru di AKHIR daftar tiap jurusan agar ID favorit dan progres tidak bergeser. Lema tanpa tanwin akhir; latin dibuat otomatis (scripts/tambah_kata.py).",
        "jumlah_entri": {t: len(out[t]) for t in TRACKS + ["Umum"]},
        "bahasa_transliterasi": "Transliterasi Latin edukatif (ḥ, kh, ż, sy, ’ hamzah, ‘ ‘ain); dibuat otomatis dari harakat.",
    }
    if legacy_path:
        old = json.loads(pathlib.Path(legacy_path).read_text(encoding="utf-8"))
        for t in TRACKS + ["Umum"]:
            n0 = len(old[t])
            geser = [i + 1 for i in range(n0) if key(old[t][i][0]) != key(out[t][i][0])]
            laporan[t + " cek ID lama"] = "aman: %d entri awal tidak bergeser" % n0 if not geser else f"PERINGATAN: {len(geser)} entri bergeser, mis. #{geser[:5]}"
    pathlib.Path(ROOT / "words.json").write_text(json.dumps(out, ensure_ascii=False, indent=0, separators=(",", ":")), encoding="utf-8")
    for k, v in laporan.items(): print(k + ":", v if isinstance(v, str) else ", ".join(v))

if __name__ == "__main__":
    main()

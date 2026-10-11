#!/usr/bin/env python3
"""Validasi words.json. Keluar dengan kode 1 jika ada kesalahan (dipakai CI)."""
import json, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACKS = ["RPL", "Akuntansi", "TBKR", "TSM", "Umum"]
SCOPES = {"all", "rpl", "akuntansi", "tbkr", "tsm"}
HARAKAT = re.compile(r"[\u064B-\u065F\u0670\u0640]")
ARABIC = re.compile(r"[\u0600-\u06FF]")
TANWIN_AKHIR = re.compile("[\u064C\u064D](?=\u0651?(\\s|$|[؟،.!]))")
errors, warnings = [], []

def key(s):
    s = HARAKAT.sub("", s)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"), ("ة", "ه"), ("ى", "ي")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

data = json.loads((ROOT / "words.json").read_text(encoding="utf-8"))
for t in TRACKS:
    if t not in data or not isinstance(data[t], list):
        errors.append(f"{t}: daftar tidak ditemukan"); continue
    seen = {}
    for i, r in enumerate(data[t], 1):
        w = f"{t} #{i}"
        if not (isinstance(r, list) and len(r) == 6 and all(isinstance(x, str) for x in r)):
            errors.append(f"{w}: harus berisi 6 teks [arab, latin, arti, kategori, contoh_arab, contoh_indonesia]"); continue
        ar, lat, mean, cat, exa, exi = r
        if not ARABIC.search(ar): errors.append(f"{w}: kolom Arab tanpa huruf Arab: {ar!r}")
        if not lat.strip() or ARABIC.search(lat): errors.append(f"{w} ({ar}): latin kosong atau berisi huruf Arab")
        if not mean.strip(): errors.append(f"{w} ({ar}): arti kosong")
        if not cat.strip(): errors.append(f"{w} ({ar}): kategori kosong")
        if any(len(x) >= 400 for x in r): errors.append(f"{w} ({ar}): ada kolom lebih dari 399 karakter")
        if TANWIN_AKHIR.search(ar): errors.append(f"{w} ({ar}): hapus tanwin di akhir kata (bentuk kamus tanpa tanwin)")
        if "«" in exa or "«" in exi: errors.append(f"{w} ({ar}): contoh berpola templat (mengandung «…»); tulis kalimat sungguhan atau kosongkan")
        if bool(exa) != bool(exi): errors.append(f"{w} ({ar}): contoh Arab dan terjemahannya harus sama-sama diisi atau sama-sama kosong")
        if exa and not ARABIC.search(exa): errors.append(f"{w} ({ar}): contoh Arab tidak berisi huruf Arab")
        if not HARAKAT.search(ar): warnings.append(f"{w} ({ar}): belum berharakat")
        k = key(ar)
        if k in seen: errors.append(f"{w} ({ar}): duplikat dengan #{seen[k]}")
        seen[k] = i
        if exa:
            stems = [x[2:] if x.startswith("ال") else x for x in k.split(" ") if len(x) >= 2]
            if not any(s in key(exa) for s in stems): warnings.append(f"{w} ({ar}): contoh tidak memuat kata ini")
pairs = data.get("Mirip", [])
for i, p in enumerate(pairs, 1):
    if not (isinstance(p, list) and len(p) == 8 and all(isinstance(x, str) and x for x in p)):
        errors.append(f"Mirip #{i}: harus berisi 8 teks"); continue
    if p[7] not in SCOPES: errors.append(f"Mirip #{i}: cakupan harus salah satu dari {sorted(SCOPES)}")

for t in TRACKS:
    c = collections.Counter(r[3] for r in data.get(t, []) if isinstance(r, list) and len(r) == 6)
    print(f"{t}: {len(data.get(t, []))} kata, {len(c)} kategori")
print(f"Mirip: {len(pairs)} pasangan")
for w in warnings[:40]: print("peringatan:", w)
if len(warnings) > 40: print(f"... dan {len(warnings) - 40} peringatan lain")
for e in errors: print("KESALAHAN:", e)
print(f"\n{len(errors)} kesalahan, {len(warnings)} peringatan")
sys.exit(1 if errors else 0)

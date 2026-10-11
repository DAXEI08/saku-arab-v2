#!/usr/bin/env python3
"""Menambah satu kata ke AKHIR daftar jurusan di words.json. Latin dibuat otomatis dari harakat.
Contoh:
  python scripts/tambah_kata.py tsm "مِحْوَر" "poros" "Rangka & Alat" "الْمِحْوَرُ مَكْسُورٌ" "Porosnya patah"
Setelah itu jalankan:  python scripts/validate.py  lalu  python scripts/build.py"""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from translit import tr

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAMA = {"rpl": "RPL", "akuntansi": "Akuntansi", "tbkr": "TBKR", "tsm": "TSM", "umum": "Umum"}
HARAKAT = re.compile(r"[\u064B-\u065F\u0670\u0640]")

def key(s):
    s = HARAKAT.sub("", s)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"), ("ة", "ه"), ("ى", "ي")): s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

if len(sys.argv) not in (5, 7) or sys.argv[1].lower() not in NAMA:
    sys.exit(__doc__)
track = NAMA[sys.argv[1].lower()]
ar, arti, kat = (x.strip() for x in sys.argv[2:5])
exa, exi = (sys.argv[5].strip(), sys.argv[6].strip()) if len(sys.argv) == 7 else ("", "")
ar = re.sub("[\u064C\u064D](?=\u0651?(\\s|$|[؟،.!]))", "", ar)   # buang tanwin akhir
if not re.search(r"[\u0600-\u06FF]", ar): sys.exit("Kolom Arab harus berisi huruf Arab")
path = ROOT / "words.json"
data = json.loads(path.read_text(encoding="utf-8"))
if any(key(r[0]) == key(ar) for r in data[track]): sys.exit(f"Sudah ada di {track}: {ar}")
data[track].append([ar, tr(ar), arti, kat, exa, exi])
path.write_text(json.dumps(data, ensure_ascii=False, indent=0, separators=(",", ":")), encoding="utf-8")
print(f"Ditambahkan ke {track} (#{len(data[track])}): {ar} -> {tr(ar)} = {arti}")

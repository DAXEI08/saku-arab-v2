#!/usr/bin/env python3
"""Menanam ulang words.json ke dalam index.html (cadangan offline) dan menaikkan versi cache di sw.js.
Jalankan setiap selesai menyunting words.json:  python scripts/build.py"""
import json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
words = json.loads((ROOT / "words.json").read_text(encoding="utf-8"))
js = json.dumps(words, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = (ROOT / "index.html").read_text(encoding="utf-8")
new, n = re.subn(r"(const EMBEDDED = /\*__DATA__\*/).*?(;\nconst UMUM)", lambda m: m.group(1) + js + m.group(2), html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Penanda data tidak ditemukan di index.html")
if new == html:
    print("Tidak ada perubahan: data tertanam sudah sama dengan words.json")
else:
    (ROOT / "index.html").write_text(new, encoding="utf-8")
    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    ver = "sakuarab-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M")
    sw = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "{ver}";', sw, count=1)
    (ROOT / "sw.js").write_text(sw, encoding="utf-8")
    print(f"index.html diperbarui, versi cache: {ver}")

# Panduan Pengembangan – Jepret Rimba

Dokumen ini untuk siapa pun yang melanjutkan game ini.

## Ringkasan desain

- **Satu mekanik**: bidik dan jepret. Layar peta dan layar wilayah hanya layar keputusan, bukan mekanik tambahan.
- **Alur**: pilih misi → pilih wilayah di peta Indonesia → kampanye 5 hari. Tiap hari 40 detik sesi, 8 jepretan.
- **Misi yang sudah jadi**: Bekantan (Kalimantan). Tarsius, Cendrawasih, dan Penyu hijau baru placeholder di `MISSIONS` (`open:false`).
- **Tema jam**: "Only one mechanics in a tropical". Tema besar: penguatan masyarakat dan keberlanjutan pesisir/hutan tropis.

## Struktur repo

```
index.html          seluruh game (HTML + CSS + JS, tanpa aset eksternal)
README.md           deskripsi, cara main, kredit, deklarasi AI
DEVELOPMENT.md      dokumen ini
tools/mapgen/       generator peta piksel Indonesia (Node)
tests/              skrip Playwright untuk uji otomatis + screenshot
```

## Menjalankan

Buka `index.html` di browser. Tidak perlu build atau server. Untuk itch.io: zip `index.html` saja (di root zip), upload sebagai HTML project, ukuran viewport 960×540.

## Peta kode di `index.html`

Cari komentar `// =====` di file. Urutannya:

| Bagian | Isi |
|---|---|
| Core | canvas 960×540 logis (di-render 2×), `fit()` letterbox, helper `lerp/clamp/rnd` |
| Input | mouse, klik, kamera |
| Audio | WebAudio sintetis, tanpa file. `CALLS` = suara tiap spesies |
| Data | `SPECIES`, `CLUEDEF` (petunjuk), `THREATDEF` (ancaman), `LAYOUTS`, `SPOTS`, `MISSIONS` |
| Pixel map | grid 320×180 RLE hasil `tools/mapgen`, `regionAt()`, `mapImage()` |
| Game state | objek `G` (hari, wilayah, laporan, bintang) |
| Entities | `ent()`, perilaku Bekantan dan hewan lain (`upd/draw/flee/moment/c`) |
| Art helpers | `ell`, `facetEll` (gaya low-poly), `leafBlob`, `ridge` |
| Creatures | gambar prosedural tiap hewan |
| Scene / Tree species | `SPP` palet spesies, `buildTree`, mahkota pohon yang bergoyang |
| Layout art | layer `far/main/fg/vig` dirender sekali per lokasi, parallax dari mouse |
| Particles / Markers | daun, serangga, penanda petunjuk dan ancaman |
| Session | `startSession`, `endSession`, `nextDay`, `processShot` |
| Region pixel map | `regionMapImage()` peta wilayah |
| Screens | menu, misi, peta, wilayah, ringkasan, arsip, cara main |
| Loop | `requestAnimationFrame` |

Hook debug di console browser: `window.__G` (state) dan `window.__SS` (sesi aktif).

## Angka yang perlu di-tuning setelah playtest

Semua ini baru usulan dan belum diuji pemain sungguhan.

- **Peluang Bekantan muncul**: `SPOTS[i].base` + bonus petunjuk (`CLUEDEF[*].bonus`) + bonus laporan. Wilayah salah = 0. Hari ≥4 dijamin muncul bila wilayah benar. Logikanya ada di `newMission` / `startSession` / `nextDay`.
- **Hewan kabur**: bidikan lebih dari 3 detik pada hewan pemalu (target utama 5 detik). Cari `lim` di bagian Session. Tanda "!" muncul di 55% batas.
- **Skor**: `processShot()` = poin spesies × (0.5 + kualitas), ×1.5 untuk momen khusus. Kualitas dari ketepatan tengah, momen, dan kejernihan (kabut bakau).
- **Bintang**: foto target dengan kualitas ≥70%, minimal 3 laporan ancaman, minimal 5 spesies.

## Menambah konten

- **Hewan baru**: tambah ke `SPECIES`, buat fungsi pembuat entitas (contoh: kuntul, kepiting) dengan `upd/draw/flee/moment/c`, lalu masukkan ke `fauna` di `SPOTS`. Tambah suara di `CALLS`.
- **Misi baru**: ubah `open:true` di `MISSIONS`, isi `region`, `brief`, dan atur peluang munculnya. Wilayah memakai kode di `REGIONS`.
- **Lokasi baru**: tambah `LAYOUTS` dan `SPOTS`, lalu `TREESPEC` (spesies pohon latar dan utama) dan `HAZE` (kabut jarak).
- **Peta wilayah per pulau**: saat ini semua pulau memakai layout peta wilayah yang sama (hanya nama berubah). Ini kandidat perbaikan utama.

## Peta Indonesia

Sumber: Natural Earth 10m (domain publik) lewat paket npm `world-atlas`. Generator di `tools/mapgen/gen.js`:

```bash
cd tools/mapgen
npm install
node gen.js     # menghasilkan map.json (+ preview.txt)
```

Kode sel: 1 negara tetangga, 2 Sumatra, 3 Jawa, 4 Kalimantan, 5 Sulawesi, 6 Nusa Tenggara, 7 Maluku, 8 Papua. Hasil `map.json` (`rle`) ditempel ke bagian Pixel map di `index.html`. Pembagian pulau ke wilayah memakai heuristik `regionOf` di `gen.js`.

## Tes otomatis

```bash
pip install playwright && playwright install chromium
python tests/play.py     # alur menu → misi → peta → wilayah → sesi
python tests/play2.py    # skenario lanjutan
python tests/snap.py     # screenshot cepat
```

Screenshot masuk ke `tests/shots/`. Koordinat klik di skrip mengikuti tata letak layar saat ini, jadi perlu disesuaikan bila UI diubah.

## Ide lanjutan

1. Playtest dengan orang lain, lalu atur ulang tingkat kesulitan.
2. Tampilan kamera ala ponsel (UI bidik).
3. Gambar hewan yang lebih chunky/toy-like agar seragam dengan gaya low-poly.
4. Peta wilayah unik per pulau.
5. Misi kedua (misalnya Tarsius di Sulawesi) memakai sistem yang sama.

## Aturan jam yang harus dijaga

- Aset pihak ketiga hanya yang berlisensi bebas dan dikreditkan di halaman itch.io.
- Penggunaan AI (kode dan aset) harus dideklarasikan jujur di halaman itch.io. Teks siap pakai ada di `README.md`.
- Tidak ada konten SARA, pornografi, kekerasan ekstrem, atau ujaran kebencian.

# Panduan Pengembangan – Jepret Rimba

Dokumen ini untuk siapa pun yang melanjutkan game ini.

## Ringkasan desain

- **Satu mekanik**: bidik dan jepret. Layar peta dan layar wilayah hanya layar keputusan, bukan mekanik tambahan.
- **Alur**: pilih misi → pilih wilayah di peta Indonesia → kampanye 3 hari. Tiap hari 40 detik sesi, 5 jepretan (`SHOTS`, `MAX_DAYS` di index.html).
- **Mobil safari**: mobil berjalan sendiri ke kiri (`DRIVE_SPEED`, 0 = mati). Pemain tidak menyetir; satu-satunya aksi tetap bidik dan jepret. Warna mobil: `CAR_STYLE` (1 Klasik, 2 Ranger, 3 Desa).
- **Latar panorama**: tiap titik dibangun sebagai satu latar lebar utuh untuk seluruh perjalanan (`wideLayout`), dengan 5 pohon khas per area (`AREATREES`). Pulau lain punya peta titik, titik, dan pohon sendiri (`ISLANDSPOTS`, `ISLANDMAP`, `ISLANDLOOK`).
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
| Data | `SPECIES`, `CLUEDEF` (petunjuk), `THREATDEF` (ancaman), `LAYOUTS`, `SPOTS` (Kalimantan), `ISLANDSPOTS` + `VILLAGER` (pulau lain), `MISSIONS` |
| Pixel map | grid 320×180 RLE hasil `tools/mapgen`, `regionAt()`, `mapImage()` |
| Game state | objek `G` (hari, wilayah, laporan, bintang) |
| Safari car (auto drive) | `DRIVE_SPEED`, `SHOTS`, `MAX_DAYS`; latar panorama per titik (`wideLayout`), posisi dunia (`drive()`, `branchYW`, `perchesIn`, `treesIn`, `placeIn`) |
| Entities | `ent()`, perilaku Bekantan dan hewan lain (`upd/draw/flee/moment/c`) |
| Art helpers | `ell`, `facetEll` (gaya low-poly), `leafBlob`, `ridge` |
| Creatures | gambar prosedural tiap hewan |
| Scene / Tree species | `SPP` palet spesies (termasuk rengas, tancang, waru), `AREATREES` (5 pohon per area), `buildTree`, mahkota pohon yang bergoyang |
| Layout art | layer `far/main/fg/vig` dirender sekali per lokasi (`getLayers`, `buildForest`); saat mobil berjalan, satu latar lebar utuh. Pohon per pulau: `ISLANDLOOK` |
| Particles / Markers | daun, serangga, penanda petunjuk dan ancaman |
| Safari car art | tampilan dari dalam mobil (`drawSafariCar`), warna `CAR_SKINS` / `CAR_STYLE` |
| Session | `startSession`, `endSession`, `nextDay`, `processShot` |
| Region pixel map | `regionMapImage()` peta titik tiap pulau, bentuk pulau `ISLANDMAP`, label `MAPLABELS` |
| Screens | `drawMenu`, `drawHowto`, `drawMissions`, `drawMap`, `drawRegion`, `drawSummary`, `drawArchive` |
| Loop | `requestAnimationFrame` |

Hook debug di console browser: `window.__G` (state) dan `window.__SS` (sesi aktif).

## Di mana mengubah apa

Semua desain digambar oleh kode di `index.html` (tidak ada file gambar). Cari nama fungsi atau data di bawah dengan Ctrl+F; nomor baris berubah setiap kali file diedit, jadi pakai nama.

### Layar menu dan peta

| Yang terlihat | Ubah di |
|---|---|
| Menu awal (judul, Mulai, Cara Main) | `drawMenu` |
| Popup Cara Main | `drawHowto` (teks aturan ada di sini) |
| Pilih misi (kartu Bekantan, kartu terkunci) | `drawMissions`; data misi di `MISSIONS` |
| Layar peta Indonesia | `drawMap`; warna dan piksel peta di `mapImage`, nama pulau di `REGIONS` |
| Layar peta titik tiap pulau (pin, panel info) | `drawRegion`; gambar peta di `regionMapImage`, bentuk pantai/sungai/desa di `ISLANDMAP`, label Laut/Sungai/Desa di `MAPLABELS`, ikon pin di `SPOTICON` |
| Ringkasan hari | `drawSummary`; pesan warga pulau salah di `VILLAGER` |
| Arsip desa (akhir misi) | `drawArchive` |
| Tombol di semua layar | `button` |
| Bingkai foto polaroid | `polaroid` |
| Huruf | `FONT`, `font()`, `text()` |

### Sesi foto

| Yang terlihat | Ubah di |
|---|---|
| HUD sesi (hari, timer, kotak jepretan, bingkai bidik, label MOMEN) | `drawSession`, label objek di `drawFrameLabel` |
| Tampilan mobil safari (atap, roll bar, sandaran tangan) | `drawSafariCar`; warna di `CAR_SKINS`, pilihan warna `CAR_STYLE` |
| Kecepatan mobil, jumlah jepretan, jumlah hari | `DRIVE_SPEED`, `SHOTS`, `MAX_DAYS` |
| Langit, bukit, tanah, air, rumput tiap titik | `getLayers` (per jenis: river, mangrove, pedada, estuary); awan/perahu tambahan di `extraSky`, tanaman depan di `extraFg` |
| Latar panorama selama perjalanan | `wideLayout` (pohon utama, pohon latar, lebar) |
| Bentuk dan warna pohon | `buildTree`, palet di `SPP`; 5 pohon per area di `AREATREES`; campuran pohon per pulau di `ISLANDLOOK` |
| Gambar satwa | `drawBekantan`, `drawKuntul`, `drawPekaka`, dan fungsi `draw…` lain di bagian Creatures; nama dan poin di `SPECIES` |
| Gambar petunjuk dan ancaman, penanda ? dan ! | `drawClue`, `drawThreat`, `drawMarker`; data di `CLUEDEF`, `THREATDEF` |
| Titik foto Kalimantan / pulau lain | `SPOTS` / `ISLANDSPOTS` (nama, waktu, satwa, ancaman, event) |

### Pembagian kerja agar tidak konflik

Satu file dipakai bersama, jadi bagi berdasarkan bagian: satu orang mengubah layar menu dan peta (bagian **Screens**, `mapImage`, `regionMapImage`), yang lain mengubah sesi foto (mobil, latar, pohon, satwa). Jangan auto-format seluruh file atau memindahkan blok kode, karena itu mengubah semua baris dan pasti konflik saat merge.

## Angka yang perlu di-tuning setelah playtest

Semua ini baru usulan dan belum diuji pemain sungguhan.

- **Peluang Bekantan muncul**: `SPOTS[i].base` + bonus petunjuk (`CLUEDEF[*].bonus`) + bonus laporan. Wilayah salah = 0. Di hari terakhir (hari 3) dijamin muncul bila wilayah benar. Logikanya ada di `newMission` / `startSession` / `nextDay`.
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

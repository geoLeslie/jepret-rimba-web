> **Versi web (HTML5 Canvas).** Ini build yang sudah bisa dimainkan dan siap upload ke itch.io. Scaffold Godot ada di folder induk repo. Panduan lanjut: [DEVELOPMENT.md](DEVELOPMENT.md).

# Jepret Rimba

Game memotret satwa endemik Indonesia untuk Game Jam IT RUSH 2026.

**Satu mekanik:** bidik dan jepret. Peta Indonesia dan peta daerah hanya layar pilih lokasi.

## Cara main

1. Pilih misi (Bekantan).
2. Pilih pulau tempat satwa itu hidup di peta Indonesia.
3. Selama 5 hari, pilih satu titik per hari lalu memotret selama 40 detik (8 jepretan).
4. Foto satwa untuk poin, foto petunjuk (?) untuk menaikkan peluang target muncul, dan foto ancaman (!) untuk dikirim sebagai laporan ke desa.
5. Misi berhasil jika satwa target terfoto dalam 5 hari.

Kontrol: gerakkan mouse atau jari untuk membidik, klik, ketuk, atau Spasi untuk menjepret.

## Menjalankan

Buka `index.html` di browser. Tidak ada dependensi atau proses build.

Untuk itch.io: zip `index.html`, upload sebagai project HTML, lalu centang "This file will be played in the browser". Viewport 960 × 540.

## Teknologi

HTML5 Canvas dan JavaScript murni dalam satu file. Semua grafis dan suara dibuat langsung oleh kode (vektor dan audio sintetis), tanpa file aset eksternal.

## Kredit dan lisensi data

- Data garis pantai peta Indonesia: [Natural Earth](https://www.naturalearthdata.com/) (domain publik), dirasterisasi menjadi kisi 320 × 180.
- Gaya visual terinspirasi game low-poly. Semua aset digambar sendiri lewat kode.

## Deklarasi penggunaan AI

Kode, grafis, dan suara game ini dibuat dengan bantuan AI (Claude, Anthropic).

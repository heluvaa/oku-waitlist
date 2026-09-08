# Oku.trade Auto Referral Bot

Script otomatisasi berbasis Python untuk pendaftaran *waitlist* atau referral secara otomatis di platform Oku.trade. Script ini terintegrasi dengan layanan email sementara (*temp mail*) dan menyertakan pemecah *Proof-of-Work* (PoW) ALTCHA.

## 🚀 Fitur Utama

- **Auto Temp-Mail:** Pembuatan email sementara secara otomatis via API `mail.tm`.
- **ALTCHA PoW Solver:** Pemecah tantangan *Proof-of-Work* bawaan tanpa memerlukan layanan pihak ketiga.
- **Auto Verification:** Ekstraksi dan eksekusi tautan verifikasi otomatis dari kotak masuk email.
- **User-Agent Rotator:** Dukungan rotasi *User-Agent* dari file eksternal untuk variasi permintaan.

## 🛠️ Prasyarat

- **Python:** Versi 3.x
- **Library:** `requests`

## 💻 Cara Penggunaan

1. **Simpan File Script**
   Unduh atau simpan script Python ke dalam folder proyek Anda.

2. **Instal Dependensi**
   Buka terminal atau Command Prompt pada folder tersebut, lalu jalankan:
   ```bash
   pip install requests

 * Siapkan File User-Agent (Opsional)
   Buat file bernama user-agent.txt di direktori yang sama. Isi dengan daftar User-Agent (satu string per baris). Jika file tidak ditemukan, script akan menggunakan User-Agent default.
 * Konfigurasi Kode Referral
   Buka file script dan sesuaikan variabel REF_CODE dengan kode milik Anda:
   REF_CODE = "KODE_REFERRAL_ANDA"

 * Jalankan Script
   python main.py

   Masukkan jumlah referral yang ingin diproses saat petunjuk muncul di terminal.
⚠️ Disklaimer
Script ini dibuat untuk tujuan edukasi dan pemahaman teknis mengenai interaksi API serta mekanisme Proof-of-Work. Penggunaan script ini untuk manipulasi sistem dapat melanggar Ketentuan Layanan (ToS) dari platform terkait. Seluruh risiko penggunaan ditanggung oleh pengguna.
📄 Lisensi
MIT License


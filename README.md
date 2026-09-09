# Oku Trade Auto Referral & Waitlist Bot

Skrip otomatisasi berbasis Python untuk melakukan pendaftaran *waitlist* dan *referral* otomatis pada platform **Oku Trade** (`oku.trade`) langsung melalui **Termux**. Skrip ini menangani pembuatan *temporary email* secara otomatis via Mail.tm, pemecahan tantangan *Proof of Work* (PoW ALTCHA), pengiriman formulir pendaftaran, rotasi *User-Agent*, hingga verifikasi email otomatis untuk mengonfirmasi *spot* waitlist.

---

## 🚀 Fitur Utama
* **Multi-Account / Bulk Referral:** Mendukung pembuatan banyak akun referral sekaligus dalam sekali jalan berdasarkan input jumlah yang diinginkan.
* **Auto Temporary Email:** Menggunakan integrasi API **Mail.tm** dengan sistem *retry* otomatis jika terjadi kendala pada server mail.
* **PoW ALTCHA Solver:** Otomatis memecahkan algoritma *hash* SHA-256 (Proof of Work) yang dikirim oleh server `accounts.icarus.tools`.
* **User-Agent Rotation:** Membaca daftar *User-Agent* dari file eksternal secara acak untuk setiap akun agar identitas perangkat bervariasi.
* **Auto Verification:** Mendeteksi kotak masuk email secara *real-time* dan mengekstrak tautan berparameter `waitlistToken` untuk mengonfirmasi spot secara instan.

---

## 🛠️ Prasyarat (Requirements)
Sebelum menjalankan skrip ini, pastikan perangkat Anda (khususnya pengguna **Termux**) telah menginstal modul Python yang dibutuhkan:

```bash
pkg update && pkg upgrade
pkg install python git
pip install requests

📦 Cara Instalasi & Pengaturan
 * Clone repository ini atau unduh file skrip ke perangkat Anda:
   git clone [https://github.com/username-anda/oku-waitlist-bot.git](https://github.com/username-anda/oku-waitlist-bot.git)
cd oku-waitlist-bot

 * Atur Kode Referral Anda:
   Buka file oku.py menggunakan editor teks (seperti nano):
   nano oku.py

   Cari baris variabel REF_CODE di bagian atas skrip, lalu ubah nilainya dengan kode referral milik Anda:
   REF_CODE = "KODE_REFERRAL_ANDA_DISINI"

   (Simpan dengan menekan Ctrl + O, Enter, lalu keluar dengan Ctrl + X)
 * Siapkan File user-agent.txt (Opsional tapi Disarankan):
   Buat atau edit file user-agent.txt di folder yang sama untuk rotasi perangkat:
   nano user-agent.txt

   Tempelkan daftar User-Agent Anda di sini (satu baris untuk satu User-Agent), lalu simpan. Jika file ini kosong atau tidak ada, skrip akan menggunakan User-Agent cadangan secara otomatis.
🚀 Cara Menjalankan Skrip
Jalankan perintah berikut di terminal Termux Anda:
python oku.py

Selanjutnya, skrip akan meminta Anda memasukkan jumlah akun referral yang ingin dibuat:
[?] Mau buat berapa referral? [Masukkan angka, contoh: 10]

⚙️ Struktur Berkas
 * oku.py — Skrip utama otomatisasi (pendaftaran, solver PoW, checker email, dan verifikasi).
 * user-agent.txt — Daftar kumpulan User-Agent browser untuk variasi identitas perangkat per akun.
⚠️ Disclaimer
Skrip ini dibuat untuk keperluan edukasi dan pengujian otomatisasi API. Gunakan dengan bijak. Segala risiko akibat penyalahgunaan bot ini ditanggung oleh pengguna masing-masing.


Menjalankan Perpustakaan Digital
================================
Fitur pencarian dan rekomendasi buku menggunakan Python. Pastikan Python 3
tersedia, lalu buka Command Prompt di folder proyek dan jalankan:

    python app.py

Buka di komputer ini:

    http://localhost:8000/

Agar bisa dibuka perangkat lain di jaringan Wi-Fi/LAN yang sama, cari alamat
IPv4 komputer server dengan menjalankan `ipconfig`, lalu buka alamat berikut
dari perangkat tersebut (ganti `192.168.x.x` dengan alamat IPv4 komputer):

    http://192.168.x.x:8000/

Jika Windows Firewall meminta izin, izinkan Python pada jaringan privat.
Server hanya boleh diakses melalui jaringan lokal; jangan teruskan port ini
ke internet atau router.

Hentikan server dengan menekan Ctrl+C pada jendela Command Prompt.

Hosting gratis di Render
========================
Proyek ini sudah memiliki konfigurasi Render di `render.yaml`. Untuk membuat
alamat publik:

1. Unggah proyek ke repository GitHub (repository privat disarankan).
2. Buat akun Render, lalu pilih New > Blueprint.
3. Hubungkan repository GitHub tersebut dan pilih deploy Blueprint.
4. Setelah status deploy menjadi Live, buka URL `onrender.com` yang diberikan.

Layanan gratis dapat tidur setelah tidak menerima kunjungan selama 15 menit;
kunjungan pertama setelah itu mungkin perlu menunggu sekitar satu menit.
File buku yang disertakan dalam deploy dapat diunduh publik melalui situs.
Pastikan izin distribusi publiknya sudah dimiliki sebelum mengunggah.

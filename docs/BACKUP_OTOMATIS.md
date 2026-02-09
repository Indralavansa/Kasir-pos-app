# 🛡️ BACKUP OTOMATIS - PANDUAN SETUP

## Daftar Isi
1. [Quick Start](#quick-start)
2. [Fitur Backup](#fitur-backup)
3. [Penggunaan Manual](#penggunaan-manual)
4. [Setup Auto Backup](#setup-auto-backup)
5. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## Quick Start

### Windows - Menu Interaktif
```bash
cd d:\python\scripts
python backup_otomatis.py
```

### Windows - Auto Backup
```bash
python backup_otomatis.py auto
```

### Command Line Arguments
```bash
python backup_otomatis.py [command]

Commands:
  produk      - Backup hanya produk ke CSV + JSON
  transaksi   - Backup hanya transaksi ke CSV + JSON
  database    - Backup hanya database SQLite
  auto        - Backup semua (produk + transaksi + database)
  list        - List semua backup files
  cleanup     - Hapus backup database lama (keep 10)
  --help      - Tampilkan bantuan
```

---

## Fitur Backup

### 1️⃣ Backup Produk
- **Format**: CSV + JSON
- **Isi**: 
  - ID, Kode, Nama, Deskripsi
  - Harga Beli, Harga Jual
  - Stok, Kategori, Minimal Stok, Satuan
  - Harga Variasi (tingkat)
- **Lokasi**: `d:\python\data\backup_produk_YYYYMMDD_HHMMSS.[csv|json]`

**Gunakan Saat**:
- Perlu backup data produk
- Ingin restore produk yang terhapus
- Analisis data produk

### 2️⃣ Backup Transaksi
- **Format**: CSV + JSON
- **Isi**:
  - Kode Transaksi, Tanggal
  - Harga (subtotal, discount, total)
  - Pembayaran (bayar, kembalian)
  - Metode (tunai, qris, ewallet, dll)
  - Kasir, Member, Poin Earned
  - Detail Items per transaksi (JSON saja)
- **Lokasi**: `d:\python\data\backup_transaksi_YYYYMMDD_HHMMSS.[csv|json]`

**Gunakan Saat**:
- Perlu archive transaksi lama
- Restore transaksi yang terhapus
- Audit & laporan

### 3️⃣ Backup Database
- **Format**: SQLite Database (*.db)
- **Isi**: Semua data lengkap (produk, transaksi, user, member, dll)
- **Lokasi**: `d:\python\backups\kasir_backup_YYYYMMDD_HHMMSS.db`

**Gunakan Saat**:
- Recovery penuh sistem
- Maintenance database

---

## Penggunaan Manual

### Cara 1: Interactive Menu (Windows)
```bash
cd d:\python\scripts
python backup_otomatis.py
```

**Menu Pilihan**:
```
1. Backup Produk (CSV + JSON)
2. Backup Transaksi (CSV + JSON)
3. Backup Database Lengkap (SQLite)
4. Backup Semua (Produk + Transaksi + Database)
5. List Semua Backup
6. Restore Database dari Backup
7. Cleanup Backup Lama
8. Setup Auto Backup
0. Keluar
```

### Cara 2: Command Line

**Backup Produk Saja**:
```bash
python backup_otomatis.py produk
```

**Backup Transaksi Saja**:
```bash
python backup_otomatis.py transaksi
```

**Backup Database Saja**:
```bash
python backup_otomatis.py database
```

**Backup Semua (Auto)**:
```bash
python backup_otomatis.py auto
```

**Lihat Semua Backup**:
```bash
python backup_otomatis.py list
```

**Cleanup Backup Lama**:
```bash
python backup_otomatis.py cleanup
```

---

## Setup Auto Backup

### Windows - Method 1: Double Click Batch File

1. Buka File Explorer
2. Navigate ke: `d:\python\scripts\`
3. Double click: `backup_otomatis.bat`
4. Pilih menu atau tunggu auto complete

### Windows - Method 2: Task Scheduler (Recommended)

**Setup Auto Backup Daily**:

1. **Buka Task Scheduler**
   - Press `Win + R`
   - Ketik: `taskschd.msc`
   - Enter

2. **Create Basic Task**
   - Klik di kanan: "Create Basic Task..."
   - Name: `Backup Otomatis Toko Sembako`
   - Description: `Auto backup produk dan transaksi`
   - Next

3. **Set Trigger (Jadwal)**
   - Pilih: `Daily`
   - Start: Hari ini atau tanggal lain
   - Recur every: `1 day`
   - **Time**: `23:00` (jam 11 malam, bisa disesuaikan)
   - Next

4. **Set Action**
   - Pilih: `Start a program`
   - Isi Program/Script:
     ```
     C:\Python311\python.exe
     ```
     (Sesuaikan dengan path Python Anda)
   
   - Isi Add Arguments:
     ```
     "D:\python\tools\backup_otomatis.py" auto
     ```
   
   - Isi Start in (optional):
     ```
     D:\python
     ```
   
   - Next

5. **Finish**
   - Review summary
   - Klik Finish

6. **Test Task**
   - Di Task Scheduler, cari task yang baru dibuat
   - Right-click → Run
   - Tunggu sampai selesai

**Output Akan Ditampilkan**:
```
✅ Backup Produk Berhasil!
   📊 Total produk: 367
   📄 CSV: backup_produk_20260208_230000.csv
   📋 JSON: backup_produk_20260208_230000.json

✅ Backup Transaksi Berhasil!
   📊 Total transaksi: 156
   📄 CSV: backup_transaksi_20260208_230000.csv
   📋 JSON: backup_transaksi_20260208_230000.json

✅ Backup Database Berhasil!
   📦 File: kasir_backup_20260208_230000.db
   💾 Ukuran: 2.45 MB
```

### Windows - Method 3: Batch File + Cmd Shortcut

1. Buat shortcut di Desktop:
   - Right-click Desktop → New → Shortcut
   - Location: 
     ```
     cmd /c "D:\python\scripts\backup_otomatis.bat auto"
     ```
   - Name: `Backup Otomatis`
   - Click Finish

2. Double-click shortcut untuk manual backup

### Linux/Mac - Cron Job

**Edit Crontab**:
```bash
crontab -e
```

**Tambahkan Baris Ini**:
```cron
# Auto backup setiap hari jam 23:00 (11 malam)
0 23 * * * cd /path/to/python && python tools/backup_otomatis.py auto

# Atau setiap 6 jam (4x sehari)
0 */6 * * * cd /path/to/python && python tools/backup_otomatis.py auto

# Atau setiap hari jam 01:00 (1 pagi)
0 1 * * * cd /path/to/python && python tools/backup_otomatis.py auto
```

---

## Lokasi File Backup

### Backup Database
```
d:\python\backups\
  ├── kasir_backup_20260208_230000.db
  ├── kasir_backup_20260208_220000.db
  └── kasir_backup_20260208_210000.db
```

### Backup Produk & Transaksi
```
d:\python\data\
  ├── backup_produk_20260208_230000.csv
  ├── backup_produk_20260208_230000.json
  ├── backup_transaksi_20260208_230000.csv
  └── backup_transaksi_20260208_230000.json
```

---

## Restore Data

### Restore Database

1. Jalankan script:
   ```bash
   python backup_otomatis.py
   ```

2. Pilih menu: `6. Restore Database dari Backup`

3. Pilih backup yang ingin di-restore

4. Konfirmasi: ketik `y` untuk proceed

5. Database akan di-restore dan backup current akan disave

### Restore Produk dari CSV

Saat ini perlu manual import ke Excel atau database tool.

Future: Akan ditambahkan fitur auto-restore produk.

---

## FAQ & Troubleshooting

### Q: Backup gagal - "Database tidak ditemukan"
**A**: Pastikan path sudah benar di `INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')`

### Q: Bagaimana menghapus backup lama?
**A**: Gunakan command:
```bash
python backup_otomatis.py cleanup
```
Ini akan keep 10 backup terbaru, hapus yang lama.

### Q: Berapa ukuran backup?
**A**: 
- Database: ~2-5 MB (tergantung data)
- Produk CSV: ~50-100 KB
- Transaksi CSV: ~500 KB - 2 MB (tergantung jumlah transaksi)

### Q: Backup file bisa di-download?
**A**: Ya, semua backup ada di folder:
- Database: `d:\python\backups\`
- CSV/JSON: `d:\python\data\`

Bisa didownload via FTP atau direktly dari folder.

### Q: Bagaimana jika Task Scheduler tidak jalan?
**Solusi**:
1. Check apakah Task Scheduler service running
2. Run as Administrator
3. Pastikan Python path benar
4. Check Event Viewer untuk error details

### Q: Ingin backup lebih sering (misal 2x sehari)?
**A**: Edit Task Scheduler:
- Klik task → Properties
- Triggers tab → Edit
- Recurrence: set 12 hours atau sesuai kebutuhan

### Q: Ingin simpan lebih banyak backup files?
**A**: Edit script di line `cleanup_old_backups(keep=10)`:
```python
cleanup_old_backups(keep=20)  # Simpan 20 file
```

### Q: CSV backup bisa diimport ke Excel?
**A**: Ya! 
1. Buka Excel
2. File → Open
3. Select `backup_produk_*.csv`
4. Excel akan auto-format

---

## Maintenance Checklist

- [ ] Setup auto backup ke Task Scheduler
- [ ] Test manual backup dulu
- [ ] Test restore dari backup
- [ ] Check backup files ada di folder
- [ ] Monitor disk space (backup bisa besar)
- [ ] Cleanup old backups monthly
- [ ] Keep 10-20 backup files terbaru saja

---

## Support

Untuk bantuan: [support@tokosembako.com]

---

**Last Updated**: 8 Februari 2026
**Version**: 1.0

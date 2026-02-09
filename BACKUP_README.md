# 🛡️ Backup Otomatis - Toko Sembako Kasir

**Sistem backup otomatis untuk melindungi data produk, transaksi, dan database.**

## Quick Start (Mulai Cepat)

### Run Backup Manual (Windows Command Prompt)

```bash
cd d:\python

# 1. Backup Hanya Produk
python tools\backup_otomatis_standalone.py produk

# 2. Backup Hanya Transaksi  
python tools\backup_otomatis_standalone.py transaksi

# 3. Backup Database Lengkap
python tools\backup_otomatis_standalone.py database

# 4. Backup Semua (DIREKOMENDASIKAN)
python tools\backup_otomatis_standalone.py auto

# 5. Lihat Daftar Backup
python tools\backup_otomatis_standalone.py list

# 6. Cleanup Backup Lama (simpan 10 terbaru)
python tools\backup_otomatis_standalone.py cleanup
```

### Run via Batch File (Lebih Mudah)

Double-click `scripts\backup_otomatis.bat` untuk interactive menu, atau:

```bash
# Dari Command Prompt atau PowerShell
scripts\backup_otomatis.bat auto
scripts\backup_otomatis.bat list
scripts\backup_otomatis.bat cleanup
```

### Run Menu Interaktif

```bash
python tools\backup_otomatis_standalone.py

# Atau via batch file (tanpa argumen)
scripts\backup_otomatis.bat
```

Kemudian pilih nomor opsi 1-7.

## Fitur Lengkap

### 📊 Backup Produk
- **File Format**: CSV + JSON
- **Fields**: ID, Kode, Nama, Deskripsi, Harga Beli, Harga Jual, Stok, Kategori, Minimal Stok, Satuan
- **Lokasi**: `d:\python\data\backup_produk_*.csv|json`

**Contoh CSV:**
```
ID,Kode,Nama,Deskripsi,Harga Beli,Harga Jual,Stok,Kategori,Minimal Stok,Satuan,Backup Date
1,SKU001,Minyak Goreng Bimoli,1L,10000,14500,50,MINYAK,10,Botol,2025-02-08 23:34:49
2,SKU002,Terigu Cakra,1kg,8000,12000,100,TEPUNG,20,Kg,2025-02-08 23:34:49
```

### 💰 Backup Transaksi
- **File Format**: CSV + JSON  
- **Fields**: Kode Transaksi, Tanggal, Subtotal, Diskon, Total, Bayar, Kembalian, Metode Pembayaran, Kasir, Member, Poin Earned
- **Lokasi**: `d:\python\data\backup_transaksi_*.csv|json`

**Contoh CSV:**
```
ID,Kode Transaksi,Tanggal,Subtotal,Diskon %,Diskon Rp,Total,Bayar,Kembalian,Metode Pembayaran,Kasir,Member,Poin Earned,Backup Date
1,TRX20250208001,2025-02-08 10:30:00,150000,10,15000,135000,150000,15000,CASH,Budi,-,1350,2025-02-08 23:34:49
2,TRX20250208002,2025-02-08 10:45:00,200000,0,0,200000,200000,0,TRANSFER,Budi,MEMBER001,2000,2025-02-08 23:34:49
```

### 🗄️ Backup Database
- **File Format**: SQLite Database (`.db`)
- **Isi**: Semua tabel dan data lengkap 
- **Lokasi**: `d:\python\backups\kasir_backup_*.db`
- **Ukuran**: ~0.09 MB per backup
- **Keamanan**: Automatic cleanup menjaga 10 backup terbaru

### 📦 Backup Lengkap (Auto)
Backup ketiga jenis data sekaligus dalam satu perintah:
1. ✅ Produk (CSV + JSON)
2. ✅ Transaksi (CSV + JSON)
3. ✅ Database lengkap (SQLite)
4. ✅ Cleanup otomatis

Dipanggil dengan: `python backup_otomatis_standalone.py auto`

## Lokasi File Backup

```
d:\python\
├── backups/               ← Database backups (.db files)
│   ├── kasir_backup_20250208_230613.db
│   ├── kasir_backup_20250208_233449.db
│   └── ...
│
└── data/                  ← CSV & JSON backups
    ├── backup_produk_20250208_233449.csv
    ├── backup_produk_20250208_233449.json
    ├── backup_transaksi_20250208_233449.csv
    └── backup_transaksi_20250208_233449.json
```

## Setup Backup Otomatis (Windows Task Scheduler)

### Langkah-langkah:

1. **Buka Task Scheduler**
   ```
   Tekan Windows + R
   Ketik: taskschd.msc
   Tekan Enter
   ```

2. **Buat Task Baru**
   - Right-click "Task Scheduler (Local)" → "Create Basic Task"
   - **Name**: Backup Kasir Otomatis
   - **Description**: Daily backup of POS database
   - Click "Next"

3. **Set Trigger (Waktu Backup)**
   - Pilih "Daily"
   - Time: 23:00 (jam 11 malam, sesuaikan sesuai kebutuhan)
   - Click "Next"

4. **Set Action (Perintah)**
   - Pilih "Start a Program"
   - **Program/script**: 
     ```
     C:\Windows\System32\cmd.exe
     ```
   - **Add arguments (opsional)**:
     ```
     /c "D:\python\scripts\backup_otomatis.bat auto"
     ```
   - **Start in (opsional)**:
     ```
     D:\python
     ```
   - Click "Next"

5. **Finish**
   - Review settings
   - Click "Finish"
   - Jika diminta password, masukkan password Windows Anda

6. **Test Task**
   - Di Task Scheduler, temukan "Backup Kasir Otomatis"
   - Right-click → "Run" 
   - Buka `d:\python\backups` dan `d:\python\data` untuk verifikasi

### Contoh Schedule yang Direkomendasikan:

- **Daily**: 23:00 (tengah malam) - minimal disk lock
- **Weekly**: Setiap Minggu 23:00 - backup mingguan ekstra
- **Monthly**: Tanggal 1 setiap bulan - archive bulanan

## Restore Database dari Backup

### Via Script (Interaktif):

```bash
python tools\backup_otomatis_standalone.py restore

# Atau via batch file:
scripts\backup_otomatis.bat restore
```

Kemudian:
1. Pilih nomor backup dari list (1-5 terbaru)
2. Konfirmasi restore (Y/N)
3. Script akan:
   - ✅ Create backup database saat ini dengan nama `kasir_backup_before_restore_*.db`
   - ✅ Restore database dari pilihan Anda
   - ✅ Selesai

### Via Manual File Copy:

1. Stop aplikasi Flask (close browser atau stop server)
2. Copy file dari `d:\python\backups\kasir_backup_YYYYMMDD_HHMMSS.db`
3. Paste ke `d:\python\instance\kasir.db` (replace)
4. Jalankan aplikasi ulang

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'openpyxl'"
**Solusi**: Gunakan script **standalone** (`backup_otomatis_standalone.py`), bukan yang lama. Script standalone tidak butuh dependencies ekstra.

### ❌ "Database tidak ditemukan"
**Cek**: Path `d:\python\instance\kasir.db` exists
```bash
# Lihat apakah file ada
dir d:\python\instance\kasir.db
```

### ❌ "Permission denied pada backups folder"
**Solusi**: 
- Tutup file explorer yang buka folder `d:\python\backups`
- Pastikan file database tidak sedang diakses aplikasi lain
- Run Command Prompt as Administrator

### ❌ "Batch file not found"
**Cek**: File `d:\python\scripts\backup_otomatis.bat` exists
```bash
# Dari d:\python directory:
dir scripts\backup_otomatis.bat
```

## CSV Files untuk Excel

Semua file backup Produk dan Transaksi dalam format CSV dapat langsung dibuka di Microsoft Excel:

1. Buka Excel
2. File → Open
3. Navigate ke `d:\python\data\` 
4. Pilih file `backup_produk_*.csv` atau `backup_transaksi_*.csv`
5. Excel akan auto-parse CSV with headers

**Tips**: 
- Ubah encoding ke UTF-8 jika ada karakter aneh
- File sudah include timestamp backup
- Cocok untuk audit, laporan, atau archival

## JSON Files untuk Integration

File JSON useful untuk integrasi ke sistem lain atau backup yang terstruktur:

```json
[
  {
    "id": 1,
    "kode": "SKU001",
    "nama": "Minyak Goreng Bimoli",
    "deskripsi": "1L",
    "harga_beli": 10000,
    "harga_jual": 14500,
    "stok": 50,
    "kategori": "MINYAK",
    "minimal_stok": 10,
    "satuan": "Botol"
  }
]
```

Bisa di-import ke Python, Node.js, atau aplikasi lain.

## Database Backup untuk Recovery

File `.db` adalah SQLite database binary yang bisa:

1. **Direct restore** - Copy ke `instance/kasir.db`
2. **Analyze dengan SQLite tools**:
   ```bash
   # Install sqlite3 (usually pre-installed on Windows)
   sqlite3 kasir_backup_20250208_233449.db
   
   # View tables
   .tables
   
   # Query data
   SELECT COUNT(*) FROM produk;
   SELECT COUNT(*) FROM transaksi;
   ```
3. **Export ke SQL**:
   ```bash
   sqlite3 kasir_backup_20250208_233449.db ".dump" > backup.sql
   ```

## Estimasi Ukuran & Waktu

| Operation | Time | Packing | Notes |
|-----------|------|---------|-------|
| Backup Produk (367 items) | <1s | ~50 KB | CSV+JSON |
| Backup Transaksi (11 items) | <1s | ~20 KB | CSV+JSON |
| Database Backup | <1s | ~90 KB | .db file |
| **Backup Lengkap (Auto)** | **~3s** | **~160 KB** | All three + cleanup |

## Best Practices

✅ **DO:**
- Run `backup_otomatis.py auto` setiap hari (setup di Task Scheduler)
- Simpan backup di lokasi alternatif (external drive, cloud) untuk disaster recovery
- Monitor backup folder ukuran (~900 KB untuk 10 database backups)
- Test restore process monthly untuk verifikasi

❌ **DON'T:**
- Hapus file backup manual - gunakan `cleanup` command
- Backup saat transaksi berjalan (minimal impact tapi possible lock)
- Rely on hanya 1 backup - redundancy penting untuk bisnis
- Simpan backup hanya di same drive dengan aplikasi

## Monitoring Checklist

Bagian dari maintenance harian/mingguan:

- [ ] Database backup folder ukuran reasonable (<100 MB untuk 10 backups)
- [ ] CSV/JSON exports bisa dibuka di Excel
- [ ] Recent backup timestamp up-to-date
- [ ] Task Scheduler shows last run successful (jika auto-backup active)
- [ ] Clean up old backups jika folder terlalu besar

## Contact & Support

Jika ada masalah dengan backup system:
1. Check nama folder paths - harus exact case-sensitive di Python
2. Verify `instance/kasir.db` readable/writable
3. Check disk space (~10 MB minimum untuk backups)
4. Run manual backup dari interactive menu untuk detailed error messages

---

**Last Updated**: Feb 2025  
**Compatible Version**: Python 3.7+  
**Database**: SQLite (kasir.db)  
**Status**: ✅ Production Ready

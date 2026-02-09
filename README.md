# 📦 Kasir Toko Sembako

Sistem manajemen penjualan modern untuk toko retail dengan fitur kasir, inventory, dan backup otomatis.

## 🚀 Quick Start

### 1. **Jalankan Aplikasi**
```bash
scripts/start_app.bat
```
Atau double-click `scripts/start_app.bat` dari Windows Explorer.

Aplikasi akan berjalan di: `http://localhost:5000`

### 2. **Login Default**
```
Admin:
- Username: admin
- Password: admin123

Kasir:
- Username: kasir
- Password: kasir123
```

### 3. **Backup Management**
```bash
scripts/backup_manage.bat
```
Menu untuk:
- List semua backup
- Restore backup terbaru
- Backup manual
- Cleanup backup lama

## 📋 Features

✅ **Autentikasi & Role-Based Access**
- Admin & Kasir roles dengan akses berbeda
- Session control yang aman
- Password hashing dengan werkzeug

✅ **Manajemen Produk**
- CRUD produk dengan kategori
- Validasi duplikasi kode
- Tracking stok dan harga
- Support multiple satuan
- **🆕 Harga Variasi / Tier Pricing** - atur harga berbeda per quantity (misal: 1-9 pcs @ Rp1000, 10+ pcs @ Rp900)

✅ **Sistem Kasir**
- Real-time product search via API
- Cart management dengan auto-calculate tier pricing
- Auto-backup setiap transaksi
- Receipt/struk cetakan
- Dynamic pricing berdasarkan quantity

✅ **Laporan & Analytics**
- Riwayat transaksi
- Penjualan per hari
- Status kategori produk

✅ **Backup Otomatis**
- Backup setelah setiap transaksi
- Keep 10 backup terbaru
- Manual restore available

✅ **Multi-Device Access**
- Akses dari jaringan: `http://192.168.1.x:5000`
- Responsive design untuk mobile
- Cookie-based session

## 🎯 Struktur Folder

```
d:\python/
├── app/                       ← Aplikasi Flask
│   ├── app_simple.py         ← Main Flask application
│   ├── config.py             ← Configuration
│   ├── static/               ← Web assets (CSS, JS)
│   └── templates/            ← HTML templates
│
├── migrations/                ← Database migrations
│   ├── migrate_db.py
│   ├── migrate_price_variants.py
│   ├── migrate_settings.py
│   └── add_harga_variasi.py  ← Migration untuk harga variasi
│
├── tools/                     ← Utility tools
│   ├── backup_system.py
│   ├── check_imports.py
│   └── create_test_user.py
│
├── tests/                     ← Test files
│   ├── test_csrf.py
│   ├── test_csrf_pages.py
│   ├── test_line_format.py
│   └── test_parse.py
│
├── scripts/                   ← Batch scripts
│   ├── start_app.bat         ← Launch aplikasi
│   ├── backup_manage.bat     ← Backup management
│   └── migrate_harga_variasi.bat ← Migration harga variasi
│
├── docs/                      ← Documentation
│   ├── SETUP.md              ← Setup guide
│   └── HARGA_VARIASI.md      ← 🆕 Panduan harga variasi
│
├── instance/                  ← Database folder
│   └── kasir.db              ← SQLite database

├── data/                      ← Sample/import data
│   └── dbamiramart_2026February - Copy (2).MDB
│
├── backups/                   ← Auto backup storage
│
├── requirements.txt           ← Python dependencies
└── README.md                  ← This file
```

## 🆕 Fitur Harga Variasi (Tier Pricing)

Sistem harga bertingkat yang memungkinkan harga berbeda berdasarkan jumlah pembelian.

### Quick Start:
1. **Jalankan Migration** (sekali saja untuk database lama):
   ```bash
   scripts\migrate_harga_variasi.bat
   ```

2. **Setup Harga Variasi**:
   - Buka **Produk** > **Tambah/Edit Produk**
   - Scroll ke section **"Harga Variasi (Tier Pricing)"**
   - Klik **"Tambah Tier Harga"**
   - Isi minimal qty dan harga untuk setiap tier
   - Save

3. **Di Kasir**:
   - Harga akan otomatis menyesuaikan dengan quantity
   - Badge hijau menunjukkan tier yang aktif

### Contoh:
```
Beras Premium 1kg:
- 1-9 kg    = Rp 15.000/kg
- 10-49 kg  = Rp 14.000/kg  
- 50-99 kg  = Rp 13.500/kg
- 100+ kg   = Rp 13.000/kg

Beli 5 kg  → 5 × Rp 15.000 = Rp 75.000
Beli 50 kg → 50 × Rp 13.500 = Rp 675.000 ✅ Hemat!
```

📖 **Dokumentasi lengkap**: [`docs/HARGA_VARIASI.md`](docs/HARGA_VARIASI.md)

## 📊 Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `nama`: Full name
- `role`: 'admin' atau 'kasir'

### Kategori
- `id`: Primary key
- `nama`: Category name (unique)
- `deskripsi`: Description

### Produk
- `id`: Primary key
- `kode`: Product code (unique)
- `nama`: Product name
- `harga_beli`: Cost price
- `harga_jual`: Selling price
- `stok`: Current stock
- `kategori_id`: Foreign key to Kategori
- `minimal_stok`: Minimum stock alert
- `satuan`: Unit (pcs, kg, liter, dll)

### HargaVariasi (🆕)
- `id`: Primary key
- `produk_id`: Foreign key to Produk
- `min_qty`: Minimal quantity untuk tier ini
- `harga`: Harga per unit pada tier ini
- `keterangan`: Label tier (opsional)

### Transaksi
- `id`: Primary key
- `kode_transaksi`: Transaction code (unique)
- `tanggal`: Transaction timestamp
- `total`: Total amount
- `bayar`: Amount paid
- `kembalian`: Change
- `user_id`: Cashier who processed

### TransaksiItem
- `id`: Primary key
- `transaksi_id`: Foreign key to Transaksi
- `produk_id`: Foreign key to Produk
- `jumlah`: Quantity
- `harga`: Price at time of transaction
- `subtotal`: Quantity × Price

## 🔒 Security Features

✅ Disable developer tools (F12, Ctrl+Shift+I)
✅ Disable right-click context menu
✅ CSRF protection dengan FlaskWTF
✅ Password hashing
✅ Role-based access control
✅ Session timeout handling
✅ HTTP header security

## ⚙️ Tech Stack

- **Backend**: Flask 3.0.3
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap 5, Alpine.js
- **Authentication**: Flask-Login
- **Validation**: WTForms
- **Password**: Werkzeug

## 🐛 Troubleshooting

**Error: "Python tidak ditemukan"**
- Pastikan Python sudah terinstall dan di PATH
- Test: `python --version` di Command Prompt

**Error: "Port 5000 sudah dipakai"**
- Kill existing process atau ganti port di `app_simple.py`
- Find: `app.run(host='0.0.0.0', debug=True, port=5000)`

**Error: "Database locked"**
- Close aplikasi yang lain yang pakai database
- Delete `instance/kasir.db` untuk fresh start

**Error: "Kode produk sudah digunakan"**
- Gunakan kode produk yang berbeda
- Atau reset database: delete `instance/kasir.db`

## 📝 Notes

- Database auto-created pada startup
- Default data sample included
- Daily backups di `backups/` folder
- Session cookie expires on browser close
- Time zone: UTC (dapat dikustomisasi)

## 📞 Support

Untuk bantuan atau bug report, kirim detail:
- Error message lengkap
- Steps untuk reproduce
- Browser & OS yang dipakai

## 📄 License

Private use untuk Toko Sembako

---

**Version**: 1.0.0
**Last Updated**: February 2026

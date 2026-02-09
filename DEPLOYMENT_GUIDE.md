# 🚀 Deployment Guide: Render + Neon PostgreSQL

## Prerequisite:
- GitHub account (untuk host kode)
- Neon account (ke sini nanti, gratis)
- Render account (ke sini nanti, gratis)

---

## Step 1: Setup GitHub Repository

### 1.1 Initialize Git
```bash
cd d:\python
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

### 1.2 Add all files & commit
```bash
git add .
git commit -m "Initial commit - POS Toko Sembako"
```

### 1.3 Create repository di GitHub
1. Buka [github.com](https://github.com) → Login/Sign Up
2. Click "New" repository
3. Name: `kasir-pos-app`
4. Description: "POS system untuk toko sembako"
5. Choose "Public" (biar bisa di-deploy gratis)
6. Click "Create repository"

### 1.4 Link & push ke GitHub
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kasir-pos-app.git
git push -u origin main
```

---

## Step 2: Setup Neon Database

### 2.1 Buat Neon Account
1. Buka [neon.tech](https://neon.tech)
2. Sign up (free tier unlimited)
3. Verify email

### 2.2 Buat PostgreSQL Database
1. Click "New project"
2. Name: `kasir-db`
3. Database name: `kasir` (auto-generated)
4. Password: `Auto-generated` (copy & save temporary)
5. Click "Create project"

### 2.3 Dapatkan Connection String
1. Di Neon dashboard, click "Connection string"
2. Copy string yang format:
   ```
   postgresql://user:password@endpoint.neon.tech:5432/database
   ```
3. Replace `password` dengan yang auto-generated tadi
4. **SAVE THIS STRING** - perlu untuk Render!

---

## Step 3: Deploy ke Render

### 3.1 Connect GitHub ke Render
1. Buka [render.com](https://render.com)
2. Sign up dengan GitHub
3. Click "New +" → "Web Service"

### 3.2 Configure Web Service
- **GitHub Integration**: Authorize & select `kasir-pos-app` repo
- **Name**: `kasir-pos-app`
- **Environment**: `Python 3.10`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app.app_simple:app
  ```

### 3.3 Set Environment Variables
Click "Environment" tab:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://user:password@endpoint.neon.tech:5432/database` |
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |

### 3.4 Deploy
Click "Create Web Service" dan tunggu deployment selesai (~2-3 menit)

---

## Step 4: Initialize Database (One-time)

Setelah Render deploy berhasil:

### 4.1 Via Render Shell
1. Di Render dashboard, click app → "Shell"
2. Jalankan:
   ```bash
   python -c "from app.app_simple import app, db; 
   with app.app_context(): 
       db.create_all()
       print('✅ Database tables created!')"
   ```

### 4.2 Create Admin User
Jalankan di shell atau via Python script:
```python
from app.app_simple import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check tahun user sudah ada
    if not User.query.filter_by(username='admin').first():
        user = User(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(user)
        db.session.commit()
        print('✅ Admin user created!')
```

### 4.3 Import Data (Optional)
Jika mau import produk dari backup:
```bash
# Export dari SQLite backup
python tools/backup_otomatis_standalone.py produk

# Kemudian import ke PostgreSQL (akan dibuat script terpisah)
```

---

## Step 5: Verifikasi Deployment

### 5.1 Test App
Render akan generate URL seperti:
```
https://kasir-pos-app.onrender.com
```

Buka di browser dan test:
- Login dengan username: `admin`, password: `admin123`
- Test create produk
- Test transaksi
- Test reports

### 5.2 Check Logs
Di Render dashboard:
- Click app → "Logs" untuk lihat server errors

### 5.3 Monitor Database
Di Neon dashboard:
- Lihat query stats
- Monitor storage usage
- Backup settings

---

## Step 6: Update & Redeploy

Workflow untuk update:

```bash
# 1. Make changes locally
# 2. Test di local
python -m flask run

# 3. Commit & push
git add .
git commit -m "Fix: login page responsive"
git push

# 4. Render auto-redeploy dalam ~1 menit
```

---

## Troubleshooting

### ❌ "Database connection error"
- Check `DATABASE_URL` environment variable di Render
- Test connection string:
  ```bash
  psql "postgresql://user:pass@host:5432/db"
  ```

### ❌ "Module not found"
- Check `requirements.txt` include semua imports
- Render logs show install errors

### ❌ "Gunicorn timeout"
- Database migration terlalu lama
- Run migrations di Render shell dulu, baru deploy

### ❌ Static files tidak load
- Check `app.config['STATIC_FOLDER']` path correct
- Di Flask, static files otomatis serve dari `static/` folder

---

## Useful Commands (Local Development)

```bash
# Test database connection
python -c "from app.app_simple import app, db; db.create_all(); print('OK')"

# Quick Flask dev server
FLASK_APP=app.app_simple FLASK_ENV=development flask run

# Generate secure SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Access PostgreSQL (jika psql installed)
psql "DATABASE_URL_STRING"
```

---

## Final Checklist

- [ ] GitHub repo created & pushed
- [ ] .gitignore proper (exclude .env, __pycache__)
- [ ] Procfile exists
- [ ] requirements.txt include gunicorn + psycopg2-binary
- [ ] app_simple.py supports DATABASE_URL env var
- [ ] Neon PostgreSQL created & connection string saved
- [ ] Render web service configured
- [ ] Environment variables set in Render
- [ ] Database initialized (create_all)
- [ ] Admin user created
- [ ] App tested in production
- [ ] Domain/URL bookmarked

---

## Production Ready! ✅

Public URL: `https://kasir-pos-app.onrender.com`

Data will persist in Neon PostgreSQL (unlimited free).

---

**Created**: Feb 2026  
**Status**: Ready for deployment

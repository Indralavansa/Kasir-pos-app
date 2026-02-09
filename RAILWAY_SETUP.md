═══════════════════════════════════════════════════════════
RAILWAY DEPLOYMENT GUIDE (Gratis & Unlimited)
═══════════════════════════════════════════════════════════

🎯 STEP-BY-STEP:

1. SIGN UP RAILWAY
   • Buka: https://railway.app
   • Klik "Start Project"
   • Login dengan GitHub

2. CREATE NEW PROJECT
   • Pilih "Deploy from GitHub repo"
   • Automatis detect repo: Kasir-pos-app
   • Klik "Deploy"

3. CONFIGURE VARIABLES (Environment)
   • Di Railway dashboard, klik "Variables"
   • Tambahkan:
   
   DATABASE_URL:
   postgresql://kasir_user:password123@localhost:5432/kasir_db
   (Railway akan auto-generate ini dari PostgreSQL plugin)
   
   SECRET_KEY:
   (Generate dari: python tools/generate_secret_key.py)

4. ADD PostgreSQL DATABASE
   • Di Railway dashboard, klik "Create New Service" 
   • Pilih "PostgreSQL"
   • Railway auto-add DATABASE_URL ke env
   • Verifikasi di Variables tab

5. CONNECT GITHUB TO RAILWAY (Auto-Deploy)
   • Railway otomatis watch GitHub
   • Setiap push = auto-deploy
   • Tidak perlu manual trigger

6. WAIT FOR DEPLOYMENT
   • Tunggu build selesai (2-5 menit)
   • Lihat logs di "Deployment" tab
   • Green checkmark = SUCCESS

7. ACCESS APP
   • Railway auto-generate domain: 
     https://<railway-generated-domain>.up.railway.app
   • Atau custom domain (premium)
   • App akan auto-initialize database

8. LOGIN
   • Username: admin
   • Password: admin123

═══════════════════════════════════════════════════════════
RAILWAY ADVANTAGES:
═══════════════════════════════════════════════════════════
✅ Gratis $5/bulan (unlimited projects = generous)
✅ PostgreSQL included (tidak perlu Neon)
✅ Auto-deploy dari GitHub push
✅ Logs real-time
✅ Scale kapan saja
✅ Custom domain bisa
✅ No cold start

═══════════════════════════════════════════════════════════
FILES ALREADY READY:
═══════════════════════════════════════════════════════════
✅ Procfile - gunicorn config
✅ requirements.txt - dependencies
✅ app/app_simple.py - Flask app dengan PostgreSQL support
✅ .env.example - template environment variables

═══════════════════════════════════════════════════════════
SETTING UP POSTGRESQL AT RAILWAY:
═══════════════════════════════════════════════════════════

Option A: Railway PostgreSQL Plugin (RECOMMENDED)
1. Dashboard → Create Service → PostgreSQL
2. Railway auto-set DATABASE_URL
3. Done!

Option B: External PostgreSQL (Neon/Supabase)
1. Get connection string dari provider
2. Set DATABASE_URL manually di Railway Variables
3. Format: postgresql://user:password@host:port/dbname

═══════════════════════════════════════════════════════════
TROUBLESHOOTING RAILWAY:
═══════════════════════════════════════════════════════════

❌ "Port not detected"
→ Railway auto-detect dari Procfile
→ Pastikan PORT=$PORT di startup

❌ "Database connection failed"
→ Cek DATABASE_URL format
→ Cek PostgreSQL service sudah added
→ Restart deployment

❌ "Module not found"
→ Pastikan requirements.txt complete
→ Railway auto-run: pip install -r requirements.txt

❌ "Redirect loop"
→ Sudah diperbaiki di latest commit
→ Flask session akan work dengan HTTP (Railway handle HTTPS)

═══════════════════════════════════════════════════════════
AFTER DEPLOYMENT SUCCESS:
═══════════════════════════════════════════════════════════

1. App live di https://your-domain.up.railway.app
2. Database auto-init tabel saat first boot
3. Admin user auto-create saat first login
4. Backup sistem ready (lihat: tools/backup_otomatis_standalone.py)

KODE UNTUK URL RAILWAY DASHBOARD:
→ https://railway.app/dashboard

═══════════════════════════════════════════════════════════
NEXT STEPS SETELAH DEPLOY:
═══════════════════════════════════════════════════════════

1. Monitor logs di Railway dashboard
2. Login dengan admin/admin123
3. Import data produk (jika ada backup SQLite)
4. Setup backup otomatis (gunakan: tools/backup_otomatis_standalone.py)
5. Configure custom domain (opsional, Railway beri domain gratis)

═══════════════════════════════════════════════════════════
REFERENSI:
═══════════════════════════════════════════════════════════
Railway Docs: https://docs.railway.app
PostgreSQL Setup: https://docs.railway.app/plugins/postgresql
Python Deployment: https://docs.railway.app/guides/deploying-python

═══════════════════════════════════════════════════════════

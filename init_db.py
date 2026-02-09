#!/usr/bin/env python
"""
Initialize database tables and create admin user
Jalankan ini di Render Shell atau lokal untuk setup database
"""
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.app_simple import app, db, User

def init_database():
    """Create all database tables"""
    print("[DB] Creating database tables...")
    with app.app_context():
        db.create_all()
        print("[DB] ✅ Database tables created successfully!")

def create_admin_user():
    """Create default admin user"""
    print("[USER] Creating admin user...")
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("[USER] Admin user sudah ada, skip...")
            return
        
        # Create new admin user
        admin = User(
            username='admin',
            email='admin@kasirtokosembako.local',
            is_active=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        print("[USER] ✅ Admin user created!")
        print("[USER]   Username: admin")
        print("[USER]   Password: admin123")
        print("[USER]   Email: admin@kasirtokosembako.local")

if __name__ == '__main__':
    try:
        init_database()
        create_admin_user()
        print("\n✅ Inisialisasi database selesai!")
        print("Anda sekarang bisa login dengan username 'admin' dan password 'admin123'")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

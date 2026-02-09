#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRATE DATA: SQLite to PostgreSQL
===================================
Script untuk migrasi data dari SQLite lokal ke PostgreSQL (Neon)
Gunakan ini setelah setup Neon database
"""

import os
import sys
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

def get_db_connection_string():
    """Get database connection string from environment"""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL tidak ditemukan di .env")
        print("Tambahkan: DATABASE_URL=postgresql://user:password@host/db")
        return None
    return db_url

def export_sqlite_to_sql():
    """Export SQLite database ke SQL file"""
    db_path = 'd:\\python\\instance\\kasir.db'
    
    if not os.path.exists(db_path):
        print(f"❌ SQLite database tidak ditemukan: {db_path}")
        return None
    
    sql_file = 'd:\\python\\data\\kasir_export.sql'
    
    try:
        # Export using sqlite3 command
        cmd = f'sqlite3 "{db_path}" ".dump" > "{sql_file}"'
        os.system(cmd)
        
        if os.path.exists(sql_file):
            print(f"✅ SQLite exported: {sql_file}")
            return sql_file
        else:
            print("❌ Export gagal")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def migrate_via_python():
    """Migrasi data menggunakan Python SQLAlchemy"""
    print("\n🔄 MIGRASI DATA: SQLite → PostgreSQL\n")
    
    # Import Flask app
    try:
        from app.app_simple import app, db
        # Models will be imported automatically via app
    except ImportError as e:
        print(f"❌ Error import app: {e}")
        return False
    
    # Get connection strings
    sqlite_url = 'sqlite:////d:/python/instance/kasir.db'
    postgres_url = get_db_connection_string()
    
    if not postgres_url:
        return False
    
    # Convert postgres:// to postgresql://
    if postgres_url.startswith('postgres://'):
        postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
    
    print(f"Source (SQLite):     {sqlite_url}")
    print(f"Target (PostgreSQL): {postgres_url}\n")
    
    try:
        # Create PostgreSQL connection
        from sqlalchemy import create_engine, inspect, MetaData, Table, insert, select
        
        sqlite_engine = create_engine(sqlite_url)
        postgres_engine = create_engine(postgres_url)
        
        # Get all tables dari SQLite
        inspector = inspect(sqlite_engine)
        table_names = inspector.get_table_names()
        
        print(f"📊 Tables found dalam SQLite: {len(table_names)}")
        for table_name in table_names:
            print(f"  • {table_name}")
        
        # Create all tables di PostgreSQL
        print("\n🔨 Creating tables di PostgreSQL...")
        metadata = MetaData()
        metadata.reflect(bind=sqlite_engine)
        metadata.create_all(postgres_engine)
        print("✅ Tables created")
        
        # Migrate data
        print("\n📤 Migrating data...")
        with sqlite_engine.connect() as sqlite_conn:
            with postgres_engine.connect() as postgres_conn:
                for table_name in table_names:
                    # Skip SQLite metadata tables
                    if table_name.startswith('sqlite_'):
                        continue
                    
                    # Get data from SQLite
                    sqlite_table = Table(table_name, metadata, autoload_with=sqlite_engine)
                    rows = sqlite_conn.execute(select(sqlite_table)).fetchall()
                    
                    if rows:
                        # Insert ke PostgreSQL
                        postgres_conn.execute(insert(sqlite_table), [row._mapping for row in rows])
                        postgres_conn.commit()
                        print(f"  ✅ {table_name}: {len(rows)} rows migrated")
                    else:
                        print(f"  ⓘ {table_name}: empty table")
        
        print("\n✅ MIGRASI SELESAI!")
        print("\nNext steps:")
        print("1. Test aplikasi dengan data baru")
        print("2. Perbarui .env dengan DATABASE_URL PostgreSQL")
        print("3. Deploy ke Render")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main migration process"""
    print("=" * 70)
    print("DATA MIGRATION: SQLite (Local) → PostgreSQL (Neon)")
    print("=" * 70)
    
    # Check if .env has DATABASE_URL
    if not os.getenv('DATABASE_URL'):
        print("\n⚠️  DATABASE_URL tidak ada di .env")
        print("\nLangkah-langkah:")
        print("1. Buat database di Neon: https://neon.tech")
        print("2. Copy PostgreSQL connection string")
        print("3. Tambahkan ke .env:")
        print("   DATABASE_URL=postgresql://user:password@host/db")
        print("\n4. Jalankan script ini lagi")
        return
    
    # Confirm
    print("\n⚠️  PENTING: Data lokal akan di-copy ke PostgreSQL")
    confirm = input("\nLanjutkan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Dibatalkan.")
        return
    
    # Run migration
    success = migrate_via_python()
    
    if success:
        print("\n📌 Sekarang:")
        print("1. Ubah DATABASE_URL di Render ke PostgreSQL")
        print("2. Deploy ulang aplikasi")
        print("3. Data akan menggunakan PostgreSQL")

if __name__ == '__main__':
    main()

"""
Script untuk import data ke production PostgreSQL database
Jalankan dengan: DATABASE_URL=xxx python import_data.py
"""
import json
import os
from pathlib import Path

# Read exported data
data_file = Path(__file__).parent / 'data' / 'production_data_export.json'

if not data_file.exists():
    print(f"ERROR: Data file tidak ditemukan: {data_file}")
    exit(1)

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"[IMPORT] Loaded data from: {data_file}")
print(f"  - Kategori: {len(data['kategori'])}")
print(f"  - Produk: {len(data['produk'])}")
print(f"  - Member: {len(data['member'])}")

# Import using Flask app context
from app.app_simple import app, db, Kategori, Produk, Member, HargaVariasi

with app.app_context():
    print("\n[IMPORT] Importing data to database...")
    
    # Check if data already imported
    existing_kategori = Kategori.query.count()
    existing_produk = Produk.query.count()
    
    if existing_kategori > 0 and existing_produk > 0:
        print("[IMPORT] Data already exists in database!")
        print(f"  - Kategori: {existing_kategori}")
        print(f"  - Produk: {existing_produk}")
        print("[IMPORT] Skipping import.")
        exit(0)
    
    # Import Kategori
    print("[IMPORT] Importing kategori...")
    kategori_map = {}  # Map old ID to new ID
    for k_data in data['kategori']:
        k = Kategori(
            nama=k_data['nama'],
            deskripsi=k_data['deskripsi']
        )
        db.session.add(k)
    db.session.commit()
    
    # Refresh to get IDs
    for k_data in data['kategori']:
        k = Kategori.query.filter_by(nama=k_data['nama']).first()
        if k:
            kategori_map[k_data['id']] = k.id
    
    print(f"  OK - {len(kategori_map)} kategori imported")
    
    # Import Produk
    print("[IMPORT] Importing produk...")
    for p_data in data['produk']:
        p = Produk(
            kode=p_data['kode'],
            nama=p_data['nama'],
            deskripsi=p_data.get('deskripsi'),
            harga_beli=p_data['harga_beli'],
            harga_jual=p_data['harga_jual'],
            stok=p_data['stok'],
            kategori_id=kategori_map.get(p_data['kategori_id']),
            minimal_stok=p_data.get('minimal_stok', 5),
            satuan=p_data.get('satuan', 'pcs')
        )
        db.session.add(p)
    db.session.commit()
    print(f"  OK - {len(data['produk'])} produk imported")
    
    # Import Member
    if data['member']:
        print("[IMPORT] Importing member...")
        for m_data in data['member']:
            from datetime import datetime
            m = Member(
                nama=m_data['nama'],
                no_telp=m_data.get('no_telp'),
                alamat=m_data.get('alamat'),
                catatan=m_data.get('catatan'),
                points=m_data.get('points', 0),
                total_spent=m_data.get('total_spent', 0),
                created_at=datetime.fromisoformat(m_data['created_at']) if m_data.get('created_at') else None
            )
            db.session.add(m)
        db.session.commit()
        print(f"  OK - {len(data['member'])} member imported")
    
    # Import HargaVariasi
    if data['harga_variasi']:
        print("[IMPORT] Importing harga variasi...")
        for hv_data in data['harga_variasi']:
            hv = HargaVariasi(
                produk_id=hv_data['produk_id'],
                min_qty=hv_data['min_qty'],
                harga=hv_data['harga']
            )
            db.session.add(hv)
        db.session.commit()
        print(f"  OK - {len(data['harga_variasi'])} harga variasi imported")

print("\n[IMPORT] Import successful!")

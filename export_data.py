"""
Script untuk export data dari lokal SQLite dan prepare untuk import ke PostgreSQL
"""
import os
import json
from datetime import datetime

from app.app_simple import app, db, Kategori, Produk, Member, Transaksi, TransaksiItem, HargaVariasi, Pengaturan

data_to_export = {
    'kategori': [],
    'produk': [],
    'member': [],
    'harga_variasi': [],
}

with app.app_context():
    print("[EXPORT] Exporting data from local database...")
    
    # Export Kategori
    print("[EXPORT] Exporting Kategori...")
    for k in Kategori.query.all():
        data_to_export['kategori'].append({
            'id': k.id,
            'nama': k.nama,
            'deskripsi': k.deskripsi,
        })
    print(f"  OK - {len(data_to_export['kategori'])} kategori")
    
    # Export Produk
    print("[EXPORT] Exporting Produk...")
    for p in Produk.query.all():
        data_to_export['produk'].append({
            'id': p.id,
            'kode': p.kode,
            'nama': p.nama,
            'deskripsi': p.deskripsi,
            'harga_beli': float(p.harga_beli),
            'harga_jual': float(p.harga_jual),
            'stok': p.stok,
            'kategori_id': p.kategori_id,
            'minimal_stok': p.minimal_stok,
            'satuan': p.satuan,
        })
    print(f"  OK - {len(data_to_export['produk'])} produk")
    
    # Export HargaVariasi
    print("[EXPORT] Exporting HargaVariasi...")
    for hv in HargaVariasi.query.all():
        data_to_export['harga_variasi'].append({
            'id': hv.id,
            'produk_id': hv.produk_id,
            'min_qty': hv.min_qty,
            'harga': float(hv.harga),
        })
    print(f"  OK - {len(data_to_export['harga_variasi'])} harga variasi")
    
    # Export Member (optional)
    print("[EXPORT] Exporting Member...")
    for m in Member.query.all():
        data_to_export['member'].append({
            'id': m.id,
            'nama': m.nama,
            'no_telp': m.no_telp,
            'alamat': m.alamat,
            'catatan': m.catatan,
            'points': m.points,
            'total_spent': float(m.total_spent),
            'created_at': m.created_at.isoformat() if m.created_at else None,
        })
    print(f"  OK - {len(data_to_export['member'])} member")

# Save to JSON
output_file = 'd:/python/data/production_data_export.json'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data_to_export, f, indent=2, ensure_ascii=False)

print(f"\n[EXPORT] Data saved to: {output_file}")
print(f"[EXPORT] Total size: {len(json.dumps(data_to_export))} bytes")

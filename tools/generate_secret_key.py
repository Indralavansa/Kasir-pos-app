#!/usr/bin/env python3
"""
Generate secure SECRET_KEY untuk Flask
Jalankan: python tools/generate_secret_key.py
"""

import secrets

def generate_secret_key():
    """Generate secure random SECRET_KEY"""
    key = secrets.token_hex(32)
    return key

if __name__ == '__main__':
    key = generate_secret_key()
    print("\n" + "="*60)
    print("🔐 GENERATED SECRET_KEY:")
    print("="*60)
    print(f"\n{key}\n")
    print("="*60)
    print("📌 Copy this key and paste into Render environment variable")
    print("   KEY: SECRET_KEY")
    print("="*60 + "\n")

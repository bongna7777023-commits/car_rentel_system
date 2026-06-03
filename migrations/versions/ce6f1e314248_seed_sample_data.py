"""Seed sample data for all tables

Revision ID: ce6f1e314248
Revises: ba8e3dc35e37
Create Date: 2026-06-03 14:17:51.930867
"""
import os
import sys
import subprocess
from alembic import op
import sqlalchemy as sa

revision = 'ce6f1e314248'
down_revision = 'ba8e3dc35e37'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    tables_to_seed = ['users', 'cars', 'bookings', 'promotions', 'notifications']
    has_data = False
    for table in tables_to_seed:
        row = conn.execute(sa.text(f"SELECT COUNT(*) AS cnt FROM {table}")).fetchone()
        if row and row[0] > 0:
            has_data = True
            break

    if has_data:
        print("  Database already has data, skipping seed migration")
        return

    seed_path = os.path.join(os.path.dirname(__file__), '../../scripts/seed_data.py')
    result = subprocess.run(
        [sys.executable, seed_path],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), '../..'),
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    )
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"  Seed script error: {result.stderr}")
    else:
        print("  Seed data migration complete")


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM notifications"))
    conn.execute(sa.text("DELETE FROM bookings"))
    conn.execute(sa.text("DELETE FROM promotions"))
    conn.execute(sa.text("DELETE FROM admin_accounts WHERE email != 'admin@luxedrive.com'"))
    conn.execute(sa.text("DELETE FROM cars"))
    conn.execute(sa.text("DELETE FROM users WHERE email NOT IN ('test@example.com','phanphoun123@gmail.com')"))
    print("  Seed data removed")

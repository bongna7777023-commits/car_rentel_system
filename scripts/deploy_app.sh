#!/bin/bash
# Run this on the APP SERVER (192.168.109.148)
# Usage: Run each section step-by-step, or pipe this script to ssh

set -e

APP_DIR="$HOME/car_rentel_system"
DB_HOST="192.168.108.234"
DB_USER="dba"
DB_PASS="abc123"
DB_NAME="car_rental_db"

echo "=== Step 1: Install system dependencies ==="
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-pip python3-venv mysql-client git

echo "=== Step 2: Copy project files ==="
# Option A: Clone from git repo
# git clone <your-repo-url> "$APP_DIR"

# Option B: Copy from local machine (run this on YOUR local machine):
# scp -r /path/to/car_rentel_system pnc@192.168.109.148:~/

# Option C: If files are already transferred, skip to next step

echo "=== Step 3: Set up Python virtual environment ==="
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate

echo "=== Step 4: Install Python dependencies ==="
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn==23.0.0

echo "=== Step 5: Configure .env ==="
cat > config/.env << EOF
# Database Configuration
DB_HOST=$DB_HOST
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASS
DB_NAME=$DB_NAME
DB_PORT=3306

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development

# Generate a real secret key:
FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
DEBUG=False

# Google OAuth - leave blank if not used
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
EOF

echo "=== Step 6: Test database connection ==="
python3 -c "
import sys; sys.path.insert(0, '.')
from app.models.db_config import get_db_connection, close_db_connection
conn = get_db_connection()
if conn:
    print('Database connection: OK')
    close_db_connection(conn)
else:
    print('Database connection: FAILED')
    sys.exit(1)
"

echo "=== Step 7: Run database migrations ==="
source venv/bin/activate
export FLASK_APP=run.py
flask db upgrade

echo "=== Step 8: Seed sample data ==="
python3 scripts/seed_data.py

echo "=== Step 9: Create systemd service ==="
sudo tee /etc/systemd/system/car-rental.service > /dev/null << 'SERVICE'
[Unit]
Description=LuxeDrive Car Rental System
After=network.target

[Service]
User=pnc
WorkingDirectory=/home/pnc/car_rentel_system
ExecStart=/home/pnc/car_rentel_system/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app
Restart=always
RestartSec=5
Environment=FLASK_ENV=production
Environment=PYTHONIOENCODING=utf-8

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable car-rental
sudo systemctl start car-rental

echo "=== Step 10: Verify service ==="
sleep 3
sudo systemctl status car-rental --no-pager

echo ""
echo "============================================="
echo "  DEPLOYMENT COMPLETE"
echo "  App running at: http://192.168.109.148:5000"
echo "  Admin login:    http://192.168.109.148:5000/admin/login"
echo "  Email:          admin@luxedrive.com"
echo "  Password:       AdminLuxe2024!"
echo "============================================="

#!/bin/bash
# =====================================================
# APP SERVER SETUP
# Target: pnc@VANNA-web  (or pnc@192.168.109.148)
# Password: 1234567
# Deploy to: /var/www/car_rentel_system
# =====================================================
# Run this on YOUR local machine:
#   scp deploy_app.sh pnc@VANNA-web:~/deploy_app.sh
#   ssh pnc@VANNA-web "sudo bash ~/deploy_app.sh"
# =====================================================

set -e

APP_DIR="/var/www/car_rentel_system"
DB_HOST="192.168.108.234"
DB_USER="dba"
DB_PASS="abc123"
DB_NAME="car_rental_db"

echo "=== Step 1: Install system dependencies ==="
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-pip python3-venv mysql-client git nginx

echo ""
echo "=== Step 2: Clone the repository ==="
rm -rf "$APP_DIR"
git clone https://github.com/bongna7777023-commits/car_rentel_system.git "$APP_DIR"

echo ""
echo "=== Step 3: Set up Python virtual environment ==="
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate

echo ""
echo "=== Step 4: Install Python dependencies ==="
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
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
FLASK_ENV=production
FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
DEBUG=False

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
EOF

echo ""
echo "=== Step 6: Test database connection ==="
python3 -c "
import sys; sys.path.insert(0, '.')
from app.models.db_config import get_db_connection, close_db_connection
conn = get_db_connection()
if conn:
    print('  Database connection: OK')
    close_db_connection(conn)
else:
    print('  Database connection: FAILED')
    sys.exit(1)
"

echo ""
echo "=== Step 7: Run database migrations ==="
export FLASK_APP=run.py
export PYTHONIOENCODING=utf-8
flask db upgrade

echo ""
echo "=== Step 8: Verify tables ==="
python3 -c "
import sys; sys.path.insert(0, '.')
from app.models.db_config import get_db_connection, close_db_connection
conn = get_db_connection()
cursor = conn.cursor()
for t in ['users', 'admin_accounts', 'cars', 'bookings', 'promotions', 'notifications']:
    cursor.execute(f'SELECT COUNT(*) FROM {t}')
    print(f'  {t}: {cursor.fetchone()[0]} rows')
cursor.close()
close_db_connection(conn)
"

echo ""
echo "=== Step 9: Create systemd service ==="
cat > /etc/systemd/system/car-rental.service << 'SERVICE'
[Unit]
Description=LuxeDrive Car Rental System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/car_rentel_system
ExecStart=/var/www/car_rentel_system/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app
Restart=always
RestartSec=5
Environment=FLASK_ENV=production
Environment=PYTHONIOENCODING=utf-8

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable car-rental
systemctl start car-rental

echo ""
echo "=== Step 10: Configure Nginx reverse proxy ==="
cat > /etc/nginx/sites-available/car-rental << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/car_rentel_system/static/;
        expires 30d;
    }

    client_max_body_size 10M;
}
NGINX

# Enable site and remove default
ln -sf /etc/nginx/sites-available/car-rental /etc/nginx/sites-enabled/car-rental
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo ""
echo "=== Step 11: Set permissions ==="
chown -R www-data:www-data "$APP_DIR"
chmod -R 755 "$APP_DIR"

echo ""
echo "=== Step 12: Verify service ==="
sleep 3
systemctl status car-rental --no-pager

echo ""
echo "============================================="
echo "  DEPLOYMENT COMPLETE"
echo "  App running at: http://VANNA-web"
echo "  (or http://192.168.109.148)"
echo ""
echo "  Admin login:  http://VANNA-web/admin/login"
echo "  Email:        admin@luxedrive.com"
echo "  Password:     AdminLuxe2024!"
echo "============================================="

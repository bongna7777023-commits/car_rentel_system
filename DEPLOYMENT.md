# LuxeDrive Car Rental System — Deployment Guide

## Overview

This document provides complete instructions for deploying the LuxeDrive Car Rental System across two Linux servers:

| Server | Hostname | IP | Purpose |
|--------|----------|-----|---------|
| Database | `pnc@dbms` | `192.168.108.234` | MariaDB database |
| Application | `pnc@VANNA-web` | `192.168.109.148` | Flask + Gunicorn + Nginx |

---

## Prerequisites

- **SSH access** to both servers with password `1234567`
- **Git** installed on your local machine
- **Python 3.8+** on the app server
- Both servers on the same network

---

## 1. Database Server Setup

### 1.1 Connect to the database server

```bash
ssh pnc@192.168.108.234
# Password: 1234567
```

### 1.2 Create the database

```bash
mysql -u dba -p'abc123' -e "CREATE DATABASE IF NOT EXISTS car_rental_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 1.3 Verify the database exists

```bash
mysql -u dba -p'abc123' -e "SHOW DATABASES LIKE 'car_rental_db';"
```

### 1.4 Grant privileges (if needed)

```bash
mysql -u dba -p'abc123' -e "GRANT ALL PRIVILEGES ON car_rental_db.* TO 'dba'@'%'; FLUSH PRIVILEGES;"
```

### 1.5 Exit the DB server

```bash
exit
```

---

## 2. Application Server Setup

### 2.1 Connect to the app server

```bash
ssh pnc@192.168.109.148
# Password: 1234567
```

### 2.2 Install system dependencies

```bash
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-pip python3-venv mysql-client git nginx
```

### 2.3 Clone the repository

```bash
sudo rm -rf /var/www/car_rentel_system
sudo git clone https://github.com/bongna7777023-commits/car_rentel_system.git /var/www/car_rentel_system
sudo chown -R pnc:pnc /var/www/car_rentel_system
```

### 2.4 Set up Python virtual environment

```bash
cd /var/www/car_rentel_system
python3 -m venv venv
source venv/bin/activate
```

### 2.5 Install Python dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 2.6 Configure environment variables

```bash
cat > /var/www/car_rentel_system/config/.env << 'EOF'
# Database Configuration
DB_HOST=192.168.108.234
DB_USER=dba
DB_PASSWORD=abc123
DB_NAME=car_rental_db
DB_PORT=3306

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=production
FLASK_SECRET_KEY=de458f2a1b3c7e8d9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d
DEBUG=False

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
EOF
```

### 2.7 Test database connection

```bash
cd /var/www/car_rentel_system
source venv/bin/activate
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
```

### 2.8 Run database migrations

```bash
export FLASK_APP=run.py
export PYTHONIOENCODING=utf-8
flask db upgrade
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> ba8e3dc35e37, Initial migration: all tables
INFO  [alembic.runtime.migration] Running upgrade ba8e3dc35e37 -> ce6f1e314248, Seed sample data for all tables
```

### 2.9 Verify tables

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from app.models.db_config import get_db_connection, close_db_connection
conn = get_db_connection()
cursor = conn.cursor()
for t in ['users', 'admin_accounts', 'cars', 'bookings', 'promotions', 'notifications']:
    cursor.execute(f'SELECT COUNT(*) FROM {t}')
    print(f'{t}: {cursor.fetchone()[0]} rows')
cursor.close()
close_db_connection(conn)
"
```

Expected output:
```
users: 5 rows
admin_accounts: 2 rows
cars: 11 rows
bookings: 5 rows
promotions: 4 rows
notifications: 3 rows
```

### 2.10 Create systemd service

```bash
sudo tee /etc/systemd/system/car-rental.service > /dev/null << 'SERVICE'
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
```

### 2.11 Start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable car-rental
sudo systemctl start car-rental
```

### 2.12 Verify the service

```bash
sudo systemctl status car-rental --no-pager
```

Expected: `Active: active (running)`

---

## 3. Nginx Reverse Proxy Setup

### 3.1 Create Nginx site configuration

```bash
sudo tee /etc/nginx/sites-available/car-rental > /dev/null << 'NGINX'
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
```

### 3.2 Enable the site

```bash
sudo ln -sf /etc/nginx/sites-available/car-rental /etc/nginx/sites-enabled/car-rental
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 3.3 Set proper permissions

```bash
sudo chown -R www-data:www-data /var/www/car_rentel_system
sudo chmod -R 755 /var/www/car_rentel_system
```

---

## 4. Verification

### 4.1 Test the application

Open a browser on any machine on the same network:

```
http://192.168.109.148
```

You should see the LuxeDrive Car Rental homepage.

### 4.2 Test admin login

```
http://192.168.109.148/admin/login
```

| Field | Value |
|-------|-------|
| Full Name | LuxeDrive Admin |
| Email | admin@luxedrive.com |
| Phone | 1234567890 |
| Password | AdminLuxe2024! |

### 4.3 Test customer login

```
http://192.168.109.148/login
```

| Field | Value |
|-------|-------|
| Email | alice@example.com |
| Password | AlicePass1 |

---

## 5. Maintenance

### 5.1 View application logs

```bash
sudo journalctl -u car-rental -f
```

### 5.2 Restart the application

```bash
sudo systemctl restart car-rental
```

### 5.3 Deploy code updates

```bash
cd /var/www/car_rentel_system
sudo -u www-data git pull
sudo systemctl restart car-rental
```

### 5.4 Create a new migration (after model changes)

```bash
cd /var/www/car_rentel_system
sudo -u www-data source venv/bin/activate
sudo -u www-data flask db migrate -m "Description of changes"
sudo -u www-data flask db upgrade
sudo systemctl restart car-rental
```

---

## 6. Architecture

```
┌──────────────┐      ┌─────────────────────────────────────┐
│   Browser    │─────▶│         Nginx (port 80)              │
│              │      │   Reverse proxy + static files        │
└──────────────┘      └──────────────┬──────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────┐
│               Gunicorn (port 5000)                       │
│               Flask Application                          │
│               run:app (4 workers)                        │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    MySQL / MariaDB                       │
│                    car_rental_db                         │
│        6 tables: users, admin_accounts,                  │
│                  cars, bookings,                         │
│                  promotions, notifications               │
└─────────────────────────────────────────────────────────┘
```

### Database Schema

| Table | Purpose |
|-------|---------|
| `users` | Customer accounts |
| `admin_accounts` | Admin/staff accounts |
| `cars` | Vehicle inventory |
| `bookings` | Rental bookings |
| `promotions` | Discount promo codes |
| `notifications` | User notifications |

---

## 7. Troubleshooting

### 7.1 Database connection refused

```bash
# Check if MariaDB is running on DB server
ssh pnc@192.168.108.234 "sudo systemctl status mariadb"

# Check if port 3306 is open
ssh pnc@192.168.108.234 "sudo ss -tlnp | grep 3306"
```

### 7.2 502 Bad Gateway (Nginx)

```bash
# Check if Gunicorn is running
sudo systemctl status car-rental

# Check the application log
sudo journalctl -u car-rental -n 50

# Test Gunicorn directly
curl http://127.0.0.1:5000
```

### 7.3 Permission errors

```bash
sudo chown -R www-data:www-data /var/www/car_rentel_system
sudo chmod -R 755 /var/www/car_rentel_system
```

### 7.4 500 Internal Server Error

```bash
sudo journalctl -u car-rental -n 50
```

---

## 8. Quick Reference

| Command | Description |
|---------|-------------|
| `sudo systemctl start car-rental` | Start the app |
| `sudo systemctl stop car-rental` | Stop the app |
| `sudo systemctl restart car-rental` | Restart the app |
| `sudo systemctl status car-rental` | Check app status |
| `sudo journalctl -u car-rental -f` | Follow live logs |
| `sudo systemctl reload nginx` | Reload Nginx config |
| `sudo nginx -t` | Test Nginx config |
| `sudo systemctl restart nginx` | Restart Nginx |

---

## 9. Credentials

| Role | URL | Email | Password |
|------|-----|-------|----------|
| Admin | `/admin/login` | admin@luxedrive.com | AdminLuxe2024! |
| Customer | `/login` | alice@example.com | AlicePass1 |
| Customer | `/login` | bob@example.com | BobPass123 |
| Customer | `/login` | charlie@example.com | CharliePass1 |
| Database |—| dba | abc123 |
| SSH (both) |—| pnc | 1234567 |
